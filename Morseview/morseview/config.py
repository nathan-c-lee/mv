import os

class Config:
	SECRET_KEY = os.environ.get("SECRET_KEY")
	SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
	MAIL_SERVER = os.environ.get("MAIL_SERVER") #'smtp.gmail.com'
	MAIL_PORT = int(os.environ.get("MAIL_PORT")) #587
	MAIL_USE_TLS = bool(os.environ.get("MAIL_USE_TLS")) #True
	MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
	MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
	STREAM_PORT = str(os.environ.get("STREAM_PORT")) #8081

class Globals:
	ROVER_QUEUE = []
	ACTIVE_QUEUE = None
	TIME_UNTIL_ROTATE = 0
	USER_LEFT = -1
	LIGHT = None
