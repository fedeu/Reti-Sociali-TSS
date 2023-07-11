from scipy.io import mmread
from target_set_selection import tss
from graph_utils.assign_threshold import *
from graph_utils.create_graph import *


def read_dataset():
    # Prima di leggere il file originale, se in .mtx c'è un solo % occorre aggiungerne un altro all'inizio del file affinché il formato venga riconosciuto correttamente
    return mmread("dataset/socfb-MIT.mtx")


def deterministic_alg_static_threshold():
    print("\nDETERMINISTIC STATIC based Threshold")

    for threshold in range(1, 11):  # Calcola TSS per soglia statica da 1 a 10
        graph = create(matrix_dataset, NUM_OF_NODES, False)  # Crea il grafo senza probabilità di attivazione
        thresholds = static_threshold(graph, threshold)  # dizionario in cui static threshold = i

        S = tss(graph, thresholds)

        print("Static Threshold %d - Seed set size = %d" % (threshold, len(S)))


def deterministic_alg_degree_threshold():
    print("\nDETERMINISTIC DEGREE based Threshold")

    for threshold in range(2, 12):
        graph = create(matrix_dataset, NUM_OF_NODES, False)  # Crea il grafo senza probabilità di attivazione
        thresholds = degree_proportional_threshold(graph, threshold)  # dizionario in cui la soglia = 1/i * deg(u)

        S = tss(graph, thresholds)

        print("Degree based Threshold %f - Seed set size %d" % (1 / threshold, len(S)))


def deterministic_alg_random_threshold():
    print("\nDETERMINISTIC PSEUDORANDOM based Threshold")

    for i in range(10):
        graph = create(matrix_dataset, NUM_OF_NODES, False)  # Crea il grafo senza probabilità di attivazione

        thresholds = random_threshold(
            graph)  # dizionario in cui la soglia è un valore pseudorandom < del grado del nodo

        S = tss(graph, thresholds)
        print("Pseudorandom Threshold - Seed set size %d" % len(S))


def probabilistic_alg_static_threshold():
    print("\nPROBABILISTIC STATIC based Threshold")
    edges_activation_dict = create_probability_edges(matrix_dataset,
                                                     type_of_probability)  # True = distribuzione uniforme, False = distribuzione normale

    # Crea dizionario per contenere i risultati ottenuti, in cui la key è il threshold i e il valore è la media tra i 10 esperimenti svolti
    results = dict()
    for key in range(1, 11):
        results[key] = 0

    for i in range(1, 11):
        for threshold in range(1, 11):
            graph = create(matrix_dataset, NUM_OF_NODES, True)  # Crea il grafo inserendo solo i nodi
            deferred_decision(matrix_dataset, edges_activation_dict, graph,
                              type_of_probability)  # Aggiunge gli archi e restituisce il grafo residuo

            thresholds = static_threshold(graph, threshold)

            S = tss(graph, thresholds)

            results[threshold] = results[threshold] + len(S)
            print("Iterazione %d - Static Threshold %d - Seed set size = %d" % (i, threshold, len(S)))

    for threshold in results.keys():
        print("Soglia ", threshold, " Media: ",
              results[threshold] / 10)  # Stampo la media dei risultati inerenti al threshold i-esimo


def probabilistic_alg_degree_threshold():
    print("\nPROBABILISTIC DEGREE based Threshold")
    edges_activation_dict = create_probability_edges(matrix_dataset, type_of_probability)

    # Crea dizionario per contenere i risultati ottenuti, in cui la key è (1/i) e il valore è la media tra i 10 esperimenti svolti
    results = dict()
    for key in [1 / x for x in range(2, 12)]:
        results[key] = 0

    for i in range(10):
        for threshold in range(2, 12):
            graph = create(matrix_dataset, NUM_OF_NODES, True)  # Crea il grafo inserendo solo i nodi
            deferred_decision(matrix_dataset, edges_activation_dict, graph,
                              type_of_probability)  # Aggiunge gli archi e restituisce il grafo residuo

            thresholds = degree_proportional_threshold(graph, threshold)

            S = tss(graph, thresholds)
            results[1 / threshold] = results[1 / threshold] + len(S)

            print("Iterazione %d di %d - Degree proportional Threshold %f - Seed set size = %d " % (
            threshold, i, 1 / threshold, len(S)))

    for threshold in results.keys():
        print("Soglia ", threshold, " Media: ",
              results[threshold] / 10)  # Stampo la media dei risultati inerenti al threshold i-esimo


def probabilistic_alg_random_threshold():
    print("\nPROBABILISTIC PSEUDORANDOM based Threshold")
    edges_activation_dict = create_probability_edges(matrix_dataset, type_of_probability)

    for i in range(10):
        res = 0
        for x in range(10):
            graph = create(matrix_dataset, NUM_OF_NODES, True)  # Crea il grafo inserendo solo i nodi
            deferred_decision(matrix_dataset, edges_activation_dict, graph,
                              type_of_probability)  # Aggiunge gli archi e restituisce il grafo residuo

            thresholds = random_threshold(graph)
            S = tss(graph, thresholds)

            res = res + len(S)
            print("Iterazione %d - Random Threshold - Seed set size = %d " % (i, len(S)))

        print("Iterazione ", i, ", dopo 10 esecuzioni tss la taglia media di S è: ", res / 10)


if __name__ == "__main__":
    NUM_OF_NODES = 6401  # (dimensione del dataset di partenza) - 1
    matrix_dataset = read_dataset()

    type_of_probability = False  # Distribuzione di probabilità a scelta tra Normale (False) e Uniforme (True)

    deterministic_alg_static_threshold()
    deterministic_alg_degree_threshold()
    deterministic_alg_random_threshold()

    probabilistic_alg_static_threshold()
    probabilistic_alg_degree_threshold()
    probabilistic_alg_random_threshold()
