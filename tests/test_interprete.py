import pytest
import io
from contextlib import redirect_stdout
from axioma.lexer import Lexer
from axioma.parser import Parser
from axioma.interprete import Interprete, ErrorEjecucion


def _interpretar(codigo):
    lexer = Lexer(codigo)
    tokens = lexer.escanear()
    parser = Parser(tokens)
    arbol = parser.parse()
    interprete = Interprete()
    f = io.StringIO()
    with redirect_stdout(f):
        interprete.interpretar(arbol)
    return f.getvalue()


def _interpretar_devuelve(codigo):
    lexer = Lexer(codigo)
    tokens = lexer.escanear()
    parser = Parser(tokens)
    arbol = parser.parse()
    interprete = Interprete()
    return interprete.interpretar(arbol)


def test_hola_mundo():
    salida = _interpretar('imprimir "Hola, mundo!";')
    assert salida.strip() == "Hola, mundo!"


class TestInterpreteNumeros:
    def test_entero(self):
        salida = _interpretar("imprimir 42;")
        assert salida.strip() == "42"

    def test_flotante(self):
        salida = _interpretar("imprimir 3.14;")
        assert salida.strip() == "3.14"

    def test_suma(self):
        salida = _interpretar("imprimir 1 + 2;")
        assert salida.strip() == "3"

    def test_resta(self):
        salida = _interpretar("imprimir 5 - 3;")
        assert salida.strip() == "2"

    def test_multiplicacion(self):
        salida = _interpretar("imprimir 4 * 3;")
        assert salida.strip() == "12"

    def test_division(self):
        salida = _interpretar("imprimir 10 / 2;")
        assert salida.strip() == "5"

    def test_modulo(self):
        salida = _interpretar("imprimir 10 % 3;")
        assert salida.strip() == "1"

    def test_precedencia(self):
        salida = _interpretar("imprimir 1 + 2 * 3;")
        assert salida.strip() == "7"

    def test_parentesis(self):
        salida = _interpretar("imprimir (1 + 2) * 3;")
        assert salida.strip() == "9"

    def test_negativo(self):
        salida = _interpretar("imprimir -5;")
        assert salida.strip() == "-5"

    def test_division_por_cero(self):
        with pytest.raises(ErrorEjecucion, match="Division por cero"):
            _interpretar_devuelve("imprimir 5 / 0;")

    def test_operacion_tipo_invalido(self):
        with pytest.raises(ErrorEjecucion, match="Se esperaba un numero"):
            _interpretar_devuelve('imprimir "hola" - 1;')


class TestInterpreteTextos:
    def test_texto(self):
        salida = _interpretar('imprimir "hola";')
        assert salida.strip() == "hola"

    def test_concatenacion(self):
        salida = _interpretar('imprimir "hola " + "mundo";')
        assert salida.strip() == "hola mundo"

    def test_concatenacion_con_numero(self):
        salida = _interpretar('imprimir "numero: " + 42;')
        assert salida.strip() == "numero: 42"


class TestInterpreteBooleanos:
    def test_verdadero(self):
        salida = _interpretar("imprimir verdadero;")
        assert salida.strip() == "verdadero"

    def test_falso(self):
        salida = _interpretar("imprimir falso;")
        assert salida.strip() == "falso"

    def test_no(self):
        salida = _interpretar("imprimir no verdadero;")
        assert salida.strip() == "falso"

    def test_y(self):
        salida = _interpretar("imprimir verdadero y falso;")
        assert salida.strip() == "falso"

    def test_o(self):
        salida = _interpretar("imprimir verdadero o falso;")
        assert salida.strip() == "verdadero"

    def test_igualdad(self):
        salida = _interpretar("imprimir 5 == 5;")
        assert salida.strip() == "verdadero"

    def test_desigualdad(self):
        salida = _interpretar("imprimir 5 != 3;")
        assert salida.strip() == "verdadero"


class TestInterpreteVariables:
    def test_declarar_y_usar(self):
        salida = _interpretar("var x = 10; imprimir x;")
        assert salida.strip() == "10"

    def test_asignar(self):
        salida = _interpretar("var x = 1; x = 2; imprimir x;")
        assert salida.strip() == "2"

    def test_asignar_mas(self):
        salida = _interpretar("var x = 5; x += 3; imprimir x;")
        assert salida.strip() == "8"

    def test_asignar_menos(self):
        salida = _interpretar("var x = 5; x -= 2; imprimir x;")
        assert salida.strip() == "3"

    def test_asignar_por(self):
        salida = _interpretar("var x = 3; x *= 4; imprimir x;")
        assert salida.strip() == "12"

    def test_variable_no_definida(self):
        with pytest.raises(ErrorEjecucion, match="Variable 'x' no definida"):
            _interpretar_devuelve("imprimir x;")


