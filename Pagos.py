import sqlite3
import customtkinter as ctk
from tkinter import messagebox
from tkinter import ttk


# Función para crear la base de datos y las tablas necesarias
def create_db():
    conn = sqlite3.connect('clientes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    usuario TEXT, 
                    contrasena TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS clientes (
                    cliente_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    nombre TEXT, 
                    dni TEXT, 
                    rtn TEXT, 
                    direccion TEXT, 
                    telefono TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS activos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    cliente_id INTEGER, 
                    numero_lote TEXT, 
                    costo_total REAL, 
                    prima REAL, 
                    medidas TEXT, 
                    plazo_anos INTEGER, 
                    fecha_inicio_pago TEXT, 
                    fecha_fin_pago TEXT, 
                    total_a_financiar REAL, 
                    desglose_cuotas TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS pagos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    cliente_id INTEGER, 
                    cuota INTEGER, 
                    fecha_pago TEXT, 
                    cantidad_abonada REAL, 
                    estado_pago TEXT, 
                    saldo_anterior REAL, 
                    saldo_actual REAL)''')
    conn.commit()
    conn.close()


# Función para obtener los clientes de la base de datos
def obtener_clientes(busqueda=""):
    conn = sqlite3.connect('clientes.db')
    c = conn.cursor()
    c.execute("SELECT cliente_id, nombre FROM clientes WHERE nombre LIKE ? OR cliente_id LIKE ?", ('%' + busqueda + '%', '%' + busqueda + '%'))
    clientes = c.fetchall()
    conn.close()
    return clientes


# Ventana de login
def login_window():
    def login():
        usuario = entry_usuario.get()
        contrasena = entry_contrasena.get()

        if usuario == "Admin" and contrasena == "Admin2025":
            ventana_login.destroy()
            menu_principal()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    ventana_login = ctk.CTk()
    ventana_login.title("Login")
    ventana_login.geometry("400x300")

    ctk.CTkLabel(ventana_login, text="Usuario").pack(pady=10)
    entry_usuario = ctk.CTkEntry(ventana_login)
    entry_usuario.pack(pady=10, padx=20, fill="x")

    ctk.CTkLabel(ventana_login, text="Contraseña").pack(pady=10)
    entry_contrasena = ctk.CTkEntry(ventana_login, show="*")
    entry_contrasena.pack(pady=10, padx=20, fill="x")

    ctk.CTkButton(ventana_login, text="Ingresar", command=login).pack(pady=20)
    ventana_login.mainloop()


# Función para el menú principal después de iniciar sesión
def menu_principal():
    ventana_menu = ctk.CTk()
    ventana_menu.title("Menú Principal")
    ventana_menu.geometry("400x400")

    ctk.CTkButton(ventana_menu, text="Crear Perfil de Cliente", command=crear_perfil_cliente).pack(pady=20)
    ctk.CTkButton(ventana_menu, text="Añadir Activos", command=añadir_activos).pack(pady=20)
    ctk.CTkButton(ventana_menu, text="Añadir Pagos", command=añadir_pago).pack(pady=20)
    ctk.CTkButton(ventana_menu, text="Visualizar Pagos del Cliente", command=ver_pagos_cliente).pack(pady=20)
    ctk.CTkButton(ventana_menu, text="Salir", command=ventana_menu.quit).pack(pady=20)

    ventana_menu.mainloop()


# Función para crear perfil de cliente
def crear_perfil_cliente():
    ventana_cliente = ctk.CTk()
    ventana_cliente.title("Crear Perfil de Cliente")
    ventana_cliente.geometry("400x500")

    ctk.CTkLabel(ventana_cliente, text="Nombre Completo").pack(pady=10)
    entry_nombre = ctk.CTkEntry(ventana_cliente)
    entry_nombre.pack(pady=10, padx=20, fill="x")

    ctk.CTkLabel(ventana_cliente, text="DNI").pack(pady=10)
    entry_dni = ctk.CTkEntry(ventana_cliente)
    entry_dni.pack(pady=10, padx=20, fill="x")

    ctk.CTkLabel(ventana_cliente, text="RTN").pack(pady=10)
    entry_rtn = ctk.CTkEntry(ventana_cliente)
    entry_rtn.pack(pady=10, padx=20, fill="x")

    ctk.CTkLabel(ventana_cliente, text="Dirección").pack(pady=10)
    entry_direccion = ctk.CTkEntry(ventana_cliente)
    entry_direccion.pack(pady=10, padx=20, fill="x")

    ctk.CTkLabel(ventana_cliente, text="Número de Teléfono").pack(pady=10)
    entry_telefono = ctk.CTkEntry(ventana_cliente)
    entry_telefono.pack(pady=10, padx=20, fill="x")

    def guardar_perfil():
        nombre = entry_nombre.get()
        dni = entry_dni.get()
        rtn = entry_rtn.get()
        direccion = entry_direccion.get()
        telefono = entry_telefono.get()

        if not nombre or not dni or not rtn or not direccion or not telefono:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        conn = sqlite3.connect('clientes.db')
        c = conn.cursor()
        c.execute('''INSERT INTO clientes (nombre, dni, rtn, direccion, telefono) 
                     VALUES (?, ?, ?, ?, ?)''',
                  (nombre, dni, rtn, direccion, telefono))
        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Perfil del cliente creado exitosamente")
        ventana_cliente.destroy()

    ctk.CTkButton(ventana_cliente, text="Guardar Perfil", command=guardar_perfil).pack(pady=20)
    ventana_cliente.mainloop()


# Ventana para seleccionar cliente
def seleccionar_cliente(ventana, combo):
    clientes = obtener_clientes()
    combo.set("Seleccionar Cliente")
    combo["values"] = [f"{cliente[0]} - {cliente[1]}" for cliente in clientes]


# Función para añadir activos
def añadir_activos():
    ventana_activos = ctk.CTk()
    ventana_activos.title("Añadir Activos al Cliente")
    ventana_activos.geometry("500x700")  # Ajustamos el tamaño de la ventana para que se vea todo

    ctk.CTkLabel(ventana_activos, text="Buscar Cliente (ID o Nombre)").pack(pady=10)
    entry_buscar_cliente = ctk.CTkEntry(ventana_activos)
    entry_buscar_cliente.pack(pady=10, padx=20, fill="x")

    def buscar_cliente():
        criterio = entry_buscar_cliente.get()
        conn = sqlite3.connect("clientes.db")
        cursor = conn.cursor()
        cursor.execute("SELECT cliente_id, nombre FROM clientes WHERE cliente_id = ? OR nombre LIKE ?",
                       (criterio, f"%{criterio}%"))
        clientes = cursor.fetchall()
        conn.close()

        lista_clientes.configure(values=[f"{c[0]} - {c[1]}" for c in clientes])

    ctk.CTkButton(ventana_activos, text="Buscar", command=buscar_cliente).pack(pady=5)

    ctk.CTkLabel(ventana_activos, text="Seleccione Cliente:").pack(pady=10)
    lista_clientes = ctk.CTkComboBox(ventana_activos, values=[], width=300)
    lista_clientes.set("")
    lista_clientes.pack(pady=5)

    ctk.CTkLabel(ventana_activos, text="Número de Lote").pack(pady=10)
    entry_numero_lote = ctk.CTkEntry(ventana_activos)
    entry_numero_lote.pack(pady=10, padx=20, fill="x")

    ctk.CTkLabel(ventana_activos, text="Costo Total del Terreno").pack(pady=10)
    entry_costo_total = ctk.CTkEntry(ventana_activos)
    entry_costo_total.pack(pady=10, padx=20, fill="x")

    ctk.CTkLabel(ventana_activos, text="Prima").pack(pady=10)
    entry_prima = ctk.CTkEntry(ventana_activos)
    entry_prima.pack(pady=10, padx=20, fill="x")

    ctk.CTkLabel(ventana_activos, text="Medidas del Terreno").pack(pady=10)
    entry_medidas = ctk.CTkEntry(ventana_activos)
    entry_medidas.pack(pady=10, padx=20, fill="x")

    ctk.CTkLabel(ventana_activos, text="Plazo de Pagos (Años)").pack(pady=10)
    entry_plazo_anos = ctk.CTkEntry(ventana_activos)
    entry_plazo_anos.pack(pady=10, padx=20, fill="x")

    ctk.CTkLabel(ventana_activos, text="Fecha Inicial de Pago").pack(pady=10)
    entry_fecha_inicio_pago = ctk.CTkEntry(ventana_activos)
    entry_fecha_inicio_pago.pack(pady=10, padx=20, fill="x")

    def agregar_activo():
        # Obtener el cliente seleccionado
        cliente_seleccionado = lista_clientes.get()
        if cliente_seleccionado == "Seleccionar Cliente" or not cliente_seleccionado:
            messagebox.showerror("Error", "Por favor, seleccione un cliente.")
            return

        cliente_id = cliente_seleccionado.split(" - ")[0]  # Extraer ID del cliente

        numero_lote = entry_numero_lote.get()
        costo_total = float(entry_costo_total.get())
        prima = float(entry_prima.get())
        medidas = entry_medidas.get()
        plazo_anos = int(entry_plazo_anos.get())
        fecha_inicio_pago = entry_fecha_inicio_pago.get()

        total_a_financiar = costo_total - prima
        desglose_cuotas = total_a_financiar / (plazo_anos * 12)

        conn = sqlite3.connect('clientes.db')
        c = conn.cursor()
        c.execute('''INSERT INTO activos (cliente_id, numero_lote, costo_total, prima, medidas, plazo_anos, 
                     fecha_inicio_pago, total_a_financiar, desglose_cuotas) 
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (cliente_id, numero_lote, costo_total, prima, medidas, plazo_anos, fecha_inicio_pago,
                   total_a_financiar, desglose_cuotas))
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Activo añadido exitosamente")
        ventana_activos.destroy()

    ctk.CTkButton(ventana_activos, text="Añadir Activo", command=agregar_activo).pack(pady=20)
    ventana_activos.mainloop()

