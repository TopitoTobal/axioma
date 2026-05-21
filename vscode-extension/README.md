# Axioma - Extension para VS Code

Soporte para el lenguaje de programacion **Axioma** en Visual Studio Code.

## Caracteristicas

- Resaltado de sintaxis para archivos `.ax`
- Configuracion de lenguaje (comentarios, brackets, auto-cierre)
- Snippets para estructuras comunes
- Icono del lenguaje

## Instalacion

1. Abre la carpeta `vscode-extension` en VS Code
2. Presiona `F5` para iniciar una ventana de Extension Development Host
3. Abre cualquier archivo `.ax` para ver el resaltado

### Instalacion permanente

```bash
# Instalar vsce si no lo tienes
npm install -g @vscode/vsce

# Empaquetar la extension
cd vscode-extension
vsce package

# Instalar el .vsix generado
code --install-extension axioma-1.0.0.vsix
```

## Snippets

| Prefijo | Descripcion |
|---------|-------------|
| `hola` | Imprime Hola mundo |
| `si` | Estructura condicional |
| `si-sino` | Condicional con sino |
| `mientras` | Bucle mientras |
| `para` | Bucle para |
| `funcion` | Declaracion de funcion |
| `imprimir` | Imprime un valor |
| `var` | Declaracion de variable |
| `clase` | Declaracion de clase |
| `clase-hereda` | Clase con herencia |
| `retornar` | Retorna un valor |
