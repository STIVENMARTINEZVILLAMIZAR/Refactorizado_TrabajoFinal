from __future__ import annotations

from typing import List, Optional

from domain.dtos import ActualizarCategoriaDTO, CrearCategoriaDTO
from domain.entities import Categoria
from infrastructure.ports.logger import AuditLogRepository
from infrastructure.ports.repositories import CategoriaRepository


class GestionCategorias:
    def __init__(self, categoria_repo: CategoriaRepository, logger: AuditLogRepository | None = None) -> None:
        self._categoria_repo = categoria_repo
        self._logger = logger

    def crear(self, dto: CrearCategoriaDTO) -> Categoria:
        payload = {"nombre": dto.nombre}
        # El adaptador JSON espera la clave `id` al agregar.
        saved = self._categoria_repo.add(payload)
        entity = Categoria.from_dict(saved)
        if self._logger:
            self._logger.append(f"Se ha creado una categoria con id={entity.id}")
        return entity

    def listar(self) -> List[Categoria]:
        return [Categoria.from_dict(x) for x in self._categoria_repo.list_all()]

    def get_por_id(self, categoria_id: int) -> Optional[Categoria]:
        data = self._categoria_repo.get_by_id(int(categoria_id))
        if not data:
            return None
        return Categoria.from_dict(data)

    def actualizar(self, dto: ActualizarCategoriaDTO) -> Optional[Categoria]:
        existing = self._categoria_repo.get_by_id(int(dto.categoria_id))
        if not existing:
            return None
        updated = {**existing, "nombre": dto.nombre}
        self._categoria_repo.update(updated)
        entity = Categoria.from_dict(updated)
        if self._logger:
            self._logger.append(f"Se ha actualizado una categoria con id={entity.id}")
        return entity

    def eliminar(self, categoria_id: int) -> bool:
        if not self._categoria_repo.get_by_id(int(categoria_id)):
            return False
        self._categoria_repo.delete_by_id(int(categoria_id))
        if self._logger:
            self._logger.append(f"Se ha eliminado una categoria con id={int(categoria_id)}")
        return True

