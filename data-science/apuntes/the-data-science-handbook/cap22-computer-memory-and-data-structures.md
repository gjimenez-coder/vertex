# The Data Science Handbook — Field Cady (Wiley, 2017)
## Capítulo 22 — Computer Memory and Data Structures (Memoria del ordenador y estructuras de datos)

> Nota de extracción: texto obtenido de la capa de texto del PDF; las citas usan la página del PDF (PDF p. N). Se conservan solo los fragmentos de código esenciales.

## Lo que necesitas saber
El capítulo explica cómo se dispone la memoria de un programa y cómo se codifican los datos en ella, para después mostrar las estructuras de datos más usadas y cómo su disposición física explica su rendimiento. Se enseña con el lenguaje C, un lenguaje de bajo nivel que da control muy fino sobre el uso de memoria; de hecho, el intérprete principal de Python está escrito en C. No es un curso de C, pero da lo suficiente para entender cómo se implementan las estructuras clave y cómo forman la base de Python.

La tesis central es que los conceptos de tipos de tamaño fijo, arrays de ellos y punteros son los ingredientes con los que se construyen estructuras complejas y eficientes. Entender esos ingredientes permite comprender por qué las listas, diccionarios, strings y clases de Python se comportan como lo hacen y por qué tienen el rendimiento que tienen.

Sales sabiendo qué son la memoria virtual, el stack y el heap; cómo se almacenan tipos atómicos, arrays, structs y punteros; y cómo se combinan para formar strings, arrays ajustables, tablas hash, listas enlazadas y árboles binarios de búsqueda. Cady recalca que en el día a día de la ciencia de datos no se necesita este detalle, pero sirve de primer contacto por si alguna vez se escriben algoritmos de bajo nivel.

## Memoria virtual, el stack y el heap
Una de las tareas más importantes del sistema operativo es permitir que varios procesos compartan la misma RAM física. Para ello da a cada proceso un "espacio de direcciones virtual" (virtual address space, VAS), con direcciones de 0 a 2^32−1 en sistemas de 32 bits y de 0 a 2^64−1 en los de 64 bits. Cada dirección contiene exactamente 1 byte. El sistema operativo gestiona qué direcciones del VAS corresponden a qué posiciones en RAM, y puede mover los datos entre RAM, las capas de caché y el disco. Desde la perspectiva del programa, el VAS es todo lo que existe.

El proceso no puede acceder al VAS a su antojo: primero debe pedir al sistema operativo que reserve RAM física y la asocie a direcciones del VAS. Si accede a una dirección no asignada, se produce un "segmentation fault" (seg fault), una clase notoria de bugs en lenguajes de bajo nivel como C, imposibles en Python. Cuando ya no se necesita el espacio, el proceso debe "liberarlo" (free), avisando al sistema operativo de que esas direcciones quedan disponibles para otro proceso.

## Programa C de ejemplo
El clásico "hello, world" muestra las partes esenciales de un programa en C:

```c
#include <stdio.h>
#include <stdlib.h>
int main(void) {
  printf("hello, world\n");
  return 0;
}
```

Lo esencial es la subrutina `main`: es obligatoria en C (en Python es opcional) y es el punto de arranque. Se escribe `int main` porque devuelve el entero 0, que se pasa al sistema operativo al terminar. La primera línea incluye la librería `stdio`, que contiene `printf`. Para compilar y ejecutar (en un mac con el toolkit de desarrollo) basta con `gcc mycode.c` y luego `./a.out`.

## Tipos de datos y arrays en memoria
Además de los enteros, C tiene tipos como `double` (números decimales) y `char` (un único carácter de 1 byte). Cada tipo atómico ocupa un número fijo de bytes, que depende del ordenador (el del autor usa 4 bytes para un `int`), pero lo clave es que el tamaño es fijo.

Un array de enteros es, por debajo, los bytes de sus enteros concatenados. Como todos los enteros ocupan lo mismo, extraer el elemento i-ésimo es tomar el grupo de bytes desplazado i*(bytes de un int) desde el inicio del array: así el ordenador sabe dónde termina un int y empieza otro, y es una operación O(1) sin importar el tamaño del array.

