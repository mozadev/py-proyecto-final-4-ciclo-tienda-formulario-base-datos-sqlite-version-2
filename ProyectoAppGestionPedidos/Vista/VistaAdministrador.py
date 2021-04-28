from tkinter import *
from tkinter import filedialog,PhotoImage,messagebox
from PIL import Image,ImageTk
from Vista import VistaLoginAdministrador
from Modelo.ModeloProducto import *
from Modelo.ModeloCliente import *
from Modelo.ModeloAdmin import *
from Modelo.ModeloGestion import *
from Modelo.ModeloVentas import *
class ventanaADM(Frame):
    foto_binario=""
    base='database.db'
    def __init__(self,raiz,nombre):
        super().__init__(raiz)
        self.raiz=raiz
        self.raiz.resizable(False,False)
        self.nombre=nombre
        self.raiz.title("Sistema de ventas")
        ancho_ventana = 720
        alto_ventana = 500

        x_ventana = self.raiz.winfo_screenwidth() // 2 - ancho_ventana // 2
        y_ventana = self.raiz.winfo_screenheight() // 2 - alto_ventana // 2

        posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
        self.raiz.geometry(posicion)
        self.pack()
        self.widgets()
        self.place(relwidth=1, relheight=1)
        self.config(bg="white")
    def widgets(self):
        #imagenes para barra
        self.colorBarra=Label(self,bg="#FFA745", width=105,height=4)
        self.colorBarra.place(x=0,y=0)
        self.colorBarra.grid(sticky=E+W)
        #barra opcion 1
        self.imgvar1 = Image.open('imagenes/barraCliente4.png')
        self.imgvar1 = self.imgvar1.resize((40, 40), Image.ANTIALIAS) # Redimension (Alto, Ancho)
        self.imgvar1 = ImageTk.PhotoImage(self.imgvar1)
        self.mainmenu1 = Menubutton(self.raiz, image=self.imgvar1,compound="left",text="Archivo")
        self.mainmenu1.place(x=0,y=0)
        self.mainmenu1.config(bg="#FFA745", activebackground="#FFA745",border=0)
        self.submenu1 = Menu(self.mainmenu1, tearoff=0)
        self.mainmenu1.config(menu=self.submenu1)
        self.submenu1.config(bg="#FFA745", activebackground="#FFA745")
        self.submenu1.add_command(label="Mi cuenta",command=self.miCuenta)
        self.submenu1.add_command(label="Cerrar Sesión",command=self.cerrar_Sesion)
        self.submenu1.add_command(label="Salir",command=self.salir)

        #barra INICIO
        self.imgenInicio = Image.open('imagenes/imagenHome.png')
        self.imgenInicio = self.imgenInicio.resize((40, 40), Image.ANTIALIAS) # Redimension (Alto, Ancho)
        self.imgenInicio = ImageTk.PhotoImage(self.imgenInicio)

        self.botonCarrito=Button(self,image=self.imgenInicio,compound="left",text="Inicio", command=self.botonInicio)
        self.botonCarrito.place(x=100,y=0)
        self.botonCarrito.config(cursor="hand2",bg="#FFA745", activebackground="#FFA745",border=0)

        #barra opcion 3

        self.imgvar2 = Image.open('imagenes/barra2.png')
        self.imgvar2 = self.imgvar2.resize((40, 40), Image.ANTIALIAS) # Redimension (Alto, Ancho)
        self.imgvar2 = ImageTk.PhotoImage(self.imgvar2)

        self.botonVentas=Button(self,image=self.imgvar2,compound="left",text="Ventas", command=self.botonVentas)
        self.botonVentas.place(x=180,y=0)
        self.botonVentas.config(cursor="hand2",bg="#FFA745", activebackground="#FFA745",border=0)

        
        #barra opcion 4

        self.imgvar3 = Image.open('imagenes/barra3.png')
        self.imgvar3 = self.imgvar3.resize((40, 40), Image.ANTIALIAS) # Redimension (Alto, Ancho)
        self.imgvar3 = ImageTk.PhotoImage(self.imgvar3)

        self.botonReportes=Button(self,image=self.imgvar3,compound="left",text="Gestión", command=self.botonReportes)
        self.botonReportes.place(x=280,y=0)
        self.botonReportes.config(cursor="hand2",bg="#FFA745", activebackground="#FFA745",border=0)

  
        #barra opcion 5
        self.imgvar4 = Image.open('imagenes/barra4.png')
        self.imgvar4 = self.imgvar4.resize((40, 40), Image.ANTIALIAS) # Redimension (Alto, Ancho)
        self.imgvar4 = ImageTk.PhotoImage(self.imgvar4)
        self.mainmenu4 = Menubutton(self.raiz, image=self.imgvar4,compound="left",text="Mantenimiento")
        self.mainmenu4.place(x=370,y=0)
        self.mainmenu4.config(bg="#FFA745", activebackground="#FFA745",border=0)
        self.submenu4 = Menu(self.mainmenu4, tearoff=0)
        self.mainmenu4.config(menu=self.submenu4)
        self.submenu4.config(bg="#FFA745", activebackground="#FFA745")
        self.submenu4.add_command(label="Producto",command=self.producto)
        self.submenu4.add_command(label="Cliente",command=self.cliente)
        self.submenu4.add_command(label="Administrador",command=self.admin)


        self.botonInicio()
    def fondo(self):
        self.miImagen = Image.open('imagenes/fondoVentanaA.jpg')
        self.miImagen = self.miImagen.resize((720, 469), Image.ANTIALIAS)
        self.miImagen=ImageTk.PhotoImage(self.miImagen)
        self.fondoLb=Label(self.raiz,image=self.miImagen)
        self.fondoLb.place(x=0,y=54)
        self.fondoLb.config(border=0)    
    def run_query(self,query,parameters=()):
        with sqlite3.connect(self.base) as conn:
            cursor=conn.cursor()
            result=cursor.execute(query,parameters)
            conn.commit()
        return result    
    def miCuenta(self):
        self.fondo()
        self.editar_cliente()
    def editar_cliente(self):
        #consultando a la base de datos
        query='SELECT * FROM Administrador WHERE Usuario=?'   
        rows=self.run_query(query,(self.nombre,))
        for row in rows:
            usuario_antiguo=row[1]
            contrasenia_antiguo=row[2]
            dni_antiguo=row[3]
            telefono_antiguo=row[4]
            imagen_antigua=row[5]
        #creando labelframe
        self.editar_ventana=LabelFrame(text="")
        self.editar_ventana.place(x=0,y=60)
        self.editar_ventana.config(border=0)
        
        #imagen de fondo
        self.miImagen = Image.open('imagenes/fondoVentanaA.jpg')
        self.miImagen = self.miImagen.resize((720, 469), Image.ANTIALIAS)
        self.miImagen=ImageTk.PhotoImage(self.miImagen)
        self.fondoLb=Label(self.editar_ventana,image=self.miImagen)
        self.fondoLb.place(x=0,y=0)
        self.fondoLb.config(border=0)
        #titulo
        self.tituloPerfil=Label(self.editar_ventana,text="Perfil")
        self.tituloPerfil.grid(padx=10,pady=10,row=0,columnspan=4) 
        self.tituloPerfil.config(bg="white",fg="#273746",justify="center",font=('Comic Sans MS', 20))
        # codigo antiguo
        Label(self.editar_ventana,text='Usuario anterior: ',bg='white').grid(row=1,column=0)
        Entry(self.editar_ventana,textvariable=StringVar(self.editar_ventana,value=usuario_antiguo),state='readonly').grid(row=1,column=1)
        #codigo nuevo
        Label(self.editar_ventana,text='Usuario nuevo: ',bg='white').grid(row=2,column=0)
        self.nuevo_usuario=Entry(self.editar_ventana)
        self.nuevo_usuario.grid(row=2,column=1)
        #nombre antiguo
        Label(self.editar_ventana,text='Contraseña anterior: ',bg='white').grid(row=3,column=0)
        Entry(self.editar_ventana,textvariable=StringVar(self.editar_ventana,value=contrasenia_antiguo),state='readonly').grid(row=3,column=1)
        #nombre nuevo
        Label(self.editar_ventana,text='Contraseña nuevo: ',bg='white').grid(row=4,column=0)
        self.nuevo_contrasenia=Entry(self.editar_ventana)
        self.nuevo_contrasenia.grid(row=4,column=1)
        # precio antiguo
        Label(self.editar_ventana,text='DNI anterior: ',bg='white').grid(row=1,column=2)
        Entry(self.editar_ventana,textvariable=StringVar(self.editar_ventana,value=dni_antiguo),state='readonly').grid(row=1,column=3)
        #precio nuevo
        Label(self.editar_ventana,text='DNI nuevo: ',bg='white').grid(row=2,column=2)
        self.nuevo_dni=Entry(self.editar_ventana)
        self.nuevo_dni.grid(row=2,column=3)
        #cantidad antiguo
        Label(self.editar_ventana,text='Telefono anterior: ',bg='white').grid(row=3,column=2)
        Entry(self.editar_ventana,textvariable=StringVar(self.editar_ventana,value=telefono_antiguo),state='readonly').grid(row=3,column=3)
        #cantidad nuevo
        Label(self.editar_ventana,text='Telefono nuevo: ',bg='white').grid(row=4,column=2)
        self.nuevo_telefono=Entry(self.editar_ventana)
        self.nuevo_telefono.grid(row=4,column=3)
        

        #Imagen nuevo
        Label(self.editar_ventana,text='Imagen nueva: ',bg='white').grid(row=6,column=0)
        nuevo_imagen=ttk.Button(self.editar_ventana,text='Abrir archivo',command=self.abrirArchivo)
        nuevo_imagen.grid(row=6,column=1)
        #boton editar

        ttk.Button(self.editar_ventana,text="Editar",command=lambda:self.editar_fila(self.nuevo_usuario.get(),usuario_antiguo,self.nuevo_contrasenia.get(),contrasenia_antiguo,self.nuevo_dni.get(),dni_antiguo,self.nuevo_telefono.get(),telefono_antiguo,imagen_antigua)).grid(row=8,columnspan=4,sticky='WE')
        #mensaje
        self.message=Label(self.editar_ventana,text='',fg='red',bg='white')
        self.message.grid(row=9,column=0,columnspan=5,sticky='WE')

        #imagenes de decoracion
        with open(f'imagenes/imagen.jpg', 'wb') as f:
            f.write(imagen_antigua)   
        self.imagenPerfil = Image.open('imagenes/imagen.jpg')
        self.imagenPerfil = self.imagenPerfil.resize((220, 220), Image.ANTIALIAS)
        self.imagenPerfil = ImageTk.PhotoImage(self.imagenPerfil)     
        self.imgPerfilLabel=Label(self.editar_ventana,image=self.imagenPerfil)
        self.imgPerfilLabel.grid(row=1,column=4,rowspan=6,padx=20)
        self.imgPerfilLabel.config(border=0)

    def validacion(self):
        return len(self.nuevo_usuario.get())!=0 and len(self.nuevo_contrasenia.get())!=0 and len(self.nuevo_dni.get())!=0 and len(self.nuevo_telefono.get())!=0
    def editar_fila(self,nuevo_usuario,antiguo_usuario,nuevo_contrasenia,antiguo_contrasenia,nuevo_dni,antiguo_dni,nuevo_telefono,antiguo_telefono,antigua_imagen):
        global foto_binario
        if self.validacion():
            try:
                with open(foto_binario, 'rb') as f:
                    nueva_imagen= f.read()
                query='UPDATE Administrador SET Usuario=?,Contraseña=?,Dni=?,Telefono=?,Imagen=? WHERE Usuario=? AND Contraseña=? AND Dni=? AND Telefono=? AND Imagen=?' 
                parameters=(nuevo_usuario,nuevo_contrasenia,nuevo_dni,nuevo_telefono,nueva_imagen,antiguo_usuario,antiguo_contrasenia,antiguo_dni,antiguo_telefono,antigua_imagen,)
                self.run_query(query,parameters)
                self.message['text']=f'El usuario {antiguo_usuario} fue actualizad@ exitosamente'
                self.editar_ventana.destroy()
                self.miCuenta()
            except:
                self.message['text']='Debe llenar los campos es requerido'
                foto_binario="" 
        else:
            self.message['text']='Debe llenar los campos es requerido '
    def abrirArchivo(self):
        global foto_binario
        try:
            archivo=filedialog.askopenfilename(title="Abrir",initialdir="/",filetypes=(("Todos los ficheros","*.*"),
            ("Fichero de texto","*.txt"),("Fichero de Excel","*.xlsx")))  
            

            foto_binario=archivo
            return True
        except: 
            return False       

    def botonInicio(self):
        self.miImagen = Image.open('imagenes/fondoVentanaA.jpg')
        self.miImagen = self.miImagen.resize((720, 469), Image.ANTIALIAS)
        self.miImagen=ImageTk.PhotoImage(self.miImagen)
        self.fondoLb=Label(self.raiz,image=self.miImagen)
        self.fondoLb.place(x=0,y=54)
        self.fondoLb.config(border=0)

    def botonVentas(self):
        self.fondo()
        GestorPedido(self.raiz)

    def botonReportes(self):
        self.fondo()
        GestorEnvio(self.raiz)


    def producto(self):
        self.fondo()
        Productos(self.raiz)

    def cliente(self):
        self.fondo()
        Clientes(self.raiz)
    def admin(self):
        self.fondo()
        Admin(self.raiz)    
        
        
    def cerrar_Sesion(self):
        self.raiz.destroy()
        VistaLoginAdministrador.abrirLoginAdm()
    def salir(self):
        valor=messagebox.askquestion("Salir","¿Deseas salir de la aplicación?")
        if valor=="yes":
            self.raiz.destroy()

def abrirVentanaADM(nombre):
    raiz=Tk()
    aplicacion1=ventanaADM(raiz,nombre)
    aplicacion1.mainloop()