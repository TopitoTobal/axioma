import pytest
from axioma.lexer import Lexer, ErrorLexico
from axioma.tokens import TiposToken


def _tokenizar(codigo):
    lexer = Lexer(codigo)
    return lexer.escanear()


def _tipos(codigo):
    return [t.tipo for t in _tokenizar(codigo)]


class TestLexerBasico:
    def test_vacio(self):
        tokens = _tokenizar("")
        assert len(tokens) == 1
        assert tokens[0].tipo == TiposToken.EOF

    def test_espacios(self):
        tokens = _tokenizar("   \t  \r  ")
        assert len(tokens) == 1
        assert tokens[0].tipo == TiposToken.EOF

    def test_nueva_linea(self):
        tokens = _tokenizar("\n\n\n")
        assert len(tokens) == 1


class TestLexerNumeros:
    def test_entero(self):
        tokens = _tokenizar("42")
        assert tokens[0].tipo == TiposToken.NUMERO
        assert tokens[0].valor == 42

    def test_flotante(self):
        tokens = _tokenizar("3.14")
        assert tokens[0].tipo == TiposToken.NUMERO
        assert tokens[0].valor == 3.14

    def test_enteros_multiples(self):
        tokens = _tokenizar("1 2 3")
        assert [t.valor for t in tokens if t.tipo == TiposToken.NUMERO] == [1, 2, 3]

    def test_cero(self):
        tokens = _tokenizar("0")
        assert tokens[0].valor == 0


class TestLexerTextos:
    def test_texto_simple(self):
        tokens = _tokenizar('"hola"')
        assert tokens[0].tipo == TiposToken.TEXTO
        assert tokens[0].valor == "hola"

    def test_texto_vacio(self):
        tokens = _tokenizar('""')
        assert tokens[0].tipo == TiposToken.TEXTO
        assert tokens[0].valor == ""

    def test_texto_con_espacios(self):
        tokens = _tokenizar('"hola mundo"')
        assert tokens[0].valor == "hola mundo"

    def test_texto_sin_cerrar(self):
        with pytest.raises(ErrorLexico, match="Texto sin cerrar"):
            _tokenizar('"hola')


class TestLexerIdentificadores:
    def test_identificador_simple(self):
        tokens = _tokenizar("variable")
        assert tokens[0].tipo == TiposToken.IDENTIFICADOR
        assert tokens[0].valor == "variable"

    def test_identificador_con_guion_bajo(self):
        tokens = _tokenizar("mi_variable_123")
        assert tokens[0].tipo == TiposToken.IDENTIFICADOR
        assert tokens[0].valor == "mi_variable_123"

    def test_palabras_clave(self):
        pares = [
            ("var", TiposToken.VAR),
            ("funcion", TiposToken.FUNCION),
            ("retornar", TiposToken.RETORNAR),
            ("si", TiposToken.SI),
            ("sino", TiposToken.SINO),
            ("mientras", TiposToken.MIENTRAS),
            ("para", TiposToken.PARA),
            ("imprimir", TiposToken.IMPRIMIR),
            ("verdadero", TiposToken.VERDADERO),
            ("falso", TiposToken.FALSO),
            ("nulo", TiposToken.NULO),
            ("y", TiposToken.Y),
            ("o", TiposToken.O),
            ("no", TiposToken.NO),
            ("clase", TiposToken.CLASE),
            ("este", TiposToken.ESTE),
            ("nuevo", TiposToken.NUEVO),
            ("heredar", TiposToken.HEREDAR),
        ]
        for palabra, tipo in pares:
            tokens = _tokenizar(palabra)
            assert tokens[0].tipo == tipo, f"'{palabra}' deberia ser {tipo}"


