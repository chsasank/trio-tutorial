import trio


class ChatServer:
    def __init__(self):
        # place to store list of current users
        # this is why we used a class instead of a function
        self.users = {}

    async def server(self, server_stream):
        await server_stream.send_all(b"<meta>: Please enter username: ")
        current_user_name = None
        async for data in server_stream:
            if server_stream not in self.users.values():
                # handle login
                proposed_user_name = data.decode().strip()
                if proposed_user_name in self.users.keys():
                    await server_stream.send_all(
                        b"<meta>: Username taken. Please enter another: "
                    )
                else:
                    current_user_name = proposed_user_name
                    self.users[current_user_name] = server_stream
                    for user_name, user_stream in self.users.items():
                        if user_name == current_user_name:
                            await user_stream.send_all(
                                f"<meta>: Welcome {current_user_name}.\n".encode()
                            )
                        else:
                            await user_stream.send_all(
                                f"<meta>: {current_user_name} joined.\n".encode()
                            )

            else:
                # broadcast the data to other users
                for user_name, user_stream in self.users.items():
                    if user_name != current_user_name:
                        await user_stream.send_all(
                            f"<{current_user_name}> : ".encode() + data
                        )

        try:
            del self.users[current_user_name]
            for user_name, user_stream in self.users.items():
                await user_stream.send_all(
                    f"<meta>: {current_user_name} left\n".encode()
                )
        except KeyError:
            pass


async def main():
    await trio.serve_tcp(ChatServer().server, port=12345)


trio.run(main)