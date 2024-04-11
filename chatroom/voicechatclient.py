import socket
import pyaudio
import threading

# Set up PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, output=True, frames_per_buffer=1024)

# Create a new client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('125.59.219.35', 8766))

print("Client is connected...")

# Function to handle receiving data from the server
def receive_data():
    while True:
        try:
            data = client.recv(1024)
            stream.write(data)
        except:
            break

# Start a new thread for receiving data from the server
receive_thread = threading.Thread(target=receive_data)
receive_thread.start()

print("Client is sending and receiving audio...")

try:
    while True:
        try:
            data = stream.read(1024)
            client.sendall(data)
        except (ConnectionAbortedError, ConnectionResetError):
            print("Connection was closed by the server.")
            break
except KeyboardInterrupt:
    print("Stopped recording.")

# Clean up
stream.stop_stream()
stream.close()
p.terminate()
client.close()
