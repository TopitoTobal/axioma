import pytest
import io
from contextlib import redirect_stdout
import os
from axioma.cli import _ejecutar


CARPETA_EJEMPLOS = os.path.join(os.path.dirname(__file__), "..", "ejemplos")


def _ejecutar_archivo(nombre):
    ruta = os.path.join(CARPETA_EJEMPLOS, nombre)
    with open(ruta, "r", encoding="utf-8") as f:
        codigo = f.read()
    f_io = io.StringIO()
    with redirect_stdout(f_io):
        _ejecutar(codigo, ruta)
    return f_io.getvalue()


@pytest.mark.parametrize("archivo", [
    "hola_mundo.ax",
    "fibonacci.ax",
    "clases.ax",
    "listas.ax",
    "numero_primo.ax",
    "diccionarios.ax",
    "rango.ax",
    "segun.ax",
    "intentar.ax",
])
def test_ejemplo(archivo):
    ruta = os.path.join(CARPETA_EJEMPLOS, archivo)
    assert os.path.exists(ruta), f"Archivo no encontrado: {ruta}"
    salida = _ejecutar_archivo(archivo)
    assert salida is not None
    assert len(salida) > 0