class TestInterpreteControlFlujo:
    def test_si_verdadero(self):
        salida = _interpretar("si (verdadero) { imprimir 1; }")
        assert salida.strip() == "1"

    def test_si_falso(self):
        salida = _interpretar("si (falso) { imprimir 1; }")
        assert salida.strip() == ""

    def test_si_sino(self):
        salida = _interpretar("si (falso) { imprimir 1; } sino { imprimir 2; }")
        assert salida.strip() == "2"

    def test_mientras(self):
        codigo = """
        var i = 0;
        mientras (i < 3) {
            imprimir i;
            i = i + 1;
        }
        """
        salida = _interpretar(codigo)
        assert salida.strip().split() == ["0", "1", "2"]

    def test_para(self):
        codigo = """
        para (var i = 0; i < 3; i = i + 1) {
            imprimir i;
        }
        """
        salida = _interpretar(codigo)
        assert salida.strip().split() == ["0", "1", "2"]

    def test_para_sin_condicion(self):
        codigo = """
        var i = 0;
        mientras (i < 3) {
            imprimir i;
            i = i + 1;
        }
        """
        salida = _interpretar(codigo)
        assert salida.strip().split() == ["0", "1", "2"]


class TestInterpreteListas:
    def test_lista_vacia(self):
        salida = _interpretar("imprimir [];")
        assert salida.strip() == "[]"

    def test_lista_con_elementos(self):
        salida = _interpretar("imprimir [1, 2, 3];")
        assert salida.strip() == "[1, 2, 3]"

    def test_acceso_lista(self):
        salida = _interpretar("var x = [10, 20]; imprimir x[0];")
        assert salida.strip() == "10"

    def test_asignar_lista(self):
        salida = _interpretar("var x = [1, 2, 3]; x[1] = 99; imprimir x;")
        assert salida.strip() == "[1, 99, 3]"

    def test_indice_fuera_rango(self):
        with pytest.raises(ErrorEjecucion, match="fuera de rango"):
            _interpretar_devuelve("var x = [1]; imprimir x[5];")


class TestInterpreteFunciones:
    def test_funcion_sin_retorno(self):
        codigo = """
        funcion saludar() {
            imprimir "hola";
        }
        saludar();
        """
        salida = _interpretar(codigo)
        assert salida.strip() == "hola"

    def test_funcion_con_retorno(self):
        codigo = """
        funcion suma(a, b) {
            retornar a + b;
        }
        imprimir suma(3, 4);
        """
        salida = _interpretar(codigo)
        assert salida.strip() == "7"

    def test_funcion_recursiva(self):
        codigo = """
        funcion factorial(n) {
            si (n <= 1) { retornar 1; }
            retornar n * factorial(n - 1);
        }
        imprimir factorial(5);
        """
        salida = _interpretar(codigo)
        assert salida.strip() == "120"

    def test_argumentos_incorrectos(self):
        codigo = """
        funcion f(a) { }
        f(1, 2);
        """
        with pytest.raises(ErrorEjecucion, match="argumentos"):
            _interpretar_devuelve(codigo)


class TestInterpreteClases:
    def test_clase_sin_metodos(self):
        codigo = """
        clase Vacio { }
        var v = nuevo Vacio();
        imprimir "ok";
        """
        salida = _interpretar(codigo)
        assert salida.strip() == "ok"

    def test_clase_con_metodo(self):
        codigo = """
        clase Saludador {
            funcion saludar() {
                imprimir "hola";
            }
        }
        var s = nuevo Saludador();
        s.saludar();
        """
        salida = _interpretar(codigo)
        assert salida.strip() == "hola"

    def test_clase_con_iniciar(self):
        codigo = """
        clase Persona {
            funcion iniciar(nombre) {
                este.nombre = nombre;
            }
            funcion presentarse() {
                imprimir "soy " + este.nombre;
            }
        }
        var p = nuevo Persona("Ana");
        p.presentarse();
        """
        salida = _interpretar(codigo)
        assert salida.strip() == "soy Ana"

    def test_herencia(self):
        codigo = """
        clase Animal {
            funcion sonido() {
                imprimir "...";
            }
        }
        clase Perro heredar Animal {
            funcion sonido() {
                imprimir "guau";
            }
        }
        var p = nuevo Perro();
        p.sonido();
        """
        salida = _interpretar(codigo)
        assert salida.strip() == "guau"


class TestInterpreteNulo:
    def test_imprimir_nulo(self):
        salida = _interpretar("imprimir nulo;")
        assert salida.strip() == "nulo"

    def test_nulo_es_falso(self):
        codigo = """
        si (nulo) { imprimir "si"; } sino { imprimir "no"; }
        """
        salida = _interpretar(codigo)
        assert salida.strip() == "no"
