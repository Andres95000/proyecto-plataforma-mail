import sqlite3

def ver_enviados(correo):
    db = sqlite3.connect("mensajerias.s3db") # Conexion a la base de datos
    db.row_factory=sqlite3.Row # Le asigno las cabeceras a la variable db (como id, nombreusuario, correo, password, estado, codigoactivacion)
    cursor = db.cursor() # Se crea un apuntador para crear las consultas
    consulta = "SELECT m.asunto, m.mensaje, m.fecha, m.hora, u.nombreusuario FROM usuarios u, mensajeria m WHERE u.correo=m.id_usu_recibe AND m.id_usu_envia='"+correo+"' ORDER BY fecha DESC, hora DESC"

    cursor.execute(consulta) # Se ejecuta la consulta

    resultado=cursor.fetchall() # La respuesta de consulta se asigna a la variable resultado

    return resultado

def ver_recibidos(correo):
    db = sqlite3.connect("mensajerias.s3db") # Conexion a la base de datos
    db.row_factory=sqlite3.Row # Le asigno las cabeceras a la variable db (como id, nombreusuario, correo, password, estado, codigoactivacion)
    cursor = db.cursor() # Se crea un apuntador para crear las consultas
    consulta = "SELECT m.asunto, m.mensaje, m.fecha, m.hora, u.nombreusuario FROM usuarios u, mensajeria m WHERE u.correo=m.id_usu_envia AND m.id_usu_recibe='"+correo+"' ORDER BY fecha DESC, hora DESC"

    cursor.execute(consulta) # Se ejecuta la consulta

    resultado=cursor.fetchall() # La respuesta de consulta se asigna a la variable resultado

    return resultado

"""La funcion validar_usuario verifica que el usuario este registrado en la base de datos"""
def validar_usuario(usuario, password):
    db = sqlite3.connect("mensajerias.s3db") # Conexion a la base de datos
    db.row_factory=sqlite3.Row # Le asigno las cabeceras a la variable db (como id, nombreusuario, correo, password, estado, codigoactivacion)
    cursor = db.cursor() # Se crea un apuntador para crear las consultas
    consulta = "SELECT * FROM usuarios WHERE correo='"+usuario+"' AND password='"+password+"' AND estado = '1'"

    cursor.execute(consulta) # Se ejecuta la consulta

    resultado=cursor.fetchall() # La respuesta de consulta se asigna a la variable resultado

    return resultado

def lista_destinatarios(usuario):
    db = sqlite3.connect("mensajerias.s3db") # Conexion a la base de datos
    db.row_factory=sqlite3.Row # Le asigno las cabeceras a la variable db (como id, nombreusuario, correo, password, estado, codigoactivacion)
    cursor = db.cursor() # Se crea un apuntador para crear las consultas
    consulta = "SELECT * FROM usuarios WHERE correo<>'"+usuario+"'"

    cursor.execute(consulta) # Se ejecuta la consulta

    resultado=cursor.fetchall() # La respuesta de consulta se asigna a la variable resultado

    return resultado

""""""

def actualizapass(password, correo):
    db = sqlite3.connect("mensajerias.s3db") # Conexion a la base de datos
    db.row_factory=sqlite3.Row # Le asigno las cabeceras a la variable db (como id, nombreusuario, correo, password, estado, codigoactivacion)
    cursor = db.cursor() # Se crea un apuntador para crear las consultas
    consulta = "UPDATE usuarios SET password='"+password+"' WHERE correo='"+correo+"'"

    cursor.execute(consulta) # Se ejecuta la consulta

    db.commit() # Confirma la insersion

    return "1"

def registrar_mail(origen, destino, asunto, mensaje):
    db = sqlite3.connect("mensajerias.s3db") # Conexion a la base de datos
    db.row_factory=sqlite3.Row # Le asigno las cabeceras a la variable db (como id, nombreusuario, correo, password, estado, codigoactivacion)
    cursor = db.cursor() # Se crea un apuntador para crear las consultas
    consulta = "INSERT INTO mensajeria (asunto, mensaje, fecha, hora, id_usu_envia, id_usu_recibe, estado) VALUES ('"+asunto+"', '"+mensaje+"', DATE('now'),TIME('now'), '"+origen+"', '"+destino+"', '0')"

    cursor.execute(consulta) # Se ejecuta la consulta

    db.commit() # Confirma la insersion

    return "1"

def registrar_usuario(nombre, correo, password, codigo):
    try:
        db = sqlite3.connect("mensajerias.s3db") # Conexion a la base de datos
        db.row_factory=sqlite3.Row # Le asigno las cabeceras a la variable db (como id, nombreusuario, correo, password, estado, codigoactivacion)
        cursor = db.cursor() # Se crea un apuntador para crear las consultas
        consulta = "INSERT INTO usuarios (nombreusuario, correo, password, estado, codigoactivacion) VALUES ('"+nombre+"', '"+correo+"', '"+password+"', '0', '"+codigo+"')"

        cursor.execute(consulta) # Se ejecuta la consulta

        db.commit() # Confirma la insersion

        return "Usuario Registrado Satisfactoriamente"

    except:
        return "ERROR!!! No es posible registrar al usuario debido a que el CORREO y/o NOMBRE DE USUARIO existen. Lo invitamos a modificar dichos campos."



def activar_usuario(codigo):
    db = sqlite3.connect("mensajerias.s3db") # Conexion a la base de datos
    db.row_factory=sqlite3.Row # Le asigno las cabeceras a la variable db (como id, nombreusuario, correo, password, estado, codigoactivacion)
    cursor = db.cursor() # Se crea un apuntador para crear las consultas
    consulta = "UPDATE usuarios set estado='1' WHERE codigoactivacion='"+codigo+"'"

    cursor.execute(consulta) # Se ejecuta la consulta

    db.commit() # Confirma la insersion

    consulta2 = "SELECT * FROM usuarios WHERE codigoactivacion='"+codigo+"' AND estado = '1'" # Cosulta para verificar el codigo de activacion

    cursor.execute(consulta2) # Se ejecuta la consulta

    resultado=cursor.fetchall() # La respuesta de consulta se asigna a la variable resultado

    return resultado