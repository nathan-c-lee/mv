
# import morseview application
from morseview import create_app #, socket_handlers

# instantiate morseview app and websocket
app, socketio = create_app()
print("morseview app created")

# run morseview app
if __name__ == "__main__":
	print("Run python-flask-socketio morseview app.")
	socketio.run(app, debug=False, host="0.0.0.0")
	#app.run(debug=True, host="0.0.0.0")
	#host="0.0.0.0" for network access