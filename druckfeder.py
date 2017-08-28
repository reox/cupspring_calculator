#!/usr/bin/env python3
import argparse

parser = argparse.ArgumentParser(description='Druckfedern')
parser.add_argument('-d', type=float, help='Drahtdurchmesser')
parser.add_argument('-D', type=float, help='Áussendurchmesser')
parser.add_argument('-n', type=float, help='Windungen')
parser.add_argument('-L', type=float, help='enstpannte Länge')

args = parser.parse_args()

# Assume cold worked
n_t = args.n + 2

# Minimal Length: S_a + L_c = L_n

L_c = n_t * args.d
S_a = (0.0015 * (args.D ** 2 / args.d) + 0.1 * args.d) * args.n

print("minimale Länge: {}".format(L_c + S_a))
