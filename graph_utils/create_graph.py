from snap import snap
import numpy as np


def create(dataset, num_of_nodes, random_edges):
    g = snap.TUNGraph.New()  # Crea un grafo non direzionato

    for i in range(0, num_of_nodes+1):  # Aggiunge i nodi
        g.AddNode(i)

    if random_edges is False:   # No decisione differita
        for i, j in zip(dataset.row, dataset.col):  # Aggiunge direttamente gli archi
            g.AddEdge(int(i), int(j))

    return g


def create_probability_edges(dataset, distribution):
    # Genera le probabilità di attivazione per ciascun arco
    probability_dict = dict()
    for i, j in zip(dataset.row, dataset.col):
        key = "(%d %d)" % (i, j)  # La chiave del dizionario sono le 2 estremità dell'arco

        # Scelta della distribuzione di probabilità da usare per l'attivazione degli archi
        if distribution is True:
            probability_dict[key] = np.random.uniform()  # low=0.0, high=1.0
        else:
            probability_dict[key] = np.random.normal()  # loc=0.0, scale=1.0, size=None

    return probability_dict


def remove_unused_nodes(g):
    # Cancella dal grafo i nodi inutilizzabili, privi di archi che li attivino
    toDelete = []
    for node in g.Nodes():
        if node.GetOutDeg() == 0:
            toDelete.append(node.GetId())
    snap.DelNodes(g, toDelete)


def deferred_decision(dataset, probability_dict, g, distribution):
    # Deferred decision: aggiunge gli archi in base alla probabilità generata
    for i, j in zip(dataset.row, dataset.col):
        key = "(%d %d)" % (i, j)
        if distribution is True:
            val = np.random.uniform()
        else:
            val = np.random.normal()

        if val > probability_dict[key]:     # se il valore generato supera la soglia stabilita in precedenza, aggiungo l'arco al grafo
            g.AddEdge(int(i), int(j))
    remove_unused_nodes(g)
