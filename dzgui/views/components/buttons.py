from typing import Callable, Literal, Self, TYPE_CHECKING, Union

from dzgui.util.clip import copy_clipboard
from dzgui.strings import buttons
from dzgui.util.strings import (
    atomic_buttons,
)
from dzgui.const.icons import (
    ICON_CLIPBOARD,
    ICON_CLOSE,
    ICON_INPUT_KEYBOARD,
    ICON_LIST_ADD,
    ICON_REFRESH,
    ICON_STEAM,
    ICON_WEB_BROWSER,
)
from dzgui.strings import connect_panel

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

if TYPE_CHECKING:
    from gi.repository import GLib
    from dzgui.controllers.mc import Controller
    from dzgui.controllers.emitter import Emitter
    from dzgui.const.enum import ServerTab


class Icon(Gtk.Image):
    def __init__(self, name: str, margin_start: int = 0, margin_end: int = 0) -> None:
        super().__init__(
            icon_name=name,
            icon_size=Gtk.IconSize.BUTTON,
            margin_start=margin_start,
            margin_end=margin_end,
            ypad=2,
        )


class LargeIcon(Gtk.Image):
    def __init__(self, name: str, margin_start: int = 5, margin_end: int = 0) -> None:
        super().__init__(
            icon_name=name,
            icon_size=Gtk.IconSize.LARGE_TOOLBAR,
            margin_start=margin_start,
            margin_end=margin_end,
        )


class IconButton(Gtk.Button):
    def __init__(
        self,
        icon: str,
        position: Gtk.PositionType = Gtk.PositionType.RIGHT,
        margin_start: int = 0,
        margin_end: int = 0,
    ) -> None:
        super().__init__()
        self.icon = Icon(icon, margin_start=margin_start, margin_end=margin_end)
        self.set_image(self.icon)
        self.set_image_position(position)
        self.set_focus_on_click(False)  # type: ignore[no-untyped-call]
        self.set_always_show_image(True)

    def swap_icon(self, icon: str) -> None:
        start = self.icon.get_margin_start()
        end = self.icon.get_margin_end()
        alt_icon = Icon(icon, margin_start=start, margin_end=end)
        self.set_image(alt_icon)

    def revert_icon(self) -> None:
        self.set_image(self.icon)


class IconTextButton(IconButton):
    def __init__(
        self, icon: str, label: str, position: Gtk.PositionType = Gtk.PositionType.RIGHT
    ) -> None:
        match position:
            case Gtk.PositionType.RIGHT:
                super().__init__(icon, position, margin_start=5)
            case Gtk.PositionType.LEFT:
                super().__init__(icon, position, margin_end=5)
            case _:
                raise ValueError("Unsupported position type")
        self.set_label(label)


class LargeIconTextButton(IconButton):
    def __init__(
        self, icon: str, label: str, position: Gtk.PositionType = Gtk.PositionType.RIGHT
    ) -> None:
        super().__init__(icon, position)
        self.set_label(label)
        self.set_image(LargeIcon(icon))


class ClipboardButton(IconTextButton):
    def __init__(self, controller: Union["Controller", None], func: Callable) -> None:
        super().__init__(ICON_CLIPBOARD, atomic_buttons.copy)
        self.controller = controller
        self.connect("clicked", self._on_button_clicked, func)

        self.set_tooltip_text(buttons.clipboard_button)

    def _on_button_clicked(self, button: Self, func: Callable[[], str]) -> None:
        def revert() -> Literal[False]:
            self.revert_icon()
            return False

        self.swap_icon("object-select-symbolic")
        data = func()
        copy_clipboard(data)
        GLib.timeout_add(600, revert)


class CopyIpButton(ClipboardButton):
    def __init__(self, func: Callable[[], str]) -> None:
        super().__init__(func)

        self.set_tooltip_text(buttons.clipboard_ip_button)


class CloseButton(IconTextButton):
    def __init__(self, label: str) -> None:
        super().__init__(icon=ICON_CLOSE, label=label)

        self.set_tooltip_text(buttons.unset_button_tooltip)


class WebButton(IconTextButton):
    def __init__(self, label: str) -> None:
        super().__init__(icon=ICON_WEB_BROWSER, label=label)
        pass


