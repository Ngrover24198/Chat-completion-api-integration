import os
import json
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from flask import Blueprint, request, current_app, render_template

from app.extensions import db, limiter
from app.models.models import chatApp, chatSession

bp = Blueprint('routes', __name__)


@bp.route("/")
def index():
    # index template for the chat application
    return render_template("chatapp/index.html")


@bp.route("/openai-completion/", methods=["POST"])
@limiter.limit("10 per minute")  # rate limit to openai-completion api route
def get_completion():
    data = request.get_json()
    prompt = data.get("prompt")
    user_id = data.get("user_id")

    # validate the input
    if not prompt or not user_id:
        return {"error": "Invalid Input! - no prompt or user_id provided"}, 400

    # retrieve or initialize the conversation history for the user from db
    user_session = chatSession.query.filter_by(user_id=user_id).first()
    if user_session:
        conversation_history = json.loads(user_session.conversation_history)
    else:
        conversation_history = []
        user_session = chatSession(
            user_id=user_id, conversation_history=json.dumps(
                conversation_history)
        )
        db.session.add(user_session)

    try:
        client = OpenAI(api_key=current_app.config["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=conversation_history +
            [{"role": "user", "content": prompt}]
        )
        completion = response.choices[0].message.content

        # updating the conversation history and database records
        conversation_history.append({"role": "user", "content": prompt})
        conversation_history.append(
            {"role": "assistant", "content": completion}
        )
        # updating the db record with the new conversation history in chat_session table
        user_session.conversation_history = json.dumps(conversation_history)
        db.session.commit()

        # updating the db record with new prompt and completion in chat_app table
        chat_log = chatApp(
            user_id=user_id,
            prompt=prompt,
            completion=completion,
            timestamp=datetime.now()
        )
        db.session.add(chat_log)
        db.session.commit()

        return {"user_id": user_id, "completion": completion}
    except Exception as e:
        return {"error": "API Failed", "Error details": str(e)}, 500
