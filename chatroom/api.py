import asyncio
import websockets
import json
import pyaudio
import wave
import datetime
import threading

chatrooms = {}
ws = {}

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


def start_recording():
    global recording, output_wave
    recording = True

    output_wave = wave.open(
        f"recording_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.wav", "wb")
    output_wave.setnchannels(1)
    output_wave.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    output_wave.setframerate(44100)

    print("Recording started")

    while recording:
        data = stream.read(1024)
        output_wave.writeframes(data)


def stop_recording():
    global recording
    recording = False
    print("Recording stopped")


async def notify_clients(chatroom):
    if chatroom in chatrooms:
        message = ",".join(chatrooms[chatroom])
        await asyncio.gather(*[client.send(message) for client in chatrooms[chatroom]])


async def handle_client(websocket):
    client_id = await websocket.recv()
    ws[client_id] = websocket
    try:
        while True:
            data = await websocket.recv()
            data = json.loads(data)
            if data['action'] == 'create':
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
                threading.Thread(target=start_recording).start()
            elif data['action'] == 'end_record':
                stop_recording()
    finally:
        del ws[client_id]
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

start_server = websockets.serve(handle_client, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
