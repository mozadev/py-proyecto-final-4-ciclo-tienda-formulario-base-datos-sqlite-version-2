from tkinter import *
from tkinter import filedialog,ttk,PhotoImage
from PIL import Image,ImageTk
import sqlite3
import random
import datetime
class Carrito(Frame):
	base='database.db'
	def __init__(self,raiz,usuario):
		self.raiz=raiz
		self.usuario=usuario
		#creando contenedor
		frame=LabelFrame(text="",bg='white')
		frame.place(x=20,y=60)
		#Titulo
		self.Titulo=Label(frame,text="Carrito de compra")
		self.Titulo.grid(row=0,column=0,padx=10,pady=9, sticky="NSEW")
		self.Titulo.config(bg="white",fg="#273746",justify="center",font=('Comic Sans MS', 20))

		
		#creando tabla
		col = ('Nombre', 'Codigo','Precio', 'Cantidad','Total')
		self.tree=ttk.Treeview(frame,height=5,column=col)
		self.tree.grid(row=1,column=0)
		self.tree.column('#0', width=150,anchor=CENTER)
		self.tree.column('#1', width=110,anchor=CENTER)
		self.tree.column('#2', width=110,anchor=CENTER)
		self.tree.column('#3', width=100,anchor=CENTER)
		self.tree.column('#4', width=100,anchor=CENTER)
		self.tree.column('#5', width=100,anchor=CENTER)
		

		self.tree.heading('#0',text='Producto')
		self.tree.heading('#1',text='Nombre')
		self.tree.heading('#2',text='Codigo')
		self.tree.heading('#3',text='Precio')
		self.tree.heading('#4',text='Cantidad')
		self.tree.heading('#5',text='Total')

		

		style=ttk.Style()
		style.configure('Treeview',rowheight=50)
		#botones 
		ttk.Button(frame,text='Quitar',command=self.eliminar_cliente).grid(row=6,column=0,sticky=W+E)
		ttk.Button(frame,text='Cambiar cantidad',command=self.editar_cliente).grid(row=7,column=0,sticky=W+E)
		ttk.Button(frame,text='Realizar Compra',command=self.compra).grid(row=8,column=0,sticky=W+E)

		#self.pack()
		#self.widgets()
		#self.place(relwidth=1, relheight=1)
		
		#Llenando las filas
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
		query='SELECT * FROM Previo_Pedido'	
		rows=self.run_query(query)
		#rellenando los datos


		self.numeros=[]
		self.variables=[]
		
		i=0
		for row in rows:
			numero=random.randint(1, 50)
			self.variables.append('a'+str(numero))
			data=row[7]
			with open(f'imagenes/imagen.jpg', 'wb') as f:
				f.write(data)	
			self.variables[i] = Image.open(f'imagenes/imagen.jpg')
			self.variables[i] = self.variables[i].resize((50, 50), Image.ANTIALIAS)
			self.variables[i] = ImageTk.PhotoImage(self.variables[i])
			self.tree.insert('',i,image=self.variables[i],values=(row[2],row[3],row[4],row[5],row[6]))
			i+=1
			
	


	def eliminar_cliente(self):	
		
		try:
			self.tree.item(self.tree.selection())['values'][1]
		except IndexError as e:
			return
		
		producto=self.tree.item(self.tree.selection())['values'][1]
		query='DELETE FROM Previo_Pedido WHERE Codigo_Producto=?'
		self.run_query(query,(producto,))	
		
		self.get_products()

	def editar_cliente(self):
		try:
			self.tree.item(self.tree.selection())['values'][1]
		except IndexError as e:			
			return
		cantidad_antigua=self.tree.item(self.tree.selection())['values'][3]
		nombre_produc=self.tree.item(self.tree.selection())['values'][0]
		self.editar_ventana=Toplevel()
		self.ancho=250
		self.alto=90
		self.x=self.editar_ventana.winfo_screenwidth()//2-self.ancho//2
		self.y=self.editar_ventana.winfo_screenheight()//2-self.alto//2
		self.posicion=str(self.ancho)+"x"+str(self.alto)+"+"+str(self.x)+"+"+str(self.y)
		self.editar_ventana.geometry(self.posicion)
		self.editar_ventana.resizable(False,False)
		self.editar_ventana.title('Editar')
		#cantidad antiguo
		Label(self.editar_ventana,text='Cantidad anterior: ',bg='white').grid(row=0,column=0)
		Entry(self.editar_ventana,textvariable=StringVar(self.editar_ventana,value=cantidad_antigua),state='readonly').grid(row=0,column=1)
		#cantidad nuevo
		Label(self.editar_ventana,text='Cantidad nueva: ',bg='white').grid(row=1,column=0)
		nueva_cantidad=Entry(self.editar_ventana)
		nueva_cantidad.grid(row=1,column=1)
		

		
		ttk.Button(self.editar_ventana,text="Editar",command=lambda:self.editar_fila(nueva_cantidad.get()	,nombre_produc)).grid(row=2,columnspan=2)

	def editar_fila(self,nueva_cantidadString,nombre_produc):
		query='SELECT * FROM Producto WHERE Nombre=?'
		rows=self.run_query(query,(nombre_produc,))
		for row in rows:
			datoCantidad=row[4]
		try:
			nueva_cantidad=int(nueva_cantidadString)
			if nueva_cantidad>0 and nueva_cantidad<=datoCantidad:
				query='SELECT * FROM Previo_Pedido WHERE Nombre_Producto=?'
				rows=self.run_query(query,(nombre_produc,))
				for row in rows:
					a=row[1]
					b=row[2]
					c=row[3]
					d=row[4]
					e=row[5]
					f=row[6]
					g=row[7]
				query='UPDATE Previo_Pedido SET Cantidad=? WHERE Usuario_Cliente=? AND Nombre_Producto=? AND Codigo_Producto=? AND Precio=? AND Cantidad=? AND Total=? AND Imagen=?'
				parameters=(nueva_cantidad,a,b,c,d,e,f,g)
				self.run_query(query,parameters)
				self.editar_ventana.destroy()
				self.get_products()
		except:
			return		
				
		
	def compra(self):
		self.sumaMontos=0
		query='SELECT * FROM Previo_Pedido WHERE Usuario_Cliente=?'
		rows=self.run_query(query,(self.usuario,))
		for row in rows:
			self.sumaMontos+=row[6]

		self.proceso=Toplevel()
		self.ancho=550
		self.alto=250
		self.x=self.proceso.winfo_screenwidth()//2-self.ancho//2
		self.y=self.proceso.winfo_screenheight()//2-self.alto//2
		self.posicion=str(self.ancho)+"x"+str(self.alto)+"+"+str(self.x)+"+"+str(self.y)
		self.proceso.geometry(self.posicion)
		self.proceso.resizable(False,False)
		self.proceso.config(bg="#73C8BE")
		self.proceso.title('Proceso de compra')
		self.titulo=Label(self.proceso,text='INGRESA AQUÍ TU DIRECCIÓN DE ENVÍO')
		self.titulo.grid(pady=10)
		self.titulo.place(x=50,y=10)
		self.titulo.config(font=('Comic Sans MS', 14),bg="#73C8BE")

		frame=LabelFrame(self.proceso,text="")
		frame.place(x=20,y=60)
		#entrada para nombre
		self.nombresLabel=Label(frame,text='Nombres: ',bg='white',width=17).grid(row=1,column=0)
		self.nombres=Entry(frame)
		self.nombres.focus()
		self.nombres.grid(row=1,column=1)
		#entrada para apellido
		self.apellidosLabel=Label(frame,text='Apellidos: ',bg='white',width=17).grid(row=2,column=0)
		self.apellidos=Entry(frame)
		self.apellidos.focus()
		self.apellidos.grid(row=2,column=1)
		#entrada para pais
		self.paisLabel=Label(frame,text='País: ',bg='white',width=17).grid(row=1,column=2)
		self.pais=Entry(frame)
		self.pais.grid(row=1,column=3)
		#entrada para departamento
		self.departamentoLabel=Label(frame,text='Departamento: ',bg='white',width=17).grid(row=2,column=2)
		self.departamento=Entry(frame)
		self.departamento.grid(row=2,column=3)


		#entrada para provincia
		self.provinciaLabel=Label(frame,text='Provincia: ',bg='white',width=17).grid(row=4,column=0)
		self.provincia=Entry(frame)
		self.provincia.focus()
		self.provincia.grid(row=4,column=1)
		#entrada para distrito
		self.distritoLabel=Label(frame,text='Distrito: ',bg='white',width=17).grid(row=3,column=0)
		self.distrito=Entry(frame)
		self.distrito.focus()
		self.distrito.grid(row=3,column=1)
		#entrada para direccion
		self.direccionLabel=Label(frame,text='Direccion: ',bg='white',width=17).grid(row=3,column=2)
		self.direccion=Entry(frame)
		self.direccion.focus()
		self.direccion.grid(row=3,column=3)
		#entrada para monto pagar
		self.montoLabel=Label(frame,text='Monto pagar: ',bg='white',width=17).grid(row=5,column=0)
		self.monto=Entry(frame)
		Entry(frame,textvariable=StringVar(frame,value=self.sumaMontos),state='readonly').grid(row=5,column=1)

		#entrada para forma de pago
		self.formaLabel=Label(frame,text='Forma de pago: ',bg='white',width=17).grid(row=4,column=2)
		self.forma=Entry(frame)
		self.forma.grid(row=4,column=3)

		#boton agregar productos
		ttk.Button(frame,text="Pagar",command=lambda:self.pagar(self.nombres.get(),self.apellidos.get(),self.pais.get(),self.departamento.get(),self.provincia.get(),self.distrito.get(),self.direccion.get(),self.sumaMontos,self.forma.get())).grid(row=6,columnspan=4,sticky=W+E)
		#mensaje de agregado
		self.message=Label(self.proceso,text='',fg='red',bg='#73C8BE')
		self.message.place(x=20,y=200)
	def pagar(self,nombres,apellidos,pais,departamento,provincia,distrito,direccion,monto,forma):
		if len(nombres)!=0 and len(apellidos)!=0 and len(pais)!=0 and len(departamento)!=0 and len(provincia)!=0 and len(distrito)!=0 and len(direccion)!=0 and len(forma)!=0:
			
				query='INSERT INTO Pedido SELECT * FROM Previo_Pedido'
				self.run_query(query)
				now = datetime.datetime.now()
					
				query='INSERT INTO Pedido_Envio VALUES(NULL,?,?,?,?,?,?,?,?,?,?,?)'
				parameters=(self.usuario,monto,forma,str(now),direccion,nombres,apellidos,pais,departamento,provincia,distrito,)	
				self.run_query(query,parameters)


				'''query='SELECT * FROM Previo_Pedido'
																records=self.run_query(query)
												
												
																
																for element in records:
												
																	codigo=element[3]
																	cantidad=element[5]
																query='SELECT * FROM Producto WHERE Codigo=?'	
																rows=self.run_query(query,(codigo,))
																for row in rows:
																	a=row[1]
																	b=row[2]
																	c=row[3]
																	d=row[4]
																	e=row[5]
																query='UPDATE Producto SET Cantidad=? WHERE Codigo=? AND Nombre=? AND Precio=? AND Cantidad=? AND Imagen=?'
																parameters=(d-cantidad,a,b,c,d,e)
																self.run_query(query,parameters)
																if d-cantidad==0:
																	query='DELETE FROM Producto WHERE Codigo=?'
																	self.run_query(query,(codigo,))	
												'''
					


				
				query='DELETE FROM Previo_Pedido'
				self.run_query(query)	
				self.proceso.destroy()
			
		else:
			self.message['text']='Debe llenar los campos es requerido '


			