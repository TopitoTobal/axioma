# Sintaxis General

## Comentarios

Axioma soporta dos tipos de comentarios:

```
// Comentario de una linea

/*
   Comentario
   de varias
   lineas
*/
```

## Punto y Coma

Todas las sentencias deben terminar con punto y coma (`;`).

```
var x = 5;
imprimir x;
```

## Bloques

Los bloques de codigo se delimitan con llaves `{ }`.

```
si (condicion) {
    imprimir "Dentro del bloque";
}
```

## Identificadores

Los nombres de variables y funciones pueden contener:

- Letras (incluyendo acentos y enie)
- Numeros (no al inicio)
- Guion bajo (`_`)

Ejemplos validos:

```
var nombre = "Ana";
var _contador = 0;
var edad123 = 25;
var anio = 2026;
var cancion = "Sol";     // Con acento
var muneco = "nino";     // Con enie
```

## Palabras Reservadas

Estas palabras no pueden usarse como identificadores:

```
var        funcion    retornar
si         sino
mientras   para
imprimir
verdadero  falso      nulo
y          o          no
clase      este       nuevo      heredar
```

## Convenciones de Estilo

- **Variables**: usar camelCase (`miVariable`) o snake_case (`mi_variable`)
- **Funciones**: usar camelCase (`calcularTotal`)
- **Clases**: usar PascalCase (`MiClase`)
- **Constantes**: escribir en MAYUSCULAS (`PI`, `LIMITE_MAXIMO`)
