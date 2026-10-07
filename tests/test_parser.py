import pytest
from axioma.lexer import Lexer
from axioma.parser import Parser, ErrorSintaxis
from axioma.tokens import TiposToken
from axioma.ast import (
    Programa, DeclararVar, AsignarVar, AsignarOp,
    DeclararFuncion, Retornar, Si, Mientras, Para, Bloque,
    Imprimir, ExpresionStmt, Binaria, Unaria, Literal,
    Variable, Llamada, GetAttr, DeclararClase,
    Este, Nueva, AccesoLista, AsignarLista, LiteralLista,
)


def _parsear(codigo):
    lexer = Lexer(codigo)
    tokens = lexer.escanear()
    parser = Parser(tokens)
    return parser.parse()


class TestParserDeclaraciones:
    def test_programa_vacio(self):
        arbol = _parsear("")
        assert isinstance(arbol, Programa)
        assert arbol.declaraciones == []

    def test_declarar_var_sin_valor(self):
        arbol = _parsear("var x;")
        assert isinstance(arbol.declaraciones[0], DeclararVar)
        assert arbol.declaraciones[0].nombre == "x"
        assert arbol.declaraciones[0].valor is None

    def test_declarar_var_con_valor(self):
        arbol = _parsear("var x = 10;")
        stmt = arbol.declaraciones[0]
        assert isinstance(stmt, DeclararVar)
        assert stmt.nombre == "x"
        assert isinstance(stmt.valor, Literal)
        assert stmt.valor.valor == 10

    def test_asignar_var(self):
        arbol = _parsear("x = 5;")
        stmt = arbol.declaraciones[0]
        assert isinstance(stmt, ExpresionStmt)
        assert isinstance(stmt.expresion, AsignarVar)
        assert stmt.expresion.nombre == "x"
        assert stmt.expresion.valor.valor == 5

    def test_declarar_funcion_sin_parametros(self):
        arbol = _parsear("funcion foo() { }")
        stmt = arbol.declaraciones[0]
        assert isinstance(stmt, DeclararFuncion)
        assert stmt.nombre == "foo"
        assert stmt.parametros == []

    def test_declarar_funcion_con_parametros(self):
        arbol = _parsear("funcion suma(a, b) { retornar a + b; }")
        stmt = arbol.declaraciones[0]
        assert isinstance(stmt, DeclararFuncion)
        assert stmt.nombre == "suma"
        assert stmt.parametros == ["a", "b"]

    def test_declarar_clase_sin_padre(self):
        arbol = _parsear("clase Foo { }")
        stmt = arbol.declaraciones[0]
        assert isinstance(stmt, DeclararClase)
        assert stmt.nombre == "Foo"
        assert stmt.padre is None

    def test_declarar_clase_con_padre(self):
        arbol = _parsear("clase Perro heredar Animal { }")
        stmt = arbol.declaraciones[0]
        assert isinstance(stmt, DeclararClase)
        assert stmt.nombre == "Perro"
        assert stmt.padre == "Animal"


