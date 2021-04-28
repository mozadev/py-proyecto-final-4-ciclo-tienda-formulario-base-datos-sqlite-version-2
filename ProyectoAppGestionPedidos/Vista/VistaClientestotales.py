from tkinter import *
from tkinter import filedialog,ttk,PhotoImage,messagebox
from PIL import Image,ImageTk
from Vista import VistaLoginCliente
import random
import sqlite3
from Vista import VistaCarritodeCompra
from Modelo.ModeloMuestraProducto import *
from Vista.VistaCarritodeCompra import Carrito


class ventanaCLIENTE(Frame):
    
    base='database.db'
    foto_binario=""
    def __init__(self,raiz,nombre):
        super().__init__(raiz)
        self.raiz=raiz
        self.raiz.resizable(False,False)
        self.nombre=nombre
        ancho_ventana = 720
        alto_ventana = 500

        x_ventana = self.raiz.winfo_screenwidth() // 2 - ancho_ventana // 2
        y_ventana = self.raiz.winfo_screenheight() // 2 - alto_ventana // 2

        posicion = str(ancho_ventana) + "x" + str(alto_ventana) + "+" + str(x_ventana) + "+" + str(y_ventana)
        self.titulo_Ventana()
        self.raiz.geometry(posicion)
        self.pack()
        self.widgets()
        self.place(relwidth=1, relheight=1)
        self.config(bg="white")
    def fondo(self):
        self.miImagen = Image.open('imagenes/fondoVentanaC.jpg')
        self.miImagen = self.miImagen.resize((720, 469), Image.ANTIALIAS)
        self.miImagen=ImageTk.PhotoImage(self.miImagen)
        self.fondoLb=Label(self.raiz,image=self.miImagen)
        self.fondoLb.place(x=0,y=54)
        self.fondoLb.config(border=0)
    def widgets(self):
        #imagenes para barra
        self.colorBarra=Label(self,bg="#CCF4DF", width=105,height=4)
        self.colorBarra.place(x=0,y=0)
        self.colorBarra.grid(sticky=E+W)
        
        #barra opcion 1
        self.imgvar1 = Image.open('imagenes/barraCliente4.png')
        self.imgvar1 = self.imgvar1.resize((40, 40), Image.ANTIALIAS) # Redimension (Alto, Ancho)
        self.imgvar1 = ImageTk.PhotoImage(self.imgvar1)
        self.mainmenu1 = Menubutton(self.raiz, image=self.imgvar1,compound="left",text="Archivo")
        self.mainmenu1.place(x=0,y=0)
        self.mainmenu1.config(bg="#CCF4DF", activebackground="#CCF4DF",border=0)
        self.submenu1 = Menu(self.mainmenu1, tearoff=0)
        self.mainmenu1.config(menu=self.submenu1)
        self.submenu1.config(bg="#CCF4DF", activebackground="#CCF4DF")
        self.submenu1.add_command(label="Mi cuenta",command=self.miCuenta)
        self.submenu1.add_command(label="Cerrar Sesión",command=self.cerrar_Sesion)
        self.submenu1.add_command(label="Salir",command=self.salir)
        
        #barra INICIO
        self.imgenInicio = Image.open('imagenes/imagenHome.png')
        self.imgenInicio = self.imgenInicio.resize((40, 40), Image.ANTIALIAS) # Redimension (Alto, Ancho)
        self.imgenInicio = ImageTk.PhotoImage(self.imgenInicio)

        self.botonCarrito=Button(self,image=self.imgenInicio,compound="left",text="Inicio", command=self.botonInicio)
        self.botonCarrito.place(x=100,y=0)
        self.botonCarrito.config(cursor="hand2",bg="#CCF4DF", activebackground="#CCF4DF",border=0)


        #barra opcion 2
        self.imgvar2 = Image.open('imagenes/barraCliente5.png')
        self.imgvar2 = self.imgvar2.resize((75, 40), Image.ANTIALIAS) # Redimension (Alto, Ancho)
        self.imgvar2 = ImageTk.PhotoImage(self.imgvar2)

        self.botonCarrito=Button(self,image=self.imgvar2,compound="left",text="Carrito", command=self.botonCarritoCompra)
        self.botonCarrito.place(x=180,y=0)
        self.botonCarrito.config(cursor="hand2",bg="#CCF4DF", activebackground="#CCF4DF",border=0)


        #barra opcion 3
        self.imgvar3 = Image.open('imagenes/barraCliente1.png')
        self.imgvar3 = self.imgvar3.resize((50, 40), Image.ANTIALIAS) # Redimension (Alto, Ancho)
        self.imgvar3 = ImageTk.PhotoImage(self.imgvar3)
        self.botonLocales=Button(self,image=self.imgvar3,compound="left",text="Locales", command=self.botonLocales)
        self.botonLocales.place(x=310,y=0)
        self.botonLocales.config(cursor="hand2",bg="#CCF4DF", activebackground="#CCF4DF",border=0)

        #barra opcion 4
        self.imgvar4 = Image.open('imagenes/barraCliente2.png')
        self.imgvar4 = self.imgvar4.resize((40, 40), Image.ANTIALIAS) # Redimension (Alto, Ancho)
        self.imgvar4 = ImageTk.PhotoImage(self.imgvar4)

        self.botonReparto=Button(self,image=self.imgvar4,compound="left",text="Zonas de Reparto", command=self.botonReparto)
        self.botonReparto.place(x=420,y=0)
        self.botonReparto.config( cursor="hand2",bg="#CCF4DF", activebackground="#CCF4DF",border=0)
        #barra opcion 5
        self.imgvar5 = Image.open('imagenes/barraCliente3.png')
        self.imgvar5 = self.imgvar5.resize((50, 40), Image.ANTIALIAS) # Redimension (Alto, Ancho)
        self.imgvar5 = ImageTk.PhotoImage(self.imgvar5)

        self.botonNosotros=Button(self,image=self.imgvar5,compound="left",text="Nosotros", command=self.botonNosotros)
        self.botonNosotros.place(x=580,y=0)
        self.botonNosotros.config( cursor="hand2",bg="#CCF4DF", activebackground="#CCF4DF",border=0)
        #..................botones de productos para agregar.......
        self.botonInicio()


        
        
    def run_query(self,query,parameters=()):
        with sqlite3.connect(self.base) as conn:
            cursor=conn.cursor()
            result=cursor.execute(query,parameters)
            conn.commit()
        return result

    def botonInicio(self):
        self.fondo()
        frame1=LabelFrame(text="")
        frame1.place(x=5,y=54)
        frame1.config(border=0)

        self.miImagen = Image.open('imagenes/fondoVentanaC.jpg')
        self.miImagen = self.miImagen.resize((720, 469), Image.ANTIALIAS)
        self.miImagen=ImageTk.PhotoImage(self.miImagen)
        self.fondoLb=Label(frame1,image=self.miImagen)
        self.fondoLb.place(x=0,y=0)
        self.fondoLb.config(border=0)
        #Buscador
        self.label_buscar=Label(frame1,text="Buscador:")
        self.label_buscar.grid(row=0,column=0,padx=10,sticky='ws',pady=10)   
        self.label_buscar.config(bg="white",fg="#273746")


        self.cuadroBuscar=Entry(frame1)
        self.cuadroBuscar.grid(row=1,column=0,padx=10,pady=10,sticky='w')
        self.cuadroBuscar.config(fg="green",font=('Arial', 13),width=17)
        self.botonBuscar=Button(frame1,text="Buscar", command=lambda:self.busquedaBoton(self.cuadroBuscar.get()))
        self.botonBuscar.grid(row=1,column=0,sticky='e')
        self.botonBuscar.config(font=('Comic Sans MS', 8),activeforeground="black", activebackground="white", bg="white", cursor="hand2",border=1)

        self.label_nombre_tienda=Label(frame1,text="Tienda Jockers")
        self.label_nombre_tienda.grid(row=0,column=1,padx=25,pady=10)   
        self.label_nombre_tienda.config(font=('Comic Sans MS', 13),bg="white",fg="#273746",justify="center")

        self.label_nombre_Lista=Label(frame1,text="Lista de Productos")
        self.label_nombre_Lista.grid(row=2,column=1,padx=25,pady=10)   
        self.label_nombre_Lista.config(font=('Comic Sans MS', 13),bg="white",fg="#273746",justify="center")



        self.imgTienda = Image.open('imagenes/tienda.jpg')
        self.imgTienda = self.imgTienda.resize((290, 125), Image.ANTIALIAS)
        self.imgTienda = ImageTk.PhotoImage(self.imgTienda)

        self.label_imagen_Tienda = Label(frame1,image = self.imgTienda)
        self.label_imagen_Tienda.grid(row=0,column=2,rowspan=3, sticky="NSEW",padx=10,pady=10)  
        self.label_imagen_Tienda.config(border=1) 

        '''------------------------------------------------------------------------------'''
        Productos(self.raiz,self.nombre)

    
    def botonCarritoCompra(self):
        self.fondo()
        Carrito(self.raiz,self.nombre)    

    

    def miCuenta(self):
        self.fondo()
        self.editar_cliente()


    def editar_cliente(self):
        #consultando a la base de datos
        query='SELECT * FROM Cliente WHERE Usuario=?'   
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
        self.miImagen = Image.open('imagenes/fondoVentanaC.jpg')
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
                query='UPDATE Cliente SET Usuario=?,Contraseña=?,Dni=?,Telefono=?,Imagen=? WHERE Usuario=? AND Contraseña=? AND Dni=? AND Telefono=? AND Imagen=?' 
                parameters=(nuevo_usuario,nuevo_contrasenia,nuevo_dni,nuevo_telefono,nueva_imagen,antiguo_usuario,antiguo_contrasenia,antiguo_dni,antiguo_telefono,antigua_imagen,)
                self.run_query(query,parameters)
                self.message['text']=f'El usuario {antiguo_usuario} fue actualizad@ exitosamente'
                self.editar_ventana.destroy()
                self.miCuenta()
                foto_binario="" 
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
    def busquedaBoton(self,nombreProducto):
        obj=Productos(self.raiz,self.nombre)
        obj.busqueda(nombreProducto)
    

   
    def botonLocales(self):
        frame=LabelFrame(text="")
        frame.place(x=5,y=54)
        frame.config(border=0)
        self.miImagen = Image.open('imagenes/fondoVentanaC.jpg')
        self.miImagen = self.miImagen.resize((720, 469), Image.ANTIALIAS)
        self.miImagen=ImageTk.PhotoImage(self.miImagen)
        self.fondoLb=Label(frame,image=self.miImagen)
        self.fondoLb.place(x=0,y=0)
        self.fondoLb.config(border=0)
        #Titulo
        self.local1=Label(frame,text="Locales")
        self.local1.grid(row=0,columnspan=2,padx=10,pady=9)   
        self.local1.config(bg="white",fg="#273746",justify="center",font=('Comic Sans MS', 20))
        #columna 1
        self.local2=Label(frame,text="Calle Las Begalias 541 San Isidro")
        self.local2.grid(row=1,column=0,padx=10,pady=5)   
        self.local2.config(bg="white",fg="#273746",justify="center",font=('Comic Sans MS', 12))
        

        self.img1 = Image.open('imagenes/Locales/Begonias.jpg')
        self.img1 = self.img1.resize((240, 140), Image.ANTIALIAS)
        self.img1 = ImageTk.PhotoImage(self.img1)

        self.label_imagen_Tienda = Label(frame,image = self.img1)
        self.label_imagen_Tienda.grid(row=2,column=0, sticky="NSEW",padx=54,pady=3)   

        self.local3=Label(frame,text="Av. Santa Cruz 669 Miraflores")
        self.local3.grid(row=3,column=0,padx=10,pady=5)   
        self.local3.config(bg="white",fg="#273746",justify="center",font=('Comic Sans MS', 12))
        self.img2 = Image.open('imagenes/Locales/SantaCruz.jpg')
        self.img2 = self.img2.resize((240, 140), Image.ANTIALIAS)
        self.img2 = ImageTk.PhotoImage(self.img2)

        self.label_imagen_Tienda = Label(frame,image = self.img2)
        self.label_imagen_Tienda.grid(row=4,column=0, sticky="NSEW",padx=54,pady=3)   

     
        
        #columna 2
        self.LBlocal2=Label(frame,text="Calle Los Nogales 901 La Molina")
        self.LBlocal2.grid(row=1,column=1,padx=40,pady=5)   
        self.LBlocal2.config(bg="white",fg="#273746",justify="center",font=('Comic Sans MS', 12))

        self.img3 = Image.open('imagenes/Locales/Nogales.jpg')
        self.img3 = self.img3.resize((240, 140), Image.ANTIALIAS)
        self.img3 = ImageTk.PhotoImage(self.img3)

        self.label_imagen_Tienda = Label(frame,image = self.img3)
        self.label_imagen_Tienda.grid(row=2,column=1, sticky="NSEW",padx=54)   


        self.LBlocal3=Label(frame,text="Jockey Plaza piso 1 n° 89 La Molina")
        self.LBlocal3.grid(row=3,column=1,padx=10,pady=5)   
        self.LBlocal3.config(bg="white",fg="#273746",justify="center",font=('Comic Sans MS', 12))

        self.img4 = Image.open('imagenes/Locales/Jockey.jpg')
        self.img4 = self.img4.resize((240, 140), Image.ANTIALIAS)
        self.img4 = ImageTk.PhotoImage(self.img4)

        self.label_imagen_Tienda = Label(frame,image = self.img4)
        self.label_imagen_Tienda.grid(row=4,column=1, sticky="NSEW",padx=54,pady=3)   


    def botonReparto(self):
        

        frame=LabelFrame(text="")
        frame.place(x=5,y=54)
        frame.config(border=0)
        self.miImagen = Image.open('imagenes/fondoVentanaC.jpg')
        self.miImagen = self.miImagen.resize((720, 469), Image.ANTIALIAS)
        self.miImagen=ImageTk.PhotoImage(self.miImagen)
        self.fondoLb=Label(frame,image=self.miImagen)
        self.fondoLb.place(x=0,y=0)
        self.fondoLb.config(border=0)
        #Titulo
        self.local1=Label(frame,text="Zonas de Reparto")
        self.local1.grid(row=0,column=0,padx=10,pady=10)   
        self.local1.config(bg="white",fg="#273746",justify="center",font=('Comic Sans MS', 20))

        self.img1 = Image.open('imagenes/Mapa.png')
        self.img1 = self.img1.resize((600, 332), Image.ANTIALIAS)
        self.img1 = ImageTk.PhotoImage(self.img1)

        self.label_imagen_Tienda = Label(frame,image = self.img1)
        self.label_imagen_Tienda.grid(row=1,column=0, sticky="NSEW",padx=50,pady=20)   

    def botonNosotros(self):
        frame=LabelFrame(text="")
        frame.place(x=5,y=54)
        frame.config(border=0)
        self.miImagen = Image.open('imagenes/fondoVentanaC.jpg')
        self.miImagen = self.miImagen.resize((720, 469), Image.ANTIALIAS)
        self.miImagen=ImageTk.PhotoImage(self.miImagen)
        self.fondoLb=Label(frame,image=self.miImagen)
        self.fondoLb.place(x=0,y=0)
        self.fondoLb.config(border=0)
        #Titulo
        self.local1=Label(frame,text="Cómo nació la tienda Jockers?")
        self.local1.grid(row=0,column=0,padx=10,pady=10)   
        self.local1.config(bg="white",fg="#273746",justify="center",font=('Comic Sans MS', 20))

        self.local2=Label(frame,text='''
            En el 2021, en plena pandemia, el dueño de la tienda Jockers se le ocurrió 
            la idea de lanzar su tienda por aplicativo online para facilitar las compras
            de víveres a los usuarios y así evitar que haya aglomeraciones masivas en su tienda,
            nace en el corazón de Miraflores y comenzaron a trabajar en su objetivo de facilitar
            las compras de los ciudadanos del Perú.
            ''')
        self.local2.grid(row=1,column=0,padx=10)   
        self.local2.config(bg="white",fg="#273746",justify="left",font=('Comic Sans MS', 10))

        self.img1 = Image.open('imagenes/Nosotros1.jpg')
        self.img1 = self.img1.resize((600, 200), Image.ANTIALIAS)
        self.img1 = ImageTk.PhotoImage(self.img1)

        self.label_imagen_Tienda = Label(frame,image = self.img1)
        self.label_imagen_Tienda.grid(row=2,column=0, sticky="NSEW",padx=50,pady=20)   



    def cerrar_Sesion(self):
        self.raiz.destroy()
        VistaLoginCliente.abrirLoginCliente()
    def salir(self):
        valor=VistaLoginCliente.messagebox.askquestion("Salir", "¿Deseas salir de la aplicación?")
        if valor=="yes":
            self.raiz.destroy()    
    def titulo_Ventana(self):
        self.raiz.title(f"Bienvenido {self.nombre}")   
           

def abrirVentanaCLIENTE(nombre):
    raiz=Tk()
    aplicacion1=VistaLoginCliente.ventanaCLIENTE(raiz, nombre)
    aplicacion1.mainloop()