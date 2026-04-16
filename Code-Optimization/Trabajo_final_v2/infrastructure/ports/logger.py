from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional


class AuditLogRepository(ABC):
    """Puerto para registrar eventos relevantes para auditoría."""

    @abstractmethod
    def append(self, message: str, *, at: Optional[datetime] = None) -> None:
        raise NotImplementedError

