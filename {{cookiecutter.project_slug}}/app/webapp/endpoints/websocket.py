from starlette.endpoints import WebSocketEndpoint


class WebSocketHandler(WebSocketEndpoint):
    encoding = "json"

    async def on_receive(self, websocket, data):
        print(data)
        await websocket.send_text(f"Message text was: {data}")
