from __future__ import annotations

from typing import List, Optional

from domain.dtos import CrearHerramientaDTO, ActualizarHerramientaDTO
from domain.entities import Herramienta, Categoria
from domain.enums import EstadoHerramienta
from infrastructure.ports.logger import AuditLogRepository
from infrastructure.ports.repositories import CategoriaRepository, HerramientaRepository


class GestionHerramientas:
    def __init__(
        self,
        herramienta_repo: HerramientaRepository,
        categoria_repo: CategoriaRepository,
        logger: AuditLogRepository | None = None,
    ) -> None:
        self._herramienta_repo = herramienta_repo
        self._categoria_repo = categoria_repo
        self._logger = logger

    def crear(self, dto: CrearHerramientaDTO) -> Herramienta:
        categoria = self._categoria_repo.get_by_id(int(dto.categoria_id))
        if not categoria:
            raise ValueError("Categoria no encontrada")

        estado_str = str(dto.estado)
        payload = {
            "nombre": dto.nombre,
            "categoria": Categoria.from_dict(categoria).to_dict(),
            "cantidad": int(dto.cantidad),
            "estado": estado_str,
            "precio": int(dto.precio),
        }
        saved = self._herramienta_repo.add(payload)
        entity = Herramienta.from_dict(saved)
        if self._logger:
            self._logger.append(f"Se ha creado una herramienta con id={entity.id}")
        return entity

    def listar(self) -> List[Herramienta]:
        return [Herramienta.from_dict(x) for x in self._herramienta_repo.list_all()]

    def get_por_id(self, herramienta_id: int) -> Optional[Herramienta]:
        data = self._herramienta_repo.get_by_id(int(herramienta_id))
        if not data:
            return None
        return Herramienta.from_dict(data)

    def actualizar(self, dto: ActualizarHerramientaDTO) -> Optional[Herramienta]:
        existing = self._herramienta_repo.get_by_id(int(dto.herramienta_id))
        if not existing:
            return None
        categoria = self._categoria_repo.get_by_id(int(dto.categoria_id))
        if not categoria:
            raise ValueError("Categoria no encontrada")

        updated = {
            **existing,
            "nombre": dto.nombre,
            "categoria": Categoria.from_dict(categoria).to_dict(),
            "cantidad": int(dto.cantidad),
            "estado": str(dto.estado),
            "precio": int(dto.precio),
        }
        self._herramienta_repo.update(updated)
        entity = Herramienta.from_dict(updated)
        if self._logger:
            self._logger.append(f"Se ha actualizado una herramienta con id={entity.id}")
        return entity

    def eliminar(self, herramienta_id: int) -> bool:
        if not self._herramienta_repo.get_by_id(int(herramienta_id)):
            return False
        self._herramienta_repo.delete_by_id(int(herramienta_id))
        if self._logger:
            self._logger.append(f"Se ha eliminado una herramienta con id={int(herramienta_id)}")
        return True

