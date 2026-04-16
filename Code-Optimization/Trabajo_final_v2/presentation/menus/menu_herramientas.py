from __future__ import annotations

from domain.dtos import ActualizarHerramientaDTO, CrearHerramientaDTO
from presentation.transforms import transformar_estado
from presentation.validators import validar_entero, validar_menu, validar_texto


def _imprimir_herramienta(h) -> None:
    print(
        f"""
            ****************************
            ID:             {h.id}
            Nombre:         {h.nombre}
            Id Categoria:   {h.categoria.id}
            Categoria:      {h.categoria.nombre}
            Cantidad:       {h.cantidad}
            Estado:         {h.estado.value}
            Precio:         {h.precio}
            """
    )


def menu_herramienta_admin(herramientas_controller, categorias_controller, logger) -> None:
    while True:
        op_herramienta = validar_menu(
            """
                        __________________________________________
                        /                                          \\
                        |    🛠️  INVENTARIO: GESTIÓN DE HERRAMIENTAS  |
                        |__________________________________________/
                        
                        Panel de Control - Selecciona una acción:
                        
                            [1] Registrar nueva herramienta
                            [2] Actualizar datos existentes
                            [3] Listar inventario completo
                            [4] Buscar herramienta especifíca
                            [5] Eliminar del sistema
                            [6] Volver al menú anterior
                            
                        __________________________________________
                        >>> Digita tu opción (1-6): """,
            1,
            6,
        )
        match op_herramienta:
            case 1:
                nombre = validar_texto("Ingrese el nombre: ", 1, 20)
                categorias = categorias_controller.listar_categorias()
                if not categorias:
                    print("NO SE PUEDE REGISTRAR HERRAMIENTA SIN CATEGORIAS")
                    logger.append("Se intento hacer un registro de Herramienta pero no hay categorias ")
                    continue
                print("Categorías disponibles:")
                for c in categorias:
                    print(f"- {c.id}: {c.nombre}")
                id_categoria = validar_entero("Ingrese el id de la categoria: ")
                while not categorias_controller.obtener_categoria(id_categoria):
                    id_categoria = validar_entero(
                        "Error, Categoria no encontrada. Intente nuevamente: "
                    )
                cantidad = validar_entero(
                    "Selecciona la cantidad disponible de esta herramienta: "
                )
                estado_id = validar_menu(
                    """
                                            Seleccion una de las 3 opciones del estado de una herramienta:
                                            1. Activa
                                            2. Fuera de servicio
                                            3. Reparación
                                            """,
                    1,
                    3,
                )
                estado = transformar_estado(estado_id)
                precio = validar_entero("Ingrese el valor que le costo la herramienta: ")
                dto = CrearHerramientaDTO(
                    nombre=nombre,
                    categoria_id=id_categoria,
                    cantidad=cantidad,
                    estado=estado,
                    precio=precio,
                )
                herramientas_controller.crear_herramienta(dto)
                print("DATOS GUARDADOS CORRECTAMENTE!")
                logger.append("Se ha registrado una herramienta nueva ")
            case 2:
                herramientas = herramientas_controller.listar_herramientas()
                if not herramientas:
                    print("No se puede actualizar porque no hay registros")
                    continue
                for h in herramientas:
                    _imprimir_herramienta(h)
                id_h = validar_entero("Ingrese el id a actualizar: ")
                existente = herramientas_controller.obtener_herramienta(id_h)
                if not existente:
                    print("NO SE ENCONTRÓ EL ID: ", id_h)
                    continue
                op_actualizar = validar_menu(
                    """
                                    1. Nombre.
                                    2. Categoria.
                                    3. Estado.
                                    4. Precio
                                    5. Cantidad
                                    6. Cancelar
                                        """,
                    1,
                    6,
                )
                nombre_n = existente.nombre
                categoria_id_n = existente.categoria.id
                cantidad_n = existente.cantidad
                estado_n = existente.estado.value
                precio_n = existente.precio
                if op_actualizar == 1:
                    nombre_n = validar_texto("Ingrese el nombre: ", 1, 20)
                elif op_actualizar == 2:
                    categorias = categorias_controller.listar_categorias()
                    for c in categorias:
                        print(f"- {c.id}: {c.nombre}")
                    categoria_id_n = validar_entero("Ingrese el id de la categoria: ")
                    while not categorias_controller.obtener_categoria(categoria_id_n):
                        categoria_id_n = validar_entero(
                            "Error, categoria no encontrada. Intente nuevamente: "
                        )
                elif op_actualizar == 3:
                    estado_id = validar_menu(
                        """
                                        Seleccion una de las 3 opciones del estado de una herramienta:
                                        1. Activa
                                        2. Fuera de servicio
                                        3. Reparación
                                        """,
                        1,
                        3,
                    )
                    estado_n = transformar_estado(estado_id)
                elif op_actualizar == 4:
                    precio_n = validar_entero(
                        "Ingrese el valor que le costo la herramienta: "
                    )
                elif op_actualizar == 5:
                    cantidad_n = validar_entero(
                        "Selecciona la cantidad disponible de esta herramienta: "
                    )
                else:
                    print("Operación cancelada!")
                    continue

                herramientas_controller.actualizar_herramienta(
                    ActualizarHerramientaDTO(
                        herramienta_id=existente.id,
                        nombre=nombre_n,
                        categoria_id=categoria_id_n,
                        cantidad=cantidad_n,
                        estado=estado_n,
                        precio=precio_n,
                    )
                )
                print("DATO ACTUALIZADO!")
                logger.append("Se ha actualizado una herramienta ")
            case 3:
                herramientas = herramientas_controller.listar_herramientas()
                if not herramientas:
                    print("No hay herramientas registradas.")
                else:
                    for h in herramientas:
                        _imprimir_herramienta(h)
            case 4:
                id_h = validar_entero("Ingrese el id a buscar: ")
                h = herramientas_controller.obtener_herramienta(id_h)
                if not h:
                    print("NO SE ENCONTRÓ EL ID: ", id_h)
                else:
                    print(
                        f"""
            ************************************************************
            ID:             {h.id}
            Nombre:         {h.nombre}
            ID Categoria:   {h.categoria.id}
            Categoria:      {h.categoria.nombre}
            Cantidad:       {h.cantidad}
            Estado:         {h.estado.value}
            Precio:         {h.precio}
                    """
                    )
            case 5:
                herramientas = herramientas_controller.listar_herramientas()
                if not herramientas:
                    print("No se puede actualizar porque no hay registros")
                    continue
                for h in herramientas:
                    _imprimir_herramienta(h)
                id_h = validar_entero("Ingrese el id a eliminar: ")
                existente = herramientas_controller.obtener_herramienta(id_h)
                if not existente:
                    print("NO SE ENCONTRÓ EL ID: ", id_h)
                    continue
                print(f"{existente.nombre} ya no esta entre nosotros!")
                herramientas_controller.eliminar_herramienta(id_h)
                logger.append("Se ha eliminado una herramienta ")
            case 6:
                return

