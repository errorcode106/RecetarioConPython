import tkinter as tk
from tkinter import ttk
import json
from tkinter.messagebox import askokcancel, showinfo
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
from datetime import date

class App(ttk.Frame):
    bandera = False    
    def __init__(self, parent):
        super().__init__(parent, padding=(20))
        self.parent = parent    # guardamos una referencia de la ventana ppal
        parent.title("Tus Recetas")
        parent.geometry("850x650+100+100")
        parent.resizable(False, False)

        self.atributo_receta()
        self.deshabilitar_campos()
        self.tabla_recetas()

    

    def atributo_receta(self):
        """Se establecen los labels,entrys, buttons de la pantalla principal"""

        def validar_entry_letras(text):
            """se verifica que el caracter ingresado sea una letra"""
            return not text.isdecimal()
        
        def validar_entry_numeros(text):
            """se verifica que el caracter ingresado sea un numero"""
            return text.isdecimal()
        
        self.label_nombre = tk.Label(self,text="Receta")
        self.label_nombre.grid(row = 0, column= 0, padx=10, pady=10)
        
        self.label_ingredientes = tk.Label(self, text="Ingredientes")
        self.label_ingredientes.grid(row = 1, column= 0, padx=10, pady=10)

        self.label_preparacion = tk.Label(self, text="Preparacion")
        self.label_preparacion.grid(row = 2, column= 0, padx=10, pady=10)

        self.label_tiempoPreparacion = tk.Label(self, text="Tiempo de Preparacion")
        self.label_tiempoPreparacion.grid(row = 3, column= 0, padx=10, pady=10)

        self.label_cartelito = tk.Label(self,text="* Ingrese el tiempo en minutos")
        self.label_cartelito.grid(row=3, column=3)
        

        self.label_tiempoCoccion = tk.Label(self, text="Tiempo de Coccion")
        self.label_tiempoCoccion.grid(row = 4, column= 0, padx=10, pady=10)

        self.label_cartelito2 = tk.Label(self,text="* Ingrese el tiempo en minutos")
        self.label_cartelito2.grid(row=4, column=3)
                                    
        self.label_imagen = tk.Label(self, text="Imagen")
        self.label_imagen.grid(row = 5, column= 0, padx=10, pady=10)

        self.label_fecha = tk.Label(self, text="Fecha")
        self.label_fecha.grid(row = 6, column= 0, padx=10, pady=10)
        
        self.nombre_receta = tk.StringVar()
        self.entry_nombre = tk.Entry(self, validate= "key", validatecommand=(self.parent.register(validar_entry_letras),"%S"), textvariable= self.nombre_receta)
        self.entry_nombre.config(width=50)
        self.entry_nombre.grid(row=0, column= 1,padx=10, pady=10,columnspan=2)
        
        self.ingredientes = tk.StringVar()
        self.entry_ingredientes = tk.Entry(self,textvariable=self.ingredientes)
        self.entry_ingredientes.config(width=50)
        self.entry_ingredientes.grid(row=1, column= 1,padx=10,pady=10,columnspan=2)

        self.preparacion = tk.StringVar()
        self.entry_preparacion = tk.Entry(self,textvariable=self.preparacion)
        self.entry_preparacion.config(width=50)
        self.entry_preparacion.grid(row=2, column= 1,padx=10, pady=10,columnspan=2)

        self.tiempoPrepa = tk.StringVar()
        self.entry_tiempoPrepa = tk.Entry(self, validate= "key", validatecommand=(self.parent.register(validar_entry_numeros),"%S"),textvariable=self.tiempoPrepa)
        self.entry_tiempoPrepa.config(width=50)
        self.entry_tiempoPrepa.grid(row=3, column= 1,padx=10, pady=10,columnspan=2)

        self.tiempoCoccion = tk.StringVar()
        self.entry_tiempoCoccion = tk.Entry(self, validate= "key", validatecommand=(self.parent.register(validar_entry_numeros),"%S"),textvariable=self.tiempoCoccion)
        self.entry_tiempoCoccion.config(width=50)
        self.entry_tiempoCoccion.grid(row=4, column= 1,padx=10, pady=10,columnspan=2)

        self.imagen = tk.StringVar()
        self.label_ruta_imagen = ttk.Label(self, textvariable=self.imagen)
        self.label_ruta_imagen.grid(row=5, column=1, columnspan=2, padx=5, pady=5)
        self.button_imagen = ttk.Button(self, text="Cargar Imagen", command=self.cargar_ruta)
        self.button_imagen.config(width=20)
        self.button_imagen.grid(row=5, column=2, padx=10, pady=10, columnspan=2)

        self.fecha = tk.StringVar()
        self.entry_fecha = tk.Entry(self,textvariable=self.fecha)
        self.entry_fecha.config(width=50)
        self.entry_fecha.grid(row=6, column= 1,padx=10, pady=10,columnspan=2)
        

        self.boton_nuevo = tk.Button(self, text= "Nueva Receta",command=self.habilitar_campos)
        self.boton_nuevo.config(width=20)
        self.boton_nuevo.grid(row = 7 , column=0)

        self.boton_editar = tk.Button(self, text= "Modificar",command=self.modificar_receta)
        self.boton_editar.config(width=20)
        self.boton_editar.grid(row = 7 , column=1)

        self.boton_Guardar = tk.Button(self, text= "Guardar",command= self.guardar_receta)
        self.boton_Guardar.config(width=18)
        self.boton_Guardar.grid(row = 7 , column=2)

        self.boton_cancelar = tk.Button(self, text= "Cancelar",command=self.deshabilitar_campos)
        self.boton_cancelar.config(width=18)
        self.boton_cancelar.grid(row = 7 , column=3)

        self.label_vacio = tk.Label(self, text=())
        self.label_vacio.grid(row = 8, column= 0, padx=10, pady=2)

    def modificar_receta(self):
        """el metodo sirve cargar una ves seleccionada una receta se carguen los datos para luego modificar"""
        self.bandera = True
        self.boton_nuevo.config(state="disabled")
        self.habilitar_campos()
        self.entry_fecha.config(state="disabled")
        seleccion = self.tabla.selection()
        # si selection() devuelve una tupla vacia, no hay seleccion
        if seleccion:
            for item_id in seleccion:
                item = self.tabla.item(item_id) # obtenemos el item y sus datos
                
            self.id_receta = item['values'][0] # capturo el id del registro
            
            with open("recetitas.json", 'r') as archivo:
                try:
                    recetas = json.load(archivo)
                except ValueError:
                    recetas = []
            
            lista_recetas=[]
            
            for receta in recetas:
                lista_recetas.append((receta["id"], receta["nombre"], receta["ingredientes"], receta["preparacion"], receta["imagen"],receta["tiempoPreparacion"], receta["tiempoCoccion"], receta["fechaCreacion"],))
            receta_buscada=[]
            for item in lista_recetas:
                if item[0] == self.id_receta:
                    receta_buscada.append(item[0])
                    receta_buscada.append(item[1])
                    receta_buscada.append(item[2])
                    receta_buscada.append(item[3])
                    receta_buscada.append(item[4])
                    receta_buscada.append(item[5])
                    receta_buscada.append(item[6])
                    receta_buscada.append(item[7])      

            self.entry_nombre.insert(0,receta_buscada[1])
            self.entry_ingredientes.insert(0,receta_buscada[2])
            self.entry_preparacion.insert(0,receta_buscada[3])
            self.imagen.set(receta_buscada[4])
            self.entry_tiempoPrepa.insert(0,receta_buscada[5])
            self.entry_tiempoCoccion.insert(0,receta_buscada[6])
            self.entry_fecha.insert(0,receta_buscada[7])
            
        else:
            showinfo(message="Debe seleccionar una fila primero de lo contrario debe agregar una receta")
            self.deshabilitar_campos()
            
    def cargar_ruta(self):
        """carga la ruta de la imagen de la receta"""
        tipos = (('Archivos de texto', '*.jpg'),
                 ('Todos los archivos', '*.*'))
        self.ruta_archivo = askopenfilename(filetypes=tipos, initialdir="./imagenes/")
        print(self.ruta_archivo)
        self.imagen.set(self.ruta_archivo)
        
         
    def guardar_receta(self):
        """guarda la receta, llama al metodo guardar para append al archivo existente y tambien llama
        a recargar_lista_tabla para actualizar la tabla"""
        with open("recetitas.json", 'r') as archivo:
            try:
                recetitas = json.load(archivo)
            except ValueError:
                recetitas = []
      
        if recetitas == []:
            nro_id = 1000
            recetas = Receta()
            recetas.set_id_receta(nro_id)
            recetas.set_nombre(self.nombre_receta.get())
            recetas.set_ingredientes(self.ingredientes.get())
            recetas.set_preparacion(self.preparacion.get())
            recetas.set_imagen(self.imagen.get())
            recetas.set_tiempoPreparacion(self.tiempoPrepa.get())
            recetas.set_tiempoCoccion(self.tiempoCoccion.get())
            recetas.set_fechaCreacion(self.fecha.get())
            recetas.guardar()
            self.recargar_lista_tabla()

        elif  self.bandera == True:
                id_modificado = self.id_receta
                recetas = Receta()
                recetas.set_id_receta(self.id_receta)
                recetas.set_nombre(self.nombre_receta.get())
                recetas.set_ingredientes(self.ingredientes.get())
                recetas.set_preparacion(self.preparacion.get())
                recetas.set_imagen(self.imagen.get())
                recetas.set_tiempoPreparacion(self.tiempoPrepa.get())
                recetas.set_tiempoCoccion(self.tiempoCoccion.get())
                recetas.set_fechaCreacion(self.fecha.get())
                recetas.guardar_modificar(id_modificado)
            
                for item in self.tabla.get_children():
                    self.tabla.delete(item)
                
                self.bandera=False
                self.mostrar_lista()        
        else: 
            info = recetitas[len(recetitas)-1]
            nro_id = (info["id"]+1)

            recetas = Receta()
            recetas.set_id_receta(nro_id)
            recetas.set_nombre(self.nombre_receta.get())
            recetas.set_ingredientes(self.ingredientes.get())
            recetas.set_preparacion(self.preparacion.get())
            recetas.set_imagen(self.imagen.get())
            recetas.set_tiempoPreparacion(self.tiempoPrepa.get())
            recetas.set_tiempoCoccion(self.tiempoCoccion.get())
            recetas.set_fechaCreacion(self.fecha.get())
            recetas.guardar()
            self.recargar_lista_tabla()

        self.deshabilitar_campos()
        self.boton_nuevo.config(state="normal")
        self.boton_editar.config(state="normal")
        self.bandera=False

    def habilitar_campos(self):
        """habilita los entry y los botones"""
        self.entry_nombre.config(state="normal")
        self.entry_ingredientes.config(state="normal")
        self.entry_preparacion.config(state="normal")
        self.entry_tiempoPrepa.config(state="normal")
        self.entry_tiempoCoccion.config(state="normal")
        self.button_imagen.config(state="normal")
        self.entry_fecha.config(state="normal")
        self.entry_fecha.insert(0,date.today())

        self.boton_Guardar.config(state="normal")
        self.boton_cancelar.config(state="normal")

        self.boton_editar.config(state="disabled")

    def deshabilitar_campos(self):
        """deshabilita los entry y los botones"""
        self.nombre_receta.set("")
        self.ingredientes.set("")
        self.preparacion.set("")
        self.tiempoPrepa.set("")
        self.tiempoCoccion.set("")
        self.imagen.set("")
        self.button_imagen
        self.fecha.set("")

        self.entry_nombre.config(state="disabled")
        self.entry_ingredientes.config(state="disabled")
        self.entry_preparacion.config(state="disabled")
        self.entry_tiempoPrepa.config(state="disabled")
        self.entry_tiempoCoccion.config(state="disabled")
        self.button_imagen.config(state="disabled")
        self.entry_fecha.config(state="disabled")

        self.boton_Guardar.config(state="disabled")
        self.boton_cancelar.config(state="disabled")   

        self.boton_nuevo.config(state="normal")
        self.boton_editar.config(state="normal")
        if self.bandera:
            self.bandera = False 

    def tabla_recetas(self):
        """definimos la tabla"""
        # definimos tabla y barra de desplazamiento
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0) # wight=0 no cambia de tamaño nunca
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        # definimos las columnas de la tabla
        columnas = ('id', 'nombre_receta', 'tiempo_preparacion', 'tiempo_coccion')

        self.tabla = ttk.Treeview(self, columns=columnas,show='headings',selectmode="browse") # sin multi-seleccion
        self.tabla.grid(row=9, column=0, columnspan=4, sticky=(tk.NSEW))

        self.tabla.heading('id', text= 'ID')
        self.tabla.heading('nombre_receta', text='Nombre')
        self.tabla.heading('tiempo_preparacion', text='Tiempo prep.')
        self.tabla.heading('tiempo_coccion', text='Tiempo cocc.')

        # agregar barra de desplazamiento
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscroll=scrollbar.set) # la enlazamos al treeview
        scrollbar.grid(row=9, column=4, sticky=tk.NS)

        self.boton_mostrar = tk.Button(self, text= "Ver", command= self.ver_receta)
        self.boton_mostrar.config(width=20)
        self.boton_mostrar.grid(row = 11 , column=0)

        self.boton_eliminar = tk.Button(self, text= "Eliminar",command=self.boton_eliminar)
        self.boton_eliminar.config(width=20)
        self.boton_eliminar.grid(row = 11 , column=1)

        self.mostrar_lista()


    def ver_receta(self):
        seleccion = self.tabla.selection()
        # si selection() devuelve una tupla vacia, no hay seleccion
        if seleccion:
            for item_id in seleccion:
                item = self.tabla.item(item_id) # obtenemos el item y sus datos
                id_receta = item['values'][0] # capturo el id de mi registro
                       
            with open("recetitas.json", 'r') as archivo:
                try:
                    recetas = json.load(archivo)
                except ValueError:
                    recetas = []
            
            lista_recetas=[]
            for receta in recetas:
                lista_recetas.append((receta["id"], receta["nombre"], receta["ingredientes"], receta["preparacion"], receta["imagen"],receta["tiempoPreparacion"], receta["tiempoCoccion"], receta["fechaCreacion"],))
            receta_buscada=[]
            for item in lista_recetas:
                if item[0] == id_receta:
                    receta_buscada.append(item[0])
                    receta_buscada.append(item[1])
                    receta_buscada.append(item[2])
                    receta_buscada.append(item[3])
                    receta_buscada.append(item[4])
                    receta_buscada.append(item[5])
                    receta_buscada.append(item[6])
                    receta_buscada.append(item[7])
                 
            # como padre indicamos la ventana principal
            toplevel = tk.Toplevel(self.parent)
            VentanaMostrarReceta(toplevel,receta_buscada).grid()
                
        else:
            showinfo(message="Debe seleccionar una fila primero de lo contrario debe agregar una receta")

    def mostrar_lista(self):
        """leemos los datos y añadimos a la ventana secundaria"""
        with open("recetitas.json", 'r') as archivo:
            try:
                recetas = json.load(archivo)
            except ValueError:
                recetas = []
        lista_recetas = []
        #generamos los datos
        for receta in recetas:
            lista_recetas.append((receta["id"], receta["nombre"], receta["tiempoPreparacion"], receta["tiempoCoccion"]))
            
        for receta in lista_recetas:
            self.tabla.insert('', tk.END, values=receta)   

    def recargar_lista_tabla(self):
        """ generamos los datos de la lista y agregamos la nueva receta a la plantalla"""
        with open("recetitas.json", 'r') as archivo:
            try:
                recetas = json.load(archivo)
            except ValueError:
                recetas = []
        lista_recetas = []
        #generamos los datos de la lista
        for receta in recetas:
            lista_recetas.append((receta["id"], receta["nombre"], receta["tiempoPreparacion"], receta["tiempoCoccion"], receta["fechaCreacion"]))
        #agregamos la nueva receta a la plantalla
        self.tabla.insert('', tk.END, values=lista_recetas[len(lista_recetas)-1])

    def boton_eliminar(self):
        seleccion = self.tabla.selection()
        # si selection() devuelve una tupla vacia, no hay seleccion
        if seleccion:
            for item_id in seleccion:
                 item = self.tabla.item(item_id) # obtenemos el item y sus datos
                 fila = item['values']
                 res = askokcancel(title="Eliminar fila",message=("¿Desea eliminar esta receta?""\n" + "".join(fila[1])))

                 if res:
                    self.tabla.delete(item_id)
                    self.eliminar_receta(fila[0])
        else:
            showinfo(message="Debe seleccionar una fila primero de lo contrario debe agregar una receta")

    def eliminar_receta(self,elemento):
        """leemos los datos, buscamos en q posicion esta el elemento para luego borrar de la lista y por ultimo guardar en json """
        with open("recetitas.json", 'r') as archivo:
            try:
                recetas = json.load(archivo)
            except ValueError:
                recetas = []
        for i in range(0,(len(recetas))):
            buscando = recetas[i]
            for valores in buscando.values():
                if (valores == elemento):
                    posicion = i

        recetas.remove(recetas[posicion])
        with open("recetitas.json","w") as archivo:
            json.dump(recetas,archivo,indent = 4)
                
