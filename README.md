# Lights Out — Álgebra Aplicada

Implementación del modelo algebraico y del solver computacional del juego
Lights Out mediante sistemas lineales sobre el cuerpo finito Z₂.

## Contenido

- `lights_out.py`: módulo principal con la función `solve_lights_out`.
- `test_lights_out.py`: pruebas unitarias del solver.
- `lights_out_app.py`: aplicación gráfica interactiva basada en Tkinter.
- `requirements.txt`: dependencias del proyecto.

## Requisitos

- Python 3.10 o superior.
- pip.

## Instalación

Desde la carpeta del proyecto, ejecutar:

```bash
python3 -m pip install -r requirements.txt
```

En sistemas Ubuntu que aplican la política PEP 668, puede ser necesario usar:

```bash
python3 -m pip install --user --break-system-packages -r requirements.txt
```

## Ejecución del solver

El módulo puede importarse desde Python:

```python
from lights_out import solve_lights_out

board = [
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1],
]

presses = solve_lights_out(board)
print(presses)
```

La función recibe una matriz cuadrada de enteros binarios y devuelve un vector
binario en orden fila por fila. Cada posición del vector indica si la celda
correspondiente debe presionarse.

Si el sistema no tiene solución, la función lanza `ValueError`. Cuando existen
varias soluciones, devuelve una solución particular fijando las variables libres
en cero.

## Ejecución de las pruebas

Para ejecutar la suite completa:

```bash
python3 -m unittest -v
```

Las pruebas cubren tableros de distintos tamaños, sistemas inconsistentes,
soluciones no únicas, entradas inválidas y la construcción de la matriz de
adyacencia.

## Ejecución de la aplicación interactiva

La interfaz gráfica permite seleccionar tableros de 3×3 a 7×7, cambiar
manualmente las luces y visualizar una pista calculada por el solver.

En Linux o macOS:

```bash
python3 lights_out_app.py
```

En Windows:

```powershell
py lights_out_app.py
```

La aplicación utiliza Tkinter, que normalmente viene incluido con Python. En
Ubuntu, si Tkinter no está instalado, ejecutar:

```bash
sudo apt install python3-tk
```

Luego:

1. Seleccionar el tamaño del tablero en el selector `CONFIGURACIÓN`.
2. Pulsar `✦ NUEVO JUEGO` para generar un tablero jugable.
3. Hacer clic en las celdas para conmutarlas junto con sus vecinos ortogonales.
4. Pulsar `↺ REINICIAR` para volver al estado inicial.
5. Pulsar `⌁ RESOLVER / PISTA` para mostrar las pulsaciones sugeridas sin
   modificar el tablero.
