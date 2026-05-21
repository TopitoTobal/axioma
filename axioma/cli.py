import sys
import os


def ejecutar_archivo(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        codigo = f.read()
    return _ejecutar(codigo, ruta)


def ejecutar_repl():
    from .logo import LOGO
    print(LOGO)
    print("Axioma v1.0 - Lenguaje de programacion en espanol")
    print("Escribe 'salir()' para terminar")
    entorno_historial = None
    while True:
        try:
            linea = input(">>> ")
            if linea.strip() == "salir()":
                break
            if not linea.strip():
                continue
            resultado = _ejecutar(linea, "<repl>")
            if resultado is not None:
                print(resultado)
        except KeyboardInterrupt:
            print("\nAdios!")
            break
        except Exception as e:
            print(f"Error: {e}")


def _ejecutar(codigo, origen):
    from .lexer import Lexer, ErrorLexico
    from .parser import Parser, ErrorSintaxis
    from .interprete import Interprete, ErrorEjecucion

    lexer = Lexer(codigo)
    try:
        tokens = lexer.escanear()
    except ErrorLexico as e:
        print(f"{origen}: {e}")
        return None

    parser = Parser(tokens)
    try:
        arbol = parser.parse()
    except ErrorSintaxis as e:
        print(f"{origen}: {e}")
        return None

    interprete = Interprete()
    try:
        return interprete.interpretar(arbol)
    except ErrorEjecucion as e:
        print(f"{origen}: {e}")
        return None


def main():
    if len(sys.argv) > 1:
        ruta = sys.argv[1]
        if not os.path.exists(ruta):
            print(f"Archivo no encontrado: {ruta}")
            sys.exit(1)
        ejecutar_archivo(ruta)
    else:
        ejecutar_repl()
