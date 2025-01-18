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

## Requisitos

- Python 3.x
- Librerias:
  - 'sqlite3' (para la base de datos)
  - 're' (para la validación de correos electronicos)
  - 'tabulate' (para mostrar la lista de libros de manera tabulada)

Puedes instalar la librería 'tabulate' ejecutando el siguiente comando:
pip install tabulate
