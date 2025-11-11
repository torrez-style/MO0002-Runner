
"""
1.  Eliminar duplicados de una lista
Dada una lista con elementos repetidos, crea una nueva lista solo con elementos únicos.
"""

#listaDuplicados=["Juan","Lupe","Marcos", "Lupe", "Juan"]
#listaSinDuplicados=[]


#for i in listaDuplicados:
    #if i not in listaSinDuplicados:
        #listaSinDuplicados.append(i)
    
#print(f"Lista sin duplicados:\n{listaSinDuplicados}")
        



"""

2.  Invertir una lista sin usar métodos

Dada una lista, crea otra nueva con los mismos elementos en orden inverso, sin usar reverse() ni slicing.
"""
#lista=["Anna", 0, "Alberth", "A", "Luis", "Wen"]
#inversa=[]


#for i in range(len(lista)-1,-1,-1):
    #inversa.append(lista[i])
#print(f"Lista invertida:\n{inversa}")
        
    



"""
3.  Contar cuántas veces aparece cada elemento

Dada una lista de palabras, muestra cuántas veces aparece cada palabra usando un diccionario y bucles.

"""
#palabras=["Carro","Carro","Carro", "Moto","Moto", "Vector","Vector","Vector", "Derivada", "Integral"]

#contador={}

#for p in palabras:
    #if p in contador:
        #contador[p]+=1
        
    #else:
        #contador[p]=1
        
#print(f"La cantidad de palabras es:\n{contador}")


"""

4.  Sumar los valores en posiciones pares y en posiciones impares

Dada una lista numérica, calcula la suma de los elementos en índices pares y la suma de los de índices impares, por separado.
"""
#numeros=[1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100]

#suma_pares=0
#suma_impares=0


#for i in range(len(numeros)):
    #if i%2==0:
        #suma_pares += numeros[i]
        
    #else:
        #suma_impares +=numeros[i]

#print(f"La suma de los indisces pares es: {suma_pares}")
#print(f"La suma de los indisces impares es: {suma_impares}")



"""
5.  Filtrar y crear lista de números mayores a un valor dado por el usuario

Solicita al usuario un número y crea una lista con los elementos mayores a ese valor.
"""

#numeros=[12,40,20,1,2,5,6,7,8,100,76]

#x=int(input("Introduzca un númeo valido:    "))
#mayores=[]

#for n in numeros:
    #if n>x:
        #mayores.append(n)
#print(f"Los números mayores a: {x} son: {mayores}")
        
    


"""

6.  Obtener el segundo elemento más grande de una lista

Dada una lista de enteros, encuentra el segundo mayor sin ordenar la lista.

"""
#numeros=[10,4,8,1,30,28,49,29,0]

#mayor=numeros[0]


#for n in numeros:
    #if n > mayor:
        #mayor =n 
        
#segundo_mayor=None 

#for n in numeros:
    #if n != mayor:
        #if segundo_mayor is None or n > segundo_mayor:
            #segundo_mayor = n
            
#print(f"El elemento mayor es: {mayor}")
#print(f"El segundo elemento mayor es: {segundo_mayor}")
"""


7.  Crear una lista con la suma de dos listas

Dadas dos listas de números del mismo tamaño, crea una lista con la suma de los elementos en posiciones correspondientes.
"""

#lista1=[1,2,3,4]
#lista2=[10,20,30,40]
#suma=[]


#for i in range(len(lista1)):
    #suma.append(lista1[i] + lista2[i])
    
#print(suma)



"""
8.  Todas las cadenas en mayúsculas

Dada una lista de palabras, recorre la lista y crea una nueva con todas las palabras en mayúsculas.
"""
#palabras=["sol", "luna", "estrellas", "galaxia"]
#ayusculas=[]

#for p in palabras:
    #mayusculas.append(p.upper())
#print(mayusculas)



"""
9.  Eliminar todos los elementos que contengan una vocal específica

Dada una lista de palabras y una vocal dada por el usuario, crea una nueva lista excluyendo las palabras que contengan esa vocal.
"""

#palabras=["palabras", "minuscula", "mayuscula", "derivada", "integral", "verctor"]


#vocal= input("Ingrese la vocal que desea filtrar.   ").lower()

#sin_vocal=[]


#for p in palabras:
    #if vocal not in p: 
        #sin_vocal.append(p)

#print(f"Lista sin palabras que contienen la vocal:  {vocal}")
#print(sin_vocal)


""""
10. Encontrar el índice de todos los elementos iguales a un valor dado

Dada una lista y un valor solicitado al usuario, encuentra y muestra los índices en los que aparece ese valor.

"""

#lista=["agua", "amor", "solo", "gladiador", "pájaro", "carro", "luna", "ferroso"]
#valor= input("Introduzca el valor a buscar:     ")

#indices=[]

#for i in range(len(lista)):
    #if lista[i]==valor:
        #indices.append(i)
        
#print(f"El valor {valor} aparece en los índices: ", indices)