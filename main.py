from collections import defaultdict
from os import getuid
from typing import Tuple, Set, Dict

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

#le asigna un puntaje al conjunto de prendas que forma un lavado
#en base a la cantidad de prendas que tiene y el tiempo de la mas grande
def calcular_puntaje(lavado: Set):
    global tiempos_lavado
    tiempos_de_prendas = [tiempos_lavado[p] for p in lavado]
    if tiempos_de_prendas == []:
        return 0
    else:
        t_max = max([tiempos_lavado[p] for p in lavado])
        
        #aumenta con el num de prendas pero baja con el tiempo de la peor
        return len(lavado)/t_max 

def mejorar_lavado(lavado: Set, grupo_compatibles: Set,
                compatibilidades: defaultdict,
                     incompatibilidades: defaultdict):
    
    puntaje = calcular_puntaje(lavado)

    mas_restrictiva = sorted(lavado,
                         key=lambda x: len(incompatibilidades[x]),
                          reverse=True)

    for prenda in mas_restrictiva:
        nuevo_lavado = lavado - {prenda}

        for p in grupo_compatibles:
            if (p not in lavado):
                if (nuevo_lavado & incompatibilidades[p]) == set():
                    nuevo_lavado.add(p)
        if calcular_puntaje(nuevo_lavado) > puntaje:
            return mejorar_lavado(nuevo_lavado, grupo_compatibles,
                                    compatibilidades, incompatibilidades)
        
    return lavado
        



def generar_lavados(compatibilidades: defaultdict,
                     incompatibilidades: defaultdict):

    #caso base
    vacio = True
    for p in compatibilidades:
        if compatibilidades[p] != set(): #vacio
            vacio = False
            break #para ahorrar algunos ciclos
    if vacio:
        return tuple() #retornar tupla vacia

    prenda, grupo_compatibles = max(compatibilidades.items(),
                                    key=lambda x:len(x[1]))
    lavado = set()

    for p in grupo_compatibles:
        # si no es incompatible con ninguna del lavado, la agrego
        if (lavado & incompatibilidades[p]) == set():
            lavado.add(p)
    lavado = mejorar_lavado(lavado, grupo_compatibles,
                            compatibilidades, incompatibilidades)
    
    #quito las prendas de este lavado del resto de las prendas
    for p in compatibilidades:
        compatibilidades[p] -= lavado
    # for p in incompatibilidades:
    #     incompatibilidades[p] -= lavado
    return lavado, *generar_lavados(compatibilidades, incompatibilidades)
    


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
    lavados = generar_lavados(compat, incompat)

    print(calcular_tiempo_total(lavados, tiempos_lavado))

    format_answer(lavados, "solucion.txt")
