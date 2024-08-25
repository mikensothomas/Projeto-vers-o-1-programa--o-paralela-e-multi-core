import socket

def cliente(host='localhost', port=8080):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    sock.connect(server_address)

    try:
        client_name = input("Digite seu nome: ")
        sock.sendall(client_name.encode('utf-8'))

        while True:
            datas_disponiveis = sock.recv(1024)
            print(datas_disponiveis.decode('utf-8'))

            escolha_do_cliente = input("Digite a data escolhida ou 's' para encerrar a conexão: ")
            sock.sendall(escolha_do_cliente.encode('utf-8'))

            if escolha_do_cliente.strip().lower() == 's':
                resposta = sock.recv(1024)
                print(resposta.decode('utf-8'))
                break

            resposta = sock.recv(1024)
            print(resposta.decode('utf-8'))

            if "confirmada com sucesso" in resposta.decode('utf-8'):
                while True:
                    assentos_disponiveis = sock.recv(1024)
                    print(assentos_disponiveis.decode('utf-8'))

                    assento_escolhido = input("Digite o assento escolhido ou 's' para encerrar a conexão: ")
                    sock.sendall(assento_escolhido.encode('utf-8'))

                    if assento_escolhido.strip().lower() == 's':
                        resposta = sock.recv(1024)
                        print(resposta.decode('utf-8'))
                        break

                    confirmacao_assento = sock.recv(1024)
                    print(confirmacao_assento.decode('utf-8'))

                    confirmacao_final = sock.recv(1024)
                    print(confirmacao_final.decode('utf-8'))

                    comprovante = sock.recv(1024)
                    print(comprovante.decode('utf-8'))

                break

    finally:
        sock.close()

cliente()