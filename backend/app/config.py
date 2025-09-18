import os
from dotenv import load_dotenv
base = os.path.dirname(__file__)
env_path = os.path.join(base, '..', 'instance', '.env')
load_dotenv(dotenv_path=env_path)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f"sqlite:///{os.path.join(base, '..', 'data.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AI_API_KEY = os.environ.get('AI_API_KEY')
