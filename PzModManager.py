import os
import sys
import string
from typing import List, Iterable, Optional, Set
import random

from PySide6.QtCore import QObject, Slot, QAbstractListModel, Qt, QSortFilterProxyModel
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget

from pz import PZModInfo
from ui.MainWindow_ui import Ui_MainWindow
from ui.ModSelector_ui import Ui_ModSelector
from pathlib import Path

if os.name == 'nt':
    # noinspection PyUnresolvedReferences
    from win import *
elif os.name == 'posix':
    # noinspection PyUnresolvedReferences
    from linux import *
else:
    raise Exception("Unsupported operating system")


class GeneratedElement(QObject):
    """Just a helper class for creating multiple instances of the same UI widget"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.uid = "".join(random.choice(string.ascii_lowercase) for _ in range(8))

    def unique(self, what: str):
        return f"{what}_{self.uid}"

    def fix_object_name(self, what: QObject):
        what.setObjectName(f"{self.unique(what.objectName())}")


class ModItem:
    """Represents an item in the data-model of the MVC ListView"""
    def __init__(self, mod_info: PZModInfo, enabled: bool, workshop_id: Optional[str]):
        """
        :param mod_info: all info about the mod
        :param enabled: whether the mod is currently enabled
        :param workshop_id: Steam's workshop element ID if this is mod is from the Steam workshop
        """
        super().__init__()
        self.modInfo = mod_info
        self.enabled = enabled
        self.workshopId = workshop_id


class ModItemModel(QAbstractListModel):
    """Represents the data-model of the MVC ListView"""
    def __init__(self, mods: List[ModItem], parent=None):
        super().__init__(parent)
        self.items = mods
        self.indices = []
        for i, modInfo in enumerate(mods):
            self.indices.append(super().createIndex(i, 0, modInfo))

        super().dataChanged.emit(self.indices[0], self.indices[-1], [])

    def index(self, row, column=0, parent=None):
        assert column == 0
        return self.indices[row]

    def parent(self):
        return super().parent()

    def rowCount(self, parent=None):
        return len(self.items)

    def flags(self, index):
        return Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemNeverHasChildren

    def data(self, index, role=...):
        if role == Qt.ItemDataRole.DisplayRole:
            if index.column() > 0:
                return None
            item = self.items[index.row()]
            mod = item.modInfo
            display_string = mod.name
            if item.workshopId:
                display_string += f" [{item.workshopId}]"
            return display_string
        elif role == Qt.ItemDataRole.BackgroundRole:
            pass

    def removeRows(self, row, count, parent=...):
        super().beginRemoveRows(parent, row, row+count)
        for _ in range(count):
            del self.items[row]
            del self.indices[row]
        super().endRemoveRows()


def discover_available_mods() -> List[ModItem]:
    local_mods: List[ModItem]
    workshop_mods: List[ModItem]
    local_mod_dir = PZ_HOME_DIR / "mods"
    workshop_dir = get_steam_path() / "steamapps" / "workshop" / "content" / "108600"

    # discover mods from workshop items (good to know: one workshop item can contain many mods)
    workshop_mods = [ModItem(PZModInfo.from_info_file(mod_info_file), False, item_dir.name)
                     for item_dir in workshop_dir.glob("*/")
                     for mod_info_file in item_dir.glob("mods/*/mod.info")]

    # discover locally installed mods
    local_mods = [ModItem(PZModInfo.from_info_file(mod_info_file), False, None)
                  for mod_info_file in local_mod_dir.glob("*/mod.info") if mod_info_file.parent.name != "examplemod"]

    return sorted(workshop_mods + local_mods, key=lambda mod: mod.modInfo.id)


def read_enabled_mods(server_config: Path, mod_items: List[ModItem]):
    # load enabled mods and items from ini file
    enabled_mods: Set[str] = set()
    enabled_workshop_items: Set[str] = set()
    with server_config.open() as f:
        for line in f.readlines():
            line = line.strip()
            if line.startswith("Mods="):
                enabled_mods.update(line[len("Mods="):].split(';'))
            elif line.startswith("WorkshopItems="):
                enabled_workshop_items.update(line[len("WorkshopItems="):].split(';'))

    # go through mod items and set 'enabled' flags accordingly
    for mod in mod_items:
        mod.enabled = mod.modInfo.id in enabled_mods or mod.workshopId in enabled_workshop_items


class ModManager(GeneratedElement):
    def __init__(self, server_config: Path, tabber: QTabWidget):
        # init stuff
        super().__init__(tabber)
        self.tabber = tabber
        self.config_name = server_config.name[:-4]
        self.config_path = server_config

        # create stuff
        self.widget = QWidget()
        self.ui = Ui_ModSelector()
        self.ui.setupUi(self.widget)
        self.fix_object_name(self.widget)

        # set up slots
        self.fix_object_name(self.ui.button_enable)
        self.ui.button_enable.clicked.connect(self.enable_mods)
        self.fix_object_name(self.ui.button_disable)
        self.ui.button_disable.clicked.connect(self.disable_mods)
        print(self.config_name + " slotted", self.ui.button_enable)

        # create data model and set up list views
        all_mods = discover_available_mods()
        read_enabled_mods(server_config, all_mods)
        model = ModItemModel(all_mods, parent=self.widget)
        disabled_filter_model = QSortFilterProxyModel(parent=self.widget)
        disabled_filter_model.setSourceModel(model)
        self.ui.list_disabledMods.setModel(disabled_filter_model)

    @Slot()
    def enable_mods(self):
        print("Enabling mods in " + self.config_name, self.tabber.currentWidget())

    @Slot()
    def disable_mods(self):
        print("Disabling mods in " + self.config_name, self.tabber.currentWidget())


def load_server_configs(tabber: QTabWidget) -> Iterable[ModManager]:
    server_config_dir = PZ_HOME_DIR / "Server"  # TODO this might not be the correct path on linux
    server_configs = server_config_dir.glob("*.ini")

    for config_file in sorted(server_configs):
        yield ModManager(config_file, tabber)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(main_window)

    manager: ModManager
    for manager in load_server_configs(ui.tabWidget):
        ui.tabWidget.addTab(manager.widget, manager.config_name)

    main_window.show()

    sys.exit(app.exec())
