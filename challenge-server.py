import asyncio
import socket
from aiocoap import *

class AsyncTCPCoAPServer:
    def __init__(self, host='127.0.0.1', port=65000):
        self.host = host
        self.port = port
        self.loop = asyncio.get_event_loop()

    async def handle_client(self, reader, writer):
        data = await reader.read(100)
        query = data.decode().strip()
        addr = writer.get_extra_info('peername')
        print(f"Received {query} from {addr}")

        coap_response = await self.fetch_coap_resource(query)
        print(f"CoAP response: {coap_response}")

        print(f"Send: {coap_response}")
        writer.write(coap_response.encode())
        await writer.drain()

        print("Close the connection")
        writer.close()

    async def fetch_coap_resource(self, query):
        protocol = await Context.create_client_context()
        request = Message(code=GET, uri=f'coap://coap.me/query?{query}')

        try:
            response = await protocol.request(request).response
            return response.payload.decode()
        except Exception as e:
            print(f'Failed to fetch CoAP resource: {e}')
            return "Error fetching CoAP resource"

    async def run_server(self):
        server = await asyncio.start_server(
            self.handle_client, self.host, self.port)

        addr = server.sockets[0].getsockname()
        print(f'Serving on {addr}')

        async with server:
            await server.serve_forever()

if __name__ == '__main__':
    server = AsyncTCPCoAPServer()
    asyncio.run(server.run_server())
