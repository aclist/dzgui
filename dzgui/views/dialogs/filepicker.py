from pathlib import Path

from dzgui.const.constants import DEBUG_LOG, SYSTEM_LOG
from dzgui.strings.filepickers import diagnostic_picker_title, debug_picker_title

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class FilePicker(Gtk.FileChooserDialog):
    def __init__(self, parent: Gtk.Window, title: str, placeholder: str) -> None:
        super().__init__(
            title=title,
            action=Gtk.FileChooserAction.SAVE,
            transient_for=parent,
            resizable=True,
        )
        self.add_buttons("_Cancel", Gtk.ResponseType.CANCEL)  # type: ignore[no-untyped-call]
        self.add_buttons("_Save", Gtk.ResponseType.OK)  # type: ignore[no-untyped-call]
        self.set_default_response(Gtk.ResponseType.OK)

        self.set_current_name(placeholder)

    def pick_file(self) -> Path | None:
        res = self.run()  # type: ignore[no-untyped-call]
        if res in (Gtk.ResponseType.CANCEL, Gtk.ResponseType.DELETE_EVENT):
            self.destroy()
            return None
        if res == Gtk.ResponseType.OK:
            file = self.get_filename()
            if file is not None:
                self.destroy()
                return Path(file)
        return None


class DiagnosticLogPicker(FilePicker):
    def __init__(self, parent: Gtk.Window) -> None:
        super().__init__(parent, diagnostic_picker_title, SYSTEM_LOG)


class DebugLogPicker(FilePicker):
    def __init__(self, parent: Gtk.Window) -> None:
        super().__init__(parent, debug_picker_title, DEBUG_LOG)


class FolderPicker(Gtk.FileChooserDialog):
    def __init__(self, parent: Gtk.Window, title: str) -> None:
        super().__init__(
            title=title,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
            parent=parent,
            resizable=True,
        )
        self.add_buttons("_Cancel", Gtk.ResponseType.CANCEL)  # type: ignore[no-untyped-call]
        self.add_buttons("_OK", Gtk.ResponseType.OK)  # type: ignore[no-untyped-call]
        self.set_default_response(Gtk.ResponseType.OK)

    def pick_folder(self) -> Path | None:
        res = self.run()  # type: ignore[no-untyped-call]
        if res in (Gtk.ResponseType.CANCEL, Gtk.ResponseType.DELETE_EVENT):
            self.destroy()
            return None
        if res == Gtk.ResponseType.OK:
            folder = self.get_current_folder()
            # TODO: this should never be possible
            if folder is None:
                try:
                    uri = self.get_uri()
                    if uri is None:
                        return None
                    return Path.from_uri(uri)
                except Exception:
                    # TODO: edge cases
                    return Path("/")
            self.destroy()
            return Path(folder)
        return None
