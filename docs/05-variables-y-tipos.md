# Variables y Tipos de Datos

## Variables

Las variables se declaran con la palabra clave `var`:

```
var nombre = "Ana";
var edad = 25;
var precio = 99.99;
var activo = verdadero;
var datos = nulo;
```

Si no se asigna un valor inicial, la variable vale `nulo`:

```
var x;      // x es nulo
```

### Reasignacion

```
var contador = 0;
contador = 10;         // Ahora vale 10
contador = "texto";    // Puede cambiar de tipo
```

### Asignacion Compuesta

```
var x = 5;
x += 3;    // x = 8   (equivalente a x = x + 3)
x -= 2;    // x = 6
x *= 4;    // x = 24
x /= 6;    // x = 4
```

## Tipos de Datos

Axioma tiene tipado dinamico: una variable puede contener cualquier tipo de dato.

### Numeros

Enteros y flotantes:

```
var entero = 42;
var flotante = 3.1416;
var negativo = -10;
```

Operaciones aritmeticas basicas:

```
var suma = 10 + 5;        // 15
var resta = 10 - 5;       // 5
var multi = 10 * 5;       // 50
var divi = 10 / 3;        // 3.333...
var modulo = 10 % 3;      // 1
```

### Texto (Strings)

Las cadenas de texto se escriben entre comillas dobles:

```
var saludo = "Hola mundo";
var nombre = "Maria";
```

Concatenacion con `+`:

```
var mensaje = "Hola " + "Mundo";     // "Hola Mundo"
var edad = 25;
var texto = "Edad: " + edad;          // "Edad: 25"
```

### Booleanos

```
var esMayor = verdadero;
var esMenor = falso;
```

### Nulo

```
var vacio = nulo;
```

Representa la ausencia de valor.

## Scope (Ambito de Variables)

Las variables declaradas dentro de un bloque `{ }` solo existen dentro de ese bloque:

```
var global = "visible";

si (verdadero) {
    var local = "solo aqui";
    imprimir global;    // OK
    imprimir local;     // OK
}

imprimir global;    // OK
imprimir local;     // Error: variable no definida
```
