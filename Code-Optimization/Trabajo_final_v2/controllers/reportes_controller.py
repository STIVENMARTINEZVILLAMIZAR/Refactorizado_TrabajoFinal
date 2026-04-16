from __future__ import annotations

from typing import List, Tuple

from application.consultas_reportes import ConsultasReportes
from domain.entities import Herramienta, Prestamo


class ReportesController:
    def __init__(self, service: ConsultasReportes) -> None:
        self._service = service

    def stock_minimo(self, stock: int) -> List[Herramienta]:
        return self._service.stock_minimo(stock)

    def prestamos_por_estado_option(self, option: int) -> List[Prestamo]:
        return self._service.prestamos_por_estado_option(option)

    def historial_usuarios(self, usuario_id: int) -> List[Prestamo]:
        return self._service.historial_usuarios(usuario_id)

    def herramienta_mas_usada(self) -> List[Tuple[int, str, int]]:
        return self._service.herramienta_mas_usada()

    def usuario_mas_usado(self) -> List[Tuple[int, str, str, int]]:
        return self._service.usuario_mas_usado()

