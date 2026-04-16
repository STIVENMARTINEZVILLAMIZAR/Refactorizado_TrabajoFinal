from __future__ import annotations

from datetime import timedelta
from typing import List, Optional, Tuple

from domain.dtos import CrearPrestamoDTO, DecidirPrestamoDTO
from domain.entities import Herramienta, Prestamo, Usuario
from domain.enums import EstadoPrestamo
from infrastructure.ports.logger import AuditLogRepository
from infrastructure.ports.repositories import HerramientaRepository, PrestamoRepository, UsuarioRepository


class GestionPrestamos:
    def __init__(
        self,
        prestamo_repo: PrestamoRepository,
        usuario_repo: UsuarioRepository,
        herramienta_repo: HerramientaRepository,
        logger: AuditLogRepository | None = None,
    ) -> None:
        self._prestamo_repo = prestamo_repo
        self._usuario_repo = usuario_repo
        self._herramienta_repo = herramienta_repo
        self._logger = logger

    def solicitar(self, dto: CrearPrestamoDTO) -> Prestamo:
        usuario_data = self._usuario_repo.get_by_id(int(dto.usuario_id))
        if not usuario_data:
            raise ValueError("Usuario no encontrado")
        herramienta_data = self._herramienta_repo.get_by_id(int(dto.herramienta_id))
        if not herramienta_data:
            raise ValueError("Herramienta no encontrada")

        usuario = Usuario.from_dict(usuario_data)
        herramienta = Herramienta.from_dict(herramienta_data)

        fecha_inicio = dto.fecha_inicio
        fecha_final = fecha_inicio + timedelta(days=int(dto.dias))

        payload = {
            # Baseline: `prestamos.json` embebe `usuario` sin la clave `tipo`.
            "usuario": usuario.to_dict_for_prestamo(),
            "herramienta": herramienta.to_dict(),
            "cantidad": int(dto.cantidad),
            "fecha_inicio": str(fecha_inicio),
            "fecha_final": str(fecha_final),
            "estado": EstadoPrestamo.EN_PROCESO.value,
            "observaciones": "Pendiente",
        }
        saved = self._prestamo_repo.add(payload)
        entity = Prestamo.from_dict(saved)
        if self._logger:
            self._logger.append(f"Se ha creado un préstamo con id={entity.id}")
        return entity

    def listar(self) -> List[Prestamo]:
        return [Prestamo.from_dict(x) for x in self._prestamo_repo.list_all()]

    def get_por_id(self, prestamo_id: int) -> Optional[Prestamo]:
        data = self._prestamo_repo.get_by_id(int(prestamo_id))
        if not data:
            return None
        return Prestamo.from_dict(data)

    def consultar_por_usuario(self, usuario_id: int) -> List[Prestamo]:
        usuario_id = int(usuario_id)
        prestamos = []
        for raw in self._prestamo_repo.list_all():
            loan_user = raw.get("usuario") or {}
            if loan_user.get("id") == usuario_id:
                prestamos.append(Prestamo.from_dict(raw))
        return prestamos

    def eliminar(self, prestamo_id: int) -> bool:
        if not self._prestamo_repo.get_by_id(int(prestamo_id)):
            return False
        self._prestamo_repo.delete_by_id(int(prestamo_id))
        if self._logger:
            self._logger.append(f"Se ha eliminado un préstamo con id={int(prestamo_id)}")
        return True

    def intentar_gestionar(self, prestamo_id: int) -> Tuple[Prestamo, str]:
        """
        Baseline: opción admin [1] Gestionar => acepta si hay stock, si no => rechaza por stock.
        """
        data = self._prestamo_repo.get_by_id(int(prestamo_id))
        if not data:
            raise ValueError("Préstamo no encontrado")

        prestamo = Prestamo.from_dict(data)
        herramienta_actual_data = self._herramienta_repo.get_by_id(prestamo.herramienta.id)
        if not herramienta_actual_data:
            raise ValueError("Herramienta asociada no encontrada")

        herramienta_actual = Herramienta.from_dict(herramienta_actual_data)

        if herramienta_actual.cantidad >= prestamo.cantidad:
            nueva_cantidad = herramienta_actual.cantidad - prestamo.cantidad
            herramienta_dict = herramienta_actual.to_dict()
            herramienta_dict["cantidad"] = nueva_cantidad
            # Se actualiza stock en repositorio de herramientas
            self._herramienta_repo.update(herramienta_dict)

            # Se actualiza estado del préstamo
            data["estado"] = EstadoPrestamo.ACEPTADA.value
            data["observaciones"] = "Se aprueba la solicitud, NO olivdes devolver la herramienta en su fecha destinada"

            # Importante: baseline no actualiza cantidad en el `herramienta` embebido dentro del préstamo.
            self._prestamo_repo.update(data)

            accepted = Prestamo.from_dict(data)
            msg = (
                f"Se acepta la solicitud debido a que hay stock de la herramienta, "
                f"y queda un total de {nueva_cantidad} unidades de esa herramienta en Stock"
            )
            if self._logger:
                self._logger.append(f"Préstamo id={accepted.id} aceptado. Stock restante={nueva_cantidad}")
            return accepted, msg

        # Rechazo por stock insuficiente (baseline)
        data["estado"] = EstadoPrestamo.RECHAZADA.value
        data["observaciones"] = "Se rechaza por no haber stock disponible"
        self._prestamo_repo.update(data)

        rejected = Prestamo.from_dict(data)
        msg = "No se puede gestionar esta solicitud debido a que no hay suficiente Stock"
        if self._logger:
            self._logger.append(
                "Se solicito un prestamo de herramienta pero fue rechazado por no haber suficiente stock solicitado"
            )
        return rejected, msg

    def rechazar(self, prestamo_id: int, motivo: str) -> Prestamo:
        data = self._prestamo_repo.get_by_id(int(prestamo_id))
        if not data:
            raise ValueError("Préstamo no encontrado")

        data["estado"] = EstadoPrestamo.RECHAZADA.value
        data["observaciones"] = str(motivo)
        self._prestamo_repo.update(data)

        rejected = Prestamo.from_dict(data)
        if self._logger:
            self._logger.append(f"Préstamo id={rejected.id} rechazado por motivo provisto por admin")
        return rejected

