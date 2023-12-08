import socket
import threading
from concurrent.futures import ThreadPoolExecutor
import numpy as np

# Функція для отримання розмірів матриць від клієнта
def receive_matrix_sizes(client_socket):
    matrix_sizes = client_socket.recv(1024).decode().split(',')
    return map(int, matrix_sizes)


# Функція для отримання матриць від клієнта
def receive_matrices(client_socket, n, m, l):
    matrix_a_data = client_socket.recv(n * m * 4)
    matrix_b_data = client_socket.recv(m * l * 4)

    if len(matrix_a_data) != n * m * 4 or len(matrix_b_data) != m * l * 4:
        raise ValueError("Отримано неправильні дані матриць")

    matrix_a = np.frombuffer(matrix_a_data, dtype=int).reshape(n, m)
    matrix_b = np.frombuffer(matrix_b_data, dtype=int).reshape(m, l)

    return matrix_a, matrix_b


# Функція для множення матриць
def multiply_matrices(matrix_a, matrix_b):
    with ThreadPoolExecutor(max_workers=1) as executor:
        result_matrix = executor.submit(np.dot, matrix_a, matrix_b).result()
    return result_matrix


# Функція для відправлення результату клієнту
def send_result_matrix(client_socket, result_matrix):
    client_socket.send(result_matrix.tobytes())


# Функція для обробки клієнта
def handle_client(client_socket):
    try:
        # Отримати розміри матриць від клієнта
        matrix_sizes = receive_matrix_sizes(client_socket)
        n, m, l = map(int, matrix_sizes)

        print(f"Від сервера: Отримано розміри матриць: {n} x {m} і {m} x {l}")

        # Перевірка на позитивні розміри матриць
        if n <= 0 or m <= 0 or l <= 0:
            raise ValueError("Розміри матриць повинні бути додатніми цілими числами")

        # Отримати дані матриць від клієнта
        matrix_a, matrix_b = receive_matrices(client_socket, n, m, l)

        print("Від сервера: Отримано матриці:")
        print("Матриця A:")
        print(matrix_a)
        print("Матриця B:")
        print(matrix_b)

        # Виконати множення матриць в окремому потоці
        result_matrix = multiply_matrices(matrix_a, matrix_b)

        print("Надсилаю результат клієнту")
        send_result_matrix(client_socket, result_matrix)
    except ValueError as ve:
        print(f"Від сервера: Помилка: {ve}")
    except Exception as e:
        print(f"Від сервера: Помилка: {e}")
    finally:
        client_socket.close()
        print("Від сервера: З'єднання закрито")


# Функція для запуску сервера
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 8888))
    server.listen(5)
    print("Сервер прослуховує порт 8888...")

    while True:
        client, addr = server.accept()
        print(f"Від сервера: Прийнято з'єднання від {addr}")
        threading.Thread(target=handle_client, args=(client,)).start()


if __name__ == "__main__":
    start_server()
