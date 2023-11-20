import socket
import threading

def handle_client(client_socket, side_choice, scores):
    print(f"Player on side {side_choice} connected.")

    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        message = data.decode('utf-8')
        print(f"Received data from Player {side_choice}: {message}")

        if message.lower() == 'exit':
            break

        if message.lower() == 'score':
            client_socket.sendall(f"Player A: {scores['A']}    Player B: {scores['B']}".encode('utf-8'))
        else:
            scores[side_choice] += 1
            if scores[side_choice] >= 5:
                client_socket.sendall(f"Player {side_choice} wins! Game over.".encode('utf-8'))
                break
            else:
                client_socket.sendall(b"Point scored. Keep playing!")

    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 8888))
    server.listen(5)
    print("Server listening on port 8888")

    scores = {'A': 0, 'B': 0}

    while True:
        client, addr = server.accept()
        side_choice = client.recv(1024).decode('utf-8')

        client_handler = threading.Thread(target=handle_client, args=(client, side_choice, scores))
        client_handler.start()

if __name__ == "__main__":
    start_server()


