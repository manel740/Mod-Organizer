import json
import zipfile

from .common import ModMetadata


class FabricParser:

    FILE_NAME = "fabric.mod.json"

    @classmethod
    def can_parse(cls, jar: zipfile.ZipFile):

        return cls.FILE_NAME in jar.namelist()

    @classmethod
    def parse(cls, jar: zipfile.ZipFile):

        with jar.open(cls.FILE_NAME) as f:

            data = json.load(f)

        meta = ModMetadata()

        meta.loader = "Fabric"

        meta.mod_id = data.get("id", "")

        meta.name = data.get("name", "")

        meta.version = data.get("version", "")

        meta.description = data.get("description", "")

        authors = data.get("authors", [])

        if isinstance(authors, list):
            meta.authors = [str(a) for a in authors]

        elif isinstance(authors, str):
            meta.authors = [authors]

        meta.depends = list(data.get("depends", {}).keys())

        meta.entrypoints = data.get("entrypoints", {})

        meta.files_found = jar.namelist()

        meta.extra = data

        return meta