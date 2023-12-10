
from flask import render_template, request, Blueprint, current_app, flash
from flask_login import current_user
from morseview.models import Post
from morseview.maneuver.forms import Lightswitch, MorseMessage

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
	page = request.args.get("page", 1, type=int)
	posts = Post.query.order_by(Post.date_posted.desc())\
		.paginate(page=page, per_page=5)
	return render_template("home.html", posts=posts, title="Comms")


@main.route('/about')
def about():
	return render_template("about.html", title="Info")


@main.route('/mission_control', methods=["GET", "POST"])
def mission_control():

	#engage_form = MCEngageForm()
	#terminate_form = MCTerminateForm()
	lightswitch_form = Lightswitch()
	morsecode_form = MorseMessage()

	ROVER_QUEUE = current_app.globals.ROVER_QUEUE
	STREAM_PORT = current_app.config["STREAM_PORT"]
	lightswitch_form.lightswitch.data = current_app.globals.LIGHT


	if current_user.is_anonymous:
		current_user.is_pilot = False;
		title = "Mission Control"
	else:
		for i in range(len(ROVER_QUEUE)):
			if ROVER_QUEUE[i] == current_user.id:
				
				if i == 0:
					current_user.is_pilot = True
					title = "Mission Control - Pilot"
				else:
					current_user.is_pilot = False
					title = "Mission Control - Next"
					
				current_user.queue_position = i
				break

	if current_user.is_authenticated \
		and not current_user.is_pilot \
		and current_user.queue_position >= 2:
			title = "Mission Control - Waiting"
			wait_time = ((current_user.queue_position - 1) * 30) + current_app.globals.TIME_UNTIL_ROTATE
			flash(f"There are other users in queue ahead of you, you could be waiting up to {wait_time} minutes.")

	return (render_template("mission_control.html", title=title, 
		lightswitch_form=lightswitch_form, morsecode_form=morsecode_form,
		legend="CONTROL MORSEVIEW", video_port=":" + STREAM_PORT))
