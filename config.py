import os


# this is the configuration file, that's usually helpful in managing multiple environment variables and definition
class Config(object):
    # OpenAI API Key
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
