# MORSEVIEW

### Video Demo

### Contents
- [Overview](#overview)
- [Deployment Considerations](#deployment-considerations)
- [Installation and Setup](#installation-and-setup)
    - [Quick install](#quick-install)
    - [Manual Install](#manual-install)
	    - [OS Notes and RPi.GPIO](#os-notes-and-rpigpio)
	    - [Motion](#motion)
	    - [Virtual Environment](#virtual-environment)
- [File Package Summary](#file-package-summary)
	- [File Tree](#file-tree)
	- [The '/Morseview' root directory](#the-morseview-root-directory)
	- [The '/morseview' subdirectory](#the-morseview-subdirectory)
	- [Subdirectories of '/Morseview/morseview'](#subdirectories-of-morseviewmorseview)
- [User Operation](#user-operation)
- [Physical Device Description](#physical-device-description)
    - [Assembly Instructions](#assembly-instructions)
- [Contact](#thank-you)


## Overview
###### [Top](#contents)
Morseview is a Raspberry Pi single board computer that has been configured as a web controlled rover car with a morse code beeper, a flashlight, and a camera feed. It is intended to be a fun hardware and software configuration project, allowing users to drive a small wifi connected rover over local network or the internet, from any connected device. Multiple users can log in to the application at a time, and Morseview is designed to demonstrate how a simple queue can be implemented when many users seek access to a single device. It is designed to be fun and interesting for all ages, to inspire creativity in it's users, and to be frightening to my cat.

Morseview is a Python Flask web application served directly from the rover that provides users with the ability to create, login to, delete, or recover and change a password for a user account. With a user account, in addition to basic account controls, users are able to post on a message board, and operate the rover controls in a way that shares time equitably among all logged in users. It requires a number of packages and modules for python, including Flask and multiple Flask extensions. Notably among the Flask extensions is Flask-SocketIO, a Flask application wrapper which provides websocket functionality for the application. It relies on "Motion", a webcam sever, which is an external application running along side, for provide the camera stream.

Below you will find installation instructions, a detailed description of all files contained in this repository, a brief summary of user operation, and a summary of the physical device components and assembly.

### Deployment considerations:
###### [Top](#contents)
This code repository has been fully deployed and tested using NGINX and python's 'gunicorn' WSGI module. It could likely also be deployed using some other server such as Apache, or another Flask compatible python WSGI module, but that has not been tested. Complete deployment to a production server is beyond the scope of this README. For the purposes of testing the installation and device, you should use the Flask development server - This will likely be sufficent for general use where you'd want to boot the rover up, drive it around for a while, and then turn it off when you are done. However, if you intend to leave the device online and accessible at all times, or if you are making it available to a large number of users, you should deploy to a production server. There are numerous excellent tutorials and resources available explaining how to deploy a Flask application, you should choose the method best for you.

## Installation and Setup
### Quick Install:
###### [Top](#contents)
You can use the included `installmv.sh` script to quickly install Morseview on a Raspberry Pi device which already has it's WiFi, SSH, and camera interface settings enabled and configured. If you need to configure your Raspberry pi, check the [Manual Install](#manual-install) and [OS Notes](#os-notes-and-rpigpio) below, or the [Raspberry Pi Documentation](https://www.raspberrypi.com/documentation/).

To run `installmv.sh`, open a terminal on your Pi and execute the following code:
```
cd ~
sudo apt update -yy && sudo apt dist-upgrade -yy
sudo apt install git
git clone https://github.com/nathan-c-lee/mv.git
cd Morseview
sudo chmod +x installmv.sh
sudo ./installmv.sh
```
This code navigates to your home directory, updates your apt source repositories and ensures git is installed. Then it clones this repository to your home folder and gives `installmv.sh` executable permission. It then executes `installmv.sh`, which first collects some needed configuration data from the user, then installs `motion` and needed dependencies. Next it sets up a python environment and installs needed python packages, before setting the `envconfig` and `motion.conf` files with the previously collected configuration data, and giving these files executable permission as well. Once finished, Morseview is fully installed, and you can now run the application on the Flask development server.

Execute
```
./launchmv.sh
```
to start Morseview, then from a connected network device, go to <http://raspberrypi:5000> (or whichever port you specified during install) to use the application and drive the rover! You can also access the application from the global internet at http://\[your-global-ip]:\[your-specified-port]. Use `curl checkip.amazonaws.com` in your terminal if you are unsure of your global ip. For example if your ip is 123.456.789.012 and you've specified port 9999, you would access morseview at http://123.456.789.012:9999. If you're having issues connecting, you may need to configure your router to send unsolicited external traffic to the pi. Consult your router's documentation for more info.

### Manual Install:
#### OS Notes and RPi.GPIO
###### [Top](#contents)
Raspberry Pi OS (formerly Raspbian) is the primary OS for RPi devices, and this project was developed running on Raspberry Pi OS. It is possible to run other debian based linux operating systems on RPis, such as Ubuntu, but RPi OS's python comes with RPi.GPIO library pre installed, which is needed for this application. You can likely use any RPi compatable debian linux you like, but keep in mind that this code has only been run and tested on RPi OS, and you will have to install RPi.GPIO python library if you use a different OS. If you are setting up with a new Pi, before assembling the rover, you will need to boot it with peripheral I/O connected and configure it. You will need to make sure the operating system is installed and setup to your liking and that it's configured to auto connect to your wifi, the camera module is connected, and that SSH login and the camera module are both enabled.
Use:
```
sudo raspi-config
```
to configure the raspberry pi's SSH and WiFi settings (found under `System Options`), and the camera module settings (found under `Interface Options`).

If you're NOT running Raspberry Pi OS, make sure to install RPi.GPIO using pip. This should be a global installation to your system python, not in a virtual environment. We'll use a virtual environment later for all other python packages, but the RPi.GPIO module is for interacting with the GPIO hardware on Raspberry Pi devices, comes already installed on RPi OS by default, and so it's a good idea to have it generally available to your Raspberry Pi's python interpreter. Again, this step is ONLY for operating systems OTHER than Raspberry Pi OS. Otherwise, ignore this step. From a terminal window, execute:
```
pip3 install RPi.GPIO
```

Ensure the device is assembled and the operating system, WiFi settings, SSH login and camera module are properly setup, you are able to log in to the Pi remotely, and the RPi.GPIO python module is installed. Once this is complete you can proceed to install Motion, configure the application environment, and install the necessary python packages and libraries.

#### Motion
###### [Top](#contents)
Motion is a feature rich, highly configurable multi-source video streaming server, recorder, and motion detection software with capabilities far exceeding the scope and requirements of this project. It is worth exploring for it's own sake, however for our purposes we will be using it simply as a camera stream providing a first person driving view to the user. For more information about Motion software, documentation and configuration options, visit <https://motion-project.github.io/>.

Motion v4.4.0 is available via `apt`, this may be enough for purposes of Morseview. However, It is recommended to install the latest version for Morseview. To install the latest version (currently 4.6.0), follow the directions below. Note, these instructions may not work on systems other than raspberry pi. If you are using another system, use `sudo apt install motion` instead, or consult motion documentation for install and configuration instructions specific to your system.

First, we will use `apt` to install needed dependencies, then use the `dpkg` debian package manager to install motion. To start, update your package manager, and install needed dependencies for Motion:
```
sudo apt update -yy && sudo apt dist-upgrade -yy
sudo apt-get install autoconf automake autopoint build-essential pkgconf libtool libzip-dev libjpeg-dev git libavformat-dev libavcodec-dev libavutil-dev libswscale-dev libavdevice-dev libwebp-dev gettext libmicrohttpd-dev libcamera-tools libcamera-dev
```
Next, determine the latest version of Motion.
Use this command:
```
inst_motion_v=$(curl -s https://motion-project.github.io/motion_news.html | grep 'Motion release' | head -1 | awk 'match($0, /[0-9]+\.[0-9]+\.[0-9]+/) {print substr($0, RSTART, RLENGTH)}') && echo "Motion version $version will be installed"
```

Finally, download and install Motion:
```
sudo wget https://github.com/Motion-Project/motion/releases/download/release-$inst_motion_v/$(lsb_release -cs)_motion_$inst_motion_v-1_$(dpkg --print-architecture).deb

sudo dpkg -i $(lsb_release -cs)_motion_$inst_motion_v-1_$(dpkg --print-architecture).deb
```

Motion is now installed, but still needs to be configured. To configure motion, you will need to edit the `motion.conf` file. Depending on which version of Motion you have installed, the motion.conf file will be found in different locations.
in version 4.6.0 or newer, the filepath for this file is `/usr/local/etc/motion/motion.conf`

Use `nano` to edit `motion.conf`:
```
sudo nano /usr/local/etc/motion/motion.conf
```

Look through the file, change the following values and remove any ";" characters preceding any of the following options in `motion.conf`:

- `daemon on`
- `pid_file /var/run/motion/motion.pid`
- `log_file /var/log/motion/motion.log`
- `target_dir /var/lib/motion`
- `video_params contrast=2, brightness=52` NOTE: adjust the contrast and brightness values to your liking. These values worked well for the picam v2.
- `width 1280`
- `height 720`
- after the height option, add a `rotate 180` option. `rotate` is not present in the distribution .conf file, it must be added.
- `framerate 30`
- `text_left MORSEVIEW` *Optional
- `text_scale 2`
- `movie_output off`
- `stream_port 8081` *This is the default. Leave as is or change to your preffered port.
- `stream_localhost off`
- after stream_localhost option, add a `stream_maxrate 30` option. It must be added.

Now press `Ctrl + s` to save the changes to `motion.conf` and press `Ctrl + x` to exit nano.

Motion is now ready to use.

To run motion, execute:
```
sudo motion
```

You should now be able to access the camera stream from your browser. If you used the default stream_port option, you can go to <http://raspberrypi:8081/> from any device on the same local network as the pi and you should be able to see the camera stream. Otherwise, adjust the URL to reflect your chosen port. To view from outside your network, you can use your global ip in the URL instead of `raspberrypi`. Use command `curl checkip.amazonaws.com` to see your global ip address.

#### Virtual Environment
###### [Top](#contents)

Once you have Motion installed, clone the Morseview project repository to the desired location on your Pi rover device. In this example we are installing it in the home folder.
Run the following command to clone the repository:
```
cd ~
git clone https://github.com/nathan-c-lee/mv.git
```

Next, create a python virtual environment with venv in the project directory, (or your own environments directory if you prefer) and activate it.

In your terminal, navigate to the desired location, then create and activate your virtual environment with:
```
cd mv
python -m venv MVenv
source MVenv/bin/activate
```

You will also need to set some configuration settings for your environment, found in the `envconfig` file. In order for users to be able to reset their password, your rover will need an app password for an email service. You can use any email provider you like, but this code was designed and tested using gmail as the mail provider. Instructions for how to create an app password for a gmail account can be found here: https://support.google.com/mail/answer/185833

Once an app password has been created, update the MAIL_USERNAME and MAIL_PASSWORD variables in the `envconfig` file with these credentials. You can use
```
nano envconfig
```
to edit the file from your terminal, then press `Ctrl + s` to save your changes, and `Ctrl + x` to exit nano.

If you are using a mail cilent other than gmail, you may also need to set the MAIL_PORT, MAIL_SERVER, and MAIL_USE_TLS variables accordingly - otherwise, the default values provided should work with gmail.

Once you have made these changes to `envconfig`, you will need to activate them in your environment. Run
```
source envconfig
```
from your terminal to activate your email configuration changes in your environment.

Now that your virtual environment is created, configured, and activated, it's time to install Flask and other python dependencies. You can use the included `requirements.txt` file to install dependencies with pip using the -r flag.

```
pip3 install -r requirements.txt
```
With all python dependencies installed, the manual installation process is complete! Morseview is now fully installed and ready to run!

To run Morseview, execute the following command:
```
python run.py
```

## File Package Summary
###### [Top](#contents)

The following directory tree represents all files contained in this repository which are considered necessary to install, launch, and use morseview, as well as this README.

### File Tree
###### [Top](#contents)
```
./Morseview
├── envconfig
├── gpiocu.py
├── installmv.sh
├── launchmv.sh
├── README.md
├── requirements.txt
├── run.py
├── /morseview
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── socket_flash.py
│   ├── /errors
│   │   ├── handlers.py
│   ├── /main
│   │   ├── routes.py
│   │   ├── socket_handlers.py
│   ├── /maneuver
│   │   ├── forms.py
│   │   ├── morse.py
│   │   ├── routes.py
│   │   ├── socket_handlers.py
│   ├── /posts
│   │   ├── forms.py
│   │   ├── routes.py
│   ├── /static
│   │   ├── control_panel.js
│   │   ├── main.css
│   │   ├── /assets
│   │   │   ├── exit.svg
│   │   │   ├── menu.svg
│   │   ├── /profile_pics
│   │   │   ├── default.jpg
│   ├── /templates
│   │   ├── layout.html
│   │   ├── ... (11 additional .html files)
│   │   ├── /errors
│   │   │   ├── 403.html
│   │   │   ├── 404.html
│   │   │   ├── 405.html
│   │   │   ├── 500.html
│   ├── /users
│   │   ├── forms.py
│   │   ├── routes.py
│   │   ├── utils.py
```
### The '/Morseview' root directory
###### [Top](#contents)
In the root `/Morseview` directory of the package, there are
seven files and one subdirectory, also called `/morseview`. These files are `envconfig`, `gpiocu.py`, `installmv.sh`, `launchmv.sh`, `README.md`, `requirements.txt` and `run.py`.

`installmv.sh` is a simple BASH shell script that collects a few configuration data points and inserts them in the `envconfig` file, then installs motion using the steps given in the manual install instructions, creates and activates a virtual env, and pip installs all the dependencies found in the `requirements.txt` file.

`launchmv.sh` is also a simple BASH shell script that activates the already installed application environment, configures the application environment with data from the `envconfig` file, and finally starts the app by invoking python on the `run.py` file.

`envconfig` is a BASH script that exports several variables to the environment. These are application variables which are set either by the user, the installer, or are generated when `envconfig` is called. Most of these variables are authentication and configuration information needed for morseview to use an email account. It also contains the user content database URI, and the application's instance specific SECRET_KEY.

`gpiocu.py` is a python script which initializes all the gpio header pins and sets them to 0 output, then runs `RPi.GPIO.cleanup()` to clear out the GPIO configuration and "free" the GPIO device for the next application. It is invoked by `launchmv.sh` after the application has finished.

`requirements.txt` is a `pip freeze` list of all the needed python libraries which must installed in your environment. It is used by `installmv.sh` or invoked using pip.

`README.md` is this document that you are currently reading.

`run.py` is the head of the python flask application and contains the app's `if __name__ == "__main__":` statement. `run.py` simply imports the application data from the `/morseview` subdirectory, and executes it.

### The '/morseview' subdirectory
###### [Top](#contents)
The `/morseview` subdirectory contains all the remaining application data. In this directory, you will find four files `__init__.py`, `config.py`, `models.py`, and `socket_flash.py`. You will also find seven subdirectories `/errors`, `/main`, `/maneuver`, `/posts`, `/static`, `/templates` and `/users`.

`__init__.py` is where the application context and websocket objects are defined, in the `create_app()` function, which is imported and called by `run.py`. The `create_app()` function returns two objects: `app`, and `socketio`. `app` is the Flask application context object, and `socketio` is the wrapper object who's method `run()` takes `app` as an argument. `__init__.py` instantiates a number of supporting objects as well, these are the `db` SQLAlchemy database object for user data and content, the encryption `bcrypt` object, the `login_manager` object, and `mail` object. These are initialized by `create_app.py` as part of the `app` object. Environment data and application global variables are imported from the `Config` and `Globals` classes defined in `config.py`, and initialized on the `app` object. All of the app route blueprints, error handler blueprints, and websocket handlers are imported from their various subdirectories and registered to the app or activated in `create_app()`. There are three route blueprints, one error handler blueprint, and two groups of websocket handlers.

`config.py` defines two object classes `Config` and `Globals`. `Config` pulls previously defined environment variables from the OS, and `Globals` defines some application wide variables which are shared across routes and across users. These are related to the position of each user in queue, the timing of the next queue rotation, and the state of the various rover controls. Both classes are imported by `__init__.py` and used by `create_app()`.

`models.py` defines a `User` class and `Post` class for the app's `login_manager` object. The `User` and `Post` classes are used to create SQL queries for the `login_manager` to pass to the SQLAlchemy `db` object when the user creates or modifies user account information, or when a user creates or modifies a post.

`socket_flash.py` defines a single function `sflash()` which is used as part of a way to provide 'flash' style messages to the user, outside the normal flask application context where flask's `flash()` function is unavailable. `flash()` will only work within the flask application context, in a route definition. In order to 'flash' a message to the user in a similar way from a socketio emit (which is part of the socketio wrapper), I have defined `sflash()` which uses python's `xml.dom` API to dynamically generate the needed html code, which is then returned as part of a JSON object, and can be emitted back to the client to display to the user.

### Subdirectories of '/Morseview/morseview'
###### [Top](#contents)
The subdirectories of `/Morseview/morseview` are `/errors`,`/main`,`/maneuver`,`/posts`,`/static`,`/templates` and `/users`. These subdirectories group all the remaining application files according to their role within the app. For example, not all application routes are defined in the same file. Those routes which define actions for interacting with the login_manager, such as account creation, log in, log out, and account management are found in the `/users/routes.py` file. Those routes related to main pages and general navigation within the site, the landing page, info page, and rover control page are defined in `/main/routes.py`. WTForms classes are handled similarly, with definitions for forms related to the login_manager found in `/users/forms.py` and forms for making posts found in `/posts/forms.py`.

There are three important kinds of `.py` files found in the `/main`, `/maneuver`, `/posts` and `/users` subdirectories. These are routes files, forms files and socket_handlers files.

The routes files are `/main/routes.py`, `/posts/routes.py`, and `/users/routes.py`. These files define all of the application routes, which are imported by `/morseview/__init__.py` as blueprints and registered to the app context by `create_app()`. As mentioned in the example above, routes in the `/main/routes.py` file define all routes related to the site's main pages. The `/posts/routes.py` file defines all routes related to posting on the message board, and the `/users/routes.py` file defines all routes for interacting with the login_manager. Across these files, 15 functions are defined for 17 total routes.

The forms files are `/maneuver/forms.py`, `/posts/forms.py`, and `/users/forms.py`, and define all classes used by WTForms for creating webforms on the various site routes. `/maneuver/forms.py` defines only two form classes for interacting with the rover's physical devices, `/posts/forms.py` only one for posting to the message board, and `/users/forms.py` defines the remaining five form classes needed for interacting with the login_manager.

There are two socket handler files, `/main/socket_handlers.py` and `/maneuver/socket_handlers.py`. These define the websocket endpoints for various emits from both the client and server. the `/main/socket_handlers.py` file defines three socket endpoints and supporting functions for handling the "rover queue" and rotating users through the queue. `/maneuver/socket_handlers.py` defines four socket endpoints and supporting functions for handling the operation of the rover's movement and hardware devices.

In addition to socket handlers, forms, and routes pages, there is a `utils.py` file found in the `/users` subdirectory, and a `morse.py` file found in the `/maneuver` subdirectory. `utils.py` defines two functions imported and used by `/users/routes.py`, and `morse.py` contains a single dictionary which associates uppercase alphanumeric characters and the " " character with morse code dots and dashes, notated as "." and "-". This dictionary is imported by `/maneuver/socket_handlers.py` and used by the "morse" socket endpoint there.

This covers all the contents of the `/main`, `/maneuver`, `/posts` and `/users` subdirectories. The remaining subdirectories `/errors`, `/static` and `/templates` contain additional files.

The `/errors` subdirectory contains a single file `handlers.py` which contains four error handling endpoints, similar to routes. These are imported as a blueprint and registered to the app context by `__init__.py`.

The `/templates` subdirectory contains all the HTML template files used by flask and jinja2 to return to the client. It also contains one subdirectory `/errors`. The primary file is `layout.html` which is the general layout of all the pages on the site. The 11 additional files here are `about.html`, `account.html`, `create_post.html`, `home.html`, `login.html`, `mission_control.html`, `post.html`, `register.html`, `reset_request.html`, `reset_token.html` and `user_posts.html`. These 11 files are used by jinja2 to extend `layout.html` when flask "renders" http responses to client requests on the various flask routes. The `/templates/errors` directory contains those extensions of `layout.html` that are rendered by error handlers. Of special note here, `layout.html` and `mission_control.html` both contain a significant amount of embedded JavaScript. This is where socket listeners for `sflash()` emits and queue rotation triggers are defined. For now, some parameters of these functions are passed by being rendered in via jinja2. For example, in one instance an evaluation of `if ("True" === "True")` is made. The `"True"` string on the left of the evaluator is rendered by jinja2 server side, and is coded in the template as `"{{ current_user.is_anonymous }}"`. Depending on the user's login status, this is sometimes rendered as `"False"`, and the evaluation is then `if ("False" === "True")`, and the condition fails. This JavaScript is necessarily embeded directly within `<script>` tags in the html in order for jinja2 to be able to render its variables in it. This needs to be fixed and this 'special note' needs to disappear.

Finally, the `/static` subdirectory contains the static data files used by the site, and two subdirectories `/assets`, and `/profile_pics`. The `/assets` directory contains two `.svg` files which are displayed in the html returned to the client. The `/profile_pics` directory contains the default user profile image, `default.jpg`, and is where user uploaded profile images with randomized file names are stored. The `style.css` stylesheet file contains responsive css style rules for the site. `control_panel.js` contains the socket emit definitions for all the hardware controls for driving the rover.

### User operation
###### [Top](#contents)

Morseview is simple to operate. Once the RPi is plugged in and turned on, as well MB102 power supply to the motors, if configured properly it should connect to your wifi network. From there, login via ssh to the Pi from your computer, activate your flask virtual environment, run the `envconfig` configuration script, and start morseview with `python run.py` in the morseview application directory. Alternatively, you can run the `launchmv.sh` script included in the repo to activate the environment, run the configuration script, and launch the application all in one. You should then be able to connect to `raspberrypi:5000` on your local network via your browser's address bar, and see the Morseview web application user interface.
\
Here, you can read posts on the `comms` page, read info about the device on the `info` page, view the camera stream on the `MISSION CONTROL` page, register a new account on the `register` page, or login to an existing account on the `AUTHENTICATE` page. Once logged in, users can view and edit their account info, create new posts on the comms page or edit their own existing posts, and pilot the the Morseview rover from the MISSION CONTROL page. The user is also placed in the "rover queue" when they log in. If there is only one user in the rover queue, that user will drive the rover indefinitely. When a second user logs in, that user is placed next in the rover queue and a 15 minute "queue timer" is started. Each additional user that logs in is placed in the rover queue, but there is only one timer, which starts when the rover queue is greater than one user. When the queue timer has elapsed, the queue positions rotate up one position, and the first in queue is moved to the end of the queue. This way, if more than one user is logged in, the first user to login has access to the control panel, and the next user then will gain access after the first users time has expired. The user who is taking the first position in queue is automatically redirected to the MISSION CONTROL page where they are able to then able to drive the rover, and remaining users are informed of their remaining wait time.


## Physical Device Description
###### [Top](#contents)

The Morseview rover consists of several physical components, which are arranged in such a way that the entire device can be easily disassembled and its parts re-purposed.

* ### Parts List:
    * Raspberry Pi 4 8gb
    * Aluminium heatsink and enclosure
    * 30x30x7mm 5v cpu fans
    * Raspberry Pi camera module
    * White LED
    * Active buzzer
    * 4x 28BYJ-48 stepper motors
    * 4x ULN2003 driver boards
    * MB102 breadboard power supply
    * 2.1a 5v Power Bank
    * M usb to M usb cable
    * M usb to M usb-c cable
    * 2x 5 pin headers
    * Lots of F to F dupont wires
    * 3D printed vehicle frame / mounting platform
    * 4 Wheels and wood dowel axels
    * Camera mount dowel
    * Styrofoam block
    * Rubber band
    * Office clip


#### Assembly instructions
###### [Top](#contents)
![morseview_rover.png](https://raw.githubusercontent.com/nathan-c-lee/somerepo/master/mv.png)


Morseview's physical components are affixed to one another in such a way that they form a simple 4 wheeled rover. To assemble the morseview rover, first fasten the heatsink / enclosure blocks around the Raspberry Pi with M2.5 hex head screws. The fan is then attatched with hex screws to the enclosure, and the fans ground wire is mapped to the Pi's GPIO pin 6, and it's positive maps to pin 4 for continuous 5v power. The Pi and motor drivers are then mounted to the vehicle frame with M2.5 screws, while the motors themselves, and the power bank, are mounted with zipties, to the corners and bottom respectively. The Pi's camera module interfaces directly to the Pi on a dedicated header (not the GPIO header), and is then mounted to the camera mount dowel with a rubber band. The camera dowel is hot glued to the vehicle frame so that the camera is oriented toward the front. Both of the 5 pin headers are soldered on the back such that each is a single electrically conductive 5 pin terminal. The terminals are hotglued directly to the top of the mounting platform, as well as the styrofoam block, which the MB102 board's underside pins are firmly pressed into. Four dupont wires are office clipped to the side of the mounting platform, and the LED light is connected to 2 of them, and the active buzzer to the other 2. The wheels are hot glued to the dowel axels, which are then each hotglued to the stepper motor axels. The usb-c cable connects the Pi's main power input to the power bank, while the remaining M to M usb cable connects one of the Pi's usb outputs to the MB102 power supply. Dupont wires are used to connect the MB102's 5v positive and ground terminals to the 5 pin terminals on the mounting platform - one ground to one terminal, one positive to the other. From there, one positive and one ground wire is run to each of the motor drivers.

*Note: The power configuration for the stepper motor drivers is configured through the Pi's USB output and MB102 as a precaution against blowing out the Pi's GPIO. *

The control wires for stepper motors themselves plug directly into the driver boards, and the control wires for the drivers are mapped to the GPIO as follows:

#####  front left:
    GPIO pins [3, 5, 7, 11] to FL driver pins [1, 2, 3, 4]
#####   front right:
    GPIO pins [8, 10, 12, 16] to FR driver pins [4, 3, 2, 1]
#####  rear left:
    GPIO pins [13, 15, 19, 21] to RL driver pins [4, 3, 2, 1]
#####  rear right:
    GPIO pins [18, 22, 24, 26] to RR driver pins [1, 2, 3, 4]

This configuration is important as you'll notice the left's mapping is 'opposite' the right's. This makes the code more ergonomic later on, as the same step sequence willcorrespond to the necessary clockwise spin on the left, and counter-clockwise on the right for forward motion. Finally, the wires connected to the buzzer and LED are connected to the GPIO where the buzzer's negative terminal maps to GPIO pin 30, its positive to pin 32, and the LED's negative (cathode) maps to pin 34, and it's positive (anode) maps to pin 36. This completes Morseview's hardware configuration.

## Thank You
###### [Top](#contents)
Huge thanks to my family for allowing me the time to put into making this project a reality, David Milan and the staff at CS50, and to Corey Schafer, who's Flask and Python tutorials on YouTube have been instrumental in solidifying my understanding of Flask and Python, and to my Dad, the greatest teacher I've ever had and the best programmer I know. Thank you all.

### Contact
Please feel free to email me with any comments or questions about this project at [nathan.christopher.lee@gmail.com](mailto:nathan.christopher.lee@gmail.com)
