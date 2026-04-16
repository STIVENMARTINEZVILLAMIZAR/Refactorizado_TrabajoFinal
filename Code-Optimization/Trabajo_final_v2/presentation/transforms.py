from __future__ import annotations

from datetime import date

from domain.enums import Rol
from presentation.validators import validar_entero


def transformar_estado(estado_id: int) -> str:
    estado_id = int(estado_id)
    if estado_id == 1:
        return "Activo"
    if estado_id == 2:
        return "En reparación"
    return "Inactiva"


def transformar_tipo(tipo_id: int) -> Rol:
    tipo_id = int(tipo_id)
    if tipo_id == 1:
        return Rol.RESIDENTE
    return Rol.ADMIN


def solicitar_fecha_inicio() -> date:
    anio = validar_entero("Ingrese el año de la solicitud: ")
    mes = validar_entero("Ingrese el mes de la solicitud: ")
    dia = validar_entero("Ingrese el dia de la solicitud: ")
    return date(anio, mes, dia)

