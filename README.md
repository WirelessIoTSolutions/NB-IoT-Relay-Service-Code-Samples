# NB-IoT Relay Service Code Samples

## Getting Started

The code samples ar written in python. To get started please create a virtual env and install the dependencies specified in the requirements.txt file.

    $ python3 -m venv venv
    $ source venv/bin/activate
    $ pip install -U pip setuptools
    $ pip install -r requirements.txt

## Code examples

### Uplink messages

Uplink messages are sent from the device to over the relay service to a message consumer.
Parameters can be accessed on the NRS dashboard.

To send an uplink message, use `uplink.py`.

    python uplink.py -H <nrs host> -i <imsi> -k <key> -m <msg>

### Consuming uplink messages

Uplink messages can be received using a mqtt consumer.
MQTT parameters can be accessed on the NRS dashboard.

Example is `consumer.py`

    $ python consumer.py -H <mqtt host> -c <mqtt client> -u <mqtt user> -p <mqtt password> -t <mqtt topic>

### Downlink Messages

Downlink messages are sent using mqtt over the relay service to a device.
The relay service will cache the messages until the next connect by the device.
MQTT parameters can be accessed on the NRS dashboard.

To send a downlink message use `downlink.py`.

    $ python downlink.py -H <mqtt host> -c <mqtt client> -u <mqtt user> -p <mqtt password> -t <mqtt topic> -i <imsi>  -m <msg>
