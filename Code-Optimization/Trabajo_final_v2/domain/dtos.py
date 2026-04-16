from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Optional

from .enums import EstadoPrestamo, Rol


@dataclass(frozen=True)
class CrearUsuarioDTO:
    nombre: str
    apellido: str
    telefono: int
    direccion: str
    tipo: Rol


@dataclass(frozen=True)
class ActualizarUsuarioDTO:
    usuario_id: int
    nombre: str
    apellido: str
    telefono: int
    direccion: str
    tipo: Rol


@dataclass(frozen=True)
class CrearCategoriaDTO:
    nombre: str


@dataclass(frozen=True)
class ActualizarCategoriaDTO:
    categoria_id: int
    nombre: str


@dataclass(frozen=True)
class CrearHerramientaDTO:
    nombre: str
    categoria_id: int
    cantidad: int
    estado: str
    precio: int


@dataclass(frozen=True)
class ActualizarHerramientaDTO:
    herramienta_id: int
    nombre: str
    categoria_id: int
    cantidad: int
    estado: str
    precio: int


@dataclass(frozen=True)
class CrearPrestamoDTO:
    usuario_id: int
    herramienta_id: int
    cantidad: int
    fecha_inicio: date
    dias: int


@dataclass(frozen=True)
class DecidirPrestamoDTO:
    prestamo_id: int
    accion: str  # "aceptar" | "rechazar"
    motivo: Optional[str] = None


@dataclass(frozen=True)
class EstadoReporteDTO:
    estado: EstadoPrestamo

