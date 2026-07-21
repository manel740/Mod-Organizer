from __future__ import annotations

import zipfile
from pathlib import Path

from core.metadata.fabric import FabricParser
from core.metadata.common import ModMetadata


class MetadataParser:

    def __init__(self):

        self.parsers = [
            FabricParser,
            # ForgeParser,
            # NeoForgeParser,
            # QuiltParser
        ]

    def parse(self, jar_path: str | Path) -> ModMetadata:

        with zipfile.ZipFile(jar_path, "r") as jar:

            for parser in self.parsers:

                if parser.can_parse(jar):

                    return parser.parse(jar)

        meta = ModMetadata()

        meta.loader = "UNKNOWN"

        return meta