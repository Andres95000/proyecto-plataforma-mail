from flask import Flask, render_template, request
import hashlib
import controlador
from datetime import datetime
import envioemail

app = Flask(__name__)
email_origen=""

@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/validarUsuario', methods=['GET', 'POST'])
def validarUsuario():
    if request.method=="POST":
        usu=request.form["txtusuario"]
        usu = usu.replace("SELECT ","").replace("INSERT ","").replace("DELETE ","").replace("UPDATE ","").replace("WHERE ","") # Para evitar INYECTION SQL
        passw=request.form["txtpass"]
        passw = passw.replace("SELECT ","").replace("INSERT ","").replace("DELETE ","").replace("UPDATE ","").replace("WHERE ","")
        passw2 = passw.encode() #Estamos codificando la contraseña para poder encriptarla
        passw2 = hashlib.sha384(passw2).hexdigest() # Estamos encriptando la contraseña con sha384

        respuesta = controlador.validar_usuario(usu, passw2)

        global email_origen

        if len(respuesta) == 0:
            email_origen=""
            mensaje = "!!!Error de autenticacion.!!! lo invitamos a verificar su usuario(correo) y contraseña"
            return render_template("informacion.html", datas=mensaje)
        else:
            email_origen=usu

        #print("usuario="+usu)
        #print("password="+passw)
        #print("password encriptado="+passw2)
            respuesta2 = controlador.lista_destinatarios(usu)
            return render_template("principal.html", datas = respuesta2)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/validacionCodigo')
def validacionCodigo():
    return render_template('valida_codigo.html')

@app.route('/registrarUsuario', methods=['GET', 'POST'])
def registrarUsuario():
    if request.method=="POST":
        nombre=request.form["txtnombre"]
        nombre=nombre.replace("SELECT ","").replace("INSERT ","").replace("DELETE ","").replace("UPDATE ","").replace("WHERE ","")
        email=request.form["txtusuario2registro"]
        email=email.replace("SELECT ","").replace("INSERT ","").replace("DELETE ","").replace("UPDATE ","").replace("WHERE ","")
        passw=request.form["txtpassregistro"]
        passw=passw.replace("SELECT ","").replace("INSERT ","").replace("DELETE ","").replace("UPDATE ","").replace("WHERE ","")
        passw2 = passw.encode() #Estamos codificando la contraseña para poder encriptarla
        passw2 = hashlib.sha384(passw2).hexdigest() # Estamos encriptando la contraseña con sha384

        """Generando el codigo de activacion"""
        codigo = datetime.now() # Variable con la fecha y hora actual
        codigo2 = str(codigo) # Convertimos codigo a un variable string para poder manipular
        codigo2 = codigo2.replace("-", "") # Se remplazan '-,  , :, .' por vacio para quitar y poder generar un codigo de validacion unico
        codigo2 = codigo2.replace(" ", "")
        codigo2 = codigo2.replace(":", "")
        codigo2 = codigo2.replace(".", "")
        print(codigo2)

        mensaje = "Sr "+ nombre +", su codigo de activacion es :\n\n"+codigo2+"\n\n Recuerde copiarlo y pegarlo en la seccion login y activar cuenta. \n\nMuchas Gracias"

        envioemail.enviar(email, mensaje,"Codigo de Activacion") # Envia el codigo de activacion al correo

        respuesta = controlador.registrar_usuario(nombre, email, passw2, codigo2)

        
        #mensaje = "El usuario "+ nombre + ", se ha registrado satisfactoriamente"
        return render_template("informacion.html", datas=respuesta)

@app.route('/enviarMAIL', methods=['GET', 'POST'])
def enviarMAIL():
    if request.method=="POST":
        emailDestino=request.form["emailDestino"]
        emailDestino=emailDestino.replace("SELECT ","").replace("INSERT ","").replace("DELETE ","").replace("UPDATE ","").replace("WHERE ","")
        asunto=request.form["asunto"]
        asunto=asunto.replace("SELECT ","").replace("INSERT ","").replace("DELETE ","").replace("UPDATE ","").replace("WHERE ","")
        mensaje=request.form["mensaje"]
        mensaje=mensaje.replace("SELECT ","").replace("INSERT ","").replace("DELETE ","").replace("UPDATE ","").replace("WHERE ","")
        mensaje2="Sr Usuario, usted recibio un mensaje nuevo, por favor ingrese a la plataforma para observar su email, en la pestaña Historial.\n\nMuchas gracias."

        controlador.registrar_mail(email_origen, emailDestino, asunto, mensaje)

        envioemail.enviar(emailDestino, mensaje2,"Nuevo Mensaje Enviado") # Envia el codigo de activacion al correo
        return "Email Enviado Satisfactoriamente"

@app.route('/activarUsuario', methods=['GET', 'POST'])
def activarUsuario():
    if request.method=="POST":
        codigo=request.form["txtcodigo"]
        codigo=codigo.replace("SELECT ","").replace("INSERT ","").replace("DELETE ","").replace("UPDATE ","").replace("WHERE ","")

        respuesta = controlador.activar_usuario(codigo)

        if len(respuesta) == 0:
            mensaje = "El codigo de activacion es erroneo, verifiquelo"
        else:
            mensaje = "El usuario se ha activado exitosamente"
        return render_template("informacion.html", datas=mensaje)

@app.route('/HistorialEnviados', methods=['GET', 'POST'])
def HistorialEnviados():
    resultado = controlador.ver_enviados(email_origen)

    return render_template("respuesta.html", datas=resultado)

@app.route('/HistorialRecibidos', methods=['GET', 'POST'])
def HistorialRecibidos():
    resultado = controlador.ver_recibidos(email_origen)

    return render_template("respuesta.html", datas=resultado)

@app.route('/actualizacionPassword', methods=['GET', 'POST'])
def actualizacionPassword():
    if request.method=="POST":
        pass1=request.form["pass"]
        pass1=pass1.replace("SELECT ","").replace("INSERT ","").replace("DELETE ","").replace("UPDATE ","").replace("WHERE ","")
        passw2 = pass1.encode() #Estamos codificando la contraseña para poder encriptarla
        passw2 = hashlib.sha384(passw2).hexdigest() # Estamos encriptando la contraseña con sha384

        respuesta = controlador.actualizapass(passw2, email_origen)

        
        return "Actualizacion de Password Satisfactoria"
