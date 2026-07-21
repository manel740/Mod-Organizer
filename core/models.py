from __future__ import annotations

from dataclasses import dataclass, field

@dataclass(slots=True)
class ModResult:

    name: str = ""
    file_name: str = ""
    path: str = ""

    loader: str = "Desconocido"
    side: str = "Revisar"

    confidence: int = 0

    mod_id: str = ""
    version: str = ""
    description: str = ""

    depends: list[str] = field(default_factory=list)

    client_score: int = 0
    server_score: int = 0

    class_score: int = 0
    mixin_score: int = 0
    resource_score: int = 0
    bytecode_score: int = 0

    warnings: list[str] = field(default_factory=list)

    metadata_found: bool = False
    mixins_found: bool = False

    classes: int = 0
    resources: int = 0

@dataclass(slots=True)
class MetadataResult:

    loader: str = "UNKNOWN"

    mod_id: str = ""
    name: str = ""
    version: str = ""
    description: str = ""

    authors: list[str] = field(default_factory=list)
    contributors: list[str] = field(default_factory=list)

    license: str = ""

    homepage: str = ""
    issues: str = ""
    sources: str = ""

    environment: str = "*"

    entrypoints: dict[str, list[str]] = field(default_factory=dict)

    depends: list[str] = field(default_factory=list)
    recommends: list[str] = field(default_factory=list)
    suggests: list[str] = field(default_factory=list)
    conflicts: list[str] = field(default_factory=list)
    breaks: list[str] = field(default_factory=list)

    mixins: list[str] = field(default_factory=list)

    access_wideners: list[str] = field(default_factory=list)
    access_transformers: list[str] = field(default_factory=list)

    icon: str = ""

    contains_metadata: bool = False

@dataclass(slots=True)
class ClassAnalysis:

    interfaces: list[str] = field(default_factory=list)

    annotations: list[str] = field(default_factory=list)

    inner_classes: list[str] = field(default_factory=list)

    packages_count: dict[str, int] = field(default_factory=dict)

    largest_package: str = ""

    total_classes: int = 0

    packages: list[str] = field(default_factory=list)

    classes: list[str] = field(default_factory=list)

    client_classes: list[str] = field(default_factory=list)

    server_classes: list[str] = field(default_factory=list)


@dataclass(slots=True)
class BytecodeAnalysis:

    class_references: list[str] = field(default_factory=list)

    string_constants: list[str] = field(default_factory=list)

    annotations: list[str] = field(default_factory=list)

    methods: int = 0

    fields: int = 0

    client_score: int = 0

    server_score: int = 0

@dataclass(slots=True)
class JVMAttribute:

    name_index: int = 0

    length: int = 0

    info: bytes = b""


@dataclass(slots=True)
class JVMField:

    access_flags: int = 0

    name_index: int = 0

    descriptor_index: int = 0

    attributes: list[JVMAttribute] = field(default_factory=list)


@dataclass(slots=True)
class JVMInstruction:

    offset: int = 0

    opcode: int = 0

    mnemonic: str = ""

    operands: bytes = b""


@dataclass(slots=True)
class JVMException:

    start_pc: int = 0

    end_pc: int = 0

    handler_pc: int = 0

    catch_type: int = 0


@dataclass(slots=True)
class JVMCode:

    max_stack: int = 0

    max_locals: int = 0

    code: bytes = b""

    instructions: list[JVMInstruction] = field(default_factory=list)

    exceptions: list[JVMException] = field(default_factory=list)

    attributes: list[JVMAttribute] = field(default_factory=list)


@dataclass(slots=True)
class JVMMethod:

    access_flags: int = 0

    name_index: int = 0

    descriptor_index: int = 0

    attributes: list[JVMAttribute] = field(default_factory=list)

    code: JVMCode | None = None


@dataclass(slots=True)
class JVMClass:

    magic: int = 0

    minor_version: int = 0

    major_version: int = 0

    constant_pool: list = field(default_factory=list)

    access_flags: int = 0

    this_class: int = 0

    super_class: int = 0

    interfaces: list[int] = field(default_factory=list)

    fields: list[JVMField] = field(default_factory=list)

    methods: list[JVMMethod] = field(default_factory=list)

    attributes: list[JVMAttribute] = field(default_factory=list)