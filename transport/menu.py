from transport.io_affichage import lire_probleme, afficher_tableau, afficher_transport
from transport.initiales import nord_ouest, balas_hammer, cout_total
from transport.marche_pied import marche_pied_potentiels


def resoudre_probleme(numero, methode):
    nom_fichier = f"problemes/probleme{numero}.txt"

    n, m, couts, provisions, commandes = lire_probleme(nom_fichier)

    print("\n" + "=" * 60)
    print(f"PROBLÈME {numero}")
    print("=" * 60)

    afficher_tableau(n, m, couts, provisions, commandes)

    if methode == "NO":
        print("\n--- Nord-Ouest ---")
        transport = nord_ouest(n, m, provisions, commandes)

    elif methode == "BH":
        print("\n--- Balas-Hammer ---")
        transport = balas_hammer(n, m, couts, provisions, commandes, afficher_details=True)

    else:
        print("Méthode inconnue.")
        return

    afficher_transport(n, m, transport, provisions, commandes)
    print("Coût initial =", cout_total(couts, transport))

    print("\n--- Marche-pied avec potentiels ---")

    solution = marche_pied_potentiels(
        n, m, couts, transport, provisions, commandes
    )

    print("\nSolution finale :")
    afficher_transport(n, m, solution, provisions, commandes)
    print("Coût final =", cout_total(couts, solution))


def menu():
    while True:
        print("\n" + "=" * 40)
        print("MENU - PROJET TRANSPORT")
        print("=" * 40)
        print("1. Résoudre un problème avec Nord-Ouest")
        print("2. Résoudre un problème avec Balas-Hammer")
        print("3. Quitter")

        choix = input("Votre choix : ")

        if choix == "3":
            print("Fin du programme.")
            break

        if choix not in ["1", "2"]:
            print("Choix invalide.")
            continue

        try:
            numero = int(input("Numéro du problème (1 à 12) : "))
        except ValueError:
            print("Numéro invalide.")
            continue

        if numero < 1 or numero > 12:
            print("Le numéro doit être entre 1 et 12.")
            continue

        if choix == "1":
            resoudre_probleme(numero, "NO")
        elif choix == "2":
            resoudre_probleme(numero, "BH")