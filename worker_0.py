import socket
import pickle
import threading
import time
from algorithms import merge_sort, quick_sort, heap_sort
from algorithms_it import heapsort, quicksort_it, mergesort_it

# Configuración del servidor
IP_ADDRESS = '192.168.1.6'  # Usamos localhost
PORT = 8081
WORKER_1_PORT = 8082  # Puerto para comunicación con Worker_1

def send_data(socket, data):
    serialized_data = pickle.dumps(data)
    length = len(serialized_data)
    socket.sendall(length.to_bytes(4, byteorder='big'))
    socket.sendall(serialized_data)

def receive_data(socket):
    length = int.from_bytes(socket.recv(4), byteorder='big')
    data = b''
    while len(data) < length:
        packet = socket.recv(length - len(data))
        if not packet:
            raise Exception("Error: socket connection broken")
        data += packet
    return pickle.loads(data)

def is_sorted(vector):
    return all(vector[i] <= vector[i + 1] for i in range(len(vector) - 1))

def handle_client(client_socket):
    try:
        print("Recibiendo datos del cliente...")  # Log para depurar
        data = receive_data(client_socket)
        algorithm = data["algorithm"]
        vector = data["vector"]
        user_time_limit = data["time_limit"]
        
        if algorithm == 1:
            extra = [1, 0]
        elif algorithm == 2:
            extra = [(0, len(vector) - 1)]
        elif algorithm == 3:
            extra = [False, len(vector)]
        print("Comenzando proceso de ordenamiento...")

        start_time = time.time()
        end_time = start_time + user_time_limit
        while not is_sorted(vector):
            if time.time() >= end_time:
                print("Tiempo límite alcanzado en Worker_0. Enviando al Worker_1...")
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as worker1_socket:
                    worker1_socket.connect((IP_ADDRESS, WORKER_1_PORT))
                    send_data(worker1_socket, {"algorithm": algorithm, "vector": vector, "time_limit": user_time_limit, "extra": extra})

                    # Recibir respuesta del Worker_1
                    response = receive_data(worker1_socket)
                    vector = response["vector"]
                    if response["completed"]:
                        print("Worker_1 devolvió el vector completamente ordenado.")
                        break
                    else:
                        print("Worker_1 no completó el ordenamiento. Retomando trabajo en Worker_0.")
                        extra = response["extra"]
            end_time = time.time() + user_time_limit
            # Ejecutar el algoritmo de ordenamiento en Worker_0
            if algorithm == 1:
                extra = mergesort_it(vector, end_time, extra)
            elif algorithm == 2:
                extra = quicksort_it(vector, end_time, extra)
            elif algorithm == 3:
                extra = heapsort(vector, end_time, extra[1])

        print("Worker_0: Vector completamente ordenado")
        total_time = round(time.time() - start_time, 2)
        response = {"sorted_vector": vector, "time_taken": total_time}
        print(f"Enviando respuesta al cliente: Vector ordenado en {total_time} segundos.")
        send_data(client_socket, response)

    except Exception as e:
        print(f"Error en Worker_0: {e}")
    finally:
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP_ADDRESS, PORT))
    server_socket.listen(5)
    print(f"Worker_0 escuchando en {IP_ADDRESS}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Conexión establecida con {client_address}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()
