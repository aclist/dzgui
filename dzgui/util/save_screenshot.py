from pathlib import Path
from typing import cast, TYPE_CHECKING

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GLib  # noqa E402

if TYPE_CHECKING:
    from dzgui.controllers.mc import Controller
    from dzgui.views.base import OuterWindow
    from dzgui.views.mixins.context_mixin import ContextMixin
    from gi.repository import GdkPixbuf

# TODO: randomize/mock PII distance values


class IdleScreenshot:
    def __init__(
        self, controller: "Controller", window: "OuterWindow", scrot_path: Path
    ) -> None:
        self.window = window
        self.controller = controller
        self.scrot_path = scrot_path

        clock = window.get_frame_clock()
        if clock is None:
            raise TypeError("Widget not realized, FrameClock not initialized")
        clock.connect("after-paint", self.callback)

    def callback(self, clock: Gdk.FrameClock) -> None:
        GLib.timeout_add(1000, self.check_idle)

    def check_idle(self) -> bool:
        tv = self.controller.get_active_treeview()
        loaded = tv.is_loaded()
        if loaded is True:
            self.emit_key_press(tv)
            GLib.timeout_add(1000, self.save_and_quit)
            return True
        return False

    def emit_key_press(self, widget: "ContextMixin") -> None:
        window = widget.get_parent_window()
        if window is None:
            raise TypeError(f"Failed to find a valid parent window for {widget}")
        event = Gdk.EventKey.new(Gdk.EventType.KEY_PRESS)
        # NOTE: GTK introspection returns Gdk.Event type
        event_key = cast(Gdk.EventKey, event)
        event_key.keyval = Gdk.KEY_l
        event_key.state = Gdk.ModifierType.CONTROL_MASK
        event_key.window = window
        event_key.time = Gdk.CURRENT_TIME
        event_key.send_event = True
        # TODO: suppress errors from synthetic key events
        widget.present_menu(widget, event)

    def save_and_quit(self) -> None:
        self.save_pixbuf()
        self.controller.save_res_and_quit()

    def save_pixbuf(self) -> None:
        pixbuf = self.capture_application()
        if pixbuf:
            pixbuf.savev(str(self.scrot_path), "png", [], [])

    def capture_application(self) -> "GdkPixbuf.Pixbuf":
        # NOTE: composited context menu over X11 window
        root = Gdk.get_default_root_window()

        xwindow = self.window.get_window()
        if xwindow is None:
            raise ValueError("Failed to get a valid X11 window")
        index, x, y = xwindow.get_origin()
        width, height = self.window.get_size()

        application = Gdk.pixbuf_get_from_window(root, x, y, width, height)
        if application is None:
            raise ValueError("Failed to get a valid GdkPixbuf")
        return application
