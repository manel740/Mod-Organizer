from __future__ import annotations


ACC_PUBLIC = 0x0001
ACC_PRIVATE = 0x0002
ACC_PROTECTED = 0x0004
ACC_STATIC = 0x0008
ACC_FINAL = 0x0010

ACC_SUPER = 0x0020
ACC_SYNCHRONIZED = 0x0020

ACC_VOLATILE = 0x0040
ACC_BRIDGE = 0x0040

ACC_TRANSIENT = 0x0080
ACC_VARARGS = 0x0080

ACC_NATIVE = 0x0100

ACC_INTERFACE = 0x0200

ACC_ABSTRACT = 0x0400

ACC_STRICT = 0x0800

ACC_SYNTHETIC = 0x1000

ACC_ANNOTATION = 0x2000

ACC_ENUM = 0x4000

ACC_MODULE = 0x8000


class AccessFlags:

    @staticmethod
    def has(
        flags: int,
        value: int
    ) -> bool:

        return (flags & value) != 0

    @staticmethod
    def is_public(
        flags: int
    ) -> bool:

        return AccessFlags.has(
            flags,
            ACC_PUBLIC
        )

    @staticmethod
    def is_private(
        flags: int
    ) -> bool:

        return AccessFlags.has(
            flags,
            ACC_PRIVATE
        )

    @staticmethod
    def is_protected(
        flags: int
    ) -> bool:

        return AccessFlags.has(
            flags,
            ACC_PROTECTED
        )

    @staticmethod
    def is_static(
        flags: int
    ) -> bool:

        return AccessFlags.has(
            flags,
            ACC_STATIC
        )

    @staticmethod
    def is_final(
        flags: int
    ) -> bool:

        return AccessFlags.has(
            flags,
            ACC_FINAL
        )

    @staticmethod
    def is_abstract(
        flags: int
    ) -> bool:

        return AccessFlags.has(
            flags,
            ACC_ABSTRACT
        )

    @staticmethod
    def is_interface(
        flags: int
    ) -> bool:

        return AccessFlags.has(
            flags,
            ACC_INTERFACE
        )

    @staticmethod
    def is_enum(
        flags: int
    ) -> bool:

        return AccessFlags.has(
            flags,
            ACC_ENUM
        )

    @staticmethod
    def is_annotation(
        flags: int
    ) -> bool:

        return AccessFlags.has(
            flags,
            ACC_ANNOTATION
        )

    @staticmethod
    def is_native(
        flags: int
    ) -> bool:

        return AccessFlags.has(
            flags,
            ACC_NATIVE
        )

    @staticmethod
    def is_synthetic(
        flags: int
    ) -> bool:

        return AccessFlags.has(
            flags,
            ACC_SYNTHETIC
        )

    @staticmethod
    def is_module(
        flags: int
    ) -> bool:

        return AccessFlags.has(
            flags,
            ACC_MODULE
        )