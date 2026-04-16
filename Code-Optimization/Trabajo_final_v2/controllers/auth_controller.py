from __future__ import annotations

from typing import Optional

from application.auth_service import AuthService


class AuthController:
    def __init__(self, auth_service: AuthService) -> None:
        self._auth_service = auth_service

    def login(self, role_choice: int, password: str) -> Optional[str]:
        return self._auth_service.authenticate(role_choice, password)

