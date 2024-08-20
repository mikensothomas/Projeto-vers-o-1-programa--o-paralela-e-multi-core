import socket

def servidor(host='localhost', port=5000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    sock.bind(server_address)
    sock.listen()

    print("Esperando a conexão com clientes...")
    client, address = sock.accept()

    try:
        client.sendall("Por favor, insira seu nome no campo embaixo ".encode('utf-8'))
        client_name = client.recv(1024).decode('utf-8')
        print(f"O servidor está conectado no {server_address[0]} na porta {server_address[1]} com o cliente {client_name}")

        while True:
            menu_message = "Menu:\n1. Opção 1\n2. Opção 2\nDigite sua escolha: "
            client.sendall(menu_message.encode('utf-8'))

            data = client.recv(1024)

            if data:
                print(f"Mensagem recebida de {client_name}: ", data.decode('utf-8'))
                message = input("Digite sua mensagem: ")
                client.sendall(message.encode('utf-8'))
                print("Mensagem enviada com sucesso")
            else:
                break
    finally:
        client.close()

servidor()