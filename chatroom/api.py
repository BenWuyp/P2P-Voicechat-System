import asyncio
import websockets
import json

chatrooms = {}
ws = {}


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
