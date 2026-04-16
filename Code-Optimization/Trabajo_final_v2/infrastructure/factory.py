from __future__ import annotations

from infrastructure.config import AppConfig
from infrastructure.json.repositories_json import (
    JsonCategoriaRepository,
    JsonHerramientaRepository,
    JsonPrestamoRepository,
    JsonUsuarioRepository,
)
from infrastructure.paths import ensure_data_dir
from infrastructure.txt.logger_txt import TxtAuditLogRepository


def build_app(config: AppConfig):
    """
    Wiring (container simple) del proyecto.

    Mantiene Open/Closed: si mañana agregas un adaptador SQL/ORM,
    el resto de capas no cambia: sólo aquí se intercambian repositorios.
    """

    ensure_data_dir(config.data_dir)

    # Repositorios
    usuario_repo = JsonUsuarioRepository(config.data_dir)
    categoria_repo = JsonCategoriaRepository(config.data_dir)
    herramienta_repo = JsonHerramientaRepository(config.data_dir)
    prestamo_repo = JsonPrestamoRepository(config.data_dir)

    # Logger
    logger = TxtAuditLogRepository(config.data_dir)

    # Servicios (application)
    from application.auth_service import AuthService
    from application.gestion_categorias import GestionCategorias
    from application.gestion_herramientas import GestionHerramientas
    from application.gestion_prestamos import GestionPrestamos
    from application.gestion_usuarios import GestionUsuarios
    from application.consultas_reportes import ConsultasReportes

    auth_service = AuthService(logger=logger)
    usuarios_service = GestionUsuarios(usuario_repo=usuario_repo, logger=logger)
    categorias_service = GestionCategorias(categoria_repo=categoria_repo, logger=logger)
    herramientas_service = GestionHerramientas(
        herramienta_repo=herramienta_repo,
        categoria_repo=categoria_repo,
        logger=logger,
    )
    prestamos_service = GestionPrestamos(
        prestamo_repo=prestamo_repo,
        usuario_repo=usuario_repo,
        herramienta_repo=herramienta_repo,
        logger=logger,
    )
    reportes_service = ConsultasReportes(
        prestamo_repo=prestamo_repo,
        herramienta_repo=herramienta_repo,
        usuario_repo=usuario_repo,
    )

    # Controladores
    from controllers.auth_controller import AuthController
    from controllers.usuarios_controller import UsuariosController
    from controllers.categorias_controller import CategoriasController
    from controllers.herramientas_controller import HerramientasController
    from controllers.prestamos_controller import PrestamosController
    from controllers.reportes_controller import ReportesController

    auth_controller = AuthController(auth_service)
    usuarios_controller = UsuariosController(usuarios_service)
    categorias_controller = CategoriasController(categorias_service)
    herramientas_controller = HerramientasController(herramientas_service)
    prestamos_controller = PrestamosController(prestamos_service)
    reportes_controller = ReportesController(reportes_service)

    # App/UI (presentation)
    from presentation.app import ConsoleApp
    return ConsoleApp(
        auth_controller=auth_controller,
        usuarios_controller=usuarios_controller,
        categorias_controller=categorias_controller,
        herramientas_controller=herramientas_controller,
        prestamos_controller=prestamos_controller,
        reportes_controller=reportes_controller,
    )


