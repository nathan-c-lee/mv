"""
# ALL ENDPOINT ROUTES USED IN V1 AND V2
# THAT INTERFACE WITH THE RPI.GPIO MODULE
# AND CONTROL DEVICE MANEUVERING AND OPERABILITY
# HAVE BEEN REPLACED WITH WEBSOCKET ENDPOINTS
# THIS DOCUMENT EXISTS FOR REFERENCE ONLY AND IS 
# NOT USED BY THE APPLICATION IN VERSION 3

import time
import RPi.GPIO as GPIO
from flask import (request, Blueprint, Response, flash,
	redirect, url_for, current_app)
from threading import Thread
from morseview.maneuver.morse import morse as MC


maneuver = Blueprint('maneuver', __name__)

MANEUVER = None #current_app.config["MANEUVER"]
LIGHT = None #current_app.config["LIGHT"]
MORSE = None #current_app.config["MORSE"]

def make_beeps(msg):
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(32, GPIO.OUT)
	for L in msg:
		for d in L:
			if d == ".":
				GPIO.output(32, True)
				time.sleep(.10)
				GPIO.output(32, False)
				time.sleep(.08)
			elif d == "-":
				GPIO.output(32, True)
				time.sleep(.35)
				GPIO.output(32, False)
				time.sleep(.08)
			elif d == "_":
				time.sleep(.20)

		time.sleep(.20)
		print("beeping message........")

	global MORSE
	MORSE = False

	if not LIGHT and not MANEUVER:
		GPIO.cleanup()

def morsecode(message):
	beep_msg = []
	for ch in message:
		try:
			if MC[ch]:
				beep_msg.append(MC[ch])
		except KeyError:
			return False
	
	
	global MORSE
	MORSE = True

	beep_thread = Thread(target=make_beeps, args=(beep_msg, ))
	beep_thread.start()
	
	beep_str = " ".join(beep_msg)
	beep_str = beep_str.replace("_", "|")
	print("##########", beep_msg, beep_str)
	return beep_str


def lightswitch(state):
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(36, GPIO.OUT)
	global LIGHT

	if state == "y":
		LIGHT = True
		current_app.globals.LIGHT = True
		GPIO.output(36, True)
	else:

		GPIO.output(36, False)
		LIGHT = False
		current_app.globals.LIGHT = False
		if not MANEUVER and not MORSE:
			GPIO.cleanup()

def initialize_maneuver(maneuver):

	GPIO.setmode(GPIO.BOARD)

	frontLeft_ControlDriver = [3, 5, 7, 11]
	rearLeft_ControlDriver = [21, 19, 15, 13]
	frontRight_ControlDriver = [8, 10, 12, 16] # wires: 8 yellow, 10 green, 12 blue, 16 purple
	rearRight_ControlDriver = [26, 24, 22, 18]
	 

	all_control_pins = [
		frontLeft_ControlDriver,
		rearLeft_ControlDriver,
		frontRight_ControlDriver,
		rearRight_ControlDriver
	]

	for driver in all_control_pins:
		for pin in driver:
			GPIO.setup(pin, GPIO.OUT)
			GPIO.output(pin, 0)
			print("pin " + str(pin) + " initialized")

	forward_seq = [
		[1,0,0,1],
		[0,0,0,1],
		[0,0,1,1],
		[0,0,1,0],
		[0,1,1,0],
		[0,1,0,0],
		[1,1,0,0],
		[1,0,0,0]	
	]
	reverse_seq = [
		[1,0,0,0],
		[1,1,0,0],
		[0,1,0,0],
		[0,1,1,0],
		[0,0,1,0],
		[0,0,1,1],
		[0,0,0,1],
		[1,0,0,1]
	]

	
	if maneuver == "forward":
		seq = [forward_seq, forward_seq]

	elif maneuver == "reverse":
		seq = [reverse_seq, reverse_seq]

	elif maneuver == "left":
		seq = [reverse_seq, forward_seq]

	elif maneuver == "right":
		seq = [forward_seq, reverse_seq]

	return dict(seq=seq, motors=all_control_pins)


def execute_maneuver(im):
	global MANEUVER
	global LIGHT
	global MORSE

	while MANEUVER:

		for halfstep in range(8):
				for pin in range(4):
					for motor in im["motors"][0:2]:
						GPIO.output(motor[pin], im["seq"][0][halfstep][pin])
					for motor in im["motors"][2:4]:
						GPIO.output(motor[pin], im["seq"][1][halfstep][pin])
				time.sleep(0.001)
		
	if not LIGHT and not MORSE:
		GPIO.cleanup()


@maneuver.route("/mission_control/engage", methods= ["POST"])
def engage_maneuver():

	global MANEUVER
	
	for req in request.form:
		if req == "submit_engage":
			continue
		if req:
			MANEUVER = req
			im = initialize_maneuver(req)
			maneuver_thread = Thread(target=execute_maneuver, args=(im, ))
			maneuver_thread.start()
	
	return Response(status = 204)

@maneuver.route("/mission_control/terminate", methods=["POST"])
def terminate_maneuver():

	global MANEUVER
	
	if request.form.get("terminate") and MANEUVER:
		MANEUVER = False

	return Response(status = 204)

@maneuver.route("/mission_control/devices", methods=["POST"])
def devices():

	lightswitch(request.form.get("lightswitch"))
	msg = request.form.get("morse_text")
	if msg:
		beeps = morsecode(msg.upper())
		if not beeps:
			flash("Sorry, invalid input. Alphanumeric characters and spaces only please.")
			return redirect(url_for("main.mission_control"))
		else:
			flash(f'''Your message '{msg}', is being transmitted by the rover as |{beeps}|!''')
			return redirect(url_for("main.mission_control"))

	return Response(status = 204)
"""