'''
Importation des modules nécessaires
'''
from datetime import timedelta, datetime
from phase1 import produire_historique
from exceptions import ErreurDate


class Bourse:
    '''
    Class bourse 
    '''
    def __init__(self, symbole, day) -> None:
        self.day = day
        self.symbole = symbole
    def prix(self) -> int:
        '''
        prix
        '''
        today = datetime.today().date()
        day = self.day
        if self.day > today:
            raise ErreurDate("Date invalide: " + str(day))
        decalage = timedelta(days = 1)
        price = produire_historique(self.symbole, self.day, self.day,'fermeture')
        while not price:
            day = day - decalage
            price = produire_historique(self.symbole, day, day,'fermeture')
        return (price[0])[1]
