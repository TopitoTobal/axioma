# Clases y Programacion Orientada a Objetos

## Definir una Clase

Las clases se definen con `clase` y contienen metodos (funciones):

```
clase NombreClase {
    funcion iniciar(parametros) {
        // constructor — se llama al crear instancias
    }

    funcion metodo() {
        // codigo del metodo
    }
}
```

## El Constructor `iniciar`

El metodo `iniciar` es el constructor. Se ejecuta automaticamente al crear una instancia con `nuevo`:

```
clase Persona {
    funcion iniciar(nombre, edad) {
        este.nombre = nombre;
        este.edad = edad;
    }
}
```

## La Palabra `este`

`este` hace referencia a la instancia actual. Se usa para acceder a propiedades y metodos del objeto:

```
clase Persona {
    funcion iniciar(nombre) {
        este.nombre = nombre;
    }

    funcion saludar() {
        imprimir "Hola, soy " + este.nombre;
    }
}
```

## Crear Instancias

Usa `nuevo` para crear una instancia de una clase:

```
var persona1 = nuevo Persona("Ana", 30);
var persona2 = nuevo Persona("Luis", 25);
```

## Llamar Metodos

```
persona1.saludar();    // Hola, soy Ana
persona2.saludar();    // Hola, soy Luis
```

## Propiedades

Las propiedades se asignan con `este.propiedad = valor` y se leen igual:

```
clase Producto {
    funcion iniciar(nombre, precio) {
        este.nombre = nombre;
        este.precio = precio;
        este.stock = 0;
    }

    funcion mostrarInfo() {
        imprimir este.nombre + " - $" + este.precio;
    }
}
```

Las propiedades tambien pueden asignarse desde fuera:

```
var p = nuevo Producto("Laptop", 999);
p.descuento = 10;    // nueva propiedad externa
```

## Herencia con `heredar`

Una clase puede heredar de otra usando `heredar`:

```
clase Animal {
    funcion iniciar(nombre) {
        este.nombre = nombre;
    }

    funcion hacerSonido() {
        imprimir "...";
    }
}

clase Perro heredar Animal {
    funcion hacerSonido() {
        imprimir "Guau!";
    }

    function moverCola() {
        imprimir "*mueve la cola*";
    }
}
```

### Llamar Metodos Heredados

Si un metodo no se encuentra en la clase hija, se busca en la clase padre:

```
var perro = nuevo Perro("Rex");
perro.hacerSonido();    // Guau! (sobrescribe)
perro.nombre;           // "Rex" (heredado del constructor)
```

## Ejemplo Completo

```
clase Figura {
    funcion iniciar(nombre) {
        este.nombre = nombre;
    }

    funcion area() {
        retornar 0;
    }

    funcion describir() {
        imprimir "Soy un " + este.nombre + " con area " + este.area();
    }
}

clase Circulo heredar Figura {
    funcion iniciar(radio) {
        este.nombre = "Circulo";
        este.radio = radio;
    }

    funcion area() {
        retornar 3.1416 * este.radio * este.radio;
    }
}

clase Rectangulo heredar Figura {
    funcion iniciar(base, altura) {
        este.nombre = "Rectangulo";
        este.base = base;
        este.altura = altura;
    }

    funcion area() {
        retornar este.base * este.altura;
    }
}

var circulo = nuevo Circulo(5);
var rect = nuevo Rectangulo(4, 6);

circulo.describir();    // Soy un Circulo con area 78.54
rect.describir();       // Soy un Rectangulo con area 24
```
