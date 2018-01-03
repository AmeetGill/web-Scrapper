from textblob import TextBlob
import sys
import os


class TagsCreator():
    def __init__(self,taskName):
        self.taskName = taskName

    def collectTags(self):
        with open('./'+self.taskName+'/text/'+self.taskName+'.txt','r') as f:
            lines = f.readlines()
        set1 = set()

        f = open('./'+self.taskName+'/text/tags.txt','w+')

        for line in lines:
            blob = TextBlob(line.decode('utf8'))
            noun_list = blob.noun_phrases
            for noun in noun_list:
                set1.add(noun)

        for word in set1:
            f.write(word.encode('utf8').decode('unicode_escape').encode('ascii','ignore')+', ')

        f.close()
