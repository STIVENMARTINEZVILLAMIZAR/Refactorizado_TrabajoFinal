from pathlib import Path


def ensure_data_dir(data_dir: Path) -> None:
    data_dir.mkdir(parents=True, exist_ok=True)


def data_file(data_dir: Path, filename: str) -> Path:
    return data_dir / filename


FILES = {
    "usuarios": "usuarios.json",
    "categorias": "categorias.json",
    "herramientas": "herramientas.json",
    "prestamos": "prestamos.json",
    "historial": "historial.txt",
}

