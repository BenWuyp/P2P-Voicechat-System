import asyncio
import websockets

connected_clients = set()
chatrooms = {}


async def notify_clients(chatroom):
    if chatroom in chatrooms:
        message = ",".join(chatrooms[chatroom])
        await asyncio.gather(*[client.send(message) for client in chatrooms[chatroom]])


async def handle_client(websocket):
    connected_clients.add(websocket)
    client_id = await websocket.recv()
    try:
        while True:
            message = await websocket.recv()
            action, payload = message.split(":")
            if action == 'create':
                chatroom = payload
                chatrooms[chatroom] = [(websocket, client_id)]
            elif action == 'join':
                chatroom = payload
                if chatroom in chatrooms:
                    chatrooms[chatroom].append((websocket, client_id))
                else:
                    await websocket.send("Chatroom does not exist.")
            elif action == 'message':
                chatroom = payload.split(":")[0]
                if chatroom in chatrooms:
                    await notify_clients(chatroom)
                else:
                    await websocket.send("Chatroom does not exist.")
            elif action == 'list':
                chatroom_list = []
                for chatroom, lst in chatrooms.items():
                    chatroom_str = chatroom + ':'
                    for ws, id in lst:
                        chatroom_str += id + '+'
                    chatroom_list.append(chatroom_str)
                await websocket.send(",".join(chatroom_list))
            elif action == 'exit':
                break
    finally:
        connected_clients.remove(websocket)
        for chatroom in chatrooms.values():
            for ws, id in chatroom:
                if (websocket == ws):
                    chatroom.remove((websocket, id))

start_server = websockets.serve(handle_client, 'localhost', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
