#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator
import click

@click.command()
@click.option("--outer", "--de", prompt=True, type=click.FloatRange(0, min_open=True), help="D_e (Outer Diamter, in mm)")
@click.option("--inner", "--di", prompt=True, type=click.FloatRange(0, min_open=True), help="D_i (Inner Diameter, in mm)")
@click.option("--thickness", "-t", prompt=True, type=click.FloatRange(0, min_open=True), help="t (Thickness, in mm)")
@click.option("--height", "-h", prompt=True, type=click.FloatRange(0, min_open=True), help="l_0 (Undeformed Height, in mm)")
@click.option("-s", type=click.FloatRange(0, min_open=True), help="Optionaler Federweg für den die Berechnung durchgeführt werden soll (in mm)")
@click.option("-E", type=click.FloatRange(0, min_open=True), default=206000.0, help="Elastizitätsmodul")
@click.option("--nu", type=click.FloatRange(0, 0.5, max_open=True), default=0.3, help="Poissonzahl")
def cli(outer, inner, thickness, height, s, e, nu):
    """
    Errechnet die Federkraft einer Tellerfeder der Gruppe 1 nach DIN 2093

    Formeln aus Haberhauer & Bodenstein, Maschinenelemente, 17. Auflage.
    Eingabe sind D_e, D_i, l_0, t (laut DIN 2093)
    Achtung: Manchmal sind die Namen dazu auch D_e = d_2, D_i = d_1, l_0 = h, t = s
    """

    # Außendurchmesser
    D_e = outer  # mm
    # Innendurchmesser
    D_i = inner  # mm
    # Dicke der Scheibe
    t = thickness # mm
    # Bauhöhe der unbelasteten Scheibe
    l_0 = height  # mm

    E = e

    if D_i >= D_e:
        raise ValueError("Invalid Input: D_i >= D_e")
    if t >= l_0:
        raise ValueError("Invalid Input: t >= l_0")


    # Berechnung der Werte
    ######################

    # Verhältnis der Durchmesser
    delta = D_e / D_i

    # Rechnerischer Federnweg bis zur Planlage
    h_0 = l_0 - t

    # Beiwerte
    K_1 = (1 / np.pi) * (((delta - 1) / delta) ** 2) / (((delta + 1)/(delta - 1)) - (2 / np.log(delta)))
    K_2 = (6 / np.pi) * (((delta - 1)/np.log(delta)) - 1) / np.log(delta)
    K_3 = (3 / np.pi) * (delta - 1) / np.log(delta)

    # Für Gruppe 1 ist K_4 = 1, ansonsten anders!
    K_4 = 1

    def F(u):
        # Federnkraft für parametrischen Federnweg u [0, 1]
        s = u * h_0
        return ((4 * E)/(1 - nu**2)) * (t**4 / (K_1 * D_e**2)) * K_4**2 * (s/t) * (K_4**2 * ((h_0/t) - (s/t)) * ((h_0 / t)-(s / (2*t))) + 1 )

    def R(u):
        # Federnrate
        s = u * h_0
        return ((4 * E)/(1 - nu**2)) * (t**3 / (K_1 * D_e**2)) * K_4**2 * (K_4**2 * ((h_0 / t)**2 - 3 * (h_0 / t) * (s/t) + ((3/2) * (s/t)**2) ) + 1 )

    def W(u):
        # Federnarbeit
        s = u * h_0
        return ((2*E)/(1 - nu**2)) * (t**5)/(K_1 * D_e**2) * K_4**2 * (s/t)**2 * (K_4**2 * ((h_0 / t) - (s/(s*t)))**2 + 1 )

    print(f"Material: {E=:.1f} MPa, {nu=:.1f}")

    print("Daten der Feder:")
    # 0.75 ist die obere Grenze lt. DIN 2093
    s_max = 0.75 * h_0
    # Reihencharacterisierung:
    # Reihe A: h_0 / t = 0.4
    # Reihe B: h_0 / t = 0.75
    # Reihe C: h_0 / t = 1.3
    print(f"{D_e = :.1f} mm, {D_i = :.1f} mm, {t = :.2f} mm, {l_0 = :.2f} mm, {h_0 = :.2f} mm")
    reihe = h_0 / t
    if np.isclose(reihe, 0.4):
        print(f"  Reihe A ({h_0 / t = :.2f})")
    elif np.isclose(reihe, 0.75):
        print(f"  Reihe B ({h_0 / t = :.2f})")
    elif np.isclose(reihe, 1.3):
        print(f"  Reihe C ({h_0 / t = :.2f})")
    else:
        print(f"  WARNUNG: Feder entspricht keiner Reihe der Norm DIN 2093! {h_0 / t = :.2f}")
    print(f"Höhe der Feder undeformiert: {l_0=}")
    print(f"Höhe der Feder deformiert: l_0 - s_max = {l_0:.2f} - {s_max:.2f} = {l_0 - s_max:.2f}")
    print()
    print(f"Federkraft bei s_max             F =  {F(0.75):>7.1f} N")
    print(f"Federrate dF/ds bei s_max        R =  {R(0.75):>7.1f} N/mm")
    print(f"Federarbeit int 0...s_max F ds   W =  {W(0.75):>7.1f} mJ")

    if s is not None:
        do_calc = True
        if s > h_0:
            print(f"FEHLER: Der angegebene Federweg ist nicht möglich! {h_0 = } aber {s = }")
            do_calc = False
        elif s > s_max:
            print(f"WARNUNG: Der angegebene Federweg ist über dem Maximum nach DIN 2093! {s_max = } aber {s = }")
        if do_calc:
            u = s / h_0
            print()
            print(f"{s = :.1f} entspricht {100 * u:.1f}% Federweg")
            print(f"Höhe der Feder deformiert: l_0 - s = {l_0:.2f} - {s:.2f} = {l_0 - s:.2f}")
            print(f"Federkraft bei {s=:.1f}            F =  {F(u):>7.1f} N")
            print(f"Federrate dF/ds bei {s=:.1f}       R =  {R(u):>7.1f} N/mm")
            print(f"Federarbeit int 0...{s:.1f} F ds    W =  {W(u):>7.1f} mJ")

    # Abbildung 2.129 aus Haberhauer & Bodenstein, Maschinenelemente 17. Auflage
    # Der Federnweg wird angenommen 0.75 * h_0 (Siehe DIN 2093)
    # Faktor für das Verhältnis s / h_0 (Parametrische Variable für den Federnweg)
    faktor = np.linspace(0, 1, 100)
    f = F(faktor)
    plt.plot(faktor, f / f[-1], label=f'$h_0 / t = {h_0 / t:.2f}$')
    plt.scatter([0.75], [F(0.75) / f[-1]], label=f'$F(s_{{max}})= {F(0.75):.1f}N$')
    plt.suptitle('Federkennlinie nach DIN 2092')
    plt.title(f'$D_e = {D_e:.1f}, D_i = {D_i:.1f}, t = {t:.2f}, l_0 = {l_0:.2f}$')
    plt.axvline(x=0.75, linestyle='--', color='red')
    plt.fill([0.75, 1.0, 1.0, 0.75], [0, 0, 1.4, 1.4], color='red', alpha=0.2)
    plt.xlabel("$s / h_0$")
    plt.ylabel("$F / F_c$")
    plt.xticks([0, 0.25, 0.5, 0.75, 1])
    plt.yticks(np.arange(0, 1.41, 0.1))
    plt.grid()
    plt.grid(which='minor')
    plt.gca().minorticks_on()
    plt.gca().xaxis.set_minor_locator(FixedLocator(np.arange(0, 1.01, 0.05)))
    plt.gca().yaxis.set_minor_locator(FixedLocator(np.arange(0, 1.41, 0.05)))
    plt.xlim(0, 1)
    plt.ylim(0, 1.4)
    plt.gca().set_aspect('equal', 'box')
    plt.legend()
    plt.axline((0,0), (1,1), linestyle=':', color='k')
    plt.show()

if __name__ == "__main__":
    cli()
