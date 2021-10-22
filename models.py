import db 
#Importamos las funciones generate_password_hash, check_password_hash
#del modulo werkzeug.security que se instala con flask
from werkzeug.security import generate_password_hash, check_password_hash

#Clase de usuario
class usuario():
    nombre =''
    usuario=''
    correo=''
    password=''

    def __init__(self, p_nombre, p_usuario, p_correo, p_password):
        self.nombre = p_nombre
        self.usuario = p_usuario
        self.correo = p_correo
        self.password = p_password
    
    #Utilizamos un metodo de clase para crear una sobrecarga
    #del constructor de usuario, donde enviando el username 
    #buscamos en la base de datos y obtenemos su información.
    @classmethod
    def cargar(cls, p_usuario):
        sql = "SELECT * FROM usuarios WHERE usuario = ?;"
        obj = db.ejecutar_select(sql, [ p_usuario ])
        if obj:
            if len(obj)>0:
                #Llamamos al constructor de la clase para 
                #devolver una instancia de usuario
                #(p_nombre, p_usuario, p_correo, p_password)
                return cls(obj[0]["nombre"], obj[0]["usuario"], obj[0]["correo"], obj[0]["password"])

        return None

    #Metodo para insertar el usuario en la base de datos
    def insertar(self):
        #Preparamos el comando INSERT para guardar el usuario en la base de datos.
        sql = "INSERT INTO usuarios (usuario,nombre,correo,password) VALUES (?, ?, ?, ?);"
        #Invocamos a la función generate_password_hash para generar el hash seguro del password 
        #del usuario y poder almacenarlo en nuestra bd.
        hashed_pwd = generate_password_hash(self.password, method="pbkdf2:sha256", salt_length=32)
        afectadas = db.ejecutar_insert(sql, [ self.usuario, self.nombre, self.correo, hashed_pwd ])
        return (afectadas > 0)


    def verificar(self):
        #Consulta con mala practica. Concatenando valores al where.
        #sin validaciones de entrada es muy suceptible a ataques de inyección de SQL
        #sql = "SELECT * FROM usuarios WHERE usuario='" + self.usuario + "' AND password ='" + self.password + "' "
        sql = "SELECT * FROM usuarios WHERE usuario = ?; "
        
        #Modificamos el execute para poder enviar los valores de parametros
        #obj_usuario = db.ejecutar_select(sql, None)

        obj_usuario = db.ejecutar_select(sql, [ self.usuario ])

        if obj_usuario:
            if len(obj_usuario) >0:
                #Invocamos a la función check_password_hash para verificar el password
                #digitado por el usuario en el login con el hash seguro almacenado en la bd.
                if check_password_hash(obj_usuario[0]["password"], self.password):
                    return True
        
        return False

class mensaje():
    id=0
    nombre=''
    correo=''
    mensaje=''
    respuesta=''
    estado=''

    #metodo constructor
    def __init__(self, p_id, p_nombre, p_correo, p_mensaje, p_respuesta='', p_estado ='S'):
        self.id = p_id
        self.nombre = p_nombre
        self.correo = p_correo
        self.mensaje = p_mensaje
        self.respuesta = p_respuesta
        self.estado = p_estado
    
    #Este es un metodo de clase, que sirve para "sobrecargar" constructores en python
    @classmethod
    def cargar(cls, p_id):
        sql = "SELECT * FROM mensajes WHERE id = ?;"
        obj = db.ejecutar_select(sql, [ p_id ])
        if obj:
            if len(obj)>0:
                #Llamamos al constructor de la clase para 
                #devolver una instancia de mensaje
                return cls(obj[0]["id"], obj[0]["nombre"], obj[0]["correo"], obj[0]["mensaje"], obj[0]["respuesta"], obj[0]["estado"])

        return None

    #Inserta en la base de datos un mensaje, a partir de los valores del objeto mensaje.
    def insertar(self):
        sql = "INSERT INTO mensajes (nombre, correo, mensaje, estado) VALUES (?,?,?,?);"
        afectadas = db.ejecutar_insert(sql, [ self.nombre, self.correo, self.mensaje, 'S' ])
        return (afectadas >0)

    #Borra el mensaje en la base de datos a partir del atributo id del objeto.
    def eliminar(self):
        sql = "DELETE mensajes WHERE id = ?;"
        afectadas = db.ejecutar_insert(sql, [ self.id ])
        return (afectadas >0)

    def responder(self):
        sql = "UPDATE mensajes SET respuesta = ?, estado='R' WHERE id = ?;"
        afectadas = db.ejecutar_insert(sql, [ self.respuesta, self.id ])
        return (afectadas >0)


    @staticmethod
    def listado():
        sql = "SELECT * FROM mensajes ORDER BY id;"
        return db.ejecutar_select(sql, None)