from __future__ import annotations

from core.models import (
    JVMClass,
    BytecodeAnalysis,
)


class BytecodeAnalyzer:

    def analyze(
        self,
        clazz: JVMClass
    ) -> BytecodeAnalysis:

        analysis = BytecodeAnalysis()

        for method in clazz.methods:

            if method.code is None:

                continue

            for instruction in method.code.instructions:

                self._analyze_instruction(
                    instruction,
                    analysis
                )

    def _analyze_instruction(
        self,
        instruction,
        analysis: BytecodeAnalysis
    ) -> None:

        mnemonic = instruction.mnemonic

        if mnemonic.startswith("invoke"):

            analysis.methods += 1

        elif mnemonic in (

            "getfield",
            "putfield",
            "getstatic",
            "putstatic"

        ):

            analysis.fields += 1

        return analysis