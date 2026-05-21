from .tokens import Token, TiposToken, PALABRAS_CLAVE


class ErrorLexico(Exception):
    def __init__(self, mensaje, linea, columna):
        self.mensaje = mensaje
        self.linea = linea
        self.columna = columna
        super().__init__(f"Error lexico L{linea}:{columna}: {mensaje}")


class Lexer:
    def __init__(self, codigo):
        self.codigo = codigo
        self.inicio = 0
        self.actual = 0
        self.linea = 1
        self.columna = 1
        self.tokens = []

    def escanear(self):
        while self.actual < len(self.codigo):
            self.inicio = self.actual
            self._escanear_token()

        self.tokens.append(Token(TiposToken.EOF, None, self.linea, self.columna))
        return self.tokens

    def _escanear_token(self):
        c = self._avanzar()

        if c in ' \t\r':
            self.columna += 1
            return

        if c == '\n':
            self.linea += 1
            self.columna = 1
            return

        if c == '/':
            if self._coincide('/'):
                while self.actual < len(self.codigo) and self.codigo[self.actual] != '\n':
                    self._avanzar()
            elif self._coincide('*'):
                self._comentario_bloque()
            else:
                self._agregar_token(TiposToken.DIV)
            return

        if c == '+':
            if self._coincide('='):
                self._agregar_token(TiposToken.ASIGNAR_MAS)
            else:
                self._agregar_token(TiposToken.MAS)
            return

        if c == '-':
            if self._coincide('='):
                self._agregar_token(TiposToken.ASIGNAR_MENOS)
            else:
                self._agregar_token(TiposToken.MENOS)
            return

        if c == '*':
            if self._coincide('='):
                self._agregar_token(TiposToken.ASIGNAR_POR)
            else:
                self._agregar_token(TiposToken.POR)
            return

        if c == '%':
            self._agregar_token(TiposToken.MOD)
            return

        if c == '=':
            if self._coincide('='):
                self._agregar_token(TiposToken.IGUAL)
            else:
                self._agregar_token(TiposToken.ASIGNAR)
            return

        if c == '!':
            if self._coincide('='):
                self._agregar_token(TiposToken.NO_IGUAL)
            else:
                raise ErrorLexico(f"Caracter inesperado '{c}'", self.linea, self.columna)
            return

        if c == '<':
            if self._coincide('='):
                self._agregar_token(TiposToken.MENOR_IGUAL)
            else:
                self._agregar_token(TiposToken.MENOR)
            return

        if c == '>':
            if self._coincide('='):
                self._agregar_token(TiposToken.MAYOR_IGUAL)
            else:
                self._agregar_token(TiposToken.MAYOR)
            return

        if c == '(':
            self._agregar_token(TiposToken.PAREN_IZQ)
            return
        if c == ')':
            self._agregar_token(TiposToken.PAREN_DER)
            return
        if c == '{':
            self._agregar_token(TiposToken.LLAVE_IZQ)
            return
        if c == '}':
            self._agregar_token(TiposToken.LLAVE_DER)
            return
        if c == '[':
            self._agregar_token(TiposToken.CORCH_IZQ)
            return
        if c == ']':
            self._agregar_token(TiposToken.CORCH_DER)
            return
        if c == ',':
            self._agregar_token(TiposToken.COMA)
            return
        if c == '.':
            self._agregar_token(TiposToken.PUNTO)
            return
        if c == ';':
            self._agregar_token(TiposToken.PUNTO_COMA)
            return
        if c == ':':
            self._agregar_token(TiposToken.DOS_PUNTOS)
            return

        if c == '"':
            self._texto()
            return

        if c.isdigit():
            self._numero()
            return

        if c.isalpha() or c == '_':
            self._identificador()
            return

        raise ErrorLexico(f"Caracter inesperado '{c}'", self.linea, self.columna)

    def _comentario_bloque(self):
        while self.actual < len(self.codigo):
            c = self._avanzar()
            if c == '\n':
                self.linea += 1
                self.columna = 1
            elif c == '*' and self.actual < len(self.codigo) and self.codigo[self.actual] == '/':
                self._avanzar()
                return
        raise ErrorLexico("Comentario de bloque sin cerrar", self.linea, self.columna)

    def _texto(self):
        while self.actual < len(self.codigo) and self.codigo[self.actual] != '"':
            if self.codigo[self.actual] == '\n':
                self.linea += 1
                self.columna = 1
            self._avanzar()

        if self.actual >= len(self.codigo):
            raise ErrorLexico("Texto sin cerrar", self.linea, self.columna)

        self._avanzar()
        valor = self.codigo[self.inicio + 1:self.actual - 1]
        self._agregar_token(TiposToken.TEXTO, valor)

    def _numero(self):
        while self.actual < len(self.codigo) and self.codigo[self.actual].isdigit():
            self._avanzar()

        if self.actual < len(self.codigo) and self.codigo[self.actual] == '.':
            self._avanzar()
            while self.actual < len(self.codigo) and self.codigo[self.actual].isdigit():
                self._avanzar()
            valor = float(self.codigo[self.inicio:self.actual])
        else:
            valor = int(self.codigo[self.inicio:self.actual])

        self._agregar_token(TiposToken.NUMERO, valor)

    def _identificador(self):
        while self.actual < len(self.codigo) and (self.codigo[self.actual].isalnum() or self.codigo[self.actual] == '_'):
            self._avanzar()

        texto = self.codigo[self.inicio:self.actual]
        tipo = PALABRAS_CLAVE.get(texto, TiposToken.IDENTIFICADOR)
        self._agregar_token(tipo, texto if tipo == TiposToken.IDENTIFICADOR else None)

    def _avanzar(self):
        self.columna += 1
        c = self.codigo[self.actual]
        self.actual += 1
        return c

    def _coincide(self, esperado):
        if self.actual >= len(self.codigo):
            return False
        if self.codigo[self.actual] != esperado:
            return False
        self._avanzar()
        return True

    def _agregar_token(self, tipo, valor=None):
        if valor is None:
            valor = self.codigo[self.inicio:self.actual]
        self.tokens.append(Token(tipo, valor, self.linea, self.columna))
