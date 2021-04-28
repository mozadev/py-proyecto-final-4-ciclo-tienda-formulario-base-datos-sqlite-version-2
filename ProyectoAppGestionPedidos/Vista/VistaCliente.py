from tkinter import *
from Modelo.ModeloCliente import *
from tkinter import PhotoImage
from PIL import Image,ImageTk
from Vista import  VistaLoginCliente
class Ventana_CRUD_CLIENTE(Frame):
    base='database.db'
    foto_binario=""
    def __init__(self,raiz):
        super().__init__(raiz)
        self.raiz=raiz
        self.raiz.resizable(False,False)
        self.raiz.title("Registar usuario")
        ancho_ventana = 720
        alto_ventana = 200


        x_ventana = self.raiz.winfo_screenwidth() // 2 - ancho_ventana // 2
        y_ventana = self.raiz.winfo_screenheight() // 2 - alto_ventana // 2

        posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
        self.raiz.geometry(posicion)
        
        self.pack()
       	self.widgets()
        self.place(relwidth=1, relheight=1)

        
    def widgets(self):
        self.miImagen1 = Image.open('imagenes/fondoNuevoUsuario.jpg')
        self.miImagen1 = self.miImagen1.resize((720, 200), Image.ANTIALIAS)
        self.miImagen1=ImageTk.PhotoImage(self.miImagen1)
        self.fondoLb1=Label(self,image=self.miImagen1)
        self.fondoLb1.place(x=0,y=0)
        self.fondoLb1.config(border=0)    

        self.img = Image.open('imagenes/flecha2.png')
        self.img = self.img.resize((30, 30), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.img)
        self.botonRegresar=Button(self,image=self.img,compound="none", command=self.botonRegresar)
        self.botonRegresar.grid(padx=10,pady=10)
        self.botonRegresar.config(font=('Comic Sans MS', 12), cursor="hand2",bg="white", activebackground="white",border=0)
        self.botonRegresar.place(x=0,y=0)

        self.titulo=Label(self,text='Registro')
        self.titulo.grid(pady=10)  
        self.titulo.place(x=310,y=10)
        self.titulo.config(font=('Comic Sans MS', 17),bg="white")  
        frame=LabelFrame(text="")
        frame.place(x=20,y=60)
        self.miImagen = Image.open('imagenes/fondoNuevoUsuario.jpg')
        self.miImagen = self.miImagen.resize((720, 200), Image.ANTIALIAS)
        self.miImagen=ImageTk.PhotoImage(self.miImagen)
        self.fondoLb=Label(frame,image=self.miImagen)
        self.fondoLb.place(x=0,y=0)
        self.fondoLb.config(border=0)    
        #entrada para codigo
        self.usuarioLabel=Label(frame,text='Usuario: ',bg='white',width=17).grid(row=1,column=0)
        self.usuario=Entry(frame)
        self.usuario.focus()
        self.usuario.grid(row=1,column=1)
        #entrada para nombre
        self.contraseniaLabel=Label(frame,text='Contraseña: ',bg='white',width=17).grid(row=2,column=0)
        self.contrasenia=Entry(frame)
        self.contrasenia.focus()
        self.contrasenia.grid(row=2,column=1)
        #entrada precio
        self.dniLabel=Label(frame,text='DNI: ',bg='white',width=17).grid(row=1,column=2)
        self.dni=Entry(frame)
        self.dni.grid(row=1,column=3)
        #entrada cantidad
        self.telefonoLabel=Label(frame,text='Telefono: ',bg='white',width=17).grid(row=2,column=2)
        self.telefono=Entry(frame)
        self.telefono.grid(row=2,column=3)
        #entrada imagen
        self.imagenLabel=Label(frame,text='Imagen: ',bg='white',width=14).grid(row=1,column=4)
        self.imagen=ttk.Button(frame,text='Abrir archivo',command=self.abrirArchivo).grid(row=1,column=5)
        #boton agregar productos
        ttk.Button(frame,text="Guardar",command=self.agregar_cliente).grid(row=3,columnspan=6,sticky=W+E)
        #mensaje de agregado
        self.message=Label(text='',fg='red',bg='white')
        self.message.place(x=20,y=150)

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
            
    def validacion(self):
        return len(self.usuario.get())!=0 and len(self.contrasenia.get())!=0 and len(self.dni.get())!=0 and len(self.telefono.get())!=0

    def agregar_cliente(self):
        global foto_binario
        if self.validacion():
            try:
                with open(foto_binario, 'rb') as f:
                    blob= f.read()
                query='INSERT INTO Cliente VALUES(NULL,?,?,?,?,?)'
                parameters=(self.usuario.get(),self.contrasenia.get(),self.dni.get(),self.telefono.get(),blob)
                self.run_query(query,parameters)
                self.message['text']=f'El cliente {self.usuario.get()} a sido agregado satisfactoriamente '
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
        



    def botonRegresar(self):
        self.raiz.destroy() 
        VistaLoginCliente.abrirLoginCliente()
def abrirRegistroCliente():
	raiz=Tk()
	obj=Ventana_CRUD_CLIENTE(raiz)
	obj.mainloop()		