import numpy as np
import scipy.optimize as sp_op
import scipy.constants as cste

#    Constantes :sigma,      v,        alpha,    Pr,    g,       L,   k,       h
constantes300 = [cste.sigma, 1.578e-5, 2.213e-5, 0.713, 9.80665, 0.2, 0.02623, 4]
constantes310 = [cste.sigma, 1.659e-5, 2.340e-5, 0.709, 9.80665, 0.2, 0.02684, 4]
constantes320 = [cste.sigma, 1.754e-5, 2.476e-5, 0.708, 9.80665, 0.2, 0.02753, 4]
constantes330 = [cste.sigma, 1.851e-5, 2.616e-5, 0.708, 9.80665, 0.2, 0.02821, 4]
constantes340 = [cste.sigma, 1.951e-5, 2.821e-5, 0.707, 9.80665, 0.2, 0.02888, 4]


def Calcul_h(T, c):
    v = c[1]
    alpha = c[2]
    Pr = c[3]
    g = c[4]
    L = c[5]
    k = c[6]
    beta = 1 / T

    DT = 35

    def sys(x):
        Ra = x[0]
        Nu = x[1]
        h = x[2]

        E = np.empty(3)

        E[0] = (h * L / k) - Nu
        E[1] = (g * beta * DT * L ** 3 / (alpha * v)) - Ra
        # E[2] = 0.58 * Ra ** (1 / 5) - Nu
        E[2] = (0.14 * Ra ** (1 / 3) * ((1 + 0.0107 * Pr) / (1 + 0.01 * Pr))) - Nu

        return E

    x0 = np.array([1, 1, 1])

    sol = sp_op.root(sys, x0)

    return sol.x


def test(constantes):
    # variables d'entrée
    # T = float(input("T (Celsuis)= ")) + 273.15
    T = 40 + 273.15

    # Print de la puissance de cette serre
    res = Calcul_h(T, constantes)
    print(res)


test(constantes340)