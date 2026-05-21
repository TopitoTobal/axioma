# Operadores

## Aritmeticos

| Operador | Descripcion | Ejemplo | Resultado |
|----------|-------------|---------|-----------|
| `+` | Suma / concatenacion | `5 + 3` | `8` |
| `-` | Resta | `10 - 4` | `6` |
| `*` | Multiplicacion | `3 * 4` | `12` |
| `/` | Division | `10 / 3` | `3.333...` |
| `%` | Modulo (resto) | `10 % 3` | `1` |

El operador `+` tambien concatena strings:

```
"Hola " + "Mundo"    // "Hola Mundo"
"Edad: " + 25        // "Edad: 25"
```

## Comparacion

| Operador | Descripcion | Ejemplo | Resultado |
|----------|-------------|---------|-----------|
| `==` | Igual a | `5 == 5` | `verdadero` |
| `!=` | Distinto de | `5 != 3` | `verdadero` |
| `<` | Menor que | `3 < 5` | `verdadero` |
| `>` | Mayor que | `5 > 3` | `verdadero` |
| `<=` | Menor o igual | `5 <= 5` | `verdadero` |
| `>=` | Mayor o igual | `5 >= 3` | `verdadero` |

## Logicos

| Operador | Descripcion | Ejemplo | Resultado |
|----------|-------------|---------|-----------|
| `y` | AND (ambos verdaderos) | `verdadero y falso` | `falso` |
| `o` | OR (al menos uno verdadero) | `verdadero o falso` | `verdadero` |
| `no` | NOT (negacion) | `no verdadero` | `falso` |

Ejemplos:

```
si (edad >= 18 y tieneLicencia) {
    imprimir "Puede conducir";
}

si (esAdmin o esModerador) {
    imprimir "Acceso permitido";
}

si (no activo) {
    imprimir "Cuenta desactivada";
}
```

## Asignacion

| Operador | Descripcion | Equivalente |
|----------|-------------|-------------|
| `=` | Asignacion simple | `x = 5` |
| `+=` | Suma y asigna | `x += 3` es `x = x + 3` |
| `-=` | Resta y asigna | `x -= 2` es `x = x - 2` |
| `*=` | Multiplica y asigna | `x *= 4` es `x = x * 4` |
| `/=` | Divide y asigna | `x /= 2` es `x = x / 2` |

## Precedencia de Operadores

De mayor a menor prioridad:

1. `()` — Parentesis
2. `no` `-` (unario) — Negacion y signo
3. `*` `/` `%` — Multiplicacion, division, modulo
4. `+` `-` — Suma y resta
5. `<` `>` `<=` `>=` — Comparacion
6. `==` `!=` — Igualdad
7. `y` — AND logico
8. `o` — OR logico
9. `=` `+=` `-=` `*=` `/=` — Asignacion

Ejemplo:

```
var resultado = 5 + 3 * 2;        // 11 (no 16)
var conParentesis = (5 + 3) * 2;  // 16
```
