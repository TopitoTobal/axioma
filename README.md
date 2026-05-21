# Axioma

Lenguaje de programación en español, open source.

## Características

- **Keywords en español**: `si`, `sino`, `mientras`, `para`, `funcion`, `var`, `retornar`, `imprimir`, `verdadero`, `falso`, `nulo`, `y`, `o`, `no`, `clase`, `este`, `nuevo`, `heredar`
- **Tipos**: números (enteros y flotantes), strings, booleanos, null, listas
- **Control de flujo**: `si/sino`, `mientras`, `para`
- **Funciones**: soporte para recursividad
- **Clases**: herencia simple, métodos, `este`
- **Operadores**: aritméticos, comparación, lógicos, asignación compuesta

## Instalación

### Opción 1: Ejecutable (recomendado)

Descarga `axioma.exe` desde la sección de releases o compílalo tú mismo:

```bash
pip install pyinstaller
pyinstaller --onefile --name=axioma --distpath=dist --clean --noconfirm --console run.py
```

Agrega `dist/` a tu PATH.

### Extension de VS Code

Extension oficial para Visual Studio Code con resaltado de sintaxis, snippets y configuracion del lenguaje.

```bash
# Desde la carpeta vscode-extension/
cd vscode-extension

# Instalar vsce (una vez)
npm install -g @vscode/vsce

# Empaquetar e instalar
vsce package
code --install-extension axioma-1.0.0.vsix
```

O simplemente abre la carpeta `vscode-extension` en VS Code y presiona `F5`.

### Opción 2: Desde Python

```bash
pip install -e .
axioma archivo.ax
```

## Uso

```bash
# Ejecutar un archivo
axioma ejemplos/hola_mundo.ax

# Modo REPL interactivo
axioma

# Salir del REPL
salir()
```

## Ejemplos

### Hola Mundo
```
imprimir "Hola, mundo!";
```

### Fibonacci
```
funcion fibonacci(n) {
    si (n <= 1) {
        retornar n;
    }
    retornar fibonacci(n - 1) + fibonacci(n - 2);
}

para (var i = 0; i < 10; i = i + 1) {
    imprimir fibonacci(i);
}
```

### Clases
```
clase Animal {
    funcion iniciar(nombre) {
        este.nombre = nombre;
    }

    funcion saludar() {
        imprimir "Hola, soy " + este.nombre;
    }
}

var a = nuevo Animal("Rex");
a.saludar();
```

### Primos
```
funcion es_primo(n) {
    si (n <= 1) { retornar falso; }
    var i = 2;
    mientras (i * i <= n) {
        si (n % i == 0) { retornar falso; }
        i = i + 1;
    }
    retornar verdadero;
}
```

## Licencia

MIT
