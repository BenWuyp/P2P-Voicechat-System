import socket
import pyaudio
import threading

# Create a new socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 8766))
s.listen(1)

print("Server is listening...")

def handle_client(client):
    # Set up PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, output=True, frames_per_buffer=1024)

    # Function to handle receiving data from the client
    def receive_data():
        while True:
            try:
                data = client.recv(1024)
                if not data:
                    break
                stream.write(data)
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
                    client.sendall(data)
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
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()