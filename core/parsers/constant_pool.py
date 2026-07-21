from __future__ import annotations

from dataclasses import dataclass

from core.parsers.byte_reader import ByteReader


CONSTANT_Utf8 = 1
CONSTANT_Integer = 3
CONSTANT_Float = 4
CONSTANT_Long = 5
CONSTANT_Double = 6
CONSTANT_Class = 7
CONSTANT_String = 8
CONSTANT_Fieldref = 9
CONSTANT_Methodref = 10
CONSTANT_InterfaceMethodref = 11
CONSTANT_NameAndType = 12
CONSTANT_MethodHandle = 15
CONSTANT_MethodType = 16
CONSTANT_Dynamic = 17
CONSTANT_InvokeDynamic = 18
CONSTANT_Module = 19
CONSTANT_Package = 20


@dataclass(slots=True)
class CPEntry:

    tag: int


@dataclass(slots=True)
class CPUtf8(CPEntry):

    value: str


@dataclass(slots=True)
class CPInteger(CPEntry):

    value: int

@dataclass(slots=True)
class CPFloat(CPEntry):

    value: float


@dataclass(slots=True)
class CPLong(CPEntry):

    value: int


@dataclass(slots=True)
class CPDouble(CPEntry):

    value: float


@dataclass(slots=True)
class CPClass(CPEntry):

    name_index: int


@dataclass(slots=True)
class CPString(CPEntry):

    string_index: int

@dataclass(slots=True)
class CPNameAndType(CPEntry):

    name_index: int

    descriptor_index: int

    class ConstantPoolParser:

     def parse(
        self,
        reader: ByteReader
    ) -> list[CPEntry | None]:

        count = reader.u2()

        # El índice 0 no existe según la especificación
        pool: list[CPEntry | None] = [None]

        index = 1

        while index < count:

            tag = reader.u1()

            entry = self._read_entry(
                tag,
                reader
            )

            pool.append(entry)

            # Long y Double ocupan dos entradas
            if tag in (
                CONSTANT_Long,
                CONSTANT_Double
            ):

                pool.append(None)

                index += 2

            else:

                index += 1

        return pool

    def _read_entry(
        self,
        tag: int,
        reader: ByteReader
    ) -> CPEntry:

        if tag == CONSTANT_Utf8:

            return self._utf8(reader)

        if tag == CONSTANT_Integer:

            return CPInteger(
                tag,
                reader.i4()
            )

        if tag == CONSTANT_Float:

            return CPFloat(
                tag,
                reader.f4()
            )

        if tag == CONSTANT_Long:

            return CPLong(
                tag,
                reader.i8()
            )

        if tag == CONSTANT_Double:

            return CPDouble(
                tag,
                reader.f8()
            )

        if tag == CONSTANT_Class:

            return CPClass(
                tag,
                reader.u2()
            )

        if tag == CONSTANT_String:

            return CPString(
                tag,
                reader.u2()
            )

        if tag == CONSTANT_NameAndType:

            return CPNameAndType(

                tag,

                reader.u2(),

                reader.u2()

            )

        raise ValueError(

            f"Constant Pool tag desconocido: {tag}"

        )


    def _utf8(
        self,
        reader: ByteReader
    ) -> CPUtf8:

        length = reader.u2()

        value = reader.read(length)

        return CPUtf8(

            CONSTANT_Utf8,

            value.decode(

                "utf-8",

                errors="replace"

            )

        )