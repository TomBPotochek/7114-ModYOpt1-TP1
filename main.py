from collections import defaultdict

def split_line(line: str):
    return line[2::].strip().split(' ')

def parse_prendas(path: str):
    with open(path, "rt") as prendas:
        incompatibilidades = defaultdict(set)
        lavados = {}
        linea = prendas.readline()
        if (linea != ''):
            loop = True
        while(loop):
            tipo = linea[0]
            if tipo == 'c':
                pass
            elif tipo == 'p':
                coment, n_prendas, n_incompat = split_line(linea)
                #solo uso n_prendas. no se para que usar el resto
                n_prendas = int(n_prendas)
                total_prendas = {a+1 for a in range(n_prendas)}
            elif tipo == 'e':
                a,b = split_line(linea)
                a,b = int(a), int(b)
                incompatibilidades[a].add(b)
            elif tipo == 'n':
                a,b = split_line(linea)
                a,b = int(a), int(b)
                lavados[a] = b
            else:
                pass
            linea = prendas.readline()
            if (linea == ''):
                loop = False
    return incompatibilidades, lavados, total_prendas

def generar_lavados(total_prendas: set,
                         compatibilidades: defaultdict):
    
    if not compatibilidades: #vacia
        return tuple()

    prenda, lavado = max(compatibilidades.items(),
                         key=lambda x:len(x[1]))
    del compatibilidades[prenda]

    for p in list(compatibilidades.keys()):
        compatibilidades[p] -= lavado
        if compatibilidades[p] == set():
            del compatibilidades[p]
    
    return lavado, *generar_lavados(tot_prendas, compatibilidades)

from typing import Tuple, Set, Dict
def format_answer(lavados: Tuple[Set], path_arhivo_solucion: str):
    with open(path_arhivo_solucion, "wt") as archivo:
        for num_lavado, lavado in enumerate(lavados):
            num_lavado += 1 #el primer indice es 0, no 1
            for prenda in lavado:
                archivo.write(f"{prenda} {num_lavado}\n")

def calcular_tiempo_total(lavados: Tuple[Set],
                 tiempo_por_prenda: Dict[int, int]):
    tiempo_total = 0
    for lavado in lavados:
        prenda_mas_larga = max(lavado, key=lambda x:tiempo_por_prenda[x])
        tiempo_total += tiempo_por_prenda[prenda_mas_larga]
    return tiempo_total



if __name__ == '__main__':
    incompat, tiempos_lavado, tot_prendas = parse_prendas("primer_problema.txt")

    compat = {}
    for prenda in tot_prendas:
        compat[prenda] = tot_prendas - incompat[prenda]
    lavados = generar_lavados(tot_prendas, compat)

    print(calcular_tiempo_total(lavados, tiempos_lavado))

    format_answer(lavados, "solucion.txt")
