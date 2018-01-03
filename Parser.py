import os
import requests
import bs4
from bs4 import BeautifulSoup


class Parser(object):
    def __init__(self,taskName, articleLink, imageLink):
        os.mkdir('./'+taskName)
        os.mkdir('./'+taskName+'/mp3')
        os.mkdir('./'+taskName+'/video')
        os.mkdir('./'+taskName+'/text')
        os.mkdir('./'+taskName+'/image')
        self.taskName = taskName
        self.articleLink = articleLink
        self.thumbnailLink = imageLink
        self.count = 0
        self.fExt = "jpg"

    def download(self,imageLink,fileName):
        print 'Downnloading Image '+fileName
        f = open('./'+self.taskName+'/image/'+fileName+'.'+self.fExt,'wb');
        req = requests.get(imageLink)
        f.write(req.content)
        f.close()

    def writeText(self,text):
        g = open('./'+self.taskName+'/text/'+self.taskName+'.txt','a')
        g.write(text.encode('utf8'))
        g.write('\n')
        g.close()

    def visit(self):
        req = requests.get(self.articleLink)
        soup = BeautifulSoup(req.content,'html.parser')
        div = soup.find("div",attrs={'itemprop':'articleBody'})
        entryImageDiv = soup.find("div",attrs={'class':'entry-image'})
        entryImage = entryImageDiv.find('img')
        print "entry image link"
        print entryImage
        self.thumbnailLink = entryImage['data-base']
        ps = div.findAll('p')
        imagesDiv = soup.find("div",attrs={'id':'gallery-3'})
        if imagesDiv is  None:
            imagesDiv = div.findAll("figure")
        if imagesDiv is not None:
            print str(len(imagesDiv)-1)+" Images"
            for d in imagesDiv:
                imgTag = d.find('img')
                if imgTag == -1:
                    continue
                print imgTag
                imgFileLink = imgTag['data-base']
                self.count += 1
                fileName = "pic%04d"%self.count
                self.download(imgFileLink,fileName)

        self.count += 1
        fileName = "pic%04d"%self.count
        self.download(self.thumbnailLink,fileName)


        iterator = 0
        for i in range(0,len(ps)):
            #print element
            #print len(ps[i].text)
            #print ps[i]['class'][0]
            #print " \n\n"
            iterator += 1
            if ps[i]['class'][0].decode('utf8')=='email':
                break;
                #self.writeText(element.text)
        for i in range(iterator,len(ps)):
            self.writeText(ps[i].text)


        return (self.fExt,self.count)
