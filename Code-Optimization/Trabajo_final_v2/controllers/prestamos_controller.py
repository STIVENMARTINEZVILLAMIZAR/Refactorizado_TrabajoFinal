from __future__ import annotations

from typing import List, Optional, Tuple

from application.gestion_prestamos import GestionPrestamos
from domain.dtos import CrearPrestamoDTO
from domain.entities import Prestamo


class PrestamosController:
    def __init__(self, service: GestionPrestamos) -> None:
        self._service = service

    def solicitar_prestamo(self, dto: CrearPrestamoDTO) -> Prestamo:
        return self._service.solicitar(dto)

    def consultar_prestamos(self, usuario_id: int) -> List[Prestamo]:
        return self._service.consultar_por_usuario(usuario_id)

    def listar_prestamos(self) -> List[Prestamo]:
        return self._service.listar()

    def obtener_prestamo(self, prestamo_id: int) -> Optional[Prestamo]:
        return self._service.get_por_id(prestamo_id)

    def eliminar_prestamo(self, prestamo_id: int) -> bool:
        return self._service.eliminar(prestamo_id)

    def gestionar_prestamo(self, prestamo_id: int) -> Tuple[Prestamo, str]:
        return self._service.intentar_gestionar(prestamo_id)

    def rechazar_prestamo(self, prestamo_id: int, motivo: str) -> Prestamo:
        return self._service.rechazar(prestamo_id, motivo)

