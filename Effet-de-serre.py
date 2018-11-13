import numpy as np
import scipy.optimize as sp_op
import scipy.constants as cste

#    Constantes :sigma,      v,        alpha,    Pr,    g,       L,   k,       h
constantes300 = [cste.sigma, 1.578e-5, 2.213e-5, 0.713, 9.80665, 0.2, 0.02623, 4]
constantes310 = [cste.sigma, 1.659e-5, 2.340e-5, 0.709, 9.80665, 0.2, 0.02684, 4]
constantes320 = [cste.sigma, 1.754e-5, 2.476e-5, 0.708, 9.80665, 0.2, 0.02753, 4]
constantes330 = [cste.sigma, 1.851e-5, 2.616e-5, 0.708, 9.80665, 0.2, 0.02821, 4]
constantes340 = [cste.sigma, 1.951e-5, 2.821e-5, 0.707, 9.80665, 0.2, 0.02888, 4]


def Bloc_effet_de_serre(T, Fd, Fi, c):
    """
    Caclule la puissance du capteur solaire en W/m^2.

    :param T: Température que l'on veut atteindre dans la serre
    :param Fd: Flux solaire direct
    :param Fi: Flux solaire indirect
    :return P: Puissance développée par la serre
    """
    # Constantes convection
    sigma = c[0]
    v = c[1]
    alpha = c[2]
    Pr = c[3]
    g = c[4]
    L = c[5]
    k = c[6]
    beta = 1 / T

    # h = c[7]

    # Définition du système d'équations
    def sys(x):
        # Inconnues
        P = x[0]
        Ts = x[1]
        Tp = x[2]
        Fs = x[3]
        Fp = x[4]

        # Inconnues convection
        Ra = x[5]
        Nu = x[6]
        h = x[7]

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
        E[6] = (g * beta * (((Ts + Tp) / 2) - T) * L ** 3 / (alpha * v)) - Ra
        # E[7] = 0.58 * Ra ** (1 / 5) - Nu
        E[7] = (0.14 * Ra ** (1 / 3) * ((1 + 0.0107 * Pr) / (1 + 0.01 * Pr))) - Nu

        return E

    # Matrice d'initialisation qui va servir de base pour trouver les racines du système
    x0 = np.array([100, 100, 100, 500, 300, 1, 1, 5])

    # Calcul des racines du systèmes
    sol = sp_op.root(sys, x0)

    return sol.x


def imprimer(T, Fd, Fi, constantes):
    # Print de la puissance de cette serre
    res = Bloc_effet_de_serre(T, Fd, Fi, constantes)
    print("P  =\t", res[0], "\nTs =\t", res[1], "\nTp =\t", res[2], "\nFs =\t", res[3], "\nFp =\t", res[4], "\nRa =\t",
          res[5], "\nNu =\t", res[6], "\nh  =\t", res[7], )


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
        print("\n", "_"*50, "\n")
        test2(constantes310)
        print("\n", "_"*50, "\n")
        test2(constantes320)
        print("\n", "_"*50, "\n")
        test2(constantes330)
        print("\n", "_"*50, "\n")
        test2(constantes340)
    elif mode == "input":
        test(constantes)
    else:
        print("Erreur")

main(input())
