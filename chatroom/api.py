import asyncio
import websockets
import json
import pyaudiowpatch as pyaudio
import wave
import datetime
import threading
import glob
import base64
from pydub import AudioSegment
import os

text = {}
chatrooms = {}
ws = {}
mute_status = {}

recording = False
output_wave = None

# Speaker stream
p = pyaudio.PyAudio()
wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
default_speakers = p.get_device_info_by_index(
    wasapi_info["defaultOutputDevice"])
print(default_speakers)
if not default_speakers["isLoopbackDevice"]:
    for loopback in p.get_loopback_device_info_generator():
        if default_speakers["name"] in loopback["name"]:
            default_speakers = loopback
print(default_speakers)

stream = p.open(
    format=pyaudio.paInt16,
    channels=default_speakers["maxInputChannels"],
    rate=int(default_speakers["defaultSampleRate"]),
    frames_per_buffer=1024,
    input=True,
    input_device_index=default_speakers["index"]
)

# Microphone stream
p2 = pyaudio.PyAudio()

stream2 = p2.open(
    format=pyaudio.paInt16,
    channels=2,
    rate=44100,
    input=True,
    frames_per_buffer=1024
)

recordings = {}


def start_recording(client_id):
    global recordings, output_wave
    recordings[client_id] = True

    file1 = f"recording1_{client_id}_{
        datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    output_wave = wave.open(file1, "wb")
    output_wave.setnchannels(2)
    output_wave.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
    output_wave.setframerate(44100)
    file2 = f"recording2_{client_id}_{
        datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    output_wave2 = wave.open(file2, "wb")
    output_wave2.setnchannels(2)
    output_wave2.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
    output_wave2.setframerate(44100)

    print(f"Recording started for {client_id}")

    while recordings[client_id]:
        if not mute_status[client_id]:
            data = stream.read(1024)
            output_wave.writeframes(data)
            data2 = stream2.read(1024)
            output_wave2.writeframes(data2)

    # Combine 2 streams
    sound1 = AudioSegment.from_file(file1)
    sound2 = AudioSegment.from_file(file2)
    combined = sound1.overlay(sound2)
    combined.export(f"combined_recording_{client_id}_{
                    datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.wav", format='wav')

    output_wave.close()
    output_wave2.close()
    os.remove(file1)
    os.remove(file2)


def stop_recording(client_id):
    global recordings
    recordings[client_id] = False
    print(f"Recording stopped for {client_id}")


def fetch_recordings():
    wav_files = glob.glob("*.wav")
    return wav_files


async def handle_client(websocket, path):
    client_id = None
    try:
        client_id = await websocket.recv()
        ws[client_id] = websocket
        mute_status[client_id] = False
        while True:
            try:
                data = await websocket.recv()
            except websockets.exceptions.ConnectionClosed:
                print(f"Connection with client {client_id} closed.")
                break
            data = json.loads(data)
            if data['action'] == 'mute':
                mute_status[client_id] = data['payload']
            elif data['action'] == 'create':
                chatroom = data['payload']
                chatrooms[chatroom] = {
                    'createdBy': client_id, 'members': [client_id]}

                text[chatroom] = []
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
                # Print out the received audio data
                print("Audio data: ", data['payload'])
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
            elif data['action'] == 'store_text':
                payload = data['payload']
                chatroom, username, message = payload['chatroom'], payload['username'], payload['message']
                text[chatroom].append((username, message))
            elif data['action'] == 'list_text':
                chatroom = data['payload']
                lst = text[chatroom]
                json_str = json.dumps({'textRecords': lst})
                await websocket.send(json_str)
    finally:
        if client_id in ws:
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
            del text[empty_room]


start_server = websockets.serve(handle_client, '0.0.0.0', 8765)

try:
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
except Exception as e:
    print(f"Error occurred: {e}")
