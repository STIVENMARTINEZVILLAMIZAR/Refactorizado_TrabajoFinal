from __future__ import annotations

import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

# Permite importar paquetes del proyecto incluso si el runner se ejecuta desde otro directorio.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from application.consultas_reportes import ConsultasReportes
from application.gestion_categorias import GestionCategorias
from application.gestion_herramientas import GestionHerramientas
from application.gestion_prestamos import GestionPrestamos
from application.gestion_usuarios import GestionUsuarios
from domain.dtos import CrearCategoriaDTO, CrearHerramientaDTO, CrearPrestamoDTO, CrearUsuarioDTO
from domain.enums import Rol
from infrastructure.json.repositories_json import (
    JsonCategoriaRepository,
    JsonHerramientaRepository,
    JsonPrestamoRepository,
    JsonUsuarioRepository,
)


class TestPrestamos(unittest.TestCase):
    def _crear_flujo_minimo(self, tmp: Path, *, stock_herramienta: int, cantidad_pedido: int):
        categoria_repo = JsonCategoriaRepository(tmp)
        usuario_repo = JsonUsuarioRepository(tmp)
        herramienta_repo = JsonHerramientaRepository(tmp)
        prestamo_repo = JsonPrestamoRepository(tmp)

        categorias_service = GestionCategorias(categoria_repo=categoria_repo, logger=None)
        usuarios_service = GestionUsuarios(usuario_repo=usuario_repo, logger=None)
        herramientas_service = GestionHerramientas(
            herramienta_repo=herramienta_repo, categoria_repo=categoria_repo, logger=None
        )
        prestamos_service = GestionPrestamos(
            prestamo_repo=prestamo_repo,
            usuario_repo=usuario_repo,
            herramienta_repo=herramienta_repo,
            logger=None,
        )
        reportes_service = ConsultasReportes(
            prestamo_repo=prestamo_repo,
            herramienta_repo=herramienta_repo,
            usuario_repo=usuario_repo,
        )

        categoria = categorias_service.crear(CrearCategoriaDTO(nombre="Construcción"))
        usuario = usuarios_service.crear(
            CrearUsuarioDTO(
                nombre="Ana",
                apellido="García",
                telefono=12345,
                direccion="Calle 1",
                tipo=Rol.RESIDENTE,
            )
        )
        herramienta = herramientas_service.crear(
            CrearHerramientaDTO(
                nombre="Taladro",
                categoria_id=categoria.id,
                cantidad=stock_herramienta,
                estado="Activo",
                precio=100,
            )
        )

        prestamo = prestamos_service.solicitar(
            CrearPrestamoDTO(
                usuario_id=usuario.id,
                herramienta_id=herramienta.id,
                cantidad=cantidad_pedido,
                fecha_inicio=date(2026, 4, 1),
                dias=2,
            )
        )

        return {
            "categorias_service": categorias_service,
            "usuarios_service": usuarios_service,
            "herramientas_service": herramientas_service,
            "prestamos_service": prestamos_service,
            "reportes_service": reportes_service,
            "prestamo_repo": prestamo_repo,
            "herramienta_repo": herramienta_repo,
            "prestamo": prestamo,
        }

    def test_aceptar_prestamo_actualiza_stock_y_estado(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            flow = self._crear_flujo_minimo(tmp, stock_herramienta=5, cantidad_pedido=2)

            prestamo_id = flow["prestamo"].id
            prestamo_result, msg = flow["prestamos_service"].intentar_gestionar(prestamo_id)
            self.assertIn("stock", msg.lower() or "")

            herramienta_data = flow["herramienta_repo"].get_by_id(flow["prestamo"].herramienta.id)
            self.assertIsNotNone(herramienta_data)
            self.assertEqual(int(herramienta_data["cantidad"]), 3)

            prestamo_data = flow["prestamo_repo"].get_by_id(prestamo_id)
            self.assertIsNotNone(prestamo_data)
            self.assertEqual(prestamo_data["estado"], "Aceptada")
            self.assertEqual(
                prestamo_data["observaciones"],
                "Se aprueba la solicitud, NO olivdes devolver la herramienta en su fecha destinada",
            )

            # Baseline: `prestamos.json` embebe usuario SIN `tipo`.
            self.assertNotIn("tipo", prestamo_data["usuario"])

            # También el objeto ya parseado debe reflejar el estado.
            self.assertEqual(prestamo_result.estado.value, "Aceptada")

    def test_rechazar_por_stock_insuficiente_actualiza_estado(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            flow = self._crear_flujo_minimo(tmp, stock_herramienta=1, cantidad_pedido=2)

            prestamo_id = flow["prestamo"].id
            prestamo_result, msg = flow["prestamos_service"].intentar_gestionar(prestamo_id)
            self.assertIn("No se puede", msg)

            herramienta_data = flow["herramienta_repo"].get_by_id(flow["prestamo"].herramienta.id)
            self.assertIsNotNone(herramienta_data)
            self.assertEqual(int(herramienta_data["cantidad"]), 1)

            prestamo_data = flow["prestamo_repo"].get_by_id(prestamo_id)
            self.assertIsNotNone(prestamo_data)
            self.assertEqual(prestamo_data["estado"], "Rechazada")
            self.assertEqual(prestamo_data["observaciones"], "Se rechaza por no haber stock disponible")
            self.assertEqual(prestamo_result.estado.value, "Rechazada")

    def test_rechazo_explicito_por_admin(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            flow = self._crear_flujo_minimo(tmp, stock_herramienta=10, cantidad_pedido=2)

            motivo = "No se cuenta con personal para la entrega"
            prestamo_id = flow["prestamo"].id
            prestamo_result = flow["prestamos_service"].rechazar(prestamo_id, motivo)

            prestamo_data = flow["prestamo_repo"].get_by_id(prestamo_id)
            self.assertIsNotNone(prestamo_data)
            self.assertEqual(prestamo_data["estado"], "Rechazada")
            self.assertEqual(prestamo_data["observaciones"], motivo)
            self.assertEqual(prestamo_result.observaciones, motivo)


if __name__ == "__main__":
    unittest.main()

