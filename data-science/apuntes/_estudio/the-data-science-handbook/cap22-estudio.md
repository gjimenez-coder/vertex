# Computer Memory and Data Structures (Memoria del ordenador y estructuras de datos) — Estudio

## Tarjetas de repaso

P: ¿Qué es el espacio de direcciones virtual (VAS) y qué rango tiene? / R: Es el conjunto de direcciones que el sistema operativo da a cada proceso; va de 0 a 2^32−1 en sistemas de 32 bits y de 0 a 2^64−1 en los de 64 bits, y cada dirección contiene exactamente 1 byte.

P: ¿Qué es un segmentation fault? / R: El error que ocurre cuando un proceso accede a una dirección del VAS que no está asignada; es un bug notorio en lenguajes de bajo nivel como C e imposible en Python.

P: ¿Por qué extraer el elemento i-ésimo de un array es O(1)? / R: Porque todos los tipos atómicos ocupan un tamaño fijo, así que el elemento i está en el grupo de bytes desplazado i*(bytes del tipo) desde el inicio del array.

P: ¿Por qué los arrays de NumPy solo contienen datos del mismo tipo? / R: Porque por debajo son arrays de C y todos los elementos deben tener el mismo tamaño fijo; esto los hace compactos y rápidos (bucles for de C sobre bytes crudos).

P: ¿Qué es un struct y cómo ocupa la memoria? / R: Es el tipo compuesto más simple, que agrupa campos primitivos de tamaño fijo; ocupa un número fijo de bytes (los campos concatenados en el orden que elige el compilador, a veces con relleno).

P: ¿Qué es un puntero? / R: Un tipo que se guarda como un entero de tamaño fijo pero almacena el índice en el VAS de un byte concreto, permitiendo referirse a datos de tamaño y complejidad arbitrarios; NULL significa que no apunta a nada.

P: ¿En qué se diferencian pasar por referencia y pasar por valor? / R: Pasar por referencia pasa punteros y los cambios persisten sobre los datos originales; pasar por valor copia la estructura entera. Python siempre pasa por referencia.

P: ¿Cuándo hay que usar el heap en vez del stack? / R: Cuando el tamaño de una estructura no se conoce en tiempo de compilación; se pide con malloc() en ejecución y se libera con free().

P: ¿Qué es un memory leak y qué es la memoria huérfana? / R: Un memory leak es no liberar memoria del heap hasta agotarla y fallar; la memoria huérfana ("orphaned") es memoria reservada sin ningún puntero que la referencie.

P: ¿Cómo logra un array ajustable inserción O(1) amortizado? / R: Reserva más espacio del necesario y, al llenarse, crea uno nuevo (típicamente del doble) y copia; las copias se vuelven el doble de caras pero la mitad de frecuentes, dando coste neto O(1) amortizado.

P: ¿Qué tres propiedades tiene una función hash? / R: Es determinista (misma entrada, misma salida), se calcula en O(1) y "parece aleatoria" (para x distintos casi siempre da resultados distintos).

P: ¿Por qué se dice que todo Python es azúcar sintáctico sobre tablas hash? / R: Porque los diccionarios, el namespace que mapea nombres de variables a objetos y las instancias de clases definidas por el usuario se implementan como tablas hash.

P: ¿Qué ventaja y desventaja tiene una lista enlazada? / R: Ventaja: insertar un elemento (con puntero al sitio) es O(1) puro; desventaja: hallar el elemento i-ésimo es O(i), no O(1).

P: ¿Qué coste tienen la búsqueda y la inserción en un BST equilibrado? / R: O(log(n)), no amortizado, siempre que el árbol esté equilibrado (cada nodo con tantos descendientes a izquierda como a derecha).

P: ¿Cómo se organizan los valores en un árbol binario de búsqueda? / R: Cada nodo tiene valor y dos hijos; los hijos de la derecha tienen valores mayores o iguales y los de la izquierda menores o iguales.

## Preguntas de autoevaluación

P: ¿Por qué el capítulo enseña estos conceptos usando el lenguaje C? / R: Porque C es un lenguaje de bajo nivel con control muy fino de la memoria, y el intérprete principal de Python está escrito en C; ayuda a entender cómo se implementan las estructuras y por qué Python se comporta como lo hace. (Sección: Lo que necesitas saber)

P: ¿Qué ingredientes básicos permiten construir estructuras de datos complejas y eficientes? / R: Los tipos de tamaño fijo, los arrays de ellos y los punteros. (Sección: Lo que necesitas saber / Estructuras de datos clave)

P: ¿Por qué un array de C, a diferencia de guardar los bytes, necesita a veces un contador como n_children o n_chars? / R: Porque en los bytes crudos no hay forma de saber dónde acaba el array, así que hace falta un entero que lleve la cuenta de la longitud. (Secciones: Punteros, el stack y el heap / Estructuras de datos clave)

P: ¿Cómo se almacena un string en C y qué dos formas hay de conocer su longitud? / R: Como un char* (puntero a un array de bytes) en el heap, porque tiene longitud variable; su longitud se sabe envolviéndolo en un struct con un contador n_chars, o con la forma antigua null-terminated (byte 0 al final), más lenta pero que ocupa algo menos de RAM. (Sección: Estructuras de datos clave)

P: ¿Qué ocurre si en una lista enlazada se invierte el orden de las dos asignaciones de la inserción? / R: El nodo apuntaría a sí mismo, creando un bucle infinito y dejando el resto de la lista huérfano; el orden correcto es primero newNode->next = currentNode->next y después currentNode->next = newNode. (Sección: Estructuras de datos clave)

P: ¿Qué es el rehashing y por qué mantiene las inserciones en O(1) amortizado? / R: Cuando la tabla hash se llena se crea una mayor con nueva función hash y se recolocan todos los pares (operación O(n)); si se crece por un factor constante, las inserciones quedan en O(1) amortizado. (Sección: Estructuras de datos clave)

P: ¿Por qué una tabla hash necesita guardar también la clave además del valor? / R: Porque a veces dos claves distintas colisionan (hash(x) = hash(y)), y hay que comparar la clave guardada para resolver la colisión buscando otra celda libre o apuntando a otra estructura. (Sección: Estructuras de datos clave)

## Puntos a dominar

- Explicar qué es el VAS, por qué un proceso debe pedir RAM al sistema operativo y qué provoca un seg fault.
- Razonar por qué el tamaño fijo de los tipos hace que el acceso al elemento i-ésimo de un array sea O(1).
- Relacionar los arrays de C con la eficiencia de NumPy y con la restricción de un único tipo por array.
- Distinguir pasar por referencia de pasar por valor y recordar que Python siempre pasa por referencia.
- Diferenciar stack y heap, y asociar malloc()/free() con la gestión manual de memoria y los memory leaks.
- Comparar los costes de las estructuras clave: array ajustable (O(1) amortizado), lista enlazada (inserción O(1), acceso O(i)), tabla hash (O(1)), BST equilibrado (O(log(n))).
- Explicar por qué los diccionarios, el namespace y las clases de Python se apoyan en tablas hash.
