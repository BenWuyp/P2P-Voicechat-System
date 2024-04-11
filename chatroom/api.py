import asyncio
import websockets
import json
import pyaudio
import wave
import datetime
import threading
import glob
import base64

chatrooms = {}
ws = {}
mute_status = {}

recording = False
output_wave = None
p = pyaudio.PyAudio()

stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=44100,
    input=True,
    frames_per_buffer=1024
)

recordings = {}


def start_recording(client_id):
    global recordings, output_wave
    recordings[client_id] = True

    output_wave = wave.open(
        f"recording_{client_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.wav", "wb")
    output_wave.setnchannels(1)
    output_wave.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    output_wave.setframerate(44100)

    print(f"Recording started for {client_id}")

    while recordings[client_id]:
        if not mute_status[client_id]:
            data = stream.read(1024)
            output_wave.writeframes(data)


def stop_recording(client_id):
    global recordings
    recordings[client_id] = False
    print(f"Recording stopped for {client_id}")


def fetch_recordings():
    wav_files = glob.glob("*.wav")
    return wav_files


async def handle_client(websocket, path):
    client_id = await websocket.recv()
    ws[client_id] = websocket
    mute_status[client_id] = False
    try:
        while True:
            data = await websocket.recv()
            data = json.loads(data)
            if data['action'] == 'mute':
                mute_status[client_id] = data['payload']
            elif data['action'] == 'create':
                chatroom = data['payload']
                chatrooms[chatroom] = {
                    'createdBy': client_id, 'members': [client_id]}
            elif data['action'] == 'join':
                chatroom = data['payload']
                if chatroom in chatrooms:
                    chatrooms[chatroom]['members'].append(client_id)
                else:
                    await websocket.send("Chatroom does not exist.")
            elif data['action'] == 'list':
                lst = json.dumps(chatrooms)
                await websocket.send(lst)
            elif data['action'] == 'quit':
                chatroom = data['payload']
                lst = chatrooms[chatroom]['members']
                lst.remove(client_id)
                if (not lst):
                    del chatrooms[chatroom]
            elif data['action'] == 'exit':
                break
            elif data['action'] == 'start_record':
                threading.Thread(target=start_recording,
                                 args=(client_id,)).start()
            elif data['action'] == 'end_record':
                stop_recording(client_id)
            elif data['action'] == 'fetch_recordings':
                await websocket.send(json.dumps(fetch_recordings()))
            elif data['action'] == 'send_recording':
                print("Received audio stream from client: ", client_id)
                print("Audio data: ", data['payload'])  # Print out the received audio data
            elif data['action'] == 'fetch_recording':
                file_name = data['payload']
                try:
                    with open(file_name, 'rb') as audio_file:
                        audio_data = audio_file.read()
                        audio_str = base64.b64encode(
                            audio_data).decode('utf-8')
                        await websocket.send(audio_str)
                except FileNotFoundError:
                    await websocket.send('File not found')
    finally:
        del ws[client_id]
        # del mute_status[client_id]
        empty_room = None
        for chatroom, obj in chatrooms.items():
            lst = obj['members']
            for id in lst:
                if (id == client_id):
                    lst.remove(id)
                    break
            if (not lst):
                empty_room = chatroom
        if (empty_room):
            del chatrooms[empty_room]


start_server = websockets.serve(handle_client, '0.0.0.0', 8765)

try:
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
except Exception as e:
    print(f"Error occurred: {e}")
