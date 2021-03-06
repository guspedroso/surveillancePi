# SurveillancePi
	My version of a surveillance system for the raspberry pi.

	- Records on motion detection and uploads to dropbox automatically
	- Sends the user a text message when the motion has been triggered
	- If desired, can specify a time frame of when to record
	- Able to be controlled by voice (Coming soon)

## Installation
	# Pre Req: Raspberry Pi: http://www.amazon.com/CanaKit-Raspberry-Complete-Original-Preloaded/dp/B008XVAVAW
	           USB Web Cam: http://www.amazon.com/Sony-PlayStation-Camera-Bulk-Packaging-Pc/dp/B0072I2240/ref=sr_1_1?ie=UTF8&qid=1443889247&sr=8-1&keywords=ps3+eye
	           Gmail: https://mail.google.com/
	           Dropbox: https://www.dropbox.com/
	           (I listed the rpi and usb cam that I have, others can be used)
	           
	# Perform the steps below in the raspberry pi terminal:

	sudo apt-get update ;
	sudo apt-get upgrade --yes ;
	sudo apt-get install motion --yes ;
	sudo nano /etc/motion/motion.conf ; 
		# make these changes to the file
		daemon on
		width 640
		height 480
		framerate 120
		pre_capture 2
		post_capture 2
		max_mpeg_time 600 # max_movie_time if using raspbian jessie
		ffmpeg_video_codec mpeg4
		locate on # locate_motion_mode if using raspbian jessie
		webcam_localhost off
		control_localhost off
		target_dir /home/pi/surveillancePi/content
		stream_auth_method 1
		stream_authentication YOURUSERNAME:YOURPASSWORD
		webcontrol_authentication YOURUSERNAME:YOURPASSWORD
		
	sudo nano /etc/default/motion ; 
		# make this change to the file
		start_motion_daemon=yes
		
	sudo apt-get install ssmtp mailutils mpack --yes ;
	sudo nano /etc/ssmtp/ssmtp.conf ; 
		# make these changes to the file to your own info
		mailhub=smtp.gmail.com:587
		hostname=ENTER YOUR RPI'S HOST NAME HERE
		AuthUser=YOU@gmail.com
		AuthPass=PASSWORD
		useSTARTTLS=YES
		
	sudo reboot ;
	cd /home/pi ;
	sudo git clone https://github.com/guspedroso/surveillancePi.git ;
	cd /home/pi/surveillancePi ;
	sudo nano surveillancePi.conf ; 
		# read the comments and change settings accordingly :)
		
	sudo git clone https://github.com/andreafabrizi/Dropbox-Uploader.git ;
	sudo chmod +x control.sh Dropbox-Uploader/dropbox_uploader.sh ;
	Dropbox-Uploader/dropbox_uploader.sh ; 
		# follow the instructions.
		
	sudo mkdir /home/pi/surveillancePi/log /home/pi/surveillancePi/content ;
	sudo chgrp motion /home/pi/surveillancePi/content ;
	sudo chmod g+rwx /home/pi/surveillancePi/content ;
	sudo chmod -R g+w /home/pi/surveillancePi/content ;
	crontab -e ;
		* * * * * /usr/bin/python /home/pi/surveillancePi/surveillancePi.py >> /home/pi/surveillancePi/log/surveillancePi.log 2>&1
                00 22 * * * /home/pi/surveillancePi/control.sh start >> /home/pi/surveillancePi/log/control.log 2>&1
                #0 18 * * * /home/pi/surveillancePi/control.sh stop >> /home/pi/surveillancePi/log/control.log 2>&1

	sudo nano ~/.bashrc ; 
		# add some aliases to make it easier to start and stop the motion detection
		# and view logs
		alias mstart='sudo service motion start'
		alias mstop='sudo service motion stop'
		alias mlog='tail /home/pi/scripts/surveillancePi/log/surveillancePi.log'
                alias mclog='tail /home/pi/scripts/surveillancePi/log/control.log'
	
	source ~/.bashrc ;

## Usage
	mstart # start surveillance
	mstop  # stop surveillance
	mlog   # view most recent activity in surveillancePi.log
	mclog  # view most recent activity in control.log
	
	# From the cron jobs we added earlier, we can modify the last two lines to specify a time to start/stop automatically.
	# I have mine set to start at 10 pm everyday, usually because I turn it off when I get home 
	# and don't want to worry about turning it back on to run through the night/morning/work.
	# I didn't specify a time to shut off because times when I get home can vary.
	# If you want to specify a time to shut off, just uncomment the last job and specify a time.
	
Referenced some steps shown here: https://mogshade.wordpress.com/2012/12/23/simple-home-security-with-raspberry-pi-and-dropbox/
