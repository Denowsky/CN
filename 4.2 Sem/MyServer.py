import socket
import threading
import requests

# Функция для получения местоположения по IP
def get_location(ip):
    response = requests.get(f"https://ipinfo.io/{ip}/json")
    data = response.json()
    location = data.get('loc', 'Местоположение неизвестно')
    return location

# Функция обработки клиента
def handle_client(client_socket):
    # Получение имени клиента
    client_name = client_socket.recv(1024).decode('utf-8')
    
    # Получение IP-адреса клиента
    client_address = client_socket.getpeername()[0]
    
    # Получение местоположения
    location = get_location(client_address)
    
    # Отправка сообщения о подключении
    message = f'Ник подключаемого клиента: {client_name}\nIP-адрес: {client_address}\nМестоположение: {location}\n'
    print(message)
    client_socket.send(message.encode('utf-8'))
    
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        # Здесь вы можете обрабатывать и рассылать сообщения между клиентами
        print(f'{client_name}: {data.decode("utf-8")}')

    client_socket.close()

# Создание сервера
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 55555))
server.listen(5)

print("Сервер готов к приему подключений...")

while True:
    client, addr = server.accept()
    print(f"Принято соединение от {addr[0]}:{addr[1]}")
    
    # Создание нового потока для обработки клиента
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()