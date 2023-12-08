import socket
import numpy as np
import time

def generate_random_matrices():
    # Генерація випадкових розмірів та матриць
    n, m, l = np.random.randint(1000, 2000, size=3)
    matrix_a = np.random.randint(1, 10, size=(n, m))
    matrix_b = np.random.randint(1, 10, size=(m, l))

    print(f"Згенерована матриця клієнтом:")
    print("Матриця A:")
    print(matrix_a)
    print("Матриця B:")
    print(matrix_b)

    return n, m, l, matrix_a, matrix_b

def send_matrices_and_sizes(client, n, m, l, matrix_a, matrix_b):
    # Надсилання розмірів матриць на сервер
    print("Надсилання розмірів матриць на сервер")
    client.send(f"{n},{m},{l}".encode())

    # Надсилання матриць на сервер
    print("Надсилання матриць на сервер")
    client.send(matrix_a.tobytes())
    client.send(matrix_b.tobytes())

def receive_result_matrix(client, n, l):
    result_data = b""
    while True:
        # Отримання результату від сервера
        chunk = client.recv(4096)
        if not chunk:
            time.sleep(0.1)  # Затримка перед закриттям з'єднання
            break
        result_data += chunk

    if len(result_data) == 0:
        print("Сервер закрито")
    else:
        # Виведення отриманої матриці результату
        result_matrix = np.frombuffer(result_data, dtype=int).reshape(n, l)

        print("Отримано результат матриці:")
        print(result_matrix)

def communicate_with_server():
    try:
        # Створення сокету та підключення до сервера
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 8888 ))

        n, m, l, matrix_a, matrix_b = generate_random_matrices()

        send_matrices_and_sizes(client, n, m, l, matrix_a, matrix_b)

        receive_result_matrix(client, n, l)

    finally:
        # Закриття з'єднання
        client.close()
        print("З'єднання закрито")

if __name__ == "__main__":
    communicate_with_server()
