import pygtk, gtk, sys, gobject
pygtk.require('2.0')

from os.path import exists, join
from eyetrainer import HOMEPATH, ICONPATH, DEFAULTIMAGEPATH, __version__

class QuestionImage(gtk.Image):
	def __init__(self):
		gtk.Image.__init__(self)
		self.set(DEFAULTIMAGEPATH)

	def set(self, image_path):
		self.set_from_file(image_path)

class QuestionText(gtk.Label):
	def __init__(self):
		gtk.Label.__init__(self)
		self.set_justify(gtk.JUSTIFY_CENTER)

	def set(self,text):
		self.set_text(text)

class GtkInterFace:
	def __init__(self):
		# Create main window
		self.MainWindow = MainWindow()
		# Content is 3 lined VBOX
		self.Content = gtk.VBox(False,0)
		# Create a frame that will contain our image
		self.QuestionImageFrame = gtk.Frame()
		# FIXME : size_request is not fixing the size of frame
		self.QuestionImageFrame.set_size_request(800,600)
		# Create a frame that will contain our question string
		self.QuestionTextFrame = gtk.Frame()
		self.QuestionTextFrame.set_size_request(800,600)
		# Create instance of QuestionImage and QuestionText
		self.QuestionImage = QuestionImage()
		self.QuestionText = QuestionText()
		# Create Status Bar, initalize it..
		self.StatusBar = gtk.Statusbar()
		self.StatusBar.push(0, "Eyetrainer version : %s" % __version__)
		# Create notebook that will make display switchs for us
		self.ScrolledWindow = gtk.ScrolledWindow()
		self.ScrolledWindow.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		self.ListStore = gtk.ListStore(gobject.TYPE_UINT, gobject.TYPE_STRING, gobject.TYPE_STRING)
		self.TreeView = gtk.TreeView(self.ListStore)
		self.TreeView.append_column(gtk.TreeViewColumn('#'  , gtk.CellRendererText(), text=0))
		self.TreeView.append_column(gtk.TreeViewColumn('Question', gtk.CellRendererText(), text=1))
		self.TreeView.append_column(gtk.TreeViewColumn('Answer', gtk.CellRendererText(), text=2))
		self.QuestionTabs = gtk.Notebook()
		self.QuestionTabs.append_page(self.QuestionImage)
		self.QuestionTabs.append_page(self.QuestionText)
		self.QuestionTabs.append_page(self.TreeView)

		# Do not show tabs
		self.QuestionTabs.set_show_tabs(False)

		# Create menus
		
		self.FileSubMenu = gtk.Menu()

		self.MenuItems = dict()
		self.MenuItems["Start"] = gtk.MenuItem("_Start")
		self.MenuItems["Stop"] = gtk.MenuItem("S_top")

		self.FileSubMenu.append(self.MenuItems["Start"])
		self.FileSubMenu.append(self.MenuItems["Stop"])
		self.FileMenu = gtk.MenuItem("_File")
		self.FileMenu.set_submenu(self.FileSubMenu)
		self.FileMenu.show()
		self.MenuBar = gtk.MenuBar()
		self.MenuBar.append(self.FileMenu)
		
		# Pack our content
		self.Content.pack_start(self.MenuBar, False)
		self.Content.pack_start(self.QuestionTabs)
		self.StartStopButton = gtk.Button(stock = gtk.STOCK_MEDIA_PLAY)
		self.StartStopButton.set_border_width(2)
		self.ProgressBar = gtk.ProgressBar()
		self.ProgressBar.set_size_request(600,0)
		self.ProgressBar.set_pulse_step(0.2)
		hline = gtk.HBox(False, 0)
		hline.pack_start(self.ProgressBar)
		hline.pack_start(self.StartStopButton)
		self.Content.pack_start(hline)
		self.Content.pack_start(self.StatusBar)
		self.MainWindow.add(self.Content)
		self.MainWindow.show_all()

	def CreateAnswersTable(self, widget = None, questions = None):
		self.ListStore.clear() # removes all rows
		c = 0
		for question in questions:
			c += 1
			self.ListStore.append((c, question.question, question.answer))

	def SetRunningState(self,widget=None,Questions=None):
		self.StartStopButton.set_label(gtk.STOCK_MEDIA_STOP)
		self.MenuItems["Start"].set_sensitive(False)
		self.MenuItems["Stop"].set_sensitive(True)
		self.QuestionImage.set(Questions[0].file_path)
		self.StatusBar.push(0,"Training started")
		
	def SetFinishedState(self,widget=None):
		self.StartStopButton.set_label(gtk.STOCK_MEDIA_PLAY)
		self.ProgressBar.set_fraction(0)
		self.MenuItems["Start"].set_sensitive(True)
		self.ShowAnswers()
		self.MenuItems["Stop"].set_sensitive(False)

	def ShowImage(self, widget=None):
		# Change current page to 0, so displays image
		self.QuestionTabs.set_current_page(0)

	def ShowText(self, widget=None):
		# Change current page to 1, so displays questions
		self.QuestionTabs.set_current_page(1)

	def ShowAnswers(self, widget = None, answers = None):
		self.QuestionTabs.set_current_page(2)


	def ShowMessage(self, widget = None, msg = None):
		# Shows a message
		dialog = gtk.MessageDialog(
				None,
				gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
				gtk.MESSAGE_INFO, gtk.BUTTONS_OK,
				str(msg))
		dialog.run()
		dialog.destroy()

	def ShowAboutDialog(self, action):
		from eyetrainer import __author__, __email__, __license__, __version__, __website__
		authors = ["%s <%s>" % (__author__, __email__)]
		about = gobject.new(gtk.AboutDialog,
							name = __name__,
							version = __version__,
							logo = gtk.gdk.pixbuf_new_from_file(ICONPATH),
							copyright = "bu dunya kimseye kalmaz",
							comments= "Short-term visional memory test application",
							license = __license__,
							authors = authors,
							website = "http://eyetrainer.googlecode.com/"
							)
		about.set_transient_for(self.MainWindow)
		about.run()
		about.destroy()

class MainWindow(gtk.Window):
	# Our main window, with icons and some other settings
	def __init__(self):
		gtk.Window.__init__(self)
		self.set_title("Eye Trainer")
		self.set_icon(gtk.gdk.pixbuf_new_from_file(ICONPATH))
		self.set_resizable(False)
		self.connect('destroy', self.Quit)

	def Quit(self, widget, user_data=None):
		print "exiting..."
		gtk.main_quit()
