"""
Takeo

Logiciel pour le dimensionnement du séchoir à poivre créé dans le cadre du projet "Pepper Challenge".

Auteurs : Arnaud Saison, Michaël Feldman, Hind Bakkali Tahiri, Younes Bouhjar, Idil Ari, Joshua Nicdao Blanco
Date : Novembre et Décembre 2018
"""

import Effet_de_serre as eds
import Environnement as env
import Ventilation as vent

msg_erreur = "Valeur non valide, veuillez réessayer"
rho = 1.177
DHvap = 2346.2e3  # J / kg
Cairsec = 1009  # J / (kg * K)


def printline(largeur=75):
    """Fonction qui imprime une ligne de séparation"""
    print(format("\n" + "#" * largeur, "bleu"))


def format(s, c="rouge"):
    """
    Fonction qui met un texte dans le format demandé
    """
    dico_styles = {"reset": "\u001b[0m", "erreur": "\u001b[31m", "gras": "\u001b[1m", "blanc": "\u001b[30;1m", "vert": "\u001b[32m",
                   "bleu": "\u001b[34m", "rouge": "\u001b[31m"}
    assert c in dico_styles
    return dico_styles[c] + s + dico_styles["reset"]


# Données de test
def donnees(mode=1):
    """Fonction qui permet d'appeler des valeurs de test"""
    Tfluide = 65 + 273.15
    a = .30
    b = .2
    Tamb = 20 + 273.15
    Esol = 19.6
    Temps_sol = 12
    HRamb = 50
    Masse_aliment = .5
    Masse_epmsi = 3
    Masse_epmsf = .1
    Temps_sec = 5
    HRmax = 20

    if mode == 1:
        Fd = 900
        Fi = 100


    else:
        # Calcul des flux solaires
        Fd, Fi = env.flux_solaires(Tamb, Esol, Temps_sol, HRamb)

    return Tfluide, a, b, Tamb, Fd, Fi, HRamb, Masse_aliment, Masse_epmsi, Masse_epmsf, Temps_sec, HRmax


def inputIfDeci(msg, msg_erreur=msg_erreur):
    """
    Fonction qui vérifie que les inputs sont des nombres et re-demande tant que ce n'en sont pas.

    :param msg: message à afficher quand on demande un input
    :param msg_erreur: message à afficher quand l'input d'est pas un nombre
    :return: input
    """
    val = ""
    cond = "True"

    while cond:
        try:
            val = float(input(msg))
            cond = False
        except:
            print(format("Erreur : " + msg_erreur, "erreur"))

    return val


def inputIfDuree(msg_lever, msg_coucher, msg_erreur=msg_erreur):
    """
    Fonction qui récupère une duree d'ensoleillement à partir d'une heure de lever et d'une heure de coucher.

    :return: (float) duree d'ensoleillement
    """
    Temps = 0
    cond = "True"

    while cond:
        try:
            # On récupère les heures de coucher et lever
            lever = input(msg_lever)
            coucher = input(msg_coucher)

            # On essaye de les convertir en une duree
            Temps = env.duree_journee(lever, coucher)

            # On arrête la boucle en mettant la condition à False
            cond = False
        except:
            print(format("Erreur : " + msg_erreur, "erreur"))

    return Temps


