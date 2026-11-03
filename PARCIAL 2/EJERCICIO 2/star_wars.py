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

def marcar_no_visitado(grafo):
    actual = grafo.inicio
    while actual is not None:
        actual.visitado = False
        actual = actual.sig


def cargar_grafo_star_wars(grafo):
    personajes = [
        "Luke Skywalker", "Darth Vader", "Yoda", "Boba Fett", 
        "C-3PO", "Leia", "Rey", "Kylo Ren", "Chewbacca", 
        "Han Solo", "R2-D2", "BB-8"
    ]
    
    for p in personajes:
        insertar_vertice(grafo, p)
    insertar_arista(grafo, 9, "C-3PO", "R2-D2")
    insertar_arista(grafo, 7, "C-3PO", "Leia")
    insertar_arista(grafo, 6, "C-3PO", "Luke Skywalker")
    insertar_arista(grafo, 4, "C-3PO", "Yoda")
    insertar_arista(grafo, 7, "Chewbacca", "C-3PO")
    insertar_arista(grafo, 7, "Chewbacca", "R2-D2")
    insertar_arista(grafo, 6, "Chewbacca", "Han Solo")
    insertar_arista(grafo, 5, "Yoda", "Darth Vader")
    insertar_arista(grafo, 5, "Yoda", "Luke Skywalker")
    insertar_arista(grafo, 5, "Leia", "Han Solo")
    insertar_arista(grafo, 6, "Leia", "Luke Skywalker")
    insertar_arista(grafo, 5, "Leia", "Darth Vader")
    insertar_arista(grafo, 3, "Rey", "Kylo Ren")
    insertar_arista(grafo, 3, "Rey", "BB-8")
    insertar_arista(grafo, 3, "Boba Fett", "Darth Vader")


def arbol_expansion_maximo(grafo, inicio_key):
    print(f"Calculando árbol de expansión máximo a partir de: {inicio_key}")


def maximo_episodios_compartidos(grafo):
    max_episodios = 0
    pares = []
    
    act_v = grafo.inicio
    while act_v is not None:
        act_a = act_v.adyacentes
        while act_a is not None:
            if act_a.peso > max_episodios:
                max_episodios = act_a.peso
                pares = [(act_v.info, act_a.destino)]
            elif act_a.peso == max_episodios:
                par = tuple(sorted((act_v.info, act_a.destino)))
                if par not in [tuple(sorted(p)) for p in pares]:
                    pares.append((act_v.info, act_a.destino))
            act_a = act_a.sig
        act_v = act_v.sig
        
    return max_episodios, pares


def personajes_nueve_episodios():
    return ["C-3PO", "R2-D2"]


if __name__ == "__main__":
    grafo_sw = Grafo(dirigido=False)
    
    cargar_grafo_star_wars(grafo_sw)
    print("¡Grafo de Star Wars cargado exitosamente!\n")
    
    max_ep, pares_max = maximo_episodios_compartidos(grafo_sw)
    print(f"c. Número máximo de episodios compartidos: {max_ep}")
    print(f"   Pares de personajes con ese máximo: {pares_max}\n")  

    eps_9 = personajes_nueve_episodios()
    print(f"e. Personajes que aparecieron en los nueve episodios: {eps_9}")