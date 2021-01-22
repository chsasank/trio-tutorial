import trio

async def echo_server(server_stream):
    print("echo_server: started")
    async for data in server_stream:
        print("echo_server: received data {!r}".format(data))
        await server_stream.send_all(data)

    print("echo_server: connection closed")

async def main():
    await trio.serve_tcp(echo_server, port=12345)

trio.run(main)
