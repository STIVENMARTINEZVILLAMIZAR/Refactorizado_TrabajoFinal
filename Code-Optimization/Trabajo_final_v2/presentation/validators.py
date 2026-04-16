from __future__ import annotations


def validar_entero(mensaje: str) -> int:
    while True:
        try:
            dato = int(input(mensaje))
            while dato <= 0:
                dato = int(input("Error. Ingrese un numero positivo: "))
            return dato
        except Exception:
            print("Error, solo se admiten número entero.")


def validar_decimales(mensaje: str) -> float:
    while True:
        try:
            dato = float(input(mensaje))
            while dato <= 0:
                dato = float(input("Error. Ingrese un numero positivo real: "))
            return dato
        except Exception:
            print("Error, solo se admiten números decimales.")


def validar_texto(mensaje: str, cantidad_minima: int, cantidad_maxima: int) -> str:
    while True:
        dato = input(mensaje)
        if dato is None:
            print("Error, no puede dejar el espacio en blanco: ")
            continue
        caracteres = len(dato.strip())
        if caracteres < cantidad_minima or caracteres > cantidad_maxima:
            print("Error, no puede dejar el espacio en blanco: ")
            continue
        return dato


def validar_menu(mensaje: str, minimo: int, maximo: int) -> int:
    op = validar_entero(mensaje)
    while op < minimo or op > maximo:
        op = validar_entero("Error intentelo nuevamente: ")
    return op

