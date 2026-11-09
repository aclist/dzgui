from __future__ import annotations
from dataclasses import dataclass
from enum import Enum

from dzgui.util import strings
from dzgui.strings import rows


class Port(Enum):
    DEFAULT = 1
    CUSTOM = 2


class ServerTab(Enum):
    BROWSER = 0
    SAVED = 1
    RECENT = 2
    LAN = 3


class Popup(Enum):
    WAIT = 1
    NOTIFY = 2
    CONFIRM = 3
    ENTRY = 4
    MODLIST = 6
    DETAILS = 7
    QUIT = 8


class VAdjustment(Enum):
    UP = 1
    DOWN = 2
    TOP = 3
    BOTTOM = 4


class CursorPosition(Enum):
    UP = 1
    DOWN = 2
    TOP = 3
    BOTTOM = 4


class FilterMode(Enum):
    INITIAL = 1
    TOGGLE_OFF = 2
    TOGGLE_ON = 3


@dataclass(slots=True, frozen=True)
class ModButtonMeta:
    label: str
    tooltip: str


@dataclass(slots=True, frozen=True)
class ButtonTypeMeta:
    label: str
    tooltip: str
    opens: NotebookPage | None


@dataclass(slots=True, frozen=True)
class ConfigKey:
    key: str


@dataclass(slots=True, frozen=True)
class NotebookMeta:
    crumbs: str
    has_statusbar: bool


@dataclass(slots=True, frozen=True)
class RowMeta:
    label: str
    tooltip: str


@dataclass(slots=True, frozen=True)
class ContextMenuMeta:
    label: str


class ContextMenuItem(Enum):
    ADD_NOTE = ContextMenuMeta(strings.add_note)
    ADD_SERVER = ContextMenuMeta(strings.add)
    CONNECT = ContextMenuMeta(strings.connect)
    COPY_LOG_CLIPBOARD = ContextMenuMeta(strings.copy_log)
    COPY_SERVER_IP = ContextMenuMeta(strings.copy_ip)
    COPY_SERVER_NAME = ContextMenuMeta(strings.copy_name)
    UNSUB_MOD = ContextMenuMeta(strings.unsub_mod)
    VALIDATE_MOD = ContextMenuMeta(strings.validate_mod)
    OPEN_WORKSHOP = ContextMenuMeta(strings.open_workshop)
    REFRESH_PLAYERS = ContextMenuMeta(strings.refresh_players)
    REMOVE_HISTORY = ContextMenuMeta(strings.remove_history)
    REMOVE_SERVER = ContextMenuMeta(strings.remove)
    SET_FAV = ContextMenuMeta(strings.add_fav)
    SHOW_DETAILS = ContextMenuMeta(strings.show_details)
    SHOW_MODS = ContextMenuMeta(strings.show_mods)

    @property
    def label(self) -> str:
        return self.value.label


class ContextMenuGroup(Enum):
    """
    Groupings of context menu items
    """

    SERVER_MOD = (ContextMenuItem.OPEN_WORKSHOP,)
    MOD = (
        ContextMenuItem.OPEN_WORKSHOP,
        ContextMenuItem.UNSUB_MOD,
        ContextMenuItem.VALIDATE_MOD,
    )
    MOD_OFFLINE = (None,)
    LOG = (ContextMenuItem.COPY_LOG_CLIPBOARD,)
    SERVER_BROWSER = (
        ContextMenuItem.CONNECT,
        ContextMenuItem.ADD_SERVER,
        ContextMenuItem.SET_FAV,
        ContextMenuItem.COPY_SERVER_NAME,
        ContextMenuItem.COPY_SERVER_IP,
        ContextMenuItem.ADD_NOTE,
        ContextMenuItem.SHOW_MODS,
        ContextMenuItem.SHOW_DETAILS,
        ContextMenuItem.REFRESH_PLAYERS,
    )
    SCAN_LAN = (
        ContextMenuItem.CONNECT,
        ContextMenuItem.SET_FAV,
        ContextMenuItem.COPY_SERVER_NAME,
        ContextMenuItem.COPY_SERVER_IP,
        ContextMenuItem.ADD_NOTE,
        ContextMenuItem.SHOW_MODS,
        ContextMenuItem.SHOW_DETAILS,
        ContextMenuItem.REFRESH_PLAYERS,
    )
    SAVED = (
        ContextMenuItem.CONNECT,
        ContextMenuItem.SET_FAV,
        ContextMenuItem.REMOVE_SERVER,
        ContextMenuItem.COPY_SERVER_NAME,
        ContextMenuItem.COPY_SERVER_IP,
        ContextMenuItem.ADD_NOTE,
        ContextMenuItem.SHOW_MODS,
        ContextMenuItem.SHOW_DETAILS,
        ContextMenuItem.REFRESH_PLAYERS,
    )
    RECENT = (
        ContextMenuItem.CONNECT,
        ContextMenuItem.ADD_SERVER,
        ContextMenuItem.SET_FAV,
        ContextMenuItem.REMOVE_HISTORY,
        ContextMenuItem.COPY_SERVER_NAME,
        ContextMenuItem.COPY_SERVER_IP,
        ContextMenuItem.ADD_NOTE,
        ContextMenuItem.SHOW_MODS,
        ContextMenuItem.SHOW_DETAILS,
        ContextMenuItem.REFRESH_PLAYERS,
    )


