import socket
import threading

assentos_disponiveis_por_data = {
    "20/08/2024": ["1A", "1B", "1C", "2A", "2B", "2C", "3A", "3B", "3C"],
    "22/08/2024": ["1A", "1B", "1C", "2A", "2B", "2C", "3A", "3B", "3C"],
    "25/08/2024": ["1A", "1B", "1C", "2A", "2B", "2C", "3A", "3B", "3C"],
    "27/08/2024": ["1A", "1B", "1C", "2A", "2B", "2C", "3A", "3B", "3C"],
    "29/08/2024": ["1A", "1B", "1C", "2A", "2B", "2C", "3A", "3B", "3C"],
    "01/09/2024": ["1A", "1B", "1C", "2A", "2B", "2C", "3A", "3B", "3C"],
    "03/09/2024": ["1A", "1B", "1C", "2A", "2B", "2C", "3A", "3B", "3C"]
}

bloqueio = threading.Lock()
servidor_rodando = True

def manipular_cliente(client, address):
    try:
        client_name = client.recv(1024).decode('utf-8')
        print(f"\nConectado com {client_name} do endereço {address}")

        while True:
            with bloqueio:
                datas_de_viagens = [data for data, assentos in assentos_disponiveis_por_data.items() if assentos]

            viagens_disponiveis = "\nDatas de viagens disponíveis:\n" + "\n".join(datas_de_viagens)
            client.sendall(viagens_disponiveis.encode('utf-8'))

            escolha_do_cliente = client.recv(1024).decode('utf-8').strip()

            if escolha_do_cliente.lower() == 's':
                print(f"{client_name} fechou a conexão.")
                client.sendall("\nConexão encerrada.".encode('utf-8'))
                break

            print(f"{client_name} escolheu a data: {escolha_do_cliente}")

            if escolha_do_cliente in datas_de_viagens:
                client.sendall(f"A data escolhida é {escolha_do_cliente}".encode('utf-8'))

                while True:
                    with bloqueio:
                        assentos_disponiveis = assentos_disponiveis_por_data.get(escolha_do_cliente, [])

                    assentos_message = f"\nAssentos disponíveis para a data {escolha_do_cliente}:\n" + ", ".join(assentos_disponiveis)
                    client.sendall(assentos_message.encode('utf-8'))

                    assento_escolhido = client.recv(1024).decode('utf-8').strip().upper()

                    if assento_escolhido == 'S':
                        print(f"{client_name} fechou a conexão durante a escolha do assento.")
                        client.sendall("Conexão encerrada.".encode('utf-8'))
                        break

                    if assento_escolhido in assentos_disponiveis:
                        with bloqueio:
                            assentos_disponiveis_por_data[escolha_do_cliente].remove(assento_escolhido)

                            if not assentos_disponiveis_por_data[escolha_do_cliente]:
                                del assentos_disponiveis_por_data[escolha_do_cliente]
                        
                        client.sendall(f"Assento {assento_escolhido} reservado com sucesso!".encode('utf-8'))
                        client.sendall("Viagem confirmada! Obrigado por escolher nossos serviços.".encode('utf-8'))
                        print(f"{client_name} reservou o assento {assento_escolhido} para a data {escolha_do_cliente}.")
                        
                        comprovante = f"""
                        Comprovante de viagem:
                        Nome do cliente: {client_name}
                        Data da viagem: {escolha_do_cliente}
                        Assento: {assento_escolhido}
                        """.strip()
                        client.sendall(comprovante.encode('utf-8'))

                        opcao_final = client.recv(1024).decode('utf-8').strip().lower()
                        if opcao_final == 's':
                            client.sendall("Conexão encerrada.".encode('utf-8'))
                            break
                    else:
                        client.sendall(f"Assento {assento_escolhido} não está disponível. Por favor, escolha outro ou 's' para sair.".encode('utf-8'))
                break
            else:
                client.sendall(f"Desculpe, a data {escolha_do_cliente} não está disponível.".encode('utf-8'))

    finally:
        client.close()

def servidor(host='localhost', port=8080):
    global servidor_rodando
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    sock.bind(server_address)
    sock.listen()

    print(f"O servidor está conectado no {server_address[0]} na porta {server_address[1]}")
    print("Esperando a conexão com clientes...")
    print("\n")

    while servidor_rodando:

        client, address = sock.accept()
        thread = threading.Thread(target=manipular_cliente, args=(client, address))
        thread.start()

servidor()