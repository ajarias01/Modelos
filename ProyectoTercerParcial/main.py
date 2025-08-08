from tkinter import *

root = Tk()
root.title("WordCraft")
root.resizable(False, False)
root.geometry("650x350")
root.iconbitmap("Images/iconoVentana.ico")
root.config(bg="black")

# Texto de bienvenida
texto = """¡Bienvenido a WordCraft!
Forma palabras usando las letras disponibles.
Este juego te ayudará a mejorar tu vocabulario
mientras te diviertes."""

etiqueta = Label(root, text=texto,
                 font=("Arial", 12),
                 fg="white", bg="black",
                 justify=LEFT)
etiqueta.pack(pady=20, padx=20, anchor="w")

# Opciones del menú
opciones = ["Jugar", "Instrucciones", "Salir"]
indice_actual = 0  # Opción seleccionada

# Crear etiquetas para cada opción
etiquetas_opciones = []

def mostrar_opciones():
    for i, texto in enumerate(opciones):
        if i == indice_actual:
            etiquetas_opciones[i].config(bg="white", fg="black", font=("Arial", 12, "bold"))
        else:
            etiquetas_opciones[i].config(bg="black", fg="white", font=("Arial", 12))

for opcion in opciones:
    lbl = Label(root, text=opcion, font=("Arial", 12), bg="black", fg="white")
    lbl.pack()
    etiquetas_opciones.append(lbl)

mostrar_opciones()

# Función para manejar las teclas ↑ ↓
def manejar_tecla(event):
    global indice_actual
    if event.keysym == "Up":
        indice_actual = (indice_actual - 1) % len(opciones)
    elif event.keysym == "Down":
        indice_actual = (indice_actual + 1) % len(opciones)
    mostrar_opciones()

# Enlazar las teclas al evento
root.bind("<Up>", manejar_tecla)
root.bind("<Down>", manejar_tecla)

root.mainloop()
