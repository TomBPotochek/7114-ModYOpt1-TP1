from collections import defaultdict

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
                #no se para que me sirve
                pass
            elif tipo == 'e':
                a,b = linea[2::].strip().split(' ')
                a,b = int(a), int(b)
                incompatibilidades[a].add(b)
            elif tipo == 'n':
                a,b = linea[2::].strip().split(' ')
                a,b = int(a), int(b)
                lavados[a] = b
            else:
                pass
            linea = prendas.readline()
            if (linea == ''):
                loop = False
    return incompatibilidades, lavados




if __name__ == '__main__':
    incompat, lavados = parse_prendas("primer_problema.txt")
    print(f"{incompat=}\n{lavados=}")
