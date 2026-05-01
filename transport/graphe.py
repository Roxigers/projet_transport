from collections import deque


def base_initiale(transport):
    aretes = []

    for i in range(len(transport)):
        for j in range(len(transport[0])):
            if transport[i][j] > 0:
                aretes.append((i, j))

    return aretes


def trouver(parent, x):
    if parent[x] != x:
        parent[x] = trouver(parent, parent[x])
    return parent[x]


def union(parent, a, b):
    ra = trouver(parent, a)
    rb = trouver(parent, b)

    if ra != rb:
        parent[rb] = ra
        return True

    return False


def rendre_non_degenere(couts, transport, base=None):
    n = len(couts)
    m = len(couts[0])

    if base is None:
        aretes = base_initiale(transport)
    else:
        aretes = base.copy()

    parent = list(range(n + m))

    base_sans_cycle = []

    for i, j in aretes:
        if union(parent, i, n + j):
            base_sans_cycle.append((i, j))

    aretes = base_sans_cycle

    candidates = []

    for i in range(n):
        for j in range(m):
            if (i, j) not in aretes:
                candidates.append((couts[i][j], i, j))

    candidates.sort()

    for cout, i, j in candidates:
        if len(aretes) == n + m - 1:
            break

        if union(parent, i, n + j):
            aretes.append((i, j))

    return aretes


def construire_graphe_base(n, m, aretes_base):
    graphe = {}

    for i in range(n):
        graphe[("P", i)] = []

    for j in range(m):
        graphe[("C", j)] = []

    for i, j in aretes_base:
        p = ("P", i)
        c = ("C", j)

        graphe[p].append(c)
        graphe[c].append(p)

    return graphe


def test_connexe_bfs(n, m, aretes_base):
    graphe = construire_graphe_base(n, m, aretes_base)

    visites = set()
    composantes = []

    for sommet in graphe:
        if sommet not in visites:
            file = deque([sommet])
            visites.add(sommet)
            composante = []

            while file:
                courant = file.popleft()
                composante.append(courant)

                for voisin in graphe[courant]:
                    if voisin not in visites:
                        visites.add(voisin)
                        file.append(voisin)

            composantes.append(composante)

    if len(composantes) == 1:
        print("Test connexité BFS : graphe connexe.")
        return True

    print("Test connexité BFS : graphe non connexe.")
    print("Sous-graphes connexes :")

    for k, comp in enumerate(composantes, 1):
        affichage = [f"{s[0]}{s[1] + 1}" for s in comp]
        print(f"Composante {k} :", affichage)

    return False


def test_acyclique_bfs(n, m, aretes_base):
    graphe = construire_graphe_base(n, m, aretes_base)

    visites = set()

    for depart in graphe:
        if depart not in visites:
            file = deque([depart])
            parent = {depart: None}
            visites.add(depart)

            while file:
                sommet = file.popleft()

                for voisin in graphe[sommet]:
                    if voisin not in visites:
                        visites.add(voisin)
                        parent[voisin] = sommet
                        file.append(voisin)

                    elif parent[sommet] != voisin:
                        print("Test acyclique BFS : cycle détecté.")
                        return False

    print("Test acyclique BFS : aucun cycle détecté.")
    return True


def chemin_entre_sommets(n, m, aretes_base, depart, arrivee):
    graphe = construire_graphe_base(n, m, aretes_base)

    file = deque([depart])
    parent = {depart: None}

    while file:
        sommet = file.popleft()

        if sommet == arrivee:
            break

        for voisin in graphe[sommet]:
            if voisin not in parent:
                parent[voisin] = sommet
                file.append(voisin)

    if arrivee not in parent:
        return None

    chemin = []
    courant = arrivee

    while courant is not None:
        chemin.append(courant)
        courant = parent[courant]

    chemin.reverse()
    return chemin