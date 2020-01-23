"""
Emulates a device sending messages to the NRS.
"""

import argparse
import asyncio
from aiocoap import Message, Context, Code
from message import NrsMessage, NrsHeader


def parse_args():
    parser = argparse.ArgumentParser(description='Send a message over the NB-IoT Relay Service')

    parser.add_argument('-H', '--host', nargs='?', help='Server domain name', default='nbiot-relayservice.net',
                        type=str)
    parser.add_argument('-P', '--port', nargs='?', help='MQTT port', type=int, default=5683)

    parser.add_argument('-i', '--imsi', nargs='?', help='Device IMSI', default=1, type=int)
    parser.add_argument('-k', '--key', nargs='?', help='Device auth key', default='ABCDEFGHIJKLMNOPQRSTUVWXYZ012345',
                        type=str)
    parser.add_argument('-m', '--msg', nargs='?', help='Message', default='Hello World!', type=str)

    return parser.parse_args()


async def send_message(host, port, imsi, msg, key):
    url = 'coap://{0}:{1}/uplink'.format(host, port)
    client = await Context.create_client_context()

    message = NrsMessage(NrsHeader.UC, imsi, 1, payload=msg)
    payload = message.to_buffer(key)

    request = Message(code=Code.PUT, payload=payload, uri=url)
    response = await client.request(request).response

    if len(response.payload) > 0:
        response_message = NrsMessage.parse(response.payload)
        print(response_message.validate(key))


def main():
    args = parse_args()
    print(args)

    if len(args.key) != 32:
        print("key must be 32 bytes")
        return

    asyncio.get_event_loop().run_until_complete(send_message(args.host, args.port, args.imsi, args.msg, args.key))


if __name__ == '__main__':
    main()