class VentanaMostrarReceta(ttk.Frame):
    def __init__(self, parent, receta_a_mostrar):
        super().__init__(parent, padding=(20))
        parent.title("Ventana Secundaria")
        parent.geometry("700x650+200+120")
        
        parent.resizable(False, False)
        self.focus()
        self.grab_set()

        receta = receta_a_mostrar
        
        self.label_nombre = tk.Label(self,text="Receta: ")
        self.label_nombre.grid(row = 0, column= 0, padx=10, pady=10)
        
        self.label_ingredientes = tk.Label(self, text="Ingredientes: ")
        self.label_ingredientes.grid(row = 1, column= 0, padx=10, pady=10)

        self.label_preparacion = tk.Label(self, text="Preparacion: ")
        self.label_preparacion.grid(row = 2, column= 0, padx=10, pady=10)

        self.label_tiempoPreparacion = tk.Label(self, text="Tiempo de Preparacion: ")
        self.label_tiempoPreparacion.grid(row = 3, column= 0, padx=10, pady=10)
                                    
        self.label_tiempoCoccion = tk.Label(self, text="Tiempo de Coccion: ")
        self.label_tiempoCoccion.grid(row = 4, column= 0, padx=10, pady=10)
                                    
        self.label_fecha = tk.Label(self, text="Fecha: ")
        self.label_fecha.grid(row = 6, column= 0, padx=10, pady=10)
        
        self.entry_nombre = tk.Entry(self)
        self.entry_nombre.grid(row=0, column= 1,padx=10, pady=10,columnspan=2)
        self.entry_nombre.insert(0,receta[1])
        self.entry_nombre.config(width=50, state="readonly")

        self.entry_ingredientes = tk.Entry(self)
        self.entry_ingredientes.grid(row=1, column= 1,padx=10,pady=10,columnspan=2)
        self.entry_ingredientes.insert(0,receta[2])
        self.entry_ingredientes.config(width=50, state="readonly")

        self.entry_preparacion = tk.Entry(self)
        self.entry_preparacion.grid(row=2, column= 1,padx=10, pady=10,columnspan=2)
        self.entry_preparacion.insert(0,receta[3])
        self.entry_preparacion.config(width=50, state="readonly")

        self.entry_tiempoPrepa = tk.Entry(self)
        self.entry_tiempoPrepa.grid(row=3, column= 1,padx=10, pady=10,columnspan=2)
        self.entry_tiempoPrepa.insert(0,receta[5])
        self.entry_tiempoPrepa.config(width=50, state="readonly")

        self.entry_tiempoCoccion = tk.Entry(self)
        self.entry_tiempoCoccion.grid(row=4, column= 1,padx=10, pady=10,columnspan=2)
        self.entry_tiempoCoccion.insert(0,receta[6])
        self.entry_tiempoCoccion.config(width=50, state="readonly")
        
        self.entry_fecha = tk.Entry(self)
        self.entry_fecha.grid(row=6, column= 1,padx=10, pady=10,columnspan=2)
        self.entry_fecha.insert(0,receta[7])
        self.entry_fecha.config(width=50, state="readonly")
        
        if receta[4] != "":
            self.image = Image.open(f"{receta[4]}")
            self.image = self.image.resize((330, 330), Image.ANTIALIAS)
            self.python_image = ImageTk.PhotoImage(self.image)
            ttk.Label(self, image=self.python_image).grid(row=7, column=1, columnspan=4, sticky=tk.EW, padx=5, pady=5)
        
        ttk.Button(self, text="Cerrar", command=parent.destroy).grid(row= 9, column=3, columnspan=2, padx=0, pady=10)              

