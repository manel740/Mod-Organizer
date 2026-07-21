from __future__ import annotations

import zipfile

from core.models import ClassAnalysis


class ClassAnalyzer:

    def analyze(
        self,
        jar_path: str
    ) -> ClassAnalysis:

        result = ClassAnalysis()

        try:

            with zipfile.ZipFile(
                jar_path,
                "r"
            ) as jar:

                for name in jar.namelist():

                    if not name.endswith(".class"):

                        continue

                    self._process_class(

                        name,

                        result

                    )

        except Exception:

            pass

        result.packages = sorted(

            set(result.packages)

        )

        result.classes = sorted(

            set(result.classes)

        )

        result.client_classes = sorted(

            set(result.client_classes)

        )

        result.server_classes = sorted(
            set(result.server_classes)
        )

        if result.packages_count:

            result.largest_package = max(
                result.packages_count,
                key=result.packages_count.get
            )

        return result

    def _process_class(
        self,
        class_path: str,
        result: ClassAnalysis
    ):

        result.total_classes += 1

        class_name = class_path[:-6]

        result.classes.append(
            class_name
        )

        if "/" in class_name:

            package = class_name.rsplit(
                "/",
                1
            )[0]

            result.packages.append(
                package
            )

            result.packages_count.setdefault(
                package,
                0
            )

            result.packages_count[package] += 1

        if self._looks_like_client(
            class_name
        ):

            result.client_classes.append(
                class_name
            )

        if self._looks_like_server(
            class_name
        ):

            result.server_classes.append(
                class_name
            )

    def _looks_like_client(
        self,
        class_name: str
    ) -> bool:

        value = class_name.lower()

        keywords = (

            "client",

            "screen",

            "gui",

            "render",

            "renderer",

            "shader",

            "hud",

            "overlay",

            "keybinding",

            "keybind",

            "texture",

            "particle",

            "sound",

            "font",

            "model"

        )

        return any(

            keyword in value

            for keyword in keywords

        )

    def _looks_like_server(
        self,
        class_name: str
    ) -> bool:

        value = class_name.lower()

        keywords = (

            "server",

            "dedicated",

            "command",

            "permission",

            "network",

            "packet",

            "world",

            "chunk",

            "entitytracker",

            "playerlist",

            "dimension",

            "tick",

            "storage",

            "save"

        )

        return any(

            keyword in value

            for keyword in keywords

        )