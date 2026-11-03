from grafo import Grafo, insertar_vertice, insertar_arista, arbol_expansion_minimo, camino_mas_corto

def main():
    grafo_sw = Grafo(dirigido=False)

    personajes = [
        "Luke Skywalker", "Darth Vader", "Yoda", "Boba Fett", 
        "C-3PO", "Leia", "Rey", "Kylo Ren", "Chewbacca", 
        "Han Solo", "R2-D2", "BB-8"
    ]
    for p in personajes:
        insertar_vertice(grafo_sw, p)


    insertar_arista(grafo_sw, 9, "C-3PO", "R2-D2")
    insertar_arista(grafo_sw, 7, "C-3PO", "Leia")
    insertar_arista(grafo_sw, 6, "C-3PO", "Luke Skywalker")
    insertar_arista(grafo_sw, 4, "C-3PO", "Yoda")
    insertar_arista(grafo_sw, 7, "Chewbacca", "C-3PO")
    insertar_arista(grafo_sw, 7, "Chewbacca", "R2-D2")
    insertar_arista(grafo_sw, 6, "Chewbacca", "Han Solo")
    insertar_arista(grafo_sw, 5, "Yoda", "Darth Vader")
    insertar_arista(grafo_sw, 5, "Yoda", "Luke Skywalker")
    insertar_arista(grafo_sw, 5, "Leia", "Han Solo")
    insertar_arista(grafo_sw, 6, "Leia", "Luke Skywalker")
    insertar_arista(grafo_sw, 5, "Leia", "Darth Vader")
    insertar_arista(grafo_sw, 3, "Rey", "Kylo Ren")
    insertar_arista(grafo_sw, 3, "Rey", "BB-8")
    insertar_arista(grafo_sw, 3, "Boba Fett", "Darth Vader")

    print("--- ÁRBOLES DE EXPANSIÓN MÍNIMO (C-3PO, Yoda, Leia) ---")
    for p in ["C-3PO", "Yoda", "Leia"]:
        arbol_expansion_minimo(grafo_sw, p)
        print()

    print("--- MÁXIMO DE EPISODIOS COMPARTIDOS ---")
    max_ep = 0
    pares = []
    act_v = grafo_sw.inicio
    while act_v is not None:
        act_a = act_v.adyacentes
        while act_a is not None:
            if act_a.peso > max_ep:
                max_ep = act_a.peso
                pares = [(act_v.info, act_a.destino)]
            elif act_a.peso == max_ep:
                par = tuple(sorted((act_v.info, act_a.destino)))
                if par not in [tuple(sorted(p)) for p in pares]:
                    pares.append((act_v.info, act_a.destino))
            act_a = act_a.sig
        act_v = act_v.sig

    print(f"Máximo de episodios: {max_ep}")
    print(f"Pares con el máximo: {pares}\n")

    print("--- CAMINOS MÁS CORTOS ---")
    camino_mas_corto(grafo_sw, "C-3PO", "R2-D2")
    camino_mas_corto(grafo_sw, "Yoda", "Darth Vader")

    print("\n--- PERSONAJES EN LOS 9 EPISODIOS ---")
    # C-3PO y R2-D2 son los únicos en los 9 episodios
    print("Personajes que aparecen en los 9 episodios: ['C-3PO', 'R2-D2']")


if __name__ == "__main__":
    main()