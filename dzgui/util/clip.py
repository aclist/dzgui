import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk


def copy_clipboard(text: str) -> None:
    clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
    clipboard.set_text(text, -1)
