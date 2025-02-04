# IMPORTS
import csv
import os
import shutil

import bcrypt

'''
PROCESAMIENTO USUARIOS
@Author: Claudia Landeira

Funciones encargadas de realizar los procesamientos de la informacion de los usuarios
'''


# FUNCION --> registrar_usuario
# Función encargada de registrar a los nuevos usuarios en la database.csv
def registrar_usuario(nombre, email, password):
    if os.path.exists('database.csv'):
        # Verificar si el email ya está en uso
        with open('database.csv', mode='r') as db:
            reader = csv.reader(db, delimiter=';')
            for row in reader:
                if row[1] == email:
                    return False

        # Encriptar la contraseña
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # Agregar el usuario al archivo CSV
        with open('database.csv', mode='a', newline='') as db:
            fieldnames = ['nombre', 'email', 'password']
            writer = csv.DictWriter(db, fieldnames=fieldnames, delimiter=';')
            writer.writerow({'nombre': nombre, 'email': email, 'password': hashed_password.decode('utf-8')})

        if os.path.exists('./usuarios/'):
            # Crear el directorio para el usuario
            os.mkdir('./usuarios/' + email)

            readme = open('./usuarios/' + email + '/readme.md', 'w')
            readme.write(nombre + ': ' + email)
            readme.close()
        else:
            os.mkdir('./usuarios/')
            os.mkdir('./usuarios/' + email)

            readme = open('./usuarios/' + email + '/readme.md', 'w')
            readme.write(nombre + ': ' + email)
            readme.close()
        return True
    else:
        archivo = open('database.csv', 'w')
        archivo.close()
        registrar_usuario(nombre, email, password)


# FUNCION --> verificar_usuario
# Función encargada de la verificacion a los usuarios que se encuentren en la database.csv
def verificar_usuario(email, password):
    with open('database.csv', mode='r') as db:
        reader = csv.reader(db, delimiter=';')
        for row in reader:
            if row[1] == email:
                if bcrypt.checkpw(password.encode('utf-8'), row[2].encode('utf-8')):
                    if administracion_usuarios(email):
                        return './usuarios/'
                    else:
                        return './usuarios/' + email
                else:
                    return False

    return False


# FUNCION --> get_usuarios
# Función encargada de obtener los usuarios de la database.csv omitiendo la cuenta de la administracion
def get_usuarios():
    usuarios = []

    if os.path.exists('./usuarios/'):
        for u in os.listdir('./usuarios/'):
            if u != 'administrador@administrador.com':
                usuarios.append(u)

    return usuarios


# FUNCION --> get_usuario
# Función encargada de obtener el correo del usuario
def get_usuario(email):
    with open('database.csv', 'r') as db:
        reader = csv.reader(db, delimiter=';')

        for line in reader:
            if line[1] == email:
                return line[1]

    return None


# FUNCION --> administracion_usuarios
# Función encargada de comprobar la cuenta del administracion
def administracion_usuarios(email):
    correo = 'administrador@administrador.com'

    if email == correo:
        return True

    return False


# FUNCION --> remove_user
# Función encargada de eliminar usuarios, tanto de la base de datos como sus chatbots
def remove_user(email):
    with open('database.csv', newline='') as db:
        reader = csv.reader(db, delimiter=';')
        data = [fila for fila in reader]

    for fila in data:
        if email in fila:
            data.remove(fila)

    with open('database.csv', 'w', newline='') as db:
        writer = csv.writer(db, delimiter=';')
        writer.writerows(data)

    if get_usuario(email) is None:
        shutil.rmtree('./usuarios/' + email)
