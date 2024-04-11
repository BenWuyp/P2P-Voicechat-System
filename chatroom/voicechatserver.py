import socket
import pyaudio
import threading

# Set up PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, output=True, frames_per_buffer=1024)

# Create a new socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 8765))
s.listen(1)

print("Server is listening...")

# Accept a connection from the client
client, address = s.accept()
print(f"Connected with {str(address)}")

# Function to handle receiving data from the client
def receive_data():
    while True:
        try:
            data = client.recv(1024)
            stream.write(data)
        except:
            break

# Start a new thread for receiving data from the client
receive_thread = threading.Thread(target=receive_data)
receive_thread.start()

print("Server is sending and receiving audio...")

try:
    while True:
        data = stream.read(1024)
        client.sendall(data)
except KeyboardInterrupt:
    print("Stopped recording.")

# Clean up
stream.stop_stream()
stream.close()
p.terminate()
client.close()
