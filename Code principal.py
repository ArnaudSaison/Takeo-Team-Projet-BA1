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


# Données de test
def donnees():
    """Fonction qui permet d'appeler des valeurs de test"""
    Tfluide = 65 + 273.15
    a = .3
    b = .2
    Tamb = 30 + 273.15
    Esol = 19.6
    Temps_sol = 12
    HRamb = 80
    Masse_aliment = .5
    Masse_epmsi = 3
    Masse_epmsf = .1
    Temps_sec = 12
    HRmax = 20

    return Tfluide, a, b, Tamb, Esol, Temps_sol, HRamb, Masse_aliment, Masse_epmsi, Masse_epmsf, Temps_sec, HRmax


def printline(largeur=75):
    """Fonction qui imprime une ligne de séparation"""
    print("\n", "#" * largeur, "\n", sep="")


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
            print("Erreur :", msg_erreur)

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
            print("Erreur :", msg_erreur)

    return Temps


def userInputs():
    """
    Fonction qui traite les inputs.

    :return: toutes le valeurs des inputs dans l'odre suivant :
    Tfluide, a, b, Tamb, Fd, Fi, HRamb, Masse_aliment, Masse_epmsi, Masse_epmsf, Temps_sec, HRmax
    """
    # Effet de serre
    printline()
    print("Partie Effet de serre :\n")

    Tfluide = inputIfDeci("T que l'on veut atteindre [C°] = ") + 273.15
    a = inputIfDeci("Longueur de la section de la boîte [m] = ")
    b = inputIfDeci("Hauteur de la section de la boîte [m] = ")

    # Environnement
    printline()
    print("Partie Environnement :\n")

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
    print("Partie Ventilation :\n")

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
    print("Partie Effet de serre :\n")

    Tfluide = inputIfDeci("T que l'on veut atteindre [C°] = ") + 273.15
    a = inputIfDeci("Longueur de la section de la boîte [m] = ")
    b = inputIfDeci("Hauteur de la section de la boîte [m] = ")

    # Environnement
    printline()
    print("Partie Environnement :\n")

    Tamb = inputIfDeci("Température ambiante [C°] = ") + 273.15
    Fd = inputIfDeci("Flux solaire direct = ", "Nombre non valide")
    Fi = inputIfDeci("Flux solaire indirect = ", "Nombre non valide")
    HRamb = inputIfDeci("Humidité relative ambiante en pourcents = ")

    # Ventilation
    printline()
    print("Partie Ventilation :\n")

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


def main(mode="labo", donnees_m=donnees()):
    """
    Fonction principale qui exécute tout le code.
    """
    print("mode : ", mode)

    # INPUTS
    if mode == "test":
        Tfluide, a, b, Tamb, Fd, Fi, HRamb, Masse_aliment, Masse_epmsi, Masse_epmsf, Temps_sec, HRmax = donnees_m

    if mode == "labo":
        Tfluide, a, b, Tamb, Fd, Fi, HRamb, Masse_aliment, Masse_epmsi, Masse_epmsf, Temps_sec, HRmax = labInputs()

    else:
        Tfluide, a, b, Tamb, Fd, Fi, HRamb, Masse_aliment, Masse_epmsi, Masse_epmsf, Temps_sec, HRmax = userInputs()

    # OUPUTS
    Yamb = env.HRversY(HRamb, Tamb)
    Ymax = env.HRversY(HRmax, Tamb)

    Q, J = vent.Bloc_ventilation(Masse_aliment, Masse_epmsi, Masse_epmsf, Yamb, Ymax, Temps_sec)
    P = eds.Bloc_effet_de_serre(Tfluide, Fd, Fi, a, b)

    D = Q / rho

    L = dimensionnement(P[0], a, Q, Tfluide, Tamb, J)

    # PRINT
    printline()
    print("OUTPUTS :")

    print("\nL =\t\t", round(L, 3), "m",
          "\nJ =\t\t", round(J, 6), "kg/s",
          "\nQ =\t\t", round(Q, 6), "kg/s",
          "\nDébit =\t", round(D, 6), "m³/s",
          "\nDébit =\t", round(D * 60, 6), "m³/min",
          "\nDébit =\t", round(D * 3600, 3), "m³/h",
          "\nYamb =\t", round(Yamb, 6), "kg d'eau par kg d'air sec",
          "\nYmax =\t", round(Ymax, 6), "kg d'eau par kg d'air sec",
          "\nFd =\t", round(Fd, 3), "W/m²",
          "\nFi =\t", round(Fi, 3), "W/m²",
          "\nP  =\t", round(P[0], 3), "W/m²",
          "\nTs =\t", round(P[1], 3), "K",
          "\nTp =\t", round(P[2], 3), "K",
          "\nFs =\t", round(P[3], 3), "W/m²",
          "\nFp =\t", round(P[4], 3), "W/m²",
          "\nRa =\t", round(P[5], 3),
          "\nNu =\t", round(P[6], 3),
          "\nh  =\t", round(P[7], 3))

    return None


if __name__ == '__main__':
    main()