from __future__ import annotations

from collections import Counter, defaultdict
from typing import DefaultDict, List, Tuple

from domain.entities import Herramienta, Prestamo
from domain.enums import EstadoPrestamo
from infrastructure.ports.repositories import HerramientaRepository, PrestamoRepository, UsuarioRepository


class ConsultasReportes:
    def __init__(
        self,
        prestamo_repo: PrestamoRepository,
        herramienta_repo: HerramientaRepository,
        usuario_repo: UsuarioRepository,
    ) -> None:
        self._prestamo_repo = prestamo_repo
        self._herramienta_repo = herramienta_repo
        self._usuario_repo = usuario_repo

    def stock_minimo(self, stock: int) -> List[Herramienta]:
        resultados: List[Herramienta] = []
        for raw in self._herramienta_repo.list_all():
            herramienta = Herramienta.from_dict(raw)
            if herramienta.cantidad <= int(stock):
                resultados.append(herramienta)
                # Baseline: imprime y retorna en el primer match.
                break
        return resultados

    def prestamos_por_estado_option(self, option: int) -> List[Prestamo]:
        option = int(option)
        if option == 1:
            target = EstadoPrestamo.EN_PROCESO.value
            return [Prestamo.from_dict(x) for x in self._prestamo_repo.list_all() if x.get("estado") == target]
        # Baseline: option 2 => Aceptada o Rechazada
        return [
            Prestamo.from_dict(x)
            for x in self._prestamo_repo.list_all()
            if x.get("estado") in (EstadoPrestamo.ACEPTADA.value, EstadoPrestamo.RECHAZADA.value)
        ]

    def historial_usuarios(self, usuario_id: int) -> List[Prestamo]:
        usuario_id = int(usuario_id)
        prestamos: List[Prestamo] = []
        for raw in self._prestamo_repo.list_all():
            user = raw.get("usuario") or {}
            if user.get("id") == usuario_id:
                prestamos.append(Prestamo.from_dict(raw))
        return prestamos

    def herramienta_mas_usada(self) -> List[Tuple[int, str, int]]:
        """
        Returns: list of (herramienta_id, nombre, contador)
        """
        tools = [Herramienta.from_dict(x) for x in self._herramienta_repo.list_all()]
        prestamos = self._prestamo_repo.list_all()
        contador = Counter()
        for loan in prestamos:
            tool = (loan.get("herramienta") or {})
            tool_id = tool.get("id")
            if tool_id is not None:
                contador[int(tool_id)] += 1

        resultados: List[Tuple[int, str, int]] = []
        for tool in tools:
            count = contador.get(tool.id, 0)
            if count > 0:
                resultados.append((tool.id, tool.nombre, count))
        return resultados

    def usuario_mas_usado(self) -> List[Tuple[int, str, str, int]]:
        usuarios = [x for x in self._usuario_repo.list_all()]
        prestamos = self._prestamo_repo.list_all()
        contador = Counter()
        for loan in prestamos:
            user = (loan.get("usuario") or {})
            user_id = user.get("id")
            if user_id is not None:
                contador[int(user_id)] += 1

        resultados: List[Tuple[int, str, str, int]] = []
        for u in usuarios:
            u_id = int(u.get("id"))
            count = contador.get(u_id, 0)
            if count > 0:
                resultados.append((u_id, str(u.get("nombre")), str(u.get("apellido")), count))
        return resultados

