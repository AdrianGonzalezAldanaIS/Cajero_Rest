from flask import Flask, jsonify, request
from models import tarjetas
from datetime import datetime
from jsonschema import Draft7Validator
from json import load
import os

curren_path = os.getcwd()
archivo = f'{curren_path}/servidor_banco/schema_object.json'


app = Flask(__name__)


@app.route('/tarjetas')
def getTarjetas():
    return jsonify(tarjetas)

@app.route('/tarjeta/<string:num_tarjeta>', methods = ['GET'])
def consulta_existencia(num_tarjeta):
    """
    Envia el recurso con el metodo HTTP ['GET']
    Descripcion: Metodo que verifica la existencia de la tarjeta (numero de tarjeta)
    dada por el usuario
    
    Entrada: num_tarjeta -> Es el numero de tarjeta dada por el usuario
    Salida: Regresa una valor booleano. True si existe (si la encontro en la BD)
                                        False si no existe (si no la encuentra en la BD)
    """
    tarjeta = [tar for tar in tarjetas if tar['num_tarjeta'] == num_tarjeta]
    es_valida = True
    if len(tarjeta)>0:
        return jsonify({"mensaje_alert":es_valida})
    else:
        es_valida = False
        return jsonify({"mensaje_alert":es_valida})


@app.route('/tarjeta/verificada/<string:num_tarjeta>', methods = ['GET'])
def getVerificada(num_tarjeta):
    """"
    Envia el recurso con el metodo HTTP ['GET']
    Descripcion: Metodo que verifica si la tarjeta esta verificada

    Entrada: num_tarjeta -> Es el numero de tarjeta dada por el usuario
    Salida: Regresa un valor booleano. True si se encuentra verificada la tarjeta
                                        False si no se encuentra verificada
    """
    tarjeta = [tar for tar in tarjetas if tar['num_tarjeta'] == num_tarjeta]
    return jsonify({"mensaje_alert":tarjeta[0]['verificada']})


@app.route('/tarjeta/vencida/<string:num_tarjeta>', methods = ['GET'])
def getVencida(num_tarjeta):
    """
    Envia el recurso con el metodo HTTP ['GET']
    Descripcion: Metodo que verifica el estado de la fecha de vencimiento

    Entrada: num_tarjeta -> Es el numero de tarjeta dada por el usuario
    Salida: Regresa un valor booleano. True si la fecha de vencimiento es mayor al da actual
                                        False si la fecha de vencimiento es menor a la fecha actual
    """
    tarjeta = [tar for tar in tarjetas if tar['num_tarjeta'] == num_tarjeta]
    fecha = tarjeta[0]['fecha_verificada']
    fecha_vencimiento = datetime.strptime(fecha,'%Y-%m-%d')
    es_vigente = True
    if fecha_vencimiento > datetime.now():
        return jsonify({"mensaje_alert":es_vigente})
    else:
        es_vigente = False
        return jsonify({"mensaje_alert":es_vigente})


@app.route('/tarjeta/bloqueada/<string:num_tarjeta>', methods = ['GET'])
def getBloqueada(num_tarjeta):
    """
    Envia el recurso con el metodo HTTP ['GET']
    Descripcion: Metodo que verifica si la tarjeta no esta bloqueada

    Entrada: num_tarjeta -> Es el numero de tarjeta dada por el usuario
    Salida: Regresa un valor booleano. False si No se encuentra bloqueada
                                        True si Si se encuentra bloqueada 
    """
    tarjeta = [tar for tar in tarjetas if tar['num_tarjeta'] == num_tarjeta]
    return jsonify({"mensaje_alert":tarjeta[0]['bloqueada']})    
    
@app.route('/nip/<string:num_tarjeta>/<int:num_nip>', methods = ['GET'])
def getNip(num_tarjeta, num_nip):
    """
    Envia el recurso con el metodo HTTP ['GET']

    Descripcion: Metodo que verifica si el nip es correcto, si es el caso el 
    numero de intentos se reestablece en cero, en caso de que no lo 
    digite bien el usuario el numero de intentos incrementa en uno.
    En caso de llegar al tercer intento se bloquea en automatico la tarjeta

    Entrada: num_tarjeta -> Es el numero de tarjeta dada por el usuario
             num_nip -> Es el nip que la que cuenta la tarjeta
    Salida: Regresa un diccionario: 
    {"mensaje_alert":False, "intentos":tarjeta[0]['intentos'], "pase":True} 
    en caso de que se sea correcto el NIP

    {"mensaje_alert":tarjeta[0]['bloqueada'],"intentos":tarjeta[0]['intentos'], "pase":False}
    en caso de que el numero de intentos sea mayor-igual a tres
    """
    tarjeta = [tar for tar in tarjetas if tar['num_tarjeta'] == num_tarjeta]
    nip = tarjeta[0]['nip']
    es_valida = False
    if nip == num_nip:
        es_valida = True
        tarjeta[0]['bloqueada'] = False
        tarjeta[0]['intentos'] = 0
    else:
        es_valida = False
        tarjeta[0]['intentos'] += 1
    if tarjeta[0]['intentos'] >= 3:
        es_valida = False
        tarjeta[0]['bloqueada'] = True
        return jsonify({"mensaje_alert":tarjeta[0]['bloqueada'],"intentos":tarjeta[0]['intentos'], "pase":es_valida})
    return jsonify({"mensaje_alert":False, "intentos":tarjeta[0]['intentos'], "pase":es_valida})

