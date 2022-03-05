# speech_jammer
A simple speech jammer using auditory delayed feedback for raspberry pi

This script is intended to work on a Raspberry Pi device running Raspberry Pi OS. 
You'll also need a usb sound card with a microphone, headset and any type of bluetooth gamepad/controller to make it work.

# instructions
-Install EVDEV and find your bluetooth controller name and button codes using this tutorial: https://raspberry-valley.azurewebsites.net/Map-Bluetooth-Controller-using-Python/
-Disable HDMI and default audio output on Raspberry Pi OS so the script can correctly find your USB sound card. Alternatively you can change the hwid of your audio output in the script.
-Put the script to rc.local if you want it to run at startup, without a display. In this case you can safely shutdown the raspberry by pressing both shutdown buttons you defined on your bluetooth controller for 5 seconds.
