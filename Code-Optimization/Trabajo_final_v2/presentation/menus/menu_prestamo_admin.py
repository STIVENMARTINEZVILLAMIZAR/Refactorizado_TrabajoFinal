from __future__ import annotations

from domain.dtos import DecidirPrestamoDTO
from presentation.transforms import solicitar_fecha_inicio
from presentation.validators import validar_entero, validar_menu, validar_texto


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
            Cantidad:       {p.cantidad}
            Estado:         {p.estado.value}
            Observaciones:  {p.observaciones}
            """
    )


def menu_prestamo_admin(prestamos_controller, logger) -> None:
    while True:
        op_herramienta = validar_menu(
            """
                        __________________________________________
                        /                                          \\
                        |       LOGÍSTICA: GESTIÓN DE PRÉSTAMOS     |
                        |__________________________________________/
                        
                        Panel de Control de Préstamos y Devoluciones:
                        
                            [1] Gestionar préstamos
                            [2] Buscar una solicitud específica
                            [3] Ver todas las solicitudes
                            [4] Eliminar registros de solicitudes
                            [5] Volver al menú anterior
                            
                        __________________________________________
                        >>> Selecciona una opción (1-5):""",
            1,
            5,
        )
        match op_herramienta:
            case 1:
                prestamos = prestamos_controller.listar_prestamos()
                if not prestamos:
                    print("No se puede gestionar porque no hay registros")
                    continue
                for p in prestamos:
                    _imprimir_prestamo(p)

                id_prestamo = validar_entero("Ingrese el id del prestamo a gestionar: ")
                existente = prestamos_controller.obtener_prestamo(id_prestamo)
                if not existente:
                    print("NO SE ENCONTRÓ EL ID: ", id_prestamo)
                    continue

                op_gestionar = validar_menu(
                    """
                                            Seleccione que opción desea realizar con el prestamo:
                                            1. Gestionar
                                            2. Rechazar
                                            """,
                    1,
                    2,
                )
                if op_gestionar == 1:
                    _, msg = prestamos_controller.gestionar_prestamo(id_prestamo)
                    print(msg)
                else:
                    motivo = validar_texto(
                        "Ingrese el motivo por el cual rechaza la solicitud de prestamo: ",
                        1,
                        100,
                    )
                    prestamos_controller.rechazar_prestamo(id_prestamo, motivo)
                logger.append("Se ha gestionado una solicitud de prestamo ")
            case 2:
                id_prestamo = validar_entero("Ingrese el id a buscar: ")
                p = prestamos_controller.obtener_prestamo(id_prestamo)
                if not p:
                    print("NO SE ENCONTRÓ EL ID: ", id_prestamo)
                else:
                    _imprimir_prestamo(p)
            case 3:
                prestamos = prestamos_controller.listar_prestamos()
                if not prestamos:
                    print("No hay registros en este momento")
                    continue
                for p in prestamos:
                    _imprimir_prestamo(p)
            case 4:
                prestamos = prestamos_controller.listar_prestamos()
                if not prestamos:
                    print("No se puede eliminar porque no hay registros")
                    continue
                for p in prestamos:
                    _imprimir_prestamo(p)
                id_prestamo = validar_entero("Ingrese el id a eliminar: ")
                existente = prestamos_controller.obtener_prestamo(id_prestamo)
                if not existente:
                    print("NO SE ENCONTRÓ EL ID: ", id_prestamo)
                    continue
                # Baseline: elemento.get('nombre', 'clave no encontrada') en un prestamo
                print("clave no encontrada ya no esta entre nosotros!")
                prestamos_controller.eliminar_prestamo(id_prestamo)
                logger.append("Se ha eliminado una solicitod de prestamo ")
            case 5:
                return

