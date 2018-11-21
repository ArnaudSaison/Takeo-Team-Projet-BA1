import Effet_de_serre as eds
import Environnement as env

def main():
    # INPUTS

    print("Partie Effet de serre :")

    Tfluide = float(input("T que l'on veut atteindre [C°] = ")) + 273.15
    print("T en Kelvin =", Tfluide)
    a = float(input("Longueur de la section de la boîte [m] = "))
    b = float(input("Hauteur de la section de la boîte [m] = "))

    print("\n", "#" * 50, "\n", sep="")
    print("Partie Environnement :")

    Tamb = float(input("Température ambiante [C°] = ")) + 273.15
    Esol = float(input("Energie solaire [MJ/m²] = "))
    Texp = float(input("Temps d'exposition [h] = "))
    HR = float(input("Humidité relative en pourcents = "))

    # OUPUTS
    Y, Fd, Fi = env.Bloc_environnement(Tamb, Esol, Texp, HR)
    P = eds.Bloc_effet_de_serre(Tfluide, Fd, Fi, a, b)

    # PRINT
    print("\n", "#" * 50, "\n", sep="")
    print(  "\nFd =\t", Fd,
            "\nFi =\t", Fi,
            "\nP  =\t", P[0],
            "\nTs =\t", P[1],
            "\nTp =\t", P[2],
            "\nFs =\t", P[3],
            "\nFp =\t", P[4],
            "\nRa =\t", P[5],
            "\nNu =\t", P[6],
            "\nh  =\t", P[7])


main()