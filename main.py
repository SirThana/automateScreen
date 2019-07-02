import numpy as np #    --> Clean arrays
import cv2 #            --> Video functionality
from mss import mss #   --> Screenshot functionality
from PIL import Image # --> Python Image Library, used in junction with mss
from PIL import ImageChops #Compare images || Image Chop --> Channel - Operations
import platform #       --> Show python version in use
import time #           --> meassure FPS 
import sys #            --> system functionality, read n write to log.txt
import datetime #       --> for logging purposes
__author__  =   "Martijn Zijl"
__version__ =   "1.1"

#TODO
#1. fix compareFrame function to return true, based on image differences || DONE
#2. Write a function that gets the true values from each frame? || DONE
#3. Write logic that reacts to frame changes by using the mouse. click on a position


#   --> Write to the log whenever a change in frame occured, do so with a timestamp
#       Use the compareFrame function to find a difference in frames
#       Perhaps even the numpy array of the image??
def writeLog(lastImage, currentImg):
    write = open("log.txt", "a")
    read = open("log.txt", "r")

    #if there is a difference in frames, log it with the current date & time
    if(compareFrame(lastImage, currentImg) == True):
        write.write(str(datetime.datetime.now()))
        write.write("\n")

        #Save a screenshot of currentImg
        date = str(datetime.datetime.now()) + '.bmp'
        currentImg.save(date)

    #Close read n write
    write.close()
    read.close()


#   --> Get the numpy array of an image
def getNumpy(image):
    return np.array(image)

#   --> Compare frames to find differences in the pixel values using ImageChop from PIL
def compareFrame(lastImage, currentImg):
    diff = ImageChops.difference(currentImg, lastImage)
    if diff.getbbox():
        return True
    return False



print(platform.python_version()) #Show python version
time.sleep(1)

#Set default variables
sct = mss()
last_time = time.time() #Keep track of time before the while loop starts

#Screen resolution used to build a frame with Image
w, h = 800, 800 
monitor = {'top': 30, 'left': 0, 'width': w, 'height': h} #Dict for sct.grab

#Keep track of previous frame
lastImage = Image.frombytes('RGB', (w,h), sct.grab(monitor).rgb)

while True:
    #Make an image out of the sct and monitor values and store it into currentImg
    currentImg = Image.frombytes('RGB', (w,h), sct.grab(monitor).rgb)

    #Draw the image using the cv2 library and the input from img in a numpy array
    #cv2.imshow('screenFeed', cv2.cvtColor(np.array(currentImg), cv2.COLOR_BGR2RGB))
    x = (compareFrame(currentImg, lastImage))
    writeLog(lastImage, currentImg)
    #reset the last image
    lastImage = currentImg


    #Meassure Frame rate per second
    print("FPS: ", 1 / float(time.time() - last_time))
    last_time = time.time() #Reset the timer

    #Break out on q
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        sys.exit()
        break
