# Lights Out — Álgebra Aplicada

Proyecto académico sobre el modelado algebraico y la resolución computacional del juego Lights Out mediante sistemas lineales sobre Z₂.

## Contenido

- `lights_out.py`: solver binario mediante eliminación gaussiana con XOR.
- `test_lights_out.py`: pruebas unitarias del solver.
- `requirements.txt`: dependencias del proyecto.
- `generar_informe_docx.py`: script para generar el informe Word con `python-docx`.

El informe final DOCX se entrega como archivo adjunto.

## Ejecución

```bash
python3 -m pip install -r requirements.txt
python3 -m unittest -v
python3 generar_informe_docx.py
```

Repositorio utilizado como referencia en el informe:
https://github.com/FranciscoLima18/lights-out-algebra-aplicada
