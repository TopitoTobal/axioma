# Listas

Las listas permiten almacenar multiples valores en una sola variable.

## Crear Listas

Se crean con corchetes `[ ]` y los elementos separados por comas:

```
var numeros = [1, 2, 3, 4, 5];
var frutas = ["manzana", "pera", "uva"];
var mixto = [1, "hola", verdadero, nulo];
var vacia = [];
```

## Acceder a Elementos

Los elementos se acceden por su indice, comenzando desde 0:

```
var frutas = ["manzana", "pera", "uva"];

imprimir frutas[0];    // manzana
imprimir frutas[1];    // pera
imprimir frutas[2];    // uva
```

## Modificar Elementos

```
var numeros = [10, 20, 30];
numeros[1] = 25;
imprimir numeros;    // [10, 25, 30]
```

## Recorrer Listas

Con `mientras`:

```
var numeros = [1, 2, 3, 4, 5];
var i = 0;
mientras (i < 5) {
    imprimir numeros[i];
    i = i + 1;
}
```

Con `para`:

```
var numeros = [10, 20, 30, 40, 50];
para (var i = 0; i < 5; i = i + 1) {
    imprimir numeros[i];
}
```

## Listas Multitipo

Las listas pueden contener diferentes tipos:

```
var datos = [42, "texto", verdadero, nulo, [1, 2, 3]];
imprimir datos[0];          // 42
imprimir datos[1];          // texto
imprimir datos[4][0];       // 1 (lista dentro de lista)
```
