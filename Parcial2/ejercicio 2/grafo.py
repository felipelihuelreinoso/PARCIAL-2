class nodoVertice:
    def __init__(self, info):
        self.info = info
        self.sig = None
        self.visitado = False
        self.adyacentes = None

class nodoArista:
    def __init__(self, destino, peso):
        self.destino = destino
        self.peso = peso
        self.sig = None

class Grafo:
    def __init__(self, dirigido=False):
        self.inicio = None
        self.dirigido = dirigido
        self.tamanio = 0


def insertar_vertice(grafo, dato):
    nuevo = nodoVertice(dato)
    if grafo.inicio is None:
        grafo.inicio = nuevo
    else:
        actual = grafo.inicio
        while actual.sig is not None:
            actual = actual.sig
        actual.sig = nuevo
    grafo.tamanio += 1


def agregar_arista(vertice_origen, dato, destino):
    nuevo = nodoArista(destino, dato)
    if vertice_origen.adyacentes is None:
        vertice_origen.adyacentes = nuevo
    else:
        actual = vertice_origen.adyacentes
        while actual.sig is not None:
            actual = actual.sig
        actual.sig = nuevo


def buscar_vertice(grafo, clave):
    actual = grafo.inicio
    while actual is not None:
        if actual.info == clave:
            return actual
        actual = actual.sig
    return None


def insertar_arista(grafo, dato, origen, destino):
    v_origen = buscar_vertice(grafo, origen)
    v_destino = buscar_vertice(grafo, destino)
    if v_origen and v_destino:
        agregar_arista(v_origen, dato, destino)
        if not grafo.dirigido:
            agregar_arista(v_destino, dato, origen)


def arbol_expansion_minimo(grafo, inicio_key):
    inicio = buscar_vertice(grafo, inicio_key)
    if inicio is None:
        print(f"  No existe el personaje {inicio_key}")
        return [], 0

    visitados = {inicio.info}
    aristas_arbol = []
    peso_total = 0

    while True:
        mejor_arista = None
        mejor_origen = None
        actual = grafo.inicio
        while actual is not None:
            if actual.info in visitados:
                arista = actual.adyacentes
                while arista is not None:
                    if arista.destino not in visitados:
                        if mejor_arista is None or arista.peso < mejor_arista.peso:
                            mejor_arista = arista
                            mejor_origen = actual.info
                    arista = arista.sig
            actual = actual.sig

        if mejor_arista is None:
            break

        aristas_arbol.append((mejor_origen, mejor_arista.destino, mejor_arista.peso))
        peso_total += mejor_arista.peso
        visitados.add(mejor_arista.destino)

    print(f"  Árbol de expansión mínimo desde {inicio_key}:")
    for origen, destino, peso in aristas_arbol:
        print(f"    {origen} -- {destino} (peso/episodios: {peso})")
    print(f"    Peso total: {peso_total}")
    return aristas_arbol, peso_total


def camino_mas_corto(grafo, origen_key, destino_key):
    origen = buscar_vertice(grafo, origen_key)
    destino = buscar_vertice(grafo, destino_key)
    if origen is None or destino is None:
        print("  No se encontró el origen o destino.")
        return [], float("inf")

    distancias = {}
    anteriores = {}
    pendientes = set()
    actual = grafo.inicio
    while actual is not None:
        distancias[actual.info] = float("inf")
        pendientes.add(actual.info)
        actual = actual.sig
    distancias[origen_key] = 0

    while pendientes:
        actual_key = min(pendientes, key=lambda nombre: distancias[nombre])
        if distancias[actual_key] == float("inf"):
            break
        pendientes.remove(actual_key)
        if actual_key == destino_key:
            break

        vertice = buscar_vertice(grafo, actual_key)
        arista = vertice.adyacentes
        while arista is not None:
            if arista.destino in pendientes:
                nueva_distancia = distancias[actual_key] + arista.peso
                if nueva_distancia < distancias[arista.destino]:
                    distancias[arista.destino] = nueva_distancia
                    anteriores[arista.destino] = actual_key
            arista = arista.sig

    if distancias[destino_key] == float("inf"):
        print(f"  No existe camino entre {origen_key} y {destino_key}.")
        return [], float("inf")

    camino = [destino_key]
    while camino[-1] != origen_key:
        camino.append(anteriores[camino[-1]])
    camino.reverse()
    print(f"  Camino más corto {origen_key} -> {destino_key}: "
          f"{' -> '.join(camino)} (peso total: {distancias[destino_key]})")
    return camino, distancias[destino_key]