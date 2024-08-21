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

            data_escolhida = input(": ")
            sock.sendall(data_escolhida.encode('utf-8'))

            if data_escolhida.strip().lower() == 's':
                resposta = sock.recv(1024)
                print(resposta.decode('utf-8'))
                break

            resposta = sock.recv(1024)
            print(resposta.decode('utf-8'))

    finally:
        sock.close()

cliente()
