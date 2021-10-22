import sqlite3

from sqlite3 import Error

#Funcion que establece la conexión a la base de datos
def conectar():
    try:
        conn = sqlite3.connect('db/datos.db')
        return conn
    except Error as err:
        print(err)
        return None

#Esta función sirve para ejecutar sentencias sql de tipo INSERT, UPDATE, DELETE
def ejecutar_insert(_sql, lista_parametros):
    try:
        conn = conectar()
        if conn:
            objeto_cursor = conn.cursor()
            filas = objeto_cursor.execute(_sql, lista_parametros).rowcount
            objeto_cursor.close()
            conn.commit()
            conn.close()

            return filas
        else:
            print("No se pudo establecer la conexión a la base de datos. Ver errores previos.")
            return -1
    except Error as err:
        print("Error al ejecutar sentencia SQL: " + str(err))
        return -1


#Funcion para ejecutar las sentencias SQL de tipo: SELECT
def ejecutar_select(_sql, lista_parametros):
    try:
        conn = conectar()
        if conn:
            #Configuramos la conexion para convertir de tuplas a diccionarios las filas
            #devueltas por el select.
            #no colocamos parametros pq estamos haciendo referencia a la funcion y no invocandola
            conn.row_factory = fabrica_diccionarios 

            objeto_cursor = conn.cursor()

            if lista_parametros:
                objeto_cursor.execute(_sql, lista_parametros)
            else:
                objeto_cursor.execute(_sql)
            
            filas = objeto_cursor.fetchall()
            objeto_cursor.close()
            conn.close()

            return filas
        else:
            print("No se pudo establecer conexión con la base de datos. Ver errores previos.")
            return None
    except Error as err:
        print("Error al ejecutar SELECT: " + str(err))
        return None

#Convierte los resultados del select de lista de tuplas a lista de diccionarios
#esto facilita la referncia a los atributos o columnas de las filas de la base de datos.
def fabrica_diccionarios(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    
    return d