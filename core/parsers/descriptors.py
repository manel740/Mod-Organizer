from __future__ import annotations


PRIMITIVES = {

    "V": "void",

    "Z": "boolean",

    "B": "byte",

    "C": "char",

    "S": "short",

    "I": "int",

    "J": "long",

    "F": "float",

    "D": "double"

}


def is_object(
    descriptor: str
) -> bool:

    return descriptor.startswith("L")


def is_array(
    descriptor: str
) -> bool:

    return descriptor.startswith("[")


def is_method(
    descriptor: str
) -> bool:

    return descriptor.startswith("(")


def primitive_name(
    code: str
) -> str:

    return PRIMITIVES.get(

        code,

        code

    )