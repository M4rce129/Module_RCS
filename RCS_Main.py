import tkinter 
import platform
import subprocess
import os

rcs_process = None  # Variable global para el proceso en segundo plano

def detectar_so():
    return platform.system()

def activate_rcs():
    global rcs_process
    if rcs_process is None or rcs_process.poll() is not None:  # Si no está corriendo
        so = detectar_so()
        if so == "Windows":
            script = "RCS_scrpt_WINDOWS.py"
        elif so == "Linux":
            script = "RCS_script_LINUX.py"
        else:
            print(f"SO no soportado: {so}")
            return
        
        try:
            rcs_process = subprocess.Popen(['python', script])
            print(f"Módulo RCS activado - Script {script} ejecutándose en segundo plano")
        except Exception as e:
            print(f"Error al activar RCS: {e}")
    else:
        print("Módulo RCS ya está activado")
    
    window.destroy()  # Cerrar la ventana como indicador de selección

def deactivate_rcs():
    global rcs_process
    if rcs_process and rcs_process.poll() is None:  # Si está corriendo
        rcs_process.terminate()
        rcs_process.wait()
        print("Script de controladores detenido")
    
    window.destroy()  # Cerrar la ventana
    print("Sistema apagándose...")


window = tkinter.Tk()
window.title("RCS - Active Modules")
window.geometry("350x200")
window.configure(bg="black")

def round_rectangle(canvas, x1, y1, x2, y2, radius=20, **kwargs):
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


def create_round_button(parent, text, command, width=140, height=50, radius=18, bg=None, fg="white", active_bg=None):
    if active_bg is None:
        active_bg = bg
    canvas = tkinter.Canvas(parent, width=width, height=height, bg="black", highlightthickness=0)
    shape = round_rectangle(canvas, 0, 0, width, height, radius=radius, fill=bg, outline=bg)
    canvas.create_text(width // 2, height // 2, text=text, fill=fg, font=("Inconsolata", 16))
    canvas.bind("<Button-1>", lambda event: command())
    canvas.bind("<Enter>", lambda event: canvas.itemconfig(shape, fill=active_bg, outline=active_bg))
    canvas.bind("<Leave>", lambda event: canvas.itemconfig(shape, fill=bg, outline=bg))
    return canvas

text = tkinter.Label(window, text = "¿Activar módulo RCS?",font=("Inconsolata", 20), fg="white", bg="black")
text.pack()

button_frame = tkinter.Frame(window, bg="black")
button_frame.pack(pady=20)

yes_button = create_round_button(button_frame, "Sí", activate_rcs, bg="#66cc66",active_bg="#abffab")
no_button = create_round_button(button_frame, "No", deactivate_rcs, bg="#cc6666",active_bg="#ffabab")
yes_button.pack(side=tkinter.LEFT, padx=10)
no_button.pack(side=tkinter.LEFT, padx=10)

window.mainloop()