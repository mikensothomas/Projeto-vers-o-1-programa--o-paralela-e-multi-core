
import socket

def servidor(host = 'localhost', port = 5000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    sock.bind(server_address)
    sock.listen()

    print("O servidor está conectado no %s e na porta %s" % server_address)
    print("Esperando a conexão com clientes...")
    client, address = sock.accept()
    print("Conectado com um cliente", address)

    try:
        while True:
            data = client.recv(1024)

            if data:
                print("Mensagem recebida do cliente: ", data.decode('utf-8'))
                message = input("Digite sua mensagem: ")
                client.sendall(message.encode('utf-8'))
                print("Mensagem enviada com sucesso")
            else:
                break
    finally:
        client.close()

servidor()