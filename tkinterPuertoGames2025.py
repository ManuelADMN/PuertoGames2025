import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from conexion_sqlserver import (
    obtener_videojuegos, obtener_videojuegos_ordenado,
    insertar_videojuego, actualizar_videojuego, eliminar_videojuego
)

def refrescar_tree(filtro=None, asc=True, ordenar=False):
    for row in tree.get_children():
        tree.delete(row)
    if ordenar:
        datos = obtener_videojuegos_ordenado(ascendente=asc)
    else:
        datos = obtener_videojuegos(filtro)
    for idv, nombre, genero, precio, stock, plataforma in datos:
        tree.insert('', 'end', values=(idv, nombre, genero, precio, stock, plataforma))

def validar_campos(require_id=False):
    campos = {
        "Nombre": entrada_nombre.get().strip(),
        "Género": entrada_genero.get().strip(),
        "Precio": entrada_precio.get().strip(),
        "Stock": entrada_stock.get().strip(),
        "Plataforma ID": entrada_plataforma.get().strip()
    }
    if require_id:
        campos["ID"] = entrada_id.get().strip()
    for k, v in campos.items():
        if not v:
            raise ValueError(f"El campo {k} es obligatorio.")
    try:
        float(campos["Precio"])
        int(campos["Stock"])
        int(campos["Plataforma ID"])
        if require_id:
            int(campos["ID"])
    except:
        raise ValueError("Precio, Stock, ID y Plataforma ID deben ser numéricos.")

def on_nuevo():
    try:
        validar_campos()
        insertar_videojuego(
            entrada_nombre.get().strip(),
            entrada_genero.get().strip(),
            float(entrada_precio.get()),
            int(entrada_plataforma.get()),
            int(entrada_stock.get())
        )
        refrescar_tree()
        for e in (entrada_nombre, entrada_genero, entrada_precio, entrada_stock, entrada_plataforma):
            e.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", e)

def on_actualizar():
    try:
        validar_campos(require_id=True)
        actualizar_videojuego(
            int(entrada_id.get()),
            entrada_nombre.get().strip(),
            entrada_genero.get().strip(),
            float(entrada_precio.get()),
            int(entrada_stock.get()),
            int(entrada_plataforma.get())
        )
        refrescar_tree()
        for e in (entrada_id, entrada_nombre, entrada_genero, entrada_precio, entrada_stock, entrada_plataforma):
            e.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", e)

def on_eliminar():
    try:
        vid = entrada_id.get().strip()
        if not vid:
            raise ValueError("ID es obligatorio para eliminar.")
        if messagebox.askyesno("Confirmar", "¿Desea eliminar este videojuego?"):
            eliminar_videojuego(int(vid))
            refrescar_tree()
            entrada_id.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", e)

def on_seleccionar(event):
    item = tree.selection()[0]
    idv, nombre, genero, precio, stock, plataforma = tree.item(item, 'values')
    for entry, val in zip(
        (entrada_id, entrada_nombre, entrada_genero, entrada_precio, entrada_stock, entrada_plataforma),
        (idv, nombre, genero, precio, stock, plataforma)
    ):
        entry.delete(0, tk.END)
        entry.insert(0, val)

def on_buscar():
    filtro = entrada_busqueda.get().strip()
    refrescar_tree(filtro=filtro)

def on_ordenar(asc):
    refrescar_tree(ordenar=True, asc=asc)

def on_estadisticas():
    datos = obtener_videojuegos()
    conteo = {}
    for *_, plataforma in datos:
        conteo[plataforma] = conteo.get(plataforma, 0) + 1
    fig, ax = plt.subplots()
    ax.bar(conteo.keys(), conteo.values())
    ax.set_ylabel("Cantidad de juegos")
    ax.set_title("Videojuegos por Plataforma")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

ventana = tk.Tk()
ventana.title("CRUD Videojuegos")
ventana.geometry("1000x700")

# Búsqueda y orden
frame_top = tk.Frame(ventana)
frame_top.pack(pady=5, fill='x')
entrada_busqueda = tk.Entry(frame_top)
entrada_busqueda.pack(side='left', padx=5)
tk.Button(frame_top, text="Buscar", command=on_buscar).pack(side='left', padx=5)
tk.Button(frame_top, text="↑ Precio", command=lambda: on_ordenar(True)).pack(side='left')
tk.Button(frame_top, text="↓ Precio", command=lambda: on_ordenar(False)).pack(side='left')
tk.Button(frame_top, text="Ver estadísticas", command=on_estadisticas).pack(side='right', padx=5)

# Treeview con scroll
cols = ("ID","Nombre","Género","Precio","Stock","Plataforma")
tree = ttk.Treeview(ventana, columns=cols, show='headings')
for c in cols:
    tree.heading(c, text=c)
    tree.column(c, width=100, anchor='center')
scroll_y = ttk.Scrollbar(ventana, orient='vertical', command=tree.yview)
scroll_x = ttk.Scrollbar(ventana, orient='horizontal', command=tree.xview)
tree.configure(yscroll=scroll_y.set, xscroll=scroll_x.set)
tree.pack(fill='both', expand=True)
scroll_y.pack(side='right', fill='y')
scroll_x.pack(side='bottom', fill='x')
tree.bind('<<TreeviewSelect>>', on_seleccionar)

# Formulario CRUD
frame_form = tk.Frame(ventana)
frame_form.pack(pady=10)
labels = ["ID","Nombre","Género","Precio","Stock","Plataforma ID"]
entries = []
for i, lbl in enumerate(labels):
    tk.Label(frame_form, text=lbl+":").grid(row=i, column=0, sticky="e", padx=5, pady=2)
    ent = tk.Entry(frame_form)
    ent.grid(row=i, column=1, padx=5, pady=2)
    entries.append(ent)
entrada_id, entrada_nombre, entrada_genero, entrada_precio, entrada_stock, entrada_plataforma = entries

# Botones CRUD
frame_btns = tk.Frame(ventana)
frame_btns.pack(pady=5)
tk.Button(frame_btns, text="Nuevo",    command=on_nuevo,    width=12).grid(row=0, column=0, padx=5)
tk.Button(frame_btns, text="Actualizar", command=on_actualizar, width=12).grid(row=0, column=1, padx=5)
tk.Button(frame_btns, text="Eliminar", command=on_eliminar, width=12).grid(row=0, column=2, padx=5)
tk.Button(frame_btns, text="Cerrar",    command=ventana.destroy, width=12).grid(row=0, column=3, padx=5)

refrescar_tree()
ventana.mainloop()
