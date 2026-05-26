from .ast import (
    Programa, DeclararVar, AsignarVar, AsignarOp,
    DeclararFuncion, Retornar, Si, Mientras, Para, Bloque,
    Imprimir, ExpresionStmt, Binaria, Unaria, Literal,
    Variable, Llamada, GetAttr, SetAttr, DeclararClase,
    Este, Nueva, AccesoLista, AsignarLista, LiteralLista,
    Romper, Continuar,
)
from .tokens import TiposToken


class ErrorEjecucion(Exception):
    def __init__(self, mensaje):
        self.mensaje = mensaje
        super().__init__(f"Error en ejecucion: {mensaje}")


class Retorno(Exception):
    def __init__(self, valor):
        self.valor = valor


class RomperExcepcion(Exception):
    pass


class ContinuarExcepcion(Exception):
    pass


class Entorno:
    def __init__(self, padre=None):
        self.valores = {}
        self.padre = padre

    def definir(self, nombre, valor):
        self.valores[nombre] = valor

    def asignar(self, nombre, valor):
        if nombre in self.valores:
            self.valores[nombre] = valor
            return
        if self.padre is not None:
            self.padre.asignar(nombre, valor)
            return
        raise ErrorEjecucion(f"Variable '{nombre}' no definida")

    def obtener(self, nombre):
        if nombre in self.valores:
            return self.valores[nombre]
        if self.padre is not None:
            return self.padre.obtener(nombre)
        raise ErrorEjecucion(f"Variable '{nombre}' no definida")

    def clonar(self):
        nuevo = Entorno(self.padre)
        nuevo.valores = dict(self.valores)
        return nuevo


class FuncionAxioma:
    def __init__(self, declaracion, entorno, es_inicializador=False):
        self.declaracion = declaracion
        self.entorno = entorno
        self.es_inicializador = es_inicializador

    def aridad(self):
        return len(self.declaracion.parametros)

    def llamar(self, interprete, argumentos):
        entorno = Entorno(self.entorno)
        for i, param in enumerate(self.declaracion.parametros):
            entorno.definir(param, argumentos[i])
        try:
            interprete._ejecutar_bloque(self.declaracion.cuerpo.declaraciones, entorno)
        except Retorno as ret:
            if self.es_inicializador:
                return self.entorno.obtener("este")
            return ret.valor
        if self.es_inicializador:
            return self.entorno.obtener("este")
        return None

    def bindear(self, instancia):
        entorno = Entorno(self.entorno)
        entorno.definir("este", instancia)
        return FuncionAxioma(self.declaracion, entorno)

    def __repr__(self):
        return f"<funcion {self.declaracion.nombre}>"


class ClaseAxioma:
    def __init__(self, nombre, padre, metodos):
        self.nombre = nombre
        self.padre = padre
        self.metodos = metodos

    def encontrar_metodo(self, nombre):
        if nombre in self.metodos:
            return self.metodos[nombre]
        if self.padre is not None:
            return self.padre.encontrar_metodo(nombre)
        return None

    def __repr__(self):
        return f"<clase {self.nombre}>"


class InstanciaAxioma:
    def __init__(self, clase):
        self.clase = clase
        self.propiedades = {}

    def obtener(self, nombre):
        if nombre in self.propiedades:
            return self.propiedades[nombre]
        metodo = self.clase.encontrar_metodo(nombre)
        if metodo is not None:
            return metodo.bindear(self)
        raise ErrorEjecucion(f"Propiedad '{nombre}' no definida en instancia de {self.clase.nombre}")

    def asignar(self, nombre, valor):
        self.propiedades[nombre] = valor

    def __repr__(self):
        return f"<instancia de {self.clase.nombre}>"


