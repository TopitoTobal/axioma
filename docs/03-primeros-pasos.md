# Primeros Pasos

## Hola Mundo

Crea un archivo llamado `hola.ax` con el siguiente contenido:

```
imprimir "Hola, mundo desde Axioma!";
```

Ejecutalo:

```bash
axioma hola.ax
```

Salida:
```
Hola, mundo desde Axioma!
```

## Modo Interactivo (REPL)

Ejecuta `axioma` sin argumentos para entrar al modo interactivo:

```bash
> axioma
```

Veras el logo seguido del prompt `>>>`. Puedes escribir codigo directamente:

```bash
>>> imprimir "Hola!";
Hola!
>>> 2 + 3
5
>>> var nombre = "Ana";
>>> imprimir "Hola " + nombre;
Hola Ana
>>> salir()
```

Escribe `salir()` para terminar.

## Estructura de un Programa

Un programa en Axioma se compone de una secuencia de declaraciones y sentencias. Cada sentencia termina con punto y coma (`;`).

```
// Esto es un comentario

var mensaje = "Hola";      // Declaracion de variable

imprimir mensaje;           // Llamada a funcion

funcion sumar(a, b) {       // Definicion de funcion
    retornar a + b;
}

imprimir sumar(3, 4);       // Llamada a funcion
```

## Extension de Archivo

Los archivos de Axioma usan la extension `.ax`.
