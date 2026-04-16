from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ConsoleApp:
    auth_controller: Any
    usuarios_controller: Any
    categorias_controller: Any
    herramientas_controller: Any
    prestamos_controller: Any
    reportes_controller: Any
    logger: Any

    def run(self) -> None:
        from presentation.menus.menu_general import run_menu_general

        run_menu_general(
            auth_controller=self.auth_controller,
            usuarios_controller=self.usuarios_controller,
            categorias_controller=self.categorias_controller,
            herramientas_controller=self.herramientas_controller,
            prestamos_controller=self.prestamos_controller,
            reportes_controller=self.reportes_controller,
            logger=self.logger,
        )

