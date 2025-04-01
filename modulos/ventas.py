from tkinter import * 
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
import datetime
import threading
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
import sys
import os

class Ventas(tk.Frame):
    db_name = "database.db"
    
    def __init__(self, padre):
        super().__init__(padre)
        self.numero_factura = self.obtener_numero_factura_actual()
        self.productos_seleccionados = []
        self.widgets()
        self.cargar_productos()
        self.cargar_clientes()
        self.timer_producto = None
    
    def obtener_numero_factura_actual(self):
        #BASE DE DATOS
        try:
            with sqlite3.connect(self.db_name) as conn:
                c = conn.cursor()
                c.execute("SELECT MAX(factura) FROM ventas") # Obtiene el número de factura más alto de la tabla 'ventas'
                last_invoice_number = c.fetchone()[0] # Extrae el número de factura máximo del resultado
                # Devuelve el siguiente número de factura, o 1 si no hay facturas
                return last_invoice_number + 1 if last_invoice_number is not None else 1 
        except sqlite3.Error as e:
            print("Error obteniendo el numero de factura actual", e)
            return 1
    
    def cargar_productos(self):
        try:
            with sqlite3.connect(self.db_name) as conn:
                c = conn.cursor()
                c.execute("SELECT articulo FROM articulos")
                #Crea una lista que contiene el primer elemento de cada tupla de la base de datos.
                self.products = [product[0] for product in c.fetchall()]
                self.entry_producto["values"] = self.products
        except sqlite3.Error as e:
            print("Error cargando productos: ", e)
    
    def fitrar_productos(self, event = None):
        if self.timer_producto:
            self.timer_producto.cancel()
        self.timer_producto = threading.Timer(0.5, self._filter_products)
        self.timer_producto.start()
    
    def _filter_products(self):
        typed = self.entry_producto.get()

        if typed == '':
            data = self.products
        else:
            data = [item for item in self.products if typed.lower() in item.lower()]
        
        if data:
            self.entry_producto['values'] == data
            self.entry_producto.event_generate('<Down>')
        else:
            self.entry_producto['values'] = ['No se encontraron resultados']
            self.entry_producto.event_generate('<Down>')
            self.entry_producto.delete(0, tk.END)
    
    def agregar_articulo(self):
        cliente = self.entry_cliente.get()
        producto = self.entry_producto.get()
        cantidad = self.entry_cantidad.get()
        
        if not cliente:
            messagebox.showerror("Error", "Por favor seleccione un cliente.")
            
        if not producto:
            messagebox.showerror("Error", "Por favor seleccione un producto.")
            
        if not cantidad.isdigit() or int(cantidad) < 1:
            messagebox.showerror("Error", "Por favor ingrese una cantidad valida.")
            return

        cantidad = int(cantidad)
        # Obtiene el valor ingresado en 'self.entry_cliente' y lo asigna a la variable 'cliente'.
        cliente = self.entry_cliente.get()
        
        try:
            with sqlite3.connect(self.db_name) as conn:
                c = conn.cursor()
                # Ejecuta una consulta que selecciona las columnas 'precio' y 'stock' de la tabla 'articulos' donde la columna 'articulo' coincide con el valor de la variable 'producto'
                c.execute("SELECT precio, stock FROM articulos WHERE articulo=?", (producto,))
                resultado = c.fetchone()
                
                if resultado is None:
                    messagebox.showerror("Error", "Producto no encontrado")
                    producto
                    
                precio, stock = resultado
                
                #LO QUE VENDO TIENE QUE SER MENOR A LO QUE HAY EN STOCK
                if cantidad > stock:
                    messagebox.showerror("Error", f"Stock insuficiente, solo hay {stock} unidades")
                
                total = precio * cantidad
                #El .0f para que no haya decimales
                total_cop = "{:,.0f}".format(total)    
                
                self.tre.insert("", "end", values=(self.numero_factura, cliente, producto, "{:,.0f}".format(precio), cantidad, total_cop))
                self.productos_seleccionados.append((self.numero_factura, cliente, producto, precio, cantidad, total_cop))
                
                #RESETEA EL COMBOBOX PARA QUE NO QUEDE ESCRITO EL PRODUCTO
                self.entry_producto.set('')
                self.entry_cantidad.delete(0, 'end')
        except sqlite3.Error as e:
            print("Error al agregar articulo", e)
        
        self.calcular_precio_total()
    
    '''
    FALTA COMENTARIO
    '''
    def calcular_precio_total(self):
        total_pagar = sum(float(str(self.tre.item(item)["values"][-1]).replace(" ", "").replace(",", " "))for item in self.tre.get_children())
        
        total_pagar_cop = "{}".format(total_pagar)
        self.label_precio_total.config(text=f"Precio a pagar: $ {total_pagar_cop}")

    def actualizar_stock (self, event=  None):
        producto_seleccionado = self.entry_producto.get()

        try:
            with sqlite3.connect(self.db_name) as conn:
                c = conn.cursor()
                c.execute("SELECT stock FROM articulos WHERE articulo=?", (producto_seleccionado,))
                stock = c.fetchone()[0]
                self.label_stock.config(text=f"Stock: {stock}")
        except sqlite3.Error as e:
            print("Error al obtener el stock del producto", e)
    
    def realizar_pago(self):
        if not self.tre.get_children():
            messagebox.showerror("Error", "No hay productos seleccionados para el pago")
            return
        
        total_ventas = sum(float(item[5].replace(" ", "").replace(",", ""))for item in self.productos_seleccionados)

        total_formateado = "{:,.0f}".format(total_ventas)

        ventana_pago = tk.Toplevel(self)
        ventana_pago.title("Realizar pago")
        ventana_pago.geometry("400x400+450+80")
        ventana_pago.config(bg= "gray")
        ventana_pago.resizable(False, False)
        ventana_pago.transient(self.master)
        ventana_pago.grab_set()
        ventana_pago.focus_set()
        ventana_pago.lift()

        label_titulo = tk.Label(ventana_pago, text="Realizar pago", font="sans 30 bold", bg="gray")
        label_titulo.place(x=70, y=10)

        label_total = tk.Label(ventana_pago, text=f"Total a pagar: {total_formateado}", font="sans 14 bold", bg="gray")
        label_total.place(x=80, y=100)

        label_monto = tk.Label(ventana_pago, text="Ingrese el monto pagado", font="sans 14 bold", bg="gray")
        label_monto.place(x=70, y=160)

        entry_monto = ttk.Entry(ventana_pago, font="sans 14 bold")
        entry_monto.place(x=80, y=210, width=240, height=40)

        button_confirmar_pago = tk.Button(ventana_pago, text="Confirmar pago", font="sans 14 bold", command=lambda: self.procesar_pago(entry_monto.get(), ventana_pago, total_ventas))
        button_confirmar_pago.place(x=80, y=270, width=240, height=40)

    def procesar_pago(self, cantidad_pagada, ventana_pago, total_ventas):
        cantidad_pagada = float(cantidad_pagada)
        cliente = self.entry_cliente.get()

        if cantidad_pagada < total_ventas:
            messagebox.showerror("Error", "La cantidad pagada es insuficiente.")
            return
        
        cambio = cantidad_pagada - total_ventas

        total_formateado = "{:,.0f}".format(total_ventas)

        mensaje= f"Total: {total_formateado} \nCantidad pagada: {cantidad_pagada:,.0f} \nCambio: {cambio:,.0f}"
        messagebox.showinfo("Pago realizado", mensaje)

        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            
            fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y")
            hora_actual = datetime.datetime.now().strftime("%H:%M:%S")

            for item in self.productos_seleccionados:
                factura, cliente, producto, precio, cantidad, total = item
                c.execute("INSERT INTO ventas (factura, cliente,  articulo, precio, cantidad, total, fecha, hora) VALUES (?,?,?,?,?,?,?,?)", (factura, cliente, producto, precio, cantidad, total.replace(" ", "").replace(",", ""), fecha_actual, hora_actual))
                
                c.execute("UPDATE articulos SET stock = stock - ? WHERE articulo = ?", (cantidad, producto))

            conn.commit()

            self.facturas_pdf(total_ventas, cliente)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al registrar la venta: {e}")
        
        self.numero_factura += 1
        self.label_numero_factura.config(text=str(self.numero_factura))

        self.productos_seleccionados = []
        self.limpiar_campos()

        ventana_pago.destroy()

    def limpiar_campos(self):
        for item in self.tre.get_children():
            self.tre.delete(item)
        self.label_precio_total.config(text="Precio a pagar: $ 0")

        self.entry_producto.set('')
        self.entry_cantidad.delete(0,'end')

    def limpiar_lista(self):
        self.tre.delete(*self.tre.get_children())
        self.productos_seleccionados.clear()
        #VUELVE A 0$
        self.calcular_precio_total()
    
    def eliminar_articulo(self):
        item_seleccionado = self.tre.selection()
        if not item_seleccionado:
            messagebox.showerror("Error", "No hay ningun articulo seleccionado")
            return
        item_id = item_seleccionado[0]
        valores_item= self.tre.item(item_id)["values"]
        factura, cliente, articulo, precio, cantidad, total = valores_item

        self.tre.delete(item_id)

        self.productos_seleccionados = [producto for producto in self.productos_seleccionados if producto[2] != articulo]

        self.calcular_precio_total()

    def editar_articulo(self):
        selected_item = self.tre.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione un articulo para editar")
            return
        
        item_valores = self.tre.item(selected_item[0], 'values')
        if not item_valores:
            return
        
        current_producto = item_valores[2]
        current_cantidad = item_valores[4]

        nueva_cantidad = simpledialog.askinteger("Editar articulo", "Ingrese la nueva cantidad:", initialvalue= current_cantidad)
        
        if nueva_cantidad is not None:
            try:
                with sqlite3.connect(self.db_name) as conn:
                    c = conn.cursor()
                    c.execute("SELECT precio, stock FROM articulos WHERE articulo =?", (current_producto,))
                    resultado = c.fetchone()

                    if resultado is None:
                        messagebox.showerror("Error", "Producto no encontrado")
                        return
                    
                    precio, stock = resultado

                    if nueva_cantidad > stock:
                        messagebox.showerror("Error", f"La nueva cantidad es mayor al STOCK disponible ({stock})")
                        return
                    
                    total = precio * nueva_cantidad
                    total_cop = "{} ".format(total)

                    self.tre.item(selected_item[0], values=[self.numero_factura, self.entry_cliente.get(), current_producto,"{} ".format(precio), nueva_cantidad, total_cop])

                    for idx, producto in enumerate(self.productos_seleccionados):
                        if producto[2] == current_producto:
                            self.productos_seleccionados[idx] = (self.numero_factura, self.entry_cliente.get(), current_producto, precio, nueva_cantidad, total_cop)
                            break
                    self.calcular_precio_total()
            except sqlite3.Error as e:
                print(f"Error al editar el articulo: {e}")

    def ver_ventas_realizadas(self):
        try:
            with sqlite3.connect(self.db_name) as conn:
                c = conn.cursor()
                c.execute("SELECT * FROM ventas")
                ventas = c.fetchall()

                ventana_ventas = tk.Toplevel(self)
                ventana_ventas.title("Ventas realizadas")
                ventana_ventas.geometry("1100x650+120+20")
                ventana_ventas.configure(bg="gray")
                ventana_ventas.resizable(False, False)
                ventana_ventas.transient(self.master)
                ventana_ventas.grab_set()
                ventana_ventas.focus_set()
                ventana_ventas.lift()

                # LABEL PRINCIPAL
                label_ventas_realizadas = tk.Label(ventana_ventas, text="Ventas realizadas", font="sans 26 italic underline", bg="gray")
                label_ventas_realizadas.place(x=420, y=5)

                # FORMULARIO FILTRO
                filtro_frame = tk.Frame(ventana_ventas, bg="gray")
                filtro_frame.place(x=20, y=60, width=1060, height=60)

                label_factura = tk.Label(filtro_frame, text="Numero de factura", bg="gray", font="sans 14 bold")
                label_factura.place(x=10, y=15)

                entry_factura = ttk.Entry(filtro_frame, font="sans 14 bold")
                entry_factura.place(x=200, y=10, width=200, height=40)

                label_cliente = tk.Label(filtro_frame, text="Cliente", bg="gray", font="sans 14 bold")
                label_cliente.place(x=420, y=15)

                entry_cliente = ttk.Entry(filtro_frame, font="sans 14 bold")
                entry_cliente.place(x=520, y=10, width=200, height=40)

                # TREEVIEW Y SCROLLS
                tree_frame = tk.Frame(ventana_ventas, bg="white")
                tree_frame.place(x=20, y=130, width=1060, height=500)

                scrol_y = ttk.Scrollbar(tree_frame)
                scrol_y.pack(side=RIGHT, fill=Y)

                scrol_x = ttk.Scrollbar(tree_frame, orient="horizontal")
                scrol_x.pack(side=BOTTOM, fill=X)

                tree = ttk.Treeview(tree_frame, columns=("Factura", "Cliente", "Producto", "Precio", "Cantidad", "Total", "Fecha", "Hora"), show="headings", yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set)
                tree.pack(expand=True, fill=BOTH)

                scrol_y.config(command=tree.yview)
                scrol_x.config(command=tree.xview)

                columnas = [("Factura", 60), ("Cliente", 120), ("Producto", 120), ("Precio", 80), ("Cantidad", 80), ("Total", 80), ("Fecha", 80), ("Hora", 80)]
                for col, ancho in columnas:
                    tree.heading(col, text=col)
                    tree.column(col, width=ancho, anchor="center")

                def cargar_ventas(lista_ventas):
                    for item in tree.get_children():
                        tree.delete(item)
                    for venta in lista_ventas:
                        venta = list(venta)
                        venta[3] = "{}".format(venta[3])
                        venta[5] = "{}".format(venta[5])
                        venta[6] = datetime.datetime.strptime(venta[6], "%d/%m/%Y").strftime("%d/%m/%Y")
                        tree.insert("", "end", values=venta)

                def filtrar_ventas():
                    factura_a_buscar = entry_factura.get()
                    cliente_buscar = entry_cliente.get().lower()

                    ventas_filtradas = [
                        venta for venta in ventas
                        if (str(venta[0]) == factura_a_buscar or not factura_a_buscar)
                        and (venta[1].lower() == cliente_buscar or not cliente_buscar)
                    ]
                    cargar_ventas(ventas_filtradas)

            # BOTON FILTRAR
            btn_filtrar = tk.Button(filtro_frame, text="Filtrar", font="sans 14 bold", command=filtrar_ventas)
            btn_filtrar.place(x=840, y=10)

            # MOSTRAR TODAS LAS VENTAS AL PRINCIPIO
            cargar_ventas(ventas)

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al obtener las ventas: {e}")

    def facturas_pdf(self, total_venta, cliente):
        try:
            factura_path = f"facturas/Factura_{self.numero_factura}.pdf"
            c = canvas.Canvas(factura_path, pagesize=letter)

            empresa_nombre ="Punto de venta V0.5"
            empresa_direccion = "Calle 1 # 1a - 01"
            empresa_telefono = "+54 123456789"
            empresa_mail = "info@gmail.com"
            empresa_web = "www.puntodeventa.com"

            c.setFont("Helvetica-Bold", 18)
            c.setFillColor(colors.darkblue)
            c.drawCentredString(300, 750, "FACTURA DE SERVICIOS")

            c.setFillColor(colors.black)
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, 710, f"{empresa_nombre}")
            c.setFont("Helvetica", 12)
            c.drawString(50, 690, f"Direccion: {empresa_direccion}")
            c.drawString(50, 670, f"Telefono: {empresa_telefono}")
            c.drawString(50, 650, f"Mail: {empresa_mail}")
            c.drawString(50, 630, f"Website: {empresa_web}")

            #DIBUJA LINEA HORIZONTAL SEPARADORA
            c.setLineWidth(0.5)
            c.setStrokeColor(colors.black)
            c.line(50, 620, 550, 620)

            #INFO FACTURA
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, 600, f"Numero factura: {self.numero_factura}")
            c.drawString(50, 580, f"Fecha: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")}")

            c.line(50, 560, 550, 560)

            c.drawString(50, 540, f"Cliente: {cliente}")
            c.drawString(50, 520, "Descripcion de productos: ")

            #TABLA DENTRO DE FACTURA PA POSICIONAR
            y_offset = 500
            c.setFont("Helvetica-Bold", 12)
            c.drawString(70, y_offset, "Producto")
            c.drawString(270, y_offset, "Cantidad")
            c.drawString(370, y_offset, "Precio")
            c.drawString(470, y_offset, "Total")

            c.line(50, y_offset - 10, 550, y_offset - 10)
            y_offset -= 30
            c.setFont("Helvetica", 12)
            for item in self.productos_seleccionados:
                factura, cliente, producto, precio, cantidad, total = item
                c.drawString(70, y_offset, producto)
                c.drawString(270, y_offset, str(cantidad))
                c.drawString(370, y_offset, "$".format(precio))
                c.drawString(470, y_offset, total)
                y_offset -= 20

            c.line(50, y_offset, 550, y_offset)
            y_offset -= 20

            #TOTAL A PAGAR EN FACTURA
            c.setFont("Helvetica-Bold", 14)
            c.setFillColor(colors.darkblue)
            c.drawString(50, y_offset, f"Total a pagar: $   {total_venta}")
            c.setFillColor(colors.black)
            c.setFont("Helvetica", 12)

            #FIN
            y_offset -= 20
            c.line(50, y_offset, 550, y_offset)

            c.setFont("Helvetica-Bold", 16)
            c.drawString(150, y_offset -60, "Gracias por su compra")

            c.save()

            messagebox.showinfo("Factura", f"Se genero la factura con exito en: {factura_path}")

            #SE ABRE LA FACTURA AUTOMATICAMENTE 
            os.startfile(os.path.abspath(factura_path))

        except Exception as e:
            messagebox.showerror("Error", f"Error al generar la factura: {e}")

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
        self.entry_producto.bind('<KeyRelease>', self.fitrar_productos)
        
        #LABEL CANTIDAD
        label_cantidad = tk.Label(label_frame, text="Cantidad: ", font="sans 14 bold", bg="gray")
        label_cantidad.place(x=500, y=11)
        self.entry_cantidad = ttk.Entry(label_frame, font="sans 14 bold")
        self.entry_cantidad.place(x=610, y=8, width=100, height=40)
        
        #CANTIDAD STOCK
        self.label_stock = tk.Label(label_frame, text="Stock: ", font="sans 14 bold", bg="gray")
        self.label_stock.place(x=500, y=70)

        # Vincula el evento de selección del Combobox 'entry_producto' ("<<ComboboxSelected>>") a la función 'actualizar_stock'.
        self.entry_producto.bind("<<ComboboxSelected>>", self.actualizar_stock)
        
        #FACTURA COMPRA
        label_factura = tk.Label(label_frame, text="Factura", font="sans 14 bold", bg="gray")
        label_factura.place(x=750, y=11)
        
        self.label_numero_factura = tk.Label(label_frame, text=f"{self.numero_factura}", font="sans 14 bold", bg="gray")
        self.label_numero_factura.place(x=950, y=11)
        
        #BOTONES
        boton_agregar = tk.Button(label_frame, text="Agregar articulo", font="sans 14 bold", command= self.agregar_articulo)
        boton_agregar.place(x=90, y=120, width=200, height=40)
        
        boton_eliminar = tk.Button(label_frame, text="Eliminar articulo", font="sans 14 bold", command=self.eliminar_articulo)
        boton_eliminar.place(x=310, y=120, width=200, height=40)
        
        boton_editar = tk.Button(label_frame, text="Editar articulo", font="sans 14 bold", command=self.editar_articulo)
        boton_editar.place(x=530, y=120, width=200, height=40)
        
        boton_limpiar = tk.Button(label_frame, text="Limpiar articulo", font="sans 14 bold", command=self.limpiar_lista)
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
        boton_pagar = tk.Button(self, text="Pagar", font="sans 14 bold", command=self.realizar_pago)
        boton_pagar.place(x=70, y=550, width=180, height=40)

        boton_ver_ventas = tk.Button(self, text="Ver ventas realizadas", font="sans 14 bold", command=self.ver_ventas_realizadas)
        boton_ver_ventas.place(x=290, y=550, width=280, height=40)