class TestLexerOperadores:
    def test_aritmeticos(self):
        assert _tipos("+")[-2] == TiposToken.MAS
        assert _tipos("-")[-2] == TiposToken.MENOS
        assert _tipos("*")[-2] == TiposToken.POR
        assert _tipos("/")[-2] == TiposToken.DIV
        assert _tipos("%")[-2] == TiposToken.MOD

    def test_comparacion(self):
        assert _tipos("==")[-2] == TiposToken.IGUAL
        assert _tipos("!=")[-2] == TiposToken.NO_IGUAL
        assert _tipos("<")[-2] == TiposToken.MENOR
        assert _tipos(">")[-2] == TiposToken.MAYOR
        assert _tipos("<=")[-2] == TiposToken.MENOR_IGUAL
        assert _tipos(">=")[-2] == TiposToken.MAYOR_IGUAL

    def test_asignacion(self):
        assert _tipos("=")[-2] == TiposToken.ASIGNAR
        assert _tipos("+=")[-2] == TiposToken.ASIGNAR_MAS
        assert _tipos("-=")[-2] == TiposToken.ASIGNAR_MENOS
        assert _tipos("*=")[-2] == TiposToken.ASIGNAR_POR

    def test_asignacion_div(self):
        assert _tipos("/=")[-2] == TiposToken.ASIGNAR_DIV


class TestLexerSimbolos:
    def test_parentesis(self):
        assert _tipos("(")[-2] == TiposToken.PAREN_IZQ
        assert _tipos(")")[-2] == TiposToken.PAREN_DER

    def test_llaves(self):
        assert _tipos("{")[-2] == TiposToken.LLAVE_IZQ
        assert _tipos("}")[-2] == TiposToken.LLAVE_DER

    def test_corchetes(self):
        assert _tipos("[")[-2] == TiposToken.CORCH_IZQ
        assert _tipos("]")[-2] == TiposToken.CORCH_DER

    def test_otros(self):
        assert _tipos(",")[-2] == TiposToken.COMA
        assert _tipos(".")[-2] == TiposToken.PUNTO
        assert _tipos(";")[-2] == TiposToken.PUNTO_COMA
        assert _tipos(":")[-2] == TiposToken.DOS_PUNTOS


class TestLexerComentarios:
    def test_comentario_linea(self):
        tokens = _tokenizar("// esto es un comentario\nvar x;")
        assert TiposToken.VAR in [t.tipo for t in tokens]

    def test_comentario_linea_fin(self):
        tokens = _tokenizar("var x; // comentario")
        assert TiposToken.VAR in [t.tipo for t in tokens]

    def test_comentario_bloque(self):
        tokens = _tokenizar("/* comentario */ var x;")
        assert TiposToken.VAR in [t.tipo for t in tokens]

    def test_comentario_bloque_multilinea(self):
        tokens = _tokenizar("/* linea1\nlinea2 */ var x;")
        assert TiposToken.VAR in [t.tipo for t in tokens]

    def test_comentario_bloque_sin_cerrar(self):
        with pytest.raises(ErrorLexico, match="Comentario de bloque sin cerrar"):
            _tokenizar("/* hola")


class TestLexerErrores:
    def test_caracter_invalido(self):
        with pytest.raises(ErrorLexico, match="Caracter inesperado"):
            _tokenizar("@")

    def test_exclamacion_sin_igual(self):
        with pytest.raises(ErrorLexico, match="Caracter inesperado"):
            _tokenizar("!")


class TestLexerPosiciones:
    def test_linea_y_columna(self):
        tokens = _tokenizar("var\n42")
        token_var = tokens[0]
        token_num = tokens[1]
        assert token_var.linea == 1
        assert token_var.columna == 4
        assert token_num.linea == 2
        assert token_num.columna == 3

    def test_columna_despues_de_espacios(self):
        tokens = _tokenizar("   var")
        assert tokens[0].columna == 10


class TestLexerSentenciasCompletas:
    def test_declaracion_var(self):
        tipos = _tipos("var x = 10;")
        assert tipos == [
            TiposToken.VAR, TiposToken.IDENTIFICADOR,
            TiposToken.ASIGNAR, TiposToken.NUMERO,
            TiposToken.PUNTO_COMA, TiposToken.EOF
        ]

    def test_si_sentencia(self):
        tipos = _tipos("si (x) { }")
        assert TiposToken.SI in tipos
        assert TiposToken.PAREN_IZQ in tipos
        assert TiposToken.PAREN_DER in tipos
        assert TiposToken.LLAVE_IZQ in tipos
        assert TiposToken.LLAVE_DER in tipos
