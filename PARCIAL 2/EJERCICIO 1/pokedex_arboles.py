import random
from collections import deque

from datos_pokemon import POKEMONS


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
    return [n for n in inorden(raiz) if texto in n.clave]

TABLA = {
    "Normal":    ([], ["Roca", "Acero"], ["Fantasma"]),
    "Fuego":     (["Planta", "Hielo", "Bicho", "Acero"], ["Fuego", "Agua", "Roca", "Dragón"], []),
    "Agua":      (["Fuego", "Tierra", "Roca"], ["Agua", "Planta", "Dragón"], []),
    "Planta":    (["Agua", "Tierra", "Roca"], ["Fuego", "Planta", "Veneno", "Volador", "Bicho", "Dragón", "Acero"], []),
    "Eléctrico": (["Agua", "Volador"], ["Eléctrico", "Planta", "Dragón"], ["Tierra"]),
    "Hielo":     (["Planta", "Tierra", "Volador", "Dragón"], ["Fuego", "Agua", "Hielo", "Acero"], []),
    "Lucha":     (["Normal", "Hielo", "Roca", "Siniestro", "Acero"], ["Veneno", "Volador", "Psíquico", "Bicho", "Hada"], ["Fantasma"]),
    "Veneno":    (["Planta", "Hada"], ["Veneno", "Tierra", "Roca", "Fantasma"], ["Acero"]),
    "Tierra":    (["Fuego", "Eléctrico", "Veneno", "Roca", "Acero"], ["Planta", "Bicho"], ["Volador"]),
    "Volador":   (["Planta", "Lucha", "Bicho"], ["Eléctrico", "Roca", "Acero"], []),
    "Psíquico":  (["Lucha", "Veneno"], ["Psíquico", "Acero"], ["Siniestro"]),
    "Bicho":     (["Planta", "Psíquico", "Siniestro"], ["Fuego", "Lucha", "Veneno", "Volador", "Fantasma", "Acero", "Hada"], []),
    "Roca":      (["Fuego", "Hielo", "Volador", "Bicho"], ["Lucha", "Tierra", "Acero"], []),
    "Fantasma":  (["Psíquico", "Fantasma"], ["Siniestro"], ["Normal"]),
    "Dragón":    (["Dragón"], ["Acero"], ["Hada"]),
    "Siniestro": (["Psíquico", "Fantasma"], ["Lucha", "Siniestro", "Hada"], []),
    "Acero":     (["Hielo", "Roca", "Hada"], ["Fuego", "Agua", "Eléctrico", "Acero"], []),
    "Hada":      (["Lucha", "Dragón", "Siniestro"], ["Fuego", "Veneno", "Acero"], []),
}


def calcular_debilidades(tipos):
    debil = []
    for atacante, (x2, x05, x0) in TABLA.items():
        mult = 1.0
        for t in tipos:
            if t in x2:
                mult *= 2
            elif t in x05:
                mult *= 0.5
            elif t in x0:
                mult *= 0
        if mult > 1:
            debil.append(atacante)
    return debil


def cargar_pokemons():
    registros = []
    for numero, nombre, tipos, mega, gigamax in POKEMONS:
        registros.append({
            "numero": numero,
            "nombre": nombre,
            "tipos": tipos,
            "debilidades": calcular_debilidades(tipos),
            "mega": mega,
            "gigamax": gigamax,
        })
    random.shuffle(registros)   
    return registros


def construir_arboles(pokemons):
    arbol_nombre = arbol_numero = arbol_tipo = None
    for pos, p in enumerate(pokemons):
        arbol_nombre = insertar_nodo(arbol_nombre, p["nombre"].lower(), pos)
        arbol_numero = insertar_nodo(arbol_numero, p["numero"], pos)
        for t in p["tipos"]:                      
            arbol_tipo = insertar_nodo(arbol_tipo, t, pos)
    return arbol_nombre, arbol_numero, arbol_tipo


def mostrar_pokemon(p):
    print(f"  #{p['numero']:<4} {p['nombre']}")
    print(f"     Tipo/s: {', '.join(p['tipos'])}")
    print(f"     Débil frente a: {', '.join(p['debilidades'])}")
    print(f"     Megaevolución: {'Sí' if p['mega'] else 'No'} | "
          f"Gigamax: {'Sí' if p['gigamax'] else 'No'}")


