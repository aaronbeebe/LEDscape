Getting Started
===============

Here's a brief list of steps:

First, we need to install the set up the Debian environment:

    apt-get update
    sudo apt-get install git build-essential
    sudo apt-get install libavformat-dev
    sudo apt-get install x264 v4l-utils ffmpeg
    sudo apt-get install libcv2.3 libcvaux2.3 libhighgui2.3 python-opencv opencv-doc libcv-dev libcvaux-dev libhighgui-dev

    (disable HDMI capes)

Next, set up LEDscape: 

    git clone git@github.com:osresearch/LEDscape.git
    cd LEDscape
    make

To run the matrix listener:

    sudo su
    cd LEDscape
    echo "CAPE-BONE-OCTO" > /sys/devices/bone_capemgr.9/slots
    bin/matrix-udp-rx sign.config &

And finally, the video player:

    Python test.py
    
