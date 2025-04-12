from tkinter import * 
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class Pedidos(tk.Frame):
    db_name = 'database.db'
    
    def __init__(self, padre):
        super().__init__(padre)
        self.widgets()
    
    def widgets(self):
        self.label_frame = tk.LabelFrame(self, text="Pedidos", font="sans 20 bold", bg= "gray")
        self.label_frame.place(x=20, y=20, width=250, height=560)
        
        label_nombre = tk.Label(self.label_frame, text="Nombre: ", font="sans 14 bold", bg="gray")
        label_nombre.place(x=10, y=20)
        self.nombre = ttk.Entry(self.label_frame, font="sans 14 bold")
        self.nombre.place(x=10, y=50, width=220, height=40)
        
        label_celular = tk.Label(self.label_frame, text="Celular: ", font="sans 14 bold", bg="gray")
        label_celular.place(x=10, y=100)
        self.celular = ttk.Entry(self.label_frame, font="sans 14 bold")
        self.celular.place(x=10, y=130, width=220, height=40)
        
        label_ciudad = tk.Label(self.label_frame, text="Ciudad: ", font="sans 14 bold", bg="gray")
        label_ciudad.place(x=10, y=180)
        self.ciudad = ttk.Entry(self.label_frame, font="sans 14 bold")
        self.ciudad.place(x=10, y=210, width=220, height=40)
        
        label_fecha = tk.Label(self.label_frame, text="Fecha: ", font="sans 14 bold", bg="gray")
        label_fecha.place(x=10, y=260)
        self.fecha = ttk.Entry(self.label_frame, font="sans 14 bold")
        self.fecha.place(x=10, y=290, width=220, height=40)
        
        #BOTON FORMULARIO
        boton_ingresar = Button(self.label_frame, fg="Black", text="Agregar pedido", font="sans 16 bold", relief="solid")
        boton_ingresar.place(x=10, y=420, width=220, height=40)
        
        boton_editar = Button(self.label_frame, fg="Black", text="Editar", font="sans 16 bold", relief="solid")
        boton_editar.place(x=10, y=470, width=220, height=40)
        
        #TREE
        tre_frame = Frame(self, bg="white")
        tre_frame.place(x=280, y=20, width=800, height=560)
        
        scrol_y = ttk.Scrollbar(tre_frame)
        scrol_y.pack(side= RIGHT, fill=Y)
        
        scrol_x = ttk.Scrollbar(tre_frame, orient=HORIZONTAL)
        scrol_x.pack(side= BOTTOM, fill=X)
        
        self.tre = ttk.Treeview(tre_frame, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set, height=40, columns=("ID", "Nombre", "Celular", "Ciudad", "Fecha"), show="headings")
        self.tre.pack(expand=True, fill=BOTH)
        
        scrol_y.config(command=self.tre.yview)
        scrol_x.config(command=self.tre.xview)
        
        
        self.tre.heading("ID", text="ID")
        self.tre.heading("Nombre", text="Nombre")
        self.tre.heading("Celular", text="Celular")
        self.tre.heading("Ciudad", text="Ciudad")
        self.tre.heading("Fecha", text="Fecha")
        
        self.tre.column("ID", width=50, anchor="center")
        self.tre.column("Nombre", width=150, anchor="center")
        self.tre.column("Celular", width=120, anchor="center")
        self.tre.column("Ciudad", width=200, anchor="center")
        self.tre.column("Fecha", width=200, anchor="center")
    
    def validacion_datos(self):
        if not self.nombre.get() or not self.celular.get() or not self.ciudad.get() or not self.fecha.get():
            messagebox.showerror("Error", "Llene todos los campos")
            return False
        return True
    
    def registrar_pedidop(self):
        if not self.validacion_datos():
            return
        
        nombre = self.nombre.get()
        celular = self.celular.get()
        ciudad = self.ciudad.get()
        fecha = self.fecha.get()
        
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO clientes (nombre, celular, ciudad, correo) VALUES (?,?,?,?)", (nombre, celular, ciudad, fecha))
                conn.commit()
                
                messagebox.showinfo("Exito", "Pedido agregado con exito")
                
                self.limpiar_treeview()
                self.limpiar_campos()
                self.cargar_pedidos()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al registrar el cliente: {e}")
    
    def cargar_pedidos(self):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM pedidos")
                filas = cursor.fetchall()
                
                for fila in filas:
                    self.tre.insert("", "end", values= fila)
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al cargar el pedido: {e}")
    
    def limpiar_treeview(self):
        for i in self.tre.get_children():
            self.tre.delete(i)

    def limpiar_campos(self):
        self.nombre.delete(0, END)
        self.ciudad.delete(0, END)
        self.ciudad.delete(0, END)
        self.fecha.delete(0, END)
    
    def editar_pedido(self):
        if not self.tre.selection():
            messagebox.showerror("Error", "Seleccione un pedido a modificar")
            return

        item = self.tre.selection()[0]
        id_pedido = self.tre.item(item, "values")[0]
        
        #VALOR EN LA DATABASE
        nombre_actual = self.tre.item(item, "values")[1]
        celular_actual = self.tre.item(item, "values")[2]
        ciudad_actual = self.tre.item(item, "values")[3]
        fecha_actual = self.tre.item(item, "values")[4]
        
        top_editar = Toplevel(self)
        top_editar.title("Modificar cliente")
        top_editar.geometry("400x400+400+50")
        top_editar.config(bg="gray")
        top_editar.resizable(False, False)
        top_editar.transient(self.master)
        top_editar.grab_set()
        top_editar.focus_set()
        top_editar.lift()
        
        #DATOS DE LA COLUMNA
        tk.Label(top_editar, text="Nombre", font="sans 14 bold", bg="gray").grid(row=0, column=0, padx=10, pady=5)
        nombre_new = tk.Entry(top_editar, font="sans 14 bold")
        nombre_new.insert(0, nombre_actual)
        nombre_new.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(top_editar, text="Celular", font="sans 14 bold", bg="gray").grid(row=1, column=0, padx=10, pady=5)
        celular_new = tk.Entry(top_editar, font="sans 14 bold")
        celular_new.insert(0, celular_actual)
        celular_new.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(top_editar, text="Ciudad", font="sans 14 bold", bg="gray").grid(row=2, column=0, padx=10, pady=5)
        ciudad_new = tk.Entry(top_editar, font="sans 14 bold")
        ciudad_new.insert(0, ciudad_actual)
        ciudad_new.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(top_editar, text="Fecha", font="sans 14 bold", bg="gray").grid(row=3, column=0, padx=10, pady=5)
        fecha_new = tk.Entry(top_editar, font="sans 14 bold")
        fecha_new.insert(0, fecha_actual)
        fecha_new.grid(row=3, column=1, padx=10, pady=5)
        
        def guargar_edicion():
            nuevo_nombre = nombre_new.get()
            nuevo_celular = celular_new.get()
            nuevo_ciudad = ciudad_new.get()
            nueva_fecha = fecha_new.get()
            
            try:
                with sqlite3.connect(self.db_name) as conn:
                    cursor = conn.cursor()
                    cursor.execute("""UPDATE clientes SET nombre = ?, celular = ?, ciudad = ?, fecha = ? WHERE ID = ?""", (nuevo_nombre, nuevo_celular, nuevo_ciudad, nueva_fecha, id_pedido))
                    conn.commit()
                    messagebox.showinfo("Exito", "Pedido modificado con exito")
                    self.limpiar_treeview()
                    self.cargar_pedidos()
                    top_editar.destroy()
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"Error al moficar el cliente: {e}")

        boton_guardar = tk.Button(top_editar, text="Guardar cambios", command=guargar_edicion, font="sans 14 bold")
        boton_guardar.grid(row= 4, column=0, columnspan=2, padx=20)