def userInputs():
    """
    Fonction qui traite les inputs.

    :return: toutes le valeurs des inputs dans l'odre suivant :
    Tfluide, a, b, Tamb, Fd, Fi, HRamb, Masse_aliment, Masse_epmsi, Masse_epmsf, Temps_sec, HRmax
    """
    # Effet de serre
    printline()
    print(format("► Partie Effet de serre :\n", "gras"))

    Tfluide = inputIfDeci("T que l'on veut atteindre [C°] = ") + 273.15
    a = inputIfDeci("Longueur de la section de la boîte [m] = ")
    b = inputIfDeci("Hauteur de la section de la boîte [m] = ")

    # Environnement : température et humidité ambiante, temps d'ensoleillement et énergie totale captée en une journée
    printline()
    print(format("► Partie Environnement :\n", "gras"))

    Tamb = inputIfDeci("Température ambiante [C°] = ") + 273.15
    Esol = inputIfDeci("Energie solaire reçue au sol au cours d'une journée [MJ/m²] = ")
    Temps_sol = inputIfDuree("Heure de lever du soleil (exemple : 18h30)= ",
                             "Heure de coucher du soleil (exemple : 18h30)= ",
                             "Echec de la conversion en duree. Veillez à bien formatter les heures. Veuillez réessayer.")
    HRamb = inputIfDeci("Humidité relative ambiante en pourcents = ")

    # Calcul des flux solaires
    Fd, Fi = env.flux_solaires(Tamb, Esol, Temps_sol, HRamb)

    # Ventilation
    printline()
    print(format("► Partie Ventilation :\n", "gras"))

    Masse_aliment = inputIfDeci("Masse de l'aliment que vous souhaitez sécher [kg] = ")
    Masse_epmsi = inputIfDeci("Masse d'eau par kg de matière sèche initiale [kg] = ")
    Masse_epmsf = inputIfDeci("Masse d'eau par kg de matière sèche que l'on souhaite atteindre au final [kg] = ")

    assert Masse_epmsi > Masse_epmsf, "Erreur : vous avez entré une masse d'eau finale dans l'aliment supérieure à la masse d'eau initiale !"

    Temps_sec = inputIfDeci("Temps de séchage souhaité [heures] = ")
    HRmax = inputIfDeci("Humidité relative maximale dans le séchoir en pourcents = ")

    return Tfluide, a, b, Tamb, Fd, Fi, HRamb, Masse_aliment, Masse_epmsi, Masse_epmsf, Temps_sec, HRmax


def labInputs():
    """
    Fonction qui traite les inputs.

    :return: toutes le valeurs des inputs dans l'odre suivant :
    Tfluide, a, b, Tamb, Fd, Fi, HRamb, Masse_aliment, Masse_epmsi, Masse_epmsf, Temps_sec, HRmax
    """
    # Effet de serre
    printline()
    print(format("► Partie Effet de serre :\n", "gras"))

    Tfluide = inputIfDeci("T que l'on veut atteindre [C°] = ") + 273.15
    a = inputIfDeci("Longueur de la section de la boîte [m] = ")
    b = inputIfDeci("Hauteur de la section de la boîte [m] = ")

    # Environnement
    printline()
    print(format("► Partie Environnement :\n", "gras"))

    Tamb = inputIfDeci("Température ambiante [C°] = ") + 273.15
    Fd = inputIfDeci("Flux solaire direct = ", "Nombre non valide")
    Fi = inputIfDeci("Flux solaire indirect = ", "Nombre non valide")
    HRamb = inputIfDeci("Humidité relative ambiante en pourcents = ")

    # Ventilation
    printline()
    print(format("► Partie Ventilation :\n", "gras"))

    Masse_aliment = inputIfDeci("Masse de l'aliment que vous souhaitez sécher [kg] = ")
    Masse_epmsi = inputIfDeci("Masse d'eau par kg de matière sèche initiale [kg] = ")
    Masse_epmsf = inputIfDeci("Masse d'eau par kg de matière sèche que l'on souhaite atteindre au final [kg] = ")

    assert Masse_epmsi > Masse_epmsf, "Erreur : vous avez entré une masse d'eau finale dans l'aliment supérieure à la masse d'eau initiale !"

    Temps_sec = inputIfDeci("Temps de séchage souhaité [heures] = ")
    HRmax = inputIfDeci("Humidité relative maximale dans le séchoir en pourcents = ")

    return Tfluide, a, b, Tamb, Fd, Fi, HRamb, Masse_aliment, Masse_epmsi, Masse_epmsf, Temps_sec, HRmax


def dimensionnement(P, l, Q, T, Tamb, J):
    """
    Fonction qui calcule la longueur de la zone de chauffage permettant d'obtenir la température voulue dans la zone de séchage.

    :param P: puissance développée par effet de serre par mètre carré de serre en W / m^2
    :param l: largeur de la boîte de chauffage en m
    :param Q: débit d'air nécessaire en kg / s
    :param T: température que l'on veut atteindre dans la zone de séchage
    :param Tamb: température de l'air ambiant
    :return: longueur de la zone de chauffage
    """
    L = ((J * DHvap) + ((T - Tamb) * Cairsec * Q)) / (P * l)
    return L


