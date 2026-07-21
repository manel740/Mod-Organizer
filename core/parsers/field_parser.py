from __future__ import annotations

from core.models import JVMField
from core.parsers.byte_reader import ByteReader


class FieldParser:

    def parse(
        self,
        reader: ByteReader,
        attribute_parser
    ) -> list[JVMField]:

        fields: list[JVMField] = []

        field_count = reader.u2()

        for _ in range(field_count):

            field = JVMField()

            field.access_flags = reader.u2()

            field.name_index = reader.u2()

            field.descriptor_index = reader.u2()

            attribute_count = reader.u2()

            for _ in range(attribute_count):

                field.attributes.append(

                    attribute_parser.read(
                        reader
                    )

                )

            fields.append(field)

        return fields