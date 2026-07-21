from __future__ import annotations

from core.models import (
    JVMAttribute
)

from core.parsers.byte_reader import ByteReader


class AttributeParser:

    def parse(
        self,
        reader: ByteReader
    ) -> JVMAttribute:

        attribute = JVMAttribute()

        attribute.name_index = reader.u2()

        attribute.length = reader.u4()

        attribute.info = reader.read(
            attribute.length
        )

        return attribute
    
    def parse_all(
        self,
        reader: ByteReader
    ) -> list[JVMAttribute]:

        count = reader.u2()

        attributes: list[JVMAttribute] = []

        for _ in range(count):

            attributes.append(

                self.parse(
                    reader
                )

            )

        return attributes