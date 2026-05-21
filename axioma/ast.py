class Nodo:
    def __repr__(self):
        return f"{type(self).__name__}({', '.join(f'{k}={v!r}' for k, v in self.__dict__.items())})"


class Programa(Nodo):
    def __init__(self, declaraciones):
        self.declaraciones = declaraciones


class AsignarVar(Nodo):
    def __init__(self, nombre, valor):
        self.nombre = nombre
        self.valor = valor


class DeclararVar(Nodo):
    def __init__(self, nombre, valor=None):
        self.nombre = nombre
        self.valor = valor


class DeclararFuncion(Nodo):
    def __init__(self, nombre, parametros, cuerpo):
        self.nombre = nombre
        self.parametros = parametros
        self.cuerpo = cuerpo


class Retornar(Nodo):
    def __init__(self, valor=None):
        self.valor = valor


class Si(Nodo):
    def __init__(self, condicion, entonces, sino=None):
        self.condicion = condicion
        self.entonces = entonces
        self.sino = sino


class Mientras(Nodo):
    def __init__(self, condicion, cuerpo):
        self.condicion = condicion
        self.cuerpo = cuerpo


class Para(Nodo):
    def __init__(self, inicializacion, condicion, incremento, cuerpo):
        self.inicializacion = inicializacion
        self.condicion = condicion
        self.incremento = incremento
        self.cuerpo = cuerpo


class Bloque(Nodo):
    def __init__(self, declaraciones):
        self.declaraciones = declaraciones


class Imprimir(Nodo):
    def __init__(self, expresion):
        self.expresion = expresion


class ExpresionStmt(Nodo):
    def __init__(self, expresion):
        self.expresion = expresion


class Binaria(Nodo):
    def __init__(self, izquierda, operador, derecha):
        self.izquierda = izquierda
        self.operador = operador
        self.derecha = derecha


class Unaria(Nodo):
    def __init__(self, operador, derecho):
        self.operador = operador
        self.derecho = derecho


class Literal(Nodo):
    def __init__(self, valor):
        self.valor = valor


class Variable(Nodo):
    def __init__(self, nombre):
        self.nombre = nombre


class Llamada(Nodo):
    def __init__(self, callee, argumentos):
        self.callee = callee
        self.argumentos = argumentos


class GetAttr(Nodo):
    def __init__(self, objeto, nombre):
        self.objeto = objeto
        self.nombre = nombre


class SetAttr(Nodo):
    def __init__(self, objeto, nombre, valor):
        self.objeto = objeto
        self.nombre = nombre
        self.valor = valor


class DeclararClase(Nodo):
    def __init__(self, nombre, padre, metodos):
        self.nombre = nombre
        self.padre = padre
        self.metodos = metodos


class Este(Nodo):
    pass


class Nueva(Nodo):
    def __init__(self, clase, argumentos):
        self.clase = clase
        self.argumentos = argumentos


class AsignarOp(Nodo):
    def __init__(self, nombre, operador, valor):
        self.nombre = nombre
        self.operador = operador
        self.valor = valor


class AccesoLista(Nodo):
    def __init__(self, lista, indice):
        self.lista = lista
        self.indice = indice


class AsignarLista(Nodo):
    def __init__(self, lista, indice, valor):
        self.lista = lista
        self.indice = indice
        self.valor = valor


class LiteralLista(Nodo):
    def __init__(self, elementos):
        self.elementos = elementos
