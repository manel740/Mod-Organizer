from __future__ import annotations

import zipfile

from core.models import BytecodeAnalysis


class BytecodeAnalyzer:

    def analyze(
        self,
        jar_path: str
    ) -> BytecodeAnalysis:

     def _scan_class(
        self,
        data: bytes,
        result: BytecodeAnalysis
    ):

        try:

            text = data.decode(

                "latin1",

                errors="ignore"

            )

        except Exception:

            return

        self._find_class_references(

            text,

            result

        )

        self._find_strings(

            text,

            result

        )

    def _find_class_references(
        self,
        text: str,
        result: BytecodeAnalysis
    ):

        prefixes = (

            "net/minecraft/",

            "com/mojang/",

            "net/fabricmc/",

            "org/spongepowered/",

            "cpw/mods/",

            "net/neoforged/"

        )

        words = text.split()

        for word in words:

            for prefix in prefixes:

                if prefix in word:

                    cleaned = self._clean_reference(
                        word
                    )

                    if cleaned:

                        result.class_references.append(
                            cleaned
                        )

                        self._score_reference(
                            cleaned,
                            result
                        )

                    break

    def _find_strings(
        self,
        text: str,
        result: BytecodeAnalysis
    ):

        for piece in text.split():

            if len(piece) < 4:

                continue

            printable = sum(

                c.isprintable()

                for c in piece

            )

            if printable < len(piece) * 0.90:

                continue

            result.string_constants.append(
                piece
            )

    def _clean_reference(
        self,
        value: str
    ) -> str:
            # ==========================================================
    # Score Reference
    # ==========================================================

     def _score_reference(
        self,
        reference: str,
        result: BytecodeAnalysis
    ):

        ref = reference.lower()

        client_rules = {

            "minecraftclient": 25,

            "screen": 15,

            "handledscreen": 18,

            "titlescreen": 20,

            "optionsscreen": 18,

            "render": 12,

            "renderer": 15,

            "gamerenderer": 25,

            "worldrenderer": 22,

            "entityrenderer": 20,

            "texture": 10,

            "texturemanager": 18,

            "shader": 20,

            "posteffect": 20,

            "particle": 12,

            "hud": 15,

            "overlay": 12,

            "font": 10,

            "model": 10,

            "keybinding": 18,

            "keyboard": 15,

            "mouse": 15,

            "soundmanager": 18,

            "clientplaynetworkhandler": 22
        }

        server_rules = {

            "minecraftserver": 25,

            "dedicatedserver": 30,

            "serverplayer": 20,

            "serverworld": 20,

            "serverplaynetworkhandler": 22,

            "commandmanager": 18,

            "commanddispatcher": 18,

            "chunkmanager": 18,

            "playermanager": 20,

            "worldsavehandler": 18,

            "dimensiontype": 15,

            "tickmanager": 15,

            "permission": 15,

            "networkhandler": 15
        }

        for keyword, score in client_rules.items():

            if keyword in ref:

                result.client_score += score

        for keyword, score in server_rules.items():

            if keyword in ref:

                result.server_score += score

        stop = [

            ";",

            "(",

            ")",

            "<",

            ">",

            "[",

            "]",

            "\x00"

        ]

        for char in stop:

            if char in value:

                value = value.split(

                    char,

                    1

                )[0]

        return value.strip()

        result = BytecodeAnalysis()

        try:

            with zipfile.ZipFile(
                jar_path    ,
                "r"
            ) as jar:

                for file in jar.namelist():

                    if not file.endswith(".class"):

                        continue

                    data = jar.read(file)

                    self._scan_class(
                        data,
                        result
                    )

        except Exception:

            pass

        result.class_references = sorted(
            set(result.class_references)
        )

        result.string_constants = sorted(
            set(result.string_constants)
        )

        result.annotations = sorted(
            set(result.annotations)
        )

        return result