import socket
import threading
from concurrent.futures import ThreadPoolExecutor
import numpy as np


def receive_matrix_sizes(client_socket):
    matrix_sizes = client_socket.recv(1024).decode().split(',')
    return map(int, matrix_sizes)


def receive_matrices(client_socket, n, m, l):
    matrix_a_data = client_socket.recv(n * m * 8)  # Припускаємо float64 для послідовності
    matrix_b_data = client_socket.recv(m * l * 8)

    if len(matrix_a_data) != n * m * 8 or len(matrix_b_data) != m * l * 8:
        raise ValueError("Отримано неправильні дані матриці")

    matrix_a = np.frombuffer(matrix_a_data, dtype=float).reshape(n, m)
    matrix_b = np.frombuffer(matrix_b_data, dtype=float).reshape(m, l)

    return matrix_a, matrix_b


def multiply_matrices(matrix_a, matrix_b):
    with ThreadPoolExecutor(max_workers=1) as executor:
        result_matrix = executor.submit(np.dot, matrix_a, matrix_b).result()
    return result_matrix


def send_matrix(client_socket, matrix):
    client_socket.send(matrix.tobytes())


def client_handling(client_socket):
    try:
        matrix_sizes = receive_matrix_sizes(client_socket)
        n, m, l = map(int, matrix_sizes)

        if n <= 0 or m <= 0 or l <= 0:
            raise ValueError("Розміри матриць повинні бути додатніми цілими числами")

        matrix_a, matrix_b = receive_matrices(client_socket, n, m, l)

        print("Від сервера: Отримано матриці:")
        print("Матриця A:")
        print(matrix_a)
        print("Матриця B:")
        print(matrix_b)

        result_matrix = multiply_matrices(matrix_a, matrix_b)

        print("Надсилаю результати матриці клієнту")
        send_matrix(client_socket, result_matrix)
    except ValueError as ve:
        print(f"Від сервера: Помилка: {ve}")
    except Exception as e:
        print(f"Від сервера: Помилка: {e}")
    finally:
        client_socket.close()
        print("Від сервера: З'єднання закрито")


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8888 ))
    server.listen(5)
    print("Сервер слухає на порту 8888 ")

    while True:
        client, addr = server.accept()
        print(f"Від сервера: прийнято з'єднання від {addr}")
        threading.Thread(target=client_handling, args=(client,)).start()


if __name__ == "__main__":
    start_server()
