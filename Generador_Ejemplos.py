import random
import os

def generar_lista_aleatoria(n):
    """
    Genera una lista de n números aleatorios únicos entre 1 y 1,000,000.
    """
    if n > 1000000:
        raise ValueError("El tamaño máximo permitido es 1,000,000 números únicos.")
    
    # Creamos un conjunto para garantizar unicidad
    numeros_unicos = set()

    while len(numeros_unicos) < n:
        numero_aleatorio = random.randint(1, 100000000)
        numeros_unicos.add(numero_aleatorio)

    # Retornamos la lista de números únicos
    return list(numeros_unicos)

def guardar(lista, nombre_archivo):
    """
    Guarda una lista de números en un archivo de texto.
    """
    with open(nombre_archivo, 'w') as archivo:
        for numero in lista:
            archivo.write(f"{numero}\n")

def leer(nombre_archivo):
    """
    Lee números desde un archivo de texto y los retorna como una lista.
    """
    lista_numeros = []
    with open(nombre_archivo, 'r') as archivo:
        for linea in archivo:
            lista_numeros.append(int(linea.strip()))
    return lista_numeros

def generar_nombre_archivo(carpeta, prefijo="numeros"):
    """
    Genera un nombre único para un archivo, basado en un prefijo y un contador.
    """
    contador = 1
    while True:
        nombre_archivo = f"{carpeta}/{prefijo}_{contador}.txt"
        if not os.path.exists(nombre_archivo):
            return nombre_archivo
        contador += 1

def asegurarse_carpeta_existe(carpeta):
    """
    Crea la carpeta si no existe.
    """
    if not os.path.exists(carpeta):
        os.makedirs(carpeta)

if __name__ == "__main__":
    # Pedir al usuario el número de elementos
    numero = int(input("Ingrese la cantidad de números aleatorios (máximo 1,000,000): "))
    
    try:
        # Generar lista aleatoria
        lista_aleatoria = generar_lista_aleatoria(numero)
        
        # Asegurarse de que la carpeta LAB3DATOS2 exista
        carpeta = "LAB3DATOS2"
        asegurarse_carpeta_existe(carpeta)

        # Generar nombre de archivo único
        nombre_archivo = generar_nombre_archivo(carpeta)

        # Guardar la lista en el archivo
        guardar(lista_aleatoria, nombre_archivo)

        print(f"Archivo generado: {nombre_archivo}")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