# Función para añadir pago
def añadir_pago():
    ventana_pago = ctk.CTk()
    ventana_pago.title("Añadir Pago al Cliente")
    ventana_pago.geometry("400x600")

    ctk.CTkLabel(ventana_pago, text="Seleccionar Cliente (ID o Nombre)").pack(pady=10)

    combo_cliente = ctk.CTkComboBox(ventana_pago, state="normal")
    combo_cliente.pack(pady=10, padx=20, fill="x")

    seleccionar_cliente(ventana_pago, combo_cliente)  # Llenamos el combo con los clientes disponibles

    ctk.CTkLabel(ventana_pago, text="Número de Cuota").pack(pady=10)
    entry_cuota = ctk.CTkEntry(ventana_pago)
    entry_cuota.pack(pady=10, padx=20, fill="x")

    ctk.CTkLabel(ventana_pago, text="Fecha de Pago").pack(pady=10)
    entry_fecha_pago = ctk.CTkEntry(ventana_pago)
    entry_fecha_pago.pack(pady=10, padx=20, fill="x")

    ctk.CTkLabel(ventana_pago, text="Cantidad Abonada").pack(pady=10)
    entry_cantidad_abonada = ctk.CTkEntry(ventana_pago)
    entry_cantidad_abonada.pack(pady=10, padx=20, fill="x")

    ctk.CTkLabel(ventana_pago, text="Estado del Pago").pack(pady=10)
    entry_estado_pago = ctk.CTkEntry(ventana_pago)
    entry_estado_pago.pack(pady=10, padx=20, fill="x")

    def agregar_pago():
        # Obtener el cliente seleccionado
        cliente_seleccionado = combo_cliente.get()
        if cliente_seleccionado == "Seleccionar Cliente":
            messagebox.showerror("Error", "Por favor, seleccione un cliente.")
            return

        cliente_id = cliente_seleccionado.split(" - ")[0]  # Extraer ID del cliente
        cuota = int(entry_cuota.get())
        fecha_pago = entry_fecha_pago.get()
        cantidad_abonada = float(entry_cantidad_abonada.get())
        estado_pago = entry_estado_pago.get()

        conn = sqlite3.connect('clientes.db')
        c = conn.cursor()
        c.execute('''INSERT INTO pagos (cliente_id, cuota, fecha_pago, cantidad_abonada, estado_pago) 
                     VALUES (?, ?, ?, ?, ?)''',
                  (cliente_id, cuota, fecha_pago, cantidad_abonada, estado_pago))
        conn.commit()
        conn.close()
        messagebox.showinfo("Éxito", "Pago añadido exitosamente")
        ventana_pago.destroy()

    ctk.CTkButton(ventana_pago, text="Añadir Pago", command=agregar_pago).pack(pady=20)
    ventana_pago.mainloop()


