from gtts import gTTS

class TTSEngine(object):
    def __init__(self, taskName, fExt):
        self.taskName = taskName
        self.fp = open('./'+taskName+'/text/'+taskName+'.txt')
        self.count = "audio";
        self.fExt = fExt


    def createMp3(self):
        line = self.fp.read().decode('unicode_escape').encode('ascii','ignore')

        tts = gTTS(text=line, lang='en-au', slow=False)
        tts.save('./'+self.taskName+'/mp3/'+self.count+'.mp3')


        self.fp.close()