class TestParserControlFlujo:
    def test_si_simple(self):
        arbol = _parsear("si (x) { }")
        stmt = arbol.declaraciones[0]
        assert isinstance(stmt, Si)
        assert isinstance(stmt.condicion, Variable)
        assert stmt.condicion.nombre == "x"
        assert isinstance(stmt.entonces, Bloque)

    def test_si_sino(self):
        arbol = _parsear("si (x) { } sino { }")
        stmt = arbol.declaraciones[0]
        assert isinstance(stmt, Si)
        assert isinstance(stmt.sino, Bloque)

    def test_mientras(self):
        arbol = _parsear("mientras (x < 10) { }")
        stmt = arbol.declaraciones[0]
        assert isinstance(stmt, Mientras)
        assert isinstance(stmt.condicion, Binaria)

    def test_para_completo(self):
        arbol = _parsear("para (var i = 0; i < 10; i = i + 1) { }")
        stmt = arbol.declaraciones[0]
        assert isinstance(stmt, Para)
        assert isinstance(stmt.inicializacion, DeclararVar)
        assert stmt.inicializacion.nombre == "i"
        assert isinstance(stmt.condicion, Binaria)
        assert isinstance(stmt.incremento, AsignarVar)

    def test_para_sin_inicializacion(self):
        arbol = _parsear("para (; x < 10; x = x + 1) { }")
        stmt = arbol.declaraciones[0]
        assert isinstance(stmt, Para)
        assert stmt.inicializacion is None

    def test_retornar_sin_valor(self):
        arbol = _parsear("retornar;")
        stmt = arbol.declaraciones[0]
        assert isinstance(stmt, Retornar)
        assert stmt.valor is None

    def test_retornar_con_valor(self):
        arbol = _parsear("retornar 42;")
        stmt = arbol.declaraciones[0]
        assert isinstance(stmt, Retornar)
        assert stmt.valor.valor == 42

    def test_retornar_variable(self):
        arbol = _parsear("retornar x;")
        stmt = arbol.declaraciones[0]
        assert isinstance(stmt, Retornar)
        assert isinstance(stmt.valor, Variable)

    def test_imprimir(self):
        arbol = _parsear('imprimir "hola";')
        stmt = arbol.declaraciones[0]
        assert isinstance(stmt, Imprimir)
        assert stmt.expresion.valor == "hola"


class TestParserExpresiones:
    def test_literal_numero(self):
        arbol = _parsear("var x = 42;")
        assert arbol.declaraciones[0].valor.valor == 42

    def test_literal_texto(self):
        arbol = _parsear('var x = "hola";')
        assert arbol.declaraciones[0].valor.valor == "hola"

    def test_literal_bool(self):
        arbol = _parsear("var x = verdadero;")
        assert arbol.declaraciones[0].valor.valor is True
        arbol2 = _parsear("var x = falso;")
        assert arbol2.declaraciones[0].valor.valor is False

    def test_literal_nulo(self):
        arbol = _parsear("var x = nulo;")
        assert arbol.declaraciones[0].valor.valor is None

    def test_variable(self):
        arbol = _parsear("x;")
        stmt = arbol.declaraciones[0]
        assert isinstance(stmt, ExpresionStmt)
        assert isinstance(stmt.expresion, Variable)
        assert stmt.expresion.nombre == "x"

    def test_binaria_suma(self):
        arbol = _parsear("1 + 2;")
        stmt = arbol.declaraciones[0]
        assert isinstance(stmt, ExpresionStmt)
        expr = stmt.expresion
        assert isinstance(expr, Binaria)
        assert expr.operador.tipo == TiposToken.MAS
        assert expr.izquierda.valor == 1
        assert expr.derecha.valor == 2

    def test_binaria_precedencia(self):
        arbol = _parsear("1 + 2 * 3;")
        stmt = arbol.declaraciones[0]
        expr = stmt.expresion
        assert isinstance(expr, Binaria)
        assert expr.operador.tipo == TiposToken.MAS
        assert isinstance(expr.derecha, Binaria)
        assert expr.derecha.operador.tipo == TiposToken.POR

    def test_unaria_menos(self):
        arbol = _parsear("-5;")
        stmt = arbol.declaraciones[0]
        assert isinstance(stmt, ExpresionStmt)
        assert isinstance(stmt.expresion, Unaria)
        assert stmt.expresion.operador.tipo == TiposToken.MENOS

    def test_unaria_no(self):
        arbol = _parsear("no verdadero;")
        stmt = arbol.declaraciones[0]
        assert isinstance(stmt, ExpresionStmt)
        assert isinstance(stmt.expresion, Unaria)
        assert stmt.expresion.operador.tipo == TiposToken.NO

    def test_parentesis(self):
        arbol = _parsear("(1 + 2) * 3;")
        stmt = arbol.declaraciones[0]
        expr = stmt.expresion
        assert isinstance(expr, Binaria)
        assert expr.operador.tipo == TiposToken.POR
        assert isinstance(expr.izquierda, Binaria)
        assert expr.izquierda.operador.tipo == TiposToken.MAS

    def test_comparacion_encadenada(self):
        arbol = _parsear("1 < 2 == 3 > 4;")
        stmt = arbol.declaraciones[0]
        assert isinstance(stmt.expresion, Binaria)
        tokens = [stmt.expresion.operador.tipo]
        assert tokens == [TiposToken.IGUAL]