class Preferences(Enum):
    STEAM = ConfigKey("steam_api")
    CLIENT = ConfigKey("client")
    WINDOW = ConfigKey("fullscreen")
    DIST = ConfigKey("use_miles")
    NAME = ConfigKey("name")
    DEFAULT = ConfigKey("default_steam_path")
    FAV_LBL = ConfigKey("fav_label")
    FAV_SRV = ConfigKey("fav_server")
    IP_LIST = ConfigKey("ip_list")
    START_TAB = ConfigKey("start_tab")

    @property
    def key(self) -> str:
        return self.value.key


class NotebookPage(Enum):
    OFFLINE = NotebookMeta(strings.crumbs.offline, True)
    CHANGELOG = NotebookMeta(strings.crumbs.changelog, True)
    DEVELOPERS = NotebookMeta(strings.crumbs.developers, False)
    HELP = NotebookMeta(strings.crumbs._help, True)
    KEYS = NotebookMeta(strings.crumbs.keys, True)
    LOG = NotebookMeta(strings.crumbs.log, True)
    MODS = NotebookMeta(strings.crumbs.mods, True)
    OPTIONS = NotebookMeta(strings.crumbs.options, False)
    SERVERS = NotebookMeta(strings.crumbs.servers, True)
    THANKS = NotebookMeta(strings.crumbs.thanks, True)
    CONNECTION = NotebookMeta(strings.crumbs.connect, True)

    @property
    def crumbs(self) -> str:
        return self.value.crumbs

    @property
    def has_statusbar(self) -> bool:
        return self.value.has_statusbar


class RowType(Enum):
    CHANGELOG = RowMeta(rows.changelog_label, rows.changelog_status)
    SHOW_LOG = RowMeta(rows.log_label, rows.log_status)
    SEPARATOR = RowMeta(rows.separator_label, rows.separator_status)
    DUMP_LOG = RowMeta(rows.system_log_label, rows.system_log_status)
    DOCS = RowMeta(rows.docs_label, rows.docs_status)
    DOCS_FALLBACK = RowMeta(rows.docs_fallback_label, rows.docs_fallback_status)
    BUGS = RowMeta(rows.bugs_label, rows.bugs_status)
    FORUM = RowMeta(rows.forum_label, rows.forum_status)
    SPONSOR = RowMeta(rows.sponsor_label, rows.sponsor_status)
    THANKS = RowMeta(rows.thanks_label, rows.thanks_status)

    @property
    def label(self) -> str:
        return self.value.label

    @property
    def tooltip(self) -> str:
        return self.value.tooltip


class ModButton(Enum):
    SELECT_ALL = ModButtonMeta(
        strings.mod_panel.select_all, strings.mod_panel.select_all_tooltip
    )
    UNSELECT_ALL = ModButtonMeta(
        strings.mod_panel.unselect_all, strings.mod_panel.unselect_all_tooltip
    )
    HIGHLIGHT_STALE = ModButtonMeta(
        strings.mod_panel.highlight_stale, strings.mod_panel.highlight_stale_tooltip
    )
    UNHIGHLIGHT_STALE = ModButtonMeta(
        strings.mod_panel.unhighlight_stale, strings.mod_panel.unhighlight_stale_tooltip
    )
    UNSUB_SELECTED = ModButtonMeta(
        strings.mod_panel.unsub_selected,
        strings.mod_panel.unsub_selected_tooltip,
    )
    SELECT_STALE = ModButtonMeta(
        strings.mod_panel.select_stale,
        strings.mod_panel.select_stale_tooltip,
    )
    VALIDATE = ModButtonMeta(
        strings.mod_panel.validate,
        strings.mod_panel.validate_tooltip,
    )

    @property
    def label(self) -> str:
        return self.value.label

    @property
    def tooltip(self) -> str:
        return self.value.tooltip


class ButtonType(Enum):
    SERVERS = ButtonTypeMeta(
        strings.buttons.servers_label,
        strings.buttons.servers_tooltip,
        NotebookPage.SERVERS,
    )
    MODS = ButtonTypeMeta(
        strings.buttons.mods_label,
        strings.buttons.mods_tooltip,
        NotebookPage.MODS,
    )
    OPTIONS = ButtonTypeMeta(
        strings.buttons.options_label,
        strings.buttons.options_tooltip,
        NotebookPage.OPTIONS,
    )
    HELP = ButtonTypeMeta(
        strings.buttons.help_label,
        strings.buttons.help_tooltip,
        NotebookPage.HELP,
    )
    EXIT = ButtonTypeMeta(
        strings.buttons.exit_label,
        strings.buttons.exit_tooltip,
        None,
    )

    @property
    def label(self) -> str:
        return self.value.label

    @property
    def tooltip(self) -> str:
        return self.value.tooltip

    @property
    def opens(self) -> NotebookPage | None:
        return self.value.opens


HELP_MENU_ROWS = (
    RowType.CHANGELOG,
    RowType.SHOW_LOG,
    RowType.DUMP_LOG,
    RowType.SEPARATOR,
    RowType.DOCS,
    RowType.DOCS_FALLBACK,
    RowType.BUGS,
    RowType.FORUM,
    RowType.SPONSOR,
    RowType.SEPARATOR,
    RowType.THANKS,
)
