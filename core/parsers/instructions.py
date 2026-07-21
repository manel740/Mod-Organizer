from __future__ import annotations


OPCODES = {

    0x2A: "aload_0",

    0x2B: "aload_1",

    0x2C: "aload_2",

    0x2D: "aload_3",

    0x12: "ldc",

    0x13: "ldc_w",

    0x14: "ldc2_w",

    0xB2: "getstatic",

    0xB3: "putstatic",

    0xB4: "getfield",

    0xB5: "putfield",

    0xB6: "invokevirtual",

    0xB7: "invokespecial",

    0xB8: "invokestatic",

    0xB9: "invokeinterface",

    0xBA: "invokedynamic",

    0xBB: "new",

    0xBD: "anewarray",

    0xC0: "checkcast",

    0xC1: "instanceof",

    0xB1: "return",

    0xAC: "ireturn",

    0xAD: "lreturn",

    0xAE: "freturn",

    0xAF: "dreturn",

    0xB0: "areturn"

}


def opcode_name(
    opcode: int
) -> str:

    return OPCODES.get(

        opcode,

        f"unknown_{opcode:02X}"

    )