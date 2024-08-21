import socket
import threading

def handle_client(client, address):
    try:
        client.sendall("Por favor, insira seu nome no campo embaixo ".encode('utf-8'))
        client_name = client.recv(1024).decode('utf-8')
        print("\n")
        print(f"Conectado com {client_name} do endereço {address}")

        datas_de_viagens = [
            "20/08/2024",
            "22/08/2024",
            "25/08/2024",
            "30/08/2024"
        ]

        while True:
            menu_message = "\nMenu:\n1. Buscar passagens \n2. Fechar conexão \n"
            client.sendall(menu_message.encode('utf-8'))

            data = client.recv(1024)

            if data:
                opcao = data.decode('utf-8')
                print(f"Mensagem recebida de {client_name}: ", opcao)
                
                if opcao == '1':
                    viagens_disponiveis = "Datas de viagens disponíveis:\n" + "\n".join(datas_de_viagens)
                    client.sendall(viagens_disponiveis.encode('utf-8'))
                    print(f"Enviei para {client_name} as datas de viagens disponíveis.")
                
                elif opcao == '2':
                    print(f"{client_name} desconectado")
                    break
                
                print("Aguarda")
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