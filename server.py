import socket
import threading

# Dicionário global de assentos disponíveis por data de viagem
assentos_disponiveis_por_data = {
    "20/08/2024": ["1A", "1B", "1C", "2A", "2B", "2C", "3A", "3B", "3C"],
    "22/08/2024": ["1A", "1B", "1C", "2A", "2B", "2C", "3A", "3B", "3C"],
    "25/08/2024": ["1A", "1B", "1C", "2A", "2B", "2C", "3A", "3B", "3C"],
    "27/08/2024": ["1A", "1B", "1C", "2A", "2B", "2C", "3A", "3B", "3C"],
    "29/08/2024": ["1A", "1B", "1C", "2A", "2B", "2C", "3A", "3B", "3C"],
    "01/09/2024": ["1A", "1B", "1C", "2A", "2B", "2C", "3A", "3B", "3C"],
    "03/09/2024": ["1A", "1B", "1C", "2A", "2B", "2C", "3A", "3B", "3C"]
}

# Criação de um lock para proteger o acesso ao dicionário de assentos
lock = threading.Lock()

def handle_client(client, address):
    try:
        client_name = client.recv(1024).decode('utf-8')
        print(f"Conectado com {client_name} do endereço {address}")

        datas_de_viagens = list(assentos_disponiveis_por_data.keys())

        while True:
            viagens_disponiveis = "Datas de viagens disponíveis:\n" + "\n".join(datas_de_viagens)
            client.sendall(viagens_disponiveis.encode('utf-8'))

            data_escolhida = client.recv(1024).decode('utf-8').strip()

            if data_escolhida.lower() == 's':
                print(f"{client_name} fechou a conexão.")
                client.sendall("Conexão encerrada.".encode('utf-8'))
                break

            print(f"{client_name} escolheu a data: {data_escolhida}")

            if data_escolhida in datas_de_viagens:
                client.sendall(f"Passagem para {data_escolhida} confirmada com sucesso!".encode('utf-8'))

                while True:
                    with lock:
                        # Obtenha a lista de assentos disponíveis para a data escolhida
                        assentos_disponiveis = assentos_disponiveis_por_data.get(data_escolhida, [])

                    if not assentos_disponiveis:
                        client.sendall("Desculpe, não há mais assentos disponíveis para esta data.".encode('utf-8'))
                        break

                    assentos_message = f"Assentos disponíveis para a data {data_escolhida}:\n" + ", ".join(assentos_disponiveis)
                    client.sendall(assentos_message.encode('utf-8'))

                    assento_escolhido = client.recv(1024).decode('utf-8').strip().upper()

                    if assento_escolhido == 'S':
                        print(f"{client_name} fechou a conexão durante a escolha do assento.")
                        client.sendall("Conexão encerrada.".encode('utf-8'))
                        break

                    if assento_escolhido in assentos_disponiveis:
                        with lock:
                            # Remove o assento escolhido para aquela data específica
                            assentos_disponiveis_por_data[data_escolhida].remove(assento_escolhido)
                        
                        client.sendall(f"Assento {assento_escolhido} reservado com sucesso!".encode('utf-8'))
                        client.sendall("Viagem confirmada! Obrigado por escolher nossos serviços.".encode('utf-8'))
                        print(f"{client_name} reservou o assento {assento_escolhido} para a data {data_escolhida}.")
                        break  # Concluímos a reserva, podemos fechar a conexão
                    else:
                        client.sendall(f"Assento {assento_escolhido} não disponível. Por favor, escolha outro ou 's' para sair.".encode('utf-8'))
                break
            else:
                client.sendall(f"Desculpe, a data {data_escolhida} não está disponível.".encode('utf-8'))

    finally:
        client.close()

def servidor(host='localhost', port=8080):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    sock.bind(server_address)
    sock.listen()

    print(f"O servidor está conectado no {server_address[0]} na porta {server_address[1]}")
    print("Esperando a conexão com clientes...")
    print("\n")

    while True:
        client, address = sock.accept()
        thread = threading.Thread(target=handle_client, args=(client, address))
        thread.start()

servidor()