class RefreshButton(IconTextButton):
    def __init__(self, controller: "Controller") -> None:
        super().__init__(
            icon=ICON_REFRESH,
            label=atomic_buttons.refresh,
        )

        self.controller = controller
        emitter = self.controller.get_emitter()
        self.loading = False
        self.is_clicked = False

        self.time = 30

        self.set_margin_top(10)
        self.set_margin_start(80)
        self.set_margin_end(80)
        self.set_tooltip_text(atomic_buttons.refresh_tooltip)

        self.connect("clicked", self._on_refresh_clicked)
        emitter.connect("servers_loaded", self._on_load)
        emitter.connect("servers_timed_out", self._on_timeout)

    def _on_timeout(self, emitter: "Emitter") -> None:
        self.is_clicked = True
        self.start_decrement()

    def _on_load(self, emitter: "Emitter", tab: "ServerTab") -> None:
        self.start_decrement()

    def _on_refresh_clicked(self, button: Self) -> None:
        """Spawned in a thread"""
        self.is_clicked = True
        self.controller.refresh_tree()
        # TODO: get server tab enum
        # if LAN tab, reload existing entries in place

    def start_decrement(self) -> None:
        if self.is_clicked is False:
            return
        if self.loading:
            return
        self.set_sensitive(False)
        self.loading = True
        self.is_clicked = False
        self.show_time(True)
        GLib.timeout_add_seconds(1, self.decrement)

    def decrement(self) -> bool:
        self.time -= 1
        if self.time == 0:
            self.time = 30
            self.show_time(False)
            self.set_sensitive(True)
            self.loading = False
            return False
        self.show_time(True)
        return True

    def show_time(self, state: bool) -> None:
        if state is True:
            self.set_label(f"{atomic_buttons.refresh} ({str(self.time)})")
        else:
            self.set_label(atomic_buttons.refresh)


class KeysButton(IconTextButton):
    def __init__(self, controller: "Controller") -> None:
        super().__init__(icon=ICON_INPUT_KEYBOARD, label=atomic_buttons.keys)

        self.controller = controller
        self.set_margin_top(10)
        self.set_margin_start(80)
        self.set_margin_end(80)

        self.set_tooltip_text(atomic_buttons.keys_tooltip)

        self.connect("clicked", self._on_keys_clicked)

    def _on_keys_clicked(self, button: Gtk.Button) -> None:
        self.controller.open_keybindings()


class SteamConnectButton(LargeIconTextButton):
    def __init__(self) -> None:
        super().__init__(icon=ICON_STEAM, label=connect_panel.connect_button)
        self.set_tooltip_text(connect_panel.connect_tooltip)


class SteamTextButton(SteamConnectButton):
    def __init__(self, label: str) -> None:
        super().__init__()
        self.set_label(label)


class SteamWorkshopButton(SteamTextButton):
    def __init__(self) -> None:
        super().__init__(label=buttons.workshop)
        self.set_tooltip_text(buttons.workshop_tooltip)
        self.set_margin_top(10)
        self.set_margin_bottom(10)


class AddButton(IconTextButton):
    def __init__(self) -> None:
        super().__init__(icon=ICON_LIST_ADD, label=connect_panel.add_button)
        self.set_tooltip_text(connect_panel.add_tooltip)


class SpinnerButton(Gtk.Button):
    def __init__(self, label: str) -> None:
        super().__init__()

        self.text = label
        self.label = Gtk.Label(label=label, halign=Gtk.Align.CENTER)

        self.spinner = Gtk.Spinner()
        self.spinner.set_halign(Gtk.Align.END)
        self.spinner.set_sensitive(False)

        grid = Gtk.Grid(column_spacing=10)
        for el in self.label, self.spinner:
            grid.add(el)

        self.add(grid)

        self.connect("clicked", self._on_button_clicked)
        self.connect("map", self._on_map)

    def _on_map(self, button: Self) -> None:
        self.spinner.set_visible(False)

    def _on_button_clicked(self, button: Self) -> None:
        self.start_spinner()

    def stop_spinner(self) -> None:
        self.spinner.set_visible(False)
        self.spinner.stop()

    def start_spinner(self) -> None:
        self.spinner.set_visible(True)
        self.spinner.start()
