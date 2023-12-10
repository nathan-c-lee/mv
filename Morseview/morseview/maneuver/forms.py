from flask_wtf import FlaskForm
from wtforms import BooleanField, TextAreaField, SubmitField

"""
class MCEngageForm(FlaskForm):
	forward = BooleanField("Forward")
	left = BooleanField("Left")
	right = BooleanField("Right")
	reverse = BooleanField("Reverse")
	submit_engage = SubmitField("Submit")

class MCTerminateForm(FlaskForm):
	terminate = BooleanField("Terminate")
	submit_terminate = SubmitField("Submit")
"""

class Lightswitch(FlaskForm):
	lightswitch = BooleanField("Light")
	#submit_lightswitch = SubmitField("Submit")

class MorseMessage(FlaskForm):
	morse_text = TextAreaField("Morse Code Message:")
	#submit_morse = SubmitField("Send Message")

