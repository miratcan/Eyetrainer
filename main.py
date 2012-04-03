from eyetrainer.ui.ui_pygame import PyGameInterface
from eyetrainer.questions import QuestionSet
from eyetrainer.common import vars
from os.path import join
from time import sleep

NumOfQuestions = 10
Interface = PyGameInterface()
QuestionSet = QuestionSet(vars.SetXmlPath, "tr")
Questions = QuestionSet.Get(NumOfQuestions)

Selected = None
Result = None
while Result <> "quit":
	Result = Interface.Menu.run()
	if Result == "start":
		Interface.runquestions(Questions)
		Interface.AnswersTable.show(Questions)
		Questions = QuestionSet.Get(NumOfQuestions)
del Interface

