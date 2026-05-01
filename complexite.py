import csv
import os
import time
import copy
import contextlib
import io
import random
import matplotlib.pyplot as plt

from transport.initiales import nord_ouest, balas_hammer
from transport.marche_pied import marche_pied_potentiels


NB_TESTS_REELS = 3

TAILLES = [10, 40, 100, 400, 1000, 4000, 10000]

DOSSIER_RESULTATS = "analyse_complexite_transport"


def generer_probleme_aleatoire(n):
    couts = [[random.randint(1, 100) for _ in range(n)] for _ in range(n)]

    flux = [[random.randint(1, 100) for _ in range(n)] for _ in range(n)]

    provisions = [
        sum(flux[i][j] for j in range(n))
        for i in range(n)
    ]

    commandes = [
        sum(flux[i][j] for i in range(n))
        for j in range(n)
    ]

    return couts, provisions, commandes


def chrono(fonction):
    debut = time.perf_counter()
    resultat = fonction()
    fin = time.perf_counter()
    return resultat, fin - debut


def sans_affichage(fonction):
    buffer = io.StringIO()

    with contextlib.redirect_stdout(buffer):
        resultat = fonction()

    return resultat


def mesurer_un_test(n):
    couts, provisions, commandes = generer_probleme_aleatoire(n)

    transport_no, theta_no = chrono(
        lambda: nord_ouest(
            n,
            n,
            provisions.copy(),
            commandes.copy()
        )
    )

    _, t_no = chrono(
        lambda: sans_affichage(
            lambda: marche_pied_potentiels(
                n,
                n,
                couts,
                copy.deepcopy(transport_no),
                provisions.copy(),
                commandes.copy()
            )
        )
    )

    transport_bh, theta_bh = chrono(
        lambda: balas_hammer(
            n,
            n,
            couts,
            provisions.copy(),
            commandes.copy(),
            afficher_details=False
        )
    )

    _, t_bh = chrono(
        lambda: sans_affichage(
            lambda: marche_pied_potentiels(
                n,
                n,
                couts,
                copy.deepcopy(transport_bh),
                provisions.copy(),
                commandes.copy()
            )
        )
    )

    return {
        "theta_no": theta_no,
        "theta_bh": theta_bh,
        "t_no": t_no,
        "t_bh": t_bh,
        "total_no": theta_no + t_no,
        "total_bh": theta_bh + t_bh
    }


def calculer_pire_cas_pour_n(n, lignes_n):
    colonnes = [
        "theta_no",
        "theta_bh",
        "t_no",
        "t_bh",
        "total_no",
        "total_bh"
    ]

    ligne = {"n": n}

    for col in colonnes:
        valeurs = [x[col] for x in lignes_n]
        ligne[col + "_pire_reel"] = max(valeurs)

    return ligne


def lancer_experience():
    os.makedirs(DOSSIER_RESULTATS, exist_ok=True)

    mesures_reelles = []
    pires_cas = []

    for n in TAILLES:
        print("\n" + "=" * 70)
        print(f"TAILLE n = {n}")
        print("=" * 70)

        lignes_n = []

        for test in range(1, NB_TESTS_REELS + 1):
            print(f"Test {test}/{NB_TESTS_REELS}")

            try:
                ligne = mesurer_un_test(n)
                ligne["n"] = n
                ligne["test"] = test

                mesures_reelles.append(ligne)
                lignes_n.append(ligne)

                print(
                    f"Initialisation Nord-Ouest = {ligne['theta_no']:.6f}s | "
                    f"Initialisation Balas-Hammer = {ligne['theta_bh']:.6f}s"
                )

                print(
                    f"Marche-Pied après Nord-Ouest = {ligne['t_no']:.6f}s | "
                    f"Marche-Pied après Balas-Hammer = {ligne['t_bh']:.6f}s"
                )

                print(
                    f"Total Nord-Ouest + Marche-Pied = {ligne['total_no']:.6f}s | "
                    f"Total Balas-Hammer + Marche-Pied = {ligne['total_bh']:.6f}s"
                )

            except MemoryError:
                print(f"Mémoire insuffisante pour n = {n}.")
                break

            except Exception as erreur:
                print(f"Erreur pour n = {n}, test = {test} : {erreur}")
                break

        if lignes_n:
            ligne_pire = calculer_pire_cas_pour_n(n, lignes_n)
            pires_cas.append(ligne_pire)

    sauvegarder_mesures_reelles(mesures_reelles)
    sauvegarder_pires_cas(pires_cas)
    generer_graphes(pires_cas)

    print("\nAnalyse terminée.")
    print("Dossier généré :", DOSSIER_RESULTATS)


