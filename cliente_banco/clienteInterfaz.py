from abc import abstractmethod
from abc import ABCMeta

class ClienteInterfaz(metaclass=ABCMeta):
    """
    Interfaz que modela el comportamiento  de la clase ClienteServicio
    del lado del cliente
    Esto es para reducir el acoplamiento
    """
    @abstractmethod
    def validate_terjet(self, num_tarjet):
        pass

    @abstractmethod
    def validate_nip(self, num_tarjeta, nip):
        pass
    
    @abstractmethod
    def verifica_saldo(self, num_tarjeta):
        pass
    
    @abstractmethod
    def verifica_limite(self, num_tarjeta):
        pass

    @abstractmethod
    def realiza_retiro(self,num_tarjeta,cantidad):
        pass
    