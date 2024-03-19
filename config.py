import os


class Config(object):
    # OpenAI API Key
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
