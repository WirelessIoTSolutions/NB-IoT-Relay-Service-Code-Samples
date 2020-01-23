"""
This is a simple MQTT message consumer. Subscribes to a topic on a MQTT server.
"""
import paho.mqtt.client as mqtt
import argparse

from paho.mqtt.client import MQTTv311


def parse_args():
    parser = argparse.ArgumentParser(description='Send a message over the NB-IoT Relay Service')
    parser.add_argument('-H', '--host', nargs='?', help='MQTT server', type=str, default='vmq.nbiot-relayservice.net')
    parser.add_argument('-P', '--port', nargs='?', help='MQTT port', type=int, default=1883)

    parser.add_argument('-c', '--client', help='Client id for connecting to the MQTT server', type=str, required=True)
    parser.add_argument('-u', '--username', help='Username for connecting to the MQTT server', type=str, required=True)
    parser.add_argument('-p', '--password', help='Password for connecting to the MQTT server', type=str, required=True)
    parser.add_argument('-t', '--topic', help='Topic to listen to on the MQTT server', type=str, required=True)

    args = parser.parse_args()
    return args


def on_connect(client, obj, flags, rc):
    print("connect")
    if rc == 0:
        print("subscribed to", client._topic)
        client.subscribe(client._topic)
    else:
        print("connection error:", rc)


def on_message(client, obj, msg):
    print(msg.topic, msg.payload)


def connect(args):
    print("Connecting to {}:{}".format(args.host, args.port))
    print("client id: {}, username: {}".format(args.client, args.username))

    client = mqtt.Client(args.client, protocol=MQTTv311, transport="tcp")
    client.username_pw_set(args.username, args.password)
    client._topic = args.topic
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(args.host, args.port)
    print("connecting...")
    client.loop_forever()


def main():
    args = parse_args()
    connect(args)


if __name__ == '__main__':
    main()
