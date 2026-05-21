# Axioma

Bienvenido a la documentacion oficial de **Axioma**, un lenguaje de programacion de codigo abierto que se programa completamente en espanol.

Axioma esta disenado para que hispanohablantes puedan programar en su idioma nativo, sin necesidad de aprender ingles para entender palabras clave como `if`, `while`, `for` o `function`.

## Caracteristicas

- **Keywords en espanol** — `si`, `sino`, `mientras`, `para`, `funcion`, `imprimir`, `clase`, `y`, `o`, `no`
- **Tipado dinamico** — Variables sin tipo fijo: numeros, texto, booleanos, listas
- **Orientado a objetos** — Clases, herencia, metodos
- **Interpretado** — Sin compilacion, ejecucion directa
- **Codigo abierto** — Licencia MIT

## Ejemplo Rapido

```
funcion fibonacci(n) {
    si (n <= 1) {
        retornar n;
    }
    retornar fibonacci(n - 1) + fibonacci(n - 2);
}

para (var i = 0; i < 10; i = i + 1) {
    imprimir "fib(" + i + ") = " + fibonacci(i);
}
```

## Comenzar

Usa el menu de navegacion para explorar la documentacion completa, o visita estos enlaces rapidos:

- :material-rocket-launch: [Instalacion](02-instalacion.md) — Como instalar Axioma
- :material-code-tags: [Primeros Pasos](03-primeros-pasos.md) — Tu primer programa
- :material-book-open-variant: [Referencia](12-referencia.md) — Resumen de sintaxis
