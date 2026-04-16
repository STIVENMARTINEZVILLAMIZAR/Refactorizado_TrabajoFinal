# Code-Optimization

Este repositorio contiene dos versiones del mismo sistema de consola (Gestión de Herramientas, Usuarios, Préstamos, Reportes y Logs):

- `Trabajo_final/`: baseline original (implementación monolítica por archivos `menu_*.py` y `gestionar_*.py`).
- `Trabajo_final_v2/`: refactor MVC con persistencia desacoplada (puertos + adaptadores JSON/TXT).

## Cómo ejecutar la versión v2

`cd Code-Optimization/Trabajo_final_v2`

Ejecutar:

`python main.py`

Se crearán/leerán los archivos de datos en el directorio `Trabajo_final_v2/`:
`usuarios.json`, `categorias.json`, `herramientas.json`, `prestamos.json` y `historial.txt`.

## Objetivos de `Trabajo_final_v2`

- Mantener el comportamiento de consola y flujo de negocio del baseline.
- Reorganizar responsabilidades por capas:
  - `presentation/` (menús CLI, prompts e impresión)
  - `controllers/` (orquestación)
  - `application/` (casos de uso/servicios)
  - `domain/` (entidades, enums y DTOs)
  - `infrastructure/` (persistencia JSON/TXT y logger, wiring)
- Diseñar persistencia con Open/Closed para agregar después un adaptador SQL/ORM sin tocar la lógica de negocio.

