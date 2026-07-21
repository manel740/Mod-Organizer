from __future__ import annotations

from core.models import (
    JVMMethod,
    JVMAttribute,
)

from core.parsers.byte_reader import ByteReader
from core.parsers.attribute_parser import AttributeParser
from core.parsers.code_attribute_parser import CodeAttributeParser
from core.parsers.constant_pool_resolver import ConstantPoolResolver


class MethodParser:

    def __init__(
        self,
        resolver: ConstantPoolResolver
    ):

        self.resolver = resolver

        self.attribute_parser = AttributeParser()

        self.code_parser = CodeAttributeParser(
            resolver
        )

    def parse(
        self,
        reader: ByteReader
    ) -> JVMMethod:

        method = JVMMethod()

        method.access_flags = reader.u2()

        method.name_index = reader.u2()

        method.descriptor_index = reader.u2()

        method.attributes = self.attribute_parser.parse_all(
            reader
        )

        for attribute in method.attributes:

            self._parse_attribute(
                method,
                attribute
            )

        return method

    def parse_all(
        self,
        reader: ByteReader
    ) -> list[JVMMethod]:

        count = reader.u2()

        methods: list[JVMMethod] = []

        for _ in range(count):

            methods.append(
                self.parse(
                    reader
                )
            )

        return methods

    def _parse_attribute(
        self,
        method: JVMMethod,
        attribute: JVMAttribute
    ) -> None:

        name = self.resolver.utf8(
            attribute.name_index
        )

        if name == "Code":

            method.code = self.code_parser.parse(
                attribute.info
            )