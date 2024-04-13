import asyncio
import socket
import pyaudio

# Function to connect to the server
async def connect_to_server():
    loop = asyncio.get_running_loop()
    # Create a new socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    await loop.sock_connect(s, ('125.59.219.35', 8766))  # Replace 'server_address' with the actual server IP

    # Set up PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, output=True, frames_per_buffer=1024)

    # Function to handle receiving data from the server
    async def receive_data():
        while True:
            data = await loop.sock_recv(s, 1024)
            if not data:
                break
            stream.write(data)

    # Function to handle sending data to the server
    async def send_data():
        while True:
            data = stream.read(1024, exception_on_overflow=False)
            await loop.sock_sendall(s, data)

    # Start concurrent tasks for receiving and sending data
    receive_task = loop.create_task(receive_data())
    send_task = loop.create_task(send_data())
    await asyncio.wait([receive_task, send_task])

# Run the client
asyncio.run(connect_to_server())