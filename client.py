
import socket

def cliente(host = 'localhost', port = 5000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)

    print("Conectado com o servidor no %s na porta %s" % server_address)
    sock.connect(server_address)

    try:
        message = input("Digite sua mensagem: ")
        sock.sendall(message.encode('utf-8'))
        print("Mensagem enviado com sucesso")

        data = sock.recv(1024)
        print("Mensagem do servidor: ", data.decode('utf-8'))

    finally:
        sock.close()

cliente()