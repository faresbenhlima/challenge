import socket
import subprocess
import os
import logging

# Setup basic logging
logging.basicConfig(filename='challenge-server.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

# Then, replace print statements with logging.info or appropriate logging level
# For example:
logging.info("Waiting for a connection...")
# The path to the Unix socket
socket_path = "/tmp/challenge-server.sock"

# Make sure the socket does not already exist
try:
    os.unlink(socket_path)
except OSError:
    if os.path.exists(socket_path):
        raise

# Create a Unix socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Bind the socket to the path
sock.bind(socket_path)

# Listen for incoming connections
sock.listen(1)

while True:
    print("Waiting for a connection...")
    connection, client_address = sock.accept()
    try:
        print("Connection from", client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(16)
            if data:
                print("Received '{}'".format(data.decode()))

                # Call CoAP client here with the received query parameter
                # This is a placeholder for calling the CoAP client.
                # You might need to use a subprocess or a CoAP library in Python
                coap_response = subprocess.run(["coap-client", "-m", "get", f"coap://coap.me/query?{data.decode()}"], capture_output=True)

                print(f"CoAP Response: {coap_response.stdout.decode()}")
                
                # Send data back to the client
                connection.sendall(coap_response.stdout)
            else:
                print("No more data from", client_address)
                break
    finally:
        # Clean up the connection
        connection.close()
