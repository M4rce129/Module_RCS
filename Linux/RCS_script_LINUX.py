#!/usr/bin/env python3
import os
import sys
import serial
from serial.tools import list_ports
import subprocess
import webbrowser
import shutil

# =========================
# CONFIG: Puerto Serial / ONOFF
# =========================
# Windows: "COM3"
# Linux Mint: "/dev/ttyACM0" (o /dev/ttyUSB0)
PORT = "COM8"
BAUDRATE = 9600

# =========================
# CONFIG: URLs por número
# =========================
URLS = {
    "0": "https://www.youtube.com",
    "1": "https://www.youtube.com/watch?v=h8UpC5JbMU0",
    "2": "https://chatgpt.com",
    "3": "https://github.com",
    "4": "https://www.youtube.com/watch?v=L1Ta38LNcUE&list=RDL1Ta38LNcUE&start_radio=1",
    "5": "https://mail.google.com/mail/u/0/#inbox",
    "6": "https://www.wigglypaint.art/",
    "7": "https://www.prepa6.unam.mx/ENP6/_P6/",
    "8": "https://aulas-virtuales.cuaed.unam.mx/",
    "9": "https://www.youtube.com/watch?v=CSvFpBOe8eY&list=RDCSvFpBOe8eY&start_radio=1"
}

# =========================
# CONFIG: RUTA de archivos (si quieres abrir PDFs, imágenes, etc.) por número
# =========================
FILES_PATHS = {
    "MODE0": "/home/tu_usuario/Documentos/IRMODULE.pdf",
    "MODE1": "/home/tu_usuario/Documentos/CodigosDelCntrol.txt",
    # "MODE2": "/ruta/a/otro/archivo",
}

# =========================
# Helpers
# =========================
IS_LINUX = sys.platform.startswith("linux")
IS_WINDOWS = sys.platform.startswith("win")

