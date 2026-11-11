import gi
import pytest

from dzgui.api.servers import Details
from dzgui.controllers.mc import Controller
from dzgui.controllers.emitter import Emitter
from dzgui.views.dialogs.servers import ServerDetailsDialog


gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MockController(Controller):
    def __init__(self) -> None:
        pass

    def get_window(self) -> None:  # type: ignore[override]
        return None

    def get_server_name(self) -> str:
        return "My server"

    def get_emitter(self) -> Emitter:
        return Emitter()


@pytest.mark.filterwarnings("ignore::DeprecationWarning")
def test_html_escaping() -> None:
    name = "Test server"
    desc = "<Server description> Game & mods"
    gametime = "05:30"
    day_accel = 5.0
    night_accel = 1.0
    details = Details([["0", "1"]], name, desc, gametime, day_accel, night_accel)
    controller = MockController()
    dialog = ServerDetailsDialog(controller, details)
    dialog.destroy()
    while Gtk.events_pending():
        Gtk.main_iteration()

    assert dialog.description.get_text() == desc
