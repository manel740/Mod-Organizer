from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Classification:

    side: str

    confidence: int


class Classifier:

    def classify(self, metadata, analysis):

        client_score = analysis["client_score"]
        server_score = analysis["server_score"]

        entrypoints = metadata.entrypoints

        has_client = "client" in entrypoints
        has_server = "server" in entrypoints
        has_main = "main" in entrypoints

        # Los entrypoints pesan muchísimo
        if has_client:
            client_score += 100

        if has_server:
            server_score += 100

        if has_main:
            client_score += 40
            server_score += 40

        # Decisión

        if client_score == 0 and server_score == 0:

            return Classification(
                side="DESCONOCIDO",
                confidence=0
            )

        difference = abs(client_score - server_score)

        total = max(client_score, server_score)

        confidence = min(
            100,
            60 + difference
        )

        if client_score > server_score:

            side = "CLIENTE"

        elif server_score > client_score:

            side = "SERVIDOR"

        else:

            side = "COMPARTIDO"

        return Classification(
            side=side,
            confidence=confidence
        )