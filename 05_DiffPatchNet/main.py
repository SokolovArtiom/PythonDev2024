#!/usr/bin/env python3
import asyncio
import cowsay

clients = {}
cow2code = {}
code2cow = {}


def get_free_cows(registred):
    return list(set(cowsay.list_cows()) - set(registred))


async def chat(reader, writer):
    me = "{}:{}".format(*writer.get_extra_info('peername'))
    clients[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())
    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)

        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                msg = q.result().decode().strip()
                if msg == "who":
                    await clients[me].put(list(cow2code.keys()))
                elif msg == "cows":
                    await clients[me].put(get_free_cows(cow2code.keys()))
                elif msg.split()[0] == "login":
                    if msg.split()[1] in get_free_cows(cow2code.keys()):
                        cow2code[msg.split()[1]] = me
                        code2cow[me] = msg.split()[1]
                elif msg.split()[0] == "say":
                    if msg.split()[1] in cow2code:
                        await clients[cow2code[msg.split()[1]]].put(cowsay.cowsay(msg.split()[2],
                                                                                  cow=code2cow[me]))
                elif msg.split()[0] == "yield":
                    for out in clients:
                        if out is not clients[me]:
                            await out.put(msg.split()[1])
                elif msg.split()[0] == "quit":
                    cow2code.pop(code2cow[me])
                    code2cow.pop(me)

            elif q is receive:
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
    send.cancel()
    receive.cancel()
    print(me, "DONE")
    del clients[me]
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
