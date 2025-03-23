from tkinter import * 
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

class Ventas(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre)
        self.widgets()
    
    def widgets(self):
        #PRIMER RECTANGULO
        label_frame = tk.LabelFrame(self, font="sans 12 bold", bg="gray")
        label_frame.place(x=25, y=30, width=1045, height=180)
        
        label_cliente = tk.Label(label_frame, text="Cliente: ", font="sans 14 bold", bg="gray")
        label_cliente.place(x=10, y=11)
        self.entry_cliente = ttk.Combobox(label_frame, font="sans 14 bold")
        self.entry_cliente.place(x=120, y=8, width=260, height=40)
        
        #SELECCIONAR PRODUCTO
        label_producto = tk.Label(label_frame, text="Producto: ", font="sans 14 bold", bg="gray")
        label_producto.place(x=10, y=70)
        self.entry_producto = ttk.Combobox(label_frame, font="sans 14 bold")
        self.entry_producto.place(x=120, y=60, width=260, height=40)
        
        #LABEL CANTIDAD
        label_cantidad = tk.Label(label_frame, text="Cantidad: ", font="sans 14 bold", bg="gray")
        label_cantidad.place(x=500, y=11)
        self.entry_cantidad = ttk.Entry(label_frame, font="sans 14 bold")
        self.entry_cantidad.place(x=610, y=8, width=100, height=40)
        
        #CANTIDAD STOCK
        self.label_stock = tk.Label(label_frame, text="Stock: ", font="sans 14 bold", bg="gray")
        self.label_stock.place(x=500, y=70)
        
        #FACTURA COMPRA
        label_factura = tk.Label(label_frame, text="Factura", font="sans 14 bold", bg="gray")
        label_factura.place(x=750, y=11)
        
        #BOTONES
        boton_agregar = tk.Button(label_frame, text="Agregar articulo", font="sans 14 bold")
        boton_agregar.place(x=90, y=120, width=200, height=40)
        
        boton_eliminar = tk.Button(label_frame, text="Eliminar articulo", font="sans 14 bold")
        boton_eliminar.place(x=310, y=120, width=200, height=40)
        
        boton_editar = tk.Button(label_frame, text="Editar articulo", font="sans 14 bold")
        boton_editar.place(x=530, y=120, width=200, height=40)
        
        boton_limpiar = tk.Button(label_frame, text="Limpiar articulo", font="sans 14 bold")
        boton_limpiar.place(x=750, y=120, width=200, height=40)
        
        #SEGUNDO RECTANGULO (BLANCO)
        tre_frame = tk.Frame(self, bg="white")
        tre_frame.place(x=70, y=220, width=980, height=300)
        
        scroll_y = ttk.Scrollbar(tre_frame)
        scroll_y.pack(side=RIGHT, fill=Y)
        '''VERTICAL👆|HORIZONTAL👇'''
        scroll_x = ttk.Scrollbar(tre_frame, orient=HORIZONTAL)
        scroll_x.pack(side=BOTTOM, fill=X)
        
        
        self.tre = ttk.Treeview(tre_frame, yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set, 
                                height=40, columns=("Factura", "Cliente", "Producto", "Precio", "Cantidad", "Total"), show="headings")
        self.tre.pack(expand=True, fill=BOTH)
        
        scroll_y.config(command=self.tre.yview)
        scroll_x.config(command=self.tre.xview)
        
        #CONFIGURAR HEADING
        self.tre.heading("Factura", text="Factura")
        self.tre.heading("Cliente", text="Cliente")
        self.tre.heading("Producto", text="Producto")
        self.tre.heading("Precio", text="Precio")
        self.tre.heading("Cantidad", text="Cantidad")
        self.tre.heading("Total", text="Total")
        
        #CONFIGURAR COLUMNAS
        self.tre.column("Factura", width=70, anchor="center")
        self.tre.column("Cliente", width=250, anchor="center")
        self.tre.column("Producto", width=250, anchor="center")
        self.tre.column("Precio", width=120, anchor="center")
        self.tre.column("Cantidad", width=120, anchor="center")
        self.tre.column("Total", width=150, anchor="center")
        
        #LABELS PRECIO
        self.label_precio_total = tk.Label(self, text="Precio a pagar: $ 0", bg="gray", font="sans 18 bold")
        self.label_precio_total.place(x=680, y=550)
        
        #BOTONES PAGOS
        boton_pagar = tk.Button(self, text="Pagar", font="sans 14 bold")
        boton_pagar.place(x=70, y=550, width=180, height=40)

        boton_ver_ventas = tk.Button(self, text="Ver ventas realizadas", font="sans 14 bold")
        boton_ver_ventas.place(x=290, y=550, width=280, height=40)
        
        