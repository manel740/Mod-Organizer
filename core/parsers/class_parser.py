from __future__ import annotations

from core.models import JVMClass

from core.parsers.byte_reader import ByteReader
from core.parsers.constant_pool import ConstantPoolParser
from core.parsers.constant_pool_resolver import ConstantPoolResolver
from core.parsers.field_parser import FieldParser
from core.parsers.method_parser import MethodParser
from core.parsers.attribute_parser import AttributeParser


class ClassParser:

    def __init__(self):

        self.constant_pool_parser = ConstantPoolParser()

        self.field_parser = FieldParser()

        self.attribute_parser = AttributeParser()

    def parse(
        self,
        data: bytes
    ) -> JVMClass:

        reader = ByteReader(data)

        clazz = JVMClass()

        clazz.magic = reader.u4()

        if clazz.magic != 0xCAFEBABE:

            raise ValueError(
                "No es un archivo .class válido."
            )

        clazz.minor_version = reader.u2()

        clazz.major_version = reader.u2()

        clazz.constant_pool = (
            self.constant_pool_parser.parse(
                reader
            )
        )

        resolver = ConstantPoolResolver(
            clazz.constant_pool
        )

        method_parser = MethodParser(
            resolver
        )

        clazz.access_flags = reader.u2()

        clazz.this_class = reader.u2()

        clazz.super_class = reader.u2()

        interfaces_count = reader.u2()

        for _ in range(interfaces_count):

            clazz.interfaces.append(
                reader.u2()
            )

        clazz.fields = (
            self.field_parser.parse_all(
                reader
            )
        )

        clazz.methods = (
            method_parser.parse_all(
                reader
            )
        )

        clazz.attributes = (
            self.attribute_parser.parse_all(
                reader
            )
        )

        return clazz