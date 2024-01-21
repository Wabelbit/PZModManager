import winreg
from pathlib import Path

PZ_HOME_DIR = Path.home() / "Zomboid"


def get_steam_path() -> Path:
    # On Windows, the Steam installation location can be read from HKEY_CURRENT_USER\SOFTWARE\Valve\Steam\SteamPath
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "SOFTWARE\\Valve\\Steam") as handle:
        steam_path = winreg.QueryValueEx(handle, "SteamPath")[0]
    return Path(steam_path)
