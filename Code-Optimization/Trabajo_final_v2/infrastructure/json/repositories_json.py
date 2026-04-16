from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Optional

from infrastructure.json.json_repository import JsonListRepository
from infrastructure.ports.repositories import CategoriaRepository, HerramientaRepository, PrestamoRepository, UsuarioRepository
from infrastructure.paths import FILES


@dataclass
class JsonUsuarioRepository(UsuarioRepository):
    data_dir: Path

    def __post_init__(self) -> None:
        self._repo = JsonListRepository(self.data_dir, FILES["usuarios"])

    def list_all(self):
        return self._repo.list_all()

    def get_by_id(self, entity_id: int) -> Optional[Dict[str, object]]:
        return self._repo.get_by_id(entity_id)

    def add(self, entity: Dict[str, object]) -> Dict[str, object]:
        return self._repo.add(entity)

    def update(self, entity: Dict[str, object]) -> None:
        self._repo.update(entity)

    def delete_by_id(self, entity_id: int) -> None:
        self._repo.delete_by_id(entity_id)


@dataclass
class JsonCategoriaRepository(CategoriaRepository):
    data_dir: Path

    def __post_init__(self) -> None:
        self._repo = JsonListRepository(self.data_dir, FILES["categorias"])

    def list_all(self):
        return self._repo.list_all()

    def get_by_id(self, entity_id: int) -> Optional[Dict[str, object]]:
        return self._repo.get_by_id(entity_id)

    def add(self, entity: Dict[str, object]) -> Dict[str, object]:
        # Baseline categorías.json: {id, nombre}
        # Nuestro dominio usa "nombre" como atributo base.
        saved = self._repo.add(entity)
        return saved

    def update(self, entity: Dict[str, object]) -> None:
        self._repo.update(entity)

    def delete_by_id(self, entity_id: int) -> None:
        self._repo.delete_by_id(entity_id)


@dataclass
class JsonHerramientaRepository(HerramientaRepository):
    data_dir: Path

    def __post_init__(self) -> None:
        self._repo = JsonListRepository(self.data_dir, FILES["herramientas"])

    def list_all(self):
        return self._repo.list_all()

    def get_by_id(self, entity_id: int) -> Optional[Dict[str, object]]:
        return self._repo.get_by_id(entity_id)

    def add(self, entity: Dict[str, object]) -> Dict[str, object]:
        return self._repo.add(entity)

    def update(self, entity: Dict[str, object]) -> None:
        self._repo.update(entity)

    def delete_by_id(self, entity_id: int) -> None:
        self._repo.delete_by_id(entity_id)


@dataclass
class JsonPrestamoRepository(PrestamoRepository):
    data_dir: Path

    def __post_init__(self) -> None:
        self._repo = JsonListRepository(self.data_dir, FILES["prestamos"])

    def list_all(self):
        return self._repo.list_all()

    def get_by_id(self, entity_id: int) -> Optional[Dict[str, object]]:
        return self._repo.get_by_id(entity_id)

    def add(self, entity: Dict[str, object]) -> Dict[str, object]:
        return self._repo.add(entity)

    def update(self, entity: Dict[str, object]) -> None:
        self._repo.update(entity)

    def delete_by_id(self, entity_id: int) -> None:
        self._repo.delete_by_id(entity_id)

