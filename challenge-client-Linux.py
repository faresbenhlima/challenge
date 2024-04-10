import socket
import sys

# The path to the Unix socket
socket_path = "/tmp/challenge-server.sock"

try:
    # Create a Unix socket
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    # Connect the socket to the port where the server is listening
    sock.connect(socket_path)

    # Send data
    message = sys.argv[1]
    print(f"Sending '{message}'")
    sock.sendall(message.encode())

    # Look for the response
    amount_received = 0
    amount_expected = len(message)
    
    while amount_received < amount_expected:
        data = sock.recv(16)
        amount_received += len(data)
        print("Received:", data.decode())

finally:
    print("Closing socket")
    sock.close()
