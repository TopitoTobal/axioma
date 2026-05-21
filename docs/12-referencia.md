# Referencia Rapida

## Palabras Clave

| Palabra | Uso |
|---------|-----|
| `var` | `var nombre = valor;` |
| `funcion` | `funcion nombre(params) { ... }` |
| `retornar` | `retornar valor;` |
| `si` | `si (condicion) { ... }` |
| `sino` | `... sino { ... }` |
| `mientras` | `mientras (condicion) { ... }` |
| `para` | `para (init; cond; inc) { ... }` |
| `imprimir` | `imprimir expresion;` |
| `verdadero` | Valor booleano true |
| `falso` | Valor booleano false |
| `nulo` | Valor nulo |
| `y` | AND logico |
| `o` | OR logico |
| `no` | NOT logico |
| `clase` | `clase Nombre { ... }` |
| `este` | Referencia a la instancia actual |
| `nuevo` | `nuevo Clase(args)` |
| `heredar` | `clase Hija heredar Padre { ... }` |

## Operadores

**Aritmeticos:** `+` `-` `*` `/` `%`

**Comparacion:** `==` `!=` `<` `>` `<=` `>=`

**Logicos:** `y` `o` `no`

**Asignacion:** `=` `+=` `-=` `*=` `/=`

## Comentarios

```
// Linea
/* Bloque */
```

## Tipos de Datos

```
var entero = 42;
var flotante = 3.14;
var texto = "Hola";
var booleano = verdadero;
var nulo = nulo;
var lista = [1, 2, 3];
```

## Estructuras de Control

```
// Condicional
si (condicion) {
    ...
} sino {
    ...
}

// Bucle mientras
mientras (condicion) {
    ...
}

// Bucle para
para (var i = 0; i < n; i = i + 1) {
    ...
}
```

## Funciones

```
funcion nombre(param1, param2) {
    retornar valor;
}
```

## Clases

```
clase MiClase {
    funcion iniciar(param) {
        este.prop = param;
    }

    funcion metodo() {
        ...
    }
}

var obj = nuevo MiClase(valor);
```

## Gramatica (EBNF)

```
programa       := declaracion*
declaracion    := varDecl | funcDecl | claseDecl | sentencia

varDecl        := "var" IDENTIFICADOR ("=" expresion)? ";"
funcDecl       := "funcion" IDENTIFICADOR "(" parametros? ")" "{" declaracion* "}"
claseDecl      := "clase" IDENTIFICADOR ("heredar" IDENTIFICADOR)? "{" funcDecl* "}"

parametros     := IDENTIFICADOR ("," IDENTIFICADOR)*

sentencia      := exprStmt | siStmt | mientrasStmt | paraStmt
                 | retornarStmt | imprimirStmt | bloque

exprStmt       := expresion ";"
siStmt         := "si" "(" expresion ")" sentencia ("sino" sentencia)?
mientrasStmt   := "mientras" "(" expresion ")" sentencia
paraStmt       := "para" "(" (varDecl | exprStmt)? ";" expresion? ";"
                  expresion? ")" sentencia
retornarStmt   := "retornar" expresion? ";"
imprimirStmt   := "imprimir" expresion ";"
bloque         := "{" declaracion* "}"

expresion      := asignacion

asignacion     := logicoO (("=" | "+=" | "-=" | "*=" | "/=") asignacion)?
logicoO        := logicoY ("o" logicoY)*
logicoY        := igualdad ("y" igualdad)*
igualdad       := comparacion (("==" | "!=") comparacion)*
comparacion    := termino (("<" | ">" | "<=" | ">=") termino)*
termino        := factor (("+" | "-") factor)*
factor         := unario (("*" | "/" | "%") unario)*
unario         := ("-" | "no") unario | llamada

llamada        := primario (("(" argumentos? ")") | "." IDENTIFICADOR
                  | "[" expresion "]")*
primario       := NUMERO | TEXTO | "verdadero" | "falso" | "nulo"
                  | "este" | "(" expresion ")" | IDENTIFICADOR
                  | "[" listaElementos? "]" | "nuevo" IDENTIFICADOR "(" argumentos? ")"

argumentos     := expresion ("," expresion)*
```
