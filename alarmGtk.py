#!/usr/bin/python

from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import Gdk

import socket
from threading import Thread

from windows.windows import AlarmWindow

# Setting the alarm window

window = AlarmWindow() # Create the object for the window.

provider = Gtk.CssProvider()
display = Gdk.Display.get_default()
screen = display.get_default_screen()

provider.load_from_data(b"""
#CountDown {
font-size: 60px;
}
""") # Set style

Gtk.StyleContext.add_provider_for_screen(screen,provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

# Setting the server to listen for command via inet socket.

listener = {
    'start':(lambda win: win.start()),
    'stop':(lambda win: win.reset())
}

def listen(window, sock):
    mess = 'ok'
    while 1 == 1:
        (clientSock, hostname) = sock.accept()
        while mess != '': # Until the other end point doesn't terminate connection continue
            mess = clientSock.recv(7)[:-2]
            if mess in listener.keys():
                listener[mess](window)
        clientSock.close() # If we read '' the other end has closed the connection.
        mess = 'ok' # Restart the control message.


server = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM)
server.bind(('127.0.0.1',9999)) # We make the application listen to the port 9999
                              # on localhost for command for the window.
server.listen(1) # We accept one connection at time.
process = Thread(target = listen, args = (window,server))
process.daemon = True
process.start()

# Start the Gtk Application

Gtk.main()

server.close() # We the application terminate we close the socket.
