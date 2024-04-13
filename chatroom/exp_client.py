import pyaudio
import socket

# Constants
CHUNK = 1024  # Number of audio samples per frame
FORMAT = pyaudio.paInt16  # Audio format (16-bit signed integers)
CHANNELS = 1  # Mono audio
RATE = 44100  # Sampling rate (samples per second)
SERVER_IP = '125.59.219.35'
SERVER_PORT = 8765

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Create socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER_IP, SERVER_PORT))

# Open microphone stream
stream = audio.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

# Read audio from microphone and send to the server
while True:
    data = stream.read(CHUNK)
    sock.sendall(data)

# Cleanup
stream.stop_stream()
stream.close()
audio.terminate()
sock.close()
