class Token:
    def __init__(self, tipo, valor, linea, columna):
        self.tipo = tipo
        self.valor = valor
        self.linea = linea
        self.columna = columna

    def __repr__(self):
        return f"Token({self.tipo}, {self.valor!r}, L{self.linea}:{self.columna})"


class TiposToken:
    NUMERO = "NUMERO"
    TEXTO = "TEXTO"
    IDENTIFICADOR = "IDENTIFICADOR"

    MAS = "MAS"
    MENOS = "MENOS"
    POR = "POR"
    DIV = "DIV"
    MOD = "MOD"

    IGUAL = "IGUAL"
    NO_IGUAL = "NO_IGUAL"
    MENOR = "MENOR"
    MAYOR = "MAYOR"
    MENOR_IGUAL = "MENOR_IGUAL"
    MAYOR_IGUAL = "MAYOR_IGUAL"

    ASIGNAR = "ASIGNAR"
    ASIGNAR_MAS = "ASIGNAR_MAS"
    ASIGNAR_MENOS = "ASIGNAR_MENOS"
    ASIGNAR_POR = "ASIGNAR_POR"
    ASIGNAR_DIV = "ASIGNAR_DIV"

    PAREN_IZQ = "PAREN_IZQ"
    PAREN_DER = "PAREN_DER"
    LLAVE_IZQ = "LLAVE_IZQ"
    LLAVE_DER = "LLAVE_DER"
    CORCH_IZQ = "CORCH_IZQ"
    CORCH_DER = "CORCH_DER"

    COMA = "COMA"
    PUNTO = "PUNTO"
    PUNTO_COMA = "PUNTO_COMA"
    DOS_PUNTOS = "DOS_PUNTOS"

    VAR = "VAR"
    FUNCION = "FUNCION"
    RETORNAR = "RETORNAR"
    SI = "SI"
    SINO = "SINO"
    MIENTRAS = "MIENTRAS"
    PARA = "PARA"
    IMPRIMIR = "IMPRIMIR"
    VERDADERO = "VERDADERO"
    FALSO = "FALSO"
    NULO = "NULO"
    Y = "Y"
    O = "O"
    NO = "NO"
    CLASE = "CLASE"
    ESTE = "ESTE"
    NUEVO = "NUEVO"
    HEREDAR = "HEREDAR"
    ROMPER = "ROMPER"
    CONTINUAR = "CONTINUAR"

    EOF = "EOF"


PALABRAS_CLAVE = {
    "var": TiposToken.VAR,
    "funcion": TiposToken.FUNCION,
    "retornar": TiposToken.RETORNAR,
    "si": TiposToken.SI,
    "sino": TiposToken.SINO,
    "mientras": TiposToken.MIENTRAS,
    "para": TiposToken.PARA,
    "imprimir": TiposToken.IMPRIMIR,
    "verdadero": TiposToken.VERDADERO,
    "falso": TiposToken.FALSO,
    "nulo": TiposToken.NULO,
    "y": TiposToken.Y,
    "o": TiposToken.O,
    "no": TiposToken.NO,
    "clase": TiposToken.CLASE,
    "este": TiposToken.ESTE,
    "nuevo": TiposToken.NUEVO,
    "heredar": TiposToken.HEREDAR,
    "romper": TiposToken.ROMPER,
    "continuar": TiposToken.CONTINUAR,
}
