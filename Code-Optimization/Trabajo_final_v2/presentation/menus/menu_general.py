from __future__ import annotations

from typing import Any, Optional

from presentation.validators import validar_menu


def _login_prompt(auth_controller: Any) -> Optional[str]:
    while True:
        op = validar_menu(
            """
                    ******************************************
                    * *
                    * SISTEMA DE INICIO DE SESIÓN *
                    * "Tu Amigo del Vecindario" *
                    * *
                    ******************************************
                            [  ◢◤  SEGURIDAD  ◥◣  ]

                    Por favor, identifícate para continuar:

                        1. Ingresar como ADMINISTRADOR
                        2. Ingresar como RESIDENTE
                        3. SALIR DEL SISTEMA

                    ------------------------------------------
                    >>> Selecciona tu perfil (1-3): """,
            1,
            3,
        )
        match op:
            case 1:
                print("-" * 15)
                print("[ZONA DE ACCESO RESTRINGIDO: ADMIN]")
                print("-" * 15)
                contrasenia = input("Introduce la clave de seguridad para continuar: ")
                rol = auth_controller.login(1, contrasenia)
                if rol == "admin":
                    return "admin"
                print("Contreseña incorrecta, sera regresado al menu de ingreso")
            case 2:
                print("-" * 15)
                print("[ ÁREA DE RESIDENTES: MI HOGAR ]")
                print("-" * 15)
                contrasenia = input("Introduce la clave de seguridad de residente: ")
                rol = auth_controller.login(2, contrasenia)
                if rol == "residente":
                    return "residente"
                print("Contreseña incorrecta, sera regresado al menu de ingreso")
            case 3:
                print(
                    """
                    __________________________________________
                    /                                          \\
                    |    👋 ¡HASTA LUEGO, VECINO!              |
                    |__________________________________________/

                    La sesión se ha cerrado correctamente.
                    Gracias por cuidar de nuestra comunidad.

                    [ ESTADO: SISTEMA FUERA DE LÍNEA ]
                    __________________________________________
                    """
                )
                return None


def run_menu_general(
    auth_controller: Any,
    usuarios_controller: Any,
    categorias_controller: Any,
    herramientas_controller: Any,
    prestamos_controller: Any,
    reportes_controller: Any,
    logger: Any,
) -> None:
    permiso = _login_prompt(auth_controller)
    if permiso is None:
        return

    while True:
        if permiso == "admin":
            op_menu_admin = validar_menu(
                """
                                        /\\______________/\\
                                        /  ¡BIENVENIDO A!  \\
                                        |      APP: TU       |
                                        |AMIGO DEL VECINDARIO|
                                        \\  ____________  /
                                        \\/            \\/

                                        ********* HOlA ADMIN **************
                                        Selecciona una opción:
                                        -----------------------
                                        1) Gestionar Herramientas
                                        2) Gestionar Categoria de Herramientas
                                        3) Gestionar Usuarios
                                        4) Gestionar Prestamos
                                        5) Consultar Reportes
                                        6) Salir
                                        -----------------------
                                        >>>""",
                1,
                6,
            )
            match op_menu_admin:
                case 1:
                    if not categorias_controller.listar_categorias():
                        print("NO SE PUEDE REALIZAR NINGUNA OPCIÓN HASTA INGRESAR UNA CATEGORIA")
                        logger.append("Se intento hacer un registro de Herramienta pero no hay categorias ")
                    else:
                        from presentation.menus.menu_herramientas import menu_herramienta_admin

                        menu_herramienta_admin(herramientas_controller, categorias_controller, logger)
                case 2:
                    from presentation.menus.menu_categoria import menu_categoria

                    menu_categoria(categorias_controller, logger)
                case 3:
                    from presentation.menus.menu_usuario import menu_usuario

                    menu_usuario(usuarios_controller, logger)
                case 4:
                    if not usuarios_controller.listar_usuarios() or not herramientas_controller.listar_herramientas():
                        print("NO SE PUEDE REALIZAR NINGUNA OPCIÓN DE PRESTAMO HASTA TENER REGISTRO DE USUARIOS Y HERRAMIENTAS")
                        logger.append(
                            "Se intento hacer una gestion de prestamo pero no hay usuarios o herramientas registradas "
                        )
                    else:
                        from presentation.menus.menu_prestamo_admin import menu_prestamo_admin

                        menu_prestamo_admin(prestamos_controller, logger)
                case 5:
                    if not prestamos_controller.listar_prestamos() or not herramientas_controller.listar_herramientas():
                        print("NO SE PUEDE REALIZAR CONSULTAS DE REPORTE PORQUE NO HAY REGISTROS")
                        logger.append("Se intento hacer una consulta de reporte pero no hay registros en estos momentos ")
                    else:
                        from presentation.menus.menu_reportes import menu_reportes

                        menu_reportes(reportes_controller, logger)
                case 6:
                    print(
                        """
                    __________________________________________
                    /                                          \\
                    |      ¡HASTA LUEGO, VECINO ADMIN!          |
                    |__________________________________________/

                    La sesión se ha cerrado correctamente.
                    Gracias por cuidar de nuestra comunidad.

                    [ ESTADO: SISTEMA FUERA DE LÍNEA ]
                    __________________________________________
                    """
                    )
                    return
        else:
            op_menu_residente = validar_menu(
                """
                                        /\\______________/\\
                                        /  ¡BIENVENIDO A!  \\
                                        |      APP: TU       |
                                        |AMIGO DEL VECINDARIO|
                                        \\  ____________  /
                                        \\/            \\/

                                        ******* HOlA VECINO ***************
                                        Selecciona una opción:
                                        -----------------------
                                        1) Gestionar Préstamos
                                        2) Salir
                                        -----------------------
                                        >>>""",
                1,
                2,
            )
            match op_menu_residente:
                case 1:
                    if not usuarios_controller.listar_usuarios() or not herramientas_controller.listar_herramientas():
                        print(
                            "No se puede solicitar un prestamo porque no hay registros de herramienta y usuarios"
                        )
                        print("Contacte al administrador para registrar usuarios y herramientas")
                        logger.append(
                            "Se intento realizar una solicitud de prestamo pero no se pudo porque no hay registros en usuarios y herramientas"
                        )
                    else:
                        from presentation.menus.menu_prestamo_residente import menu_prestamo_residente

                        menu_prestamo_residente(prestamos_controller, usuarios_controller, herramientas_controller, logger)
                case 2:
                    print(
                        """
                    __________________________________________
                    /                                          \\
                    |      ¡HASTA LUEGO, VECINO RESIDENTE!      |
                    |__________________________________________/

                    La sesión se ha cerrado correctamente.
                    Gracias por cuidar de nuestra comunidad.

                    [ ESTADO: SISTEMA FUERA DE LÍNEA ]
                    __________________________________________
                    """
                    )
                    return

