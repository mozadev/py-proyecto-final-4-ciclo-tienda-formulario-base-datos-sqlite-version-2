from tkinter import ttk 
from tkinter import *
from tkinter import filedialog
from tkinter import PhotoImage
from PIL import Image,ImageTk
import sqlite3
import random
class Admin(Frame):
	base='database.db'
	foto_binario=""
	def __init__(self,raiz):
		self.raiz=raiz
		#creando contenedor
		frame=LabelFrame(text="Registra un nuevo administrador",bg='white')
		frame.place(x=20,y=60)
		#entrada para codigo
		self.usuarioLabel=Label(frame,text='Usuario: ',bg='white',width=14).grid(row=1,column=0)
		self.usuario=Entry(frame)
		self.usuario.focus()
		self.usuario.grid(row=1,column=1)
		#entrada para nombre
		self.contraseniaLabel=Label(frame,text='Contraseña: ',bg='white',width=14).grid(row=2,column=0)
		self.contrasenia=Entry(frame)
		self.contrasenia.focus()
		self.contrasenia.grid(row=2,column=1)
		#entrada precio
		self.dniLabel=Label(frame,text='DNI: ',bg='white',width=14).grid(row=1,column=2)
		self.dni=Entry(frame)
		self.dni.grid(row=1,column=3)
		#entrada cantidad
		self.telefonoLabel=Label(frame,text='Telefono: ',bg='white',width=14).grid(row=2,column=2)
		self.telefono=Entry(frame)
		self.telefono.grid(row=2,column=3)
		#entrada imagen
		self.imagenLabel=Label(frame,text='Imagen: ',bg='white',width=14).grid(row=1,column=4)
		self.imagen=ttk.Button(frame,text='Abrir archivo',command=self.abrirArchivo).grid(row=1,column=5)

		#boton agregar productos
		ttk.Button(frame,text="Guardar",command=self.agregar_cliente).grid(row=3,columnspan=6,sticky=W+E)
		#mensaje de agregado
		self.message=Label(frame,text='',fg='red',bg='white')
		self.message.grid(row=4,column=0,columnspan=6)
		self.subTitulo=Label(frame,text='Registro de Administrador',fg='red',bg='white')
		self.subTitulo.grid(row=5,column=0,columnspan=6)
		#creando tabla
		
		col = ('Usuario', 'Contraseña','DNI', 'Telefono')
		self.tree=ttk.Treeview(frame,height=4,columns=col)
		self.tree.grid(row=6,columnspan=6)
		self.tree.column('#0', width=150,anchor=CENTER)
		self.tree.column('#1', width=150,anchor=CENTER)
		self.tree.column('#2', width=130,anchor=CENTER)
		self.tree.column('#3', width=130,anchor=CENTER)
		self.tree.column('#4', width=130,anchor=CENTER)
		
		self.tree.heading('#0',text='Imagen')
		self.tree.heading('#1',text='Usuario')
		self.tree.heading('#2',text='Contraseña')
		self.tree.heading('#3',text='DNI')
		self.tree.heading('#4',text='Telefono')
		

		style=ttk.Style()
		style.configure('Treeview',rowheight=50)
		#botones 
		ttk.Button(frame,text='Borrar',command=self.eliminar_cliente).grid(row=11,columnspan=6,sticky=W+E)
		ttk.Button(frame,text='Editar',command=self.editar_cliente).grid(row=12,columnspan=6,sticky=W+E)
		

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
		query='SELECT * FROM Administrador'	
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
		return len(self.usuario.get())!=0 and len(self.contrasenia.get())!=0 and len(self.dni.get())!=0 and len(self.telefono.get())!=0

	def agregar_cliente(self):
		global foto_binario
		if self.validacion():
			try:
				with open(foto_binario, 'rb') as f:
					blob= f.read()
				query='INSERT INTO Administrador VALUES(NULL,?,?,?,?,?)'
				parameters=(self.usuario.get(),self.contrasenia.get(),self.dni.get(),self.telefono.get(),blob)
				self.run_query(query,parameters)
				self.message['text']=f'El administrador {self.usuario.get()} a sido agregado satisfactoriamente '
				self.usuario.delete(0,END)
				self.contrasenia.delete(0,END)
				self.dni.delete(0,END)
				self.telefono.delete(0,END)
				foto_binario=""
			except:
				self.message['text']='Debe llenar los campos es requerido'
				foto_binario=""	
		else:
			self.message['text']='Debe llenar los campos es requerido '
		self.get_products()	

	def eliminar_cliente(self):	
		self.message['text']=''
		try:
			self.tree.item(self.tree.selection())['values'][0]
		except IndexError as e:
			self.message['text']='Selecciona un valor'
			return
		self.message['text']=''	
		usuario=self.tree.item(self.tree.selection())['values'][0]
		query='DELETE FROM Administrador WHERE Usuario=?'
		self.run_query(query,(usuario,))	
		self.message['text']=f'El usuario {usuario} a sido eliminado satisfactoriamente'
		self.get_products()

	def editar_cliente(self):
		self.message['text']=''
		try:
			self.tree.item(self.tree.selection())['values'][1]
		except IndexError as e:
			self.message['text']='Selecciona un administrador'
			return
		usuario_antiguo=self.tree.item(self.tree.selection())['values'][0]
		contrasenia_antiguo=self.tree.item(self.tree.selection())['values'][1]
		dni_antiguo=self.tree.item(self.tree.selection())['values'][2]
		telefono_antiguo=self.tree.item(self.tree.selection())['values'][3]
		self.editar_ventana=Toplevel()
		self.ancho=460
		self.alto=120
		self.x=self.editar_ventana.winfo_screenwidth()//2-self.ancho//2
		self.y=self.editar_ventana.winfo_screenheight()//2-self.alto//2
		self.posicion=str(self.ancho)+"x"+str(self.alto)+"+"+str(self.x)+"+"+str(self.y)
		self.editar_ventana.geometry(self.posicion)

		self.editar_ventana.title('Editar administrador')
		# codigo antiguo
		Label(self.editar_ventana,text='Usuario anterior: ',bg='white').grid(row=0,column=0)
		Entry(self.editar_ventana,textvariable=StringVar(self.editar_ventana,value=usuario_antiguo),state='readonly').grid(row=0,column=1)
		#codigo nuevo
		Label(self.editar_ventana,text='Usuario nuevo: ',bg='white').grid(row=1,column=0)
		nuevo_usuario=Entry(self.editar_ventana)
		nuevo_usuario.grid(row=1,column=1)
		#nombre antiguo
		Label(self.editar_ventana,text='Contraseña anterior: ',bg='white').grid(row=2,column=0)
		Entry(self.editar_ventana,textvariable=StringVar(self.editar_ventana,value=contrasenia_antiguo),state='readonly').grid(row=2,column=1)
		#nombre nuevo
		Label(self.editar_ventana,text='Contraseña nuevo: ',bg='white').grid(row=3,column=0)
		nuevo_contrasenia=Entry(self.editar_ventana)
		nuevo_contrasenia.grid(row=3,column=1)
		# precio antiguo
		Label(self.editar_ventana,text='DNI anterior: ',bg='white').grid(row=0,column=2)
		Entry(self.editar_ventana,textvariable=StringVar(self.editar_ventana,value=dni_antiguo),state='readonly').grid(row=0,column=3)
		#precio nuevo
		Label(self.editar_ventana,text='DNI nuevo: ',bg='white').grid(row=1,column=2)
		nuevo_dni=Entry(self.editar_ventana)
		nuevo_dni.grid(row=1,column=3)
		#cantidad antiguo
		Label(self.editar_ventana,text='Telefono anterior: ',bg='white').grid(row=2,column=2)
		Entry(self.editar_ventana,textvariable=StringVar(self.editar_ventana,value=telefono_antiguo),state='readonly').grid(row=2,column=3)
		#cantidad nuevo
		Label(self.editar_ventana,text='Telefono nueva: ',bg='white').grid(row=3,column=2)
		nuevo_telefono=Entry(self.editar_ventana)
		nuevo_telefono.grid(row=3,column=3)
		
		
		ttk.Button(self.editar_ventana,text="Editar",command=lambda:self.editar_fila(nuevo_usuario.get(),usuario_antiguo,nuevo_contrasenia.get(),contrasenia_antiguo,nuevo_dni.get(),dni_antiguo,nuevo_telefono.get(),telefono_antiguo)).grid(row=4,columnspan=6)
	def editar_fila(self,nuevo_usuario,antiguo_usuario,nuevo_contrasenia,antiguo_contrasenia,nuevo_dni,antiguo_dni,nuevo_telefono,antiguo_telefono):
		query='UPDATE Administrador SET Usuario=?,Contraseña=?,Dni=?,Telefono=? WHERE Usuario=? AND Contraseña=? AND Dni=? AND Telefono=?' 
		parameters=(nuevo_usuario,nuevo_contrasenia,nuevo_dni,nuevo_telefono,antiguo_usuario,antiguo_contrasenia,antiguo_dni,antiguo_telefono)
		self.run_query(query,parameters)
		self.editar_ventana.destroy()
		self.message['text']=f'El usuario {antiguo_usuario} fue actualizad@ exitosamente'
		self.get_products()



