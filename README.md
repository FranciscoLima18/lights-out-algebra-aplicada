# Lights Out — Álgebra Aplicada

Implementación del modelo algebraico y del solver computacional del juego Lights Out mediante sistemas lineales sobre el cuerpo finito Z₂.

## Contenido

- `lights_out.py`: módulo principal con la función `solve_lights_out`.
- `test_lights_out.py`: pruebas unitarias del solver.
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

La función recibe una matriz cuadrada de enteros binarios y devuelve un vector binario en orden fila por fila. Cada posición del vector indica si la celda correspondiente debe presionarse.

Si el sistema no tiene solución, la función lanza `ValueError`. Cuando existen varias soluciones, devuelve una solución particular fijando las variables libres en cero.

## Ejecución de las pruebas

Para ejecutar la suite completa:

```bash
python3 -m unittest -v
```

Las pruebas cubren tableros de distintos tamaños, sistemas inconsistentes, soluciones no únicas, entradas inválidas y la construcción de la matriz de adyacencia.
