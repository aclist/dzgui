from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ServerLabels:
    browser: str
    saved: str
    recent: str
    lan: str


@dataclass(slots=True, frozen=True)
class Init:
    is_steam_running: str
    is_dayz_running: str
    requires_steam: str


@dataclass(slots=True, frozen=True)
class Options:
    header: str
    steam_web: str
    enter_steam: str
    steam_placeholder: str
    name_placeholder: str
    last_used: str
    always_fs: str
    steam: str
    flatpak: str
    km: str
    mi: str
    client: str
    window_size: str
    distance: str
    name: str
    manual_dl: str
    auto_dl: str
    update: str
    api_key: str
    prefs: str
    mods: str
    version: str
    branch: str
    stable: str
    testing: str


# General
dz = "DayZ"
dz_exp = "DayZ Experimental"
delimiter = "␞"

# Wait dialogs
ping = "Ping"
mod = "Mod"
_id = "ID"

# Columns
mod_cols = ["Mod", "Symlink", "ID", "Size (MiB)", "Color"]
log_cols = ["Timestamp", "Flag", "Traceback", "Message"]
browser_cols = [
    "Name",
    "Map",
    "View",
    "Gametime",
    "Players",
    "Max",
    "Queue",
    "IP",
    "Qport",
    "Ping",
]

# Errors
server_timeout = "Timed out when querying server(s). Check IP or try again later."


# buttons
ping_servers = "Ping servers"
ping_tooltip = (
    "Refresh the ping for visible servers.\n" "Available once per unique filter context"
)

# use e.g. filters.1pp
filter_1pp = "1PP"
filter_3pp = "3PP"
filter_day = "Day"
filter_night = "Night"
filter_empty = "Empty"
filter_full = "Full"
filter_lowpop = "Low pop"
filter_nonascii = "Non-ASCII"
filter_duplicate = "Duplicate"
filter_official = "Official"
filter_unofficial = "Unofficial"
filter_modded = "Modded"
filter_unmodded = "Unmodded"

# state
unknown = "Unknown"
none_provided = "None provided"
disabled = "Disabled"
enabled = "Enabled"
null = "-"
unspecified = "not specified"

# DLC
dlc_frostline = "Frostline"
dlc_badlands = "Badlands"
dlc_none = "None"

# platform
windows = "Windows"
linux = "Linux"

init = Init(
    is_steam_running="Is Steam running? DZGUI must be run on top of Steam.",
    is_dayz_running="Is DayZ already running? DZGUI cannot launch DayZ if another process is using it.",
    requires_steam="Your chosen client (Steam/Flatpak Steam) must be installed on the system.",
)


options = Options(
    header="Options",
    steam_web="Steam API page",
    enter_steam="Enter your Steam API key",
    steam_placeholder="Steam API key",
    name_placeholder="Identifies you to other players in-game",
    last_used="Last used dimensions",
    always_fs="Always fullscreen",
    steam="Steam",
    flatpak="Flatpak (experimental)",
    km="km (kilometers)",
    mi="mi (miles)",
    client="Steam client",
    window_size="Window size at boot",
    distance="Distance display",
    name="Player name",
    manual_dl="Manual",
    auto_dl="Auto",
    update="Update",
    api_key="API Key",
    prefs="Preferences",
    mods="Mods",
    version="Version",
    branch="DZGUI branch",
    stable="Stable",
    testing="Testing",
)

server_labels = ServerLabels(
    browser="Server Browser",
    saved="Saved Servers",
    recent="Recent",
    lan="LAN",
)
