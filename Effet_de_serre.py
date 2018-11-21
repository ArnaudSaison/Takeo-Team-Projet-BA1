"""
Bloc effet de serre
Team Takeo
"""

import numpy as np
import scipy.optimize as sp_op
import scipy.constants as cste

g = cste.g         # accélération gravifique
sigma = cste.sigma  # constante de Stefan Boltzmann pour équation corps noir

# Constantes :   sigma, g, v,        alpha,    Pr,    k,
constantes300 = (sigma, g, 1.578e-5, 2.213e-5, 0.713, 0.02623)
constantes310 = (sigma, g, 1.659e-5, 2.340e-5, 0.709, 0.02684)
constantes320 = (sigma, g, 1.754e-5, 2.476e-5, 0.708, 0.02753)
constantes330 = (sigma, g, 1.851e-5, 2.616e-5, 0.708, 0.02821)
constantes340 = (sigma, g, 1.951e-5, 2.821e-5, 0.707, 0.02888)


def Bloc_effet_de_serre(T, Fd, Fi, a, b, c=constantes320):
    """
    Caclule la puissance du capteur solaire en W/m^2.

    :param T: Température que l'on veut atteindre dans la serre
    :param Fd: Flux solaire direct
    :param Fi: Flux solaire indirect
    :param c: constantes : sigma, g, v, alpha, Pr, k
    :param L: périmètre de la section de la boîte
    :param a: longeur section
    :param b:
    :return P: Puissance développée par la serre
    """

    # Constantes convection
    sigma, g, v, alpha, Pr, k, beta = c[0], c[1], c[2], c[3], c[4], c[5], (1 / T)

    # Longueur carctéristique
    L = 2 * a * b / (a + b)

    # Définition du système d'équations
    def sys(x):
        # Inconnues
        P, Ts, Tp, Fs, Fp = x[0], x[1], x[2], x[3], x[4]

        # Inconnues convection
        Ra, Nu, h = x[5], x[6], x[7]

        # Vecteur qui va contenir les équations
        E = np.empty(8)

        # Equations
        E[0] = h * (Tp - T) + h * (Ts - T) - P
        E[1] = sigma * Tp ** 4 - Fp
        E[2] = sigma * Ts ** 4 - Fs
        E[3] = P + Fp - Fd - Fi
        E[4] = Fs + h * (Ts - T) - Fd - Fp

        # Equations de a convection
        E[5] = (h * L / k) - Nu
        E[6] = ((g * beta * (((Tp + Ts) / 2) - T) * L ** 3) / (alpha * v)) - Ra
        E[7] = (0.14 * (Ra ** (1 / 3)) * ((1.0 + 0.0107 * Pr) / (1.0 + 0.01 * Pr))) - Nu

        return E

    # Matrice d'initialisation qui va servir de base pour trouver les racines du système
    # x0 = np.array([100.0, 300.0, 300.0, 400.0, 400.0, 1.0, 1.0, 4.0])
    x0 = np.array([100.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 4.0])

    # Calcul des racines du systèmes
    sol = sp_op.root(sys, x0)

    return sol.x

"""
##################################################################################################################

PARTIE TEST

##################################################################################################################
"""
# Partie de test :


def imprimer(T, Fd, Fi, constantes):
    # Print de la puissance de cette serre
    res = Bloc_effet_de_serre(T, Fd, Fi, 0.4, 0.02, constantes)
    print("P  =\t", res[0],
          "\nTs =\t", res[1],
          "\nTp =\t", res[2],
          "\nFs =\t", res[3],
          "\nFp =\t", res[4],
          "\nRa =\t", res[5],
          "\nNu =\t", res[6],
          "\nh  =\t", res[7], )
    # print(res)


def test2(constantes):
    T = 65 + 273.15
    Fd = 400
    Fi = 400

    imprimer(T, Fd, Fi, constantes)


def test(constantes):
    # variables d'entrée
    T = float(input("T (Celsuis) = ")) + 273.15
    print("T en Kelvin =", T)
    Fd = float(input("Fd (Watts par mètre carré)= "))
    Fi = float(input("Fi (Watts par mètre carré)= "))

    imprimer(T, Fd, Fi, constantes)


def main(mode):
    print("\n", "#" * 50, "\n", "#" * 50, "\n")

    if mode == "test":
        test2(constantes300)
        print("\n", "_" * 50, "\n")
        test2(constantes310)
        print("\n", "_" * 50, "\n")
        test2(constantes320)
        print("\n", "_" * 50, "\n")
        test2(constantes330)
        print("\n", "_" * 50, "\n")
        test2(constantes340)
    elif mode == "input":
        test(constantes330)
    else:
        print("Erreur")
