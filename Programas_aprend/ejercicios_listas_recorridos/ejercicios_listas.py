#Ejemplos practicos y sencillos de listas

"""
Imprimir todos los elementos de una lista
Crea una lista de 5 nombres y recórrela con un bucle for para imprimir cada nombre.

"""

#lista=["Juan", "Pedro", "Anna", "Wendy", "Marcos"]
#for i in lista:
    #print(i)

"""
Sumar elementos numéricos
Dada una lista de números, recorre la lista y muestra la suma total de sus elementos.
"""

#numeros=[1,2,3,4,5,6]
#contador=0

#for i in numeros:
    #contador+=i
    
#print(f"La suma total es: {contador}")



"""
3.Encontrar el valor máximo
Dada una lista de enteros, recórrela y encuentra el número mayor (sin usar la función max).
"""
#numeros=[12,49,60,99,1,0]
#mayor=numeros[0]
#for i in numeros:
    #if i>mayor:
        #mayor=i
#print(f"El número mayor es: {mayor}")

"""
4.Contar elementos pares
Dada una lista de números, recórrela y cuenta cuántos son pares.
"""
#numeros=[10,40,35,73,45,21,22,10,7]
#contador=0
#for i in numeros:
    #if i%2==0:
        #contador+=1
"cuando usamos contador +=1 contamos, cuando usamos contador +=i sumanos los nuemros contados"
#print(f"En total hay {contador} números pares. ")

"""
5.Buscar un elemento específico
Recibe un elemento por input y verifica si está en una lista determinada, recorriéndola manualmente.
"""

"Esto es lo que salio de mi cabecita y tecnicamente esta bien, pero el detalle es que hay que usar un bucle, o sea for!!!!"
#lista=["Marcos", "Juan", "Ferreto", "Torrez"]

#nom=input("Ingrese el nombre que desea buscar: ")
#if nom in lista:
    #print(f"El nombre: {nom} ha sido encontrado con exito!!!!!")
#else:
    #print("Error de busqueda!!!!")
    
"La ia me dice que:"

#lista=["Marcos", "Juan", "Ferreto", "Torrez"]

#nom=input("Ingrese el nombre que desea buscar: ")

#encontrado=False

#for i in lista:
    #if i ==nom:
        #encontrado=True
        #break
#if encontrado:
    #print(f"El nombre: {nom} ha sido encontrado con exito!!!!!")
#else:
    #print("Error de busqueda!!!!!!!")




"""
6.Duplicar los valores de una lista
Dada una lista de números, crea una nueva lista con el doble de cada valor usando una list comprehension o un bucle.
"""
#numeros=[2,3,4,5,6,7,8,9,10]
#duplicados=[]

#for i in numeros:
    #duplicados.append(i*2)
    
#print(f"Números duplicados:\n{duplicados}")

"""
7.Suma de los elementos en posiciones impares
Dada una lista de números, suma sólo los que están en posiciones (índices) impares.
"""
#numeros=[1,4,6,7,8,9,23,45,6,7,78,9]
#suma=0

#for i in range(1,len(numeros),2): #Empieza en 1 y salta a 2
    #suma+=numeros[i]

#print(f"El resultado de la suma de los elemtos en posición impar es: {suma}")

"""
8.Imprimir los elementos en orden inverso
Dada una lista, recórrela e imprime cada elemento desde el último hasta el primero.
"""
#Usando comprehension 

#lista=["perro", "gato", "zorro", "CoD"]
#for i in reversed(lista):
    #print(f"Lista en orden invertido:\n{i}")
    
#Usando indices negativos

#lista=["Ana", "Marcus", "Juan", "Donovan", "Elena", "Manyel"]

#for i in range(len(lista)-1,-1,-1,): #sin importar los elementos de la lista solo se ponen 3 (-1), solo que acá si controlamos el tamaño 
    #print(f"Los elementos invertidos son:\n{lista[i]}")
    

#Usando slicing(solo para crear la lista invertida)

#lista=["Rojo", "Negro", "Amarillo", "Azul"]

#for i in lista[::-1]:
    
    #print(i)   
    
#Creo que en esto hay un eror con el print, pero me da peresa resolverlo jajajajja
"""

9.Eliminar todos los elementos negativos
Dada una lista de enteros, crea una nueva con sólo los números mayores o iguales a cero.
"""
#lista=[1,-1,2,-2,-3,3,-4,4,-5,5,-6,6,-7,7,-8,8,-9,9,-10,10]
#positivos=[]

#for i in lista:
    #if i >=0:
        #positivos.append(i)
#print (f"Los números enteros positivos son:\n{positivos}")



"""
10.Concatenar dos listas elemento a elemento
Dadas dos listas del mismo tamaño, recórralas y concatenen (como cadenas) los elementos que ocupan la misma posición. Ejemplo: [“a”, “b”] + [“x”, “y”] → [“ax”, “by”]

"""
#Usando comprehesion con un bucle:
#lista1=["a","b","c", "d"]
#lista2=["x", "y", "z","w"]
#cadena=[]

#for i in range(len(lista1)):
    #cadena.append(lista1[i]+lista2[i])
#print(f"Lista combinada:\n{cadena}")

#Solución usando list comprehension
lista1=["a","b","c","d"]
lista2=["x","y","z","w"]

cadena=[lista1[i]+lista2[i] for i in range(len(lista1))]

print(f"Lista combinada:\n{cadena}")


#Usando zip()
#lista1=["a","b","c","d"]
#lista2=["x","y","z","w"]

#cadena=[a+b for a,b in zip(lista1, lista2)]

#print(f"Lista combianda:\n{cadena}")


