"""
Takeo

CODE DU BLOC VENTILATION

     grandeur                                    symbole            [unités]
Les inputs :
   - Masse de l'aliment que l'on veut sécher     Masse_aliment      [kg]
   - Masse d'eau par matière sèche initiale      Masse_epmsi        [kg d'eau par kg de matière sèche]
   - Masse d'eau par matière sèche finale        Masse_epmsf        [kg d'eau par kg de matière sèche]
   -                                             Yamb               []
   -                                             Ymax               []
   - Temps de séchage souhaité                   Dt                 [heures]

Les outputs :
   - débit d'air sec                             Q                  [kg d'air sec/s]
"""


def Bloc_ventilation(Masse_aliment, Masse_epmsi, Masse_epmsf, Yamb, Ymax, Dt=16):
    """
    Ce programme nous permet de trouver le débit d'air nécessaire à notre séchoir
    Ce débit d'air est très important, car il va réguler l'humidité de la machine.
    """
    # Données
    Masse_init_eau = Masse_epmsi / (Masse_epmsi + 1) * Masse_aliment
    Masse_fin_eau = Masse_epmsf / (Masse_epmsi + 1) * Masse_aliment

    D_masse = Masse_init_eau - Masse_fin_eau
    Dt = Dt * 3600  # Conversion du temps en secondes

    # Equations permettant de calculer par la suite le débit d'air sec
    J = D_masse / Dt
    Dy = Yamb - Ymax

    # Calcul du débit d'air
    Q_max = J / Dy

    return Q_max, J
