import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Définir les variables floues (entrées et sortie)
vitesse = ctrl.Antecedent(np.arange(0, 101, 1), 'vitesse')  # vitesse en km/h (de 0 à 100)
distance = ctrl.Antecedent(np.arange(0, 6001, 1), 'distance')  # distance en m (de 0 à 5000)
freinage = ctrl.Consequent(np.arange(0, 101, 1), 'freinage')  # force de freinage en %

# Définir les subdivisions floues manuellement
vitesse['stopped'] = fuzz.trimf(vitesse.universe, [0, 0, 0])
vitesse['very_slow'] = fuzz.trimf(vitesse.universe, [0, 1.5, 3])
vitesse['slow'] = fuzz.trimf(vitesse.universe, [2, 8.5, 15])
vitesse['medium'] = fuzz.trimf(vitesse.universe, [10, 22.5, 35])
vitesse['medium_fast'] = fuzz.trimf(vitesse.universe, [30, 37.5, 45])
vitesse['fast'] = fuzz.trimf(vitesse.universe, [40, 55, 70])
vitesse['very_fast'] = fuzz.trimf(vitesse.universe, [65, 82.5, 100])

distance['at'] = fuzz.trimf(distance.universe, [0, 0.5, 1])
distance['very_near'] = fuzz.trimf(distance.universe, [0.5, 5.25, 10])
distance['near'] = fuzz.trimf(distance.universe, [5, 102.5,200])
distance['medium'] = fuzz.trimf(distance.universe, [100, 800, 1500])
distance['medium_far'] = fuzz.trimf(distance.universe, [1000, 2250, 3500])
distance['far'] = fuzz.trimf(distance.universe, [3000,4000, 5000])
distance['very_far'] = fuzz.trimf(distance.universe, [4000, 5000, 6000])

freinage['no'] = fuzz.trimf(freinage.universe, [0, 0, 0])
freinage['very_slight'] = fuzz.trimf(freinage.universe, [0, 3.5, 7])
freinage['slight'] = fuzz.trimf(freinage.universe, [5, 17.5, 30])
freinage['almost_medium'] = fuzz.trimf(freinage.universe, [25, 37.5, 50])
freinage['medium'] = fuzz.trimf(freinage.universe, [45, 65, 85])
freinage['almost_full'] = fuzz.trimf(freinage.universe, [80, 90, 100])
freinage['full'] = fuzz.trimf(freinage.universe, [90, 95, 100])

# Créer un système de contrôle flou
freinage_ctrl = ctrl.ControlSystem()

# Ajouter des règles
rules = [
    ctrl.Rule(vitesse['stopped'] & distance['at'], freinage['no']),
    ctrl.Rule(vitesse['stopped'] & distance['very_far'], freinage['very_slight']),
    ctrl.Rule(vitesse['very_slow'] & distance['very_near'], freinage['no']),
    ctrl.Rule(vitesse['very_slow'] & distance['very_far'], freinage['slight']),
    ctrl.Rule(vitesse['slow'] & distance['near'], freinage['slight']),
    ctrl.Rule(vitesse['slow'] & distance['medium'], freinage['medium']),
    ctrl.Rule(vitesse['slow'] & distance['very_far'], freinage['almost_medium']),
    ctrl.Rule(vitesse['medium'] & distance['near'], freinage['slight']),
    ctrl.Rule(vitesse['medium'] & distance['very_far'], freinage['medium']),
    ctrl.Rule(vitesse['medium'] & distance['medium'], freinage['almost_medium']),
    ctrl.Rule(vitesse['medium_fast'] & distance['medium_far'], freinage['medium']),
    ctrl.Rule(vitesse['medium_fast'] & distance['very_far'], freinage['full']),
    ctrl.Rule(vitesse['medium_fast'] & distance['far'], freinage['full']),
    ctrl.Rule(vitesse['fast'] & distance['far'], freinage['full']),
    ctrl.Rule(vitesse['fast'] & distance['medium_far'], freinage['almost_full']),
    ctrl.Rule(vitesse['fast'] & distance['very_far'], freinage['full']),
    ctrl.Rule(vitesse['very_fast'] & distance['very_far'], freinage['full']),
]

# Ajouter les règles au système
freinage_ctrl = ctrl.ControlSystem(rules)
freinage_simulation = ctrl.ControlSystemSimulation(freinage_ctrl)

# Fonction pour simuler et afficher la force de freinage
def simulate_braking(v, d):
    freinage_simulation.input['vitesse'] = v
    freinage_simulation.input['distance'] = d
    freinage_simulation.compute()
    
    # Affichage de la sortie avant de la retourner
    print(f"Entrées: vitesse={v}, distance={d}, Sortie calculée: freinage={freinage_simulation.output}")

    # Vérifier si la sortie existe
    if 'freinage' in freinage_simulation.output:
        return freinage_simulation.output['freinage']
    else:
        return None  # ou 0 si vous préférez



# Cas à analyser
cas = [
    (45, 2500),
    (0.9, 2500),
    (3, 150),
    (12.5, 150)
]

# Afficher les résultats
# Afficher les résultats
for v, d in cas:
    force_freinage = simulate_braking(v, d)
    if force_freinage is not None:
        print(f"Pour une vitesse de {v} km/h et une distance de {d} m, la force de freinage est : {force_freinage:.2f}%")
    else:
        print(f"Pour une vitesse de {v} km/h et une distance de {d} m, aucune force de freinage définie(case vide sans regle).")






