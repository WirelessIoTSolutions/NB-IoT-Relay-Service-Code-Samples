"""
Send a test message to the device over the NRS."
"""
import argparse
import base64
import json
import paho.mqtt.publish as publish


def parse_args():
    parser = argparse.ArgumentParser(description='Send a message over the NB-IoT Relay Service')

    parser.add_argument('-H', '--host', nargs='?', help='MQTT server', type=str, default='vmq.nbiot-relayservice.net')
    parser.add_argument('-P', '--port', nargs='?', help='MQTT port', type=int, default=1883)

    parser.add_argument('-c', '--client', help='Client id for connecting to the MQTT server', type=str, required=True)
    parser.add_argument('-u', '--username', help='Username for connecting to the MQTT server', type=str, required=True)
    parser.add_argument('-p', '--password', help='Password for connecting to the MQTT server', type=str, required=True)
    parser.add_argument('-t', '--topic', help='Topic to publish to on the MQTT server', type=str, required=True)
    parser.add_argument('-i', '--imsi', help='IMSI to publish to on the MQTT server', type=str)
    parser.add_argument('-m', '--message', help='Message to send to the device', type=str)

    return parser.parse_args()


def main():
    args = parse_args()
    print('connecting to {}:{}'.format(args.host, args.port))
    print('client id: {}, username: {}, password: {}'.format(args.client, args.username, args.password))

    auth = {'username': args.username, 'password': args.password}

    data = {"payload": base64.b64encode(args.message.encode()).decode()}
    if args.imsi is not None:
        data['imsi'] = args.imsi

    msgs = [
        {'topic': args.topic, 'payload': json.dumps(data)},
    ]

    publish.multiple(msgs, hostname=args.host, port=args.port, client_id=args.client, auth=auth)


if __name__ == '__main__':
    main()
