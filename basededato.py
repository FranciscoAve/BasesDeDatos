import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from datetime import datetime



class EventosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Eventos (Modo Temporal)")

        # Configuración de la conexión con autocommit=False para manejar transacciones
        self.conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",  # la contraseña de uds
            database="g07",
            autocommit=False
        )
        self.cursor = self.conexion.cursor()

        # Iniciar transacción
        self.cursor.execute("START TRANSACTION")

        # Frame principal
        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Variables para los campos
        self.codigo_var = tk.StringVar()
        self.fecha_var = tk.StringVar()
        self.ubicacion_var = tk.StringVar()
        self.tematica_var = tk.StringVar()
        self.descripcion_var = tk.StringVar()
        self.valor_var = tk.StringVar()

        # Crear campos de entrada
        # Crear campos de entrada
        ttk.Label(self.frame, text="Código:", font=("Times New Roman", 12, "bold")).grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(self.frame, textvariable=self.codigo_var, font=("Times New Roman", 12), width=20).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Fecha (YYYY-MM-DD):", font=("Times New Roman", 12, "bold")).grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(self.frame, textvariable=self.fecha_var, font=("Times New Roman", 12), width=20).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Ubicación:", font=("Times New Roman", 12, "bold")).grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(self.frame, textvariable=self.ubicacion_var, font=("Times New Roman", 12), width=20).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Temática:", font=("Times New Roman", 12, "bold")).grid(row=3, column=0, sticky=tk.W)
        ttk.Entry(self.frame, textvariable=self.tematica_var, font=("Times New Roman", 12), width=20).grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Descripción:", font=("Times New Roman", 12, "bold")).grid(row=4, column=0, sticky=tk.W)
        ttk.Entry(self.frame, textvariable=self.descripcion_var, font=("Times New Roman", 12), width=20).grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Valor Total:", font=("Times New Roman", 12, "bold")).grid(row=5, column=0, sticky=tk.W)
        ttk.Entry(self.frame, textvariable=self.valor_var, font=("Times New Roman", 12), width=20).grid(row=5, column=1, padx=5, pady=5)


        # Botones CRUD alineados a la derecha de los campos de entrada
        self.create_button = ttk.Button(self.frame, text="Crear", command=self.crear_evento, style="TButton")
        self.create_button.grid(row=0, column=2, padx=10, pady=5)

        self.search_button = ttk.Button(self.frame, text="Buscar", command=self.buscar_evento, style="TButton")
        self.search_button.grid(row=1, column=2, padx=10, pady=5)

        self.update_button = ttk.Button(self.frame, text="Actualizar", command=self.actualizar_evento, style="TButton")
        self.update_button.grid(row=2, column=2, padx=10, pady=5)

        self.delete_button = ttk.Button(self.frame, text="Eliminar", command=self.eliminar_evento, style="TButton")
        self.delete_button.grid(row=3, column=2, padx=10, pady=5)

        # Estilo de los botones
        style = ttk.Style()
        style.configure("TButton",
                        font=("Arial", 10, "bold"),
                        relief="raised",
                        padding=10,
                        width=12)
        style.configure("TButton:hover",
                        background="#4CAF50",
                        foreground="white")
        style.configure("TButton:active",
                        background="#45a049",
                        foreground="white")

        # Botones de control de transacción
        self.save_button = ttk.Button(self.frame, text="Guardar Cambios", command=self.commit_cambios,
                                      style='Accent.TButton')
        self.save_button.grid(row=7, column=0, columnspan=2, pady=10, sticky="ew")

        self.discard_button = ttk.Button(self.frame, text="Descartar Cambios", command=self.descartar_cambios,
                                         style='Accent.TButton')
        self.discard_button.grid(row=7, column=2, columnspan=2, pady=10, sticky="ew")

        # Estilo de los botones de acción
        style.configure("Accent.TButton",
                        font=("Arial", 12, "bold"),
                        background="#008CBA",
                        foreground="white",
                        padding=15)
        style.map("Accent.TButton",
                  background=[("active", "#006f8f")])

        # Tabla de eventos
        self.tree = ttk.Treeview(self.frame,
                                 columns=("Código", "Fecha", "Ubicación", "Temática", "Descripción", "Valor"),
                                 show="headings")
        self.tree.grid(row=8, column=0, columnspan=4, pady=10, sticky="nsew")

        # Configurar columnas de la tabla
        self.tree.heading("Código", text="Código")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Ubicación", text="Ubicación")
        self.tree.heading("Temática", text="Temática")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.heading("Valor", text="Valor Total")

        # Etiqueta de modo temporal
        ttk.Label(self.frame, text="MODO TEMPORAL - Los cambios no se guardarán hasta que presiones 'Guardar Cambios'",
                  foreground='red', font=("Arial", 10, "italic")).grid(row=9, column=0, columnspan=4)

        # Cargar datos iniciales
        self.actualizar_tabla()

        # Bind para selección en la tabla
        self.tree.bind('<<TreeviewSelect>>', self.item_seleccionado)

        # Bind para el cierre de la ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        """Maneja el cierre de la ventana"""
        if messagebox.askyesno("Confirmar", "¿Deseas guardar los cambios antes de salir?"):
            self.commit_cambios()
        else:
            self.descartar_cambios()
        self.root.destroy()

    def commit_cambios(self):
        """Guarda los cambios en la base de datos"""
        try:
            self.conexion.commit()
            messagebox.showinfo("Éxito", "Cambios guardados correctamente")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al guardar cambios: {err}")

    def descartar_cambios(self):
        """Descarta todos los cambios realizados"""
        try:
            self.conexion.rollback()
            self.actualizar_tabla()
            messagebox.showinfo("Éxito", "Cambios descartados")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al descartar cambios: {err}")

    def limpiar_campos(self):
        self.codigo_var.set("")
        self.fecha_var.set("")
        self.ubicacion_var.set("")
        self.tematica_var.set("")
        self.descripcion_var.set("")
        self.valor_var.set("")

    def actualizar_tabla(self, eventos=None):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Si no se pasan eventos, traer todos
        if eventos is None:
            self.cursor.execute("SELECT * FROM Evento")
            eventos = self.cursor.fetchall()

        # Mostrar los datos
        for evento in eventos:
            self.tree.insert("", "end", values=evento)

    def crear_evento(self):
        try:
            sql = """INSERT INTO Evento (codigo, fecha, ubicacion, tematica, descripcion, valorTotal) 
                     VALUES (%s, %s, %s, %s, %s, %s)"""
            valores = (
                self.codigo_var.get(),
                self.fecha_var.get(),
                self.ubicacion_var.get(),
                self.tematica_var.get(),
                self.descripcion_var.get(),
                float(self.valor_var.get())
            )
            self.cursor.execute(sql, valores)
            messagebox.showinfo("Éxito", "Evento creado (pendiente de guardar)")
            self.limpiar_campos()
            self.actualizar_tabla()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al crear evento: {err}")

    def buscar_evento(self):
        codigo = self.codigo_var.get()
        try:
            self.cursor.execute("SELECT * FROM Evento WHERE codigo = %s", (codigo,))
            eventos = self.cursor.fetchall()
            if eventos:
                self.actualizar_tabla(eventos)  # Solo mostrar resultados de la búsqueda
            else:
                messagebox.showinfo("Búsqueda", "No se encontró el evento")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al buscar evento: {err}")

    def actualizar_evento(self):
        try:
            sql = """UPDATE Evento SET fecha = %s, ubicacion = %s, tematica = %s, 
                     descripcion = %s, valorTotal = %s WHERE codigo = %s"""
            valores = (
                self.fecha_var.get(),
                self.ubicacion_var.get(),
                self.tematica_var.get(),
                self.descripcion_var.get(),
                float(self.valor_var.get()),
                self.codigo_var.get()
            )
            self.cursor.execute(sql, valores)
            messagebox.showinfo("Éxito", "Evento actualizado (pendiente de guardar)")
            self.actualizar_tabla()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al actualizar evento: {err}")

    def eliminar_evento(self):
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este evento?"):
            try:
                self.cursor.execute("DELETE FROM Evento WHERE codigo = %s", (self.codigo_var.get(),))
                messagebox.showinfo("Éxito", "Evento eliminado (pendiente de guardar)")
                self.limpiar_campos()
                self.actualizar_tabla()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al eliminar evento: {err}")

    def item_seleccionado(self, event):
        seleccion = self.tree.selection()
        if seleccion:
            item = self.tree.item(seleccion[0])
            valores = item['values']
            self.codigo_var.set(valores[0])
            self.fecha_var.set(valores[1])
            self.ubicacion_var.set(valores[2])
            self.tematica_var.set(valores[3])
            self.descripcion_var.set(valores[4])
            self.valor_var.set(valores[5])


if __name__ == "__main__":
    root = tk.Tk()
    app = EventosApp(root)
    root.mainloop()
