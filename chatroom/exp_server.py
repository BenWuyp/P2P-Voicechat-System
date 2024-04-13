import pyaudio
import socket

# Constants
CHUNK = 1024  # Number of audio samples per frame
FORMAT = pyaudio.paInt16  # Audio format (16-bit signed integers)
CHANNELS = 1  # Mono audio
RATE = 44100  # Sampling rate (samples per second)
SERVER_IP = '0.0.0.0'
SERVER_PORT = 8765

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((SERVER_IP, SERVER_PORT))
sock.listen(5)

# Accept client connection
print("Waiting for client connection...")
conn, addr = sock.accept()
print("Client connected:", addr)

# Open speaker stream
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    output=True,
                    frames_per_buffer=CHUNK)

# Receive audio data and play through the speaker
while True:
    data = conn.recv(CHUNK)
    stream.write(data)

# Cleanup
stream.stop_stream()
stream.close()
audio.terminate()
sock.close()