En NumPy todos los números se guardan como arrays de C; por eso ocupan tan poco y son tan rápidos: son bucles for de C sobre los bytes crudos. También por eso los arrays de NumPy, a diferencia de las listas de Python, solo contienen datos del mismo tipo: todos los elementos deben tener el mismo tamaño.

## Structs
El tipo compuesto más simple es el struct, que agrupa varios campos de tipos primitivos de tamaño fijo:

```c
struct Person {
  int age;
  char gender;
  double height;
};
typedef struct Person Person;
```

El `typedef` permite escribir `Person` en vez de `struct Person`. Como los tipos atómicos, un `Person` ocupa un número fijo de bytes: los de `age`, `gender` y `height` concatenados en un orden que elige el compilador, a veces con bytes de relleno por rendimiento. El código compilado no habla del campo "gender", sino de los bytes desplazados cierta distancia desde el inicio del `Person`. Se pueden tener arrays de structs y acceder a sus datos eficientemente: el género del n-ésimo `Person` es el byte desplazado n*(bytes de un Person) + (offset del campo gender) desde el inicio del array.

## Punteros, el stack y el heap
Un puntero es un tipo muy importante: se guarda como un entero (tamaño fijo) pero almacena el índice en el VAS de un byte concreto. Así se puede referir a datos en cualquier ubicación, que puede ser el inicio de un objeto o array de tamaño y complejidad arbitrarios. Si un `Person` tiene un campo `struct Person* spouse`, ese campo no es un `Person` sino un puntero al primer byte de un `Person`. El término `NULL` significa que el puntero no apunta a nada (todos 0s).

Al pasar objetos a una función hay dos modos. "Pasar por referencia" significa pasar punteros, de modo que los cambios afectan a los datos originales en memoria y persisten al terminar la subrutina; se accede a los campos con `->` en vez de `.`, y `&Bob` es la sintaxis para un puntero a `Bob`. En Python los objetos siempre se pasan por referencia: si `B = A` sobre un diccionario, modificar `B` modifica `A`. La alternativa, "pasar por valor", copia la estructura entera: a veces es más rápido (no hay que seguir punteros) pero cuesta copiar estructuras potencialmente enormes.

La razón para usar el heap en vez del stack es que el compilador necesita conocer el tamaño de todas las estructuras en tiempo de compilación. Si queremos un array de `Person` cuyo tamaño decida el usuario en ejecución, ese array debe ir al heap: se pide al sistema operativo en tiempo de ejecución un bloque de ese tamaño, con `malloc()` (devuelve un puntero al primer byte), y hay que avisarle cuando ya no se necesita con `free()`. Como en los bytes no hay forma de saber dónde acaba el array, hace falta un `int n_children` para llevar la cuenta de la longitud.

Si no se libera la memoria del heap, se produce un "memory leak" (fuga de memoria): un bug sorprendentemente fácil de escribir en el que el programa reserva variables sin parar hasta agotar la memoria y fallar. La memoria reservada pero sin ningún puntero que la referencie se llama "orphaned" (huérfana). El autor advierte de que su código es deliberadamente descuidado para facilitar la comprensión y que no debe escribirse así en producción, por ejemplo respecto a si los punteros apuntan a lugares válidos.

## Estructuras de datos clave
Con structs de tamaño fijo, arrays de ellos y punteros se construye una gran variedad de estructuras complejas y eficientes, base de Python y de casi todo el software.

Strings: en C no son un tipo atómico (como sí en Python) porque tienen longitud variable, así que se crean en el heap y se guardan como un `char*` (puntero a un array de bytes interpretados como caracteres, normalmente ASCII). Para saber su longitud hay dos opciones: envolver el `char*` en un struct con un contador `n_chars`, o la forma antigua de terminar el array con un byte 0 ("null-terminated"), más difícil de manejar y más lenta, pero que ocupa algo menos de RAM.

Arrays de tamaño ajustable: un array normal tiene tamaño fijo, así que añadir un elemento obliga a reservar uno nuevo, copiar y colocar el último, una operación O(n). Los arrays ajustables lo convierten en O(1) amortizado: se reserva más espacio del necesario y se rellenan los huecos. Cuando se llena, se crea uno nuevo (típicamente del doble de tamaño) y se copia; las copias se vuelven el doble de caras pero la mitad de frecuentes, dando coste neto O(1) amortizado. La lista de Python es, por debajo, un array ajustable, pero de punteros a objetos arbitrarios de Python, no de ints.

