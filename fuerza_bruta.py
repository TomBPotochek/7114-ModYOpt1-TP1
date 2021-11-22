import tp2

if __name__ == "__main__":
    grafo = tp2.parse_prendas("segundo_problema.txt")
    tp2.fuerza_bruta(grafo)