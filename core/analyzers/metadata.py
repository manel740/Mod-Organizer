from __future__ import annotations

import json
import zipfile

from core.models import MetadataResult


class MetadataAnalyzer:
    """
    Analiza la metadata de un mod de Minecraft.

    Soporta:

    - Fabric
    - Quilt
    - Forge
    - NeoForge

    Este analizador únicamente recopila
    información. No decide si el mod es
    de cliente o servidor.
    """

    # ==========================================================
    # Public API
    # ==========================================================

    def analyze(
        self,
        jar_path: str
    ) -> MetadataResult:

        result = MetadataResult()

        try:

            with zipfile.ZipFile(jar_path, "r") as jar:

                files = set(jar.namelist())

                if "fabric.mod.json" in files:

                    self._fabric(
                        jar,
                        result
                    )

                elif "quilt.mod.json" in files:

                    self._quilt(
                        jar,
                        result
                    )

                elif "META-INF/mods.toml" in files:

                    self._forge(
                        jar,
                        result
                    )

                elif "META-INF/neoforge.mods.toml" in files:

                    self._neoforge(
                        jar,
                        result
                    )

        except Exception:

            pass

        return result

    # ==========================================================
    # Fabric
    # ==========================================================

    def _fabric(
        self,
        jar,
        result
    ):

        try:

            with jar.open(
                "fabric.mod.json"
            ) as file:

                data = json.load(file)

        except Exception:

            return

        result.loader = "FABRIC"

        result.contains_metadata = True

        self._read_basic(
            data,
            result
        )

        self._read_authors(
            data,
            result
        )

        self._read_contacts(
            data,
            result
        )

        self._read_environment(
            data,
            result
        )

        self._read_entrypoints(
            data,
            result
        )

        self._read_dependencies(
            data,
            result
        )

        self._read_mixins(
            data,
            result
        )

        self._read_access_widener(
            data,
            result
        )

    # ==========================================================
    # Quilt
    # ==========================================================

    def _quilt(
        self,
        jar,
        result
    ):

        pass

    # ==========================================================
    # Forge
    # ==========================================================

    def _forge(
        self,
        jar,
        result
    ):

        pass

    # ==========================================================
    # NeoForge
    # ==========================================================

    def _neoforge(
        self,
        jar,
        result
    ):

        pass

    # ==========================================================
    # Basic Information
    # ==========================================================

    def _read_basic(
        self,
        data,
        result
    ):

        result.mod_id = str(
            data.get(
                "id",
                ""
            )
        )

        result.name = str(
            data.get(
                "name",
                ""
            )
        )

        result.version = str(
            data.get(
                "version",
                ""
            )
        )

        result.description = str(
            data.get(
                "description",
                ""
            )
        )

        license_value = data.get(
            "license",
            ""
        )

        if isinstance(
            license_value,
            list
        ):

            result.license = ", ".join(
                str(x)
                for x in license_value
            )

        else:

            result.license = str(
                license_value
            )

        icon = data.get(
            "icon",
            ""
        )

        if isinstance(
            icon,
            dict
        ):

            if icon:

                result.icon = str(
                    next(
                        iter(
                            icon.values()
                        )
                    )
                )

        else:

            result.icon = str(icon)

    # ==========================================================
    # Authors
    # ==========================================================

    def _read_authors(
        self,
        data,
        result
    ):

        result.authors = self._normalize_people(
            data.get(
                "authors",
                []
            )
        )

        result.contributors = self._normalize_people(
            data.get(
                "contributors",
                []
            )
        )

    # ----------------------------------------------------------

    def _normalize_people(
        self,
        value
    ):

        people = []

        if not value:

            return people

        if isinstance(
            value,
            list
        ):

            for person in value:

                if isinstance(
                    person,
                    str
                ):

                    person = person.strip()

                    if person:

                        people.append(
                            person
                        )

                    continue

                if isinstance(
                    person,
                    dict
                ):

                    name = person.get(
                        "name",
                        ""
                    )

                    if name:

                        people.append(
                            str(name)
                        )

        elif isinstance(
            value,
            str
        ):

            value = value.strip()

            if value:

                people.append(
                    value
                )

        unique = []

        seen = set()

        for person in people:

            key = person.lower()

            if key in seen:

                continue

            seen.add(key)

            unique.append(person)

        return unique
        # ==========================================================
    # Contact Information
    # ==========================================================

    def _read_contacts(
        self,
        data,
        result
    ):

        contact = data.get(
            "contact",
            {}
        )

        if not isinstance(
            contact,
            dict
        ):
            return

        result.homepage = str(
            contact.get(
                "homepage",
                ""
            )
        )

        result.issues = str(
            contact.get(
                "issues",
                ""
            )
        )

        result.sources = str(
            contact.get(
                "sources",
                ""
            )
        )

    # ==========================================================
    # Environment
    # ==========================================================

    def _read_environment(
        self,
        data,
        result
    ):

        environment = data.get(
            "environment",
            "*"
        )

        result.environment = str(
            environment
        )

    # ==========================================================
    # Entrypoints
    # ==========================================================

    def _read_entrypoints(
        self,
        data,
        result
    ):

        entrypoints = data.get(
            "entrypoints",
            {}
        )

        if not isinstance(
            entrypoints,
            dict
        ):
            return

        normalized = {}

        for key, values in entrypoints.items():

            normalized[key] = []

            if isinstance(
                values,
                list
            ):

                for value in values:

                    if isinstance(
                        value,
                        str
                    ):

                        normalized[key].append(
                            value
                        )

                    elif isinstance(
                        value,
                        dict
                    ):

                        adapter = value.get(
                            "value",
                            ""
                        )

                        if adapter:

                            normalized[key].append(
                                str(adapter)
                            )

        result.entrypoints = normalized

    # ==========================================================
    # Dependencies
    # ==========================================================

    def _read_dependencies(
        self,
        data,
        result
    ):

        dependency_types = [

            "depends",

            "recommends",

            "suggests",

            "conflicts",

            "breaks"

        ]

        for dep_type in dependency_types:

            values = data.get(
                dep_type,
                {}
            )

            if not isinstance(
                values,
                dict
            ):
                continue

            destination = getattr(
                result,
                dep_type
            )

            for mod_id in values.keys():

                destination.append(
                    str(mod_id)
                )

        result.depends = sorted(
            set(result.depends)
        )

        result.recommends = sorted(
            set(result.recommends)
        )

        result.suggests = sorted(
            set(result.suggests)
        )

        result.conflicts = sorted(
            set(result.conflicts)
        )

        result.breaks = sorted(
            set(result.breaks)
        )
            # ==========================================================
    # Mixins
    # ==========================================================

    def _read_mixins(
        self,
        data,
        result
    ):

        mixins = data.get(
            "mixins",
            []
        )

        if not mixins:
            return

        if isinstance(
            mixins,
            str
        ):

            result.mixins.append(
                mixins
            )

            return

        if isinstance(
            mixins,
            list
        ):

            for mixin in mixins:

                if isinstance(
                    mixin,
                    str
                ):

                    result.mixins.append(
                        mixin
                    )

                    continue

                if isinstance(
                    mixin,
                    dict
                ):

                    config = mixin.get(
                        "config",
                        ""
                    )

                    if config:

                        result.mixins.append(
                            str(config)
                        )

        result.mixins = sorted(
            set(result.mixins)
        )

    # ==========================================================
    # Access Widener
    # ==========================================================

    def _read_access_widener(
        self,
        data,
        result
    ):

        widener = data.get(
            "accessWidener"
        )

        if widener:

            result.access_wideners.append(
                str(widener)
            )

        result.access_wideners = sorted(
            set(result.access_wideners)
        )

    # ==========================================================
    # Utilities
    # ==========================================================

    def _safe_string(
        self,
        value
    ) -> str:

        if value is None:
            return ""

        return str(value).strip()
        # ==========================================================
    # TOML Parser
    # ==========================================================

    def _parse_toml(
        self,
        text: str
    ) -> dict:

        """
        Parser TOML simplificado.

        Extrae pares clave=valor y secciones.

        Está diseñado específicamente para
        mods.toml y neoforge.mods.toml.

        Más adelante añadiremos soporte para
        listas, tablas y arrays complejos.
        """

        result = {}

        current = result

        for raw_line in text.splitlines():

            line = raw_line.strip()

            # -------------------------

            if not line:

                continue

            if line.startswith("#"):

                continue

            # -------------------------

            if line.startswith("[") and line.endswith("]"):

                section = line[1:-1].strip()

                if section not in result:

                    result[section] = {}

                current = result[section]

                continue

            # -------------------------

            if "=" not in line:

                continue

            key, value = line.split(

                "=",

                1

            )

            key = key.strip()

            value = value.strip()

            if value.startswith('"') and value.endswith('"'):

                value = value[1:-1]

            current[key] = value

        return result

    # ==========================================================
    # Read TOML File
    # ==========================================================

    def _read_toml_file(
        self,
        jar,
        path
    ):

        try:

            with jar.open(path) as file:

                text = file.read().decode(

                    "utf-8",

                    errors="ignore"

                )

        except Exception:

            return None

        return self._parse_toml(text)
        # ==========================================================
    # Forge
    # ==========================================================

    def _forge(
        self,
        jar,
        result
    ):

        data = self._read_toml_file(

            jar,

            "META-INF/mods.toml"

        )

        if not data:

            return

        result.loader = "FORGE"

        result.contains_metadata = True

        self._read_forge_basic(

            data,

            result

        )

    # ==========================================================
    # NeoForge
    # ==========================================================

    def _neoforge(
        self,
        jar,
        result
    ):

        data = self._read_toml_file(

            jar,

            "META-INF/neoforge.mods.toml"

        )

        if not data:

            return

        result.loader = "NEOFORGE"

        result.contains_metadata = True

        self._read_forge_basic(

            data,

            result

        )

    # ==========================================================
    # Forge Basic Information
    # ==========================================================

    def _read_forge_basic(
        self,
        data,
        result
    ):

        mods = data.get(

            "mods",

            {}

        )

        if not isinstance(
            mods,
            dict
        ):

            return

        result.mod_id = self._safe_string(

            mods.get(

                "modId",

                ""

            )

        )

        result.name = self._safe_string(

            mods.get(

                "displayName",

                ""

            )

        )

        result.version = self._safe_string(

            mods.get(

                "version",

                ""

            )

        )

        result.description = self._safe_string(

            mods.get(

                "description",

                ""

            )

        )

        result.license = self._safe_string(

            data.get(

                "license",

                ""

            )

        )
                # -------------------------
        # Authors
        # -------------------------

        authors = data.get(
            "authors",
            ""
        )

        if authors:

            if isinstance(
                authors,
                str
            ):

                result.authors.append(
                    authors
                )

            elif isinstance(
                authors,
                list
            ):

                for author in authors:

                    result.authors.append(
                        self._safe_string(author)
                    )

        # -------------------------
        # Display URL
        # -------------------------

        result.homepage = self._safe_string(
            data.get(
                "displayURL",
                ""
            )
        )

        # -------------------------
        # Logo
        # -------------------------

        result.icon = self._safe_string(
            data.get(
                "logoFile",
                ""
            )
        )

        result.authors = sorted(
            set(result.authors)
        )

    # ==========================================================
    # Quilt
    # ==========================================================

    def _quilt(
        self,
        jar,
        result
    ):

        try:

            with jar.open(
                "quilt.mod.json"
            ) as file:

                data = json.load(file)

        except Exception:

            return

        result.loader = "QUILT"

        result.contains_metadata = True

        loader = data.get(
            "quilt_loader",
            {}
        )

        self._read_quilt_basic(
            loader,
            result
        )
            # ==========================================================
    # Quilt Basic Information
    # ==========================================================

    def _read_quilt_basic(
        self,
        loader,
        result
    ):

        result.mod_id = self._safe_string(
            loader.get(
                "id",
                ""
            )
        )

        result.version = self._safe_string(
            loader.get(
                "version",
                ""
            )
        )

        metadata = loader.get(
            "metadata",
            {}
        )

        if isinstance(
            metadata,
            dict
        ):

            result.name = self._safe_string(
                metadata.get(
                    "name",
                    ""
                )
            )

            result.description = self._safe_string(
                metadata.get(
                    "description",
                    ""
                )
            )

            license_value = metadata.get(
                "license",
                ""
            )

            if isinstance(
                license_value,
                list
            ):

                result.license = ", ".join(
                    str(x)
                    for x in license_value
                )

            else:

                result.license = self._safe_string(
                    license_value
                )

            icon = metadata.get(
                "icon",
                ""
            )

            result.icon = self._safe_string(
                icon
            )

            contributors = metadata.get(
                "contributors",
                {}
            )

            if isinstance(
                contributors,
                dict
            ):

                for name in contributors.keys():

                    result.contributors.append(
                        self._safe_string(name)
                    )

        entrypoints = loader.get(
            "entrypoints",
            {}
        )

        if isinstance(
            entrypoints,
            dict
        ):

            result.entrypoints = {}

            for key, values in entrypoints.items():

                result.entrypoints[key] = []

                if isinstance(
                    values,
                    list
                ):

                    for value in values:

                        result.entrypoints[key].append(
                            self._safe_string(value)
                        )

        depends = loader.get(
            "depends",
            []
        )

        if isinstance(
            depends,
            list
        ):

            for dependency in depends:

                if isinstance(
                    dependency,
                    dict
                ):

                    mod_id = dependency.get(
                        "id",
                        ""
                    )

                    if mod_id:

                        result.depends.append(
                            self._safe_string(mod_id)
                        )

        result.depends = sorted(
            set(result.depends)
        )

        result.contributors = sorted(
            set(result.contributors)
        )
            # ==========================================================
    # Validation
    # ==========================================================

    def _validate(
        self,
        result
    ):

        """
        Normaliza la información obtenida
        antes de devolver el resultado.
        """

        result.mod_id = self._safe_string(
            result.mod_id
        )

        result.name = self._safe_string(
            result.name
        )

        result.version = self._safe_string(
            result.version
        )

        result.description = self._safe_string(
            result.description
        )

        result.license = self._safe_string(
            result.license
        )

        result.icon = self._safe_string(
            result.icon
        )

        result.homepage = self._safe_string(
            result.homepage
        )

        result.issues = self._safe_string(
            result.issues
        )

        result.sources = self._safe_string(
            result.sources
        )

        result.environment = self._safe_string(
            result.environment
        )

        result.authors = sorted(
            set(result.authors)
        )

        result.contributors = sorted(
            set(result.contributors)
        )

        result.depends = sorted(
            set(result.depends)
        )

        result.recommends = sorted(
            set(result.recommends)
        )

        result.suggests = sorted(
            set(result.suggests)
        )

        result.conflicts = sorted(
            set(result.conflicts)
        )

        result.breaks = sorted(
            set(result.breaks)
        )

        result.mixins = sorted(
            set(result.mixins)
        )

        result.access_wideners = sorted(
            set(result.access_wideners)
        )

    # ==========================================================
    # Helpers
    # ==========================================================

    def _has_file(
        self,
        jar,
        path
    ) -> bool:

        try:

            jar.getinfo(path)

            return True

        except KeyError:

            return False