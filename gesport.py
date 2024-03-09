'''gesport'''
import argparse
from datetime import datetime
import numpy as np
from portefeuille import Portefeuille

from bourse import Bourse

#analyse des commandes
CH = "A AAPl C GOOG HOG HPQ INTC IBM LUV MMM MSFT T TGT TXN XOM WMT"

def analyser_commande():
    'fonction analyse_commande'
    parser = argparse.ArgumentParser(
        description = 'Gestionnaire de portefeuille d\'actions',
        usage = '%(prog)s ACTION [-h] [-d DATE] [-q INT] [-t STRING [STRING [STRING ...]]]'
        '\n[-r FLOAT] [-v FLOAT] [-g BOOL] [-p STRING]'

    )
    parser.add_argument(
        '-d', '--date', metavar = 'DATE',
        type = str, help = "Date effective (par défaut, date du jour)",
        default = str(datetime.today().date())
    )
    parser.add_argument(
        '-q', '--quantité', metavar = 'INT',
        type = str, help = "Quantité désirée (par défaut: 1)",
        default = 1
    )
    parser.add_argument(
        '-t', '--titres', metavar = 'STRING [STRING [STRING ...]]',
        type = str,
        help = "Le ou les titres à considérer"
                "(par défaut, tous les titres du portefeuille sont considérés)",
        default = CH
    )
    parser.add_argument(
        '-r', '--rendement', metavar = 'FLOAT', type = float,
        help = 'Rendement annuel global (par défaut, 0)', default = 0
    )
    parser.add_argument(
        '-v', '--volatilité', metavar = 'FLOAT',
        type = float, help = "Indice de volatilité global sur le rendement annuel\n(par défaut, 0)",
        default = 0
    )
    parser.add_argument(
        '-g', '--graphique', metavar = 'BOOL', type = bool,
        default = None, help = "Affichage graphique (par défaut, pas d'affichage graphique)"
    )
    parser.add_argument(
        '-p', '--portefeuille', metavar = 'STRING', type = str, default = 'folio',
        help = 'Nom de portefeuille (par défaut, utiliser folio)'
    )
    actions_parser = parser.add_subparsers(title='ACTIONS', dest='action',
                                            help='Action à effectuer')
    deposer_parser = actions_parser.add_parser('déposer', help='À la date spécifiée,'
                                               'déposer la quantité de dollars spécifiée')
    deposer_parser.add_argument('--date', help='Date spécifiée')
    deposer_parser.add_argument('--quantité', type=float, help='Quantité de dollars à déposer')
    deposer_parser.add_argument('--portefeuille', type=str, help='fichier de depot')

# Action: Acheter
    acheter_parser = actions_parser.add_parser('acheter', help='À la date spécifiée'
                                               'acheter la quantité spécifiée des titres spécifiés')
    acheter_parser.add_argument('--date', metavar = 'DATE', help='Date spécifiée')
    acheter_parser.add_argument('--titres', nargs='+', help='Titres à acheter')
    acheter_parser.add_argument('--quantité', type=float, help='Quantité à acheter', default=1.0)
    acheter_parser.add_argument('--portefeuille', type=str, help='fichier de depot')

# Action: Vendre
    vendre_parser = actions_parser.add_parser('vendre', help='À la date spécifiée,'
                                              'vendre la quantité spécifiée des titres spécifiés')
    vendre_parser.add_argument('--date', help='Date spécifiée')
    vendre_parser.add_argument('--titres', nargs='+', help='Titres à vendre')
    vendre_parser.add_argument('--quantité', type=float, help='Quantité à vendre', default=1.0)
    vendre_parser.add_argument('--portefeuille', type=str, help='fichier de depot')

# Action: Lister
    lister_parser = actions_parser.add_parser('lister', help='À la date spécifiée,'
                                              'lister les nombres d\'actions détenues'
                                               'ainsi que leur valeur totale')
    lister_parser.add_argument('--date', help='Date spécifiée')
    lister_parser.add_argument('--titres', nargs='+', help='Titres à lister')
    lister_parser.add_argument('--portefeuille', type=str, help='fichier de depot')

# Action: Projeter
    projeter_parser = actions_parser.add_parser('projeter',
                help='À la date future spécifiée, projeter la valeur totale des titres spécifiés,'
                            'en tenant compte des rendements et indices de volatilité spécifiés')
    projeter_parser.add_argument('--date_future', help='Date future spécifiée')
    projeter_parser.add_argument('--rendements', type=float, help='Rendements spécifiés')
    projeter_parser.add_argument('--volatilite', type=float, help='Indice de volatilité spécifié')
    projeter_parser.add_argument('--portefeuille', type=str, help='fichier de depot')

    return parser.parse_args()

def actions(args, folio, date=datetime.today().date()):
    'fonction actions'
    folio.data = folio.lire_json()
    update(folio)
    if args.action == 'déposer':
        folio.déposer(int(args.quantité), date)
        print(f'solde = {folio.solde(date):.2f}')
        folio.data = folio.ecrire_json()

    elif args.action == 'acheter':
        for i in args.titres:
            folio.acheter(i, args.quantité, date)
            print(f'solde = {folio.solde(date):.2f}')
        folio.ecrire_json()

    elif args.action == 'vendre':
        for i in args.titres:
            folio.vendre(i, args.quantité, date)
        print(f'solde = {folio.solde(date):.2f}')
        folio.ecrire_json()

    elif args.action == 'lister':
        day = date.strftime('%Y-%m-%d')
        for key, value in folio.historique[day].items():
            if value != 0:
                print(f'{key} = {int(value)} * {Bourse(key, date).prix()} = '
                      f'{int(value)*Bourse(key, date).prix():.2f}')

    elif args.action == 'projeter':
        date_future = datetime.strptime(args.date_future, "%Y-%m-%d").date()
        print(f'valeurs projetée ='
              f'{projeter(folio, date_future,float(args.rendement), float(args.volatilité))}')   

def projeter(folio, date, rendement, volatilite):
    'fonction projeter'
    rendements_simules = np.random.normal(loc=rendement, scale=volatilite, size=1000)
    projections = folio.valeur_projetée(date, rendement) * np.exp(rendements_simules)

    q1 = np.percentile(projections, 25)
    q2 = np.percentile(projections, 50)
    q3 = np.percentile(projections, 75)

    return f"{q1:.2f}, {q2:.2f}, {q3:.2f}"
def update(folio):
    'fonction update'
    folio.balance = folio.data["solde"]
    folio.assets = folio.data["titres"]
    folio.historique = folio.data["historique"]
    folio.solde_du_jour = folio.data["solde_du_jour"]
arg = analyser_commande()
dat = datetime.strptime(arg.date, "%Y-%m-%d").date()
actions(arg, Portefeuille(arg.portefeuille), dat)
