
## Primera impresión

Si bien el problema suena simple, no me fue claro qué metodología se tendría que aplicar para resolver el problema. 
Mi primera impresión es que debíamos implementar
esencialmente los mismos algoritm|os que emplean programas como GLPK para resolver
programación lineal contínua, lo cual es algo que no tengo idea como hacer ni sé
cuales son esos algoritmos. 

Luego de pensarlo más, el problema me recordaba al problema del viajante, ya que uno
querria de alguna manera "pasar" por todas las prendas minimizando el tiempo total
que se pasó lavando. El problema es que no es una relación directa con el prboblema
ya que las prendas se agrupan en lavados y serian estos lavados los obejtos que se
corresponderian con las ciudades que visita el viajante, pero la cantidad de ciudades
y las distancias entre ellas estarian variando en el problema al ser que mientras
mas prendas agrupe en un lavado, menos ciudades distintas podrian haber y a su vez cambiar 
el tiempo de lavado o la "distancia" entre ciudades. Por esto me alejé de esta idea.

## Primeras ideas

Como primera idea, pensé en tomar la primera prenda que vemos al iterar y asociarle la mayor cantidad
de prendas compatibles que podamos, ignorando el tiempo que lleva cada prenda en lavar. luego asociar todo ese conjunto a un lavado y quitarlas
del total de prendas, luego repetir el razonamiento con el resto de las prendas que encontramos hasta que (con suerte) no queden mas prendas.
Luego repetir todo este razonamiento de nuevo pero viendo si empezando con distintas prendas logramos mejores resultados.

Tal vez es mejor elegir la prenda con mas compatibilidades posibles en lugar de simplemente la primera
y repetir ese razonamiento, usando siempre la prenda que tenga el mayor numero de prendas compatibles
en cada instancia. Con esta heurística, estaria usando un algoritmo *'greedy'*.