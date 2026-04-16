from __future__ import annotations

from typing import List, Optional

from application.gestion_herramientas import GestionHerramientas
from domain.dtos import ActualizarHerramientaDTO, CrearHerramientaDTO
from domain.entities import Herramienta


class HerramientasController:
    def __init__(self, service: GestionHerramientas) -> None:
        self._service = service

    def crear_herramienta(self, dto: CrearHerramientaDTO) -> Herramienta:
        return self._service.crear(dto)

    def listar_herramientas(self) -> List[Herramienta]:
        return self._service.listar()

    def obtener_herramienta(self, herramienta_id: int) -> Optional[Herramienta]:
        return self._service.get_por_id(herramienta_id)

    def actualizar_herramienta(self, dto: ActualizarHerramientaDTO) -> Optional[Herramienta]:
        return self._service.actualizar(dto)

    def eliminar_herramienta(self, herramienta_id: int) -> bool:
        return self._service.eliminar(herramienta_id)

