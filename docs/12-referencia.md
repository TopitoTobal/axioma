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

## Metodos de Texto

| Metodo | Uso | Descripcion |
|--------|-----|-------------|
| `mayusculas()` | `texto.mayusculas()` | Convierte el texto a mayusculas |
| `minusculas()` | `texto.minusculas()` | Convierte el texto a minusculas |
| `recortar()` | `texto.recortar()` | Elimina espacios en blanco al inicio y al final |
| `dividir()` | `texto.dividir()` | Divide el texto por espacios en blanco y devuelve una lista |
| `dividir(separador)` | `texto.dividir(",")` | Divide el texto usando el separador indicado y devuelve una lista |

Estos metodos devuelven un nuevo resultado sin modificar el texto original.

```
// Conversion y recorte
var texto = "  Hola Axioma  ";

imprimir texto.mayusculas(); // "  HOLA AXIOMA  "
imprimir texto.minusculas(); // "  hola axioma  "
imprimir texto.recortar();   // "Hola Axioma"

// Encadenamiento
imprimir texto.recortar().mayusculas(); // "HOLA AXIOMA"

// Division por espacios en blanco
imprimir "uno dos tres".dividir(); // [uno, dos, tres]

// Division con un separador
imprimir "uno,dos,tres".dividir(","); // [uno, dos, tres]

// El texto original conserva su contenido
imprimir texto; // "  Hola Axioma  "
```

`mayusculas()`, `minusculas()` y `recortar()` no reciben argumentos.
`dividir()` recibe cero o un argumento. Si se indica un separador,
debe ser un texto no vacio.

Cuando se usa `dividir()` sin argumentos, los espacios en blanco
consecutivos se consideran un solo separador y no se generan elementos
vacios en los extremos.

```
// Espacios consecutivos
imprimir "  uno   dos  ".dividir(); // [uno, dos]

// Un separador explicito conserva los elementos vacios
imprimir "uno,,tres".dividir(","); // [uno, , tres]
```

Las llamadas con una cantidad incorrecta de argumentos, un separador
invalido o un metodo desconocido producen un error de ejecucion.

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
