def lire_probleme(nom_fichier):
    with open(nom_fichier, "r", encoding="utf-8") as fichier:
        lignes = fichier.readlines()

    n, m = map(int, lignes[0].split())

    couts = []
    provisions = []

    for i in range(1, n + 1):
        valeurs = list(map(int, lignes[i].split()))
        couts.append(valeurs[:m])
        provisions.append(valeurs[m])

    commandes = list(map(int, lignes[n + 1].split()))

    return n, m, couts, provisions, commandes


def afficher_tableau(n, m, couts, provisions, commandes):
    print("\nTableau des coûts :\n")

    print("      ", end="")
    for j in range(m):
        print(f"{'C' + str(j + 1):>6}", end="")
    print("   | Provision")

    print("-" * (10 + m * 6 + 15))

    for i in range(n):
        print(f"P{i + 1:<4}", end="")
        for j in range(m):
            print(f"{couts[i][j]:>6}", end="")
        print(f"   | {provisions[i]}")

    print("-" * (10 + m * 6 + 15))

    print("Cmd ", end="")
    for j in range(m):
        print(f"{commandes[j]:>6}", end="")
    print()


def afficher_transport(n, m, transport, provisions, commandes):
    print("\nProposition de transport :\n")

    print("      ", end="")
    for j in range(m):
        print(f"{'C' + str(j + 1):>6}", end="")
    print("   | Provision")

    print("-" * (10 + m * 6 + 15))

    for i in range(n):
        print(f"P{i + 1:<4}", end="")
        for j in range(m):
            print(f"{transport[i][j]:>6}", end="")
        print(f"   | {provisions[i]}")

    print("-" * (10 + m * 6 + 15))

    print("Cmd ", end="")
    for j in range(m):
        print(f"{commandes[j]:>6}", end="")
    print()


def afficher_matrice(n, m, matrice, titre):
    print(f"\n{titre} :\n")

    print("      ", end="")
    for j in range(m):
        print(f"{'C' + str(j + 1):>6}", end="")
    print()

    print("-" * (10 + m * 6))

    for i in range(n):
        print(f"P{i + 1:<4}", end="")
        for j in range(m):
            print(f"{matrice[i][j]:>6}", end="")
        print()