from tkinter import ttk 
from tkinter import *
from tkinter import filedialog
from tkinter import PhotoImage
from PIL import Image,ImageTk
import sqlite3
import random
class GestorPedido(Frame):
	base='database.db'
	foto_binario=""
	def __init__(self,raiz):
		self.raiz=raiz
		#creando contenedor
		frame=LabelFrame(text="Ventas",bg='white')
		frame.place(x=20,y=70)
		#creando tabla
		style=ttk.Style()
		style.theme_use("clam")
		style.configure('Treeview',background="silver",foreground="black",rowheight=30,fieldbackground="white")

		col = ('Usuario', 'Producto','Codigo', 'Precio', 'Cantidad','Total')
		self.tree=ttk.Treeview(frame,height=4, show='headings',columns=col)
		self.tree.grid(row=0,column=0)
		self.tree.column('Usuario', width=100,anchor=CENTER)
		self.tree.column('Producto', width=100,anchor=CENTER)
		self.tree.column('Codigo', width=100,anchor=CENTER)
		self.tree.column('Precio', width=100,anchor=CENTER)
		self.tree.column('Cantidad', width=100,anchor=CENTER)
		self.tree.column('Total', width=100,anchor=CENTER)
		
		self.tree.heading('Usuario',text='Usuario')
		self.tree.heading('Producto',text='Producto')
		self.tree.heading('Codigo',text='Codigo')
		self.tree.heading('Precio',text='Precio')
		self.tree.heading('Cantidad',text='Cantidad')
		self.tree.heading('Total',text='Total')



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
		query='SELECT * FROM Pedido'	
		rows=self.run_query(query)
		
		i=0
		for row in rows:
			self.tree.insert('',i,values=(row[1],row[2],row[3],row[4],row[5],row[6]))
			i+=1
			