def titulo(texto):
    print("\n" + "=" * 60 + f"\n{texto}\n" + "=" * 60)


def datos_por_numero(pokemons, arbol_numero, numero):
    nodo = buscar(arbol_numero, numero)
    if nodo is None:
        print(f"  No existe el Pokémon número {numero}")
    else:
        for pos in nodo.pos:
            mostrar_pokemon(pokemons[pos])


def datos_por_nombre(pokemons, arbol_nombre, texto):
    nodos = buscar_proximidad(arbol_nombre, texto)
    if not nodos:
        print(f"  Ningún nombre comienza con o contiene '{texto}'")
    for nodo in nodos:
        mostrar_pokemon(pokemons[nodo.pos[0]])


def nombres_por_tipo(pokemons, arbol_tipo, tipo):
    nodo = buscar(arbol_tipo, tipo)
    nombres = sorted(pokemons[pos]["nombre"] for pos in nodo.pos) if nodo else []
    print(f"  {tipo} ({len(nombres)}): {', '.join(nombres)}")


def debiles_frente_a(pokemons, arbol_nombre, arbol_numero, nombre):
    nodo = buscar(arbol_nombre, nombre.lower())
    if nodo is None:
        print(f"  {nombre} no está cargado")
        return
    tipos_atacante = pokemons[nodo.pos[0]]["tipos"]
    res = [pokemons[n.pos[0]]["nombre"] for n in inorden(arbol_numero)
           if set(pokemons[n.pos[0]]["debilidades"]) & set(tipos_atacante)]
    print(f"  {nombre} ({'/'.join(tipos_atacante)}) -> {len(res)} Pokémon débiles:")
    print("   ", ", ".join(res))


def main():
    pokemons = cargar_pokemons()
    arbol_nombre, arbol_numero, arbol_tipo = construir_arboles(pokemons)
    print(f"Pokémon cargados: {len(pokemons)}")

    titulo("Datos de un Pokémon por NÚMERO (25 y 697)")
    datos_por_numero(pokemons, arbol_numero, 25)
    datos_por_numero(pokemons, arbol_numero, 697)

    titulo("Datos por NOMBRE con búsqueda por proximidad: 'bul', 'char', 'saur'")
    for texto in ("bul", "char", "saur"):
        print(f"\n> '{texto}'")
        datos_por_nombre(pokemons, arbol_nombre, texto)

    titulo("Nombres de Pokémon por tipo")
    for tipo in ("Fantasma", "Fuego", "Acero", "Eléctrico"):
        nombres_por_tipo(pokemons, arbol_tipo, tipo)

    titulo("Listado ascendente por NÚMERO")
    for n in inorden(arbol_numero):
        p = pokemons[n.pos[0]]
        print(f"  {p['numero']:>4} - {p['nombre']}")

    titulo("Listado ascendente por NOMBRE")
    for n in inorden(arbol_nombre):
        print("  ", pokemons[n.pos[0]]["nombre"])

    titulo("Listado POR NIVEL del árbol de nombres")
    nivel_actual = -1
    for nivel, n in por_nivel(arbol_nombre):
        if nivel != nivel_actual:
            nivel_actual = nivel
            print(f"\n  Nivel {nivel}:", end=" ")
        print(pokemons[n.pos[0]]["nombre"], end=", ")
    print()

    titulo("Pokémon débiles frente a Jolteon, Lycanroc y Tyrantrum")
    for nombre in ("Jolteon", "Lycanroc", "Tyrantrum"):
        debiles_frente_a(pokemons, arbol_nombre, arbol_numero, nombre)

    titulo("Tipos de Pokémon y cantidad de cada uno")
    for n in inorden(arbol_tipo):
        print(f"  {n.clave:<10} {len(n.pos)}")

    titulo("Megaevoluciones y Gigamax")
    cant_mega = sum(1 for n in inorden(arbol_numero) if pokemons[n.pos[0]]["mega"])
    cant_giga = sum(1 for n in inorden(arbol_numero) if pokemons[n.pos[0]]["gigamax"])
    print(f"  Con megaevolución: {cant_mega}")
    print(f"  Con forma gigamax: {cant_giga}")


if __name__ == "__main__":
    main()
