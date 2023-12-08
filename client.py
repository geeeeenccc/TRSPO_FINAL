import socket
import numpy as np


def generate_random_matrix(rows, cols):
    return np.random.rand(rows, cols)


def start_client():
    # Генерація та заповнення матриць
    matrix_a = generate_random_matrix(np.random.randint(1000, 2000), np.random.randint(1000, 2000))
    matrix_b = generate_random_matrix(matrix_a.shape[1], np.random.randint(1000, 2000))

    # Встановлення з'єднання з сервером
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 8888))

    # Надсилання розмірів та елементів матриць серверу
    sizes = f"{matrix_a.shape[0]},{matrix_a.shape[1]},{matrix_b.shape[0]},{matrix_b.shape[1]}"
    client.send(sizes.encode())
    client.send(matrix_a.tobytes())
    client.send(matrix_b.tobytes())

    # Отримання та виведення результатів в консоль
    result_matrix = np.frombuffer(client.recv(matrix_a.shape[0] * matrix_b.shape[1] * 8), dtype=np.float64).reshape(
        (matrix_a.shape[0], matrix_b.shape[1]))
    print('[Client] Received result matrix:')
    print(result_matrix)

    client.close()


if __name__ == "__main__":
    start_client()
