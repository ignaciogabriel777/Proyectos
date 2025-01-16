import sqlite3
from datetime import datetime, timedelta

conn=sqlite3.connect('Gestion_biblioteca.db')
cursor=conn.cursor()

#Funcion para agragar un libro
def Agregar_libro(titulo,autor,genero,año):
    cursor.execute('INSERT INTO Libros (titulo,autor,genero,año_publicacion,estado) VALUES (?,?,?,?,?)',(titulo,autor,genero,año,'Disponible'))
    conn.commit()
    print("libro agregado exitosamente.")
    
#Funcion de lista de libros
def Lista_libros():
    cursor.execute('SELECT * FROM Libros')
    return cursor.fetchall()

#Funcion para registrarse
def Registrarse(nombre, correo):
    cursor.execute('INSERT INTO Usuarios (nombre, correo) VALUES (?, ?)',(nombre, correo))
    conn.commit()
    print("Usuario registrado correctamente.")
    
#funcion de prestamo
def Registrar_prestamo(usuario_id,libro_id):
    cursor.execute('SELECT estado FROM Libros where id_libro = ?',(libro_id,))
    resultado= cursor.fetchone()

    if resultado :
        estado_libro=resultado[0]
        
        if estado_libro.lower() == 'disponible':
            fecha_d = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
            cursor.execute('INSERT INTO Prestamos (id_libro,id_usuario,fecha_devolucion) VALUES (?,?,?)',
            (libro_id,usuario_id,fecha_d))
            
            cursor.execute('UPDATE Libros SET estado = ? where id_libro = ?',("Prestado",libro_id))
            conn.commit()
            print("prestamo registrado correctamente")
            
        else:
            print("el libro no esta disponible")
    else:
        print("el libro no existe en la base de datos")
        
#Registrar devolucion
def Registrar_devolucion(libro_id,prestamo_id,estado_l):
    cursor.execute('UPDATE Prestamos set estado = ? where id_libro= ?',("Devuelto",libro_id))
    cursor.execute('UPDATE Libros set estado = ? where id_libro = ?',("Disponible",libro_id))
    fecha_d=datetime.now().strftime('%Y-%m-%d')
    cursor.execute('INSERT INTO Devoluciones (id_prestamo,fecha_devolucion,estado_libro) VALUES (?,?,?)',(prestamo_id,fecha_d,estado_l))
    conn.commit()
    print("libro devuelto exitosamente.")



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
            año=int(input("año del libro: "))
            Agregar_libro(titulo,autor,genero,año)
        elif opcion == '2':
            libros=Lista_libros()
            print("<--------> Lista de libros <-------->")
            for li in libros:
                print(f"id: {li[0]}, Titulo: {li[1]}, Autor: {li[2]}, Genero: {li[3]}, Año: {li[4]}, Estado: {li[5]}")
        elif opcion == '3':
            nombre=input("ingrese su nombre: ")
            correo=input("ingrese su correo: ")
            Registrarse(nombre,correo)
        elif opcion == '4':
            libro_id=int(input("ingrese el id del libro que desea llevarse: "))
            usuario_id=int(input("ingrese su id de usuario: "))
            Registrar_prestamo(libro_id,usuario_id)
        elif opcion == '5':
            libro=int(input("ingrese id del libro: "))
            prestamo_id=int(input("ingrese su id de prestamo: "))
            estado=input("ingrese el estado del libro Nuevo o Dañado: ")
            Registrar_devolucion(libro,prestamo_id,estado)
        elif opcion == '6':
            print("saliendo....")
            break
        else:
            print("opcion no valida")

if __name__ == "__main__":
    try:
        menu()
    finally:
        conn.close()
