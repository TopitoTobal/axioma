# Ejemplos Completos

## 1. Hola Mundo

```
imprimir "Hola, mundo!";
```

## 2. Calculadora de IMC

```
funcion calcularIMC(peso, altura) {
    retornar peso / (altura * altura);
}

var peso = 70;
var altura = 1.75;
var imc = calcularIMC(peso, altura);

imprimir "Peso: " + peso + " kg";
imprimir "Altura: " + altura + " m";
imprimir "IMC: " + imc;

si (imc < 18.5) {
    imprimir "Bajo peso";
} sino si (imc < 25) {
    imprimir "Peso normal";
} sino si (imc < 30) {
    imprimir "Sobrepeso";
} sino {
    imprimir "Obesidad";
}
```

## 3. Fibonacci

```
funcion fibonacci(n) {
    si (n <= 1) {
        retornar n;
    }
    retornar fibonacci(n - 1) + fibonacci(n - 2);
}

imprimir "Secuencia de Fibonacci:";
para (var i = 0; i < 10; i = i + 1) {
    imprimir "fib(" + i + ") = " + fibonacci(i);
}
```

## 4. Numeros Primos

```
funcion esPrimo(n) {
    si (n <= 1) {
        retornar falso;
    }

    var i = 2;
    mientras (i * i <= n) {
        si (n % i == 0) {
            retornar falso;
        }
        i = i + 1;
    }
    retornar verdadero;
}

imprimir "Primos del 1 al 50:";
para (var i = 1; i <= 50; i = i + 1) {
    si (esPrimo(i)) {
        imprimir i;
    }
}
```

## 5. Sistema de Biblioteca con Clases

```
clase Libro {
    funcion iniciar(titulo, autor) {
        este.titulo = titulo;
        este.autor = autor;
        este.prestado = falso;
    }

    funcion prestar() {
        si (este.prestado) {
            imprimir "El libro ya esta prestado";
        } sino {
            este.prestado = verdadero;
            imprimir "Libro prestado con exito";
        }
    }

    funcion devolver() {
        este.prestado = falso;
        imprimir "Libro devuelto";
    }

    funcion mostrarInfo() {
        imprimir "Titulo: " + este.titulo;
        imprimir "Autor: " + este.autor;
        si (este.prestado) {
            imprimir "Estado: Prestado";
        } sino {
            imprimir "Estado: Disponible";
        }
    }
}

clase Biblioteca {
    funcion iniciar(nombre) {
        este.nombre = nombre;
        este.libros = [];
        este.cantidad = 0;
    }

    funcion agregarLibro(libro) {
        este.libros[este.cantidad] = libro;
        este.cantidad = este.cantidad + 1;
        imprimir "Libro agregado a la biblioteca";
    }

    funcion listarLibros() {
        imprimir "Biblioteca: " + este.nombre;
        para (var i = 0; i < este.cantidad; i = i + 1) {
            este.libros[i].mostrarInfo();
            imprimir "---";
        }
    }
}

var libro1 = nuevo Libro("Cien anios de soledad", "Gabriel Garcia Marquez");
var libro2 = nuevo Libro("1984", "George Orwell");
var biblio = nuevo Biblioteca("Municipal");

biblio.agregarLibro(libro1);
biblio.agregarLibro(libro2);

libro1.prestar();
libro1.mostrarInfo();
libro1.devolver();

biblio.listarLibros();
```

## 6. Numeros Pares e Impares

```
funcion esPar(n) {
    retornar n % 2 == 0;
}

imprimir "Numeros pares del 1 al 20:";
para (var i = 1; i <= 20; i = i + 1) {
    si (esPar(i)) {
        imprimir i;
    }
}
```

## 7. Tabla de Multiplicar

```
funcion tablaMultiplicar(numero, limite) {
    para (var i = 1; i <= limite; i = i + 1) {
        imprimir numero + " x " + i + " = " + (numero * i);
    }
}

tablaMultiplicar(7, 10);
```

## 8. Conversion de Temperatura

```
funcion celsiusAFahrenheit(celsius) {
    retornar (celsius * 9 / 5) + 32;
}

funcion fahrenheitACelsius(fahrenheit) {
    retornar (fahrenheit - 32) * 5 / 9;
}

imprimir "0 C = " + celsiusAFahrenheit(0) + " F";
imprimir "100 C = " + celsiusAFahrenheit(100) + " F";
imprimir "32 F = " + fahrenheitACelsius(32) + " C";
imprimir "212 F = " + fahrenheitACelsius(212) + " C";
```