# Función para ver pagos del cliente
def ver_pagos_cliente():
    ventana_ver_pagos = ctk.CTk()
    ventana_ver_pagos.title("Visualizar Pagos del Cliente")
    ventana_ver_pagos.geometry("600x400")

    ctk.CTkLabel(ventana_ver_pagos, text="Seleccionar Cliente por ID o Nombre").pack(pady=10)

    combo_cliente = ctk.CTkComboBox(ventana_ver_pagos, state="normal")
    combo_cliente.pack(pady=10, padx=20, fill="x")

    seleccionar_cliente(ventana_ver_pagos, combo_cliente)  # Llenamos el combo con los clientes disponibles

    def mostrar_pagos():
        cliente_seleccionado = combo_cliente.get()
        if cliente_seleccionado == "Seleccionar Cliente":
            messagebox.showerror("Error", "Por favor, seleccione un cliente.")
            return

        cliente_id = cliente_seleccionado.split(" - ")[0]  # Extraer ID del cliente

        conn = sqlite3.connect('clientes.db')
        c = conn.cursor()
        c.execute('''SELECT * FROM pagos WHERE cliente_id = ?''', (cliente_id,))
        pagos = c.fetchall()

        # Crear tabla para mostrar pagos
        for widget in ventana_ver_pagos.winfo_children():
            widget.destroy()

        tree = ttk.Treeview(ventana_ver_pagos, columns=(
        "Cuota", "Fecha de Pago", "Cantidad Abonada", "Estado del Pago", "Saldo Anterior", "Saldo Actual"),
                            show="headings")
        tree.pack(pady=20)

        for col in tree["columns"]:
            tree.heading(col, text=col)

        for pago in pagos:
            tree.insert("", "end", values=pago)

    ctk.CTkButton(ventana_ver_pagos, text="Mostrar Pagos", command=mostrar_pagos).pack(pady=20)
    ventana_ver_pagos.mainloop()


# Crear base de datos
create_db()

# Llamar a la ventana de login
login_window()
