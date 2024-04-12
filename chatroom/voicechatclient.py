import socket
import pyaudio
import threading

# Create a new socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('125.59.219.35', 8766))  # Replace 'server_ip' with the IP address of the server

# Set up PyAudio
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, output=True, frames_per_buffer=1024)

# Function to handle receiving data from the server
def receive_data():
    while True:
        try:
            data = s.recv(1024)
            if not data:
                break
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
            if not stream.is_stopped():
                data = stream.read(1024)
                s.sendall(data)
            else:
                break
        except (ConnectionAbortedError, ConnectionResetError):
            print("Connection was closed by the server.")
            break
except KeyboardInterrupt:
    print("Stopped recording.")

# Clean up
stream.stop_stream()
stream.close()
p.terminate()
s.close()