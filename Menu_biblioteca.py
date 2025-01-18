import sqlite3
import re
from datetime import datetime, timedelta
from tabulate import tabulate

conn=sqlite3.connect('Gestion_biblioteca.db')
cursor=conn.cursor()

#Funcion para agragar un libro a la tabla Libros
def Agregar_libro(titulo,autor,genero,año):
    try:
        cursor.execute('INSERT INTO Libros (titulo,autor,genero,año_publicacion,estado) VALUES (?,?,?,?,?)',(titulo,autor,genero,año,'Disponible'))
        conn.commit()
        print("Libro agregado exitosamente.")
    except Exception as e:
        print(f"Error al agregar un libro: {e}")
    
#Funcion para mostrar la tabla Libros
def Lista_libros():
    try:
        cursor.execute('SELECT * FROM Libros')
        libros= cursor.fetchall()
        if libros:
            print(tabulate(libros,headers=["ID", "Titulo", "Autor", "Genero", "Año", "Estado"], tablefmt="grid"))
        else:
            print("No hay libros registrados.")
    except Exception as e:
        print(f"Error al listar los libros: {e}")

#Funcion para validar correo
def El_correo_es_valido(correo):
    patron= r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(patron, correo) is not None

#Funcion para registrar un usuario a la tabla Usuarios
def Registrarse(nombre, correo):
    try:
        # Validar el correo antes de registrarlo
        if not El_correo_es_valido(correo):
            print("El correo ingresado no es válido. Intenta nuevamente.")
            return
        
        #Agraga un nuevo usuario
        cursor.execute('INSERT INTO Usuarios (nombre, correo) VALUES (?, ?)',(nombre, correo))
        conn.commit()
        print(f"Usuario {nombre} registrado correctamente.")
    except Exception as e:
        print(f"Error al registrar el usuario: {e}")
    
#funcion para Registrar un prestamo en la tabla Prestamos
def Registrar_prestamo(usuario_id,libro_id):
    try:
        # Verifica si el usuario existe
        cursor.execute('SELECT 1 FROM Usuarios WHERE id_usuario = ?', (usuario_id,))
        if not cursor.fetchone():
            print("El usuario no existe.")
            return

        # Verifica si el libro existe
        cursor.execute('SELECT 1 FROM Libros WHERE id_libro = ?', (libro_id,))
        if not cursor.fetchone():
            print("El libro no existe.")
            return
        
        #Verifica si el usuario ya tiene un prestamo activo del mismo libro
        cursor.execute(
            'SELECT 1 FROM Prestamos WHERE id_usuario = ? AND id_libro = ? AND estado = "Activo"',
            (usuario_id, libro_id)
        )
        if cursor.fetchone():
            print("El usuario ya tiene un prestamo activo para este libro.")
            return
        
        #Verifica el estado del libro y obtener su título
        cursor.execute('SELECT estado,titulo FROM Libros where id_libro = ?',(libro_id,))
        resultado= cursor.fetchone()
        
        if resultado :
            estado_libro,titulo=resultado
        
            if estado_libro.lower() == 'disponible':
                fecha_d = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
                
                #Registra el prestamo
                cursor.execute('INSERT INTO Prestamos (id_libro,id_usuario,fecha_devolucion) VALUES (?,?,?)',
                (libro_id,usuario_id,fecha_d))
            
                #Actualiza el estado del libro a "Prestado"
                cursor.execute('UPDATE Libros SET estado = ? where id_libro = ?',("Prestado",libro_id))
                conn.commit()
                print(f"Prestamo registrado correctamente. El libro {titulo} ha sido prestado al usuario con ID {usuario_id}")
            
            else:
                print(f"El libro {titulo} no esta disponible")
        else:
            print("El libro no existe en la base de datos")
    except Exception as e:
        print(f"Error al registrar prestamo: {e}")
        
#Funcion para registrar una devolucion en la tabla Devoluciones
def Registrar_devolucion(libro_id,prestamo_id,estado_l):
    try:
        # Verifica si el prestamo existe y esta Activo
        cursor.execute(
            'SELECT id_prestamo FROM Prestamos WHERE id_prestamo = ? AND estado = "Activo"',
            (prestamo_id,)
        )
        prestamo = cursor.fetchone()
        if not prestamo:
            print("El préstamo no existe o ya ha sido devuelto.")
            return
        
        #Verifica si el libro existe en la base de datos
        cursor.execute('SELECT titulo FROM Libros WHERE id_libro = ?', (libro_id,))
        titulo = cursor.fetchone()
        if titulo:
            titulo = titulo[0]
            
            # Actualiza el estado del prestamo y del libro
            cursor.execute('UPDATE Prestamos set estado = ? where id_libro= ?',("Devuelto",libro_id))
            cursor.execute('UPDATE Libros set estado = ? where id_libro = ?',("Disponible",libro_id))
            
            #Registra la devolucion
            fecha_d=datetime.now().strftime('%Y-%m-%d')
            cursor.execute('INSERT INTO Devoluciones (id_prestamo,fecha_devolucion,estado_libro) VALUES (?,?,?)',(prestamo_id,fecha_d,estado_l))
            conn.commit()
            print(f"Libro {titulo} devuelto exitosamente. Estado: {estado_l}")
        else:
            print("El libro no existe en la base de datos")
    except Exception as e:
        print(f"Error al registrar devolucion: {e}")

#menu interactivo para habilitar las funciones
def menu():
    while True:
        print("\n--- Biblioteca ---")
        print("1.Agregar un libro")
        print("2.Lista de libros")
        print("3.Registrarse")
        print("4.Registrar prestamo")
        print("5.Registrar devolucion")
        print("6.Salir")
        
        opcion=input("seleccione una opcion: ")
        
        if opcion == '1':
            titulo=input("ingrese el titulo: ")
            autor=input("nombre del autor: ")
            genero=input("ingrese su genero: ")
            try:
                año=int(input("año del libro: "))
                Agregar_libro(titulo,autor,genero,año)
            except ValueError:
                print("El año debe de ser un numero entero")

        elif opcion == '2':
            print("<--------> Lista de libros <-------->")
            Lista_libros()

        elif opcion == '3':
            nombre=input("ingrese su nombre: ")
            correo=input("ingrese su correo: ")
            Registrarse(nombre,correo)

        elif opcion == '4':
            try:
                usuario_id=int(input("ingrese su id de usuario: "))
                libro_id=int(input("ingrese el id del libro que desea llevarse: "))
                Registrar_prestamo(usuario_id,libro_id)
            except ValueError:
                print("Los IDs deben de ser enteros")

        elif opcion == '5':
            try:
                libro=int(input("ingrese id del libro: "))
                prestamo_id=int(input("ingrese su id de prestamo: "))
                estado=input("ingrese el estado del libro Nuevo o Dañado: ")
                Registrar_devolucion(libro,prestamo_id,estado)
            except ValueError:
                print("Los IDs deben de ser enteros")
        elif opcion == '6':
            print("saliendo....")
            break
        else:
            print("opcion no valida")

if __name__ == "__main__":
    try:
        menu()
    finally:
        if conn:
            conn.close()
