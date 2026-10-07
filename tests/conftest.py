import pytest
from axioma.lexer import Lexer
from axioma.parser import Parser
from axioma.interprete import Interprete


def tokenizar(codigo):
    lexer = Lexer(codigo)
    return lexer.escanear()


def parsear(codigo):
    tokens = tokenizar(codigo)
    parser = Parser(tokens)
    return parser.parse()


def interpretar(codigo):
    arbol = parsear(codigo)
    interprete = Interprete()
    interprete.interpretar(arbol)
    return interprete


def evaluar_expresion(codigo):
    codigo_completo = f"var _r = {codigo}; imprimir _r;"
    import io
    from contextlib import redirect_stdout
    arbol = parsear(codigo_completo)
    interprete = Interprete()
    f = io.StringIO()
    with redirect_stdout(f):
        interprete.interpretar(arbol)
    salida = f.getvalue().strip()
    return salida


@pytest.fixture
def interprete():
    return Interprete()
