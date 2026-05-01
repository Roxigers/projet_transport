def calcul_potentiels(couts, aretes_base):
    n = len(couts)
    m = len(couts[0])

    u = [None] * n
    v = [None] * m

    u[0] = 0
    changement = True

    while changement:
        changement = False

        for i, j in aretes_base:
            if u[i] is not None and v[j] is None:
                v[j] = couts[i][j] - u[i]
                changement = True

            elif v[j] is not None and u[i] is None:
                u[i] = couts[i][j] - v[j]
                changement = True

    return u, v


def calcul_couts_potentiels(couts, u, v):
    n = len(couts)
    m = len(couts[0])

    potentiels = [[0 for _ in range(m)] for _ in range(n)]

    for i in range(n):
        for j in range(m):
            potentiels[i][j] = u[i] + v[j]

    return potentiels


def calcul_couts_marginaux(couts, u, v):
    n = len(couts)
    m = len(couts[0])

    marginaux = [[0 for _ in range(m)] for _ in range(n)]

    for i in range(n):
        for j in range(m):
            marginaux[i][j] = couts[i][j] - (u[i] + v[j])

    return marginaux


def trouver_arete_ameliorante(marginaux, aretes_base):
    meilleure_valeur = 0
    meilleure_arete = None

    n = len(marginaux)
    m = len(marginaux[0])

    for i in range(n):
        for j in range(m):
            if (i, j) not in aretes_base:
                if marginaux[i][j] < meilleure_valeur:
                    meilleure_valeur = marginaux[i][j]
                    meilleure_arete = (i, j)

    return meilleure_arete, meilleure_valeur


def toutes_aretes_ameliorantes(marginaux, aretes_base):
    aretes = []

    n = len(marginaux)
    m = len(marginaux[0])

    for i in range(n):
        for j in range(m):
            if (i, j) not in aretes_base and marginaux[i][j] < 0:
                aretes.append((i, j, marginaux[i][j]))

    aretes.sort(key=lambda x: x[2])

    return aretes