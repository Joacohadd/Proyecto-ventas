from tkinter import * 
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import sys
import os

class Inventario(tk.Frame):
    def __init__(self, padre):
        super().__init__(padre)
        self.widgets()
        
        #CREA LA CARPETA SI NO EXISTE YA
        self.image_folder = "fotos"
        if not os.path.exists(self.image_folder):
            os.makedirs(self.image_folder)
    
    def widgets(self):
    #PRIMER LABEL FRAME
        
        canva_articulos = tk.LabelFrame(self, text="Articulos", font="arial 14 bold", bg="gray")
        canva_articulos.place(x=300, y=10, width=780, height=580)
        
        self.canva = tk.Canvas(canva_articulos, bg="gray")
        self.scrollbar = tk.Scrollbar(canva_articulos, orient="vertical", command=self.canva.yview) 
        self.scrollable_frame = tk.Frame(self.canva, bg="gray")
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canva.configure(
                scrollregion= self.canva.bbox("all")
            )
        )
        
        self.canva.create_window((0,0), window= self.scrollable_frame, anchor="nw")
        self.canva.configure(yscrollcommand= self.scrollbar.set)
        
        self.scrollbar.pack(side="right", fill="y")
        self.canva.pack(side="left", fill="both", expand=True)
    #====================================================================
    
    #SEGUNDO LABEL FRAME
        lblframe_buscar = LabelFrame(self, text="Buscar", font="arial 14 bold", bg="gray")
        lblframe_buscar.place(x=10, y=10, width=280, height=80)
        
        self.combobox_buscar = ttk.Combobox(lblframe_buscar, font="arial 12")
        self.combobox_buscar.place(x=5, y=5, width=260, height=40)
    #====================================================================

    #TERCER LABEL FRAME
        lblframe_seleccion = LabelFrame(self, text="Selección", font="arial 14 bold", bg="gray")
        lblframe_seleccion.place(x=10, y=95, width=280, height=190)
        
        self.label_select = tk.Label(lblframe_seleccion, text="Articulo: ", font="arial 12", bg="gray", wraplength=300)
        self.label_select.place(x=5, y=10)
        
        self.label_select_2 = tk.Label(lblframe_seleccion, text="Precio: ", font="arial 12", bg="gray")
        self.label_select_2.place(x=5, y=40)
        
        self.label_select_3 = tk.Label(lblframe_seleccion, text="Stock: ", font="arial 12", bg="gray", wraplength=300)
        self.label_select_3.place(x=5, y=70)
        
        self.label_select_4 = tk.Label(lblframe_seleccion, text="Estado: ", font="arial 12", bg="gray", wraplength=300)
        self.label_select_4.place(x=5, y=100)
    #====================================================================

    #CUARTO LABEL FRAME
        lblframe_botones = LabelFrame(self, bg="gray",text="Opciones", font="arial 14 bold")
        lblframe_botones.place(x=10, y=290, width=280, height=300)
        
        boton_1 = tk.Button(lblframe_botones, text="Agregar", font="arial 14 bold", command= self.agregar_articulo)
        boton_1.place(x=20, y=20, width=180, height=40)
        
        boton_2 = tk.Button(lblframe_botones, text="Editar", font="arial 14 bold")
        boton_2.place(x=20, y=80, width=180, height=40)
        
        boton_3 = tk.Button(lblframe_botones, text="Eliminar", font="arial 14 bold")
        boton_3.place(x=20, y=140, width=180, height=40)

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            image = Image.open(file_path)
            image = image.resize((200, 200), Image.LANCZOS)
            
            image_name = os.path.basename(file_path)
            image_save_path = os.path.join(self.image_folder, image_name)
            image.save(image_save_path, "PNG")
            
            self.image_tk = ImageTk.PhotoImage(image)
            self.product_image = self.image_tk
            
            self.image_path = image_save_path
            img_label = tk.Label(self.frame_img, image= self.image_tk)
            img_label.place(x=0, y=0, width=200, height=200)
    

    def agregar_articulo(self):
        top = tk.Toplevel(self)
        top.title("Agregar articulo")
        top.geometry("700x400+200+50")
        top.config(bg="gray")
        top.resizable(False, False)
        
        #Esto hace que solo se pueda usar esta ventana hasta que se cierre
        top.transient(self.master)
        top.grab_set()
        top.focus_set()
        top.lift()
        
        #LABELS
        tk.Label(top, text="Articulo: ", font="arial 13 bold", background="gray").place(x=20, y=22, width=100, height=25)
        entry_articulo = ttk.Entry(top, font="arial 12 bold").place(x=120, y=20, width=250, height=30)
        
        tk.Label(top, text="Precio: ", font="arial 13 bold", background="gray").place(x=20, y=62, width=100, height=25)
        entry_precio = ttk.Entry(top, font="arial 12 bold").place(x=120, y=60, width=250, height=30)
        
        tk.Label(top, text="Stock: ", font="arial 13 bold", background="gray").place(x=20, y=102, width=100, height=25)
        entry_stock = ttk.Entry(top, font="arial 12 bold").place(x=120, y=100, width=250, height=30)
        
        tk.Label(top, text="Estado: ", font="arial 13 bold", background="gray").place(x=20, y=142, width=100, height=25)
        entry_estado = ttk.Entry(top, font="arial 12 bold").place(x=120, y=140, width=250, height=30)
        
        self.frame_img = tk.Frame(top, bg="white", highlightbackground="black", highlightthickness=1)
        self.frame_img.place(x=440, y=30, width=200, height=200)
        
        boton_img = tk.Button(top, text="Cargar imagen", font="arial 12 bold", command=self.load_image)
        boton_img.place(x=470, y=260, width=150, height=50)