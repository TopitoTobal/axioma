import sys
import os
import argparse


VERSION = "1.0.0"


# --- Colores ANSI ---
class Color:
    ROJO = "\033[91m"
    VERDE = "\033[92m"
    AMARILLO = "\033[93m"
    AZUL = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    NEGRITA = "\033[1m"
    RESET = "\033[0m"
    GRIS = "\033[90m"


def _usar_colores():
    return os.name != "nt" or os.environ.get("TERM_PROGRAM") in (
        "vscode", "mintty", "ghostty"
    ) or "WT_SESSION" in os.environ or "ANSICON" in os.environ


def _col(coloreado, texto):
    return f"{coloreado}{texto}{Color.RESET}" if _usar_colores() else texto


def _mostrar_error(origen, codigo, linea, columna, mensaje, tipo="Error"):
    lineas = codigo.split("\n")
    label = _col(Color.ROJO + Color.NEGRITA, f"{tipo}:")
    encabezado = _col(Color.GRIS, f"{origen}:{linea}:{columna}") if origen != "<repl>" else _col(Color.GRIS, f"L{linea}:{columna}")

    print(f"  {encabezado} {label} {_col(Color.AMARILLO, mensaje)}")

    if 0 <= linea - 1 < len(lineas):
        ln = lineas[linea - 1]
        num_str = f"{linea:4d}"
        print(f"  {_col(Color.GRIS, num_str)} | {ln}")
        caret = " " * (columna - 1) + _col(Color.VERDE + Color.NEGRITA, "^" if columna <= len(ln) else "")
        print(f"  {_col(Color.GRIS, '     |')} {caret}")


def ejecutar_archivo(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        codigo = f.read()
    return _ejecutar(codigo, ruta)


def ejecutar_repl():
    try:
        import readline
    except ImportError:
        try:
            import pyreadline3 as readline
        except ImportError:
            pass

    from .logo import LOGO
    print(LOGO)
    print(f"Axioma v{VERSION} - Lenguaje de programacion en espanol")
    print("Escribe 'salir()' para terminar")
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
        except EOFError:
            print()
            break
        except Exception as e:
            print(f"  {_col(Color.ROJO + Color.NEGRITA, 'Error:')} {e}")


def _ejecutar(codigo, origen):
    from .lexer import Lexer, ErrorLexico
    from .parser import Parser, ErrorSintaxis
    from .interprete import Interprete, ErrorEjecucion

    lexer = Lexer(codigo)
    try:
        tokens = lexer.escanear()
    except ErrorLexico as e:
        _mostrar_error(origen, codigo, e.linea, e.columna, e.mensaje, "Error lexico")
        return None

    parser = Parser(tokens)
    try:
        arbol = parser.parse()
    except ErrorSintaxis as e:
        _mostrar_error(origen, codigo, e.token.linea, e.token.columna, e.mensaje, "Error sintactico")
        return None

    interprete = Interprete()
    try:
        return interprete.interpretar(arbol)
    except ErrorEjecucion as e:
        print(f"  {_col(Color.GRIS, origen)} {_col(Color.ROJO + Color.NEGRITA, 'Error en ejecucion:')} {_col(Color.AMARILLO, e.mensaje)}")
        return None


def main():
    parser = argparse.ArgumentParser(
        prog="axioma",
        description="Lenguaje de programacion en espanol",
        add_help=False,
    )
    parser.add_argument("--version", action="store_true", help="Muestra la version y sale")
    parser.add_argument("--help", action="store_true", help="Muestra esta ayuda y sale")
    parser.add_argument("--repl", action="store_true", help="Fuerza el modo interactivo")
    parser.add_argument("-c", type=str, metavar="<codigo>", help="Ejecuta codigo inline")
    parser.add_argument("archivo", nargs="?", type=str, help="Archivo .ax a ejecutar")
    args = parser.parse_args()

    if args.version:
        print(f"Axioma v{VERSION}")
        return

    if args.help:
        print("Uso: axioma [--version] [--help] [--repl] [-c <codigo>] [<archivo>]")
        print()
        print("Opciones:")
        print("  --version              Muestra la version y sale")
        print("  --help                 Muestra esta ayuda y sale")
        print("  --repl                 Fuerza el modo interactivo")
        print("  -c <codigo>            Ejecuta codigo inline")
        print()
        print("Ejemplos:")
        print("  axioma                 Modo interactivo (REPL)")
        print("  axioma archivo.ax      Ejecuta un archivo")
        print('  axioma -c "imprimir 2+2"')
        print("  axioma --repl          Fuerza el REPL")
        return

    if args.c:
        _ejecutar(args.c, "<inline>")
        return

    if args.archivo:
        if not os.path.exists(args.archivo):
            print(f"  {_col(Color.ROJO + Color.NEGRITA, 'Error:')} archivo no encontrado: {args.archivo}")
            sys.exit(1)
        ejecutar_archivo(args.archivo)
        return

    ejecutar_repl()
