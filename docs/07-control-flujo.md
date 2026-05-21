# Control de Flujo

## Condicional: si / sino

### si simple

```
si (condicion) {
    // codigo si la condicion es verdadera
}
```

Ejemplo:

```
var edad = 18;

si (edad >= 18) {
    imprimir "Eres mayor de edad";
}
```

### si / sino

```
si (condicion) {
    // codigo si es verdadera
} sino {
    // codigo si es falsa
}
```

Ejemplo:

```
var temperatura = 30;

si (temperatura > 25) {
    imprimir "Hace calor";
} sino {
    imprimir "Hace fresco";
}
```

### si / sino anidados

```
var nota = 85;

si (nota >= 90) {
    imprimir "Excelente";
} sino si (nota >= 70) {
    imprimir "Bien";
} sino si (nota >= 60) {
    imprimir "Suficiente";
} sino {
    imprimir "Reprobado";
}
```

## Bucle: mientras

Ejecuta un bloque mientras la condicion sea verdadera:

```
mientras (condicion) {
    // codigo a repetir
}
```

Ejemplo — contar del 1 al 5:

```
var i = 1;
mientras (i <= 5) {
    imprimir i;
    i = i + 1;
}
```

Ejemplo — leer elementos de una lista:

```
var frutas = ["manzana", "pera", "uva"];
var i = 0;
mientras (i < 3) {
    imprimir frutas[i];
    i = i + 1;
}
```

## Bucle: para

El bucle `para` tiene tres partes: inicializacion, condicion e incremento.

```
para (inicializacion; condicion; incremento) {
    // codigo a repetir
}
```

Ejemplo — contar del 1 al 5:

```
para (var i = 1; i <= 5; i = i + 1) {
    imprimir i;
}
```

Ejemplo — recorrer una lista:

```
var numeros = [10, 20, 30, 40, 50];
para (var i = 0; i < 5; i = i + 1) {
    imprimir numeros[i];
}
```

Cualquiera de las tres partes puede omitirse:

```
// Solo condicion
var i = 0;
para (; i < 5; ) {
    imprimir i;
    i = i + 1;
}
```

## Valores Truthy y Falsy

En una condicion, los siguientes valores se evaluan como `falso`:

- `falso`
- `nulo`
- `0` (cero)
- `""` (string vacio)

Todo lo demas se evalua como `verdadero`:

```
si (0) {         // falso — no se ejecuta
si ("") {        // falso — no se ejecuta
si (nulo) {      // falso — no se ejecuta
si (1) {         // verdadero — se ejecuta
si ("texto") {   // verdadero — se ejecuta
si ([]) {        // verdadero — se ejecuta
```
