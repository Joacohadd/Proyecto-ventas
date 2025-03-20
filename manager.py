from tkinter import * 
from tkinter import ttk
from modulos.login import Login, Registro
from contenedor import Container
import sys
import os

class Manager(Tk):
    def __init__(self, *args, **kwagrs):
        super().__init__(*args, **kwagrs)
        self.title("Gestor locales V0.1")
        self.geometry("1100x650+120+20")
        
        contenedor = Frame(self)
        contenedor.pack(side=TOP, fill=BOTH, expand=True)
        contenedor.configure(bg="gray")
        
        self.frames ={}
        for i in (Login, Registro, Container):
            frame = i(contenedor, self)
            self.frames[i] = frame
            
        self.show_frame(Container)
        
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        
    def show_frame(self, contenedor):
        frame = self.frames[contenedor]
        frame.tkraise()

def main():
    app = Manager()
    app.mainloop()

if __name__ == "__main__":
    main()