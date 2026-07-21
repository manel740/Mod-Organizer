from __future__ import annotations

from core.models import (
    JVMCode,
    JVMException,
)

from core.parsers.byte_reader import ByteReader
from core.parsers.attribute_parser import AttributeParser
from core.parsers.instruction_parser import InstructionParser
from core.parsers.constant_pool_resolver import ConstantPoolResolver


class CodeAttributeParser:

    def __init__(
        self,
        resolver: ConstantPoolResolver
    ):

        self.attribute_parser = AttributeParser()

        self.instruction_parser = InstructionParser(
            resolver
        )

    def parse(
        self,
        data: bytes
    ) -> JVMCode:

        reader = ByteReader(data)

        code = JVMCode()

        code.max_stack = reader.u2()

        code.max_locals = reader.u2()

        length = reader.u4()

        code.code = reader.read(length)

        code.instructions = (
            self.instruction_parser.parse(
                code.code
            )
        )

        exceptions = reader.u2()

        for _ in range(exceptions):

            exception = JVMException()

            exception.start_pc = reader.u2()

            exception.end_pc = reader.u2()

            exception.handler_pc = reader.u2()

            exception.catch_type = reader.u2()

            code.exceptions.append(
                exception
            )

        code.attributes = (
            self.attribute_parser.parse_all(
                reader
            )
        )

        return code 