class Receta:
    """ definicion de la clase receta"""
    def __init__(self):
        self.nombre = ""
        self.ingredientes = ""
        self.preparacion = ""
        self.imagen = ""
        self.tiempoPreparacion = ""
        self.tiempoCoccion = ""
        self.fechaCreacion = ""
        self.id_receta = 1000

    def set_id_receta(self,id):
        """metodo para agregar el valor al atributo id de la clase Receta"""
        self.id_receta = id

    def set_nombre(self, nombre):
        """metodo para agregar el valor al atributo nombre de la clase Receta"""
        self.nombre = nombre

    def set_ingredientes(self,ingredientes):
        """metodo para agregar el valor al atributo ingredientes de la clase Receta"""
        self.ingredientes = ingredientes
    
    def set_preparacion(self,preparacion):
        """metodo para agregar el valor al atributo preparacion de la clase Receta"""
        self.preparacion = preparacion
    
    def set_imagen(self,imagen = None):
        """metodo para agregar el valor al atributo imagen de la clase Receta, puede estar vacio"""
        self.imagen = imagen

    def set_tiempoPreparacion(self,tiempoPreparacion):
        """metodo para agregar el valor al atributo tiempoCreacion de la clase Receta"""
        self.tiempoPreparacion = tiempoPreparacion

    def set_tiempoCoccion(self,tiempoCoccion):
        """metodo para agregar el valor al atributo tiempoCoccion de la clase Receta"""
        self.tiempoCoccion = tiempoCoccion

    def set_fechaCreacion(self,fechaCreacion=None):
        """metodo para agregar el valor al atributo fechaCreacion de la clase Receta"""
        self.fechaCreacion = fechaCreacion
 
    def guardar(self):
        """metodo para guardar cada receta nueva q se agrega"""
        with open("recetitas.json","r") as archivo:
            try:
                recetas = json.load(archivo) #deserializa el archivo
            except ValueError:
                recetas= [] 
        receta =  {}
        receta["id"] = self.id_receta
        receta["nombre"] = self.nombre
        receta["ingredientes"] = self.ingredientes
        receta["preparacion"] = self.preparacion
        receta["imagen"] = self.imagen
        receta["tiempoPreparacion"] = self.tiempoPreparacion
        receta["tiempoCoccion"] = self.tiempoCoccion
        receta["fechaCreacion"] = self.fechaCreacion
        recetas.append(receta)
        with open("recetitas.json","w") as archivo:
            json.dump(recetas,archivo,indent = 4)

    def guardar_modificar(self,id_receta):
        """metodo para guardar luego de modificar la  receta seleccionada"""
        with open("recetitas.json", 'r') as archivo:
            try:
                recetas = json.load(archivo)
            except ValueError:
                pass
        aux = []
        for elem in recetas:
            if elem['id'] != id_receta:
                aux.append(elem)
            else:
                receta = {}
                receta["id"] = self.id_receta
                receta["nombre"] = self.nombre
                receta["ingredientes"] = self.ingredientes
                receta["preparacion"] = self.preparacion
                receta["imagen"] = self.imagen
                receta["tiempoPreparacion"] = self.tiempoPreparacion
                receta["tiempoCoccion"] = self.tiempoCoccion
                receta["fechaCreacion"] = self.fechaCreacion
                aux.append(receta)
        recetas = aux
        with open("recetitas.json", 'w') as archivo:
            json.dump(recetas, archivo,indent=4)

root = tk.Tk()
App(root).grid()
root.mainloop()