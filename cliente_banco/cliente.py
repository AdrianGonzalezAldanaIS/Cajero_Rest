from urllib import request
import json
import requests as rq

class Cliente:

    """
    Clase que consume los servicios del servidor en base a enrutamientos con las URI's correctas
    ya definidas como recursos en el lado del servidor
    """

    def consulta_tarjeta(self, num_tarjeta):
        url_consulta = "http://localhost:4000/tarjeta/"
        resp = request.urlopen(url_consulta + num_tarjeta)
        data = json.loads(resp.read())
        return data['mensaje_alert']
        

    def consulta_verificada(self, num_tarjeta):
        url_verificada = "http://localhost:4000/tarjeta/verificada/"
        resp = request.urlopen(url_verificada + num_tarjeta)
        data = json.loads(resp.read())
        return data['mensaje_alert']
    

    def consulta_vencida(self, num_tarjeta):
        url_vencida = "http://localhost:4000/tarjeta/vencida/"
        resp = request.urlopen(url_vencida + num_tarjeta)
        data = json.loads(resp.read())
        return data['mensaje_alert']
    
    def consulta_bloqueada(self, num_tarjeta):
        url_bloqueada = "http://localhost:4000/tarjeta/bloqueada/"
        resp = request.urlopen(url_bloqueada + num_tarjeta)
        data = json.loads(resp.read())
        return data['mensaje_alert']

    def consulta_nip(sefl, num_tarjeta, nip):
        url_nip = "http://localhost:4000/nip/"
        resp = request.urlopen(url_nip + num_tarjeta+"/"+nip)
        data = json.loads(resp.read())
        return data
    
    def consulta_saldo(self, num_tarjeta):
        url_saldo = "http://localhost:4000/retiro/saldo/"
        resp = request.urlopen(url_saldo + num_tarjeta)
        data = json.loads(resp.read())
        return data['mensaje_alert']
    
    
    def consulta_limite(self, num_tarjeta):
        url_limite = "http://localhost:4000/retiro/limite/"
        resp = request.urlopen(url_limite + num_tarjeta)
        data = json.loads(resp.read())
        return data['mensaje_alert']

    def verifica_saldo(self,num_tarjeta,cantidad):
        url_verifica_saldo = "http://localhost:4000/retira/saldo/"
        resp = request.urlopen(url_verifica_saldo + num_tarjeta+"/"+str(cantidad))
        data = json.loads(resp.read())
        return data['mensaje_alert']
    
    def verifica_limite(self, num_tarjeta,cantidad):
        url_verifica_limite = "http://localhost:4000/retira/limite/"
        resp = request.urlopen(url_verifica_limite + num_tarjeta+"/"+str(cantidad))
        data = json.loads(resp.read())
        return data['mensaje_alert']
    
    def actualizar_saldo(self, num_tarjeta, cantidad):
        """
        Se utiliza la libreria request (rq) para poder hacer la llamada con el
        metodo HTTP ['POST'] y a su vez pasarle la cantidad al servicio
        """
        url_actualiza = "http://localhost:4000/retira/actualiza/"
        response = rq.post(url_actualiza + num_tarjeta, json={'pago': cantidad})
        data = response.json()
        return data




