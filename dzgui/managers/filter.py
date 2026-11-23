from typing import TYPE_CHECKING

from dzgui.model.model_factory import ModelFactory
from dzgui.strings import metadata

if TYPE_CHECKING:
    from dzgui.model.model_factory import FastInsertListStore


class FilterManager:
    def __init__(self, show_empty: bool = False, show_full: bool = False) -> None:

        self.map_store = ModelFactory().make_map_store()

        # TODO: namespace under own file: metadata.filters
        self.default_filters = {
            metadata.filter_1pp: True,
            metadata.filter_day: True,
            metadata.filter_empty: show_empty,
            metadata.filter_3pp: True,
            metadata.filter_night: True,
            metadata.filter_full: show_full,
            metadata.filter_official: True,
            metadata.filter_modded: True,
            metadata.filter_lowpop: True,
            metadata.filter_unofficial: True,
            metadata.filter_unmodded: True,
            metadata.filter_duplicate: False,
            metadata.filter_nonascii: False,
        }

        # TODO: strings
        self.tooltips = {
            metadata.filter_1pp: "First-person perspective",
            metadata.filter_day: "In-game time between 0600 and 1759",
            metadata.filter_empty: "Servers with no players",
            metadata.filter_3pp: "Third-person perspective",
            metadata.filter_night: "In-game time between 1800 and 0559",
            metadata.filter_full: "Servers with no open slots",
            metadata.filter_official: "Bohemia official servers",
            metadata.filter_nonascii: "Server names using non-standard, complex glyphs",
            metadata.filter_lowpop: "Current population is under 30% of total",
            metadata.filter_unofficial: "Third-party servers",
            metadata.filter_duplicate: "Duplicates of existing servers (usually spoofed)",
            metadata.filter_modded: "Servers with one or more mods",
            metadata.filter_unmodded: "Servers with no mods",
        }

        self.active_keyword = ""
        self.active_map = (0, metadata.all_maps)
        self.prior_map = metadata.all_maps

        self.enabled_filters = dict(self.default_filters)

    def get_tooltips(self) -> dict[str, str]:
        return self.tooltips

    def set_prior_map(self, name: str) -> None:
        self.prior_map = name

    def get_active_map_name(self) -> str:
        return self.active_map[1]

    def get_active_map(self) -> tuple[int, str]:
        return self.active_map

    def set_active_map(self, ind: int, name: str) -> None:
        self.active_map = (ind, name)

    def get_active_keyword(self) -> str:
        return self.active_keyword

    def set_active_keyword(self, word: str) -> None:
        self.active_keyword = word

    def get_default_filters(self) -> dict[str, bool]:
        """Deep copy of defaults"""
        return dict(self.default_filters)

    def get_filters(self) -> dict[str, bool]:
        return self.enabled_filters

    def set_filter(self, label: str, state: bool) -> None:
        self.enabled_filters[label] = state

    def get_map_store(self) -> "FastInsertListStore":
        return self.map_store

    def reinit_map_store(self) -> None:
        model = ModelFactory().make_map_store()
        model.append([metadata.all_maps])
        self.map_store = model
        self.active_map = (0, metadata.all_maps)

    def append_map(self, row: list[str]) -> None:
        self.map_store.append(row)

    def set_unique_maps(self, maps: list[str]) -> None:
        if maps is None:
            return
        if len(maps) < 1:
            self.reinit_map_store()
            return

        self.reinit_map_store()
        maps.sort()
        clean = [m for m in maps if m != metadata.all_maps]
        for m in clean:
            self.append_map([m])

    def get_all_filters(self) -> tuple[str, ...]:
        map_name = self.get_active_map_name()
        enabled = self.get_filters()
        kw = self.get_active_keyword()
        filters = []
        filters.append(map_name)
        filters.append(kw)
        for filt in enabled:
            if enabled[filt] is False:
                filters.append(filt)
        return tuple(filters)
