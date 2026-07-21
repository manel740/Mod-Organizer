from __future__ import annotations

from core.scanner import ModScanner
from core.metadata_parser import MetadataParser
from core.classifier import Classifier
from core.models import ModResult

from core.analyzers.classes import ClassAnalyzer
from core.analyzers.mixins import MixinAnalyzer


class AnalysisEngine:

    def __init__(self):

        self.metadata_parser = MetadataParser()

        self.classifier = Classifier()

        self.class_analyzer = ClassAnalyzer()

        self.mixin_analyzer = MixinAnalyzer()

    def analyze_folder(self, folder):

        scanner = ModScanner(folder)

        mods = scanner.scan()

        results = []

        for mod in mods:

            result = self.analyze_mod(mod)

            results.append(result)

        return results

    def analyze_mod(self, mod):

        metadata = self.metadata_parser.parse(mod.path)

        class_info = self.class_analyzer.analyze(mod.path)

        mixin_info = self.mixin_analyzer.analyze(mod.path)

        classification = self.classifier.classify(
            metadata,
            class_info
        )

        result = ModResult()

        result.name = metadata.name or mod.name
        result.file_name = mod.name
        result.path = mod.path

        result.loader = metadata.loader

        result.side = classification.side

        result.confidence = classification.confidence

        result.depends = list(metadata.depends)

        result.mod_id = metadata.mod_id

        result.version = metadata.version

        result.description = metadata.description

        result.client_score = class_info["client_score"]

        result.server_score = class_info["server_score"]

        result.class_score = (
            class_info["client_score"]
            + class_info["server_score"]
        )

        result.mixin_score = (
            mixin_info["client_score"]
            + mixin_info["server_score"]
        )

        result.classes = class_info["classes"]

        result.resources = class_info["resources"]

        result.metadata_found = True

        result.mixins_found = (
            len(mixin_info["mixins"]) > 0
        )

        return result