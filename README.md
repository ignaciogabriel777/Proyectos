# Gestión de Biblioteca

Este proyecto es una aplicacion para gestionar una biblioteca utilizando una base de datos SQLite. Permite a los usuarios registrar libros, llevar un control de los prestamos y devoluciones,
asi como gestionar usuarios dentro del sistema. El sistema incluye funcionalidades como agregar libros, visualizar el inventario, registrar usuarios y realizar prestamos,con un manejo de 
errores adecuado para asegurar la integridad de los datos.

## Funcionalidades

1. **Agregar libros**: Permite añadir nuevos libros a la base de datos con informacion como título, autor, genero y año de publicación.
2. **Lista de libros**: Muestra una lista de todos los libros disponibles en la biblioteca con su estado actual (disponible o prestado).
3. **Registro de usuarios**: Los usuarios pueden registrarse en el sistema proporcionando su nombre y correo electronico.
4. **Registrar prestamos**: Los usuarios pueden solicitar prestamos de libros, siempre que el libro este disponible y el usuario no haya prestado previamente el mismo libro.
5. **Registrar devoluciones**: Permite registrar la devolución de un libro prestado, y actualizar el estado del libro como "disponible" nuevamente. También se puede registrar el estado del
libro (nuevo o dañado) al devolverlo.

## Uso
-Al iniciar el programa, se presentará un menú interactivo con las siguientes opciones:

1. **Agregar un libro**
2. **Ver la lista de libros**
3. **Registrarse como usuario**
4. **Registrar un préstamo**
5. **Registrar una devolución**
6. **Salir del sistema**
-Según la opción seleccionada, el sistema pedirá la información correspondiente (como el título de un libro o el ID de un usuario) y ejecutará la acción deseada.

## Requisitos

- Python 3.x
- Librerias:
  - 'sqlite3' (para la base de datos)
  - 're' (para la validación de correos electronicos)
  - 'tabulate' (para mostrar la lista de libros de manera tabulada)

Puedes instalar la librería 'tabulate' ejecutando el siguiente comando:
pip install tabulate

## Estructura de la Base de Datos

1. **Libros**: Almacena la información de los libros (id_libro(PK), título, autor, genero, año_publicacion, estado).
2. **Usuarios**: Contiene los datos de los usuarios (id_usuarios(PK), nombre, correo, fecha_registro).
3. **Prestamos**: Guarda los registros de los prestamos realizados (id_prestamos(PK), id_usuario(FK), id_libro(FK), usuario, libro, fecha_devolucion, estado).
4. **Devoluciones**: Registra las devoluciones de los libros, incluyendo el estado del libro al ser devuelto (id_devoluciones(PK), id_prestamos(FK), fecha_devolucion, estado_libro).

