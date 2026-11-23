from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class ServerLabels:
    browser: str
    saved: str
    recent: str
    lan: str


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


server_labels = ServerLabels(
    browser="Server Browser",
    saved="Saved Servers",
    recent="Recent",
    lan="LAN",
)
