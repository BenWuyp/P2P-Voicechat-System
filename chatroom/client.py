import asyncio
import websockets


async def client():
    async with websockets.connect('ws://localhost:8765') as websocket:
        client_id = input("Enter your ID: ")
        await websocket.send(client_id)
        while True:
            action = input(
                "Choose an action ([1] Create chatroom, [2] Join chatroom, [3] Send message, [4] Get chatroom list, [5] exit): ")
            if action == '1':
                chatroom = input("Enter chatroom name: ")
                message = f"create:{chatroom}"
                await websocket.send(message)
            elif action == '2':
                chatroom = input("Enter chatroom name: ")
                message = f"join:{chatroom}"
                await websocket.send(message)
            elif action == '3':
                chatroom = input("Enter chatroom name: ")
                message = input("Enter your message: ")
                message = f"message:{chatroom}:{message}"
                await websocket.send(message)
            elif action == '4':
                message = "list:"
                await websocket.send(message)
                response = await websocket.recv()
                chatroom_list = response.split(",")
                print("Available Chatrooms:", chatroom_list)
            elif action == '5':
                message = "exit:"
                await websocket.send(message)
                break
            else:
                print("Invalid action. Please choose again.")

asyncio.run(client())
