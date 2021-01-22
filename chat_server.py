import trio


class ChatServer:
    def __init__(self):
        self.users = {}

    async def server(self, server_stream):
        await server_stream.send_all(b"<meta>: Please enter username: ")
        user_name = None
        async for data in server_stream:
            if server_stream not in self.users.values():
                # handle login
                proposed_user_name = data.decode().strip()
                if proposed_user_name in self.users.keys():
                    await server_stream.send_all(
                        b"<meta>: Username taken. Please enter another: "
                    )
                else:
                    user_name = proposed_user_name
                    self.users[user_name] = server_stream
                    for other_user_name, other_user_stream in self.users.items():
                        if other_user_name == user_name:
                            await other_user_stream.send_all(
                                f"<meta>: Welcome to the chat, {user_name}.\n".encode()
                            )
                        else:
                            await other_user_stream.send_all(
                                f"<meta>: {user_name} joined the chat.\n".encode()
                            )

            else:
                # broadcast the data to other users
                for other_user_name, other_user_stream in self.users.items():
                    if other_user_name != user_name:
                        await other_user_stream.send_all(
                            f"<{user_name}> : ".encode() + data
                        )

        try:
            del self.users[user_name]
            for other_user_name, other_user_stream in self.users.items():
                await other_user_stream.send_all(f"<meta>: {user_name} left\n".encode())
        except KeyError:
            pass


async def main():
    await trio.serve_tcp(ChatServer().server, port=12345)


trio.run(main)
