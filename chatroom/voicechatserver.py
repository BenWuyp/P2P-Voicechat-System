import socket
import pyaudio


p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, output=True)


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 12345)) 
server.listen(1)  

print("Server is listening...")

while True:
    client, address = server.accept()  
    print(f"Connected to {address}")
    
    data = client.recv(1024) 
    while data:
        stream.write(data)  
        data = client.recv(1024)  

    client.close()  
