"""
Takeo

CODE PRINCIPAL
"""

import Effet_de_serre as eds
import Environnement as env
import Ventilation as vent

msg_erreur = "Valeur non valide, veuillez réessayer"


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
            val = input(msg)
            float(val)
            cond = False
        except:
            print("Erreur :", msg_erreur)

    return float(val)


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
    Tfluide, a, b, Tamb, Esol, Texp, HR, Masse_aliment, Yamb, Ymax
    """
    print("\n", "#" * 50, "\n", sep="")
    print("Partie Effet de serre :\n")

    Tfluide = inputIfDeci("T que l'on veut atteindre [C°] = ") + 273.15
    a = inputIfDeci("Longueur de la section de la boîte [m] = ")
    b = inputIfDeci("Hauteur de la section de la boîte [m] = ")

    print("\n", "#" * 50, "\n", sep="")
    print("Partie Environnement :\n")

    Tamb = inputIfDeci("Température ambiante [C°] = ") + 273.15
    Esol = inputIfDeci("Energie solaire reçue au sol au cours d'une journée [MJ/m²] = ")
    Temps_sol = inputIfDuree("Heure de lever du soleil (exemple : 18h30)= ",
                             "Heure de coucher du soleil (exemple : 18h30)= ",
                             "Echec de la conversion en duree. Veillez à bien formatter les heures. Veuillez réessayer.")
    HRamb = inputIfDeci("Humidité relative ambiante en pourcents = ")

    print("\n", "#" * 50, "\n", sep="")
    print("Partie Ventilation :\n")

    Masse_aliment = inputIfDeci("Masse de l'aliment que vous souhaitez sécher [kg] = ")
    Masse_epmsi = inputIfDeci("Masse d'eau par kg de matière sèche initiale [kg] = ")
    Masse_epmsf = inputIfDeci("Masse d'eau par kg de matière sèche que l'on souhaite atteindre au final [kg] = ")

    assert Masse_epmsi < Masse_epmsf, "Erreur : vous avez entré une masse d'eau finale dans l'aliment supérieure à la masse d'eau initiale !"

    Temps_sec = inputIfDeci("Temps de séchage souhaité [heures] = ")
    HRmax = inputIfDeci("Humidité relative maximale dans le séchoir en pourcents= ")

    return Tfluide, a, b, Tamb, Esol, Temps_sol, HRamb, Masse_aliment, Masse_epmsi, Masse_epmsf, Temps_sec, HRmax


def main(mode=""):
    """
    Fonction principale qui exécute tout le code.
    """
    # INPUTS
    if mode == "test":
        Tfluide = 65 + 273.15
        a = .4
        b = .2
        Tamb = 30 + 273.15
        Esol = 19.6
        Temps_sol = 12
        HRamb = 80
        Masse_aliment = 20
        Masse_epmsi = 3
        Masse_epmsf = .1
        Temps_sec = 12
        HRmax = 30

    else:
        Tfluide, a, b, Tamb, Esol, Temps_sol, HRamb, Masse_aliment, Masse_epmsi, Masse_epmsf, Temps_sec, HRmax = userInputs()

    # OUPUTS
    Fd, Fi = env.flux_solaires(Tamb, Esol, Temps_sol, HRamb)
    Yamb = env.HRversY(HRamb, Tamb)
    Ymax = env.HRversY(HRmax, Tamb)

    Q = vent.Bloc_ventilation(Masse_aliment, Masse_epmsi, Masse_epmsf, Yamb, Ymax, Temps_sec)
    P = eds.Bloc_effet_de_serre(Tfluide, Fd, Fi, a, b)

    # PRINT
    print("\n", "#" * 50, "\n", sep="")
    print("OUTPUTS :")

    print("\nQ =\t\t", Q, "m³/s",
          "\nYamb =\t", Yamb, "kg d'eau par kg d'air sec",
          "\nYmax =\t", Ymax, "kg d'eau par kg d'air sec",
          "\nFd =\t", Fd, "W/m²",
          "\nFi =\t", Fi, "W/m²",
          "\nP  =\t", P[0], "W/m²",
          "\nTs =\t", P[1], "K",
          "\nTp =\t", P[2], "K",
          "\nFs =\t", P[3], "W/m²",
          "\nFp =\t", P[4], "W/m²",
          "\nRa =\t", P[5],
          "\nNu =\t", P[6],
          "\nh  =\t", P[7])

    return None


main(input("> 'test' pour passer en mode test\n> touche Enter pour passer en mode input\n").lower())
