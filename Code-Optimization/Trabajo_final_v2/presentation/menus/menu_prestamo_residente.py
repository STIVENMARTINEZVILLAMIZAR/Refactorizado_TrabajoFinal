from __future__ import annotations

from domain.dtos import CrearPrestamoDTO
from presentation.transforms import solicitar_fecha_inicio
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
                    Cantidad:       {p.cantidad}
                    Estado:         {p.estado.value}
                    Observaciones:  {p.observaciones}
                    """
    )


def menu_prestamo_residente(prestamos_controller, usuarios_controller, herramientas_controller, logger) -> None:
    while True:
        op_herramienta = validar_menu(
            """
                        __________________________________________
                        /                                          \\
                        |       ÁREA RESIDENTE: MIS PRÉSTAMOS      |
                        |__________________________________________/
                        
                        ¿En qué podemos ayudarte hoy?
                        
                            [1] Solicitar un nuevo préstamo
                            [2] Consultar el estado de mis préstamos
                            [3] Volver al menú anterior
                            
                        __________________________________________
                        >>> Selecciona una opción (1-3):""",
            1,
            3,
        )
        match op_herramienta:
            case 1:
                usuarios = usuarios_controller.listar_usuarios()
                if not usuarios:
                    print("No hay usuarios registrados.")
                    continue
                for u in usuarios:
                    print(f"- {u.id}: {u.nombre} {u.apellido}")
                id_usuario = validar_entero("Ingrese el id del usuario: ")
                while not usuarios_controller.obtener_usuario(id_usuario):
                    id_usuario = validar_entero(
                        "Error, usuario no encontrada. Intente nuevamente: "
                    )

                herramientas = herramientas_controller.listar_herramientas()
                for h in herramientas:
                    print(f"- {h.id}: {h.nombre} (stock={h.cantidad})")
                id_herramienta = validar_entero("Ingrese el id de la herramienta: ")
                while not herramientas_controller.obtener_herramienta(id_herramienta):
                    id_herramienta = validar_entero(
                        "Error, Herramienta no enctrada. Intente nuevamente: "
                    )

                cantidad = validar_entero(
                    "Ingrese la cantidad de herramientas a solicitar: "
                )
                fecha_inicio = solicitar_fecha_inicio()
                dias = validar_entero("Ingrese la cantidad de días a usar la herramienta: ")

                dto = CrearPrestamoDTO(
                    usuario_id=id_usuario,
                    herramienta_id=id_herramienta,
                    cantidad=cantidad,
                    fecha_inicio=fecha_inicio,
                    dias=dias,
                )
                prestamo = prestamos_controller.solicitar_prestamo(dto)
                print("DATOS GUARDADOS CORRECTAMENTE!")
                print(
                    f"SU ID ES {prestamo.id}, POR FAVOR GUARDELO PARA HACER SEGUIMIENTO"
                )
            case 2:
                id_usuario = validar_entero(
                    "Ingrese el id de su Usuario. Si no lo conoce contacte al administrador: "
                )
                prestamos = prestamos_controller.consultar_prestamos(id_usuario)
                if not prestamos:
                    print("No hay registros en este momento")
                else:
                    for p in prestamos:
                        _imprimir_prestamo(p)
            case 3:
                return

