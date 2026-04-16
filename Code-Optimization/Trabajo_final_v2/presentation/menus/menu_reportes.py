from __future__ import annotations

from presentation.validators import validar_entero, validar_menu


def _imprimir_prestamo(p) -> None:
    print(
        f"""
                            ****************************
                            ID:             {p.id}
                            Usuario:        {p.usuario.nombre}
                            ID Usuario:     {p.usuario.id}
                            Herramienta:    {p.herramienta.nombre}
                            ID Herramienta: {p.herramienta.id}
                            Fecha Inicio:   {p.fecha_inicio}
                            Fecha Entrega:  {p.fecha_final}
                            Estado:         {p.estado.value}
                            Observaciones:  {p.observaciones}
                            """
    )


def menu_reportes(reportes_controller, logger) -> None:
    while True:
        op = validar_menu(
            """
                        __________________________________________
                        /                                          \\
                        |       REPORTE Y CONSULTAS GENERALES      |
                        |__________________________________________/
                        
                        Filtros de información disponibles:
                        
                            [1]  Stock mínimo (Baja disponibilidad)
                            [2]  Solicitudes en proceso / completadas
                            [3]  Buscar solicitudes por usuario
                            [4]  Herramientas más usadas
                            [5]  Usuarios con más prestamos
                            [6]  Volver al menú anterior
                            
                        __________________________________________
                        >>> Selecciona el reporte a generar (1-4):""",
            1,
            6,
        )
        match op:
            case 1:
                stock = validar_entero(
                    "Ingrese la cantidad stock minimo que se encuentre disponible en las herramientas que desea buscar: "
                )
                resultados = reportes_controller.stock_minimo(stock)
                if not resultados:
                    print("NO SE ENCONTRÓ NINGÚN STOCK CON ESA CANTIDAD MINIMA: ", stock)
                else:
                    for h in resultados:
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
            case 2:
                option = validar_menu(
                    """
                        1. En proceso
                        2. Completados
                        """,
                    1,
                    2,
                )
                prestamos = reportes_controller.prestamos_por_estado_option(option)
                if not prestamos:
                    if option == 1:
                        print("NO SE ENCONTRO NINGUN PRESTAMO EN ESTADO DE: EN PROCESO")
                    else:
                        print("NO SE ENCONTRÓ NINGUN PRESTAAMO EN ESTADO: COMPLETADA O RECHAZADA")
                else:
                    for p in prestamos:
                        _imprimir_prestamo(p)
            case 3:
                id_usuario = validar_entero(
                    "Ingrese el id de su Usuario. Si no lo conoce contacte al administrador: "
                )
                prestamos = reportes_controller.historial_usuarios(id_usuario)
                if not prestamos:
                    print("No hay registros en este momento")
                else:
                    for p in prestamos:
                        _imprimir_prestamo(p)
            case 4:
                resultados = reportes_controller.herramienta_mas_usada()
                if not resultados:
                    print("No hay registros en este momento")
                else:
                    for tool_id, nombre, contador in resultados:
                        print(f"{tool_id}, {nombre} = {contador}\n", end="")
            case 5:
                resultados = reportes_controller.usuario_mas_usado()
                if not resultados:
                    print("No hay registros en este momento")
                else:
                    for u_id, nombre, apellido, contador in resultados:
                        print(f"{u_id}, {nombre} {apellido} = {contador}\n", end="")
            case 6:
                return

