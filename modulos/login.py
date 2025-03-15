from tkinter import * 
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import sqlite3
from contenedor import Container

class Login(tk.Frame):
    db_name = "database.db"
    
    
    #FONDO DE LOGIN
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.pack()
        self.place(x=0, y=0, width=1100, height=650)
        self.controlador = controlador
        self.widgets()
    
    def validacion(self, user, password):
        return len(user) > 0 and len(password) > 0
    
    def login(self):
        user = self.user_name.get()
        passsword = self.contraseña.get()
        
        #BASE DE DATOS
        if self.validacion(user, passsword):
            consulta = "SELECT * FROM usuarios WHERE username = ? AND password = ?"
            parametros = (user, passsword)
            
            try:
                with sqlite3.connect(self.db_name) as conn:
                    cursor = conn.cursor()
                    cursor.execute(consulta, parametros)
                    resultado = cursor.fetchall()
                    
                    if resultado:
                        self.contro_1()
                    else:
                        self.user_name.delete(0, 'end')
                        self.contraseña.delete(0, 'end')
                        messagebox.showerror(title="Error", message="Usuario y/o contraseña incorrecta")
                        
            except sqlite3.Error as e:
                messagebox.showerror(title="Error", message="No se conecto a la base de datos. {}".format(e))
        else:
            messagebox.showerror(title="Error", message="Complete todos los campos")
        
    def contro_1(self):
        self.controlador.show_frame(Container)
    
    def control_2(self):
        self.controlador.show_frame(Registro)
    
    
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
        
        boton_iniciar = tk.Button(frame_recuadro, text="Iniciar", font="arial 16 bold", command=self.login)
        boton_iniciar.place(x=80, y=440, width=240, height=40)
        
        boton_registrar = tk.Button(frame_recuadro, text="Registrar", font="arial 16 bold", command=self.control_2)
        boton_registrar.place(x=80, y=500, width=240, height=40)



class Registro(tk.Frame):
    db_name = "database.db"
    
    
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.pack()
        self.place(x=0, y=0, width=1100, height=650)
        self.controlador = controlador
        self.widgets()
    
    def validacion(self, user, password):
        return len(user) > 0 and len(password) > 0


    def ejecu_consulta(self, consulta, parametros=()):
        try:
            with sqlite3.connect(self.db_name) as conn:
                cursor = conn.cursor()
                cursor.execute(consulta, parametros)
                conn.commit
        except sqlite3.Error as e:
            messagebox.showerror(title="Error", message="Error al ejecutar la consulta: {}".format(e))
    
    def registro(self):
        user = self.user_name.get()
        password = self.contraseña.get()
        key = self.key.get()
        if self.validacion(user, password):
            if len(password) < 4:
                messagebox.showinfo(title="Error", message="Contraseña corta (MIN 4 CARAC)")
                self.user_name.delete(0, 'end')
                self.contraseña.delete(0, 'end')
            else:
                if key== "1234":
                    consulta = "INSERT INTO usuarios VALUES (?,?,?)"
                    parametros = (None, user, password)
                    self.ejecu_consulta(consulta, parametros)
                    self.control_1()
                else:
                    messagebox.showerror(title="Registro", message="Error al ingresar el codigo de registro")
        else:
            messagebox.showerror(title="Error", message="Complete sus datos")

    #SI SE CREA EL USUARIO AL CONTAINER
    def control_1(self):
        self.controlador.show_frame(Container)
    
    #VUELVE AL LOGIN
    def control_2(self):
        self.controlador.show_frame(Login)



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
        
        boton_iniciar_registro = tk.Button(frame_recuadro, text="Registrarse", font="arial 16 bold", command=self.registro)
        boton_iniciar_registro.place(x=80, y=520, width=240, height=40)
        
        boton_registrar_registro = tk.Button(frame_recuadro, text="Volver", font="arial 16 bold", command=self.control_2)
        boton_registrar_registro.place(x=80, y=570, width=240, height=40)