@app.route('/retiro/saldo/<string:num_tarjeta>', methods = ['GET'])
def getSaldo(num_tarjeta):
    """
    Envia el recurso con el metodo HTTP ['GET']
    Descripcion: Metodo que regresa la cantidad de saldo con que dispone la tarjeta

    Entrada: num_tarjeta -> Es el numero de tarjeta dada por el usuario
    Salida: Regresa la cantidad de saldo de la tarjeta
    """
    tarjeta = [tar for tar in tarjetas if tar['num_tarjeta'] == num_tarjeta]
    return jsonify({"mensaje_alert":tarjeta[0]['saldo']})


@app.route('/retiro/limite/<string:num_tarjeta>', methods = ['GET'])
def getLimite(num_tarjeta):
    """
    Envia el recurso con el metodo HTTP ['GET']
    Metod que regresa la cantidad limite para poder retirar

    Entrada: num_tarjeta -> Es el numero de tarjeta dada por el usuario
    Salida: Regresa la cantidad limite para poder retirar
    """
    tarjeta = [tar for tar in tarjetas if tar['num_tarjeta'] == num_tarjeta]
    return jsonify({"mensaje_alert":tarjeta[0]['limite']})

@app.route('/retira/actualiza/<string:num_tarjeta>/', methods = ['POST'])
def retirar(num_tarjeta):
    """
    Envia el recurso con el mtodo HTTP ['POST']
    Descripcion: Metodo que realiza el retiro sobre el saldo y lo actualiza a nivel memoria

    Entrada: num_tarjeta -> Es el numero de tarjeta dada por el usuario
    Salida: Regresa la cantidad resultante del retiro sobre el saldo
    """
    tarjeta = [tar for tar in tarjetas if tar['num_tarjeta'] == num_tarjeta]
    cantidad = request.json['pago']
    if cantidad <= tarjeta[0]['limite'] and cantidad <= tarjeta[0]['saldo']:
        tarjeta[0]['saldo'] -= cantidad
    return jsonify({"mensaje_alert":tarjeta[0]['saldo']})


@app.route('/retira/saldo/<string:num_tarjeta>/<float:cantidad>', methods = ['GET'])
def consulta_saldo(num_tarjeta,cantidad):
    """
    Envia el recurso con el mtodo HTTP ['GET']
    Descripcion: Metodo que verifica que el saldo sea mayor-igual a la cantidad 
    y que el saldo sea meyor-igual a cero

    Entrada: num_tarjeta -> Es el numero de tarjeta dada por el usuario
             cantidad -> es la cantidad de saldo solicitado por el usuario
    Salida: Regresa un valor booleano. True en caso de pasar la validacion
                                        False en caso de no pasar la validacion
    """
    tarjeta = [tar for tar in tarjetas if tar['num_tarjeta'] == num_tarjeta]
    if cantidad <= tarjeta[0]['saldo'] and tarjeta[0]['saldo'] >= 0:
        return jsonify({"mensaje_alert":True})
    else:
        return jsonify({"mensaje_alert":False})

@app.route('/retira/limite/<string:num_tarjeta>/<float:cantidad>', methods = ['GET'])
def consulta_limite(num_tarjeta,cantidad):
    """
    Envia el recurso con el mtodo HTTP ['GET']
    Descripcion: Metodo que verifica si la cantidad ingresada por el usuario
    no excede el limite defindo en la BD

    Entrada: num_tarjeta -> Es el numero de tarjeta dada por el usuario
             cantidad -> Es la cantidad ingresada, a retirar, por el usuario
    Salida: Regresa un valor booleano. True si la cantidad ingresada es menor-igual
                                        al limite definido en la BD
                                        False si la cantidad es mayor al
                                        limite definido en la BD
    """
    tarjeta = [tar for tar in tarjetas if tar['num_tarjeta'] == num_tarjeta]
    if cantidad <= tarjeta[0]['limite']:
        return jsonify({"mensaje_alert":True})
    else:
        return jsonify({"mensaje_alert":False})

if __name__ == '__main__':
    app.run(debug = True, port = 4000)





