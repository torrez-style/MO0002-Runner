"""
1. Crea una lista de números y muestra solo los elementos impares recorriéndola con un bucle.

"""

#numeros = [12, 23, 18, 34, 56, 67, 7, 10, 4, 29, 94, 29, 3535, 21, 345,6, 7, 909,1]

#impares = []

#for i in numeros:
    #if i % 2 !=0:
        #impares. append(i)
        
#print(impares)


"""
2. Dada una lista de cadenas, imprime las palabras que tienen más de 5 letras.

"""

#palabras = ["uno", "dos", "tres", "cuatro", "cinco", "seis", "siente", "ocho", "Torrez", "Manyel", "Melanie", "Prisilla"]

#for p in palabras:
    #if len (p) > 5:
        #print(p)
        

"""
3. Recorre una lista de números y multiplica por 3 cada uno, formando una nueva lista, luego imprímela.

"""


#numeros = [1,2,3,4,5,6,7,8,9,10]
#multiplicacion = []


#for n in numeros:
    #multiplicacion.append(n*3)

#print(multiplicacion)

"""
4. Dada una lista de temperaturas (números flotantes), cuenta cuántas son mayores a 25.


"""


#temperatura = [12.4, 0.24452,13.6,27.4,67.8,56.7]
#contador = 0

#for i in temperatura:
    #if i > 25:
        #contador += 1 
#print(contador)

"""
5. Dada una lista de nombres, imprime uno por uno junto con su posición en la lista (índice).

"""
#lista = ["Juan", "Marcos", "Diego", "Anna", "Luis", "Torrez"]

#for i in range(len(lista)):
    #print(f"índice {i}: {lista[i]}")
    

"""
6. Pide al usuario 5 palabras, guárdalas en una lista y luego recórrela para mostrar las palabras
    en orden inverso.
"""

                #opción 1:

#alabras = []

#for i in range (5):
    #p = input(f"Ingrese la palabra {i + 1}: ")
    #palabras.append(p)
    
#print("\nPalabras en orden inverso: ")
#or p in reversed(palabras):
    #print(p)

                #opción 2:

#palabras = []

#for i in range(5):
    #p = input(f"Ingrese la palabra {i + 1}: ")
    #palabras.append(p)
    
#print("\nPalabras en orden inverso: ")
#for p in palabras [::-1]:
    #print(p)


                #opción 3
                
#palabras = []
#for i in range(5):
    #p = input(f"Ingrese la palabra {i + 1}: ")
    #palabras. append(p)
    
#palabras.reverse()

#print("\nPalabras en orden inverso: ")
#for p in palabras:
    #print(p)
    
"""
7. Dada una lista, suma solo los números negativos y muestra el total.
"""

#lista = [1,0,-2,3.5, -5, -5, -0.2354, 10, 2, -0]
#suma = 0

#for i in lista:
    #if i < 0 :
        #suma += i 
#print(suma )

"""
8.  Dada una lista con palabras y números mezclados, recorre la lista y separa los elementos numéricos en otra lista.

"""

                            #opción 1:
                            

#lista = ["Mango", "Pera", 12, 34, "Uva", 23, "Fresa", 10, "Banana", 2.34353535353521145431]

#numeros = []

#for i in lista:
    #if isinstance (i, (int, float)):
        #numeros.append(i)
        
#print(f"Lista original:\n{lista}")
#print(f"\nSolo números:\n{numeros }")

"""
La función isinstance() se usa para verificar si un objeto es una instancia de una clase o tipo
específico, o bien de una tupla de tipos. Esta función devuelve True si el objeto pertenece (o
hereda de) el tipo indicado y False si no.


¿Por qué utilizar isinstance()?

Flexibilidad: Permite comprobar si un valor pertenece a varios tipos (int, float, str, etc.), 
incluso si el objeto es de una clase derivada (herencia).


Control en tiempo de ejecución: Es útil para crear funciones que admiten múltiples tipos de
datos o para validar el tipo de entrada antes de realizar operaciones específicas.

"""
                            #opción 2:


#lista = ["hola", 12, "we", "you", 23, 45, "uno ", "dos", 3,"tres"]
#numeros = []

#for i in lista:
    #if type(i) in (int, float):
        #numeros.append(i)

#print("Solo numeros:    ", numeros)



"""
La función type() en Python sirve principalmente para determinar el tipo de dato de un objeto.
Es una función incorporada que te devuelve la clase o tipo al que pertenece cualquier valor o
variable que le pases como argumento.


Usos principales de type()
Conocer el tipo de un objeto

La función type() te permite saber si un objeto es un número entero (int), decimal (float),
cadena de texto (str), lista (list), etc. 

"""


"""
9. Dada una lista de palabras, imprime solo aquellas que empiezan con vocal (a, e, i, o, u).

"""

#palabras = ["Elefante", "Casa", "Carro", "Perro", "Oso", "OSs", "Nombre", "Luis", "Uva", "iglesia", "osa" ]
#vocales = ["a", "e", "i", "o", "u"]

#for p in palabras:
    #if p[0].lower() in vocales:
        #print(p)
        


"""
10. Dada una lista de números, recorre e imprime los que están en posiciones pares (índices 0, 2, 4, …).

"""

#numeros = [11, 22, 23, 24, 45, 56, 67, 78, 100]
#for i in range (0, len(numeros), 2):
    #print(numeros[i])
    
    
                    #opciones:
                    
#numeros = [11, 13, 45, 56, 78, 0, 10, 34, 56, 6]

#for i in numeros [::2]:
    #print(i)
    
#En el caso de los impares solo hay que poner 
#for i in range (1, len (numeros), 2): 