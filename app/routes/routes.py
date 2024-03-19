import os
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI
from flask import Blueprint, request, current_app, render_template

from app.extensions import db, limiter
from app.models.models import chatApp

bp = Blueprint('routes', __name__)


@bp.route("/")
def index():
    return render_template("chatapp/index.html")


@bp.route("/openai-completion/", methods=["POST"])
@limiter.limit("20 per minute")  # Apply a rate limit to this route
def get_completion():
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return {"error": "No prompt provided"}, 400

    try:
        client = OpenAI(api_key=current_app.config["OPENAI_API_KEY"])
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        completion = response.choices[0].message.content

        chat_log = chatApp(
            prompt=prompt,
            completion=completion,
            timestamp=datetime.now()
        )
        db.session.add(chat_log)
        db.session.commit()

        return {"completion": completion}
    except Exception as e:
        return {"error": "API Failed", "Error details": str(e)}, 500
