from transport.io_affichage import afficher_transport, afficher_matrice
from transport.initiales import cout_total
from transport.graphe import (
    base_initiale,
    rendre_non_degenere,
    test_acyclique_bfs,
    test_connexe_bfs,
    chemin_entre_sommets,
)
from transport.potentiels import (
    calcul_potentiels,
    calcul_couts_potentiels,
    calcul_couts_marginaux,
    toutes_aretes_ameliorantes,
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


def obtenir_cases_moins(cycle):
    cases_moins = []

    for k, (i, j) in enumerate(cycle):
        if k % 2 == 1:
            cases_moins.append((i, j))

    return cases_moins


def calcul_theta(transport, cycle):
    cases_moins = obtenir_cases_moins(cycle)

    if not cases_moins:
        return None

    return min(transport[i][j] for i, j in cases_moins)


def choisir_arete_sortante(transport, cycle, base):
    cases_moins = obtenir_cases_moins(cycle)
    theta = calcul_theta(transport, cycle)

    candidates = []

    for i, j in cases_moins:
        if transport[i][j] == theta and (i, j) in base:
            candidates.append((i, j))

    if not candidates:
        return None

    # En cas d'égalité, on choisit une arête de base à quantité nulle si possible.
    for i, j in candidates:
        if transport[i][j] == 0:
            return (i, j)

    return candidates[0]


def maximiser_sur_cycle(transport, cycle, base, arete_entrante):
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

    arete_sortante = choisir_arete_sortante(transport, cycle, base)

    for signe, i, j in signes:
        if signe == "+":
            transport[i][j] += theta
        else:
            transport[i][j] -= theta

    print("\nValeurs après modification du cycle :")

    for signe, i, j in signes:
        print(f"P{i + 1} -> C{j + 1} devient {transport[i][j]}")

    if arete_entrante not in base:
        base.append(arete_entrante)

    if arete_sortante is not None and arete_sortante in base:
        base.remove(arete_sortante)

    if theta == 0:
        print("\nPivot dégénéré : θ = 0.")
        print("La proposition ne change pas, mais la base est modifiée.")

    if arete_sortante is not None:
        i, j = arete_sortante
        print("Arête supprimée de la base :")
        print(f"P{i + 1} -> C{j + 1}")
    else:
        print("Aucune arête sortante trouvée.")

    return theta, arete_sortante


def nettoyer_base(base):
    nouvelle_base = []

    for arete in base:
        if arete not in nouvelle_base:
            nouvelle_base.append(arete)

    return nouvelle_base


def marche_pied_potentiels(n, m, couts, transport, provisions, commandes):
    iteration = 1
    iteration_max = 500

    base = base_initiale(transport)
    base = rendre_non_degenere(couts, transport, base)

    while iteration <= iteration_max:
        print(f"ITÉRATION MARCHE-PIED numéro {iteration}")

        afficher_transport(n, m, transport, provisions, commandes)
        print("Coût actuel =", cout_total(couts, transport))

        base = nettoyer_base(base)
        base = rendre_non_degenere(couts, transport, base)

        print("Arêtes de base =", [(i + 1, j + 1) for i, j in base])

        test_acyclique_bfs(n, m, base)
        test_connexe_bfs(n, m, base)

        u, v = calcul_potentiels(couts, base)

        print("Potentiels fournisseurs u =", u)
        print("Potentiels clients v =", v)

        couts_pot = calcul_couts_potentiels(couts, u, v)
        afficher_matrice(n, m, couts_pot, "Table des coûts potentiels")

        marginaux = calcul_couts_marginaux(couts, u, v)
        afficher_matrice(n, m, marginaux, "Table des coûts marginaux")

        aretes_am = toutes_aretes_ameliorantes(marginaux, base)

        if not aretes_am:
            print("\nAucune arête améliorante : solution optimale trouvée.")
            print("Coût optimal =", cout_total(couts, transport))
            return transport

        amelioration_faite = False

        for i, j, valeur in aretes_am:
            arete_entrante = (i, j)

            print(
                f"\nArête améliorante testée : P{i + 1} -> C{j + 1} "
                f"avec coût marginal {valeur}"
            )

            cycle = cycle_marche_pied(n, m, base, arete_entrante)

            if cycle is None:
                print("Cycle introuvable pour cette arête, on teste la suivante.")
                continue

            afficher_cycle(cycle)

            theta, arete_sortante = maximiser_sur_cycle(
                transport,
                cycle,
                base,
                arete_entrante
            )

            if arete_sortante is None:
                print("Impossible de faire sortir une arête, on teste la suivante.")
                continue

            amelioration_faite = True
            break

        if not amelioration_faite:
            print("\nAucune amélioration possible malgré des coûts marginaux négatifs.")
            print("Arrêt de sécurité.")
            print("Coût atteint =", cout_total(couts, transport))
            return transport

        iteration += 1

    print("\nNombre maximal d'itérations atteint.")
    print("Arrêt de sécurité.")
    return transport