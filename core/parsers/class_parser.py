from __future__ import annotations

from core.models import JVMClass
from core.parsers.byte_reader import ByteReader
from core.parsers.constant_pool import ConstantPoolParser


class ClassParser:

    def __init__(self):

        self.cp_parser = ConstantPoolParser()

    def parse(
        self,
        data: bytes
    ) -> JVMClass:

     def _read_field(

        self,

        reader: ByteReader

    ):

        from core.models import JVMField

        field = JVMField()

        field.access_flags = reader.u2()

        field.name_index = reader.u2()

        field.descriptor_index = reader.u2()

        attribute_count = reader.u2()

        for _ in range(attribute_count):

            field.attributes.append(

                self._read_attribute(

                    reader

                )

            )

        return field

        reader = ByteReader(data)

        clazz = JVMClass()
        clazz.magic = reader.u4()

        if clazz.magic != 0xCAFEBABE:

            raise ValueError(
                "Archivo .class inválido."
            )

        clazz.minor_version = reader.u2()

        clazz.major_version = reader.u2()

        clazz.constant_pool = self.cp_parser.parse(
            reader
        )

        clazz.access_flags = reader.u2()

        clazz.this_class = reader.u2()

        clazz.super_class = reader.u2()

        interface_count = reader.u2()

        for _ in range(interface_count):

            clazz.interfaces.append(

                reader.u2()

            )

        field_count = reader.u2()

        for _ in range(field_count):

            clazz.fields.append(

                self._read_field(

                    reader

                )

            )

        method_count = reader.u2()

        for _ in range(method_count):

            clazz.methods.append(

                self._read_method(

                    reader

                )

            )

        attribute_count = reader.u2()

        for _ in range(attribute_count):

            clazz.attributes.append(

                self._read_attribute(

                    reader

                )

            )

        return clazz