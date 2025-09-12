import socket

def start_server(host='0.0.0.0', port=5001):
    server_name = "Server of Rajit"  
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server started at {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        print(f"Connection from {addr}")

        data = conn.recv(1024).decode()
        if not data:
            break
        
        client_name, client_number = data.split(',')
        client_number = int(client_number)
        
        print(f"Client Name: {client_name}")
        print(f"Client Number: {client_number}")
      
        if client_number < 1 or client_number > 100:
            print("Number out of range. Closing server.")
            conn.close()
            break
        
        server_number = 42  
        total_sum = client_number + server_number
        
        print(f"Server Name: {server_name}")
        print(f"Server Number: {server_number}")
        print(f"Sum: {total_sum}")
        conn.send(f"{server_name},{server_number}".encode())
        conn.close()

    server_socket.close()

if __name__ == "__main__":
    start_server()
