from tkinter import ttk 
from tkinter import *
from tkinter import filedialog
from tkinter import PhotoImage
from PIL import Image,ImageTk
import sqlite3
import random
class GestorEnvio(Frame):
	base='database.db'
	foto_binario=""
	def __init__(self,raiz):
		self.raiz=raiz
		#creando contenedor
		frame=LabelFrame(text="Gestion envío",bg='white')
		frame.place(x=0,y=70)
		#creando tabla
		style=ttk.Style()
		style.theme_use("clam")
		style.configure('Treeview',background="silver",foreground="black",rowheight=30,fieldbackground="white")
		#style.map('Treeview',background[('selected','green')])
		
		col = ('Usuario', 'Monto','Forma pago', 'Fecha', 'Direccion','Nombres', 'Apellidos', 'Pais', 'Departamento','Provincia', 'Distrito')
		self.tree=ttk.Treeview(frame,height=4, show='headings',columns=col)
		self.tree.grid(row=0,column=0)
		self.tree.column('Usuario', width=50,anchor=CENTER)
		self.tree.column('Monto', width=45,anchor=CENTER)
		self.tree.column('Forma pago', width=78,anchor=CENTER)
		self.tree.column('Fecha', width=96,anchor=CENTER)
		self.tree.column('Direccion', width=70,anchor=CENTER)
		self.tree.column('Nombres', width=70,anchor=CENTER)
		self.tree.column('Apellidos', width=60,anchor=CENTER)
		self.tree.column('Pais', width=50,anchor=CENTER)
		self.tree.column('Departamento', width=85,anchor=CENTER)
		self.tree.column('Provincia', width=60,anchor=CENTER)
		self.tree.column('Distrito', width=50,anchor=CENTER)
		
		self.tree.heading('Usuario',text='Usuario')
		self.tree.heading('Monto',text='Monto')
		self.tree.heading('Forma pago',text='Forma pago')
		self.tree.heading('Fecha',text='Fecha')
		self.tree.heading('Direccion',text='Direccion')
		self.tree.heading('Nombres',text='Nombres')
		self.tree.heading('Apellidos',text='Apellidos')
		self.tree.heading('Pais',text='Pais')
		self.tree.heading('Departamento',text='Departamento')
		self.tree.heading('Provincia',text='Provincia')
		self.tree.heading('Distrito',text='Distrito')

	
		self.get_products()
	def run_query(self,query,parameters=()):
		with sqlite3.connect(self.base) as conn:
			cursor=conn.cursor()
			result=cursor.execute(query,parameters)
			conn.commit()
		return result
	def get_products(self):
		
		#limpiando la tabla
		records=self.tree.get_children()
		for element in records:
			self.tree.delete(element)
		#consultando datos
		query='SELECT * FROM Pedido_Envio'	
		rows=self.run_query(query)
		
		i=0
		for row in rows:
			self.tree.insert('',i,values=(row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11]))
			i+=1
			



