# Desafío 3 GrupoRA: Pandemic Simulator 
## Instrucciones 
---
Requiere python 3 y Unidecode 1.1.

Al momento de ejecutar el código se puede utilizar el siguiente comando.

    $ python3 main.py <max_lines> 

El código se puede ejecutar sin argumentos o con cualquiera de los presentados:
- max_lines: Cantidad de líneas del data set que se insertan en la estructura. Por defecto 1500.


## Estructura 
La estructura utilizada para este desafío fue un Trie. Cada nodo del Trie contiene una palabra. Los nodos que son hojas del árbol contienen un contador que indica la cantidad de veces que fue ingresada la oración.

Uno de los grandes problemas que encontramos con la estructura Trie fue la búsqueda. En el caso de que se comience una búsqueda en una palabra que no está en el nodo raiz, las probabilidades de encontrarla son muy bajas. Así mismo, encontrar una palabra en la búsqueda no nos asegura encontrar todas las instancias de esa palabra en el árbol. 

Para mejorar la fidelidad de la búsqueda y el tiempo de ejecución, se implementó la búsqueda en anchura para recorrer todo el árbol. Recordemos que la complejidad de la búsqueda en profundidad es muy alta. Es por esto que también se definió una profundidad máxima de búsqueda. La profundidad máxima es igual a la cantidad de palabras que se buscan

Los resultados de esto aportan a encontrar más coincidencias de la palabra, sin embargo, se pierde un poco el contexto de la oración. Los resultados con esta mejora son muy superiores a los del trie standard.

## Algoritmo
El algoritmo comienza cargando el data set e insertando todos los datos al Trie, hasta un máximo de líneas. Para ello, se realiza una limpieza de los caracteres no perteneciente a la codificación estándar Unicode. Luego se separa cada oración en strings de palabras individuales, las cuales se insertan al Trie.

Luego de esto, se realizan búsquedas de inputs ingresados hasta que se ingresa un input vacío. Finalmente, al ser ingresado una cadena vacía, el programa finaliza su ejecución

### Trie.query
La búsqueda dentro del Trie se comporta distinto dependiendo de si la palabra o palabras buscadas están o no dentro del nodo origen. 

Si la primera palabra de la query se encuentra dentro del nodo origen, se continúa la búsqueda siguiendo el camino correspondiente hasta la última palabra, si se encuentra se calcula su probabilidad en base al contador de los nodos encontrados para todas las ramas con origen en el último nodo encontrado.

Si la primera palabra no se encuentra, se realiza una búsqueda en en anchura para encontrar todas las instancias de la palabra dentro del trie. Luego, se calcula su probabilidad en base al contador de los nodos encontrados para todas las ramas con origen en el último nodo encontrado.

Finalmente, se retornan los resultados ordenados de mayor a menor para que el algoritmo principal los muestre hasta un máximo de 10 resultados.