class Interprete:
    def __init__(self):
        self.entorno_global = Entorno()
        self.entorno = self.entorno_global
        self._registrar_nativas()

    def _registrar_nativas(self):
        def _len(*args):
            if len(args) != 1:
                raise ErrorEjecucion(f"len() espera 1 argumento, se recibieron {len(args)}")
            val = args[0]
            if isinstance(val, (list, str)):
                return len(val)
            raise ErrorEjecucion(f"len() no soporta el tipo {type(val).__name__}")

        self.entorno_global.definir("len", _len)

    def interpretar(self, nodo):
        if isinstance(nodo, Programa):
            return self._visitar_programa(nodo)
        raise ErrorEjecucion(f"Nodo desconocido: {type(nodo).__name__}")

    def _visitar_programa(self, nodo):
        resultado = None
        for declaracion in nodo.declaraciones:
            resultado = self._ejecutar(declaracion)
        return resultado

    def _ejecutar(self, nodo):
        if isinstance(nodo, DeclararVar):
            return self._visitar_declarar_var(nodo)
        if isinstance(nodo, AsignarVar):
            return self._visitar_asignar_var(nodo)
        if isinstance(nodo, AsignarOp):
            return self._visitar_asignar_op(nodo)
        if isinstance(nodo, DeclararFuncion):
            return self._visitar_declarar_funcion(nodo)
        if isinstance(nodo, DeclararClase):
            return self._visitar_declarar_clase(nodo)
        if isinstance(nodo, Si):
            return self._visitar_si(nodo)
        if isinstance(nodo, Mientras):
            return self._visitar_mientras(nodo)
        if isinstance(nodo, Para):
            return self._visitar_para(nodo)
        if isinstance(nodo, Bloque):
            return self._visitar_bloque(nodo)
        if isinstance(nodo, Retornar):
            return self._visitar_retornar(nodo)
        if isinstance(nodo, Imprimir):
            return self._visitar_imprimir(nodo)
        if isinstance(nodo, ExpresionStmt):
            return self._evaluar(nodo.expresion)
        if isinstance(nodo, Nueva):
            return self._visitar_nueva(nodo)
        if isinstance(nodo, Romper):
            raise RomperExcepcion()
        if isinstance(nodo, Continuar):
            raise ContinuarExcepcion()
        raise ErrorEjecucion(f"No se puede ejecutar: {type(nodo).__name__}")

    def _evaluar(self, nodo):
        if isinstance(nodo, Literal):
            return nodo.valor
        if isinstance(nodo, Variable):
            return self.entorno.obtener(nodo.nombre)
        if isinstance(nodo, Binaria):
            return self._evaluar_binaria(nodo)
        if isinstance(nodo, Unaria):
            return self._evaluar_unaria(nodo)
        if isinstance(nodo, Llamada):
            return self._visitar_llamada(nodo)
        if isinstance(nodo, GetAttr):
            return self._visitar_get_attr(nodo)
        if isinstance(nodo, SetAttr):
            return self._visitar_set_attr(nodo)
        if isinstance(nodo, Este):
            return self._visitar_este(nodo)
        if isinstance(nodo, LiteralLista):
            return [self._evaluar(e) for e in nodo.elementos]
        if isinstance(nodo, AsignarVar):
            return self._visitar_asignar_var(nodo)
        if isinstance(nodo, AsignarOp):
            return self._visitar_asignar_op(nodo)
        if isinstance(nodo, AccesoLista):
            lista = self._evaluar(nodo.lista)
            indice = self._evaluar(nodo.indice)
            if not isinstance(lista, list):
                raise ErrorEjecucion("Solo se puede acceder por indice a listas")
            if not isinstance(indice, int):
                raise ErrorEjecucion("El indice debe ser un numero entero")
            if indice < 0 or indice >= len(lista):
                raise ErrorEjecucion(f"Indice {indice} fuera de rango")
            return lista[indice]
        if isinstance(nodo, Nueva):
            return self._visitar_nueva(nodo)
        if isinstance(nodo, AsignarLista):
            lista = self._evaluar(nodo.lista)
            indice = self._evaluar(nodo.indice)
            valor = self._evaluar(nodo.valor)
            if not isinstance(lista, list):
                raise ErrorEjecucion("Solo se puede asignar por indice a listas")
            if not isinstance(indice, int):
                raise ErrorEjecucion("El indice debe ser un numero entero")
            if indice < 0 or indice >= len(lista):
                raise ErrorEjecucion(f"Indice {indice} fuera de rango")
            lista[indice] = valor
            return valor
        raise ErrorEjecucion(f"No se puede evaluar: {type(nodo).__name__}")

    def _evaluar_binaria(self, nodo):
        izquierda = self._evaluar(nodo.izquierda)
        derecha = self._evaluar(nodo.derecha)
        op = nodo.operador.tipo

        if op == TiposToken.MAS:
            if isinstance(izquierda, (int, float)) and isinstance(derecha, (int, float)):
                return izquierda + derecha
            if isinstance(izquierda, str) or isinstance(derecha, str):
                return self._formatear(izquierda) + self._formatear(derecha)
            raise ErrorEjecucion("Tipos incompatibles para suma")
        if op == TiposToken.MENOS:
            self._chequear_numero(izquierda, derecha)
            return izquierda - derecha
        if op == TiposToken.POR:
            self._chequear_numero(izquierda, derecha)
            return izquierda * derecha
        if op == TiposToken.DIV:
            self._chequear_numero(izquierda, derecha)
            if derecha == 0:
                raise ErrorEjecucion("Division por cero")
            return izquierda / derecha
        if op == TiposToken.MOD:
            self._chequear_numero(izquierda, derecha)
            return izquierda % derecha
        if op == TiposToken.IGUAL:
            return izquierda == derecha
        if op == TiposToken.NO_IGUAL:
            return izquierda != derecha
        if op == TiposToken.MENOR:
            self._chequear_numero(izquierda, derecha)
            return izquierda < derecha
        if op == TiposToken.MAYOR:
            self._chequear_numero(izquierda, derecha)
            return izquierda > derecha
        if op == TiposToken.MENOR_IGUAL:
            self._chequear_numero(izquierda, derecha)
            return izquierda <= derecha
        if op == TiposToken.MAYOR_IGUAL:
            self._chequear_numero(izquierda, derecha)
            return izquierda >= derecha
        if op in (TiposToken.Y,):
            return self._es_verdadero(izquierda) and self._es_verdadero(derecha)
        if op in (TiposToken.O,):
            return self._es_verdadero(izquierda) or self._es_verdadero(derecha)

        raise ErrorEjecucion(f"Operador desconocido: {nodo.operador.tipo}")

    def _evaluar_unaria(self, nodo):
        derecho = self._evaluar(nodo.derecho)
        op = nodo.operador.tipo
        if op == TiposToken.MENOS:
            self._chequear_numero(derecho)
            return -derecho
        if op == TiposToken.NO:
            return not self._es_verdadero(derecho)
        raise ErrorEjecucion(f"Operador unario desconocido: {nodo.operador.tipo}")

    def _chequear_numero(self, *args):
        for arg in args:
            if not isinstance(arg, (int, float)):
                raise ErrorEjecucion(f"Se esperaba un numero, se obtuvo {type(arg).__name__}")

    def _es_verdadero(self, valor):
        if valor is None:
            return False
        if isinstance(valor, bool):
            return valor
        if isinstance(valor, (int, float)):
            return valor != 0
        if isinstance(valor, str):
            return len(valor) > 0
        return True

    def _visitar_declarar_var(self, nodo):
        valor = None
        if nodo.valor is not None:
            valor = self._evaluar(nodo.valor)
        self.entorno.definir(nodo.nombre, valor)

    def _visitar_asignar_var(self, nodo):
        valor = self._evaluar(nodo.valor)
        self.entorno.asignar(nodo.nombre, valor)
        return valor

    def _visitar_asignar_op(self, nodo):
        var_actual = self.entorno.obtener(nodo.nombre)
        self._chequear_numero(var_actual)
        valor = self._evaluar(nodo.valor)
        self._chequear_numero(valor)
        if nodo.operador == "+":
            resultado = var_actual + valor
        elif nodo.operador == "-":
            resultado = var_actual - valor
        elif nodo.operador == "*":
            resultado = var_actual * valor
        elif nodo.operador == "/":
            if valor == 0:
                raise ErrorEjecucion("Division por cero")
            resultado = var_actual / valor
        else:
            raise ErrorEjecucion(f"Operador de asignacion desconocido: {nodo.operador}")
        self.entorno.asignar(nodo.nombre, resultado)
        return resultado

    def _visitar_declarar_funcion(self, nodo):
        funcion = FuncionAxioma(nodo, self.entorno)
        self.entorno.definir(nodo.nombre, funcion)

    def _visitar_declarar_clase(self, nodo):
        padre = None
        if nodo.padre is not None:
            padre = self.entorno.obtener(nodo.padre)
            if not isinstance(padre, ClaseAxioma):
                raise ErrorEjecucion(f"'{nodo.padre}' no es una clase")

        metodos = {}
        for metodo in nodo.metodos:
            funcion = FuncionAxioma(metodo, self.entorno, es_inicializador=metodo.nombre == "iniciar")
            metodos[metodo.nombre] = funcion

        clase = ClaseAxioma(nodo.nombre, padre, metodos)
        self.entorno.definir(nodo.nombre, clase)

    def _visitar_si(self, nodo):
        if self._es_verdadero(self._evaluar(nodo.condicion)):
            self._ejecutar(nodo.entonces)
        elif nodo.sino is not None:
            self._ejecutar(nodo.sino)

    def _visitar_mientras(self, nodo):
        while self._es_verdadero(self._evaluar(nodo.condicion)):
            try:
                self._ejecutar(nodo.cuerpo)
            except RomperExcepcion:
                break
            except ContinuarExcepcion:
                continue

    def _visitar_para(self, nodo):
        entorno_para = Entorno(self.entorno)
        entorno_anterior = self.entorno
        self.entorno = entorno_para

        try:
            if nodo.inicializacion is not None:
                self._ejecutar(nodo.inicializacion)

            while True:
                if nodo.condicion is not None and not self._es_verdadero(self._evaluar(nodo.condicion)):
                    break
                try:
                    self._ejecutar(nodo.cuerpo)
                except RomperExcepcion:
                    break
                except ContinuarExcepcion:
                    pass
                if nodo.incremento is not None:
                    self._evaluar(nodo.incremento)
        finally:
            self.entorno = entorno_anterior

    def _visitar_bloque(self, nodo):
        self._ejecutar_bloque(nodo.declaraciones, Entorno(self.entorno))

    def _ejecutar_bloque(self, declaraciones, entorno):
        anterior = self.entorno
        self.entorno = entorno
        try:
            for declaracion in declaraciones:
                self._ejecutar(declaracion)
        finally:
            self.entorno = anterior

    def _visitar_retornar(self, nodo):
        valor = None
        if nodo.valor is not None:
            valor = self._evaluar(nodo.valor)
        raise Retorno(valor)

    def _visitar_imprimir(self, nodo):
        valor = self._evaluar(nodo.expresion)
        print(self._formatear(valor))

    def _visitar_llamada(self, nodo):
        callee = self._evaluar(nodo.callee)
        argumentos = [self._evaluar(arg) for arg in nodo.argumentos]

        if isinstance(callee, FuncionAxioma):
            if len(argumentos) != callee.aridad():
                raise ErrorEjecucion(f"Se esperaban {callee.aridad()} argumentos, se recibieron {len(argumentos)}")
            return callee.llamar(self, argumentos)

        if isinstance(callee, ClaseAxioma):
            instancia = InstanciaAxioma(callee)
            iniciador = callee.encontrar_metodo("iniciar")
            if iniciador is not None:
                entorno_instancia = Entorno()
                entorno_instancia.definir("este", instancia)
                func_iniciar = FuncionAxioma(iniciador.declaracion, entorno_instancia, es_inicializador=True)
                if len(argumentos) != func_iniciar.aridad():
                    raise ErrorEjecucion(f"Se esperaban {func_iniciar.aridad()} argumentos, se recibieron {len(argumentos)}")
                func_iniciar.llamar(self, argumentos)
            return instancia

        if callable(callee):
            return callee(*argumentos)

        raise ErrorEjecucion(f"No se puede llamar: {type(callee).__name__}")

    def _visitar_get_attr(self, nodo):
        objeto = self._evaluar(nodo.objeto)
        if isinstance(objeto, InstanciaAxioma):
            return objeto.obtener(nodo.nombre)
        if isinstance(objeto, ClaseAxioma):
            metodo = objeto.encontrar_metodo(nodo.nombre)
            if metodo is not None:
                return metodo
            raise ErrorEjecucion(f"La clase {objeto.nombre} no tiene metodo '{nodo.nombre}'")
        raise ErrorEjecucion(f"Solo las instancias tienen propiedades")

    def _visitar_set_attr(self, nodo):
        objeto = self._evaluar(nodo.objeto)
        valor = self._evaluar(nodo.valor)
        if isinstance(objeto, InstanciaAxioma):
            objeto.asignar(nodo.nombre, valor)
            return valor
        raise ErrorEjecucion(f"Solo las instancias pueden tener propiedades")

    def _visitar_este(self, nodo):
        return self.entorno.obtener("este")

    def _visitar_nueva(self, nodo):
        from .ast import LiteralLista
        clase = self.entorno.obtener(nodo.clase)
        if not isinstance(clase, ClaseAxioma):
            raise ErrorEjecucion(f"'{nodo.clase}' no es una clase")
        instancia = InstanciaAxioma(clase)
        iniciador = clase.encontrar_metodo("iniciar")
        if iniciador is not None:
            argumentos = [self._evaluar(arg) for arg in nodo.argumentos]
            entorno_instancia = Entorno()
            entorno_instancia.definir("este", instancia)
            func_iniciar = FuncionAxioma(iniciador.declaracion, entorno_instancia, es_inicializador=True)
            if len(argumentos) != func_iniciar.aridad():
                raise ErrorEjecucion(f"Se esperaban {func_iniciar.aridad()} argumentos, se recibieron {len(argumentos)}")
            func_iniciar.llamar(self, argumentos)
        return instancia

    def _formatear(self, valor):
        if valor is None:
            return "nulo"
        if isinstance(valor, bool):
            return "verdadero" if valor else "falso"
        if isinstance(valor, float):
            if valor == int(valor):
                return str(int(valor))
            return str(valor)
        if isinstance(valor, list):
            return "[" + ", ".join(self._formatear(e) for e in valor) + "]"
        if isinstance(valor, str):
            return valor
        return str(valor)
