import asyncio
import socket
import pyaudio
from threading import Thread

# Create a new socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 8766))
s.listen(5)

print("Server is listening...")

# List to store connected clients
clients = []

# Set up PyAudio
p = pyaudio.PyAudio()
device_info = p.get_device_info_by_host_api_device_index(0, 0)

stream = p.open(format=pyaudio.paInt16, 
                channels=2, 
                rate=44100, 
                input=True, 
                output=True, 
                frames_per_buffer=1024, 
                input_device_index=device_info['index'])

def handle_client(client):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # Function to handle receiving data from the client
    async def receive_data():
        while True:
            try:
                data = await loop.sock_recv(client, 1024)
                if not data:
                    break
                # Broadcast the received data to all connected clients
                for c in clients:
                    if c != client:
                        await loop.sock_sendall(c, data)
            except ConnectionResetError:
                if client in clients:
                    clients.remove(client)
                break

    # Function to handle sending data to the client
    async def send_data():
        while True:
            try:
                if not stream.is_stopped():
                    data = stream.read(1024, exception_on_overflow=False)
                    # Broadcast the audio data to all connected clients
                    for c in clients:
                        if c != client:
                            await loop.sock_sendall(c, data)
            except ConnectionResetError:
                if client in clients:
                    clients.remove(client)
                break

    # Start concurrent tasks for receiving and sending data
    receive_task = loop.create_task(receive_data())
    send_task = loop.create_task(send_data())
    loop.run_until_complete(asyncio.wait([receive_task, send_task]))

def main():
    while True:
        client, address = s.accept()
        print(f"Connected with {str(address)}")
        clients.append(client)  # Add the client to the list of connected clients
        Thread(target=handle_client, args=(client,)).start()  # Handle the client in a separate thread

# Run the server
main()
