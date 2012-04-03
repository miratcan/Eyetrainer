from os.path import join, exists
from os import getenv, getcwd, name # curdir returns current directory

class vars:
	if name == "posix":
		print "Posix system found"
		if exists(join(getenv("HOME"),".eyetrainer")):
			HomePath = join(getenv("HOME"),".eyetrainer")
		else:
			HomePath = getcwd()
	elif name == "nt":
		print "Nt system found"
		HomePath = getcwd()

	MenuFontPath = join(HomePath, "data","bahamas.ttf")
	DefaultFontPath = join(HomePath, "data","freesansbold.ttf")
	CommonFontPath = join(HomePath, "data","sans .ttf")
	QuestionsFolderPath = join(HomePath, "questions")
	SetXmlPath = join(HomePath , "questions","set.xml")
	MenuBackGroundPath = join(HomePath, "data","default_image.png")
	ProgramIconPath = join(HomePath, "data","eyetrainer.png")

print vars.MenuFontPath, vars.DefaultFontPath

