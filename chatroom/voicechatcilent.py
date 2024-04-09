import socket
import pyaudio


p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 12345))  

print("Client is connected and sending audio...")

try:
    while True:
        data = stream.read(1024) 
        client.sendall(data) 
except KeyboardInterrupt:
    print("Stopped recording.")

stream.stop_stream()
stream.close() 
p.terminate()
client.close()
