# -*- coding: UTF-8 -*-

import pygame
from numpy import sin, cos
from time import sleep
from os.path import join
from eyetrainer.common import vars
from sys import exit

pygame.init()
pygame.font.init()

Display = pygame.display.set_mode((800,600))
pygame.display.set_icon(pygame.image.load(vars.ProgramIconPath))
pygame.display.set_caption("Eyetrainer 0.1 Alfa - (PyGame Interface)")

clock = pygame.time.Clock()

class QuestionImage:
	def __init__(self):
		pass

	def set(self, path):
		self.Object = pygame.image.load(path)
		self.Rectangle = self.Object.get_rect()

	def show(self):
		Display.fill((0,0,0))
		Display.blit(self.Object, self.Rectangle)


class QuestionText():
	def __init__(self):
		self._font = pygame.font.Font(vars.DefaultFontPath, 35)
		self._bcolor = (0,0,0)
		self._fcolor = (255,255,255)

	def set(self, string):
		self.Object = self._font.render(string, True, self._fcolor, self._bcolor)
		self.Rectangle = self.Object.get_rect(centerx=Display.get_width()/2,centery=Display.get_height()/2)
		
	def show(self):
		Display.fill((0,0,0))
		Display.blit(self.Object, self.Rectangle)


class ProgressBar():
	def __init__(self, fgcolor = (255,255,255), bgcolor = (100,100,100), height = 20):
		self.fraction = 0
		self._bcolor = bgcolor
		self._fcolor = fgcolor
		self._height = height

	def show(self):
		pygame.draw.rect(Display, self._bcolor, \
			(0,	Display.get_height() - self._height,\
			Display.get_width(), Display.get_height()\
		))
		
		pygame.draw.rect(Display, self._fcolor, \
			(0,	Display.get_height() - self._height ,\
			Display.get_width() * self.fraction, Display.get_height() \
		))


class AnswersTable():
	def __init__(self):
		self._font = pygame.font.Font(vars.DefaultFontPath, 15)
		self._titlefont = pygame.font.Font(vars.DefaultFontPath, 30)
	def show(self,Questions):
		Display.fill((255,255,255),	(0, 0,	Display.get_width(),Display.get_height()))
		string = self._titlefont.render("AnswersTable", True, (0,0,0))
		Display.blit(string, string.get_rect())
		for index in range(len(Questions)):
			string = self._font.render(str(index+1)+")"+Questions[index].question+" : "+Questions[index].answer, True, (0,0,0))
			rectangle = string.get_rect()
			rectangle[1] = rectangle[1] + (22 * index) + 50
			Display.blit(string, rectangle)
		string = self._font.render("Press Any Key...", True, (0,0,0))
		rectangle = string.get_rect()
		rectangle[1] = Display.get_height() - 20
		Display.blit(string,rectangle)
		pygame.display.flip()
		pause = True
		while pause:
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					pause = False
		
class Menu:
	def __init__(self, \
		fontsize = 50,\
		choices = None,\
		itemcolor = (100,100,100)):
		self._font = pygame.font.Font(vars.MenuFontPath, fontsize)
		self._choices = choices
		self._itemcolor = itemcolor
		self._bgimage = pygame.image.load(vars.MenuBackGroundPath)
		self._selected = 0
		self._frame = 0
		self._cosmap = [sin(n * 3.14 / 15) for n in range(30)]

	def run(self):
		selected = None

		while not selected:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					selected = "quit"
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					selected = "quit"
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and self._selected < len(self._choices)-1:
					self._selected += 1 
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP and self._selected > 0:
					self._selected -= 1
				elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
					print "enter pressed"
					selected = self._choices[self._selected][0]

			Display.fill((255,255,255),(0,0,Display.get_width(), Display.get_height()))
			rectangle = self._bgimage.get_rect()
			rectangle[0] = 300
			rectangle[1] = 50
			Display.blit(self._bgimage,rectangle)
			self._drawlake()
			self._drawchoices()
			pygame.display.flip()
		return selected

	def _drawlake(self):
		pixels = pygame.surfarray.pixels2d(Display)
		self._frame += 1
		for x in range(10,180):
			for y in range(0,120):
				c = self._cosmap[(self._frame + y) % 30] * 4
				p = pixels[x+300][int(y + c + 60)]
				pixels[x+300][270-y] = p
	

	def _drawchoices(self):
		for index in range(len(self._choices)):
			if index == self._selected:
				Display.fill(
				(150,150,150),
				(0, (index * 50) + 350,	Display.get_width(),50))
			string = self._font.render(self._choices[index][1], True, self._itemcolor)
			rectangle = string.get_rect()
			rectangle[0] = (Display.get_width() / 2) - (rectangle[2] / 2)
			rectangle[1] = rectangle[1] + (50 * index) + 355
			Display.blit(string, rectangle)

class PyGameInterface:
	def __init__(self):
		pass

	def __del__(self):
		pygame.quit()
	class Action:
		SHOWIMAGE, SHOWTEXT, SHOWANSWERS = 0, 1, 2

	QuestionImage = QuestionImage()
	QuestionText = QuestionText()
	ProgressBar = ProgressBar()
	Menu = Menu(choices = (('start','Start Test'), ('quit','quit')))
	
	AnswersTable = AnswersTable()

	def runquestions(self,questions):
		clock = pygame.time.Clock()
		currentquestion = 0
		Seconds = 0
		Running = True
		self.Step = self.Action.SHOWIMAGE
		self.QuestionImage.set(questions[0].file_path)
		self.QuestionText.set(questions[0].question)
		pygame.time.set_timer(pygame.USEREVENT + 1, 1000)
		while Seconds < len(questions) * 10 and Running == True:
			events = pygame.event.get()
			for event in events:
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()
				if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
					Running = False
				if event.type == pygame.USEREVENT + 1:
					if Seconds % 5 == 0:
						if self.Step == self.Action.SHOWIMAGE:
							self.QuestionImage.show()
							currentquestion += 1
						elif self.Step == self.Action.SHOWTEXT:
							self.QuestionText.show()
							if currentquestion < len(questions):
								self.QuestionImage.set(questions[\
								currentquestion].file_path)
								self.QuestionText.set(questions[\
								currentquestion].question)
						self.Step = self.Step ^ True
					self.ProgressBar.fraction = float(Seconds) / float(\
					len(questions) * 10)
					self.ProgressBar.show()
					pygame.display.flip()
					self.ProgressBar.fraction
					Seconds += 1
