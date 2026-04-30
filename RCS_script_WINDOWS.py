#!/usr/bin/env python3
import os
import sys
import serial
from serial.tools import list_ports
import subprocess
import webbrowser
import shutil
import keyboard

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
# CONFIG: RUTA de archivos (si quieres abrir PDFs, imágenes, etc.) por numero 
# =========================
Archivos_RUTA = {
    "MODE0": r"C:\Users\marce\OneDrive\Desktop\MODULE_RCS\IRMODULE.pdf",
    "MODE1": r"C:\Users\marce\OneDrive\Desktop\MODULE_RCS\CodigosDelCntrol.txt",
    "MODE2": r"C:\Users\marce\OneDrive\Desktop\Roblox Studio.lnk",
    "MODE3": r"C:\Users\marce\OneDrive\Desktop\Spotify.lnk",
    "MODE4": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Medibang\MediBang Paint Pro\MediBang Paint Pro.lnk",
    "MODE5": r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Google Chrome.lnk",
    "MODE6": r"C:\Users\marce\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Discord Inc\Discord.lnk",
    "MODE7": r"C:\Users\marce\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Steam\Yu-Gi-Oh!  Master Duel.url",
    "MODE8": r"C:\Users\marce\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Steam\Steam.lnk",
    "MODE9": r"C:\Users\marce\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Roblox\Roblox Player.lnk"
    #"#": r "---(La ruta)---",
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

if IS_WINDOWS:
    import ctypes

    user32 = ctypes.WinDLL("user32", use_last_error=True)
    KEYEVENTF_KEYDOWN = 0
    KEYEVENTF_KEYUP = 2

    VK_CONTROL = 0x11
    VK_TAB = 0x09
    VK_SHIFT = 0x10
    VK_MEDIA_PLAY_PAUSE = 0xB3
    VK_MEDIA_NEXT_TRACK = 0xB0
    VK_MEDIA_PREV_TRACK = 0xB1
    VK_VOLUME_MUTE = 0xAD
    VK_VOLUME_DOWN = 0xAE
    VK_VOLUME_UP = 0xAF

    def press_vk(vk):
        user32.keybd_event(vk, 0, KEYEVENTF_KEYDOWN, 0)
        user32.keybd_event(vk, 0, KEYEVENTF_KEYUP, 0)

    def send_hotkey(vks):
        for vk in vks:
            user32.keybd_event(vk, 0, KEYEVENTF_KEYDOWN, 0)
        for vk in reversed(vks):
            user32.keybd_event(vk, 0, KEYEVENTF_KEYUP, 0)

    def windows_media_key(vk):
        press_vk(vk)
else:
    def windows_media_key(vk):
        raise RuntimeError("windows_media_key solo está disponible en Windows")


def music_play_pause():
    if IS_WINDOWS:
        windows_media_key(VK_MEDIA_PLAY_PAUSE)
        return
    if PLAYERCTL:
        run_bg([PLAYERCTL, "play-pause"])
    else:
        print("[WARN] 'playerctl' no está instalado. En Linux Mint: sudo apt install playerctl")

def music_next():
    if IS_WINDOWS:
        windows_media_key(VK_MEDIA_NEXT_TRACK)
        return
    if PLAYERCTL:
        run_bg([PLAYERCTL, "next"])
    else:
        print("[WARN] 'playerctl' no está instalado. sudo apt install playerctl")

def music_prev():
    if IS_WINDOWS:
        windows_media_key(VK_MEDIA_PREV_TRACK)
        return
    if PLAYERCTL:
        run_bg([PLAYERCTL, "previous"])
    else:
        print("[WARN] 'playerctl' no está instalado. sudo apt install playerctl")

def music_vol_up(step="0.05"):
    if IS_WINDOWS:
        windows_media_key(VK_VOLUME_UP)
        return
    if PLAYERCTL:
        run_bg([PLAYERCTL, "volume", f"{step}+"])
    else:
        print("[WARN] 'playerctl' no está instalado. sudo apt install playerctl")

def music_vol_down(step="0.05"):
    if IS_WINDOWS:
        windows_media_key(VK_VOLUME_DOWN)
        return
    if PLAYERCTL:
        run_bg([PLAYERCTL, "volume", f"{step}-"])
    else:
        print("[WARN] 'playerctl' no está instalado. sudo apt install playerctl")

def music_mute():
    if IS_WINDOWS:
        windows_media_key(VK_VOLUME_MUTE)
        return
    if PLAYERCTL:
        run_bg([PLAYERCTL, "volume", "0"])
    else:
        print("[WARN] 'playerctl' no está instalado. sudo apt install playerctl")

def next_browser_tab():
    if IS_WINDOWS:
        send_hotkey([VK_CONTROL, VK_TAB])
        print("Cambiar a la siguiente pestaña (ctrl+Tab)")
        return
    if IS_LINUX and XDOTOOL:
        run_fg([XDOTOOL, "key", "ctrl+Tab"])
        print("Cambiar a la siguiente pestaña (ctrl+Tab)")
    else:
        print("[WARN] xdotool no disponible (o no estás en Linux).")

def prev_browser_tab():
    if IS_WINDOWS:
        send_hotkey([VK_CONTROL, VK_TAB, VK_SHIFT])
        print("Cambiar a la pestaña anterior (ctrl+shift+Tab)")
        return
    if IS_LINUX and XDOTOOL:
        run_fg([XDOTOOL, "key", "ctrl+shift+Tab"])
        print("Cambiar a la pestaña anterior (ctrl+shift+Tab)")
    else:
        print("[WARN] xdotool no disponible (o no estás en Linux).")
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
        default_tag = " (default)" if port == default_port else ""
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
try:
    ser = serial.Serial(PORT, BAUDRATE, timeout=1)
except serial.SerialException as e:
    print(f"[ERROR] No pude abrir el puerto serial {PORT}: {e}")
    print("Asegúrate de que el puerto sea correcto y de que ninguna otra aplicación esté usando el puerto (Arduino IDE, Monitor serial, etc.).")
    print("Puertos seriales detectados:", list_serial_ports())
    sys.exit(1)

# Configura el puerto serial antes de conectar
PORT = choose_serial_port(PORT)
print(f"Usando puerto serial: {PORT}")
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
    if key in Archivos_RUTA:
        try:
            os.startfile(Archivos_RUTA[key])
            print(f"Abrir → {key} : {Archivos_RUTA[key]}")
        except OSError as e:
            print(f"Error: El archivo '{Archivos_RUTA[key]}' no existe o no se puede abrir. Detalles: {e}")
        continue

    # ---------- 2) Controles de música ----------
    # En tu Arduino mandas: "Pausa", "Left", "Rigt", "+", "-", "VolOFF"
    if key == "Pausa":
        music_play_pause()
        print("Música: Play/Pause")
        continue

    if key == "Rigt":
        music_prev()
        print("Música: Anterior")
        continue

    if key == "Left":
        music_next()
        print("Música: Siguiente")
        continue

    if key == "+":
        music_vol_up("0.5")
        print("Volumen: +")
        continue

    if key == "-":
        music_vol_down("0.5")
        print("Volumen: -")
        continue

    if key == "VolOFF":
        music_mute()
        print("Música: Mute")
        continue

    # ---------- 2.5) Controles de WEB ----------

    if key == "MODEPausa":
        keyboard.press_and_release('space')
        continue

    if key == "MODERigt":
        keyboard.press_and_release('right')
        print("web: Rigth")
        continue

    if key == "MODELeft":
        keyboard.press_and_release('left')
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
        print("ON/OFF (apagar o encender el sistema dig) ")
        continue

    if key == "MODE":
        print("MODE (cambiar modo) ")
        continue
    print(f"Ignorado/No mapeado: {key}")

    #---------- COMO CREAR NUEVAS FUNCIONES ----------
    # Si quieres agregar más comandos, hazlo con esta estructura:
    # if key == "NOMBRE_COMANDO":
    #     # Carga de codigo utiles,
