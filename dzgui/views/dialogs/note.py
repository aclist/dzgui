from typing import Self, TYPE_CHECKING

from dzgui.strings import notes
from dzgui.views.components.entry import ValidatedEntry
from dzgui.views.dialogs.generic import GenericDialog

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

if TYPE_CHECKING:
    from dzgui.controllers.mc import Controller


class NoteDialog(GenericDialog):
    def __init__(self, controller: "Controller"):
        super().__init__(
            controller=controller,
            text=notes.dialog_title,
            buttons=Gtk.ButtonsType.NONE,
            mtype=Gtk.MessageType.INFO,
            secondary=notes.dialog_subtitle,
        )

        self.controller = controller

        delete_button = Gtk.Button(label=notes.delete_button)
        delete_button.set_sensitive(False)
        self.add_action_widget(delete_button, Gtk.ResponseType.CANCEL)
        self.ok = self.add_button(notes.ok_button, Gtk.ResponseType.OK)
        self.ok.grab_default()

        self.entry = ValidatedEntry(controller, self.validate)
        self.entry.set_max_length(30)
        self.entry.set_size_request(250, 0)
        self.pack(self.entry)

        note = self.controller.get_note()
        self.entry.set_text(note)
        if len(note) > 0:
            delete_button.set_sensitive(True)
            self.format_secondary_text(notes.current_note.format(note))
        elif len(note) == 0:
            self.ok.set_sensitive(False)

        self.show_all()
        # NOTE: explicitly deselect region and move to end of line
        self.entry.set_position(-1)

        self.entry.set_activates_default(True)
        self.connect("response", self._on_response)
        self.entry.connect("changed", self._on_text_changed)

    def _on_text_changed(self, entry: Gtk.Entry) -> None:
        if len(entry.get_text()) == 0:
            self.ok.set_sensitive(False)

    def validate(self, text: str) -> bool:
        if text.isspace():
            sensitive = False
        else:
            sensitive = True
        self.ok.set_sensitive(sensitive)
        return sensitive

    def _on_response(self, dialog: Self, response: Gtk.ResponseType) -> None:
        match response:
            case Gtk.ResponseType.OK:
                note = self.entry.get_text()
                self.controller.add_note(note)
            case Gtk.ResponseType.CANCEL:
                self.controller.delete_note()
            case _:
                pass
        self.destroy()
