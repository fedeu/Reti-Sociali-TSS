def update_and_delete(v, t, g, case_3):
    edges_to_delete = set()

    for u in v.GetOutEdges():  # Tengo traccia degli archi incidenti sul nodo da cancellare
        if case_3 is False:     # Se non sono nel caso 3 bisogna anche decrementare la soglia del nodo u
            if t[u] >= 1:
                t[u] = t[u] - 1  # Si decrementa il threshold dei vicini
        edges_to_delete.add(u)

    for edge in edges_to_delete:  # Rimuovo gli archi dal grafo
        g.DelEdge(v.GetId(), edge)

    g.DelNode(v.GetId())  # Rimuovo il nodo dal grafo
    edges_to_delete.clear()


def tss(graph, t):
    S = set()
    while graph.GetNodes() != 0:  # Finché il grafo non è vuoto
        case3 = True
        for v in graph.Nodes():  # Scorri i vertici

            # CASO 1: nodo ha soglia = 0
            if t[v.GetId()] == 0:  # controllo per il grado = 0 del nodo
                case3 = False
                update_and_delete(v, t, graph, case3)

            # CASO 2: il grado del nodo è inferiore alla sua soglia: il nodo non ha vicini a sufficienza per essere influenzato
            elif v.GetOutDeg() < t[v.GetId()]:
                S.add(v.GetId())  # Aggiungo v al seed set
                case3 = False
                update_and_delete(v, t, graph, case3)

        # CASO 3: situazione standard
        if case3 is True:
            max_ratio = -1
            node_id = -1
            for u in graph.Nodes():  # Selezione del nodo che massimizza la quantità specificata
                ratio = t[u.GetId()] / (u.GetOutDeg() * (u.GetOutDeg() + 1))  # Euristica per porre un bound al seed set
                if ratio >= max_ratio:  # A parità di ratio si elimina il nodo con l'id maggiore
                    max_ratio = ratio
                    node_id = u.GetId()

            # Elimino il nodo che massimizza la quantità
            update_and_delete(graph.GetNI(node_id), t, graph, True)

    return S
