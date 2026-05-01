import os
import sys
from contextlib import redirect_stdout

from transport.io_affichage import lire_probleme, afficher_tableau, afficher_transport
from transport.initiales import nord_ouest, balas_hammer, cout_total
from transport.marche_pied import marche_pied_potentiels


GROUPE = "AFR7"
EQUIPE = "C"


def executer_trace(numero, methode):
    nom_fichier = f"problemes/probleme{numero}.txt"

    n, m, couts, provisions, commandes = lire_probleme(nom_fichier)

    print("=" * 60)
    print(f"GROUPE {GROUPE} - EQUIPE {EQUIPE}")
    print(f"PROBLEME {numero}")
    print(f"METHODE INITIALE : {methode.upper()}")
    print("=" * 60)

    afficher_tableau(n, m, couts, provisions, commandes)

    if methode == "no":
        print("\nProposition initiale : Nord-Ouest")
        transport = nord_ouest(n, m, provisions, commandes)
    else:
        print("\nProposition initiale : Balas-Hammer")
        transport = balas_hammer(n, m, couts, provisions, commandes, afficher_details=True)

    afficher_transport(n, m, transport, provisions, commandes)
    print("Coût initial =", cout_total(couts, transport))

    print("\nMarche-pied avec potentiels")
    solution = marche_pied_potentiels(n, m, couts, transport, provisions, commandes)

    print("\nSolution finale")
    afficher_transport(n, m, solution, provisions, commandes)
    print("Coût final =", cout_total(couts, solution))


def generer_toutes_les_traces():
    os.makedirs("traces", exist_ok=True)

    for numero in range(1, 13):
        for methode in ["no", "bh"]:
            nom_trace = f"{GROUPE}-{EQUIPE}-trace{numero}-{methode}.txt"
            chemin_trace = os.path.join("traces", nom_trace)

            with open(chemin_trace, "w", encoding="utf-8") as fichier:
                with redirect_stdout(fichier):
                    executer_trace(numero, methode)

            print("Trace générée :", chemin_trace)


if __name__ == "__main__":
    generer_toutes_les_traces()