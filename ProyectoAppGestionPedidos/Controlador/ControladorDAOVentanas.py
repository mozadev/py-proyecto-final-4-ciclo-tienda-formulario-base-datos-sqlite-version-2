
from tkinter import *
from tkinter import messagebox
from tkinter import PhotoImage
from PIL import Image,ImageTk

from Vista import VistaCliente, VistaLoginAdministrador
from Vista.VistaLoginCliente import *
from Vista.VistaLoginAdministrador import *
class Index(Frame):
	def __init__(self,raiz):
		super().__init__(raiz)
		self.raiz=raiz
		self.raiz.resizable(False,False)
		ancho_ventana = 720
		alto_ventana = 500

		x_ventana = self.raiz.winfo_screenwidth() // 2 - ancho_ventana // 2
		y_ventana = self.raiz.winfo_screenheight() // 2 - alto_ventana // 2

		posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
		self.raiz.geometry(posicion)
		self.raiz.title("Sistema de Gestión de Pedidos")

		'''
		self.imagen = PhotoImage(file = "C:/Users/51980/Dropbox/Mi PC (LAPTOP-4BGG3MQ0)/Desktop/ProyectoAppGestionPedidos/imagenes/iFondo.gif")
		background = Label(image = self.imagen, text = "Imagen S.O de fondo")
		background.place(x = 0, y = 0, relwidth = 1, relheight = 1)
		'''
		'''
		self.image = Image.open("C:/Users/51980/Dropbox/Mi PC (LAPTOP-4BGG3MQ0)/Desktop/ProyectoAppGestionPedidos/imagenes/iFondo.gif")
        self.img_copy= self.image.copy()
        self.background_image = ImageTk.PhotoImage(self.image)

        self.background = Label(self, image=self.background_image)
        self.background.pack(fill=BOTH, expand=YES)
        self.background.bind('<Configure>', self._resize_image)
        self.pack(fill=BOTH, expand=YES)
		'''

		self.pack()
		self.widgets()
		self.place(relwidth=1, relheight=1)
		self.config(bg="#17A589")
	def widgets(self):
		self.miImagen = Image.open('imagenes/fondo.jpg')
		self.miImagen = self.miImagen.resize((720, 500), Image.ANTIALIAS)
		self.miImagen=ImageTk.PhotoImage(self.miImagen)
		self.fondoLb=Label(self,image=self.miImagen)
		self.fondoLb.place(x=0,y=0)
		self.fondoLb.config(border=0)

		self.titulo=Label(self,text="Sistema de Gestión")
		self.titulo.grid(padx=20,pady=20)	
		self.titulo.place(x=220,y=20)
		self.titulo.config(font=('Comic Sans MS', 23),bg="white",fg="black",justify="center")

		
		self.Subtitulo1=Label(self,text="Inicio de sesión como administrador")
		self.Subtitulo1.grid(sticky="e",padx=20,pady=20)
		self.Subtitulo1.place(x=30,y=100)
		self.Subtitulo1.config(font=('Comic Sans MS', 15),bg="white",fg="black")
		self.Subtitulo2=Label(self,text="Inicio de sesión como cliente")
		self.Subtitulo2.grid( sticky="e",padx=20,pady=20)
		self.Subtitulo2.place(x=430,y=100)
		self.Subtitulo2.config(font=('Comic Sans MS', 15),bg="white",fg="black")
		



		self.imgADM = Image.open('imagenes/imagenADM.png')
		self.imgADM = self.imgADM.resize((140, 120), Image.ANTIALIAS) # Redimension (Alto, Ancho)
		self.imgADM = ImageTk.PhotoImage(self.imgADM)
		self.botonEntrarAdm=Button(self,image=self.imgADM,text="Administrador",compound="top", command=self.botonAdm)
		self.botonEntrarAdm.grid(padx=30,pady=30)
		self.botonEntrarAdm.place(x=120,y=190)
		self.botonEntrarAdm.config(font=('Comic Sans MS', 12), cursor="hand2",bg="white",fg="black", activebackground="white",border=0)

		self.imgCLIENTE = Image.open('imagenes/imagenCLIENTE.png')
		self.imgCLIENTE = self.imgCLIENTE.resize((140, 120), Image.ANTIALIAS) # Redimension (Alto, Ancho)
		self.imgCLIENTE = ImageTk.PhotoImage(self.imgCLIENTE)
		self.botonEntrarCliente=Button(self,image=self.imgCLIENTE,text="Cliente",compound="top", command=self.botonCliente)
		self.botonEntrarCliente.grid(padx=30,pady=30)
		self.botonEntrarCliente.place(x=490,y=190)
		self.botonEntrarCliente.config(font=('Comic Sans MS', 12), cursor="hand2",bg="white",fg="black", activebackground="white",border=0)
		
		
	def botonAdm(self):
		self.raiz.destroy()
		VistaLoginAdministrador.abrirLoginAdm()

	def botonCliente(self):
		self.raiz.destroy()
		VistaLoginCliente.abrirLoginCliente()

def abrirIndex():
	raiz=Tk()
	obj=Index(raiz)
	obj.mainloop()		