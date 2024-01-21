import string
import sys
from typing import List, Iterable, Tuple, Optional, Set
import random
import winreg  # TODO windows only!

from PySide6.QtCore import QObject, Slot, QAbstractItemModel, QModelIndex, QAbstractListModel, Qt, QSortFilterProxyModel
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget
from MainWindow_ui import Ui_MainWindow
from ModSelector_ui import Ui_ModSelector
from pathlib import Path


PZ_HOME_DIR = Path.home() / "Zomboid"


class GeneratedElement(QObject):
    """Just a helper class for creating multiple instances of the same UI widget"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.uid = "".join(random.choice(string.ascii_lowercase) for _ in range(8))

    def unique(self, what: str):
        return f"{what}_{self.uid}"

    def fix_object_name(self, what: QObject):
        what.setObjectName(f"{self.unique(what.objectName())}")


class PZModInfo:
    """Represents the contents of the mod.info file that is part of every mod"""

    # noinspection PyPep8Naming
    # noinspection PyShadowingBuiltins
    def __init__(self,
                 name: str,
                 id: str,
                 poster: Optional[List[Path]] = None,
                 require: Optional[List[str]] = None,
                 versionMin: Optional[str] = None,
                 versionMax: Optional[str] = None,
                 description: Optional[List[str]] = None,
                 pack: Optional[List[Path]] = None,
                 tiledef: Optional[List[str]] = None,
                 url: Optional[List[str]] = None,
                 icon: Optional[str] = None,
                 authors: Optional[List[str]] = None,
                 **kwargs
                 ):
        """
        :param name: The name of the mod
        :param id: The id of the mod
        :param poster: Cover image(s)
        :param require: Mod ID(s) of dependencies
        :param versionMin: Lowest compatible game version
        :param versionMax: Highest compatible game version
        :param description: The description displayed in the mod menu
        :param url: Website URL
        :param pack: Third-party texture pack(s)
        :param tiledef: File(s) with tile parameters
        """
        assert name
        assert id
        self.name = name
        self.id = id
        self.poster = poster
        self.require = require
        self.versionMin = versionMin
        self.versionMax = versionMax
        self.description = "\n".join(description)
        self.pack = pack
        self.tiledef = tiledef
        self.url = url
        self.icon = icon
        self.authors = authors
        self.extra_fields = kwargs

    @staticmethod
    def from_info_file(mod_info_file: Path):
        data = {"name": "", "id": ""}
        with open(mod_info_file) as f:
            for line in f.readlines():
                line = line.strip()
                if not line:
                    continue
                key, value = line.split("=")
                if key not in data:
                    data[key] = []
                if isinstance(data[key], list):
                    data[key].append(value)
                else:
                    data[key] = value
        return PZModInfo(**data)


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
            return self.items[index.row()].modInfo.name
        elif role == Qt.ItemDataRole.BackgroundRole:
            pass

    def removeRows(self, row, count, parent=...):
        super().beginRemoveRows(parent, row, row+count)
        for _ in range(count):
            del self.items[row]
            del self.indices[row]
        super().endRemoveRows()


def get_steam_path() -> Path:
    # On Windows, the Steam installation location can be read from HKEY_CURRENT_USER\SOFTWARE\Valve\Steam\SteamPath
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\Valve\\Steam") as handle:
        steam_path = winreg.QueryValueEx(handle, "SteamPath")[0]
    return Path(steam_path)


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
        filterModel_disabled = QSortFilterProxyModel(parent=self.widget)
        filterModel_disabled.setSourceModel(model)
        self.ui.list_disabled.setModel(filterModel_disabled)

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
