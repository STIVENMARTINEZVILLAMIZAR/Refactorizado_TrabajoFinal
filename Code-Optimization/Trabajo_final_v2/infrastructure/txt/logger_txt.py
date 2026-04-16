from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

from infrastructure.ports.logger import AuditLogRepository


@dataclass
class TxtAuditLogRepository(AuditLogRepository):
    data_dir: Path
    filename: str = "historial.txt"

    def _path(self) -> Path:
        return self.data_dir / self.filename

    def append(self, message: str, *, at: Optional[datetime] = None) -> None:
        at = at or datetime.now()
        # Baseline: mensaje + ' en la fecha de ' + str(datetime.now()) y además imprime.
        text = f"{message} en la fecha de {at}"
        print(text)
        self._path().parent.mkdir(parents=True, exist_ok=True)
        with self._path().open("a", encoding="utf-8") as f:
            f.write(text + "\n")

