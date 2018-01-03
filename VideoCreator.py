import cv2
import subprocess
import time
import sys
import numpy as np
import glob
import os
from mutagen.mp3 import MP3
import math

class VideoCreator(object):
    def __init__ (self, noOfFiles, imageType, taskName):
        self.noOfFiles = noOfFiles
        self.imageType = imageType
        self.taskName = taskName
        self.f = open('./'+taskName+'/video/mpg.txt','w+')

    def makeVid(self):
        audio = MP3('./'+self.taskName+'/mp3/audio.mp3')
        mp3Len = audio.info.length
        frameRate = math.ceil(mp3Len/self.noOfFiles)
        test = subprocess.Popen(['ffmpeg','-r','1/'+str(frameRate),'-f','image2','-i','./'+self.taskName+'/image/pic%04d.jpg','-i','./'+self.taskName+'/mp3/audio.mp3','-vcodec','libx264','-acodec','copy','./'+self.taskName+'/'+self.taskName+'.mp4'], stdout=subprocess.PIPE)
        time.sleep(30)
        self.f.close()


    def normalizeImages(self):
        for i in glob.glob('./'+self.taskName+'/image/*'):
            img = cv2.imread(i);
            height,width,channels = img.shape[::]
            if height%2 != 0:
                height -= 1
            if width%2 !=0:
                width -= 1
            img1 = img[0:height,0:width,:]
            cv2.imwrite(i,img1)
