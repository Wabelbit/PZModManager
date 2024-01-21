from pathlib import Path
from typing import Optional, List


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
