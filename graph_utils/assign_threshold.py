import math
import random


def static_threshold(g, val):  # Valore diverso per ogni iterazione
    threshold_dict = dict()
    for v in g.Nodes():
        threshold_dict[v.GetId()] = val
    return threshold_dict


def degree_proportional_threshold(g, val):
    threshold_dict = dict()
    alpha = 1/val
    for v in g.Nodes():
        threshold_dict[v.GetId()] = math.ceil(v.GetDeg() * alpha)
    return threshold_dict


def random_threshold(g):
    threshold_dict = dict()
    for v in g.Nodes():
        val = random.uniform(1, v.GetDeg())     # considero valori random che siano inferiori al threshold del nodo
        threshold_dict[v.GetId()] = val
    return threshold_dict
