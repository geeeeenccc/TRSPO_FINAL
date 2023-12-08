import socket
import threading
from concurrent.futures import ThreadPoolExecutor
import numpy as np


def handle_client(client_socket):
    # Отримуємо розміри та елементи матриць від клієнта
    matrix_sizes = client_socket.recv(1024).decode()
    rows_a, cols_a, rows_b, cols_b = map(int, matrix_sizes.split(','))

    matrix_a = np.frombuffer(client_socket.recv(rows_a * cols_a * 8), dtype=np.float64).reshape((rows_a, cols_a))
    matrix_b = np.frombuffer(client_socket.recv(rows_b * cols_b * 8), dtype=np.float64).reshape((rows_b, cols_b))

    # Обчислюємо результати перемноження матриць
    result_matrix = np.dot(matrix_a, matrix_b)

    # Надсилаємо результати клієнту
    client_socket.send(result_matrix.tobytes())
    client_socket.close()


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8888))
    server.listen(5)
    print('[Server] Listening on port 8888...')

    with ThreadPoolExecutor(max_workers=5) as executor:
        while True:
            client, addr = server.accept()
            print(f'[Server] Accepted connection from {addr}')
            executor.submit(handle_client, client)


if __name__ == "__main__":
    start_server()
