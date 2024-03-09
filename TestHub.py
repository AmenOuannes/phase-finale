''' Cellule de test '''
import json

class Folio():
    '''
    class folio
    '''
    def __init__(self, nom_portefeuille='folio'):
        self.nom_portefeuille = nom_portefeuille
        self.contenu = self.lire_json()

    def lire_json(self):
        '''
        fonction lire_json
        '''
        try:
            with open(f"{self.nom_portefeuille}.json", 'r', encoding='utf-8') as fichier:
                return json.load(fichier)
        except FileNotFoundError:
            return {"liquidites": 0, "titres": {}}

    def ecrire_json(self):
        '''
        fonction ecrire_json
        '''
        with open(f"{self.nom_portefeuille}.json", 'w', encoding='utf-8') as fichier:
            json.dump(self.contenu, fichier, indent=2)
