from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List, Optional


Entity = Dict[str, object]


class BaseRepository(ABC):
    @abstractmethod
    def list_all(self) -> List[Entity]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[Entity]:
        raise NotImplementedError

    @abstractmethod
    def add(self, entity: Entity) -> Entity:
        """
        Agrega una entidad y retorna la entidad guardada (idealmente con `id`).
        """

        raise NotImplementedError

    @abstractmethod
    def update(self, entity: Entity) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete_by_id(self, entity_id: int) -> None:
        raise NotImplementedError


class UsuarioRepository(BaseRepository, ABC):
    pass


class CategoriaRepository(BaseRepository, ABC):
    pass


class HerramientaRepository(BaseRepository, ABC):
    pass


class PrestamoRepository(BaseRepository, ABC):
    pass

