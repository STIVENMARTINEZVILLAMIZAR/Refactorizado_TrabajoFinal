from __future__ import annotations

from enum import Enum


class Rol(Enum):
    RESIDENTE = "Residente"
    ADMIN = "Administrador"


class EstadoHerramienta(Enum):
    ACTIVA = "Activo"
    EN_REPARACION = "En reparación"
    INACTIVA = "Inactiva"


class EstadoPrestamo(Enum):
    EN_PROCESO = "En proceso"
    ACEPTADA = "Aceptada"
    RECHAZADA = "Rechazada"

