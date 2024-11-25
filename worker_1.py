import socket
import pickle
import time
from algorithms import merge_sort, quick_sort, heap_sort
from algorithms_it import heapsort, quicksort_it, mergesort_it

# Configuración del servidor Worker_1
IP_ADDRESS = '192.168.1.6'
PORT = 8082

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


def handle_worker0_connection(worker0_socket):
    try:
        print("Recibiendo datos de Worker_0...")
        data = receive_data(worker0_socket)
        vector = data["vector"]
        algorithm = data["algorithm"]
        user_time_limit = data["time_limit"]
        extra = data["extra"]

        # Validación inicial
        if is_sorted(vector):
            send_data(worker0_socket, {"vector": vector, "completed": True})
            return

        print("Worker_1: Comenzando proceso de ordenamiento...")
        start_time = time.time()
        end_time = start_time + user_time_limit

        while not is_sorted(vector):
            if algorithm == 1:
                extra = mergesort_it(vector, end_time, extra)
            elif algorithm == 2:
                extra = quicksort_it(vector, end_time, extra)
            elif algorithm == 3:
                extra = heapsort(vector, end_time, extra[1])

            if is_sorted(vector):
                print("Worker_1: Vector completamente ordenado.")
                send_data(worker0_socket, {"vector": vector, "extra": extra, "completed": True})
                return 

            if time.time() >= end_time:
                print("Worker_1: Tiempo límite alcanzado. Devolviendo vector parcialmente ordenado a Worker_0.")
                send_data(worker0_socket, {"vector": vector, "extra": extra,  "completed": False})
                return 

    except Exception as e:
        print(f"Error en Worker_1: {e}")
    finally:
        worker0_socket.close()

def start_worker1():
    print(f"Worker_1 escuchando en {IP_ADDRESS}:{PORT}")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP_ADDRESS, PORT))
    server_socket.listen(5)

    while True:
        worker0_socket, _ = server_socket.accept()
        print("Worker_1: Conexión establecida.")
        handle_worker0_connection(worker0_socket)

if __name__ == "__main__":
    start_worker1()
