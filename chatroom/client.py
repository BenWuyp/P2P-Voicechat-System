import asyncio
import websockets
import json


async def client():
    async with websockets.connect('ws://localhost:8765') as websocket:
        client_id = input("Enter your ID: ")
        await websocket.send(client_id)
        while True:
            action = input(
                "Choose an action ([1] Create chatroom, [2] Join chatroom, [3] Send message, [4] Get chatroom list, [5] quit chatroom, [6] exit): ")
            if action == '1':
                chatroom = input("Enter chatroom name: ")
                data = {'action': 'create', 'payload': chatroom}
                json_str = json.dumps(data)
                await websocket.send(json_str)
            elif action == '2':
                chatroom = input("Enter chatroom name: ")
                data = {'action': 'join', 'payload': chatroom}
                json_str = json.dumps(data)
                await websocket.send(json_str)
            elif action == '3':
                chatroom = input("Enter chatroom name: ")
                message = input("Enter your message: ")
                message = f"message:{chatroom}:{message}"
                await websocket.send(message)
            elif action == '4':
                message = "list:"
                data = {'action': 'list'}
                json_str = json.dumps(data)
                await websocket.send(json_str)
                response = await websocket.recv()
                chatrooms = json.loads(response)
                print("Available Chatrooms:", chatrooms)
            elif action == '5':
                chatroom = input("Enter chatroom name: ")
                data = {'action': 'quit', 'payload': chatroom}
                json_str = json.dumps(data)
                await websocket.send(json_str)
            elif action == '6':
                data = {'action': 'exit'}
                json_str = json.dumps(data)
                await websocket.send(json_str)
                break
            else:
                print("Invalid action. Please choose again.")

asyncio.run(client())
