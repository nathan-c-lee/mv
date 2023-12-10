import time
from threading import Thread
from flask_socketio import SocketIO
from morseview.socket_flash import sflash


def queue_timer(socketio, app):
	app.globals.ACTIVE_QUEUE = True
	print("timer started")
	print(app.globals.ROVER_QUEUE)

	MINUTES = 14
	SECONDS = 60
	apnd = True
	m = MINUTES

	while m >= 0:
		app.globals.TIME_UNTIL_ROTATE = m + 1
		s = SECONDS
		while s: 
			if m == 0:
				msg = f"T -{s}"
				socketio.emit("flash", sflash("Mission Control - Next", msg, False), broadcast=True)		
			else:
				msg = f"{m + 1} minutes remaining"
				socketio.emit("flash", sflash("Mission Control - Next", msg, False), broadcast=True)				
			#remaining_seconds = (m * 60) + s
			time.sleep(1)
			if app.globals.USER_LEFT > -1:
				if app.globals.USER_LEFT == 0:
					apnd = False
					m = -1
					app.globals.USER_LEFT = -1
					break

				app.globals.ROVER_QUEUE.pop(app.globals.USER_LEFT)
				app.globals.USER_LEFT = -1
				if len(app.globals.ROVER_QUEUE) == 0:
					app.globals.ACTIVE_QUEUE = False
					return
				time.sleep(.02)
				socketio.emit("rotate_users", broadcast=True)

			s -= 1
		m -= 1

	print("timer ended")
	socketio.emit("flash", sflash("Mission Control - Next", f"""T -0
		Have Fun!""", False), broadcast=True)	
	
	driver =  app.globals.ROVER_QUEUE[0]
	app.globals.ROVER_QUEUE.pop(0)
	if apnd:
		app.globals.ROVER_QUEUE.append(driver)
	time.sleep(.02)
	socketio.emit("rotate_users", broadcast=True)
	socketio.emit("flash", sflash("off_MC", "driver changed", redir="/mission_control"), broadcast=True)
	#socketio.emit("flash", sflash("all_authenticated", "All auth flash!!"), broadcast=True)
	#socketio.emit("flash", sflash("all_socketio", "all user flash!!"), broadcast=True)	
	
	app.globals.ACTIVE_QUEUE = False

def main_handlers(socketio, app):

	@socketio.on("connect")
	def connect():
		#print(dir(socketio))
		print("\n----connected----\n")
	
	@socketio.on("disconnect")
	def disconnect():
		print("\n----disconnected----\n")

	@socketio.on("rover_active")
	def rover_active():
		print("rover is active")
		if app.globals.ACTIVE_QUEUE:
			return
		rover_queue_timer = Thread(target=queue_timer, args=(socketio, app))
		rover_queue_timer.start()

		