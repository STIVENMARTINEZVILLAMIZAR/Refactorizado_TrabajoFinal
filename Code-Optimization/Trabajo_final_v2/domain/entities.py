from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any, Dict, Optional

from .enums import EstadoHerramienta, EstadoPrestamo, Rol


@dataclass(frozen=True)
class Usuario:
    id: int
    nombre: str
    apellido: str
    telefono: int
    direccion: str
    tipo: Rol

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Usuario":
        tipo_val = data.get("tipo")
        rol = Rol(tipo_val) if tipo_val in [r.value for r in Rol] else Rol.RESIDENTE
        return Usuario(
            id=int(data["id"]),
            nombre=str(data["nombre"]),
            apellido=str(data["apellido"]),
            telefono=int(data["telefono"]),
            direccion=str(data["direccion"]),
            tipo=rol,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "telefono": self.telefono,
            "direccion": self.direccion,
            "tipo": self.tipo.value,
        }


@dataclass(frozen=True)
class Categoria:
    id: int
    nombre: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Categoria":
        return Categoria(id=int(data["id"]), nombre=str(data.get("categoria") or data.get("nombre")))

    def to_dict(self) -> Dict[str, Any]:
        # Baseline usa la clave `nombre` en categorias.json pero `categoria` dentro de herramientas.
        return {"id": self.id, "categoria": self.nombre}


@dataclass(frozen=True)
class Herramienta:
    id: int
    nombre: str
    categoria: Categoria
    cantidad: int
    estado: EstadoHerramienta
    precio: int

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Herramienta":
        categoria_data = data.get("categoria") or {}
        estado_val = data.get("estado")
        estado = EstadoHerramienta(estado_val)
        return Herramienta(
            id=int(data["id"]),
            nombre=str(data["nombre"]),
            categoria=Categoria.from_dict(categoria_data),
            cantidad=int(data["cantidad"]),
            estado=estado,
            precio=int(data["precio"]),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "categoria": self.categoria.to_dict(),
            "cantidad": self.cantidad,
            "estado": self.estado.value,
            "precio": self.precio,
        }


@dataclass
class Prestamo:
    id: int
    usuario: Usuario
    herramienta: Herramienta
    cantidad: int
    fecha_inicio: str
    fecha_final: str
    estado: EstadoPrestamo
    observaciones: str

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Prestamo":
        estado = EstadoPrestamo(data.get("estado"))
        fecha_inicio = str(data.get("fecha_inicio"))
        fecha_final = str(data.get("fecha_final"))
        return Prestamo(
            id=int(data["id"]),
            usuario=Usuario.from_dict(data["usuario"]),
            herramienta=Herramienta.from_dict(data["herramienta"]),
            cantidad=int(data["cantidad"]),
            fecha_inicio=fecha_inicio,
            fecha_final=fecha_final,
            estado=estado,
            observaciones=str(data.get("observaciones", "")),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "usuario": self.usuario.to_dict(),
            "herramienta": self.herramienta.to_dict(),
            "cantidad": self.cantidad,
            "fecha_inicio": self.fecha_inicio,
            "fecha_final": self.fecha_final,
            "estado": self.estado.value,
            "observaciones": self.observaciones,
        }

    @staticmethod
    def compute_fecha_final(fecha_inicio: date, dias: int) -> str:
        return str(fecha_inicio + (dias and __import__("datetime").timedelta(days=dias) or __import__("datetime").timedelta(days=0)))

