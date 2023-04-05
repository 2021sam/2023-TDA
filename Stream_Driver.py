import pyodbc
import websockets
import asyncio
import datetime
import math

# pip install nest-asyncio
from Class.StreamingClient import StreamingClient
import nest_asyncio
nest_asyncio.apply()

from Class.Stream import Stream
stream = Stream()


if __name__ == '__main__':
	client = StreamingClient()
	loop = asyncio.get_event_loop()
	socket = loop.run_until_complete(client.socketconnect())
	tasks = [asyncio.ensure_future(client.receive(socket)),
                asyncio.ensure_future(client.send( stream.login )),
                asyncio.ensure_future(client.receive(socket)),
                asyncio.ensure_future(client.send( stream.qos )),
                asyncio.ensure_future(client.receive(socket)),
                asyncio.ensure_future(client.send( stream.quote )),
                asyncio.ensure_future(client.receive(socket)),
            ]

	loop.run_until_complete(asyncio.wait(tasks))