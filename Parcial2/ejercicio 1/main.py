import random
from arbol_binario import insertar_nodo, buscar, inorden, por_nivel, buscar_proximidad
from datos_pokemon import POKEMONS

TABLA_TIPOS = {
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
    for atacante, (x2, x05, x0) in TABLA_TIPOS.items():
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


def mostrar_pokemon(p):
    print(f"  #{p['numero']:<4} {p['nombre']}")
    print(f"     Tipo/s: {', '.join(p['tipos'])}")
    print(f"     Débil frente a: {', '.join(p['debilidades'])}")
    print(f"     Megaevolución: {'Sí' if p['mega'] else 'No'} | Gigamax: {'Sí' if p['gigamax'] else 'No'}")


def main():
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
    print(f"Total de Pokémons cargados: {len(registros)}")


    arbol_nombre = arbol_numero = arbol_tipo = None
    for pos, p in enumerate(registros):
        arbol_nombre = insertar_nodo(arbol_nombre, p["nombre"].lower(), pos)
        arbol_numero = insertar_nodo(arbol_numero, p["numero"], pos)
        for t in p["tipos"]:
            arbol_tipo = insertar_nodo(arbol_tipo, t, pos)


    print("\n--- BÚSQUEDA POR NÚMERO (25) ---")
    nodo_num = buscar(arbol_numero, 25)
    if nodo_num:
        for pos in nodo_num.pos:
            mostrar_pokemon(registros[pos])

    print("\n--- BÚSQUEDA POR PROXIMIDAD ('bul') ---")
    nodos_prox = buscar_proximidad(arbol_nombre, "bul")
    for n in nodos_prox:
        mostrar_pokemon(registros[n.pos[0]])


    print("\n--- POKÉMONS POR TIPO (Fantasma, Fuego, Acero, Eléctrico) ---")
    for t_buscado in ["Fantasma", "Fuego", "Acero", "Eléctrico"]:
        nodo_t = buscar(arbol_tipo, t_buscado)
        nombres = sorted(registros[pos]["nombre"] for pos in nodo_t.pos) if nodo_t else []
        print(f"  {t_buscado} ({len(nombres)}): {', '.join(nombres)}")


    print("\n--- LISTADO ASCENDENTE POR NÚMERO ---")
    for n in inorden(arbol_numero):
        p = registros[n.pos[0]]
        print(f"  #{p['numero']:>4} - {p['nombre']}")

    print("\n--- LISTADO ASCENDENTE POR NOMBRE ---")
    for n in inorden(arbol_nombre):
        print(f"  {registros[n.pos[0]]['nombre']}")

    print("\n--- LISTADO POR NIVEL (ÁRBOL NOMBRES) ---")
    nivel_act = -1
    for nivel, n in por_nivel(arbol_nombre):
        if nivel != nivel_act:
            nivel_act = nivel
            print(f"\nNivel {nivel}:", end=" ")
        print(registros[n.pos[0]]["nombre"], end=", ")
    print()


    print("\n--- DÉBILES FRENTE A JOLTEON, LYCANROC Y TYRANTRUM ---")
    for ref_nombre in ["Jolteon", "Lycanroc", "Tyrantrum"]:
        nodo_ref = buscar(arbol_nombre, ref_nombre.lower())
        if nodo_ref:
            tipos_ref = registros[nodo_ref.pos[0]]["tipos"]
            debiles = [registros[n.pos[0]]["nombre"] for n in inorden(arbol_numero)
                       if set(registros[n.pos[0]]["debilidades"]) & set(tipos_ref)]
            print(f"  Débiles frente a {ref_nombre} ({'/'.join(tipos_ref)}): {len(debiles)}")


    print("\n--- CANTIDAD POR TIPO ---")
    for n in inorden(arbol_tipo):
        print(f"  {n.clave}: {len(n.pos)}")

    cant_mega = sum(1 for n in inorden(arbol_numero) if registros[n.pos[0]]["mega"])
    cant_giga = sum(1 for n in inorden(arbol_numero) if registros[n.pos[0]]["gigamax"])
    print(f"\nTotal con Megaevolución: {cant_mega}")
    print(f"Total con Forma Gigamax: {cant_giga}")


if __name__ == "__main__":
    main()