def run_bg(cmd_list):
    """Ejecuta sin bloquear (para no trabar el loop)."""
    try:
        subprocess.Popen(cmd_list, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception as e:
        print(f"[ERROR] No pude ejecutar: {cmd_list} -> {e}")

def run_fg(cmd_list):
    """Ejecuta y espera (si lo necesitas)."""
    try:
        subprocess.run(cmd_list, check=False)
    except Exception as e:
        print(f"[ERROR] No pude ejecutar: {cmd_list} -> {e}")

# Detecta si playerctl existe (Linux)
PLAYERCTL = shutil.which("playerctl") if IS_LINUX else None
XDOTOOL  = shutil.which("xdotool")  if IS_LINUX else None

def music_play_pause():
    if PLAYERCTL:
        run_bg([PLAYERCTL, "play-pause"])
    else:
        print("[WARN] 'playerctl' no está instalado. En Linux Mint: sudo apt install playerctl")

def music_next():
    if PLAYERCTL:
        run_bg([PLAYERCTL, "next"])
    else:
        print("[WARN] 'playerctl' no está instalado. sudo apt install playerctl")

def music_prev():
    if PLAYERCTL:
        run_bg([PLAYERCTL, "previous"])
    else:
        print("[WARN] 'playerctl' no está instalado. sudo apt install playerctl")

def music_vol_up(step="0.05"):
    if PLAYERCTL:
        run_bg([PLAYERCTL, "volume", f"{step}+"])
    else:
        print("[WARN] 'playerctl' no está instalado. sudo apt install playerctl")

def music_vol_down(step="0.05"):
    if PLAYERCTL:
        run_bg([PLAYERCTL, "volume", f"{step}-"])
    else:
        print("[WARN] 'playerctl' no está instalado. sudo apt install playerctl")

def music_mute():
    if PLAYERCTL:
        run_bg([PLAYERCTL, "volume", "0"])
    else:
        print("[WARN] 'playerctl' no está instalado. sudo apt install playerctl")

def open_local_file(path):
    if not os.path.exists(path):
        print(f"[ERROR] El archivo no existe: {path}")
        return

    if IS_LINUX:
        xdg_open = shutil.which("xdg-open")
        if xdg_open:
            run_bg([xdg_open, path])
            return

    try:
        webbrowser.open(f"file://{os.path.abspath(path)}")
    except Exception as e:
        print(f"[ERROR] No pude abrir el archivo: {path} -> {e}")


def browser_key(key_name):
    if IS_LINUX and XDOTOOL:
        run_fg([XDOTOOL, "key", key_name])
        return True

    print("[WARN] xdotool no disponible (o no estás en Linux).")
    return False


def next_browser_tab():
    if browser_key("ctrl+Tab"):
        print("Cambiar a la siguiente pestaña (ctrl+Tab)")


def prev_browser_tab():
    if browser_key("ctrl+shift+Tab"):
        print("Cambiar a la pestaña anterior (ctrl+shift+Tab)")

# =========================
# Helpers
# =========================

def get_serial_ports():
    return [p.device for p in list_ports.comports()]


def list_serial_ports():
    ports = get_serial_ports()
    if not ports:
        return "<ninguno>"
    return ", ".join(ports)


def choose_serial_port(default_port=None):
    ports = get_serial_ports()
    if not ports:
        print("[WARN] No hay puertos seriales detectados.")
        return default_port

    print("Puertos seriales detectados:")
    for idx, port in enumerate(ports, start=1):
        default_tag = " (predeterminado)" if port == default_port else ""
        print(f"  {idx}. {port}{default_tag}")

    selection = input("Selecciona un puerto por número o deja vacío para usar el predeterminado: ").strip()
    if selection == "":
        return default_port

    if selection.isdigit():
        index = int(selection) - 1
        if 0 <= index < len(ports):
            return ports[index]

    if selection in ports:
        return selection

    print("Selección no válida. Usando el puerto predeterminado.")
    return default_port

# =========================
# MAIN
# =========================
PORT = choose_serial_port(PORT)
print(f"Usando puerto serial: {PORT}")
try:
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
except serial.SerialException as e:
    print(f"[ERROR] No pude abrir el puerto serial {PORT}: {e}")
    print("Asegúrate de que el puerto sea correcto y de que ninguna otra aplicación esté usando el puerto (Arduino IDE, Monitor serial, etc.).")
    print("Puertos seriales detectados:", list_serial_ports())
    sys.exit(1)

print("Escuchando Arduino...")

while True:
    line = ser.readline().decode("utf-8", errors="ignore").strip()

    # Esperamos líneas tipo: KEY:3
    if not line.startswith("KEY:"):
        continue

    key = line[4:]  # extrae el comando (ej: "3", "Pausa", "Left", "+", etc.)

    # ---------- 1) URLs ----------
    if key in URLS:
        webbrowser.open(URLS[key])
        print(f"Abrir → {key} : {URLS[key]}")
        continue

    # ---------- 1.5) Archivos locales ----------
    if key in FILES_PATHS:
        open_local_file(FILES_PATHS[key])
        print(f"Abrir → {key} : {FILES_PATHS[key]}")
        continue

    # ---------- 2) Controles de música ----------
    # En tu Arduino mandas: "Pausa", "Left", "Rigt", "+", "-", "VolOFF"
    if key == "Pausa":
        music_play_pause()
        print("Música: Play/Pause")
        continue

    if key == "Left":
        music_prev()
        print("Música: Anterior")
        continue

    if key == "Rigt":
        music_next()
        print("Música: Siguiente")
        continue

    if key == "+":
        music_vol_up("0.05")
        print("Música: Volumen +")
        continue

    if key == "-":
        music_vol_down("0.05")
        print("Música: Volumen -")
        continue

    if key == "VolOFF":
        music_mute()
        print("Música: Mute")
        continue

    # ---------- 2.5) Controles de WEB ----------
    if key == "MODEPausa":
        browser_key("Return")
        continue

    if key == "MODERigt":
        browser_key("Right")
        print("web: Right")
        continue

    if key == "MODELeft":
        browser_key("Left")
        print("web: Left")
        continue

    if key == "MODE+":
        next_browser_tab()
        print("web: next tab")
        continue

    if key == "MODE-":
        prev_browser_tab()
        print("web: previous tab")
        continue

    # ---------- 3) Otros ----------
    if key == "ONOFF":
        print("ON/OFF (apagar o encender el sistema dig)")
        continue

    if key == "MODE":
        print("MODE (cambiar modo)")
        continue

    print(f"Ignorado/No mapeado: {key}")


    #---------- COMO CREAR NUEVAS FUNCIONES ----------
    # Si quieres agregar más comandos, hazlo con esta estructura:
    # if key == "NOMBRE_COMANDO":
    #     # Carga de codigo utiles,
    