from __future__ import annotations

from datetime import datetime

from domain.dtos import ActualizarCategoriaDTO, CrearCategoriaDTO
from presentation.validators import validar_menu, validar_texto, validar_entero


def _imprimir_categoria(c) -> None:
    print(
        f"""
            *********************************************************
            id:             {c.id}
            categoria:      {c.nombre}
            """
    )


def menu_categoria(categorias_controller, logger) -> None:
    while True:
        op = validar_menu(
            """
            __________________________________________
            /                                          \\
            |        CONFIGURACIÓN: CATEGORÍAS         |
            |__________________________________________/
            
            Organización de Herramientas del Barrio:
            
                [1] Registrar nueva categoría
                [2] Actualizar datos existentes
                [3] Listar todas las categorías
                [4] Buscar categoría específica
                [5] Eliminar categoría
                [6] Volver al menú anterior
            __________________________________________
            >>> Selecciona una opción (1-6):""",
            1,
            6,
        )
        match op:
            case 1:
                nombre = validar_texto("Ingrese la categoria de la herramienta: ", 1, 30)
                categorias_controller.crear_categoria(CrearCategoriaDTO(nombre=nombre))
                print("DATOS GUARDADOS CORRECTAMENTE!")
                logger.append("Se ha creado una nueva categoria ")
            case 2:
                categorias = categorias_controller.listar_categorias()
                if not categorias:
                    print("No se puede actualizar porque no hay registros")
                    continue
                for c in categorias:
                    _imprimir_categoria(c)
                id_categoria = validar_entero("Ingrese el id a actualizar: ")
                existente = categorias_controller.obtener_categoria(id_categoria)
                if not existente:
                    print("NO SE ENCONTRÓ EL ID: ", id_categoria)
                    continue

                op_actualizar = validar_menu(
                    """
                                    1. Nombre Categoria.
                                    2. Cancelar   
                                        """,
                    1,
                    2,
                )
                if op_actualizar == 1:
                    nuevo = validar_texto("Ingrese la categoria: ", 1, 20)
                    categorias_controller.actualizar_categoria(
                        ActualizarCategoriaDTO(categoria_id=id_categoria, nombre=nuevo)
                    )
                    print("DATO ACTUALIZADO!")
                    logger.append("Se ha actualizado una categoria ")
                else:
                    print("Operación cancelada!")
            case 3:
                categorias = categorias_controller.listar_categorias()
                if not categorias:
                    print("No hay categorías registradas.")
                else:
                    for c in categorias:
                        _imprimir_categoria(c)
            case 4:
                id_categoria = validar_entero("Ingrese el id a buscar: ")
                c = categorias_controller.obtener_categoria(id_categoria)
                if not c:
                    print("NO SE ENCONTRÓ EL ID: ", id_categoria)
                else:
                    print(
                        f"""
                    ****************************
                    ID:             {c.id}
                    Categoria:      {c.nombre}
                    """
                    )
            case 5:
                categorias = categorias_controller.listar_categorias()
                if not categorias:
                    print("No se puede eliminar porque no hay registros")
                    continue
                for c in categorias:
                    _imprimir_categoria(c)
                id_categoria = validar_entero("Ingrese el id a eliminar: ")
                existente = categorias_controller.obtener_categoria(id_categoria)
                if not existente:
                    print("NO SE ENCONTRÓ EL ID: ", id_categoria)
                    continue
                print(f"{existente.nombre} ya no esta entre nosotros!")
                categorias_controller.eliminar_categoria(id_categoria)
                logger.append("Se ha eliminado una categoria ")
            case 6:
                return

