from __future__ import annotations

from core.models import JVMField

from core.parsers.byte_reader import ByteReader
from core.parsers.attribute_parser import AttributeParser


class FieldParser:

    def __init__(self):

        self.attribute_parser = AttributeParser()
    
    def parse(
        self,
        reader: ByteReader
    ) -> JVMField:

        field = JVMField()

        field.access_flags = reader.u2()

        field.name_index = reader.u2()

        field.descriptor_index = reader.u2()

        field.attributes = self.attribute_parser.parse_all(
            reader
        )

        return field
    
    def parse_all(
        self,
        reader: ByteReader
    ) -> list[JVMField]:

        count = reader.u2()

        fields: list[JVMField] = []

        for _ in range(count):

            fields.append(
                self.parse(reader)
            )

        return fields