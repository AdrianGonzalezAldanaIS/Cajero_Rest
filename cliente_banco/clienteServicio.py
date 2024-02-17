from cliente import Cliente
from clienteInterfaz import ClienteInterfaz

class ClienteServicio(ClienteInterfaz):
    cliente = Cliente()

    """
    Clase que implementa la interfaz ClienteInterfaz, esto con el fin de reducir el acoplamiento.
    Clase encargada de hacer las validaciones pertinentes sobre las respuestas del servidor
    """

    def validate_terjet(self, num_tarjet):
        respuesta = {"mensaje": "La tarjeta se encuentra dentro de las validaciones requeridas","verificada":True}
        if not self.cliente.consulta_tarjeta(num_tarjet):
            respuesta['mensaje'] = 'El numero de la tarjeta no esta registrada'
            respuesta['verificada'] = False
            return respuesta
        elif not self.cliente.consulta_verificada(num_tarjet):
            respuesta['mensaje'] = 'La tarjeta no esta verificada'
            respuesta['verificada'] = False
            return respuesta
        elif not self.cliente.consulta_vencida(num_tarjet):
            respuesta['mensaje'] = 'La tarjeta expiro'
            respuesta['verificada'] = False
            return respuesta
        elif self.cliente.consulta_bloqueada(num_tarjet):
            print("resp ",self.cliente.consulta_bloqueada(num_tarjet))
            respuesta['mensaje'] = 'La tarjeta esta bloqueada'
            respuesta['verificada'] = False
            return respuesta
        return respuesta

    def validate_nip(self, num_tarjeta, nip):
        pasa = self.cliente.consulta_nip(num_tarjeta, nip)
        respuesta = {"mensaje": "El NIP es correcto","verificada":True, "intentos":pasa['intentos']}
        if not pasa["pase"]:
            respuesta['mensaje'] = "Lo sentimos, tu NIP es incorrecto 🧐"
            respuesta['verificada'] = pasa['pase']
            respuesta["intentos"] = pasa['intentos']
        return respuesta

    def verifica_saldo(self, num_tarjeta):
        return self.cliente.consulta_saldo(num_tarjeta)

    def verifica_limite(self, num_tarjeta):
        return self.cliente.consulta_limite(num_tarjeta)

    def realiza_retiro(self,num_tarjeta,cantidad):
        saldo = self.cliente.consulta_saldo(num_tarjeta)
        respuesta = {"mensaje": "Retiro exitoso","retirar":True, "saldo":saldo}
        if not self.cliente.verifica_limite(num_tarjeta, cantidad):
            respuesta['mensaje'] = 'Excedes el limite para retirar 🥺'
            respuesta['verificada'] = False
            return respuesta
        elif not self.cliente.verifica_saldo(num_tarjeta,cantidad):
            respuesta['mensaje'] = 'Saldo insuficiente'
            respuesta['verificada'] = False
            return respuesta
        else:
            retiro = self.cliente.actualizar_saldo(num_tarjeta,cantidad)
            respuesta['saldo'] = retiro['mensaje_alert']
            return respuesta