def sauvegarder_mesures_reelles(mesures):
    chemin = os.path.join(
        DOSSIER_RESULTATS,
        "01_mesures_reelles.csv"
    )

    colonnes = [
        "n",
        "test",
        "theta_no",
        "theta_bh",
        "t_no",
        "t_bh",
        "total_no",
        "total_bh"
    ]

    with open(chemin, "w", newline="", encoding="utf-8") as fichier:
        writer = csv.DictWriter(fichier, fieldnames=colonnes)
        writer.writeheader()
        writer.writerows(mesures)

    print("Mesures réelles sauvegardées :", chemin)


def sauvegarder_pires_cas(pires_cas):
    chemin = os.path.join(
        DOSSIER_RESULTATS,
        "02_pires_cas.csv"
    )

    colonnes = [
        "n",
        "theta_no_pire_reel",
        "theta_bh_pire_reel",
        "t_no_pire_reel",
        "t_bh_pire_reel",
        "total_no_pire_reel",
        "total_bh_pire_reel"
    ]

    with open(chemin, "w", newline="", encoding="utf-8") as fichier:
        writer = csv.DictWriter(fichier, fieldnames=colonnes)
        writer.writeheader()
        writer.writerows(pires_cas)

    print("Pires cas sauvegardés :", chemin)


def tracer_graphe(pires_cas, colonne, titre, nom_fichier):
    ns = [ligne["n"] for ligne in pires_cas]
    temps = [ligne[colonne] for ligne in pires_cas]

    plt.figure()
    plt.plot(ns, temps, marker="o")
    plt.xlabel("n")
    plt.ylabel("Temps en secondes")
    plt.title(titre)
    plt.grid(True)

    chemin = os.path.join(DOSSIER_RESULTATS, nom_fichier)
    plt.savefig(chemin, dpi=200, bbox_inches="tight")
    plt.close()


def generer_graphes(pires_cas):
    graphes = [
        (
            "theta_no_pire_reel",
            "Initialisation Nord-Ouest",
            "03_initialisation_nord_ouest.png"
        ),
        (
            "theta_bh_pire_reel",
            "Initialisation Balas-Hammer",
            "04_initialisation_balas_hammer.png"
        ),
        (
            "t_no_pire_reel",
            "Marche-Pied après Nord-Ouest",
            "05_marche_pied_apres_nord_ouest.png"
        ),
        (
            "t_bh_pire_reel",
            "Marche-Pied après Balas-Hammer",
            "06_marche_pied_apres_balas_hammer.png"
        ),
        (
            "total_no_pire_reel",
            "Total Nord-Ouest + Marche-Pied",
            "07_total_nord_ouest_marche_pied.png"
        ),
        (
            "total_bh_pire_reel",
            "Total Balas-Hammer + Marche-Pied",
            "08_total_balas_hammer_marche_pied.png"
        )
    ]

    for colonne, titre, nom_fichier in graphes:
        tracer_graphe(pires_cas, colonne, titre, nom_fichier)

    print("Graphiques générés dans :", DOSSIER_RESULTATS)


if __name__ == "__main__":
    lancer_experience()