# Implementación de referencia

Implementación de referencia para trabajar con árboles AVL mediante un intérprete de comandos.

## Requisitos

- Python 3.14 o superior
- [uv](https://docs.astral.sh/uv/)

## Preparar el entorno

Desde la raíz del proyecto:

```powershell
uv sync
```

Este comando instala el proyecto como paquete editable y prepara el entorno virtual.

## Ejecutar el intérprete

El intérprete recibe como argumento un fichero de comandos:

```powershell
uv run python -m trees.interpreter TEST.test
```

También se puede indicar una ruta diferente:

```powershell
uv run python -m trees.interpreter ruta/al/fichero.test
```

Debe ejecutarse como módulo (`-m trees.interpreter`), no directamente mediante `python src/trees/interpreter.py`, porque el código utiliza imports relativos del paquete.

## Formato del fichero de comandos

Cada línea contiene un comando y sus argumentos. Las líneas vacías y las que comienzan por `#` se ignoran.

Ejemplo:

```text
# Cargar datos desde un fichero JSON
LOAD data.json

# Mostrar el árbol
PRINT

# Buscar una clave
FIND "Hubble"
```

Comandos disponibles:

- `LOAD <fichero>`
- `PRINT`
- `INSERT <valor>`
- `REMOVE <valor>`
- `FIND <clave>`
- `UPDATE <clave> <valor>`

## Lanzar el debugger

1. Abre la vista **Run and Debug** de VS Code (`Ctrl+Shift+D`).
2. Selecciona `Depurar interpreter con TEST.test`.
3. Pulsa `F5` o el botón de inicio.

Para depurar el programa de prueba, selecciona `Depurar test.py` en lugar de la configuración anterior.

Antes de iniciar la depuración, ejecuta `uv sync` si todavía no has preparado el entorno. Coloca puntos de interrupción haciendo clic a la izquierda del número de línea.
