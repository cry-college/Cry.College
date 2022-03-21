import pytest


def xor(a, b):
    raise NotImplementedError("TODO: Implement me plx")


class XORCipher:

    def __init__(self, key):
        self.key = key

    def encrypt(self, data):
        if not isinstance(data, bytes):
            raise ValueError("You can only encrypt bytes.")
        
        """
        Encrypt the data using the Vigenère cipher
        """
        raise NotImplementedError("TODO: Implement me plx")

    def decrypt(self, data):
        """
        Decrypt the data using the Vigenère cipher
        """
        raise NotImplementedError("TODO: Implement me plx")


@pytest.fixture
def xor_cipher():
    key = bytes.fromhex("AB CD EF AFFE AFFE DEADBEEF")
    cipher = XORCipher(key)
    return cipher


def test_xor_enc(xor_cipher):
    res = xor_cipher.encrypt(b"HALLO!")
    assert(res == b'\xe3\x8c\xa3\xe3\xb1\x8e')


def test_xor_dec(xor_cipher):
    res = xor_cipher.decrypt(b'\xe3\x8c\xa3\xe3\xb1\x8e')
    assert(res == b"HALLO!")


def test_xor_equiv(xor_cipher):
    msg = b"dkahsdjkasdhashdahsdha"
    assert(xor_cipher.encrypt(msg) == xor_cipher.decrypt(msg))


def test_shortkey():
    msg = b"a" * 1000
    key = b"1337"

    cipher = XORCipher(key)
    assert cipher.decrypt(cipher.encrypt(msg)) == msg