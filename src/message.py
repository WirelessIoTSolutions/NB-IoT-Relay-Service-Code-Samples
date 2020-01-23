import hashlib
import os


class NrsHeader:
    UC = b'UC'


class NrsMessage:

    def __init__(self, header, imsi, counter, payload=b'', nonce=None, checksum=None):
        self.header = header
        self.imsi = imsi
        self.counter = counter

        if isinstance(payload, str):
            payload = payload.encode()

        self.payload = payload

        if nonce is None:
            nonce = os.urandom(8)
        self.nonce = nonce

        self.checksum = checksum

    def validate(self, auth_key):
        data = self.to_buffer(auth_key)
        return self.checksum == data[-32:]

    @classmethod
    def parse(cls, buffer: bytes):
        total_len = len(buffer)

        header = buffer[0:2]
        imsi = int.from_bytes(buffer[2:10], byteorder='big')
        counter = buffer[10]
        payload = buffer[11: total_len - 40]
        nonce = buffer[total_len - 40: total_len - 32]
        checksum = buffer[-32:]

        message = NrsMessage(header, imsi, counter, payload, nonce, checksum)

        return message

    def to_buffer(self, auth_key: str) -> bytes:
        data = bytearray()
        data.extend(self.header)
        data.extend(self.imsi.to_bytes(8, byteorder='big'))
        data.append(self.counter)
        data.extend(self.payload)
        data.extend(self.nonce)

        if isinstance(auth_key, str):
            auth_key = auth_key.encode()

        data.extend(auth_key)

        sha = hashlib.sha256()
        sha.update(data)
        checksum = sha.digest()
        data[-32:] = checksum

        return data
