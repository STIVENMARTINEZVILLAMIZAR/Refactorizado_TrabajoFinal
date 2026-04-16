from __future__ import annotations

from typing import List, Optional

from application.gestion_usuarios import GestionUsuarios
from domain.dtos import ActualizarUsuarioDTO, CrearUsuarioDTO
from domain.entities import Usuario


class UsuariosController:
    def __init__(self, service: GestionUsuarios) -> None:
        self._service = service

    def crear_usuario(self, dto: CrearUsuarioDTO) -> Usuario:
        return self._service.crear(dto)

    def listar_usuarios(self) -> List[Usuario]:
        return self._service.listar()

    def obtener_usuario(self, usuario_id: int) -> Optional[Usuario]:
        return self._service.get_por_id(usuario_id)

    def actualizar_usuario(self, dto: ActualizarUsuarioDTO) -> Optional[Usuario]:
        return self._service.actualizar(dto)

    def eliminar_usuario(self, usuario_id: int) -> bool:
        return self._service.eliminar(usuario_id)

