# Persistencia JSON/TXT (Open/Closed)

Persistencia en v2:

- Archivos JSON:
  - `usuarios.json`
  - `categorias.json`
  - `herramientas.json`
  - `prestamos.json`
- Archivo TXT:
  - `historial.txt`

Cómo se desacopla:

- Puertos en `Trabajo_final_v2/infrastructure/ports/`:
  - repositorios por agregado (`UsuarioRepository`, `CategoriaRepository`, `HerramientaRepository`, `PrestamoRepository`)
  - `AuditLogRepository` para historial
- Adaptadores en `Trabajo_final_v2/infrastructure/json/` y `Trabajo_final_v2/infrastructure/txt/`:
  - repositorios JSON implementan los puertos con lista de dicts
  - logger TXT hace append y mantiene el formato baseline
- Wiring central:
  - `Trabajo_final_v2/infrastructure/factory.py` crea repositorios, servicios, controladores y la UI.

Extensión futura:

Para conectar una DB/ORM, se crean adaptadores nuevos que implementen los puertos, y sólo se cambia `factory.py`.

