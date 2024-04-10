import socket
import sys

# Server's address and port
host, port = '127.0.0.1', 65000

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect the socket to the server's address and port
    sock.connect((host, port))

    # Send data
    message = ' '.join(sys.argv[1:])  # Takes the command line arguments and sends them as a single message
    print(f"Sending '{message}'")
    sock.sendall(message.encode())

    # Look for the response
    response = sock.recv(1024)
    print("Received:", response.decode())

finally:
    print("Closing socket")
    sock.close()
