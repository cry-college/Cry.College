import struct
from copy import deepcopy

MASK_32BIT = 0xffffFFFF


def uint32(num):
    return num & MASK_32BIT


def rol32(a, x):
    return uint32(a << x) | uint32(a >> (32 - x))


def u8_array_as_u32_le(array):
    r = struct.unpack("<I", struct.pack("<4B", *array))
    return r[0]


class Chacha20:
    def __init__(self, key, nonce):
        raise NotImplementedError("TODO: Implement me plx")
        self.state = [
            """
            TODO
            """
        ]

    @staticmethod
    def quarterround(state, a, b, c, d):
        raise NotImplementedError("TODO: Implement me plx")

    def chacha20_block(self, counter):
        self.state[12] = uint32(counter)
        state = deepcopy(self.state)
        old_state = deepcopy(self.state)

        for _ in range(10):
            Chacha20.quarterround(state, 0, 4, 8,12)
            Chacha20.quarterround(state, 1, 5, 9,13)
            Chacha20.quarterround(state, 2, 6,10,14)
            Chacha20.quarterround(state, 3, 7,11,15)
            Chacha20.quarterround(state, 0, 5,10,15)
            Chacha20.quarterround(state, 1, 6,11,12)
            Chacha20.quarterround(state, 2, 7, 8,13)
            Chacha20.quarterround(state, 3, 4, 9,14)

        for i in range(16):
            state[i] = uint32(state[i] + old_state[i])

        result = b''

        for number in state:
            result += number.to_bytes(4, "little")

        return result

    @staticmethod
    def xor(plaintext, keystream):
        result = bytearray()

        for i in range(len(plaintext)):
            result.append(plaintext[i] ^ keystream[i])

        return bytes(result)

    def encrypt(self, plaintext):
        raise NotImplementedError("TODO: Implement me plx")

    def decrypt(self, ciphertext):
        return self.encrypt(ciphertext)


def test_quarterround():
    chacha20 = Chacha20(b'\x00' * 32, b'\x00' * 12)
    chacha20.state = [
        0x11111111, 0x01020304, 0x9b8d6f43, 0x01234567,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
    ]
    chacha20.state = list(map(lambda x: uint32(x), chacha20.state))
    Chacha20.quarterround(chacha20.state, 0, 1, 2, 3)

    assert chacha20.state[0] == 0xea2a92f4
    assert chacha20.state[1] == 0xcb1cf8ce
    assert chacha20.state[2] == 0x4581472e
    assert chacha20.state[3] == 0x5881c4bb


def test_block_test_vector():
    chacha20 = Chacha20(
        b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
        b'\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f',
        b'\x00\x00\x00\x09\x00\x00\x00\x4a\x00\x00\x00\x00'
    )

    block = chacha20.chacha20_block(1)
    assert block == b'\x10\xf1\xe7\xe4\xd1\x3b\x59\x15\x50\x0f\xdd\x1f\xa3\x20\x71\xc4\xc7\xd1\xf4\xc7\x33\xc0' \
                    b'\x68\x03\x04\x22\xaa\x9a\xc3\xd4\x6c\x4e\xd2\x82\x64\x46\x07\x9f\xaa\x09\x14\xc2\xd7\x05' \
                    b'\xd9\x8b\x02\xa2\xb5\x12\x9c\xd1\xde\x16\x4e\xb9\xcb\xd0\x83\xe8\xa2\x50\x3c\x4e'


def test_encryption_test_vector():
    chacha20 = Chacha20(
        b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e"
        b"\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f",
        b"\x00\x00\x00\x00\x00\x00\x00\x4a\x00\x00\x00\x00"
    )

    ciphertext = chacha20.encrypt(b"Ladies and Gentlemen of the class of '99: "
                                  b"If I could offer you only one tip for the future, sunscreen would be it.")

    assert ciphertext == b'\x6e\x2e\x35\x9a\x25\x68\xf9\x80\x41\xba\x07\x28\xdd\x0d\x69\x81\xe9\x7e\x7a' \
                         b'\xec\x1d\x43\x60\xc2\x0a\x27\xaf\xcc\xfd\x9f\xae\x0b\xf9\x1b\x65\xc5\x52\x47' \
                         b'\x33\xab\x8f\x59\x3d\xab\xcd\x62\xb3\x57\x16\x39\xd6\x24\xe6\x51\x52\xab\x8f' \
                         b'\x53\x0c\x35\x9f\x08\x61\xd8\x07\xca\x0d\xbf\x50\x0d\x6a\x61\x56\xa3\x8e\x08' \
                         b'\x8a\x22\xb6\x5e\x52\xbc\x51\x4d\x16\xcc\xf8\x06\x81\x8c\xe9\x1a\xb7\x79\x37' \
                         b'\x36\x5a\xf9\x0b\xbf\x74\xa3\x5b\xe6\xb4\x0b\x8e\xed\xf2\x78\x5e\x42\x87\x4d'


def test_encryption_decryption():
    plaintext = b"Hallo Welt"
    
    chacha20 = Chacha20(
        b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11"
        b"\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f",
        b"\x00\x00\x00\x00\x00\x00\x00\x4a\x00\x00\x00\x00")

    assert plaintext, chacha20.decrypt(chacha20.encrypt(plaintext))