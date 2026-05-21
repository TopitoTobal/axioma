# Ruta de Desarrollo - Axioma

Cosas por terminar y mejorar, ordenadas por prioridad.

---

## 1. VS Code Extension — Publicar en Marketplace

- [ ] Crear publisher `TopitoTobal` en https://marketplace.visualstudio.com/manage
- [ ] Generar PAT (Personal Access Token) en https://dev.azure.com
- [ ] Ejecutar `vsce login TopitoTobal` y pegar el token
- [ ] Publicar con `vsce publish`

## 2. Documentacion — Deploy a Netlify

- [ ] Ir a https://app.netlify.com > Add new site > Import from GitHub
- [ ] Seleccionar `TopitoTobal/axioma`
- [ ] Netlify detecta automaticamente: build = `pip install -r requirements-docs.txt && mkdocs build`, publish = `site`
- [ ] Configurar dominio personalizado (opcional)
- [ ] Agregar badge de "Deployed on Netlify" al README

## 3. Testing — Suite de Pruebas

- [ ] Tests unitarios para el lexer
- [ ] Tests unitarios para el parser
- [ ] Tests unitarios para el interprete
- [ ] Tests de integracion con los ejemplos
- [ ] CI/CD con GitHub Actions (ejecutar tests en cada push)

## 4. Mejoras al Lenguaje

- [ ] `len()` — Obtener longitud de listas y strings
- [ ] `sino si` — Sintaxis compacta para condiciones anidadas
- [ ] `romper` — Break en bucles
- [ ] `continuar` — Continue en bucles
- [ ] `segun` — Switch/case
- [ ] `importar` — Sistema de modulos/archivos
- [ ] Operadores de comparacion encadenados (`1 < x < 10`)
- [ ] Metodos de string: `mayusculas()`, `minusculas()`, `recortar()`, `dividir()`
- [ ] Metodos de lista: `empujar()`, `sacar()`, `longitud()`
- [ ] Tipos de datos adicionales: diccionarios/objetos literales (`{ clave: valor }`)
- [ ] Rango (`1..10`)
- [ ] Funciones anonimas (lambdas)
- [ ] `intentar` / `atrapar` — Manejo de errores

## 5. Mejoras al CLI

- [ ] Mejor formateo de errores (colores, contexto de linea)
- [ ] Historial de comandos en REPL (flecha arriba)
- [ ] Comando `--version`
- [ ] Comando `--help`
- [ ] Comando `--repl` para forzar modo interactivo
- [ ] Poder ejecutar codigo con `-c "imprimir 2+2"`

## 6. VS Code Extension — Mejoras

- [ ] Formateador de codigo
- [ ] Linter con deteccion de errores en tiempo real
- [ ] Resaltado de errores inline
- [ ] Ir a definicion de funciones
- [ ] Autocompletado (IntelliSense)
- [ ] Hover con informacion de tipos
- [ ] Snippets para estructuras de control comunes

## 7. Performance

- [ ] Compilador a bytecode + maquina virtual (reemplazar tree-walking)
- [ ] Reescritura en Rust (usando `rustyline` para REPL, `cranelift` para JIT)
- [ ] O reescritura en Go (simple, cross-compilacion nativa)

## 8. Ecosistema

- [ ] Pagina web del lenguaje (landing page con docs, playground, ejemplos)
- [ ] Playground online en el navegador (compilar a WASM)
- [ ] Lenguaje:2026 - Protocolo de servidor de lenguaje (LSP)
- [ ] Gestor de paquetes (`axioma install`)
- [ ] Editor de codigo online (Monaco Editor con syntax highlighting)

## 9. Documentacion — Completar

- [ ] Tutorial interactivo paso a paso
- [ ] Video de introduccion al lenguaje
- [ ] Seccion de mejores practicas
- [ ] Guia de migracion desde Python/JS
- [ ] Referencia de libreria estandar
- [ ] Diagrama de la arquitectura del interprete

## 10. Community

- [ ] Template para issues (bug report, feature request)
- [ ] Template para pull requests
- [ ] Contributing guidelines (CONTRIBUTING.md)
- [ ] Code of conduct
- [ ] Discord / Telegram para la comunidad
