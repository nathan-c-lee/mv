
# Flask imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_socketio import SocketIO

# application config import
from morseview.config import Config, Globals

# instantiate db, encryption, login manager, and mail objects
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()

# configure login manager
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"

# define application
def create_app(config_class=Config):
	# instantiate Flask
	app = Flask(__name__)
	# configure Flask
	app.config.from_object(Config)
	app.globals = Globals

	# initialize app db, encryption, mail, and login manager.
	db.init_app(app)
	bcrypt.init_app(app)
	mail.init_app(app)
	login_manager.init_app(app)

	# instantiate socket server
	socketio = SocketIO(app)

	# import route and error blueprints
	from morseview.users.routes import users
	from morseview.posts.routes import posts
	from morseview.main.routes import main
	#from morseview.maneuver.routes import maneuver
	from morseview.errors.handlers import errors

	# register blueprints
	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(main)
	#app.register_blueprint(maneuver)
	app.register_blueprint(errors)

	# import websocket handlers
	from morseview.main.socket_handlers import main_handlers
	from morseview.maneuver.socket_handlers import maneuver_handlers

	# activate websocket handlers
	main_handlers(socketio, app)
	maneuver_handlers(socketio, app)

	# return application object
	return app, socketio
