from __future__ import annotations

from domain.dtos import ActualizarUsuarioDTO, CrearUsuarioDTO
from presentation.transforms import transformar_tipo
from presentation.validators import validar_entero, validar_menu, validar_texto


def _imprimir_usuario(u) -> None:
    print(
        f"""
            ****************************
            ID:             {u.id}
            Nombre:         {u.nombre}
            Apellido:       {u.apellido}
            Telefono:       {u.telefono}
            Direccion:      {u.direccion}
            Tipo Usuario:   {u.tipo.value}
            """
    )


def menu_usuario(usuarios_controller, logger) -> None:
    while True:
        op_herramienta = validar_menu(
            """
                    __________________________________________
                    /                                          \\
                    |       DIRECTORIO: GESTIÓN DE USUARIOS     |
                    |__________________________________________/
                    
                    Administración de Miembros del Vecindario:
                    
                        [1]  Registrar nuevo usuario
                        [2]  Actualizar datos existentes
                        [3]  Listar todos los residentes
                        [4]  Buscar usuario especifíco
                        [5]  Eliminar del sistema
                        [6]  Volver al menú anterior
                        
                    __________________________________________
                    >>> Selecciona una gestión (1-6):""",
            1,
            6,
        )
        match op_herramienta:
            case 1:
                nombre = validar_texto("Ingrese el nombre de la persona: ", 1, 30)
                apellido = validar_texto("Ingrese el apellido de la persona: ", 1, 30)
                telefono = validar_entero("Ingrese su numero de telefono: ")
                direccion = validar_texto(
                    "Ingrese la dirección de residencia del usuario: ", 1, 50
                )
                tipo_id = validar_menu(
                    """
                                            Seleccion el tipo de usuario:
                                            1. Residente
                                            2. Administrador
                                            """,
                    1,
                    2,
                )
                dto = CrearUsuarioDTO(
                    nombre=nombre,
                    apellido=apellido,
                    telefono=telefono,
                    direccion=direccion,
                    tipo=transformar_tipo(tipo_id),
                )
                usuarios_controller.crear_usuario(dto)
                print("DATOS GUARDADOS CORRECTAMENTE!")
                logger.append("Se ha creado un nuevo usuario ")
            case 2:
                usuarios = usuarios_controller.listar_usuarios()
                if not usuarios:
                    print("No se puede actualizar porque no hay registros")
                    continue
                for u in usuarios:
                    _imprimir_usuario(u)
                id_usuario = validar_entero("Ingrese el id a actualizar: ")
                existente = usuarios_controller.obtener_usuario(id_usuario)
                if not existente:
                    print("NO SE ENCONTRÓ EL ID: ", id_usuario)
                    continue
                op_actualizar = validar_menu(
                    """
                                    1. Nombre.
                                    2. Apellido.
                                    3. Telefono.
                                    4. Direccion
                                    5. Tipo de usuario
                                    6. Cancelar
                                        """,
                    1,
                    6,
                )
                nombre_n = existente.nombre
                apellido_n = existente.apellido
                telefono_n = existente.telefono
                direccion_n = existente.direccion
                tipo_n = existente.tipo
                if op_actualizar == 1:
                    nombre_n = validar_texto("Ingrese el nombre: ", 1, 20)
                elif op_actualizar == 2:
                    apellido_n = validar_texto("Ingrese el nombre: ", 1, 20)
                elif op_actualizar == 3:
                    telefono_n = validar_entero("Ingrese su numero de telefono: ")
                elif op_actualizar == 4:
                    direccion_n = validar_texto(
                        "Ingrese la dirección de residencia del usuario: ", 1, 50
                    )
                elif op_actualizar == 5:
                    tipo_id = validar_menu(
                        """
                                            Seleccion el tipo de usuario:
                                            1. Residente
                                            2. Administrador
                                            """,
                        1,
                        2,
                    )
                    tipo_n = transformar_tipo(tipo_id)
                else:
                    print("Operación cancelada!")
                    continue

                usuarios_controller.actualizar_usuario(
                    ActualizarUsuarioDTO(
                        usuario_id=existente.id,
                        nombre=nombre_n,
                        apellido=apellido_n,
                        telefono=telefono_n,
                        direccion=direccion_n,
                        tipo=tipo_n,
                    )
                )
                print("DATO ACTUALIZADO!")
                logger.append("Se ha actualizado un usuario ")
            case 3:
                usuarios = usuarios_controller.listar_usuarios()
                if not usuarios:
                    print("No hay usuarios registradas.")
                else:
                    for u in usuarios:
                        _imprimir_usuario(u)
            case 4:
                id_usuario = validar_entero("Ingrese el id a buscar: ")
                u = usuarios_controller.obtener_usuario(id_usuario)
                if not u:
                    print("NO SE ENCONTRÓ EL ID: ", id_usuario)
                else:
                    _imprimir_usuario(u)
            case 5:
                usuarios = usuarios_controller.listar_usuarios()
                if not usuarios:
                    print("No se puede actualizar porque no hay registros")
                    continue
                for u in usuarios:
                    _imprimir_usuario(u)
                id_usuario = validar_entero("Ingrese el id a eliminar: ")
                existente = usuarios_controller.obtener_usuario(id_usuario)
                if not existente:
                    print("NO SE ENCONTRÓ EL ID: ", id_usuario)
                    continue
                print(f"{existente.nombre} ya no esta entre nosotros!")
                usuarios_controller.eliminar_usuario(id_usuario)
                logger.append("Se ha eliminado un usuario ")
            case 6:
                return

