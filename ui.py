import tkinter as tk
from tkinter import messagebox
from controllers import *

def actualizar_lista_mesas():
    """Actualiza la lista de mesas en la interfaz."""
    lista_mesas.delete(0, tk.END)
    for mesa_id in range(1, 11):  # Suponiendo que hay 10 mesas
        estado = obtener_estado_mesa(mesa_id)
        lista_mesas.insert(tk.END, f"Mesa {mesa_id}: {estado}")

def cambiar_estado():
    """Cambia el estado de la mesa seleccionada."""
    seleccion = lista_mesas.curselection()
    if not seleccion:
        messagebox.showwarning("Aviso", "Seleccione una mesa")
        return
    mesa_id = seleccion[0] + 1
    nuevo_estado = estado_var.get()
    cambiar_estado_mesa(mesa_id, nuevo_estado)
    actualizar_lista_mesas()

def iniciar_interfaz():
    """Inicia la interfaz gráfica."""
    global lista_mesas, estado_var
    
    root = tk.Tk()
    root.title("Gestión de Comedor")
    root.geometry("400x400")

    lista_mesas = tk.Listbox(root, height=10)
    lista_mesas.pack(pady=10)

    estado_var = tk.StringVar()
    estados = ["Libre", "Ocupada", "Reservada", "Pagada"]
    estado_menu = tk.OptionMenu(root, estado_var, *estados)
    estado_menu.pack()

    btn_cambiar_estado = tk.Button(root, text="Cambiar Estado", command=cambiar_estado)
    btn_cambiar_estado.pack()

    actualizar_lista_mesas()
    root.mainloop()