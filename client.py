import os
import sys
import socket
import pickle
from Generador_Ejemplos import guardar, leer

# Configuración del cliente
SERVER_IP_ADDRESS = '192.168.1.6'  # Cambia si el servidor está en otra máquina
SERVER_PORT = 8081

def send_data(socket, data):
    """Envía los datos al servidor en fragmentos."""
    serialized_data = pickle.dumps(data)
    length = len(serialized_data)
    socket.sendall(length.to_bytes(4, byteorder='big'))  # Enviar el tamaño
    socket.sendall(serialized_data)  # Enviar los datos

def receive_data(socket):
    """Recibe los datos del servidor en fragmentos."""
    length = int.from_bytes(socket.recv(4), byteorder='big')
    data = b''
    while len(data) < length:
        packet = socket.recv(length - len(data))
        if not packet:
            raise Exception("Error: socket connection broken")
        data += packet
    return pickle.loads(data)

def seleccionar_archivo_txt(carpeta="LAB3DATOS2"):
    """Busca archivos .txt relevantes en una carpeta específica y permite al usuario seleccionar uno."""
    if not os.path.exists(carpeta):
        print(f"La carpeta {carpeta} no existe.")
        sys.exit(1)

    archivos_txt = [f for f in os.listdir(carpeta) if f.endswith('.txt')]
    if len(archivos_txt) == 0:
        print(f"No se encontraron archivos TXT en la carpeta {carpeta}.")
        sys.exit(1)
    elif len(archivos_txt) == 1:
        print(f"Encontrado un archivo TXT en {carpeta}: {archivos_txt[0]}")
        return os.path.join(carpeta, archivos_txt[0])
    else:
        print(f"Se encontraron múltiples archivos TXT en {carpeta}:")
        for idx, archivo in enumerate(archivos_txt, start=1):
            print(f"{idx}. {archivo}")
        while True:
            try:
                eleccion = int(input("Ingrese el número del archivo que desea usar: "))
                if 1 <= eleccion <= len(archivos_txt):
                    return os.path.join(carpeta, archivos_txt[eleccion - 1])
                else:
                    print("Número inválido. Por favor, elija un número válido.")
            except ValueError:
                print("Entrada no válida. Por favor, ingrese un número.")

def start_client():
    """Inicia el cliente y se conecta al servidor."""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP_ADDRESS, SERVER_PORT))
        print("Conectado al servidor principal (worker_0).")

        archivo_elegido = seleccionar_archivo_txt(carpeta="LAB3DATOS2")
        print(f"Procesando el archivo: {archivo_elegido}")
        vector = leer(archivo_elegido)

        print("Seleccione el algoritmo de ordenamiento:")
        print("1. Mergesort")
        print("2. Quicksort")
        print("3. Heapsort")
        while True:
            try:
                choice = int(input("Ingrese su elección (1-3): "))
                if choice in [1, 2, 3]:
                    break
                else:
                    print("Opción inválida. Por favor, elija un número entre 1 y 3.")
            except ValueError:
                print("Entrada no válida. Por favor, ingrese un número.")

        while True:
            try:
                time_limit = int(input("Ingrese el tiempo límite por worker (en segundos): "))
                if time_limit > 0:
                    break
                else:
                    print("El tiempo debe ser mayor a 0.")
            except ValueError:
                print("Entrada no válida. Por favor, ingrese un número entero positivo.")

        data = {
            "algorithm": choice,
            "vector": vector,
            "time_limit": time_limit
        }
        send_data(client_socket, data)
        print("Esperando respuesta del servidor...")
        response = receive_data(client_socket)

        carpeta_archivo = os.path.dirname(archivo_elegido)
        nombre_archivo_ordenado = os.path.join(carpeta_archivo, "ordenado_final.txt")
        guardar(response["sorted_vector"], nombre_archivo_ordenado)
        print(f"Vector ordenado recibido y guardado en {nombre_archivo_ordenado}.")
        print(f"Tiempo total: {response['time_taken']} segundos")

    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    start_client()
