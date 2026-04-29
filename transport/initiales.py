def nord_ouest(n, m, provisions, commandes):
    transport = [[0 for _ in range(m)] for _ in range(n)]

    prov_rest = provisions.copy()
    cmd_rest = commandes.copy()

    i = 0
    j = 0

    while i < n and j < m:
        qte = min(prov_rest[i], cmd_rest[j])
        transport[i][j] = qte

        prov_rest[i] -= qte
        cmd_rest[j] -= qte

        if prov_rest[i] == 0 and cmd_rest[j] == 0:
            i += 1
            j += 1
        elif prov_rest[i] == 0:
            i += 1
        elif cmd_rest[j] == 0:
            j += 1

    return transport


def calcul_penalites(couts, lignes_actives, colonnes_actives):
    n = len(couts)
    m = len(couts[0])

    penal_l = [None] * n
    penal_c = [None] * m

    for i in range(n):
        if not lignes_actives[i]:
            continue

        valeurs = [couts[i][j] for j in range(m) if colonnes_actives[j]]

        if len(valeurs) >= 2:
            valeurs.sort()
            penal_l[i] = valeurs[1] - valeurs[0]
        elif len(valeurs) == 1:
            penal_l[i] = valeurs[0]

    for j in range(m):
        if not colonnes_actives[j]:
            continue

        valeurs = [couts[i][j] for i in range(n) if lignes_actives[i]]

        if len(valeurs) >= 2:
            valeurs.sort()
            penal_c[j] = valeurs[1] - valeurs[0]
        elif len(valeurs) == 1:
            penal_c[j] = valeurs[0]

    return penal_l, penal_c


def balas_hammer(n, m, couts, provisions, commandes, afficher_details=True):
    transport = [[0 for _ in range(m)] for _ in range(n)]

    prov_rest = provisions.copy()
    cmd_rest = commandes.copy()

    lignes_actives = [True] * n
    colonnes_actives = [True] * m

    while any(lignes_actives) and any(colonnes_actives):
        penal_l, penal_c = calcul_penalites(couts, lignes_actives, colonnes_actives)

        max_pen = -1
        choix = ("ligne", -1)

        for i in range(n):
            if penal_l[i] is not None and penal_l[i] > max_pen:
                max_pen = penal_l[i]
                choix = ("ligne", i)

        for j in range(m):
            if penal_c[j] is not None and penal_c[j] > max_pen:
                max_pen = penal_c[j]
                choix = ("colonne", j)

        if afficher_details:
            print("\nPénalités lignes :", penal_l)
            print("Pénalités colonnes :", penal_c)
            print("Pénalité maximale :", max_pen, "sur", choix[0], choix[1] + 1)

        if choix[0] == "ligne":
            i = choix[1]
            j = min(
                [j for j in range(m) if colonnes_actives[j]],
                key=lambda j: couts[i][j]
            )
        else:
            j = choix[1]
            i = min(
                [i for i in range(n) if lignes_actives[i]],
                key=lambda i: couts[i][j]
            )

        if afficher_details:
            print(f"Arête choisie à remplir : P{i + 1} -> C{j + 1}")

        qte = min(prov_rest[i], cmd_rest[j])
        transport[i][j] = qte

        prov_rest[i] -= qte
        cmd_rest[j] -= qte

        if prov_rest[i] == 0:
            lignes_actives[i] = False

        if cmd_rest[j] == 0:
            colonnes_actives[j] = False

    return transport


def cout_total(couts, transport):
    total = 0

    for i in range(len(couts)):
        for j in range(len(couts[0])):
            total += couts[i][j] * transport[i][j]

    return total