class TestParserLogicos:
    def test_y(self):
        arbol = _parsear("a y b;")
        stmt = arbol.declaraciones[0]
        assert isinstance(stmt.expresion, Binaria)
        assert stmt.expresion.operador.tipo == TiposToken.Y

    def test_o(self):
        arbol = _parsear("a o b;")
        stmt = arbol.declaraciones[0]
        assert isinstance(stmt.expresion, Binaria)
        assert stmt.expresion.operador.tipo == TiposToken.O

    def test_no(self):
        arbol = _parsear("no a;")
        stmt = arbol.declaraciones[0]
        assert isinstance(stmt.expresion, Unaria)
        assert stmt.expresion.operador.tipo == TiposToken.NO


class TestParserLlamadas:
    def test_llamada_sin_argumentos(self):
        arbol = _parsear("foo();")
        stmt = arbol.declaraciones[0]
        assert isinstance(stmt, ExpresionStmt)
        assert isinstance(stmt.expresion, Llamada)
        assert stmt.expresion.argumentos == []

    def test_llamada_con_argumentos(self):
        arbol = _parsear("foo(1, 2);")
        stmt = arbol.declaraciones[0]
        assert isinstance(stmt, ExpresionStmt)
        assert isinstance(stmt.expresion, Llamada)
        assert len(stmt.expresion.argumentos) == 2

    def test_llamada_anidada(self):
        arbol = _parsear("foo(bar());")
        stmt = arbol.declaraciones[0]
        assert isinstance(stmt, ExpresionStmt)
        assert isinstance(stmt.expresion, Llamada)
        assert isinstance(stmt.expresion.argumentos[0], Llamada)

    def test_get_attr(self):
        arbol = _parsear("obj.prop;")
        stmt = arbol.declaraciones[0]
        assert isinstance(stmt, ExpresionStmt)
        assert isinstance(stmt.expresion, GetAttr)
        assert stmt.expresion.nombre == "prop"

    def test_llamada_metodo(self):
        arbol = _parsear("obj.metodo(1);")
        stmt = arbol.declaraciones[0]
        assert isinstance(stmt, ExpresionStmt)
        assert isinstance(stmt.expresion, Llamada)
        assert isinstance(stmt.expresion.callee, GetAttr)


class TestParserListas:
    def test_lista_vacia(self):
        arbol = _parsear("var x = [];")
        stmt = arbol.declaraciones[0]
        assert isinstance(stmt.valor, LiteralLista)
        assert stmt.valor.elementos == []

    def test_lista_con_elementos(self):
        arbol = _parsear("var x = [1, 2, 3];")
        stmt = arbol.declaraciones[0]
        assert isinstance(stmt.valor, LiteralLista)
        assert len(stmt.valor.elementos) == 3

    def test_acceso_lista(self):
        arbol = _parsear("x[0];")
        stmt = arbol.declaraciones[0]
        assert isinstance(stmt, ExpresionStmt)
        assert isinstance(stmt.expresion, AccesoLista)


class TestParserErrores:
    def test_punto_y_coma_faltante(self):
        with pytest.raises(ErrorSintaxis):
            _parsear("var x")

    def test_parentesis_faltante(self):
        with pytest.raises(ErrorSintaxis):
            _parsear("si (x { }")

    def test_expresion_inesperada(self):
        with pytest.raises(ErrorSintaxis, match="Expresion inesperada"):
            _parsear("}")

    def test_identificador_esperado(self):
        with pytest.raises(ErrorSintaxis):
            _parsear("var 123;")

    def test_parametro_invalido(self):
        with pytest.raises(ErrorSintaxis):
            _parsear("funcion f(123) { }")
