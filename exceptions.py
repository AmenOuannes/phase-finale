'''
Toute les exceptions
'''

class ErreurDate(RuntimeError):
    '''
    Erreur date
    '''
    def __init__(self, message='Date n\'existe pas!'):
        super().__init__(message)
    def __str__(self) -> str:
        return str(self.args[0])
class ErreurQuantité(RuntimeError):
    '''
    Erreur Quantité
    '''
    def __init__(self, message= 'Pas assez d\'actions!'):
        super().__init__(message)
    def __str__(self) -> str:
        return str(self.args[0])
class LiquiditéInsuffisante(RuntimeError):
    '''
    Liquidité Insuffissante'''
    def __init__(self, message='Solde insuffisant!'):
        super().__init__(message)
    def __str__(self) -> str:
        return str(self.args[0])
