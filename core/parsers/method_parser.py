from __future__ import annotations

from core.models import JVMMethod
from core.parsers.byte_reader import ByteReader


class MethodParser:
    
    def parse(
        self,
        reader: ByteReader,
        attribute_parser
    ) -> list[JVMMethod]:

        methods: list[JVMMethod] = []

        method_count = reader.u2()

        for _ in range(method_count):

            method = JVMMethod()

            method.access_flags = reader.u2()

            method.name_index = reader.u2()

            method.descriptor_index = reader.u2()

            attribute_count = reader.u2()

            for _ in range(attribute_count):

                method.attributes.append(

                    attribute_parser.read(
                        reader
                    )

                )

            methods.append(method)

        return methods