import io
import pytest
from contextlib import redirect_stdout

from axioma.lexer import Lexer
from axioma.parser import Parser
from axioma.interprete import Interprete, ErrorEjecucion
from axioma.tokens import TiposToken


def evaluar_expresion(codigo):
    codigo_completo = f"var _r = {codigo}; imprimir _r;"
    arbol = Parser(Lexer(codigo_completo).escanear()).parse()
    interprete = Interprete()
    f = io.StringIO()
    with redirect_stdout(f):
        interprete.interpretar(arbol)
    return f.getvalue().strip()


def ejecutar(codigo):
    arbol = Parser(Lexer(codigo).escanear()).parse()
    interprete = Interprete()
    f = io.StringIO()
    with redirect_stdout(f):
        interprete.interpretar(arbol)
    return f.getvalue().strip()


def tokenizar(codigo):
    return Lexer(codigo).escanear()


class TestLexerNuevosTokens:
    def test_punto_punto(self):
        tokens = tokenizar("1..5")
        tipos = [t.tipo for t in tokens]
        assert tipos == [TiposToken.NUMERO, TiposToken.PUNTO_PUNTO, TiposToken.NUMERO, TiposToken.EOF]

    def test_punto_simple_sigue_funcionando(self):
        tokens = tokenizar("a.b")
        tipos = [t.tipo for t in tokens]
        assert tipos == [TiposToken.IDENTIFICADOR, TiposToken.PUNTO, TiposToken.IDENTIFICADOR, TiposToken.EOF]

    def test_flotante_sigue(self):
        tokens = tokenizar("1.5")
        assert tokens[0].valor == 1.5

    def test_flotante_rango(self):
        tokens = tokenizar("1.5..3")
        assert tokens[0].valor == 1.5
        assert tokens[1].tipo == TiposToken.PUNTO_PUNTO

    def test_keywords(self):
        for palabra, tipo in [("segun", TiposToken.SEGUN), ("caso", TiposToken.CASO),
                              ("defecto", TiposToken.DEFECTO), ("intentar", TiposToken.INTENTAR),
                              ("atrapar", TiposToken.ATRAPAR)]:
            assert tokenizar(palabra)[0].tipo == tipo


class TestRango:
    def test_rango_basico(self):
        assert evaluar_expresion("1..5") == "[1, 2, 3, 4, 5]"

    def test_rango_uno(self):
        assert evaluar_expresion("3..3") == "[3]"

    def test_rango_vacio_invertido(self):
        assert evaluar_expresion("5..1") == "[]"

    def test_rango_no_entero(self):
        import pytest
        from axioma.interprete import ErrorEjecucion
        with pytest.raises(ErrorEjecucion):
            evaluar_expresion("1.5..5")

    def test_rango_en_para(self):
        from axioma.lexer import Lexer
        from axioma.parser import Parser
        from axioma.interprete import Interprete
        import io
        from contextlib import redirect_stdout
        src = "var s = 0;\npara (var i = 0; i < len(1..4); i = i + 1) { s = s + 1; }\nimprimir s;"
        f = io.StringIO()
        with redirect_stdout(f):
            Interprete().interpretar(Parser(Lexer(src).escanear()).parse())
        assert f.getvalue().strip() == "4"


class TestDiccionarios:
    def test_literal(self):
        assert evaluar_expresion('{"a": 1, "b": 2}') == "{a: 1, b: 2}"

    def test_acceso(self):
        assert evaluar_expresion('{"a": 1}["a"]') == "1"

    def test_asignacion(self):
        from axioma.lexer import Lexer
        from axioma.parser import Parser
        from axioma.interprete import Interprete
        import io
        from contextlib import redirect_stdout
        src = 'var d = {"a": 1};\nd["b"] = 2;\nimprimir d["b"];'
        f = io.StringIO()
        with redirect_stdout(f):
            Interprete().interpretar(Parser(Lexer(src).escanear()).parse())
        assert f.getvalue().strip() == "2"

    def test_len_dict(self):
        assert evaluar_expresion('len({"a": 1, "b": 2})') == "2"

    def test_clave_inexistente(self):
        import pytest
        from axioma.interprete import ErrorEjecucion
        with pytest.raises(ErrorEjecucion):
            evaluar_expresion('{"a": 1}["zzz"]')

    def test_getattr_dict(self):
        assert evaluar_expresion('{"a": 42}.a') == "42"


