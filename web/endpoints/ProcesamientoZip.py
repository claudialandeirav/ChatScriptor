# IMPORTS
import os
import shutil
import zipfile
from flask import request

'''
PROCESAMIENTO ARCHIVOS ZIP
@Author: Claudia Landeira

Funciones encargadas de realizar los procesamientos de los archivos zip (importar, exportar)
'''


# FUNCION --> descomprimir_archivo
# Función encargada de descomprimir el archivo zip del chatbot
def descomprimir_archivo(rootdir):
    f = request.files['archivo_zip']

    if f.filename.endswith('.zip'):
        fnombre = f.filename
        f.save(fnombre)

        if comprobar_estructura(f.filename):
            with zipfile.ZipFile(fnombre, 'r') as zip_ref:
                zip_ref.extractall(rootdir + '/' + os.path.splitext(f.filename)[0])
            os.remove(fnombre)
            return True

        os.remove(fnombre)
        return False
    return False


# FUNCION --> exportar_archivos
# Función encargada de comprimir y exportar el directorio del chatbot
def exportar_archivos(rootdir, name):
    if os.path.exists(rootdir + name):
        zip_dir = shutil.make_archive(name, format='zip', root_dir=rootdir + name)
        print(f'\033[34mEl chatbot se ha descargado\033[0m')
        return zip_dir


# FUNCION --> comprobar_estructura
# Función encargada de verificar que el archivo zip tiene la estructura necesaria
def comprobar_estructura(archivo_zip):
    estructura1 = ['entities', 'intents', 'agent.json', 'package.json']
    estructura2 = ['intents', 'agent.json', 'package.json']

    with zipfile.ZipFile(archivo_zip, 'r') as zip_ref:
        estructura_zip = set()

        for nombre in zip_ref.namelist():
            pr_estructura_zip = os.path.split(nombre)[0]
            if pr_estructura_zip:
                estructura_zip.add(pr_estructura_zip)

        for nombre in zip_ref.namelist():
            if '/' not in nombre:
                estructura_zip.add(nombre)

        if estructura_zip == set(estructura1) or estructura_zip == set(estructura2):
            return True
        else:
            return False
