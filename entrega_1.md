
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

## Cambios

El primer intento devuelve lavados con prendas que son incompatibles, y luego me 
dí cuenta que es porque hice mal el razonamiento que hice para calcular prendas que son
 compatibles. Para solucionarlo, tenía que ver de obtener grupos de prendas compatibles entre si. Yo estaba obteniendo una lista de prendas compatibles con
una prenda dada, pero erroneamente asumía que ademas todas esas prendas eran compatibles entre sí (sin darme cuenta).

siguiendo la idea anterior, luego pensé en tomar la prenda con mas prendas compatibles e ir tratando de armar un lavado, asegurandome que cada prenda que agrego es compatible con las otras.

Con eso logré armar un algoritmo recursivo que primero arma un posible lavado con la prenda que 
mas prendas compatibles tiene y luego intenta mejorarla quitandole una prenda del lavado 
con mas prendas incompatibles y viendo si quitar esa prenda permite agregar mas prendas
de las que se podrian tener en el lavado manteniendo esa prenda. Esto lo hace recursivamente hasta que no se puede mejorar ese lavado.

Luego, tambien en forma recursiva, se devuelve ese lavado junto con otro mejor lavado
usando las prendas restantes.

Así obtuve un tiempo total de lavado de 66.

Tambien cambie la función `calcular_puntaje` para que tenga en cuenta el tiempo
que lleva ese lavado en hacerse, pero el resultado final no cambió. La formula es el cociente
entre el numero de prendas en ese lavado y el tiempo que lleva en hacerse ese lavado.

## Comentarios Finales

El puntaje obtenido de 66 no es óptimo ya que en el ranking hay puntajes mejores de hasta 61.
Por lo tanto este algoritmo tampoco puede ser óptimo. El algoritmo consta de hacer pequeños cambios
en la combinacion de prendas en un lavado y eligir una solución localmente óptima, y no tengo
ninguna justificación para deducir que este algoritmo (*'greedy'*) eligiendo la mejor opción local va 
llegar a la solución óptima general.

Por su puesto que un algoritmo que prueba todas las combinaciones posibles puede llegar
a la solución óptima, pero ni siquiera quería pensar en el número total de posibilidades que
mi algoritmo debería probar...
