import time
def quicksort_it(arr, tiempo_limite, stack):

    # Mientras haya subarrays en la pila
    while stack:
        # Verificar si se ha excedido el tiempo límite
        if time.time() > tiempo_limite:
            return stack  # Retornar False si se ha excedido el tiempo
        
        inicio, fin = stack.pop()
        
        if inicio < fin:
            # Particionar el array
            p = particionar(arr, inicio, fin)
            
            # Agregar los subarrays a la pila
            stack.append((inicio, p - 1))
            stack.append((p + 1, fin))
    
    return []  # Retornar True si se ha completado la ordenación dentro del tiempo

def particionar(arr, inicio, fin):
    pivote = arr[fin]
    i = inicio - 1
    for j in range(inicio, fin):
        if arr[j] <= pivote:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[fin] = arr[fin], arr[i + 1]
    return i + 1

def heapify(arr, n, i, tiempo_limite):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and arr[left] > arr[largest]:
        largest = left

    if right < n and arr[right] > arr[largest]:
        largest = right

    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        # Verificar si se ha excedido el tiempo límite
        if time.time() > tiempo_limite:
            return False  # Retornar False si se ha excedido el tiempo
        if not heapify(arr, n, largest, tiempo_limite):
            return False

    return True

def heapsort(arr, tiempo_limite, n):
    # Construir el heap (reorganizar el array)
    for i in range(n // 2 - 1, -1, -1):
        if time.time() > tiempo_limite:
            return False, n  # Retornar False si se ha excedido el tiempo
        if not heapify(arr, n, i, tiempo_limite):
            return False, n
    # Uno por uno extraer los elementos
    for i in range(n - 1, 0, -1):
        # Verificar si se ha excedido el tiempo límite
        if time.time() > tiempo_limite:
            return False, i+1  

        arr[i], arr[0] = arr[0], arr[i]  # Mover el root actual al final
        if not heapify(arr, i, 0, tiempo_limite):
            return False, i
    return True, 0


def mergesort_it(arr, time_limit, extra):
    loaded = True
    if len(arr) <= 1:
        return None
    curr_size = extra[0]
    n = len(arr)
    while curr_size < n:
        if loaded:
            loaded = False
            left = extra[1]
        else:
            left = 0
        while left < n:
            if time.time() >= time_limit:
                return curr_size, left
            # Encuentra el índice del elemento medio
            middle = min(left + curr_size - 1, n - 1)
            right = min(left + 2 * curr_size - 1, n - 1)

            # Combina los subarreglos [left..middle] y [middle+1..right]
            merge(arr, left, middle, right)
            left += 2 * curr_size
        curr_size *= 2
    print("termino")
    return curr_size, left

def merge(arr, left, middle, right):

    n1 = middle - left + 1
    n2 = right - middle

    # Crear arreglos temporales
    L = [0] * n1
    R = [0] * n2

    # Copiar datos a los arreglos temporales L[] y R[]
    for i in range(0, n1):
        L[i] = arr[left + i]
    for j in range(0, n2):
        R[j] = arr[middle + 1 + j]

    # Fusionar los arreglos temporales de nuevo en arr[left..right]
    i = 0     # Índice inicial del primer subarreglo
    j = 0     # Índice inicial del segundo subarreglo
    k = left   # Índice inicial del subarreglo fusionado

    while i < n1 and j < n2:
        if L[i] <= R[j]:
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    # Copiar los elementos restantes de L[], si los hay
    while i < n1:
        arr[k] = L[i]
        i += 1
        k += 1

    # Copiar los elementos restantes de R[], si los hay
    while j < n2:
        arr[k] = R[j]
        j += 1
        k += 1

if __name__ == "__main__":
    j = [1,2,3]
    n = len(j) // 2
    print(j[:n], j[n:])
    
    


    


