from .tokens import TiposToken
from .ast import (
    Programa, DeclararVar, AsignarVar, AsignarOp,
    DeclararFuncion, Retornar, Si, Mientras, Para, Bloque,
    Imprimir, ExpresionStmt, Binaria, Unaria, Literal,
    Variable, Llamada, GetAttr, SetAttr, DeclararClase,
    Este, Nueva, AccesoLista, AsignarLista, LiteralLista,
)


class ErrorSintaxis(Exception):
    def __init__(self, mensaje, token):
        self.mensaje = mensaje
        self.token = token
        super().__init__(f"Error sintactico L{token.linea}:{token.columna}: {mensaje}")


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.actual = 0

    def parse(self):
        declaraciones = []
        while not self._fin():
            declaraciones.append(self._declaracion())
        return Programa(declaraciones)

    def _declaracion(self):
        if self._coincide(TiposToken.VAR):
            return self._declarar_var()
        if self._coincide(TiposToken.FUNCION):
            return self._declarar_funcion()
        if self._coincide(TiposToken.CLASE):
            return self._declarar_clase()
        return self._sentencia()

    def _declarar_var(self):
        nombre = self._consumir(TiposToken.IDENTIFICADOR, "Se esperaba nombre de variable despues de 'var'")
        valor = None
        if self._coincide(TiposToken.ASIGNAR):
            valor = self._expresion()
        self._consumir(TiposToken.PUNTO_COMA, "Se esperaba ';' despues de la declaracion de variable")
        return DeclararVar(nombre.valor, valor)

    def _declarar_funcion(self):
        nombre = self._consumir(TiposToken.IDENTIFICADOR, "Se esperaba nombre de funcion")
        self._consumir(TiposToken.PAREN_IZQ, "Se esperaba '(' despues del nombre de funcion")
        parametros = []
        if self._coincide(TiposToken.PAREN_DER):
            pass
        else:
            parametros.append(self._consumir(TiposToken.IDENTIFICADOR, "Se esperaba nombre de parametro").valor)
            while self._coincide(TiposToken.COMA):
                parametros.append(self._consumir(TiposToken.IDENTIFICADOR, "Se esperaba nombre de parametro").valor)
            self._consumir(TiposToken.PAREN_DER, "Se esperaba ')' despues de parametros")
        self._consumir(TiposToken.LLAVE_IZQ, "Se esperaba '{' antes del cuerpo de la funcion")
        cuerpo = self._bloque()
        return DeclararFuncion(nombre.valor, parametros, cuerpo)

    def _declarar_clase(self):
        nombre = self._consumir(TiposToken.IDENTIFICADOR, "Se esperaba nombre de clase").valor
        padre = None
        if self._coincide(TiposToken.HEREDAR):
            padre = self._consumir(TiposToken.IDENTIFICADOR, "Se esperaba nombre de la clase padre").valor
        self._consumir(TiposToken.LLAVE_IZQ, "Se esperaba '{' antes del cuerpo de la clase")
        metodos = []
        while not self._coincide(TiposToken.LLAVE_DER) and not self._fin():
            self._consumir(TiposToken.FUNCION, "Se esperaba 'funcion' dentro de la clase")
            metodos.append(self._declarar_funcion())
        return DeclararClase(nombre, padre, metodos)

    def _sentencia(self):
        if self._coincide(TiposToken.SI):
            return self._sentencia_si()
        if self._coincide(TiposToken.MIENTRAS):
            return self._sentencia_mientras()
        if self._coincide(TiposToken.PARA):
            return self._sentencia_para()
        if self._coincide(TiposToken.RETORNAR):
            return self._sentencia_retornar()
        if self._coincide(TiposToken.IMPRIMIR):
            return self._sentencia_imprimir()
        if self._coincide(TiposToken.LLAVE_IZQ):
            return self._bloque()
        return self._sentencia_expresion()

    def _sentencia_si(self):
        self._consumir(TiposToken.PAREN_IZQ, "Se esperaba '(' despues de 'si'")
        condicion = self._expresion()
        self._consumir(TiposToken.PAREN_DER, "Se esperaba ')' despues de la condicion")
        entonces = self._sentencia()
        sino = None
        if self._coincide(TiposToken.SINO):
            sino = self._sentencia()
        return Si(condicion, entonces, sino)

    def _sentencia_mientras(self):
        self._consumir(TiposToken.PAREN_IZQ, "Se esperaba '(' despues de 'mientras'")
        condicion = self._expresion()
        self._consumir(TiposToken.PAREN_DER, "Se esperaba ')' despues de la condicion")
        cuerpo = self._sentencia()
        return Mientras(condicion, cuerpo)

    def _sentencia_para(self):
        self._consumir(TiposToken.PAREN_IZQ, "Se esperaba '(' despues de 'para'")

        inicializacion = None
        if not self._coincide(TiposToken.PUNTO_COMA):
            if self._coincide(TiposToken.VAR):
                nombre = self._consumir(TiposToken.IDENTIFICADOR, "Se esperaba nombre de variable")
                valor = None
                if self._coincide(TiposToken.ASIGNAR):
                    valor = self._expresion()
                inicializacion = DeclararVar(nombre.valor, valor)
            else:
                inicializacion = self._sentencia_expresion()
        self._consumir(TiposToken.PUNTO_COMA, "Se esperaba ';' en la inicializacion del 'para'")

        condicion = None
        if not self._coincide(TiposToken.PUNTO_COMA):
            condicion = self._expresion()
        self._consumir(TiposToken.PUNTO_COMA, "Se esperaba ';' en la condicion del 'para'")

        incremento = None
        if not self._coincide(TiposToken.PAREN_DER):
            incremento = self._expresion()
        self._consumir(TiposToken.PAREN_DER, "Se esperaba ')' despues del 'para'")

        cuerpo = self._sentencia()
        return Para(inicializacion, condicion, incremento, cuerpo)

    def _sentencia_retornar(self):
        valor = None
        if not self._coincide(TiposToken.PUNTO_COMA):
            valor = self._expresion()
        self._consumir(TiposToken.PUNTO_COMA, "Se esperaba ';' despues de 'retornar'")
        return Retornar(valor)

    def _sentencia_imprimir(self):
        valor = self._expresion()
        self._consumir(TiposToken.PUNTO_COMA, "Se esperaba ';' despues de 'imprimir'")
        return Imprimir(valor)

    def _sentencia_expresion(self):
        expr = self._expresion()
        self._consumir(TiposToken.PUNTO_COMA, "Se esperaba ';' despues de la expresion")
        return ExpresionStmt(expr)

    def _bloque(self):
        declaraciones = []
        while not self._coincide(TiposToken.LLAVE_DER) and not self._fin():
            declaraciones.append(self._declaracion())
        return Bloque(declaraciones)

    def _expresion(self):
        return self._asignacion()

    def _asignacion(self):
        expr = self._logico_o()

        if self._coincide(TiposToken.ASIGNAR):
            valor = self._asignacion()
            if isinstance(expr, Variable):
                return AsignarVar(expr.nombre, valor)
            elif isinstance(expr, GetAttr):
                return SetAttr(expr.objeto, expr.nombre, valor)
            elif isinstance(expr, AccesoLista):
                return AsignarLista(expr.lista, expr.indice, valor)
            raise ErrorSintaxis("Destino de asignacion invalido", self._anterior())

        if self._coincide(TiposToken.ASIGNAR_MAS):
            valor = self._asignacion()
            if isinstance(expr, Variable):
                return AsignarOp(expr.nombre, "+", valor)
            raise ErrorSintaxis("Destino de asignacion invalido", self._anterior())

        if self._coincide(TiposToken.ASIGNAR_MENOS):
            valor = self._asignacion()
            if isinstance(expr, Variable):
                return AsignarOp(expr.nombre, "-", valor)
            raise ErrorSintaxis("Destino de asignacion invalido", self._anterior())

        if self._coincide(TiposToken.ASIGNAR_POR):
            valor = self._asignacion()
            if isinstance(expr, Variable):
                return AsignarOp(expr.nombre, "*", valor)
            raise ErrorSintaxis("Destino de asignacion invalido", self._anterior())

        if self._coincide(TiposToken.ASIGNAR_DIV):
            valor = self._asignacion()
            if isinstance(expr, Variable):
                return AsignarOp(expr.nombre, "/", valor)
            raise ErrorSintaxis("Destino de asignacion invalido", self._anterior())

        return expr

    def _logico_o(self):
        expr = self._logico_y()
        while self._coincide(TiposToken.O):
            operador = self._anterior()
            derecha = self._logico_y()
            expr = Binaria(expr, operador, derecha)
        return expr

    def _logico_y(self):
        expr = self._igualdad()
        while self._coincide(TiposToken.Y):
            operador = self._anterior()
            derecha = self._igualdad()
            expr = Binaria(expr, operador, derecha)
        return expr

    def _igualdad(self):
        expr = self._comparacion()
        while self._coincide(TiposToken.IGUAL, TiposToken.NO_IGUAL):
            operador = self._anterior()
            derecha = self._comparacion()
            expr = Binaria(expr, operador, derecha)
        return expr

    def _comparacion(self):
        expr = self._termino()
        while self._coincide(TiposToken.MENOR, TiposToken.MAYOR, TiposToken.MENOR_IGUAL, TiposToken.MAYOR_IGUAL):
            operador = self._anterior()
            derecha = self._termino()
            expr = Binaria(expr, operador, derecha)
        return expr

    def _termino(self):
        expr = self._factor()
        while self._coincide(TiposToken.MAS, TiposToken.MENOS):
            operador = self._anterior()
            derecha = self._factor()
            expr = Binaria(expr, operador, derecha)
        return expr

    def _factor(self):
        expr = self._unario()
        while self._coincide(TiposToken.POR, TiposToken.DIV, TiposToken.MOD):
            operador = self._anterior()
            derecha = self._unario()
            expr = Binaria(expr, operador, derecha)
        return expr

    def _unario(self):
        if self._coincide(TiposToken.MENOS):
            operador = self._anterior()
            derecho = self._unario()
            return Unaria(operador, derecho)
        if self._coincide(TiposToken.NO):
            operador = self._anterior()
            derecho = self._unario()
            return Unaria(operador, derecho)
        return self._llamada()

    def _llamada(self):
        expr = self._primario()
        while True:
            if self._coincide(TiposToken.PAREN_IZQ):
                argumentos = []
                if not self._coincide(TiposToken.PAREN_DER):
                    argumentos.append(self._expresion())
                    while self._coincide(TiposToken.COMA):
                        argumentos.append(self._expresion())
                    self._consumir(TiposToken.PAREN_DER, "Se esperaba ')' despues de argumentos")
                expr = Llamada(expr, argumentos)
            elif self._coincide(TiposToken.PUNTO):
                nombre = self._consumir(TiposToken.IDENTIFICADOR, "Se esperaba nombre de propiedad despues de '.'")
                expr = GetAttr(expr, nombre.valor)
            elif self._coincide(TiposToken.CORCH_IZQ):
                indice = self._expresion()
                self._consumir(TiposToken.CORCH_DER, "Se esperaba ']' despues del indice")
                expr = AccesoLista(expr, indice)
            else:
                break
        return expr

    def _primario(self):
        if self._coincide(TiposToken.FALSO):
            return Literal(False)
        if self._coincide(TiposToken.VERDADERO):
            return Literal(True)
        if self._coincide(TiposToken.NULO):
            return Literal(None)
        if self._coincide(TiposToken.ESTE):
            return Este()
        if self._coincide(TiposToken.NUMERO, TiposToken.TEXTO):
            return Literal(self._anterior().valor)
        if self._coincide(TiposToken.IDENTIFICADOR):
            return Variable(self._anterior().valor)
        if self._coincide(TiposToken.PAREN_IZQ):
            expr = self._expresion()
            self._consumir(TiposToken.PAREN_DER, "Se esperaba ')' despues de la expresion")
            return expr
        if self._coincide(TiposToken.CORCH_IZQ):
            elementos = []
            if not self._coincide(TiposToken.CORCH_DER):
                elementos.append(self._expresion())
                while self._coincide(TiposToken.COMA):
                    elementos.append(self._expresion())
                self._consumir(TiposToken.CORCH_DER, "Se esperaba ']' para cerrar la lista")
            return LiteralLista(elementos)
        if self._coincide(TiposToken.NUEVO):
            nombre = self._consumir(TiposToken.IDENTIFICADOR, "Se esperaba nombre de clase despues de 'nuevo'")
            self._consumir(TiposToken.PAREN_IZQ, "Se esperaba '(' despues del nombre de clase")
            argumentos = []
            if not self._coincide(TiposToken.PAREN_DER):
                argumentos.append(self._expresion())
                while self._coincide(TiposToken.COMA):
                    argumentos.append(self._expresion())
                self._consumir(TiposToken.PAREN_DER, "Se esperaba ')' despues de argumentos")
            return Nueva(nombre.valor, argumentos)

        raise ErrorSintaxis("Expresion inesperada", self._ver_actual())

    def _coincide(self, *tipos):
        for tipo in tipos:
            if not self._fin() and self._ver_actual().tipo == tipo:
                self._avanzar()
                return True
        return False

    def _consumir(self, tipo, mensaje):
        if self._fin() or self._ver_actual().tipo != tipo:
            raise ErrorSintaxis(mensaje, self._ver_actual())
        return self._avanzar()

    def _avanzar(self):
        token = self.tokens[self.actual]
        self.actual += 1
        return token

    def _anterior(self):
        return self.tokens[self.actual - 1]

    def _ver_actual(self):
        return self.tokens[self.actual]

    def _fin(self):
        return self._ver_actual().tipo == TiposToken.EOF
