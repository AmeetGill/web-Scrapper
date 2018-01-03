import os
import subprocess
import sys
import requests
import bs4
from bs4 import BeautifulSoup
import re
import cv2
from gtts import gTTS
import ssl
import time

# import my files
from Parser import Parser
from TTSEngine import TTSEngine
from VideoCreator import VideoCreator
from TagsCreator import TagsCreator
import glob

req = requests.get('http://www.motortrend.com/')

soup  = BeautifulSoup(req.content,'html.parser')
#print soup
print "parsing home page"
temp = 1
#ffmpeg -r 1/10 -f image2 -i pic%04d.jpg -i 1.mp3 -vcodec libx264 -acodec copy out.mp4
for article in soup.findAll('article'):
    print '----------------------------------------------------------'
    a = article.find('a',attrs={'data-sobject-id':'CategoryTag'})
    print str(a.text.strip())
    if(a.text.strip()=="News" or a.text.strip()=="Spy Photos" or a.text.strip() == "Concept Cars"):
        print "true"+'\n\n'
    else:
        continue
    img = article.find('img')
    imageLink = img['src']
    if temp==1:
        temp = 2
        continue
    articleName = article.h2.a.text.strip().encode('utf8')

    articleLink = article.h2.a['href']
    print 'fount task : '+articleName
    print articleLink
    try:
        parser = Parser(taskName = articleName.decode('unicode_escape').encode('ascii','ignore'), articleLink = articleLink, imageLink = imageLink)
        fExt,noOfFiles = parser.visit()
    #fExt = "jpg"
    #noOfFiles = 16
    except OSError:
        continue

    print "Converting text to speech"

    tts = TTSEngine(taskName = articleName.decode('unicode_escape').encode('ascii','ignore'), fExt = fExt)

    tts.createMp3()

    print "creating vids"

    vidCreator = VideoCreator(noOfFiles = noOfFiles, imageType = fExt, taskName = articleName.decode('unicode_escape').encode('ascii','ignore'))

    print "Normalizing images"

    vidCreator.normalizeImages()
    print "Making videos"

    vidCreator.makeVid()

    print "Collecting Tags"

    Tags = TagsCreator(taskName = articleName.decode('unicode_escape').encode('ascii','ignore'))
    Tags.collectTags()
    print "Finished"
