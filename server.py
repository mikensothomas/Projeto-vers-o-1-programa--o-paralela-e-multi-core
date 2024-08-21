import socket
import threading

def handle_client(client, address):
    try:
        client.sendall("Por favor, insira seu nome no campo embaixo ".encode('utf-8'))
        client_name = client.recv(1024).decode('utf-8')
        print("\n")
        print(f"Conectado com {client_name} do endereço {address}")

        while True:
            menu_message = "\nMenu:\n1. Buscar passagens \n2. Fechar conexão \n"
            client.sendall(menu_message.encode('utf-8'))

            data = client.recv(1024)

            if data:
                print(f"Mensagem recebida de {client_name}: ", data.decode('utf-8'))
                if data.decode('utf-8') == '2':
                    print(f"{client_name} desconectado")
                    break

                message = input("Digite sua mensagem: ")
                client.sendall(message.encode('utf-8'))
                print("Mensagem enviada com sucesso")
            else:
                break
    finally:
        client.close()

def servidor(host='localhost', port=5000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    sock.bind(server_address)
    sock.listen()

    print(f"O servidor está conectado no {server_address[0]} na porta {server_address[1]}")
    print("Esperando a conexão com clientes...")

    while True:
        client, address = sock.accept()
        thread = threading.Thread(target=handle_client, args=(client, address))
        thread.start()

servidor()