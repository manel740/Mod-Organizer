from __future__ import annotations

from typing import List

from core.metadata.common import ModMetadata


class DependencyChecker:

    @staticmethod
    def check(
        all_mods: List[ModMetadata]
    ):

        installed = set()

        for mod in all_mods:

            if mod.mod_id:

                installed.add(mod.mod_id.lower())

        missing = {}

        for mod in all_mods:

            for dep in mod.depends:

                dep = dep.lower()

                if dep in (
                    "minecraft",
                    "fabricloader",
                    "forge",
                    "java",
                    "neoforge"
                ):
                    continue

                if dep not in installed:

                    missing.setdefault(mod.name, []).append(dep)

        return missing