from __future__ import annotations

from core.models import (
    ConstantPool,
    CPEntry,
    CPUtf8,
    CPInteger,
    CPFloat,
    CPLong,
    CPDouble,
    CPClass,
    CPString,
    CPFieldRef,
    CPMethodRef,
    CPInterfaceMethodRef,
    CPNameAndType,
    CPMethodHandle,
    CPMethodType,
    CPDynamic,
    CPInvokeDynamic,
    CPModule,
    CPPackage,
)

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


class ConstantPoolParser:

    def parse(
        self,
        reader: ByteReader
    ) -> ConstantPool:

        count = reader.u2()

        pool = ConstantPool()

        # El índice 0 no existe según la especificación JVM.
        pool.append(None)

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

    def _read_entry(
        self,
        tag: int,
        reader: ByteReader
    ) -> CPEntry:

        if tag == CONSTANT_Utf8:
            return self._utf8(reader)

        if tag == CONSTANT_Integer:
            return self._integer(reader)

        if tag == CONSTANT_Float:
            return self._float(reader)

        if tag == CONSTANT_Long:
            return self._long(reader)

        if tag == CONSTANT_Double:
            return self._double(reader)

        if tag == CONSTANT_Class:
            return self._class(reader)

        if tag == CONSTANT_String:
            return self._string(reader)

        if tag == CONSTANT_Fieldref:
            return self._fieldref(reader)

        if tag == CONSTANT_Methodref:
            return self._methodref(reader)

        if tag == CONSTANT_InterfaceMethodref:
            return self._interface_methodref(reader)

        if tag == CONSTANT_NameAndType:
            return self._name_and_type(reader)

        if tag == CONSTANT_MethodHandle:
            return self._method_handle(reader)

        if tag == CONSTANT_MethodType:
            return self._method_type(reader)

        if tag == CONSTANT_Dynamic:
            return self._dynamic(reader)

        if tag == CONSTANT_InvokeDynamic:
            return self._invoke_dynamic(reader)

        if tag == CONSTANT_Module:
            return self._module(reader)

        if tag == CONSTANT_Package:
            return self._package(reader)

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

    def _integer(
        self,
        reader: ByteReader
    ) -> CPInteger:

        return CPInteger(
            CONSTANT_Integer,
            reader.i4()
        )

    def _float(
        self,
        reader: ByteReader
    ) -> CPFloat:

        return CPFloat(
            CONSTANT_Float,
            reader.f4()
        )

    def _long(
        self,
        reader: ByteReader
    ) -> CPLong:

        return CPLong(
            CONSTANT_Long,
            reader.i8()
        )

    def _double(
        self,
        reader: ByteReader
    ) -> CPDouble:

        return CPDouble(
            CONSTANT_Double,
            reader.f8()
        )

    def _class(
        self,
        reader: ByteReader
    ) -> CPClass:

        return CPClass(
            CONSTANT_Class,
            reader.u2()
        )

    def _string(
        self,
        reader: ByteReader
    ) -> CPString:

        return CPString(
            CONSTANT_String,
            reader.u2()
        )

    def _name_and_type(
        self,
        reader: ByteReader
    ) -> CPNameAndType:
        
        def _fieldref(
        self,
        reader: ByteReader
    ) -> CPFieldRef:

         return CPFieldRef(
            CONSTANT_Fieldref,
            reader.u2(),
            reader.u2()
        )

    def _methodref(
        self,
        reader: ByteReader
    ) -> CPMethodRef:

        return CPMethodRef(
            CONSTANT_Methodref,
            reader.u2(),
            reader.u2()
        )

    def _interface_methodref(
        self,
        reader: ByteReader
    ) -> CPInterfaceMethodRef:

        return CPInterfaceMethodRef(
            CONSTANT_InterfaceMethodref,
            reader.u2(),
            reader.u2()
        )

    def _method_handle(
        self,
        reader: ByteReader
    ) -> CPMethodHandle:

        return CPMethodHandle(
            CONSTANT_MethodHandle,
            reader.u1(),
            reader.u2()
        )

    def _method_type(
        self,
        reader: ByteReader
    ) -> CPMethodType:

        return CPMethodType(
            CONSTANT_MethodType,
            reader.u2()
        )

    def _dynamic(
        self,
        reader: ByteReader
    ) -> CPDynamic:

        return CPDynamic(
            CONSTANT_Dynamic,
            reader.u2(),
            reader.u2()
        )

    def _invoke_dynamic(
        self,
        reader: ByteReader
    ) -> CPInvokeDynamic:

        return CPInvokeDynamic(
            CONSTANT_InvokeDynamic,
            reader.u2(),
            reader.u2()
        )

    def _module(
        self,
        reader: ByteReader
    ) -> CPModule:

        return CPModule(
            CONSTANT_Module,
            reader.u2()
        )

    def _package(
        self,
        reader: ByteReader
    ) -> CPPackage:

        return CPPackage(
            CONSTANT_Package,
            reader.u2()
        )
        
        

        return CPNameAndType(
            CONSTANT_NameAndType,
            reader.u2(),
            reader.u2()
        )