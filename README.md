# Michoacan-Juego-de-Pesca-de-Paquetes

**Michoacán: juego de pesca de paquetes en red.** Una analogía de lago y peces nativos para aprender redes y protocolos, entrenar personal técnico o competir. Reglas y scripts para el host y los jugadores.

> **Michoacán** significa *"lugar de pescadores"*. En este juego, la red es un lago o un río y cada paquete que capturas es un pez.

---

## ¿Qué es?

"Michoacán" es el nombre de una serie de reglas pensadas para crear un juego con el que los más pequeños pueden acercarse y experimentar, de forma real, el mundo de las redes y los protocolos de red.

- **Estudiantes:** una herramienta para comprender mejor los conceptos y apropiarse del conocimiento.
- **Profesionales** (por ejemplo, ingenieros que instalan y dan mantenimiento a sensores en cualquier industria): una herramienta de entrenamiento de personal, para entender qué sucede en realidad en la red.
- **Competencia profesional:** puede usarse entre verdaderos profesionales del código y las redes, con contextos únicos y reglas específicas. Imagina a dos titanes de la tecnología codificando en tiempo real, cabeza a cabeza: un boxeo de código.

## La analogía

Los paquetes son **peces nativos de Michoacán**; la red es un **lago, río u océano**. Es solo eso: una analogía práctica que le da sentido a las reglas. Todo el contexto puede cambiar, y las reglas pueden volverse más específicas y difíciles. Esto es el comienzo de la concepción del juego; en competencias reales debe ser un reto completo.

## Los peces

El host crea una lista de palabras codificadas de diferentes formas. Son nombres de especies de peces nativas de Michoacán.

| Paquete (pez)   | Protocolo | Codificación |
|-----------------|-----------|--------------|
| Kurucha urapiti | TCP       | UTF-8        |
| Charari         | UDP       | UTF-8        |
| Akúmara         | FTP       | UTF-8        |

El host puede agregar más peces, otros protocolos u otras codificaciones para subir la dificultad.

## Contenido del repositorio

```
Michoacan-Juego-de-Pesca-de-Paquetes/
├── README.md        ← esta guía general
├── host/
│   ├── peces.csv    ← lista de paquetes codificados que el host enviará
│   └── paketsender  ← software que envía los paquetes a toda la red
├── jugador/
│   └── pescador.py  ← script base: captura el paquete, lo decodifica y muestra el resultado
└── LICENSE
```

## Cómo se juega

Las reglas son simples:

1. El host entrega a los participantes un código muy básico de referencia (`pescador.py`).
2. El host dicta las reglas y los tiempos de captura, porque es quien libera los paquetes en la red.
3. Antes de liberar cada paquete, el host dicta cómo debe capturarse, de qué forma viene codificado, qué protocolo usa y si debe guardarse en una base de datos específica.
4. Cada participante lleva una **tabla personal** donde registra los paquetes ya decodificados.
5. Al finalizar, el host analiza qué participantes cumplieron todas las reglas de captura a tiempo. Puede haber empates en los mismos lugares.

---

## Guía para el host

1. **Prepara la lista de peces.** Edita `host/peces.csv` con un pez por línea: nombre, protocolo, codificación, mensaje codificado y puntos.
2. **Define las reglas de la partida.** Duración, tiempos entre paquetes, forma de captura y si se guarda en una base de datos.
3. **Entrega el script base** (`jugador/pescador.py`) a los participantes y confirma que todos están conectados a la misma red.
4. **Avisa que empieza la pesca.** Antes de cada paquete, dicta las reglas de ese pez (cómo capturarlo, codificación y protocolo).
5. **Libera los paquetes** con `paketsender`, que los envía a toda la red.
6. **Al terminar, revisa las tablas personales** de los participantes y asigna lugares según quiénes cumplieron todas las reglas en tiempo.

## Guía para el jugador

1. **Conéctate a la red del juego** que indique el host.
2. **Prepara el script base** (`pescador.py`) con lo que pida el host para ejecutarlo.
3. **Espera el aviso del host** con las reglas del siguiente pez.
4. **Captura el paquete.** El script lo captura, lo decodifica y te muestra el resultado.
5. **Regístralo en tu tabla personal.**

Ejemplo de tabla personal:

| Pez capturado | Protocolo | Codificación | Mensaje decodificado | Hora |
|---------------|-----------|--------------|----------------------|------|
|               |           |              |                      |      |

6. **Entrega tu tabla al host** al finalizar.

---

## Seguridad

El script captura tráfico de red. Juega **solo en una red acordada entre todos los participantes** y nunca en redes ajenas. Si juegan niñas y niños, hazlo con supervisión de una persona adulta.

## Crea tus propias reglas

Juega con tus amigos, crea tus propias reglas y compártelas con la comunidad.

## Licencia

Michoacán se distribuye bajo la licencia **GNU General Public License v3.0 (GPL-3.0)**. Puedes jugarlo, modificarlo y compartirlo; si distribuyes una versión modificada, debe mantenerse libre bajo la misma licencia.