def main(mode="labo"):
    """
    Fonction principale qui exécute tout le code.
    """

    # INPUTS
    if "test" in mode:
        if mode == "test":
            Tfluide, a, b, Tamb, Fd, Fi, HRamb, Masse_aliment, Masse_epmsi, Masse_epmsf, Temps_sec, HRmax = donnees(0)

        elif mode == "test1":
            Tfluide, a, b, Tamb, Fd, Fi, HRamb, Masse_aliment, Masse_epmsi, Masse_epmsf, Temps_sec, HRmax = donnees(1)


    elif mode == "labo":
        Tfluide, a, b, Tamb, Fd, Fi, HRamb, Masse_aliment, Masse_epmsi, Masse_epmsf, Temps_sec, HRmax = labInputs()

    else:
        Tfluide, a, b, Tamb, Fd, Fi, HRamb, Masse_aliment, Masse_epmsi, Masse_epmsf, Temps_sec, HRmax = userInputs()

    # OUPUTS
    Yamb = env.HRversY(HRamb, Tamb)
    Ymax = env.HRversY(HRmax, Tfluide)

    Q, J = vent.Bloc_ventilation(Masse_aliment, Masse_epmsi, Masse_epmsf, Yamb, Ymax, Temps_sec)
    P = eds.Bloc_effet_de_serre(Tfluide, Fd, Fi, a, b)

    D = Q / rho

    L = dimensionnement(P[0], a, Q, Tfluide, Tamb, J)

    # PRINT
    printline()
    print(format("► Résultats :", "gras"))

    print("\u001b[1;32m" + "\nLongueur =", round(L, 2), "m" + "\u001b[0m",
          "\nJ =\t\t", round(J, 6), "kg/s",
          "\nQ =\t\t", round(Q, 6), "kg/s",
          "\u001b[1;32m" + "\nDébit =\t", round(D, 6), "m³/s",
          "\nDébit =\t", round(D * 60, 6), "m³/min",
          "\nDébit =\t", round(D * 3600, 3), "m³/h",
          "\nDébit =\t", round(D / (0.04 ** 2 * 3.1416), 3), "m/s (pour 4cm de dimaètre)" + "\u001b[0m",
          "\nYamb =\t", round(Yamb, 6), "kg d'eau par kg d'air sec",
          "\nYmax =\t", round(Ymax, 6), "kg d'eau par kg d'air sec",
          "\nFd =\t", round(Fd, 3), "W/m²",
          "\nFi =\t", round(Fi, 3), "W/m²",
          "\nP  =\t", round(P[0], 3), "W/m²",
          "\nTs =\t", round(P[1], 3), "K",
          "\nTp =\t", round(P[2], 3), "K",
          "\nFs =\t", round(P[3], 3), "W/m²",
          "\nFp =\t", round(P[4], 3), "W/m²",
          "\nRa =\t", int(P[5]),
          "\nRa / 10^7 =", round(P[5] / 10 ** 7, 2),
          "\u001b[1;35m" + "\nValidité des corrélations :", 10 ** 7 < P[5], "\u001b[0m",
          "\nNu =\t", round(P[6], 3),
          "\u001b[1;35m" + "\nh  =\t", round(P[7], 2)), "\u001b[0m"

    return None


if __name__ == '__main__':
    print("""\nChoisissez le mode de fonctionnement du logiciel :
    - test : calcul classique des flux solaires et données issues de la section \"données\" du code
    - test1 : toutes les données, y compris les flux solaires, sont à entrer dans la section \"données\" du code
    - labo : vous entrez directements les valeurs, y compris celles de flux solaire
    - appuyez sur ENTER pour utiliser le logiciel en mode classique. Vous devrez alors entrer toutes les données de terrain.""")
    m = input("\n\nmode (pour utiliser un mode sépacial : [test / test1 / labo ], sinon appuyez sur ENTER) : ")
    if m != "labo" and m != "test" and m != "test1":
        m = "terrain"

    print("\nmode activé :", format(m, "vert"))
    main(m)
