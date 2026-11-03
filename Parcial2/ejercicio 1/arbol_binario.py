from collections import deque

class NodoArbol:
    def __init__(self, clave, pos):
        self.clave = clave      
        self.pos = [pos]        
        self.izq = None
        self.der = None


def insertar_nodo(raiz, clave, pos):
    if raiz is None:
        return NodoArbol(clave, pos)
    if clave == raiz.clave:
        raiz.pos.append(pos)
    elif clave < raiz.clave:
        raiz.izq = insertar_nodo(raiz.izq, clave, pos)
    else:
        raiz.der = insertar_nodo(raiz.der, clave, pos)
    return raiz


def buscar(raiz, clave):
    while raiz is not None:
        if clave == raiz.clave:
            return raiz
        raiz = raiz.izq if clave < raiz.clave else raiz.der
    return None


def inorden(raiz):
    if raiz is not None:
        yield from inorden(raiz.izq)
        yield raiz
        yield from inorden(raiz.der)


def por_nivel(raiz):
    if raiz is None:
        return
    cola = deque([(0, raiz)])
    while cola:
        nivel, nodo = cola.popleft()
        yield nivel, nodo
        if nodo.izq is not None:
            cola.append((nivel + 1, nodo.izq))
        if nodo.der is not None:
            cola.append((nivel + 1, nodo.der))


def buscar_proximidad(raiz, texto):
    texto = texto.lower()
    return [n for n in inorden(raiz) if texto in str(n.clave).lower()]