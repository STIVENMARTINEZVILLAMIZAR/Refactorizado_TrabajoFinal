from __future__ import annotations

from typing import Optional

from infrastructure.ports.logger import AuditLogRepository


class AuthService:
    """
    Servicio de autenticación desacoplado de la UI.
    Baseline: admin123 y residente123.
    """

    def __init__(self, logger: AuditLogRepository | None = None) -> None:
        self._logger = logger

    def authenticate(self, role_choice: int, password: str) -> Optional[str]:
        role_choice = int(role_choice)
        password = str(password)

        if role_choice == 1 and password == "admin123":
            return "admin"
        if role_choice == 2 and password == "residente123":
            return "residente"

        if self._logger:
            self._logger.append("Intento de login fallido", at=None)
        return None

