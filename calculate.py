#!/usr/bin/env python3
from math import pi, log

# Errechnet die Federnkraft einer Tellerfeder der Gruppe 1 nach DIN 2093
#
# Formeln aus http://www.christianbauer.com/de/img-cust/Katalog_D_2TheoriePraxis.pdf
#
# Eingabe sind D_e, D_i, l_0, t (laut DIN 2093)

# Außendurchmesser
D_e = 10.0
# Innendurchmesser
D_i = 5.2
# Dicke der Scheibe
t = 0.5
# Bauhöhe der unbelasteten Scheibe
l_0 = 0.75

# Reihencharacterisierung:
# Reihe 1: h_0 / t = 0.4
# Reihe 2: h_0 / t = 0.75
# Reihe 3: h_0 / t = 1.3

# Materialkennwerte
# Laut DIN 2093
# Elastizitätsmodul
E = 206000.0 # MPa
# Poissionzahl
nu = 0.3


# Berechnung der werte

# Verhältnis der Durchmesser
delta = D_e / D_i

# Rechnerrischer Federnweg bis zur Planlage
h_0 = l_0 - t

# Der Federnweg wird angenommen 0.75 * h_0 (Siehe DIN 2093)
s = 0.75 * h_0

# Beiwerte
K_1 = (1 / pi) * (((delta - 1) / delta) ** 2) / (((delta + 1)/(delta - 1)) - (2 / log(delta)))
K_2 = (6 / pi) * (((delta - 1)/log(delta)) - 1) / log(delta)
K_3 = (3 / pi) * (delta - 1) / log(delta)

# Für Gruppe 1 ist K_4 = 1, ansonsten anders!
K_4 = 1

# Federnkraft für 0.75 * h_0 = s
F = ((4 * E)/(1 - nu**2)) * (t**4 / (K_1 * D_e**2)) * K_4**2 * (s/t) * (K_4**2 * ((h_0/t) - (s/t)) * ((h_0 / t)-(s / (2*t))) + 1 )

# Federnrate
R = ((4 * E)/(1 - nu**2)) * (t**3 / (K_1 * D_e**2)) * K_4**2 * (K_4**2 * ((h_0 / t)**2 - 3 * (h_0 / t) * (s/t) + ((3/2) * (s/t)**2) ) + 1 )

# Federnarbeit
W = ((2*E)/(1 - nu**2)) * (t**5)/(K_1 * D_e**2) * K_4**2 * (s/t)**2 * (K_4**2 * ((h_0 / t) - (s/(s*t)))**2 + 1 )

print("Daten der Feder:")
print("D_e: %f, D_i: %f, t: %f, l_0: %f, h_0: %f, s: %f" % (D_e, D_i, t, l_0, h_0, s))
print()
print("Federnkraft F:", F, "N")
print("Federnrate dF/ds = R:", R, "N/mm")
print("Federnarbeit int 0...s F ds = W:", W, "mJ")
