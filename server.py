
import socket

def servidor(host = 'localhost', port = 5000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    sock.bind(server_address)
    sock.listen()

    print("O servidor está conectado no %s e na porta %s" % server_address)
    print("Esperando a conexão com clientes...")

    while True:
        client, address = sock.accept()

        print("Conectado com um cliente", address)

        data = client.recv(1024)
        print("Mensagem recebida do cliente:", data.decode('utf-8'))

        if data:
            message = "Hello client"
            print("Mensagem enviada com sucesso")
            client.sendall(message.encode('utf-8'))

servidor()