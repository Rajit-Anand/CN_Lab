import socket

def start_client(host='127.0.0.1', port=5001):
    client_name = "Client of Vansh"  
    client_number = int(input("Enter an integer between 1 and 100: "))

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    client_socket.send(f"{client_name},{client_number}".encode())

    data = client_socket.recv(1024).decode()
    server_name, server_number = data.split(',')
    server_number = int(server_number)

    
    print(f"Client Name: {client_name}")
    print(f"Client Number: {client_number}")
    print(f"Server Name: {server_name}")
    print(f"Server Number: {server_number}")
    print(f"Sum: {client_number + server_number}")
    
    client_socket.close()

if __name__ == "__main__":
    start_client()

# broadcasting and threading karna hai