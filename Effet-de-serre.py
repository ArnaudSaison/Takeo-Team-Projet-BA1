import numpy as np
import scipy.optimize as sp_op
import scipy.constants as cste

# Constantes
CONST_h = 4
CONST_sigma = cste.sigma

def Bloc_effet_de_serre(T, Fd, Fi, h, sigma):
    """
    Caclule la puissance du capteur solaire en W/m^2.

    :param T: Température que l'on veut atteindre dans la serre
    :param Fd: Flux solaire direct
    :param Fi: Flux solaire indirect
    :param h: Coefficient d'échange de chaleur
    :param sigma: Constante de Stefan Boltzmann pour l'équation de corps noirs
    :return P: Puissance développée par la serre
    """

    # Définition du système d'équations
    def sys(x):
        # Inconnues
        P = x[0]
        Ts = x[1]
        Tp = x[2]
        Fs = x[3]
        Fp = x[4]

        # Vecteur qui va contenir les équations
        E = np.empty((5))

        # Equations
        E[0] = h * (Tp - T) + h * (Ts - T) - P
        E[1] = sigma * Tp ** 4 - Fp
        E[2] = sigma * Ts ** 4 - Fs
        E[3] = P + Fp - Fd - Fi
        E[4] = Fs + h * (Ts - T) - Fd - Fp

        return E

    # Matrice d'initialisation qui va servir de base pour trouver les racines du système
    x0 = np.array([1, 1, 1, 1, 1])

    # Calcul des racines du systèmes
    sol = sp_op.fsolve(sys, x0)

    return sol[0]


# variables d'entrée
T = float(input("T = "))
Fd = float(input("Fd = "))
Fi = float(input("Fi = "))

# Print de la puissance de cette serre
print(Bloc_effet_de_serre(T, Fd, Fi, CONST_h, CONST_sigma), "Watts par mètre carré")