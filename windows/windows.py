# This module provide the classes for the clock-window
# and the window for the alarm.

from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import Gdk

from timers.timer import Timer,fromArr2Time,fromStr2Time

# Here follow the definitions of the classes for the two windows

class AlarmWindow(Gtk.Window):

   def __init__(self):

      Gtk.Window.__init__(self,title='Alarm')
      self.hbox = Gtk.HBox(spacing=6)

      self.__default_countdown__ = Timer(hour=0,min=1,sec=0) # hidden member
      self.__timeoutref__ = ''

      self.countdown = self.__default_countdown__.copy() 
      self.label = Gtk.Label('- '+str(self.countdown))
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
      self.countdown = self.__default_countdown__.copy()
      self.updateCountdown()
      return True

   def start(self): # Start countdown
      
      if self.countdown == Timer(): # If the countdown is on zero we do nothing
         return False 
      # otherwise ...
      if self.__timeoutref__ != '': # If there's a countdown already active.
         return False
      # otherwise
      self.show_all()
      self.updateCountdown()
      self.__timeoutref__ = GLib.timeout_add_seconds(1,self.updateCountdown)      
      return True

   def stop(self): # stop the CountDown
      
      if self.__timeoutref__ != '':
         GLib.source_remove(self.__timeoutref__)
      self.__timeoutref__ = ''
      return True

   def updateCountdown(self):

      flashTime = Timer(min=1,sec=0) # Time when start to flashing
      finish = Timer() # Time is end
      
      self.label.set_text('- '+str(self.countdown))
      self.countdown.dec() # Decrement the countdown
      if self.countdown == finish: # if countdown is zero, we stop cycling
         return False # and stop the countdown
   
      return True # Otherwise we countinue to cycle

   def setDialogSet(self): # This method open a dialog box
                       # that ask for the default countdown
      dialog = Gtk.Dialog()
      contentArea = dialog.get_content_area() # This is the part of dialog 
                                               # that will contain label and entries
      actionArea = dialog.get_action_area() # This instead is the area that contain buttons

      dialog.button = Gtk.Button('Set') # Button to setting the countdown
      dialog.label = Gtk.Label('Inserire un countdown nella forma HH:MM:SS')
      dialog.entry = Gtk.Entry()

      dialog.button.connect('clicked',lambda x: self.setTimer(dialog))

      contentArea.add(dialog.label)
      contentArea.add(dialog.entry)
      actionArea.add(dialog.button)

      dialog.show_all()

   def setTimer(self, dialog):
      
      self.__default_countdown__ = fromStr2Time(dialog.entry.get_text(),[0,1,0]) # As default time we take 00:01:00 [0,1,0]
      self.reset()
      dialog.destroy() # Once we setted the timer we don't need anymore 
                       # the dialog window
      return True
