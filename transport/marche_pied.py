from transport.io_affichage import afficher_transport, afficher_matrice
from transport.initiales import cout_total
from transport.graphe import (
    rendre_non_degenere,
    test_acyclique_bfs,
    test_connexe_bfs,
    chemin_entre_sommets,
)
from transport.potentiels import (
    calcul_potentiels,
    calcul_couts_potentiels,
    calcul_couts_marginaux,
    trouver_arete_ameliorante,
)


def cycle_marche_pied(n, m, aretes_base, arete_ajoutee):
    i, j = arete_ajoutee

    depart = ("C", j)
    arrivee = ("P", i)

    chemin = chemin_entre_sommets(n, m, aretes_base, depart, arrivee)

    if chemin is None:
        return None

    cycle_cases = [arete_ajoutee]

    for k in range(len(chemin) - 1):
        a = chemin[k]
        b = chemin[k + 1]

        if a[0] == "P" and b[0] == "C":
            cycle_cases.append((a[1], b[1]))
        elif a[0] == "C" and b[0] == "P":
            cycle_cases.append((b[1], a[1]))

    return cycle_cases


def afficher_cycle(cycle):
    print("\nCycle trouvé :")

    signes = []

    for k, (i, j) in enumerate(cycle):
        signe = "+" if k % 2 == 0 else "-"
        signes.append((signe, i, j))
        print(f"{signe} P{i + 1} -> C{j + 1}")

    return signes


def maximiser_sur_cycle(transport, cycle):
    signes = []

    for k, (i, j) in enumerate(cycle):
        signe = "+" if k % 2 == 0 else "-"
        signes.append((signe, i, j))

    cases_moins = [(i, j) for signe, i, j in signes if signe == "-"]

    theta = min(transport[i][j] for i, j in cases_moins)

    print("\nMaximisation sur le cycle :")
    print("Conditions pour chaque case du cycle :")

    for signe, i, j in signes:
        ancienne_valeur = transport[i][j]

        if signe == "+":
            print(f"P{i + 1} -> C{j + 1} : {ancienne_valeur} + θ")
        else:
            print(f"P{i + 1} -> C{j + 1} : {ancienne_valeur} - θ >= 0")

    print("Donc θ = min des cases avec signe -")

    for i, j in cases_moins:
        print(f"P{i + 1} -> C{j + 1} contient {transport[i][j]}")

    print("θ =", theta)

    for signe, i, j in signes:
        if signe == "+":
            transport[i][j] += theta
        else:
            transport[i][j] -= theta

    print("\nValeurs après modification du cycle :")

    for signe, i, j in signes:
        print(f"P{i + 1} -> C{j + 1} devient {transport[i][j]}")

    aretes_supprimees = []

    for i, j in cases_moins:
        if transport[i][j] == 0:
            aretes_supprimees.append((i, j))

    if aretes_supprimees:
        print("Arête(s) supprimée(s) :")
        for i, j in aretes_supprimees:
            print(f"P{i + 1} -> C{j + 1}")
    else:
        print("Aucune arête supprimée.")

    return theta


def marche_pied_potentiels(n, m, couts, transport, provisions, commandes):
    iteration = 1

    while True:
        print("\n" + "-" * 60)
        print(f"ITÉRATION MARCHE-PIED {iteration}")
        print("-" * 60)

        afficher_transport(n, m, transport, provisions, commandes)
        print("Coût actuel =", cout_total(couts, transport))

        aretes_base = rendre_non_degenere(couts, transport)

        print("Arêtes de base =", [(i + 1, j + 1) for i, j in aretes_base])

        test_acyclique_bfs(n, m, aretes_base)
        test_connexe_bfs(n, m, aretes_base)

        u, v = calcul_potentiels(couts, aretes_base)

        print("Potentiels fournisseurs u =", u)
        print("Potentiels clients v =", v)

        couts_pot = calcul_couts_potentiels(couts, u, v)
        afficher_matrice(n, m, couts_pot, "Table des coûts potentiels")

        marginaux = calcul_couts_marginaux(couts, u, v)
        afficher_matrice(n, m, marginaux, "Table des coûts marginaux")

        arete, valeur = trouver_arete_ameliorante(marginaux, aretes_base)

        if arete is None:
            print("\nAucune arête améliorante : solution optimale trouvée.")
            print("Coût optimal =", cout_total(couts, transport))
            return transport

        i, j = arete
        print(
            f"\nArête améliorante : P{i + 1} -> C{j + 1} "
            f"avec coût marginal {valeur}"
        )

        cycle = cycle_marche_pied(n, m, aretes_base, arete)

        if cycle is None:
            print("Erreur : aucun cycle trouvé.")
            return transport

        afficher_cycle(cycle)

        theta = maximiser_sur_cycle(transport, cycle)

        if theta == 0:
            print("Attention : θ = 0, cas dégénéré particulier.")
            print("On arrête cette optimisation pour éviter une boucle infinie.")
            return transport

        iteration += 1