from __future__ import annotations

import struct


class ByteReader:

    def __init__(
        self,
        data: bytes
    ):

        self.data = data

        self.position = 0

    def tell(self) -> int:

        return self.position

    def seek(
        self,
        offset: int
    ):

        self.position = offset

    def skip(
        self,
        amount: int
    ):

        self.position += amount

    def remaining(self) -> int:

        return len(self.data) - self.position

    def read(
        self,
        size: int
    ) -> bytes:

        value = self.data[
            self.position:
            self.position + size
        ]

        self.position += size

        return value

    def u1(self) -> int:

        return struct.unpack(

            ">B",

            self.read(1)

        )[0]

    def u2(self) -> int:

        return struct.unpack(

            ">H",

            self.read(2)

        )[0]

    def u4(self) -> int:

        return struct.unpack(

            ">I",

            self.read(4)

        )[0]

    def u8(self) -> int:

        return struct.unpack(

            ">Q",

            self.read(8)

        )[0]

    def i1(self):

        return struct.unpack(

            ">b",

            self.read(1)

        )[0]

    def i2(self):

        return struct.unpack(

            ">h",

            self.read(2)

        )[0]

    def i4(self):

        return struct.unpack(

            ">i",

            self.read(4)

        )[0]

    def i8(self):

        return struct.unpack(

            ">q",

            self.read(8)

        )[0]

    def f4(self):

        return struct.unpack(

            ">f",

            self.read(4)

        )[0]

    def f8(self):

        return struct.unpack(

            ">d",

            self.read(8)

        )[0]
    from core.parsers.byte_reader import ByteReader

class ConstantPoolParser:

    def parse(
        self,
        reader: ByteReader
    ) -> list[CPEntry | None]:

        count = reader.u2()

        pool: list[CPEntry | None] = [None]

        index = 1

        while index < count:

            tag = reader.u1()

            entry = self._read_entry(
                tag,
                reader
            )

            pool.append(entry)

            if tag in (
                CONSTANT_Long,
                CONSTANT_Double
            ):

                pool.append(None)

                index += 2

            else:

                index += 1

        return pool
