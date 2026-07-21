from __future__ import annotations


_PRIMITIVES = {
    "V": "void",
    "Z": "boolean",
    "B": "byte",
    "C": "char",
    "S": "short",
    "I": "int",
    "J": "long",
    "F": "float",
    "D": "double",
}


class DescriptorParser:

    def parse_type(
        self,
        descriptor: str
    ) -> str:

        value, _ = self._parse(
            descriptor,
            0
        )

        return value

    def parse_method(
        self,
        descriptor: str
    ) -> tuple[list[str], str]:

        if not descriptor.startswith("("):

            raise ValueError(
                "Descriptor de método inválido."
            )

        index = 1

        parameters: list[str] = []

        while descriptor[index] != ")":

            value, index = self._parse(
                descriptor,
                index
            )

            parameters.append(
                value
            )

        index += 1

        return_type, _ = self._parse(
            descriptor,
            index
        )

        return (
            parameters,
            return_type
        )

    def _parse(
        self,
        descriptor: str,
        index: int
    ) -> tuple[str, int]:

        char = descriptor[index]

        if char in _PRIMITIVES:

            return (
                _PRIMITIVES[char],
                index + 1
            )

        if char == "L":

            end = descriptor.index(
                ";",
                index
            )

            name = descriptor[
                index + 1:end
            ]

            return (
                name.replace(
                    "/",
                    "."
                ),
                end + 1
            )

        if char == "[":

            value, index = self._parse(
                descriptor,
                index + 1
            )

            return (
                value + "[]",
                index
            )

        raise ValueError(
            f"Descriptor inválido: {descriptor}"
        )

    def is_method(
        self,
        descriptor: str
    ) -> bool:

        return descriptor.startswith("(")

    def is_field(
        self,
        descriptor: str
    ) -> bool:

        return not self.is_method(
            descriptor
        )