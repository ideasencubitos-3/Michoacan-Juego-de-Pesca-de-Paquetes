#!/usr/bin/env python3
"""
pescador.py - Script base del jugador
Michoacán: juego de pesca de paquetes en red ("lugar de pescadores")

¿QUÉ HACE?
    1. Escucha la red hasta capturar UN paquete (tu pez).
    2. Lo decodifica con la codificación que dictó el host.
    3. Te muestra el mensaje decodificado.
    4. Opcional: lo registra en tu tabla de la base de datos del host.

REQUISITOS
    - Python 3.8 o superior.
    - Scapy (para capturar):               pip install scapy
    - Solo si vas a guardar en la BD:      pip install mysql-connector-python
    - Permisos de administrador para capturar paquetes:
        * Linux/macOS: ejecuta con sudo.
        * Windows: instala Npcap y abre la terminal como administrador.

EJEMPLOS (usa los datos que te dicte el host)
    # Capturar un paquete UDP en el puerto 5005, decodificarlo como UTF-8:
    sudo python3 pescador.py --protocolo udp --puerto 5005 --codificacion utf-8

    # Capturar y guardar en tu tabla de la base de datos del host:
    sudo python3 pescador.py --protocolo tcp --puerto 5005 \\
        --guardar --servidor 192.168.1.10 --usuario jugador01 \\
        --tabla capturas_jugador01

    # Probar la decodificación sin red (no necesita permisos):
    python3 pescador.py --texto 506573636173746520756e2043686172617269 --codificacion hex

IMPORTANTE
    Juega solo en la red acordada con todos los participantes. Usa --puerto con
    el puerto que indique el host, para capturar únicamente los paquetes del juego.

Este es un código base: puedes modificarlo, mejorarlo y compartirlo (GPL-3.0).
"""

import argparse
import base64
import getpass
import os
import re
import sys

# Filtros de captura según el protocolo del pez.
# FTP usa por defecto el puerto 21 (puedes cambiarlo con --puerto).
FILTROS = {"tcp": "tcp", "udp": "udp", "ftp": "tcp port 21"}


def decodificar(carga: bytes, codificacion: str) -> str:
    """Convierte los bytes del paquete en el mensaje legible."""
    if codificacion == "utf-8":
        return carga.decode("utf-8")
    if codificacion == "hex":
        # El paquete trae el mensaje escrito en hexadecimal.
        return bytes.fromhex(carga.decode("ascii").strip()).decode("utf-8")
    if codificacion == "base64":
        return base64.b64decode(carga.strip()).decode("utf-8")
    raise ValueError(f"Codificación no soportada: {codificacion}")


def capturar_paquete(interfaz, protocolo, puerto, tiempo):
    """Espera un paquete con datos y devuelve sus bytes (o None si no llegó)."""
    try:
        from scapy.all import sniff, Raw
    except ImportError:
        sys.exit("Falta Scapy. Instálalo con:  pip install scapy")

    filtro = FILTROS[protocolo]
    if puerto:
        base = "udp" if protocolo == "udp" else "tcp"
        filtro = f"{base} port {puerto}"

    print(f"Pescando... (filtro: {filtro}, espera máxima: {tiempo} s)")
    paquetes = sniff(
        iface=interfaz,
        filter=filtro,
        count=1,
        timeout=tiempo,
        lfilter=lambda p: Raw in p,  # solo paquetes que traen datos
    )
    if not paquetes:
        return None
    return bytes(paquetes[0][Raw].load)


def guardar_en_bd(args, pez, protocolo, codificacion, mensaje):
    """Registra la captura en tu tabla. La hora la pone el servidor."""
    try:
        import mysql.connector
    except ImportError:
        sys.exit("Falta el conector. Instálalo con:  pip install mysql-connector-python")

    # El nombre de la tabla solo puede tener letras, números y guion bajo.
    if not args.tabla or not re.fullmatch(r"[A-Za-z0-9_]+", args.tabla):
        sys.exit("Indica tu tabla con --tabla (solo letras, números y guion bajo).")

    clave = os.environ.get("PESCADOR_CLAVE") or getpass.getpass(
        f"Contraseña de {args.usuario}: "
    )
    conexion = mysql.connector.connect(
        host=args.servidor,
        port=args.puerto_bd,
        user=args.usuario,
        password=clave,
        database=args.bd,
    )
    try:
        cursor = conexion.cursor()
        cursor.execute(
            f"INSERT INTO {args.tabla} "
            "(pez, protocolo, codificacion, mensaje_decodificado) "
            "VALUES (%s, %s, %s, %s)",
            (pez, protocolo.upper(), codificacion.upper(), mensaje),
        )
        conexion.commit()
    finally:
        conexion.close()
    print(f"Registrado en {args.bd}.{args.tabla}.")


def leer_argumentos():
    p = argparse.ArgumentParser(
        description="Pescador: captura, decodifica y registra paquetes (Michoacán)."
    )
    p.add_argument("--protocolo", choices=FILTROS, default="udp",
                   help="Protocolo del pez (lo dicta el host). Por defecto: udp")
    p.add_argument("--codificacion", choices=["utf-8", "hex", "base64"],
                   default="utf-8", help="Codificación del mensaje (la dicta el host)")
    p.add_argument("--puerto", type=int,
                   help="Puerto del juego (lo indica el host)")
    p.add_argument("--interfaz",
                   help="Tarjeta de red a escuchar. Si no la indicas, usa la principal")
    p.add_argument("--tiempo", type=int, default=60,
                   help="Segundos máximos de espera. Por defecto: 60")
    p.add_argument("--texto",
                   help="Modo prueba: decodifica este texto sin capturar nada")

    bd = p.add_argument_group("Registro en la base de datos del host")
    bd.add_argument("--guardar", action="store_true",
                    help="Guarda la captura en tu tabla")
    bd.add_argument("--servidor", default="127.0.0.1", help="IP del host")
    bd.add_argument("--puerto-bd", type=int, default=3306, dest="puerto_bd")
    bd.add_argument("--bd", default="michoacan", help="Nombre de la base de datos")
    bd.add_argument("--tabla", help="Tu tabla, por ejemplo capturas_jugador01")
    bd.add_argument("--usuario", help="Tu usuario, por ejemplo jugador01")
    bd.add_argument("--pez", help="Nombre del pez capturado")
    return p.parse_args()


def main():
    args = leer_argumentos()

    # 1. Obtener el paquete (capturado o de prueba)
    if args.texto:
        carga = args.texto.encode("utf-8")
    else:
        carga = capturar_paquete(args.interfaz, args.protocolo, args.puerto, args.tiempo)
        if carga is None:
            sys.exit("No pescaste nada esta vez. Intenta de nuevo.")

    print(f"¡Algo picó! Paquete de {len(carga)} bytes ({args.protocolo.upper()}).")

    # 2. Decodificar
    try:
        mensaje = decodificar(carga, args.codificacion)
    except ValueError:
        sys.exit("No pude decodificarlo con esa codificación. "
                 "Revisa lo que dictó el host e intenta otra vez.")

    # 3. Mostrar resultado
    print("\nMensaje decodificado:")
    print(f"  {mensaje}\n")

    # 4. Registrar (opcional)
    if args.guardar:
        if not args.usuario:
            sys.exit("Indica tu usuario con --usuario.")
        pez = args.pez or input("¿Qué pez capturaste? ").strip()
        if not pez:
            sys.exit("Necesito el nombre del pez para registrarlo.")
        guardar_en_bd(args, pez, args.protocolo, args.codificacion, mensaje)


if __name__ == "__main__":
    main()
