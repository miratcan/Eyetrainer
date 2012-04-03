#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml.etree.ElementTree import ElementTree
from os.path import dirname, exists, join
from random import randrange
from random import choice as randchoice

class Image:
    def __init__(self, file_path, question, answer):
        self.file_path = file_path
        self.question = question
        self.answer = answer

class QuestionSet:
    def __init__(self, xml_path, language):
        self.xmlpath = xml_path
        self.rootpath = dirname(self.xmlpath)
        self.language = language
        self.tree = ElementTree().parse(xml_path)
        self.Reset()

    def ParseImages(self):
        NumOfQuestions = 0
        for ImageElement in self.tree.findall("image"):
            FileName = ImageElement.attrib["file"]
            if exists(join(self.rootpath,FileName)):
                QuestionList = list()
                for QuestionElement in ImageElement.findall("question"):
                    if QuestionElement.attrib["lang"] == self.language:
                        QuestionList.append((QuestionElement.attrib["string"], QuestionElement.attrib["answer"]))
                        NumOfQuestions += 1
                if QuestionList :
                    rquestion = randchoice(QuestionList)
                    # bir reim ve rasgele bir cevap
                    self.images.append(Image(join(self.rootpath,join(FileName)), rquestion[0], rquestion[1]))
            else:
                print "File %s not found, skipping" % FileName
        print "Parsed %s images and  %s questions" % (len(self.images), NumOfQuestions)

    def Get(self, NumOfQuestions):
        AvailibleImages = self.images[:]
        Questions = list()
        for counter in range(NumOfQuestions):
            select = randrange(len(AvailibleImages))
            Image = AvailibleImages[select]
            Questions.append(Image)
            del(AvailibleImages[select])
        return Questions

    def Reset(self):
        self.images = list()
        self.ParseImages()

if __name__ == "__main__":
    from eyetrainer import SETXMLPATH
    questionset = QuestionSet(SETXMLPATH,"tr")
    questions = questionset.Get(5)
    for image in questions:
        print image.file_path, image.question
    print "-------------------------------------------"
    questions = questionset.Get(5)
    for image in questions:
        print image.file_path, image.question

