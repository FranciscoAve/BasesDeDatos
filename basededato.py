import tkinter as tk
from tkinter import ttk, messagebox
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
            password="sucontraseña >:c", #la contraseña de uds
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
        ttk.Label(self.frame, text="Código:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(self.frame, textvariable=self.codigo_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Fecha (YYYY-MM-DD):").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(self.frame, textvariable=self.fecha_var).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Ubicación:").grid(row=2, column=0, sticky=tk.W)
        ttk.Entry(self.frame, textvariable=self.ubicacion_var).grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Temática:").grid(row=3, column=0, sticky=tk.W)
        ttk.Entry(self.frame, textvariable=self.tematica_var).grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Descripción:").grid(row=4, column=0, sticky=tk.W)
        ttk.Entry(self.frame, textvariable=self.descripcion_var).grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(self.frame, text="Valor Total:").grid(row=5, column=0, sticky=tk.W)
        ttk.Entry(self.frame, textvariable=self.valor_var).grid(row=5, column=1, padx=5, pady=5)

        # Botones CRUD
        ttk.Button(self.frame, text="Crear", command=self.crear_evento).grid(row=6, column=0, pady=10)
        ttk.Button(self.frame, text="Buscar", command=self.buscar_evento).grid(row=6, column=1, pady=10)
        ttk.Button(self.frame, text="Actualizar", command=self.actualizar_evento).grid(row=6, column=2, pady=10)
        ttk.Button(self.frame, text="Eliminar", command=self.eliminar_evento).grid(row=6, column=3, pady=10)

        # Botones de control de transacción
        ttk.Button(self.frame, text="Guardar Cambios", command=self.commit_cambios,
                   style='Accent.TButton').grid(row=7, column=0, columnspan=2, pady=10)
        ttk.Button(self.frame, text="Descartar Cambios", command=self.descartar_cambios,
                   style='Accent.TButton').grid(row=7, column=2, columnspan=2, pady=10)

        # Tabla de eventos
        self.tree = ttk.Treeview(self.frame,
                                 columns=("Código", "Fecha", "Ubicación", "Temática", "Descripción", "Valor"),
                                 show="headings")
        self.tree.grid(row=8, column=0, columnspan=4, pady=10)

        # Configurar columnas
        self.tree.heading("Código", text="Código")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Ubicación", text="Ubicación")
        self.tree.heading("Temática", text="Temática")
        self.tree.heading("Descripción", text="Descripción")
        self.tree.heading("Valor", text="Valor Total")

        # Etiqueta de modo temporal
        ttk.Label(self.frame, text="MODO TEMPORAL - Los cambios no se guardarán hasta que presiones 'Guardar Cambios'",
                  foreground='red').grid(row=9, column=0, columnspan=4)

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

    def actualizar_tabla(self):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Obtener y mostrar datos
        self.cursor.execute("SELECT * FROM Evento")
        for evento in self.cursor.fetchall():
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
            evento = self.cursor.fetchone()
            if evento:
                self.codigo_var.set(evento[0])
                self.fecha_var.set(evento[1])
                self.ubicacion_var.set(evento[2])
                self.tematica_var.set(evento[3])
                self.descripcion_var.set(evento[4])
                self.valor_var.set(evento[5])
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