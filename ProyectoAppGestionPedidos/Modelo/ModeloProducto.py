from tkinter import *
from tkinter import filedialog,ttk,PhotoImage
from PIL import Image,ImageTk
import sqlite3
import random
class Productos(Frame):
	base='database.db'
	foto_binario=""
	def __init__(self,raiz):
		self.raiz=raiz
		#creando contenedor
		frame=LabelFrame(text="Registra un nuevo producto",bg='white')
		frame.place(x=20,y=60)
		#entrada para codigo
		self.codigoLabel=Label(frame,text='Código: ',bg='white',width=14).grid(row=1,column=0)
		self.codigo=Entry(frame)
		self.codigo.focus()
		self.codigo.grid(row=1,column=1)
		#entrada para nombre
		self.nombreLabel=Label(frame,text='Nombre: ',bg='white',width=14).grid(row=2,column=0)
		self.nombre=Entry(frame)
		self.nombre.focus()
		self.nombre.grid(row=2,column=1)
		#entrada precio
		self.precioLabel=Label(frame,text='Precio: ',bg='white',width=14).grid(row=1,column=2)
		self.precio=Entry(frame)
		self.precio.grid(row=1,column=3)
		#entrada cantidad
		self.cantidadLabel=Label(frame,text='Cantidad: ',bg='white',width=14).grid(row=2,column=2)
		self.cantidad=Entry(frame)
		self.cantidad.grid(row=2,column=3)
		#entrada imagen
		self.imagenLabel=Label(frame,text='Imagen: ',bg='white',width=14).grid(row=1,column=4)
		self.imagen=ttk.Button(frame,text='Abrir archivo  ',command=self.abrirArchivo).grid(row=1,column=5)

		#self.imagen.grid(row=1,column=5)

		#boton agregar productos
		ttk.Button(frame,text="Guardar",command=self.agregar_producto).grid(row=3,columnspan=6,sticky=W+E)
	
		#mensaje de agregado
		self.message=Label(frame,text='',fg='red',bg='white')
		self.message.grid(row=4,column=0,columnspan=6)
		self.subTitulo=Label(frame,text='Registro de Producto',fg='red',bg='white')
		self.subTitulo.grid(row=5,column=0,columnspan=6)
		#creando tabla
		col = ('Codigo', 'Nombre','Precio', 'Cantidad')
		self.tree=ttk.Treeview(frame,height=4,columns=col)
		self.tree.grid(row=6,columnspan=6)
		#self.tree.column('#0', width=150,anchor=CENTER)
		self.tree.column('#0', width=150,anchor=CENTER)
		self.tree.column('#1', width=150,anchor=CENTER)
		self.tree.column('#2', width=130,anchor=CENTER)
		self.tree.column('#3', width=130,anchor=CENTER)
		self.tree.column('#4', width=130,anchor=CENTER)

		self.tree.heading('#0',text='Imagen')
		self.tree.heading('#1',text='Codigo')
		self.tree.heading('#2',text='Nombre')
		self.tree.heading('#3',text='Precio')
		self.tree.heading('#4',text='Cantidad')
		

		style=ttk.Style()
		style.configure('Treeview',rowheight=50)

		#botones 
		ttk.Button(frame,text='Borrar',command=self.eliminar_producto).grid(row=11,columnspan=6,sticky=W+E)
		ttk.Button(frame,text='Editar',command=self.editar_producto).grid(row=12,columnspan=6,sticky=W+E)
		

		#self.pack()
		#self.widgets()
		#self.place(relwidth=1, relheight=1)
		
		#Llenando las filas
		self.get_products()

	def abrirArchivo(self):
		global foto_binario
		try:
			archivo=filedialog.askopenfilename(title="Abrir",initialdir="/",filetypes=(("Todos los ficheros","*.*"),
			("Fichero de texto","*.txt"),("Fichero de Excel","*.xlsx")))  
			
			
			foto_binario=archivo
			return True
		except: 
			return False
	'''def convertir_a_binario(self,foto):
					with open(foto, 'rb') as f:
						blob= f.read()
					return blob	'''

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
		query='SELECT * FROM Producto' #ORDER BY Nombre DESC	
		rows=self.run_query(query)
		#rellenando los datos
		self.numeros=[]
		self.variables=[]
		
		i=0
		for row in rows:
			numero=random.randint(1, 50)
			self.variables.append('a'+str(numero))
			data=row[5]
			with open(f'imagenes/imagen.jpg', 'wb') as f:
				f.write(data)	
			self.variables[i] = Image.open(f'imagenes/imagen.jpg')
			self.variables[i] = self.variables[i].resize((50, 50), Image.ANTIALIAS)
			self.variables[i] = ImageTk.PhotoImage(self.variables[i])
			self.tree.insert('',i,image=self.variables[i],values=(row[1],row[2],row[3],row[4]))
			

			
			i+=1
			
	def validacion(self):
		return len(self.codigo.get())!=0 and len(self.nombre.get())!=0 and len(self.precio.get())!=0 and len(self.cantidad.get())!=0 

	def agregar_producto(self):
		global foto_binario
		if self.validacion():
			try:
				with open(foto_binario, 'rb') as f:
					blob= f.read()

				
				query='INSERT INTO Producto VALUES(NULL,?,?,?,?,?)'		
				parameters=(self.codigo.get(),self.nombre.get(),self.precio.get(),self.cantidad.get(),blob)
				self.run_query(query,parameters)
				self.message['text']=f'El producto {self.nombre.get()} a sido agregado satisfactoriamente '
				self.codigo.delete(0,END)
				self.nombre.delete(0,END)
				self.precio.delete(0,END)
				self.cantidad.delete(0,END)
				foto_binario=""
				
			except:
				self.message['text']='Debe llenar los campos es requerido'
				foto_binario=""
		else:
			self.message['text']='Debe llenar los campos es requerido'
		self.get_products()	

	def eliminar_producto(self):	
		self.message['text']=''
		try:
			self.tree.item(self.tree.selection())['values'][0]
		except IndexError as e:
			self.message['text']='Selecciona un valor'
			return
		self.message['text']=''	
		nombre=self.tree.item(self.tree.selection())['values'][0]
		query='DELETE FROM Producto WHERE Codigo=?'
		self.run_query(query,(nombre,))	
		self.message['text']=f'El valor {nombre} a sido eliminado satisfactoriamente'
		self.get_products()

	def editar_producto(self):
		self.message['text']=''
		try:
			self.tree.item(self.tree.selection())['values'][1]
		except IndexError as e:
			self.message['text']='Selecciona un valor'
			return
		codigo_antiguo=self.tree.item(self.tree.selection())['values'][0]
		nombre_antiguo=self.tree.item(self.tree.selection())['values'][1]
		precio_antiguo=self.tree.item(self.tree.selection())['values'][2]
		cantidad_antiguo=self.tree.item(self.tree.selection())['values'][3]
		self.editar_ventana=Toplevel()
		self.ancho=460
		self.alto=120
		self.x=self.editar_ventana.winfo_screenwidth()//2-self.ancho//2
		self.y=self.editar_ventana.winfo_screenheight()//2-self.alto//2
		self.posicion=str(self.ancho)+"x"+str(self.alto)+"+"+str(self.x)+"+"+str(self.y)
		self.editar_ventana.geometry(self.posicion)

		self.editar_ventana.title('Editar producto')
		# codigo antiguo
		Label(self.editar_ventana,text='Codigo anterior: ',bg='white').grid(row=0,column=0)
		Entry(self.editar_ventana,textvariable=StringVar(self.editar_ventana,value=codigo_antiguo),state='readonly').grid(row=0,column=1)
		#codigo nuevo
		Label(self.editar_ventana,text='Codigo nuevo: ',bg='white').grid(row=1,column=0)
		nuevo_codigo=Entry(self.editar_ventana)
		nuevo_codigo.grid(row=1,column=1)
		#nombre antiguo
		Label(self.editar_ventana,text='Nombre anterior: ',bg='white').grid(row=2,column=0)
		Entry(self.editar_ventana,textvariable=StringVar(self.editar_ventana,value=nombre_antiguo),state='readonly').grid(row=2,column=1)
		#nombre nuevo
		Label(self.editar_ventana,text='Nombre nuevo: ',bg='white').grid(row=3,column=0)
		nuevo_nombre=Entry(self.editar_ventana)
		nuevo_nombre.grid(row=3,column=1)
		# precio antiguo
		Label(self.editar_ventana,text='Precio anterior: ',bg='white').grid(row=0,column=2)
		Entry(self.editar_ventana,textvariable=StringVar(self.editar_ventana,value=precio_antiguo),state='readonly').grid(row=0,column=3)
		#precio nuevo
		Label(self.editar_ventana,text='Precio nuevo: ',bg='white').grid(row=1,column=2)
		nuevo_precio=Entry(self.editar_ventana)
		nuevo_precio.grid(row=1,column=3)
		#cantidad antiguo
		Label(self.editar_ventana,text='Cantidad anterior: ',bg='white').grid(row=2,column=2)
		Entry(self.editar_ventana,textvariable=StringVar(self.editar_ventana,value=cantidad_antiguo),state='readonly').grid(row=2,column=3)
		#cantidad nuevo
		Label(self.editar_ventana,text='Cantidad nueva: ',bg='white').grid(row=3,column=2)
		nuevo_cantidad=Entry(self.editar_ventana)
		nuevo_cantidad.grid(row=3,column=3)
		
		
		ttk.Button(self.editar_ventana,text="Editar",command=lambda:self.editar_fila(nuevo_codigo.get(),codigo_antiguo,nuevo_nombre.get(),nombre_antiguo,nuevo_precio.get(),precio_antiguo,nuevo_cantidad.get(),cantidad_antiguo)).grid(row=4,columnspan=6)
	def editar_fila(self,nuevo_codigo,antiguo_codigo,nuevo_nombre,antiguo_nombre,nuevo_precio,antiguo_precio,nuevo_cantidad,antiguo_cantidad):
		query='UPDATE Producto SET Codigo=?,Nombre=?,Precio=?,Cantidad=? WHERE Codigo=? AND Nombre=? AND Precio=? AND Cantidad=?' 
		parameters=(nuevo_codigo,nuevo_nombre,nuevo_precio,nuevo_cantidad,antiguo_codigo,antiguo_nombre,antiguo_precio,antiguo_cantidad)
		self.run_query(query,parameters)
		self.editar_ventana.destroy()
		self.message['text']=f'La fila {antiguo_nombre} fue actualizad@ exitosamente'
		self.get_products()
	



#if __name__=='__main__':
'''
def abrirCRUD():
	root=Tk()
	obj=Productos(root)
	obj.mainloop()
'''	
