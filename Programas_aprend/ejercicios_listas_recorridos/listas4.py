"""
1. Cuadrados y cubos
Dada una lista de 10 números, imprime cada número, su cuadrado y su cubo.

"""

#numeros = [1,2,3,4,5,6,7,8,9,10]

#cuadrado = []
#cubo = []


#for n in numeros:
    
    #cuadrado.append(n**2)
    #cubo.append(n**3)
    
    #print("\n")
    #print(f"Número: {n}, cuadrado: {n**2}, cubo: {n**3}")
#print("\n")
#print("Lista de cuadrados:  ", cuadrado)
#print("\n")
#print("Lista de cubos:  ", cubo)
#print("\n")


"""
2. Filtro: mayores a un valor
Dada una lista de números, pide al usuario un valor y muestra solo los elementos de la lista que son mayores que ese valor.

"""
                            #opción básica: 

#lista = [12, 35, 56, 7 , 8, 0, 90, 1, 2,3, 4, 3, 34, 67, 78]

#valor = int(input("Ingrese un número:   "))

#for n in lista:
    #if valor < n:
        #print(n)
        
        
#numeros = [12, 45, 56, 78, 89, 1, 2, 3,5, 67, 87, 90, 21,24, 557,0]
#valor = int(input("Ingrese un valor:    "))

#mayores = []

#for n in numeros:
    #if n > valor:
        #mayores.append(n)
        
#print(f"Numeros mayores a: {valor}\n",mayores)


"""
3. Eliminar todos los repetidos
Dada una lista con números repetidos, crea una nueva lista solo con los valores únicos (sin usar set()).

"""

#umeros = [1,2,3,4,5,6,1,2,35,1,2,3,6,7,929,1,3,111111,33,33,4,2,5,578,832,24521,11,15]


#unicos = []

#for n in numeros:
    #if n not in unicos:
        #unicos.append(n)
        
#print("Lista de numeros repetidos:")
#print(numeros)
#print("\n")
#print("Lista de numeros sin repetidos: ")
#print(unicos)



"""
4. Suma condicional
Suma todos los números de una lista que estén entre 5 y 15 (inclusive) y muestra el total.

"""


#lista = [1, 24, 5, 34, 8, 9, 15, 30, 10, 12]

#suma = 0

#for n in lista:
    #if 5 <= n <=15:
        #suma += n
#print(suma)


"""
5. Lista al revés con copy
Dada una lista, crea una nueva lista que contenga los mismos elementos pero en orden inverso (sin usar .reverse()).
"""

#lista = ["Anna", "Juana", "María", "José", "Java"]

#inverso = []

#for n in lista[::-1]:
    
    #inverso.append(n)

#print(inverso)

"""
6. Buscar elemento
Pide al usuario un número y verifica si ese número está en la lista. Imprime su posición (índice) si lo encuentras, o un mensaje si no está.

"""

lista = [1,2,3,4,5,6,7,8,9,10]

buscar = int(input("\nIngrese un número:    "))

encontrado = False

for n in range(len(lista)): 
    
    if lista[n] == buscar:
        