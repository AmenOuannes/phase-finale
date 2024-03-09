"""
Importation des modules nécessaires
"""
from datetime import date as dt
from datetime import datetime, timedelta
import json
from bourse import Bourse
import exceptions as exception


class Portefeuille():
    '''
    Class Portefeuille
    '''
    def __init__(self, nom_portefeuille = "folio"):
        self.balance = 0       #instance qui garde la valeur du solde à la date d'aujourd'hui
        self.historique = {}   #dico qui enregistre toutes les operations
        self.solde_du_jour = {} #dico qui enregistre le solde à la date t
        self.assets = {}        #dico qui garde toutes les actions achetés
        self.bourse = Bourse
        self.nom_portefeuille = nom_portefeuille
        self.data = self.lire_json()

    def lire_json(self):
        '''
        fonction lire_json
        '''
        try:
            with open(f"{self.nom_portefeuille}.json", 'r', encoding='utf-8') as fichier:
                return json.load(fichier)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"solde": 0, "titres": {}, "historique": {}, "solde_du_jour": {}}

    def ecrire_json(self):
        '''
        fonction ecrire_json
        '''
        data = {
        "solde": self.balance,
        "titres": self.assets,
        "historique": self.historique,
        "solde_du_jour": self.solde_du_jour
        }
        with open(f"{self.nom_portefeuille}.json", 'w', encoding='utf-8') as fichier:
            json.dump(data, fichier, indent=2)
        return fichier

    def déposer(self, montant, date = datetime.today().date()):
        '''
        déposer
        '''
        if date > datetime.today().date():
            raise exception.ErreurDate('date de soumission n\'existe pas : ' + str(date))
        self.balance += montant
        day = date.strftime('%Y-%m-%d')
        if day in self.historique:
            (self.historique[day])['dépot'] = montant + (self.historique[day]).get('dépot', 0)
        else:
            dico = {}
            dico['dépot'] = montant
            self.historique[day] = dico
        (self.solde_du_jour)[day] = self.balance
        return self
    def solde(self, date = datetime.today().date()):
        '''
        solde
        '''
        if date > datetime.today().date():
            raise exception.ErreurDate('date de consultation n\'existe pas : ' + str(date))
        day = date.strftime('%Y-%m-%d')
        return self.solde_du_jour.get(day, 0)
    def acheter(self, symbole, quantité, date = datetime.today().date()):
        '''
        achat 
        '''
        if date > datetime.today().date():
            raise exception.ErreurDate('date de d\'achat n\'existe pas : ' + str(date))
        prix_unitaire = (self.bourse(symbole, date)).prix()
        achat = prix_unitaire * quantité
        day = date.strftime('%Y-%m-%d')
        self.assets[symbole] = quantité + self.assets.get(symbole, 0)
        if self.balance < achat:
            raise exception.LiquiditéInsuffisante(f'Solde insuffisant : {self.balance} < {achat}')
        self.historique[day] = self.assets
        self.balance -= achat
        self.solde_du_jour[day] = self.balance
        return self
    def vendre(self, symbole, quantité, date = datetime.today().date()):
        '''
        vendre 
        '''
        if date > datetime.today().date():
            raise exception.ErreurDate('date de d\'achat n\'existe pas : ' + str(date))
        quantite_dispo = self.assets.get(symbole)
        if quantite_dispo < quantité:
            raise exception.ErreurQuantité(f'Pas assez d\'actions! : {quantite_dispo} < {quantité}')
        day = date.strftime('%Y-%m-%d')
        b =self.bourse(symbole, date)
        gain = quantité * b.prix()
        self.balance += gain
        self.solde_du_jour[day] = self.balance
        self.assets[symbole] -= quantité
        self.historique[day] = self.assets
        return self
    def titres(self, date = datetime.today().date()):
        '''
        titres
        '''
        if date > datetime.today().date():
            raise exception.ErreurDate('date de d\'achat n\'existe pas : ' + str(date))
        if date == datetime.today().date():
            return self.assets
        date_valide = chercheur_dates(self.historique, date)
        dico = {}
        day = date_valide.strftime('%Y-%m-%d')
        for clé in self.historique[day].keys():
            if clé != 'dépot':
                dico[clé] = int((self.historique[day])[clé])
        return dico
    def valeur_des_titres(self, symboles, date = datetime.today().date()):
        '''
        valeur des titres
        '''
        if date > datetime.today().date():
            raise exception.ErreurDate('date de d\'achat n\'existe pas : ' + str(date))
        valeur = 0
        dico = self.titres(date)
        for symbole in symboles:
            valeur += dico[symbole] * self.bourse(symbole, date).prix()
        return valeur
    def valeur_totale(self, date = datetime.today().date()):
        '''
        valeur totale
        '''
        if date > datetime.today().date():
            raise exception.ErreurDate('date de d\'achat n\'existe pas : ' + str(date))
        liste = list(self.titres(date).keys())
        date_valide = chercheur_dates(self.solde_du_jour, date)
        day = date_valide.strftime('%Y-%m-%d')
        return self.solde_du_jour[day] + self.valeur_des_titres(liste, date)
    def valeur_projetée(self, date, rendement):
        '''
        valeur projetée 
        '''
        if date <= datetime.today().date():
            raise exception.ErreurDate('date déjà passée!')
        valeur = 0
        if isinstance(rendement, float):
            for symbole, value in self.assets.items():
                valeur += value * prix_final(symbole, rendement, date)
        else:
            if not isinstance(rendement, dict):
                raise TypeError("Le rendement doit être de type float ou dict.")

            for symbole, value in self.assets.items():
                valeur += value * prix_final(symbole, rendement.get(symbole, 0), date)
        return valeur + self.balance
def prix_final(symbole, rendement, date):
    '''
    prix final
    '''
    value = Bourse(symbole, dt.today()).prix()
    années = date.year - dt.today().year
    jours = (date - dt.today()).days
    return round(value*((1+rendement/100)**années) + value * rendement * jours/36500, 3)
def chercheur_dates(dico, date):
    '''
    chercheur dates
    '''
    day = date.strftime('%Y-%m-%d')
    while day not in dico:
        date -= timedelta(days = 1)
        day = date.strftime('%Y-%m-%d')
    return date
