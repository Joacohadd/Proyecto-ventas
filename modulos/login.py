from tkinter import * 
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class Login(tk.Frame):
    
    #FONDO DE LOGIN
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.pack()
        self.place(x=0, y=0, width=1100, height=650)
        self.controlador = controlador
        self.widgets()
    
    def widgets(self):
        fondo = tk.Frame(self, bg="gray")
        fondo.pack()
        fondo.place(x=0, y=0, width=1100, height=650)

        self.bg_img = Image.open("imagenes/fondo_super.jpg")
        self.bg_img = self.bg_img.resize((1100, 650))
        self.bg_img = ImageTk.PhotoImage(self.bg_img)
        self.bg_label = ttk.Label(fondo, image=self.bg_img)
        self.bg_label.place(x=0, y=0, width=1100, height=650)

        #INICIO SESION
        frame_recuadro = tk.Frame(self, bg="gray", highlightbackground="black", highlightthickness="1")
        frame_recuadro.place(x=350, y=70, width=400, height=560)
        
        user = ttk.Label(frame_recuadro, text="Nombre de usuario", font="arial 16 bold", background="#FFFFFF")
        user.place(x=100, y=250)
        self.user_name = ttk.Entry(frame_recuadro, font="arial 16 bold")
        self.user_name.place(x=80, y=290, width=240, height=40)
        
        password = ttk.Label(frame_recuadro, text="Contraseña", font="arial 16 bold", background="#FFFFFF")
        password.place(x=100, y=340)
        self.contraseña = ttk.Entry(frame_recuadro, show="*", font="arial 16 bold")
        self.contraseña.place(x=80, y=380, width=240, height=40)
        
        boton_iniciar = tk.Button(frame_recuadro, text="Iniciar", font="arial 16 bold")
        boton_iniciar.place(x=80, y=440, width=240, height=40)
        
        boton_registrar = tk.Button(frame_recuadro, text="Registrar", font="arial 16 bold")
        boton_registrar.place(x=80, y=500, width=240, height=40)



class Registro(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.pack()
        self.place(x=0, y=0, width=1100, height=650)
        self.controlador = controlador
        self.widgets()

    def widgets(self):
        fondo = tk.Frame(self, bg="gray")
        fondo.pack()
        fondo.place(x=0, y=0, width=1100, height=650)

        self.bg_img = Image.open("imagenes/fondo_super.jpg")
        self.bg_img = self.bg_img.resize((1100, 650))
        self.bg_img = ImageTk.PhotoImage(self.bg_img)
        self.bg_label = ttk.Label(fondo, image=self.bg_img)
        self.bg_label.place(x=0, y=0, width=1100, height=650)

        #INICIO SESION
        frame_recuadro = tk.Frame(self, bg="gray", highlightbackground="black", highlightthickness="1")
        frame_recuadro.place(x=350, y=10, width=400, height=630)
        
        user = ttk.Label(frame_recuadro, text="Nombre de usuario", font="arial 16 bold", background="#FFFFFF")
        user.place(x=100, y=250)
        self.user_name = ttk.Entry(frame_recuadro, font="arial 16 bold")
        self.user_name.place(x=80, y=290, width=240, height=40)
        
        password = ttk.Label(frame_recuadro, text="Contraseña", font="arial 16 bold", background="#FFFFFF")
        password.place(x=100, y=340)
        self.contraseña = ttk.Entry(frame_recuadro, show="*", font="arial 16 bold")
        self.contraseña.place(x=80, y=380, width=240, height=40)
        
        key = ttk.Label(frame_recuadro, text="Codigo de registro", font="arial 16 bold")
        key.place(x=100, y=430)
        self.key = ttk.Entry(frame_recuadro, show="*", font="arial 16 bold")
        self.key.place(x=80, y=470, width=240, height=40)
        
        boton_iniciar_registro = tk.Button(frame_recuadro, text="Registrarse", font="arial 16 bold")
        boton_iniciar_registro.place(x=80, y=520, width=240, height=40)
        
        boton_registrar_registro = tk.Button(frame_recuadro, text="Volver", font="arial 16 bold")
        boton_registrar_registro.place(x=80, y=570, width=240, height=40)
