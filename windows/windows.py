# This module provide the classes for the clock-window
# and the window for the alarm.

from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import Gdk

from datetime import datetime, timedelta

from re import match

# Here follow the definitions of the classes for the two windows

delta = timedelta(seconds=1) # This is the increment of countdown

class AlarmWindow(Gtk.Window):

   def __init__(self):

      Gtk.Window.__init__(self,title='Alarm')
      self.hbox = Gtk.HBox(spacing=6)
      self.count = timedelta() # Set the timer to 0
      self.endCount = timedelta(seconds=180) # count will increment of a sec till it reaches endCount
      self.timer = -1 # an id to reference the GLib timeout

      self.label = Gtk.Label('- '+str(self.endCount - self.count)[2:])
      self.buttonBox = Gtk.VBox()
      self.setButton = Gtk.Button('Set')
      self.resetButton = Gtk.Button('Reset')
      self.startButton = Gtk.Button('Start')

      self.label.set_name('CountDown')

      # Connect the signals of the buttons to methods to call

      self.startButton.connect('clicked', lambda void: self.start())
      self.resetButton.connect('clicked', lambda void: self.reset())
      self.setButton.connect('clicked', lambda void: self.setDialogSet())

      self.buttonBox.pack_start(self.setButton, True, True, 0)
      self.buttonBox.pack_start(self.resetButton, True, True, 0)
      self.buttonBox.pack_start(self.startButton, True, True, 0)

      self.hbox.pack_start(self.label, True, True, 0)
      self.hbox.pack_start(self.buttonBox, True, True, 0)
      self.set_name('Alarm')
      self.add(self.hbox)

      self.connect('delete-event', Gtk.main_quit)
      

      self.show_all()


   def reset(self): # Reset the counter

      self.stop()
      self.count = timedelta()
      self.updateCountdown()
      return True

   def start(self): # Start countdown

      if self.timer < 0: # If the countdown is not already started we start it
         self.updateCountdown()
         self.timer = GLib.timeout_add_seconds(1,self.updateCountdown)      
      return True # otherwise we do nothing

   def stop(self): # stop the CountDown
      if self.timer >= 0:
         if GLib.source_remove(self.timer): # Stop the counter
            self.timer = -1 # and set the counter to the id of a non valid id
      return True

   def updateCountdown(self):

      self.label.set_text('- '+str(self.endCount - self.count)[2:])
      self.count = self.count + delta # increment the counter of delta=1sec
      if self.count > self.endCount:
         self.timer = -1 # If we arrive to endCount secs the counter stops  
         return False    # and we the destroy the reference to the timer, which is non valid
      return True # Otherwise we countinue to cycle

   def setDialogSet(self): # This method open a dialog box
                           # that ask for the default countdown
      dialog = Gtk.Dialog()
      contentArea = dialog.get_content_area() # This is the part of dialog 
                                               # that will contain label and entries
      actionArea = dialog.get_action_area() # This instead is the area that contain buttons

      dialog.button = Gtk.Button('Set') # Button to setting the countdown
      dialog.label = Gtk.Label('Inserire un countdown nella forma MM:SS')
      dialog.entry = Gtk.Entry()

      dialog.button.connect('clicked',lambda x: self.setTimer(dialog))

      contentArea.add(dialog.label)
      contentArea.add(dialog.entry)
      actionArea.add(dialog.button)

      dialog.show_all()

   def setTimer(self, dialog):
      
      if match('^[0-9]{2}:[0-9]{2}$',dialog.entry.get_text()) == None:
         print('Errore il formato di tempo inserito non e` corretto')
      else:
         self.endCount = datetime.strptime('00:'+dialog.entry.get_text(),'%H:%M:%S')-datetime.strptime('00:00:00','%H:%M:%S')
      self.reset()
      dialog.destroy() # Once we setted the timer we don't need anymore 
                       # the dialog window
      return True
