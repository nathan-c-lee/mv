#!/bin/bash

echo -e "\n\nInstalling Morseview\n\n";
echo -e "You will need an Email address for Morseview to send email from. Do not use your personal email for this, it is recommended to create a gmail account for this purpose. You will also need an 'app password' for this account, which Morseview will use to access it. The app password is different than the primary password for the account. If you do not have an app password, please visit https://support.google.com/mail/answer/185833 and follow the instructions to create one for Gmail.\n" | fmt -w 90;
while true; do
    read -p "Email address: " email_address;
    read -p "App password: " app_password;
    echo -e "\nThe email address you would like Morseview to use is: $email_address"
    echo "The app password for $email_address is: $app_password";
    read -p "Is this correct? Y/N: " email_correct;
    if [ -z $email_correct ]; then
        echo;
        echo "Y or N only please"
        continue;
    elif [ $email_correct == "y" ] || [ $email_correct == "Y" ]; then
        break;
    fi
    echo;
done

echo -e "\nWhich port should the Flask Dev server use to serve Morseview?"
echo "Enter preferred port number, or press enter to leave the default port 5000.";
while true; do
    read -p "Flask Dev server port (default 5000): " flask_port;
    if [ -z $flask_port ]; then
        echo -e "\nLeaving default port 5000";
        flask_port=5000;
        echo -e "You will access Morseview locally at http://$(hostname):$flask_port\nOr globally at http://$(curl -s checkip.amazonaws.com):$flask_port\n";
        #echo -n "Is this correct? Y/N: ";
        #read flask_port_correct;
        #if [ $flask_port_correct == "y" ] || [ $flask_port_correct == "Y" ]; then
        #    break;
        #fi
        break;
    elif [[ "$flask_port" =~ ^[0-9]+$ ]]; then
        echo -e "\nYou would like Flask to serve Morseview on port $flask_port\nYou will access Morseview locally at http://$(hostname):$flask_port\nOr globally at http://$(curl -s checkip.amazonaws.com):$flask_port";
        read -p "Is this correct? Y/N: " flask_port_correct;
        if [ $flask_port_correct == "y" ] || [ $flask_port_correct == "Y" ]; then
            break;
        fi
    else
        echo "Sorry, that's not a valid port number. Please enter a valid port.";
    fi
    echo;
done

echo -e "\nWhich port should Motion serve the camera stream to?\nEnter preferred port number, or press enter to leave the default port 8081:";
while true; do
    read -p "Motion server video stream port (default 8081): " stream_port;
    if [ -z $stream_port ]; then
        echo -e "\nLeaving default port 8081";
        stream_port=8081;
        echo -e "Morseview users will access the camera stream locally at http://$(hostname):$stream_port\nOr globally at http://$(curl -s checkip.amazonaws.com):$stream_port\n";
        #echo -n "Is this correct? Y/N: ";
        #read stream_port_correct;
        #if [ $stream_port_correct == "y" ] || [ $stream_port_correct == "Y" ]; then
        #    break;
        #fi
        break;
    elif [[ "$stream_port" =~ ^[0-9]+$ ]]; then
        if [[ $stream_port == $flask_port ]]; then
            echo -e "\n\n!!!!\nStream port cannot be the same as the flask dev server port ($flask_port)\n!!!!";
            continue;
        fi

        echo -e "\n\nYou would like Motion to serve the camera stream on port $stream_port\nYou will access the camera stream locally at http://$(hostname):$stream_port\nOr globally at http://$(curl -s checkip.amazonaws.com):$stream_port";
        read -p "Is this correct? Y/N: " stream_port_correct;
        if [ $stream_port_correct == "y" ] || [ $stream_port_correct == "Y" ]; then
            echo;
            break;
        fi
    else
        echo "Sorry, that's not a valid port number. Please enter a valid port.";
    fi
    echo;
done

read -p "Camera stream left side text (optional): " user_left;
read -p "Camera stream right side text (optional): " user_right;

