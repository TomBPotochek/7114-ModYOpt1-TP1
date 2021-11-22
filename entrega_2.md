## Usando el algoritmo de TP1
Primero veo qué resulta de usar el algoritmo del TP1 en el problema del TP2 sin modificarlo.
Resulta que existe un bug en la implementación del algoritmo ya que devuelve 1 lavado con todas 
las prendas que existen en el problema, lo cual es claramente imposible ya que al menos 1 par 
de prendas eran incompatibles entre sí.  
El motivo yace en la línea `compat[prenda] = tot_prendas - incompat[prenda]` donde 
se determina las compatibilidades de una prenda en base a las incompatibilidades de la misma. 
El problema es que esta implícitamente asumiendo cierta simetría en estas incompatibilidades que 
no esta explicitado en ningún lado: que si `a` es incompatible con `b`, entonces `b` tiene 
a `a` en su lista de prendas incompatibles. Esto no era así en el código tal cual estaba. 
Por lo tanto, si una prenda no "tenía problemas" con ninguna prenda, su lista de incompatibilidades 
era nula, por más que otras prendas eran incompatibles con esa prenda.  
La solución a esto es simplemente modificar la función que parsea el archivo para que cuando 
agrega la incompatibilidad `(a,b)`, tambien agregue la incompatibilidad `(b,a)`.

Con esta modificación efectuada, el puntaje obtenido es de un tiempo total de lavado de 691 
repartido entre 42 lavados.

## Nuevas ideas

Ahora es claro que el problema es un problema de coloreo de grafos.  
Si tengo un grafo que tiene a cada prenda en un vértice y cada vértice está conectado 
con una prenda incompatible con sí misma, se podría decir que armar lavados 
es lograr tener la menor cantidad de colores posibles tal que ningún vertice 
esta pintado del mismo color que uno adyacente.  
Se tendría que cada color representaría un lavado/tanda y que nunca se daría 
el caso que un vértice es del mismo color que el de un vértice con el cual 
es incompatible.

Sin embargo, el problema modelado de esta manera no tiene en cuenta los tiempos 
de lavado de cada prenda y por lo tanto no optimiza los tiempos de los lavados.
Investigando un poco, se tiene que existe una variante conocida del problema del coloreo 
de grafos que considera exactamente esta problemática, y se lo suele llamar 
*"Scheduling on a Batch Machine with Job Compatibilities"* en inglés.

Resulta que hay mucha literatura sobre este problema, la mayor parte refiriendose a 
modelos de programación lineal y otra parte a algoritmos para aproximar una solución optima, 
pero casi todos esos algoritmos son muy complicados y dificiles de enteder (e implementar).

## Intentos mejora al algoritmo del tp1

Una cosa que quería intentar era cambiar la manera en la que el algoritmo 
elije una prenda para mejorar el puntaje de un lavado dado. Para eso cambié 
que se elija una prenda para intercambiar en base a cuál (de entre las compatibles) tiene 
en sí la mayor cantidad de prendas compatibles. Luego se removería esta prenda de la variable 
que lleva cuenta de estas para no volver a elejirla.  
Esto resulto futíl ya que la solución final empeoró a 801.

## Nuevo método

Ahora probé plantiar el algoritmo como uno que trabaja con grafos y usa una heurística simple 
para elejir un color a cada vértice.  
Básicamente, el grafo es una lista de adyacencias donde cada adyacencia representa la incompatibilidad entre 
ese par de prendas. El algoritmo v1 itera por cada vertice y le asigna un color que no lo tenga ninguno 
de los vertices adyacentes.

Tambien implementé que se recorra los vertices en un órden al azar cada vez que se ejecuta el programa, 
per ademas si uno quiere repetir una corrida exactamente, el programa reporta la semilla usada para 
el módulo `random` y se lo puede pasar por parametro al programa con el flag `--seed $N` donde `$N` 
lo uso para indicar la semilla a usar.

### Posibles mejoras

El algoritmo en sí no tiene en cuenta los distintos pesos (tiempos de lavado) asociados a cada 
vértice. Como el algoritmo es sensible a el órden en que se recorre el grafo y se lo colorea, 
obtener mejores resultados se esta haciendo solamente variando ese órden.  
Una posible mejora seria entonces mirar a qué color se esta por asignar a un vértice y ver cuál 
es el peso máximo actual asociado a ese color. Si el peso es similar, usar ese color. Si es muy 
distinto, usar otro color, al costo de terminar creando un lavado nuevo.  
Otra posibilidad es probar con distintos seed por fuerza bruta. 
