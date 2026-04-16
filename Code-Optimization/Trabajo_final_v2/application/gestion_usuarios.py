from __future__ import annotations

from typing import List, Optional

from domain.dtos import ActualizarUsuarioDTO, CrearUsuarioDTO
from domain.entities import Usuario
from domain.enums import Rol
from infrastructure.ports.logger import AuditLogRepository
from infrastructure.ports.repositories import UsuarioRepository


class GestionUsuarios:
    def __init__(self, usuario_repo: UsuarioRepository, logger: AuditLogRepository | None = None) -> None:
        self._usuario_repo = usuario_repo
        self._logger = logger

    def crear(self, dto: CrearUsuarioDTO) -> Usuario:
        payload = {
            "nombre": dto.nombre,
            "apellido": dto.apellido,
            "telefono": dto.telefono,
            "direccion": dto.direccion,
            "tipo": dto.tipo.value,
        }
        saved = self._usuario_repo.add(payload)
        entity = Usuario.from_dict(saved)
        if self._logger:
            self._logger.append(f"Se ha creado un usuario con id={entity.id}")
        return entity

    def listar(self) -> List[Usuario]:
        return [Usuario.from_dict(x) for x in self._usuario_repo.list_all()]

    def get_por_id(self, usuario_id: int) -> Optional[Usuario]:
        data = self._usuario_repo.get_by_id(int(usuario_id))
        if not data:
            return None
        return Usuario.from_dict(data)

    def actualizar(self, dto: ActualizarUsuarioDTO) -> Optional[Usuario]:
        existing = self._usuario_repo.get_by_id(int(dto.usuario_id))
        if not existing:
            return None

        updated = {
            **existing,
            "nombre": dto.nombre,
            "apellido": dto.apellido,
            "telefono": dto.telefono,
            "direccion": dto.direccion,
            "tipo": dto.tipo.value,
        }
        self._usuario_repo.update(updated)
        entity = Usuario.from_dict(updated)
        if self._logger:
            self._logger.append(f"Se ha actualizado un usuario con id={entity.id}")
        return entity

    def eliminar(self, usuario_id: int) -> bool:
        if not self._usuario_repo.get_by_id(int(usuario_id)):
            return False
        self._usuario_repo.delete_by_id(int(usuario_id))
        if self._logger:
            self._logger.append(f"Se ha eliminado un usuario con id={int(usuario_id)}")
        return True