class TestMetodosLista:
    def test_empujar(self):
        from axioma.lexer import Lexer
        from axioma.parser import Parser
        from axioma.interprete import Interprete
        import io
        from contextlib import redirect_stdout
        src = "var l = [1, 2];\nl.empujar(3);\nimprimir l;"
        f = io.StringIO()
        with redirect_stdout(f):
            Interprete().interpretar(Parser(Lexer(src).escanear()).parse())
        assert f.getvalue().strip() == "[1, 2, 3]"

    def test_sacar(self):
        assert evaluar_expresion("[1, 2, 3].sacar()") == "3"

    def test_sacar_indice(self):
        assert evaluar_expresion("[1, 2, 3].sacar(0)") == "1"

    def test_longitud(self):
        assert evaluar_expresion("[1, 2, 3].longitud()") == "3"

    def test_vaciar(self):
        from axioma.lexer import Lexer
        from axioma.parser import Parser
        from axioma.interprete import Interprete
        import io
        from contextlib import redirect_stdout
        src = "var l = [1, 2];\nl.vaciar();\nimprimir l;"
        f = io.StringIO()
        with redirect_stdout(f):
            Interprete().interpretar(Parser(Lexer(src).escanear()).parse())
        assert f.getvalue().strip() == "[]"

    def test_metodo_desconocido(self):
        import pytest
        from axioma.interprete import ErrorEjecucion
        with pytest.raises(ErrorEjecucion):
            evaluar_expresion("[1].borrar()")


class TestSegun:
    def test_caso_basico(self):
        from axioma.lexer import Lexer
        from axioma.parser import Parser
        from axioma.interprete import Interprete
        import io
        from contextlib import redirect_stdout
        src = '''segun (2) {
    caso 1: imprimir "uno";
    caso 2: imprimir "dos";
    defecto: imprimir "otro";
}'''
        f = io.StringIO()
        with redirect_stdout(f):
            Interprete().interpretar(Parser(Lexer(src).escanear()).parse())
        assert f.getvalue().strip() == "dos"

    def test_defecto(self):
        from axioma.lexer import Lexer
        from axioma.parser import Parser
        from axioma.interprete import Interprete
        import io
        from contextlib import redirect_stdout
        src = '''segun (99) {
    caso 1: imprimir "uno";
    defecto: imprimir "otro";
}'''
        f = io.StringIO()
        with redirect_stdout(f):
            Interprete().interpretar(Parser(Lexer(src).escanear()).parse())
        assert f.getvalue().strip() == "otro"

    def test_segun_string(self):
        from axioma.lexer import Lexer
        from axioma.parser import Parser
        from axioma.interprete import Interprete
        import io
        from contextlib import redirect_stdout
        src = '''segun ("b") {
    caso "a": imprimir 1;
    caso "b": imprimir 2;
}'''
        f = io.StringIO()
        with redirect_stdout(f):
            Interprete().interpretar(Parser(Lexer(src).escanear()).parse())
        assert f.getvalue().strip() == "2"


class TestIntentar:
    def test_atrapa_error(self):
        from axioma.lexer import Lexer
        from axioma.parser import Parser
        from axioma.interprete import Interprete
        import io
        from contextlib import redirect_stdout
        src = '''intentar {
    var x = 1 / 0;
} atrapar (e) {
    imprimir e;
}'''
        f = io.StringIO()
        with redirect_stdout(f):
            Interprete().interpretar(Parser(Lexer(src).escanear()).parse())
        assert f.getvalue().strip() == "Division por cero"

    def test_sin_error(self):
        from axioma.lexer import Lexer
        from axioma.parser import Parser
        from axioma.interprete import Interprete
        import io
        from contextlib import redirect_stdout
        src = '''intentar {
    imprimir "ok";
} atrapar (e) {
    imprimir "error";
}'''
        f = io.StringIO()
        with redirect_stdout(f):
            Interprete().interpretar(Parser(Lexer(src).escanear()).parse())
        assert f.getvalue().strip() == "ok"

    def test_atrapar_sin_variable(self):
        from axioma.lexer import Lexer
        from axioma.parser import Parser
        from axioma.interprete import Interprete
        import io
        from contextlib import redirect_stdout
        src = '''intentar {
    var l = [1];
    imprimir l[5];
} atrapar {
    imprimir "atrapado";
}'''
        f = io.StringIO()
        with redirect_stdout(f):
            Interprete().interpretar(Parser(Lexer(src).escanear()).parse())
        assert f.getvalue().strip() == "atrapado"


class TestIndiceString:
    def test_acceso_string(self):
        assert evaluar_expresion('"hola"[1]') == "o"
