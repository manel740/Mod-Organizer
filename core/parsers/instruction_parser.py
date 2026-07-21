from __future__ import annotations

from core.models import JVMInstruction
from core.parsers.constant_pool_resolver import ConstantPoolResolver


OPCODES = {
    0x00: "nop",
    0x01: "aconst_null",

    0x02: "iconst_m1",
    0x03: "iconst_0",
    0x04: "iconst_1",
    0x05: "iconst_2",
    0x06: "iconst_3",
    0x07: "iconst_4",
    0x08: "iconst_5",

    0x10: "bipush",
    0x11: "sipush",

    0x12: "ldc",
    0x13: "ldc_w",
    0x14: "ldc2_w",

    0x15: "iload",
    0x19: "aload",

    0x36: "istore",
    0x3A: "astore",

    0x57: "pop",
    0x59: "dup",

    0x60: "iadd",

    0x84: "iinc",

    0x99: "ifeq",
    0x9A: "ifne",

    0xA7: "goto",

    0xAC: "ireturn",
    0xB0: "areturn",
    0xB1: "return",

    0xB2: "getstatic",
    0xB3: "putstatic",

    0xB4: "getfield",
    0xB5: "putfield",

    0xB6: "invokevirtual",
    0xB7: "invokespecial",
    0xB8: "invokestatic",
    0xB9: "invokeinterface",

    0xBB: "new",

    0xBD: "anewarray",

    0xC0: "checkcast",

    0xC1: "instanceof",

    0xC6: "ifnull",

    0xC7: "ifnonnull",
}


OPERAND_SIZES = {

    0x10: 1,
    0x11: 2,

    0x12: 1,
    0x13: 2,
    0x14: 2,

    0x15: 1,
    0x19: 1,

    0x36: 1,
    0x3A: 1,

    0x84: 2,

    0x99: 2,
    0x9A: 2,
    0xA7: 2,

    0xB2: 2,
    0xB3: 2,
    0xB4: 2,
    0xB5: 2,

    0xB6: 2,
    0xB7: 2,
    0xB8: 2,

    0xB9: 4,

    0xBB: 2,

    0xBD: 2,

    0xC0: 2,

    0xC1: 2,

    0xC6: 2,

    0xC7: 2,
}


class InstructionParser:

    def __init__(
        self,
        resolver: ConstantPoolResolver
    ):

        self.resolver = resolver

    def parse(
        self,
        code: bytes
    ) -> list[JVMInstruction]:

        instructions: list[JVMInstruction] = []

        offset = 0

        while offset < len(code):

            opcode = code[offset]

            mnemonic = OPCODES.get(
                opcode,
                f"opcode_{opcode:02X}"
            )

            instruction = JVMInstruction()

            instruction.offset = offset

            instruction.opcode = opcode

            instruction.mnemonic = mnemonic

            size = OPERAND_SIZES.get(
                opcode,
                0
            )

            instruction.operands = code[
                offset + 1:
                offset + 1 + size
            ]

            if (
                len(instruction.operands) == 2
                and opcode in (
                    0xB2,
                    0xB3,
                    0xB4,
                    0xB5,
                    0xB6,
                    0xB7,
                    0xB8,
                    0xBB,
                    0xBD,
                    0xC0,
                    0xC1,
                )
            ):

                instruction.constant_index = int.from_bytes(
                    instruction.operands,
                    "big"
                )

                self._resolve_reference(
                    instruction
                )

            instructions.append(
                instruction
            )

            offset += 1 + size

        return instructions

    def _resolve_reference(
        self,
        instruction: JVMInstruction
    ) -> None:

        try:

            if instruction.mnemonic in (

                "getfield",
                "putfield",
                "getstatic",
                "putstatic"

            ):

                (
                    instruction.owner,
                    instruction.name,
                    instruction.descriptor
                ) = self.resolver.fieldref(
                    instruction.constant_index
                )

            elif instruction.mnemonic in (

                "invokevirtual",
                "invokespecial",
                "invokestatic"

            ):

                (
                    instruction.owner,
                    instruction.name,
                    instruction.descriptor
                ) = self.resolver.methodref(
                    instruction.constant_index
                )

            elif instruction.mnemonic == "invokeinterface":

                (
                    instruction.owner,
                    instruction.name,
                    instruction.descriptor
                ) = self.resolver.interface_methodref(
                    instruction.constant_index
                )

        except Exception:

            pass