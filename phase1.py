"""
importation des modules
"""
import argparse
from datetime import datetime
import json
import requests


#analyse des commandes
def analyser_commande():
    """
    Générer un interpréteur de commande.
    """
    valeurs = ['fermeture', 'ouverture', 'min', 'max', 'volume']
    parser = argparse.ArgumentParser(
        description='Extraction de valeurs historiques pour un ou plusieurs symboles boursiers.',
        usage='%(prog)s [-h] [-d DATE] [-f DATE] '
        '\n             [-v {fermeture,ouverture,min,max,volume}] '
        '\n             symbole [symbole ...]'
    )

    parser.add_argument(
        'symbole', metavar = 'symbole',
        type = str, help = "Nom d'un symbole boursier"
    )

    parser.add_argument(
        '-d', '--début', metavar = 'DATE',
        type = str, help = "Date recherchée la plus ancienne (format: AAAA-MM-JJ)"
    )

    parser.add_argument(
        '-f', '--fin', metavar = 'DATE',
        type = str, help = "Date recherchée la plus récente (format: AAAA-MM-JJ)"
    )

    parser.add_argument(
        '-v', '--valeur', metavar = '{fermeture,ouverture,min,max,volume}',
        type = str, choices = valeurs,
        default = 'fermeture', help = 'La valeur désirée (par défaut: fermeture)'
        )

    args = parser.parse_args()
    return args
#construire la data à afficher
def produire_historique(symbole, date_d, date_f, valeur):
    """
    fonction qui interagit avec le serveur du cours afin de récupérer l'historique 
    des symboles désirés.
    """
    liste = []
    url = f'https://pax.ulaval.ca/action/{symbole}/historique/'
    #impotation des donnés du site
    params1 = {'début': date_d, 'fin': date_f, }
    reponse = requests.get(url = url, params = params1, timeout = 10)
    fetch = json.loads((reponse.text)) #dictionnaire principale
    historique = fetch["historique"]    #dictionnnaire aux valeurs à traiter
    #parcours date par date
    for dates in historique.items():
        a = datetime.strptime(dates[0], '%Y-%m-%d').date(), dates[1].get(valeur)
        liste.append(a)  #remplissage du tableau
    return liste

#main
def main():
    """
    Fonction principale .
    arguments:
    dates converties en datetime.date()
    symbole
    valeurs
    +traitement de quelques cas particuliers.
    """
    arg = analyser_commande()
    symboles = ['A', 'AAPL', 'C', 'GOOG', 'HOG', 'HPQ',
                'INTC', 'IBM', 'LUV', 'MMM', 'MSFT', 'T',
                'TGT', 'TXN', 'XOM', 'WMT']
    # Traitement des cas particuliers
    if arg.symbole.upper() not in symboles:
        raise ValueError("Veuillez saisir une compagnie valide")
    if arg.début > arg.fin :
        raise ValueError("saisir une date de début avant la date de la fin")
    # Convertir les dates en date()
    date_d = datetime.strptime(arg.début, '%Y-%m-%d').date()
    date_f = datetime.strptime(arg.fin, '%Y-%m-%d').date()
    liste = produire_historique(arg.symbole, date_d, date_f, arg.valeur)
    # Affichage
    print(f'titre={arg.symbole}: valeur={arg.valeur}, début={date_d}, fin={date_f}')
    print(liste[::-1] if liste else 'la bourse est fermée dans cette période')

# Exécution du programme
if __name__ == "__main__":
    main()
