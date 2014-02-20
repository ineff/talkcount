#!/usr/bin/python

from gi.repository import Gtk
from gi.repository import GLib
from gi.repository import Gdk

from timers.timer import Timer

from windows.windows import AlarmWindow

window = AlarmWindow()

provider = Gtk.CssProvider()
display = Gdk.Display.get_default()
screen = display.get_default_screen()

provider.load_from_data(b"""
#CountDown {
font-size: 60;
}
""")

Gtk.StyleContext.add_provider_for_screen(screen,provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

Gtk.main()
