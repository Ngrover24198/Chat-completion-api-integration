from flask_sqlalchemy import SQLAlchemy
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# good practice to initialize the db separately to avoid circular import issues
db = SQLAlchemy()

# initialize Flask-Limiter without attaching to any specific app
limiter = Limiter(key_func=get_remote_address)
