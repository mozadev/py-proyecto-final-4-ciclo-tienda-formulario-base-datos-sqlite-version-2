from tkinter import *
from tkinter import ttk,PhotoImage,messagebox
from PIL import Image,ImageTk
#from tkhtmlview import HTMLLabel
from Vista import VistaClientestotales
from Vista.VistaClientestotales import *
#import ventanaCRUDCliente
from Vista.VistaCliente import *
from Controlador import ControladorDAOVentanas
from Controlador.ControladorDAOVentanas import *
import sqlite3
class Login(Frame):
	base='database.db'
	def __init__(self,raiz):
		super().__init__(raiz)
		self.raiz=raiz
		self.raiz.resizable(False,False)
		ancho_ventana = 550
		alto_ventana = 380

		x_ventana = self.raiz.winfo_screenwidth() // 2 - ancho_ventana // 2
		y_ventana = self.raiz.winfo_screenheight() // 2 - alto_ventana // 2

		posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
		self.raiz.geometry(posicion)
		self.raiz.title("Login Cliente")
	
		self.pack()
		self.widgets()
		self.place(relwidth=1, relheight=1)

	def widgets(self):
		self.miImagen = Image.open('imagenes/fondoLoginC.jpg')
		self.miImagen = self.miImagen.resize((550, 380), Image.ANTIALIAS)
		self.miImagen=ImageTk.PhotoImage(self.miImagen)
		self.fondoLb=Label(self,image=self.miImagen)
		self.fondoLb.place(x=0,y=0)
		self.fondoLb.config(border=0)

		self.titulo=Label(self,text="Login")
		self.titulo.grid(padx=30,pady=30)	
		self.titulo.place(x=260,y=40)
		self.titulo.config(font=('Comic Sans MS',23),bg="white",fg="black",justify="center")

		self.miNombre=StringVar()
		self.miContraseña=StringVar()
		self.cuadroNombre=Entry(self, textvariable=self.miNombre)
		self.cuadroNombre.grid(padx=10,pady=10)
		self.cuadroNombre.place(x=240,y=130)
		self.cuadroNombre.config(fg="green",justify="center",font=('Arial', 13))
		self.cuadroNombre.focus()
		self.cuadroPass=Entry(self, textvariable=self.miContraseña)
		self.cuadroPass.grid(padx=10,pady=10)
		self.cuadroPass.place(x=240,y=170)
		self.cuadroPass.config(show="*",fg="green",justify="center",font=('Arial', 13))


		self.nombreLabel=Label(self,text="Usuario: ")
		self.nombreLabel.grid(sticky="e",padx=10,pady=10)
		self.nombreLabel.place(x=100,y=130)	
		self.nombreLabel.config(font=('Arial', 15),fg="black",bg="white")
		self.passLabel=Label(self,text="Contraseña: ")
		self.passLabel.grid(sticky="e",padx=10,pady=10)
		self.passLabel.place(x=100,y=170)
		self.passLabel.config(font=('Arial', 15),bg="white",fg="black")
		self.botonEnvio=Button(self,text="Confirmar", command=self.botonEnvio)
		self.botonEnvio.grid(padx=10,pady=10)
		self.botonEnvio.place(x=240,y=230)
		self.botonEnvio.config(font=('Comic Sans MS', 12),activeforeground="black", activebackground="white", bg="white", cursor="hand2",border=1)
		#self.botonEnvio.place(x=300, y=300, width=140, height=30)

		self.img = Image.open('imagenes/flecha2.png')
		self.img = self.img.resize((30, 30), Image.ANTIALIAS) # Redimension (Alto, Ancho)
		self.img = ImageTk.PhotoImage(self.img)

		self.botonRegresar=Button(self,image=self.img,compound="none", command=self.botonRegresar)
		self.botonRegresar.grid(padx=10,pady=10)
		self.botonRegresar.config(font=('Comic Sans MS', 12), cursor="hand2",bg="white", activebackground="white",border=0)
		self.botonRegresar.place(x=0,y=0)
		#botonNuevo1 = tkinter.Button(root, image=img, text="asdfasdf", compound="top")
		
		#botonNuevo1 = tkinter.Button(root, image=img, text="asdfasdf", compound="top")
		#botonNuevo1.place(x=500, y=100)

		#Enlace de registro
		
		#self.enlace=HTMLLabel(self,html='<p style="color: red;background-color: #17A589">¿Usuario Nuevo?<a href="ventanaCRUDCliente.abrir_ventanta_crud_cliente()"> Registrarse</a></p>')
		self.lblRegistar=Label(self,text="¿Nuevo Usuario?  ",bg="white")
		self.lblRegistar.place(x=330,y=10)	
		self.lblRegistar.config(font=('Arial', 11),fg="black",bg="white")
		self.btnRegistrar=ttk.Button(self,text='Registrarse',command=self.registrarCRUD).place(x=460,y=8)
		#btnRegistrar.config(bg="#17A589", activebackground="#17A589")
	def registrarCRUD(self):
		self.raiz.destroy()
		VistaCliente.abrirRegistroCliente()
	def botonEnvio(self):
		if len(self.miNombre.get())==0:
			messagebox.showwarning("Error","Campo usuario requerido.")
			self.miNombre.set("")
		if len(self.miContraseña.get())==0:
			messagebox.showwarning("Error","Campo contraseña requerido.")
			self.miContraseña.set("")
		if len(self.miContraseña.get())!=0 and len(self.miNombre.get())!=0:
			self.validacion()
	def run_query(self,query,parameters=()):
		with sqlite3.connect(self.base) as conn:
			cursor=conn.cursor()
			result=cursor.execute(query,parameters)
			conn.commit()
		return result	
	def validacion(self):
		try:
			self.parameters=(self.miNombre.get(),self.miContraseña.get())
			self.query='SELECT COUNT(*) FROM Cliente WHERE Usuario =? AND Contraseña=?'
			self.valor=self.run_query(self.query,self.parameters).fetchall()
			
			if self.valor[0]==(1,):
				self.raiz.destroy()
				VistaClientestotales.abrirVentanaCLIENTE(self.miNombre.get())
			else:
				messagebox.showwarning("Error","Usuario no registrado")	
			
		except:
			messagebox.showwarning("Error","Usuario no registrado")			

	def botonRegresar(self):
		self.raiz.destroy()	
		ControladorDAOVentanas.abrirIndex()


def abrirLoginCliente():
	raiz=Tk()
	obj=Login(raiz)
	obj.mainloop()		