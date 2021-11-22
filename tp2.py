from collections import defaultdict
from itertools import count
from os import getuid
from typing import (DefaultDict, Dict, List, Tuple, Set, Iterable,
                    Optional)
from dataclasses import dataclass
import random


color = int
prenda = int
no_color = -1

@dataclass
class Incompatibilidades:
    """el grafo de prendas con sus prendas incompatibles 
    como lista de adyacencias"""
    adyacencias: DefaultDict[prenda, Set[prenda]]
    lista: Set[prenda] # total de prendas en el grafo
    tiempos: Dict[prenda, int] # los tiempos de lavado de cada prenda

    def iterar(self):
        """generador para iterar las prendas 
        siguiendo las adyacencias"""
        for u in self.adyacencias:
            for v in self.adyacencias[u]:
                yield u, v

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
                incompatibilidades[b].add(a)
            elif tipo == 'n':
                a,b = split_line(linea)
                a,b = int(a), int(b)
                lavados[a] = b
            else:
                pass
            linea = prendas.readline()
            if (linea == ''):
                loop = False
    return Incompatibilidades(incompatibilidades, total_prendas, lavados)



def coloreo(grafo: Incompatibilidades):
    prendas_por_color: DefaultDict[color,Set[prenda]] = defaultdict(set)
    colores_por_prenda: DefaultDict[prenda,color] = DefaultDict(lambda : no_color)
    nuevo_color: color = count()

    prendas_al_azar = list(grafo.lista)
    random.shuffle(prendas_al_azar)
    for u in prendas_al_azar:
        if colores_por_prenda[u] == no_color:
            if grafo.adyacencias[u] != set():
                colores_adyacentes = {colores_por_prenda[p] for p in grafo.adyacencias[u]}
                col_max = max(colores_adyacentes)
            else:
                colores_adyacentes = set()
                col_max = no_color

            if col_max == no_color:
                col_max = 1
            rango_colores = {c for c in range(1, col_max+2)}
            color_asignado = min(rango_colores - colores_adyacentes)

            prendas_por_color[color_asignado].add(u)
            colores_por_prenda[u] = color_asignado
    
    return prendas_por_color






def format_answer(lavados: Dict[color, Set], path_arhivo_solucion: str):
    with open(path_arhivo_solucion, "wt") as archivo:
        for color, lavado in lavados.items():
            for prenda in lavado:
                archivo.write(f"{prenda} {color}\n")

def calcular_tiempo_total(lavados: Dict[color, Set],
                grafo: Incompatibilidades):
    tiempo_total = 0
    tot_prendas = set()
    for lavado in lavados:
        for p in lavados[lavado]:
            if (lavados[lavado] & grafo.adyacencias[p]) != set():
                raise Exception(f"lavado = {lavado} no respeta incompatibilidades")

        prenda_mas_larga = max(lavados[lavado], key=lambda x:grafo.tiempos[x])
        tiempo_total += grafo.tiempos[prenda_mas_larga]
        tot_prendas |= lavados[lavado]
    if tot_prendas != grafo.lista:
        raise Exception("Los lavados no lavan toda la ropa")
    return tiempo_total

def setear_seed(seed=None):
    if seed is None:
        from sys import maxsize
        seed = random.randrange(maxsize)
    random.seed(seed)
    return seed

def fuerza_bruta(grafo: Incompatibilidades):
    mejor_tiempo = 99999
    mejor_seed = 0
    mejor_lavado = None
    try:
        while True:
            seed = setear_seed()
            lavados = coloreo(grafo)
            tiempo_actual = calcular_tiempo_total(lavados, grafo)
            if tiempo_actual < mejor_tiempo:
                mejor_tiempo = tiempo_actual
                mejor_seed = seed
                mejor_tanda = lavados
    except KeyboardInterrupt:
        print(f"mejor seed = {seed}")
        print(f"puntaje = {mejor_tiempo}")
        format_answer(mejor_tanda, "fuerza_bruta.txt")
        


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("-s", "--seed", type=int,
                        help='seed to use instead of using a random seed.')
    parser.add_argument("archivo", metavar="path_archivo", 
                        help="path al arhivo donde guardar la solucion generada")

    args = parser.parse_args()

    print(f"seed = {setear_seed(args.seed)}")



    grafo = parse_prendas("segundo_problema.txt")
    lavados = coloreo(grafo)
    print(calcular_tiempo_total(lavados, grafo))
    format_answer(lavados, args.archivo)


