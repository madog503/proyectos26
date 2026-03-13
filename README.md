# Generador de artículos técnicos automotrices

Script en Python para generar artículos HTML en español, listos para pegar en Blogger.

## Características

- Entrada por título (`--title`) desde una lista predefinida de temas automotrices.
- Generación con estructura HTML fija solicitada (H1, secciones H2, listas y conclusión).
- Contenido enfocado en diagnóstico, síntomas, causas y solución de fallas comunes.
- Modo masivo para generar artículos de todos los títulos (`--all`).

## Uso

Listar títulos disponibles:

```bash
python3 generator.py --list-topics
```

Generar un solo artículo (salida por stdout):

```bash
python3 generator.py --title "P0300: Fallos de encendido aleatorios"
```

Generar todos los artículos en archivos `.html`:

```bash
python3 generator.py --all --output-dir output
```

Cada archivo generado queda con HTML limpio, sin envoltorios extra, para copiar y pegar directamente en Blogger.
