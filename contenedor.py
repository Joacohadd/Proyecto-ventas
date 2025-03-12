from tkinter import * 
import tkinter as tk
from modulos.ventas import Ventas
from modulos.inventario import Inventario
from modulos.pedidos import Pedidos
from modulos.clientes import Clientes
from modulos.informacion import Informacion
from modulos.proveedor import Proveedor
import sys
import os

class Container(tk.Frame):
    def __init__(self, padre, controlador):
        super().__init__(padre)
        self.controlador = controlador
        self.pack()
        self.place(x = 0, y = 0, width = 1100, height = 650)
        self.widgets()
        self.frames = {}
        self.buttons = []
        for i in (Ventas, Inventario, Clientes, Pedidos, Informacion, Proveedor):
            frame = i(self)
            self.frames[i] = frame
            frame.pack()
            frame.config(bg= "gray", highlightbackground= "red", highlightthickness= 1)
            frame.place(x= 0, y= 40, width= 1100, height= 610)
        self.show_frames(Ventas)


    def show_frames(self, contenedor):
        frame = self.frames[contenedor]
        frame.tkraise()

    def ventas(self):
        self.show_frames(Ventas)

    def inventario(self):
        self.show_frames(Inventario)

    def informacion(self):
        self.show_frames(Informacion)

    def clientes(self):
        self.show_frames(Clientes)

    def pedidos(self):
        self.show_frames(Pedidos)
        
    def proveedor(self):
        self.show_frames(Proveedor)


    def widgets(self):
        frame_2 = tk.Frame(self)
        frame_2.place(x=0, y= 0, width=1100, height= 40)
        
        self.btn_ventas = Button(frame_2, fg= "black", text= "Ventas", font= "sans 16 bold", command= self.ventas)
        self.btn_ventas.place(x= 0, y= 0, width= 184, height= 40)
        
        self.btn_informacion = Button(frame_2, fg= "black", text= "Informacion", font= "sans 16 bold", command= self.informacion)
        self.btn_informacion.place(x= 184, y= 0, width= 184, height= 40)
        
        self.btn_inventario = Button(frame_2, fg= "black", text= "Inventario", font= "sans 16 bold", command= self.inventario)
        self.btn_inventario.place(x= 369, y= 0, width= 184, height= 40)
        
        self.btn_clientes = Button(frame_2, fg= "black", text= "Clientes", font= "sans 16 bold", command= self.clientes)
        self.btn_clientes.place(x= 554, y= 0, width= 184, height= 40)
        
        self.btn_pedidos = Button(frame_2, fg= "black", text= "Pedidos", font= "sans 16 bold", command= self.pedidos)
        self.btn_pedidos.place(x= 739, y= 0, width= 184, height= 40)
        
        self.btn_proveedor = Button(frame_2, fg= "black", text= "Proveedor", font= "sans 16 bold", command= self.proveedor)
        self.btn_proveedor.place(x= 923, y= 0, width= 184, height= 40)
        
        self.buttons = [self.btn_clientes, self.btn_informacion, self.btn_inventario, self.btn_pedidos, self.btn_pedidos, self.btn_ventas]