## install motion
#####################
# go to .deb download archive directory and update package manager
pushd /var/cache/apt/archives
sudo apt update -yy && sudo apt dist-upgrade -yy;
# install motion dependencies
sudo apt-get install autoconf automake autopoint build-essential pkgconf libtool libzip-dev libjpeg-dev git libavformat-dev libavcodec-dev libavutil-dev libswscale-dev libavdevice-dev libwebp-dev gettext libmicrohttpd-dev libcamera-tools libcamera-dev;
# determine motion version
inst_motion_v=$(curl -s https://motion-project.github.io/motion_news.html | grep 'Motion release' | head -1 | awk 'match($0, /[0-9]+\.[0-9]+\.[0-9]+/) {print substr($0, RSTART, RLENGTH)}') && echo "Motion version $version will be installed"
# download latest version
sudo wget https://github.com/Motion-Project/motion/releases/download/release-$inst_motion_v/$(lsb_release -cs)_motion_$inst_motion_v-1_$(dpkg --print-architecture).deb
# install motion dpkg package
sudo dpkg -i $(lsb_release -cs)_motion_$inst_motion_v-1_$(dpkg --print-architecture).deb
popd
#### create venv
python3 -m venv MVenv
source MVenv/bin/activate
pip3 install -r requirements.txt

##### set config files options for motion. needs to actually install motion first tho
#motion_conf="../other/motion-dist.conf"
motion_conf="/usr/local/etc/motion/motion.conf"

    # add new option after match
sed -i '/framerate 15/s/$/\n\nrotate 180/' $motion_conf
sed -i -E '/text_right %Y-%m-%d\\n%T-%q/s/$/\n\ntext_scale 2/g' $motion_conf
sed -i '/stream_localhost on/s/$/\n\nstream_maxrate 30/' $motion_conf
    # replace match
sed -i 's/daemon off/daemon on/g' $motion_conf
sed -i 's|; pid_file value|pid_file /var/run/motion/motion.pid|g' $motion_conf
sed -i 's|; log_file value|log_file /var/log/motion/motion.log|g' $motion_conf
sed -i 's|; target_dir value|target_dir /var/lib/motion|g' $motion_conf
sed -i 's/; video_params value/video_params contrast=2, brightness=52/g' $motion_conf
sed -i 's/width 640/width 1280/g' $motion_conf
sed -i 's/height 480/height 720/g' $motion_conf
sed -i 's/framerate 15/framerate 30/g' $motion_conf
if [ -z $user_left ]; then
    sed -i "s/text_left CAMERA1/; text_left/g" $motion_conf
else
    sed -i "s/text_left CAMERA1/text_left $user_left/g" $motion_conf
fi
if [ -z $user_right ]; then
    sed -i -E 's|text_right %Y-%m-%d\\n%T-%q|; text_right|g' $motion_conf
else
    sed -i -E 's|text_right %Y-%m-%d\\n%T-%q|text_right '"$user_right"'|g' $motion_conf
fi

sed -i 's/text_scale 0/text_scale 2/g' $motion_conf
sed -i 's/movie_output on/movie_output off/g' $motion_conf
sed -i "s/stream_port 8081/stream_port $stream_port/g" $motion_conf
sed -i 's/stream_localhost on/stream_localhost off/g' $motion_conf

##### set envconfig opts
sed -i 's/export STREAM_PORT="YOUR STREAM HERE"/export STREAM_PORT="'"$stream_port"'"/g' envconfig
sed -i 's/export MAIL_USERNAME="YOUR EMAIL HERE"/export MAIL_USERNAME="'"$email_address"'"/g' envconfig
sed -i 's/export MAIL_PASSWORD="YOUR PASSWORD HERE"/export MAIL_PASSWORD="'"$app_password"'"/g' envconfig

# set flask server port
if [ $flask_port != "5000" ]; then
    sed -i 's/socketio.run(app, debug=True, host="0.0.0.0")/socketio.run(app, debug=True, host="0.0.0.0", port="'"$flask_port"'")/g' run.py
fi

## change execute permission for env config and launchmv.sh
chmod +x envconfig
chmod +x launchmv.sh

echo "Morseview has been installed successfully. Type './launchmv.sh' to run Morseview.";
exit
