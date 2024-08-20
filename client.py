import socket

def cliente(host='localhost', port=5000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    sock.connect(server_address)

    try:
        data = sock.recv(1024)
        print(data.decode('utf-8'))

        client_name = input("Digite seu nome: ")
        sock.sendall(client_name.encode('utf-8'))
        print("Conectado com o servidor no %s na porta %s" % server_address)

        while True:
            menu = sock.recv(1024).decode('utf-8')
            print(menu)

            choice = input("Escolha uma opção: ")
            sock.sendall(choice.encode('utf-8'))

            data = sock.recv(1024)
            if data:
                print("Mensagem do servidor:", data.decode('utf-8'))
            else:
                break
    finally:
        sock.close()

cliente()