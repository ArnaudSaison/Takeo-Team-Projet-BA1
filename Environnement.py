"""
Takeo

CODE DU BLOC EFFET DE SERRE

     grandeur                 symbole     [unités]
Les inputs :
   - énergie solaire reçue    Esol        [MJ/m²]
   - température ambiante     Tamb        [C°]
   - temps d'exposition       Texp        [h]
   - humidité relative        HR          [adimensionnel] (exprimé en pourcents)

Les outputs :
   - flux solaire direct      Fd         [W/m²]
   - flux solaire indirect    Fi         [W/m²]
   - humidité absolue         Y          [adimensionnel]
"""

import math
import scipy.constants as cste

# CONSTANTES

# température dont on connait la pression de saturation (60°C) [K]
T0 = 333.15
# constante des gaz parfaits [J/K]
R = cste.R
# pression atmosphérique [Pa]
PATM = cste.atm
# chaleur latente molaire de vaporisation de l'eau [J/mol]
LAMBDA = 42440
# constante de Stefan-Boltzmann [W/m²K⁴]
SIGMA = cste.sigma

"""
Fonctions qui calculent le nombre d'heures dans une journée.
"""


def time2min(time):
    """Trasnforme l'heure en minutes"""
    return time[0] * 60 + time[1]


def min2time(min):
    """Trasnforme un nombre de minutes en heures"""
    hour = min // 60
    min = min % 60
    return (hour, min)


def min2hours(temps):
    """Converti un temps exprimé en heures et minutes vers un temps en heures"""
    return temps[0] + temps[1] / 60

def min2sec(min):
    return min * 60


def duree(debut, fin):
    """Renvoie la durée entre les deux heures donneés"""
    temps = time2min(fin) - time2min(debut)
    if temps < 0:
        temps += 24 * 60

    return min2time(temps)


def duree_journee(lever="6h30", coucher="18h30"):
    """Calcule la durée d'une jounée à partir des heures de lever et de coucher du soleil."""
    # Nettoyage et découpage des heures
    lever = lever.replace(" ", "").split("h")
    lever[0], lever[1] = float(lever[0]), float(lever[1])
    coucher = coucher.replace(" ", "").split("h")
    coucher[0], coucher[1] = float(coucher[0]), float(coucher[1])

    # Calcul de la duree
    temps = duree(lever, coucher)
    temps = temps[0] + temps[1] / 60

    return temps


"""
Fonctions du bloc environnement
"""


def FPsat(T):
    """
    Fonction qui calcule la pression de saturation Psat en fonction de la température T.
    """
    if T == T0:
        res = 2 * 10 ** 4
    else:
        deltaT = 1 / T - 1 / T0  # [1/K]
        expo = -LAMBDA * deltaT / R  # [adim]

        res = FPsat(T0) * math.exp(expo)  # [Pa]

    return res


# on attribue des valeurs par défaut pour les grandeurs dans le cas où elles ne sont pas données (Tamb de 30°C, Esol de 19.6 MJ/m², HR de 80%)

def flux_solaires(Tamb=303.15, Esol=19.6, Texp=12.0, HR=80.0):
    """
    Fonction qui calcule le flux solaire direct et indirect grâce à l'énegie solaire qui atteint le sol en une journée.

    :param Tamb: (float) température ambiante en degrés celsuis
    :param Esol: (float) énergie solaire reçue au cours d'une journée complète
    :param Texp: (float) temps que dure une journée en haures
    :return:    - (float) Flux direct en W/m²
                - (float) Flux indirect en W/m²
    """
    # passage pourcents -> décimales
    HR = HR / 100

    # flux direct :
    Fd = 10 ** 4 * Esol / (36 * Texp)  # 10**4 et 36 viennent de la conversion MJ -> J et h -> s

    # flux indirect :
    Tr = LAMBDA * Tamb / (LAMBDA - R * Tamb * math.log(HR))  # Tr est la température de rosée [K] et le log est un ln dans ce module

    Tr -= 273.15  # passage de K à °C
    Tciel = Tamb * (0.711 + 0.0056 * Tr + 7.3 * 10 ** (-5) * Tr ** 2) ** 0.25  # on néglige le cosinus car il est proche de 0
    Fi = SIGMA * Tciel ** 4

    return Fd, Fi


def HRversY(HR, T):
    """
    Fonction qui calcule l'humidité absolue à partir de l'humidité relative

    :param HR: (float) humidété relative en pourcent (ex : HR = 80.0 est 80%)
    :return: (float) humidité absolue en kg d'eau par kg de matière sèche
    """
    HR = HR / 100  # passage pourcents -> décimales

    # humidité absolue :
    Psat = FPsat(T)
    Y = HR * 0.62 * Psat / (PATM - Psat)  # 0.62 = Meau/Mair


    return Y
