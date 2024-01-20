import string
import sys
from typing import List, Iterable, Tuple
import random

import PySide6
from PySide6.QtCore import QObject, Slot
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget
from MainWindow_ui import Ui_MainWindow
from ModSelector_ui import Ui_ModSelector
from pathlib import Path


class GeneratedElement(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.uid = "".join(random.choice(string.ascii_lowercase) for _ in range(8))

    def unique(self, what: str):
        return f"{what}_{self.uid}"

    def fix_object_name(self, what: QObject):
        what.setObjectName(f"{self.unique(what.objectName())}")


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

    @Slot()
    def enable_mods(self):
        print("Enabling mods in " + self.config_name, self.tabber.currentWidget())

    @Slot()
    def disable_mods(self):
        print("Disabling mods in " + self.config_name, self.tabber.currentWidget())


def load_server_configs(tabber: QTabWidget) -> Iterable[ModManager]:
    server_config_dir = Path.home() / "Zomboid" / "Server"  # TODO this might not be true on linux
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
