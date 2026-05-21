# Funciones

## Definicion

Las funciones se definen con la palabra clave `funcion`:

```
funcion nombre(parametro1, parametro2) {
    // cuerpo de la funcion
    retornar resultado;
}
```

Ejemplo basico:

```
funcion saludar(nombre) {
    imprimir "Hola " + nombre;
}

saludar("Ana");     // Hola Ana
saludar("Luis");    // Hola Luis
```

## Parametros

Una funcion puede tener cero o mas parametros:

```
funcion mostrarVersion() {
    imprimir "Axioma v1.0";
}

funcion sumar(a, b) {
    retornar a + b;
}

funcion crearUsuario(nombre, edad, activo) {
    imprimir "Usuario: " + nombre;
    imprimir "Edad: " + edad;
    imprimir "Activo: " + activo;
}
```

## Retorno

Usa `retornar` para devolver un valor:

```
funcion cuadrado(n) {
    retornar n * n;
}

var resultado = cuadrado(5);    // resultado = 25
```

Si no se usa `retornar`, la funcion devuelve `nulo`:

```
funcion soloImprimir(mensaje) {
    imprimir mensaje;
    // no hay retornar — devuelve nulo
}
```

## Recursion

Las funciones pueden llamarse a si mismas:

```
funcion factorial(n) {
    si (n <= 1) {
        retornar 1;
    }
    retornar n * factorial(n - 1);
}

imprimir factorial(5);    // 120
```

## Scope en Funciones

Las variables declaradas dentro de una funcion son locales a ella:

```
var global = "accesible desde cualquier lugar";

funcion ejemplo() {
    var local = "solo existe dentro de la funcion";
    imprimir global;    // OK
    imprimir local;     // OK
}

imprimir global;    // OK
imprimir local;     // Error! local no existe fuera
```

## Funciones como Valores

Las funciones se pueden asignar a variables y pasar como argumentos:

```
funcion aplicar(a, b, operacion) {
    retornar operacion(a, b);
}

funcion sumar(x, y) {
    retornar x + y;
}

funcion multiplicar(x, y) {
    retornar x * y;
}

imprimir aplicar(3, 4, sumar);        // 7
imprimir aplicar(3, 4, multiplicar);  // 12
```

## Funcion dentro de Funcion

```
funcion exterior(x) {
    funcion interior(y) {
        retornar y * 2;
    }
    retornar interior(x) + 1;
}

imprimir exterior(5);    // 11
```
