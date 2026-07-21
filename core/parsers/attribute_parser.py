from __future__ import annotations

from core.models import JVMAttribute
from core.parsers.byte_reader import ByteReader


class AttributeParser:

    def parse(
        self,
        reader: ByteReader
    ) -> list[JVMAttribute]:

        attributes: list[JVMAttribute] = []

        count = reader.u2()

        for _ in range(count):

            attributes.append(

                self.read(
                    reader
                )

            )

        return attributes

    def read(
        self,
        reader: ByteReader
    ) -> JVMAttribute:

        attribute = JVMAttribute()

        attribute.name_index = reader.u2()

        length = reader.u4()

        attribute.info = reader.read(length)

        return attribute