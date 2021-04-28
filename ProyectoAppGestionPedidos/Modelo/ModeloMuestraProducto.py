from tkinter import *
from tkinter import filedialog,ttk,PhotoImage
from PIL import Image,ImageTk
import sqlite3
import random
class Productos(Frame):
    base='database.db'
    def __init__(self,raiz,nombre):
        self.raiz=raiz
        self.nombre=nombre
        #creando contenedor
        frame1=LabelFrame(text="",bg='white')
        frame1.place(x=5,y=200)
    
        self.message=Label(frame1,text='',fg='red',bg='white')
        self.message.grid(row=0,column=0,sticky=W+E)
        #creando tabla
        style=ttk.Style()
        style.configure('Treeview',rowheight=50)
        
        

        col = ('Codigo', 'Nombre','Precio', 'Cantidad')
        self.tree=ttk.Treeview(frame1,height=4,columns=col)
        self.tree.grid(row=1,columnspan=3)

        #self.tree.column('#0', width=150,anchor=CENTER)
        self.tree.column('#0', width=150,anchor=CENTER)
        self.tree.column('#1', width=150,anchor=CENTER)
        self.tree.column('#2', width=130,anchor=CENTER)
        self.tree.column('#3', width=130,anchor=CENTER)
        self.tree.column('#4', width=130,anchor=CENTER)

        self.tree.heading('#0',text='Producto')
        self.tree.heading('#1',text='Codigo')
        self.tree.heading('#2',text='Nombre')
        self.tree.heading('#3',text='Precio')
        self.tree.heading('#4',text='Cantidad')
        
        
        #botones 
        ttk.Button(frame1,text='Añadir al carrito',command=self.sumarAlCarrito).grid(row=5,columnspan=5,sticky=W+E)
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
    def sumarAlCarrito(self):
        self.message['text']=''
        try:
            self.tree.item(self.tree.selection())['values'][1]
        except IndexError as e:
            self.message['text']='Selecciona un valor'
            return
        nombre_produc=self.tree.item(self.tree.selection())['values'][1]
        self.procesoCarrito(nombre_produc)
    def procesoCarrito(self,nombre):
        #consultando a la base de datos
        query='SELECT * FROM Producto WHERE Nombre=?'
        rows=self.run_query(query,(nombre,))
        for row in rows:
            codigo_producto=row[1]
            nombre_producto=row[2]
            precio_producto=row[3]
            cantidad_producto=row[4]
            imagen_producto=row[5]
        if cantidad_producto>0:
            try:
                query='SELECT * FROM Previo_Pedido WHERE Nombre_Producto=?'
                rows=self.run_query(query,(nombre_producto,))
                for row in rows:
                    a=row[1]
                    b=row[2]
                    c=row[3]
                    d=row[4]
                    e=row[5]
                    f=row[6]
                    g=row[7]
                    
                if e<cantidad_producto:   
                    query='UPDATE Previo_Pedido SET Cantidad=? WHERE Usuario_Cliente=? AND Nombre_Producto=? AND Codigo_Producto=? AND Precio=? AND Cantidad=? AND Total=? AND Imagen=?' 
                    parameters=(e+1,a,b,c,d,e,f,g)
                    self.run_query(query,parameters)    
                else:
                    pass
            except:
                query='INSERT INTO Previo_Pedido VALUES(NULL,?,?,?,?,?,?)'
                parameters=(self.nombre,nombre_producto,codigo_producto,precio_producto,1,imagen_producto)
                self.run_query(query,parameters) 
                self.message['text']=f'El producto {nombre_producto} fue añadido al carrito exitosamente'         
        else:
            self.message['text']=f'El producto {nombre_producto} se ha agotado'
    def busqueda(self,nombreProducto):
        if nombreProducto!="":
            query='SELECT COUNT(*) FROM Producto WHERE Nombre =?'
            self.valor=self.run_query(query,(nombreProducto,)).fetchall()
            
            if self.valor[0]==(1,):
                #consultando a la base de datos
                query='SELECT * FROM Producto WHERE Nombre=?'
                rows=self.run_query(query,(nombreProducto,))
                #limpiando la tabla
                records=self.tree.get_children()
                for element in records:
                    self.tree.delete(element)
                for row in rows:
                    data=row[5]
                    with open(f'imagenes/imagen.jpg', 'wb') as f:
                        f.write(data)   
                    self.variable= Image.open(f'imagenes/imagen.jpg')
                    self.variable = self.variable.resize((50, 50), Image.ANTIALIAS)
                    self.variable = ImageTk.PhotoImage(self.variable)
                    self.tree.insert('',0,image=self.variable,values=(row[1],row[2],row[3],row[4]))
            else:
                self.message['text']=f'El producto no esta registrado'
                self.get_products()
        else:
            self.get_products()


                                          
