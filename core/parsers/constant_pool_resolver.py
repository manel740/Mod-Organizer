from __future__ import annotations

from core.models import (
    ConstantPool,
    CPUtf8,
    CPClass,
    CPString,
    CPNameAndType,
    CPFieldRef,
    CPMethodRef,
    CPInterfaceMethodRef,
)


class ConstantPoolResolver:

    def __init__(
        self,
        pool: ConstantPool
    ):

        self.pool = pool

    def entry(
        self,
        index: int
    ) -> object:

        if index <= 0 or index >= len(self.pool):

            raise IndexError(
                f"Índice de Constant Pool inválido: {index}"
            )

        return self.pool[index]

    def utf8(
        self,
        index: int
    ) -> str:

        entry = self.entry(index)

        if not isinstance(
            entry,
            CPUtf8
        ):

            raise TypeError(
                "Se esperaba una entrada CPUtf8."
            )

        return entry.value

    def class_name(
        self,
        index: int
    ) -> str:

        entry = self.entry(index)

        if not isinstance(
            entry,
            CPClass
        ):

            raise TypeError(
                "Se esperaba una entrada CPClass."
            )

        return self.utf8(
            entry.name_index
        )

    def string(
        self,
        index: int
    ) -> str:

        entry = self.entry(index)

        if not isinstance(
            entry,
            CPString
        ):

            raise TypeError(
                "Se esperaba CPString."
            )

        return self.utf8(
            entry.string_index
        )
    
    def name_and_type(
        self,
        index: int
    ) -> tuple[str, str]:

        entry = self.entry(index)

        if not isinstance(
            entry,
            CPNameAndType
        ):

            raise TypeError(
                "Se esperaba CPNameAndType."
            )

        return (
            self.utf8(
                entry.name_index
            ),
            self.utf8(
                entry.descriptor_index
            )
        )

    def fieldref(
        self,
        index: int
    ) -> tuple[str, str, str]:

        entry = self.entry(index)

        if not isinstance(
            entry,
            CPFieldRef
        ):

            raise TypeError(
                "Se esperaba CPFieldRef."
            )

        owner = self.class_name(
            entry.class_index
        )

        name, descriptor = self.name_and_type(
            entry.name_and_type_index
        )

        return (
            owner,
            name,
            descriptor
        )

    def methodref(
        self,
        index: int
    ) -> tuple[str, str, str]:

        entry = self.entry(index)

        if not isinstance(
            entry,
            CPMethodRef
        ):

            raise TypeError(
                "Se esperaba CPMethodRef."
            )

        owner = self.class_name(
            entry.class_index
        )

        name, descriptor = self.name_and_type(
            entry.name_and_type_index
        )

        return (
            owner,
            name,
            descriptor
        )
    
    def interface_methodref(
        self,
        index: int
    ) -> tuple[str, str, str]:

        entry = self.entry(index)

        if not isinstance(
            entry,
            CPInterfaceMethodRef
        ):

            raise TypeError(
                "Se esperaba CPInterfaceMethodRef."
            )

        owner = self.class_name(
            entry.class_index
        )

        name, descriptor = self.name_and_type(
            entry.name_and_type_index
        )

        return (
            owner,
            name,
            descriptor
        )