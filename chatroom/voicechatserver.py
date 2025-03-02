import socket
import pyaudio
import threading

# Create a new socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 8766))
s.listen(5)

print("Server is listening...")

# List to store connected clients
clients = []

def handle_client(client):
    # Set up PyAudio
    # Set up PyAudio with ASIO
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, output=True, frames_per_buffer=1024, input_device_index=p.get_device_info_by_host_api_device_index(0, 0)['index'])


    # Function to handle receiving data from the client
    def receive_data():
        while True:
            try:
                data = client.recv(1024)
                if not data:
                    break
                # Broadcast the received data to all connected clients
                for c in clients:
                    if c != client:
                        c.sendall(data)
            except:
                break

    # Start a new thread for receiving data from the client
    receive_thread = threading.Thread(target=receive_data)
    receive_thread.start()

    print("Server is sending and receiving audio...")

    try:
        while True:
            try:
                if not stream.is_stopped():
                    data = stream.read(1024)
                    # Broadcast the audio data to all connected clients
                    for c in clients:
                            c.sendall(data)
                else:
                    break
            except (ConnectionAbortedError, ConnectionResetError):
                print("Connection was closed by the client.")
                break
    except KeyboardInterrupt:
        print("Stopped recording.")

    # Clean up
    stream.stop_stream()
    stream.close()
    p.terminate()
    client.close()

while True:
    # Accept a connection from the client
    client, address = s.accept()
    print(f"Connected with {str(address)}")
    clients.append(client)  # Add the client to the list of connected clients
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()
