from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List
import hashlib


# ============================================================
# Modelo de datos
# ============================================================

@dataclass(slots=True)
class ModFile:
    """
    Representa un archivo .jar encontrado.
    """

    path: Path
    name: str
    size: int
    sha1: str


# ============================================================
# Scanner
# ============================================================

class ModScanner:

    def __init__(self, mods_folder: str | Path):

        self.mods_folder = Path(mods_folder)

    # --------------------------------------------------------

    def exists(self) -> bool:
        return self.mods_folder.exists() and self.mods_folder.is_dir()

    # --------------------------------------------------------

    def scan(self) -> List[ModFile]:

        if not self.exists():
            raise FileNotFoundError(
                f"No existe la carpeta: {self.mods_folder}"
            )

        mods: List[ModFile] = []

        for file in sorted(self.mods_folder.iterdir()):

            if not file.is_file():
                continue

            if file.suffix.lower() != ".jar":
                continue

            mod = ModFile(
                path=file,
                name=file.name,
                size=file.stat().st_size,
                sha1=self.calculate_sha1(file)
            )

            mods.append(mod)

        return mods

    # --------------------------------------------------------

    @staticmethod
    def calculate_sha1(path: Path) -> str:

        sha1 = hashlib.sha1()

        with open(path, "rb") as f:

            while True:

                data = f.read(65536)

                if not data:
                    break

                sha1.update(data)

        return sha1.hexdigest()