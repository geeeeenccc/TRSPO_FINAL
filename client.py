import socket
import numpy as np
import time


# Функція для генерації розмірів та даних матриць
def generate_matrices():
    n, m, l = np.random.randint(1000, 2000, size=3)
    matrix_a = np.random.randint(1, 10, size=(n, m))
    matrix_b = np.random.randint(1, 10, size=(m, l))
    return n, m, l, matrix_a, matrix_b


# Функція для відправлення розмірів матриць на сервер
def send_matrix_sizes(client, n, m, l):
    print("Надсилання розмірів матриць на сервер")
    client.send(f"{n},{m},{l}".encode())


# Функція для відправлення матриць на сервер
def send_matrices(client, matrix_a, matrix_b):
    print("Надсилання матриць на сервер")
    client.send(matrix_a.tobytes())
    client.send(matrix_b.tobytes())


# Функція для отримання результату від сервера
def receive_result(client, n, l):
    result_data = b""
    while True:
        chunk = client.recv(4096)
        if not chunk:
            time.sleep(0.1)  # Затримка перед закриттям з'єднання
            break
        result_data += chunk

    if len(result_data) == 0:
        print("Сервер закрито")
    else:
        result_matrix = np.frombuffer(result_data, dtype=int).reshape(n, l)

        print("Отримано результат матриці:")
        print(result_matrix)

    client.close()
    print("З'єднання закрито")


# Функція для взаємодії з сервером
def communicate_with_server():
    try:
        # Підключення до сервера
        client = connect_to_server()

        # Згенерувати розміри та дані матриць
        n, m, l, matrix_a, matrix_b = generate_matrices()

        print(f"Згенерована матриця клієнтом:")
        print("Матриця A:")
        print(matrix_a)
        print("Матриця B:")
        print(matrix_b)

        # Відправлення розмірів матриць на сервер
        send_matrix_sizes(client, n, m, l)

        # Відправлення матриць на сервер
        send_matrices(client, matrix_a, matrix_b)

        # Отримання результату від сервера
        receive_result(client, n, l)

    except Exception as e:
        print(f"Помилка при взаємодії з сервером: {e}")


# Функція для підключення до сервера
def connect_to_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 8888))
    return client


if __name__ == "__main__":
    communicate_with_server()
