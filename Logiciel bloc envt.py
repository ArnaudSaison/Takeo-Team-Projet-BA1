"""
CODE DU BLOC ENVIRONNEMENT

  Légende : grandeur décrite - symbole utilisé dans le code - [unités]

* Les inputs :
   - énergie solaire reçue    - Esol - [MJ/m²]
   - température ambiante     - Tamb - [K]
   - temps d'exposition       - Texp - [h]
   - humidité relative        - HR   - [adimensionnel] (exprimé en pourcents)

* Les outputs :
   - flux solaire direct      -  Fd  - [W/m²]
   - flux solaire indirect    -  Fi  - [W/m²]
   - humidité absolue         -  Y   - [adimensionnel]

"""

import math

# 1) on définit d'abord les constantes que l'on va utiliser :

T0     = 333.15          # température dont on connait la pression de saturation (60°C) [K]
R      = 8.314           # constante des gaz parfaits [J/K]
PATM   = 101325          # pression atmosphérique [Pa]
LAMBDA = 42440           # chaleur latente molaire de vaporisation de l'eau [J/mol]
SIGMA  = 5.6704*10**(-8) # constante de Stefan-Boltzmann [W/m²K⁴]



# 2) on définit ensuite les fonctions que l'on va utiliser


   # pression de saturation Psat en fonction de la température T :

def FPsat(T) :
    if T == T0 :
        return 2*10**4
    deltaT = 1/T - 1/T0              #[1/K]
    exp = -LAMBDA * deltaT / R       #[adim]
    return FPsat(T0)*math.exp(exp)   #[Pa]

   # on attribue des valeurs par défaut pour les grandeurs dans le cas où elles ne sont pas données (Tamb de 30°C, Esol de 19.6 MJ/m², HR de 70%)

def environnement(Tamb=303.15, Esol=19.6, Texp=12, HR=70):
    HR = HR/100                        #passage pourcents -> décimales
    # humidité absolue :
    Psat = FPsat(Tamb)
    Y = 0.62*HR*Psat / (PATM-Psat)   #0.62 = Meau/Mair
    # flux direct :
    Fd=10**4*Esol / (36*Texp)        #10**4 et 36 viennent de la conversion MJ -> J et h -> s
    # flux indirect :
    Tr=LAMBDA*Tamb / (LAMBDA - R*Tamb*math.log(HR))             #Tr est la température de rosée [K] et le log est un ln dans ce module
    Tciel=Tamb*(0.711 + 0.0056*Tr + 7.3*10**(-5)*Tr**2)**0.25   #on néglige le cosinus car il est proche de 0
    Fi=SIGMA*Tciel**4

    return Y, Fd, Fi


# 3) on peut enfin tester notre fonction :

print("Inputs : ")
Tamb = float(input("Température ambiante [K]       : "))
Esol = float(input("Energie solaire [MJ/m²]        : "))
Texp = float(input("Temps d'exposition [h]         : "))
HR   = float(input("Humidité relative en pourcents : "))
(Y,Fd,Fi)= environnement(Tamb, Esol, Texp, HR)
print()
print("Outputs : ")
print("Humidité absolue : " + str(Y) + " kg d'eau par kg d'air sec")
print("Flux direct      : " + str(Fd) + " W/m²")
print("Flux indirect    : " + str(Fi) + " W/m²")