Tablas hash: los arrays solo se indexan por enteros; una tabla hash permite mapear tipos más flexibles como strings. Su pieza central es una función hash f() que toma un objeto x y devuelve un entero en el rango 0 a N, con tres propiedades: es determinista (misma entrada, misma salida), se calcula en O(1), y "parece aleatoria" (para x distintos casi siempre da resultados distintos). La idea: se guardan los datos en un array pero el índice es el hash de la clave, así la búsqueda sigue siendo O(1); el array suele ser de punteros, `NULL` donde no hay elemento.

En Python las tablas hash son centrales: los diccionarios se implementan así, igual que el namespace que mapea nombres de variables a objetos y las instancias de clases definidas por el usuario; se dice que todo Python es azúcar sintáctico sobre tablas hash. Como a veces dos claves distintas colisionan (`hash(x) = hash(y)`), hay que guardar también la clave para compararla, y resolver colisiones buscando otra celda libre o apuntando a otra estructura. Cuando la tabla se llena se hace un "rehashing": se crea una tabla mayor con nueva función hash y se recolocan todos los pares, una operación O(n) que, si se crece por un factor constante, mantiene las inserciones en O(1) amortizado.

Listas enlazadas: una lista enlazada es una forma ligera de implementar una lista de objetos de un tipo conocido. Cada nodo es un struct con dos campos: el valor y un puntero al siguiente nodo; el último apunta a `NULL`.

```c
struct LinkedListNode {
  int Value;
  LinkedListNode* next;
};
```

Su gran desventaja es que hallar el elemento i-ésimo es O(i), no O(1). Su gran ventaja (además de la simplicidad) es que insertar un elemento, si se tiene un puntero al sitio, es O(1) puro, no amortizado. En la inserción el orden importa: primero `newNode->next = currentNode->next` y después `currentNode->next = newNode`; invertirlos haría que el nodo apuntara a sí mismo, creando un bucle infinito y dejando el resto de la lista huérfano. Equivocarse en manipulaciones de punteros es notoriamente fácil, y por eso atraen lenguajes de alto nivel como Python; aun así, con cuidado, C logra un rendimiento con el que Python solo puede soñar.

Árboles binarios de búsqueda (BST): cada nodo contiene un valor numérico y tiene dos hijos, "left" y "right". En todo momento, los hijos de la derecha tienen valores mayores o iguales y los de la izquierda menores o iguales. Si el árbol está equilibrado (cada nodo con tantos descendientes a la izquierda como a la derecha), comprobar si un número está o añadir uno nuevo es O(log(n)), y de nuevo no amortizado. La búsqueda es recursiva: si el nodo es `NULL` devuelve falso; si n es menor que el valor del nodo busca a la izquierda; si no, a la derecha. El autor cierra recordando que en la práctica diaria de la ciencia de datos no se necesita esto, y que el capítulo sirve de primer contacto por si se escriben algoritmos de bajo nivel.

## Ideas clave
- El sistema operativo da a cada proceso un espacio de direcciones virtual (VAS); acceder a memoria no asignada provoca un seg fault, imposible en Python.
- Los tipos atómicos y los structs son de tamaño fijo; un array es sus bytes concatenados, por lo que acceder al elemento i-ésimo es O(1).
- NumPy usa arrays de C por debajo: de ahí su eficiencia y que todos los elementos deban ser del mismo tipo.
- Un puntero es un entero que guarda una dirección del VAS; pasar por referencia modifica el objeto original, pasar por valor copia la estructura. Python siempre pasa por referencia.
- El heap guarda memoria reservada dinámicamente con `malloc()` y liberada con `free()`; no liberarla causa memory leaks y memoria huérfana.
- Los arrays ajustables (lista de Python) dan inserción O(1) amortizado duplicando su tamaño al llenarse.
- Las tablas hash mapean claves a valores usando una función hash determinista y O(1); son la base de los diccionarios, el namespace y las clases de Python.
- Las listas enlazadas dan inserción O(1) pero acceso O(i); los BST equilibrados dan búsqueda e inserción O(log(n)).
