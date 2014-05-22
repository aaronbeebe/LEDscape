import cv2, cv
import socket
import numpy
import datetime
import time

# LEDscape screen geometry
screenWidth = 512
screenHeight = 64

UDP_IP = "127.0.0.1"
UDP_PORT = 9999

# LEDscape packet geometry
subFrames = 2
subFrameHeight = screenHeight / subFrames
subFrameSize = 1 + subFrameHeight*screenWidth*3

# LEDscape message setup
message = numpy.zeros(screenWidth*screenHeight*3 + subFrames, numpy.uint8);
message[0] = 0
message[subFrameSize] = 1

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_SNDBUF,int(screenWidth*screenHeight*1.5))

# Open the video for playback
#cap = cv2.VideoCapture('Coney Island, Luna Park at Night 1905.avi')
cap = cv2.VideoCapture('Daft Punk - Around The World.avi')

fps = cap.get(cv.CV_CAP_PROP_FPS)
frameDelay = 1.0/fps

nextTime = time.time() + frameDelay

while(cap.isOpened()):
    # Get the video frame
    ret, frame = cap.read()

    # If we've reached the end, reset the position to the beginning
    if not ret:
        cap.set(cv.CV_CAP_PROP_POS_MSEC, 0)
        ret, frame = cap.read()

    # Resize the video to be the width that we actually want
    originalHeight = frame.shape[0]
    originalWidth = frame.shape[1]
    originalAspect = float(originalWidth)/originalHeight
    
    desiredWidth = 32*5
    desiredHeight = int(desiredWidth/originalAspect)

    smaller = cv2.resize(frame,(desiredWidth, desiredHeight))
    frame = smaller

    # Copy the image data into the LEDscape format
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    flattenedFrame = frame.reshape(frameHeight, frameWidth*3)

    copyWidth = min(screenWidth, frameWidth)
    copyHeight = min(screenHeight, frameHeight)

    copyLength = copyWidth*3       

    for row in range(0, copyHeight):
        offset = 1 + (row / subFrameHeight)
        messageOffset = (row*screenWidth)*3 + offset

        message[messageOffset:messageOffset+copyLength] = flattenedFrame[row, 0:copyLength]

    # Send the data to the LEDscape host
    sock.sendto(message[0:subFrameSize], (UDP_IP, UDP_PORT))
    sock.sendto(message[subFrameSize:subFrameSize*2], (UDP_IP, UDP_PORT))

    # Delay until it's time to show the next frame.
    while time.time() < nextTime:
       pass

    nextTime += frameDelay
