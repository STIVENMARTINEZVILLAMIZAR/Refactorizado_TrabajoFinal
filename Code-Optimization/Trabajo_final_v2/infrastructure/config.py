from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    """
    Configuración básica para persistencia en archivos.

    Por defecto guarda/lee los JSON/TXT dentro del directorio de `Trabajo_final_v2`,
    para mantener independencia del proyecto `Trabajo_final` baseline.
    """

    data_dir: Path = Path(__file__).resolve().parent

