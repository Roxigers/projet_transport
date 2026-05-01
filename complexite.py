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


# ============================
# CONFIGURATION
# ============================

NB_TESTS = 100
TAILLES = [10, 20, 40, 60, 80, 100]

DOSSIER_RESULTATS = "analyse_complexite_transport"


# ============================
# GENERATION PROBLEME
# ============================

def generer_probleme_aleatoire(n):
    couts = [[random.randint(1, 100) for _ in range(n)] for _ in range(n)]
    flux = [[random.randint(1, 100) for _ in range(n)] for _ in range(n)]

    provisions = [sum(flux[i][j] for j in range(n)) for i in range(n)]
    commandes = [sum(flux[i][j] for i in range(n)) for j in range(n)]

    return couts, provisions, commandes


# ============================
# OUTILS
# ============================

def chrono(f):
    debut = time.perf_counter()
    res = f()
    fin = time.perf_counter()
    return res, fin - debut


def sans_affichage(f):
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        return f()


# ============================
# MESURE
# ============================

def mesurer(n):
    couts, provisions, commandes = generer_probleme_aleatoire(n)

    transport_no, theta_no = chrono(
        lambda: nord_ouest(n, n, provisions.copy(), commandes.copy())
    )

    _, t_no = chrono(
        lambda: sans_affichage(
            lambda: marche_pied_potentiels(
                n, n, couts,
                copy.deepcopy(transport_no),
                provisions.copy(),
                commandes.copy()
            )
        )
    )

    transport_bh, theta_bh = chrono(
        lambda: balas_hammer(
            n, n, couts,
            provisions.copy(),
            commandes.copy(),
            afficher_details=False
        )
    )

    _, t_bh = chrono(
        lambda: sans_affichage(
            lambda: marche_pied_potentiels(
                n, n, couts,
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


# ============================
# EXPERIENCE
# ============================

def lancer():
    os.makedirs(DOSSIER_RESULTATS, exist_ok=True)

    pires = []

    for n in TAILLES:
        print(f"\n===== n = {n} =====")

        valeurs = {
            "theta_no": [],
            "theta_bh": [],
            "t_no": [],
            "t_bh": [],
            "total_no": [],
            "total_bh": []
        }

        for i in range(NB_TESTS):
            print(f"Test {i+1}/{NB_TESTS}")

            try:
                res = mesurer(n)

                for k in valeurs:
                    valeurs[k].append(res[k])

            except Exception as e:
                print("Erreur :", e)
                break

        pire = {"n": n}

        for k in valeurs:
            if valeurs[k]:
                pire[k] = max(valeurs[k])
            else:
                pire[k] = 0

        pires.append(pire)

    generer_graphes(pires)
    sauvegarder_csv(pires)

    print("\nTerminé ✔️")


# ============================
# GRAPHES
# ============================

def tracer(pires, cle, titre, fichier):
    ns = [x["n"] for x in pires]
    ys = [x[cle] for x in pires]

    plt.figure()
    plt.plot(ns, ys, marker="o")
    plt.xlabel("n")
    plt.ylabel("Temps (s)")
    plt.title(titre)
    plt.grid()

    plt.savefig(os.path.join(DOSSIER_RESULTATS, fichier))
    plt.close()


def generer_graphes(pires):
    tracer(pires, "theta_no",
           "Initialisation Nord-Ouest",
           "01_initialisation_nord_ouest.png")

    tracer(pires, "theta_bh",
           "Initialisation Balas-Hammer",
           "02_initialisation_balas_hammer.png")

    tracer(pires, "t_no",
           "Marche-Pied après Nord-Ouest",
           "03_marche_pied_no.png")

    tracer(pires, "t_bh",
           "Marche-Pied après Balas-Hammer",
           "04_marche_pied_bh.png")

    tracer(pires, "total_no",
           "Total Nord-Ouest + Marche-Pied",
           "05_total_no.png")

    tracer(pires, "total_bh",
           "Total Balas-Hammer + Marche-Pied",
           "06_total_bh.png")


# ============================
# CSV
# ============================

def sauvegarder_csv(pires):
    chemin = os.path.join(DOSSIER_RESULTATS, "resultats.csv")

    with open(chemin, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=pires[0].keys())
        writer.writeheader()
        writer.writerows(pires)


# ============================
# MAIN
# ============================

if __name__ == "__main__":
    lancer()