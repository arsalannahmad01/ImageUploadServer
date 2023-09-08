from flask import Flask
from config.settings import Config

app = Flask(__name__)
app.config.from_object(Config)

from app.routes import routes  # Import your API route modules