import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from MainWindow_ui import Ui_MainWindow
from pathlib import Path


def load_server_configs():
    server_config_dir = Path.home() / "Zomboid"  # TODO this might not be true on linux


if __name__ == "__main__":
    app = QApplication(sys.argv)

    main_window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(main_window)

    load_server_configs()

    main_window.show()

    sys.exit(app.exec())
