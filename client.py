import socket

def cliente(host='localhost', port=8080):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    sock.connect(server_address)

    try:
        # Envia o nome do cliente
        client_name = input("Digite seu nome: ")
        sock.sendall(client_name.encode('utf-8'))

        while True:
            # Recebe e imprime as datas de viagens disponíveis
            datas_disponiveis = sock.recv(1024)
            print(datas_disponiveis.decode('utf-8'))

            # Cliente escolhe a data ou opta por sair
            data_escolhida = input("Digite a data escolhida ou 's' para encerrar a conexão: ")
            sock.sendall(data_escolhida.encode('utf-8'))

            if data_escolhida.strip().lower() == 's':
                resposta = sock.recv(1024)
                print(resposta.decode('utf-8'))
                break

            # Recebe a confirmação da data
            resposta = sock.recv(1024)
            print(resposta.decode('utf-8'))

            if "confirmada com sucesso" in resposta.decode('utf-8'):
                while True:
                    # Recebe a lista de assentos disponíveis
                    assentos_disponiveis = sock.recv(1024)
                    print(assentos_disponiveis.decode('utf-8'))

                    # Cliente escolhe um assento
                    assento_escolhido = input("Digite o assento escolhido ou 's' para encerrar a conexão: ")
                    sock.sendall(assento_escolhido.encode('utf-8'))

                    if assento_escolhido.strip().lower() == 's':
                        resposta = sock.recv(1024)
                        print(resposta.decode('utf-8'))
                        break

                    # Recebe a confirmação da reserva do assento
                    confirmacao_assento = sock.recv(1024)
                    print(confirmacao_assento.decode('utf-8'))

                    # Recebe a mensagem final de confirmação da viagem
                    confirmacao_final = sock.recv(1024)
                    print(confirmacao_final.decode('utf-8'))
                    break
                break

    finally:
        sock.close()

cliente()