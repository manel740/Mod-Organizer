from dataclasses import dataclass, field
from typing import List, Dict


@dataclass(slots=True)
class ModMetadata:
    """
    Información común de cualquier mod, sin importar el loader.
    """

    # Loader
    loader: str = "UNKNOWN"

    # Identificación
    mod_id: str = ""
    name: str = ""
    version: str = ""
    description: str = ""

    # Autores
    authors: List[str] = field(default_factory=list)

    # Dependencias
    depends: List[str] = field(default_factory=list)

    # Entrypoints
    entrypoints: Dict[str, List[str]] = field(default_factory=dict)

    # Archivos encontrados dentro del jar
    files_found: List[str] = field(default_factory=list)

    # Información extra específica del loader
    extra: Dict = field(default_factory=dict)