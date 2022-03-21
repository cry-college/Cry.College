import math

class Poly1305:
    @staticmethod
    def mac(msg, key):
        raise NotImplementedError("TODO: Implement me plx")


    @staticmethod
    def verify(msg, key, tag):
        return Poly1305.mac(msg, key) == tag

def test_vector():
    key = bytes.fromhex('85d6be7857556d337f4452fe42d506a80103808afb0db2fd4abff6af4149f51b')
    msg = b"Cryptographic Forum Research Group"

    assert Poly1305.mac(msg, key) == bytes.fromhex('a8061dc1305136c6c22b8baf0c0127a9')

def test_verify():
    key = bytes.fromhex('85d6be7857556d337f4452fe42d506a80103808afb0db2fd4abff6af4149f51b')
    msg = b"Cryptographic Forum Research Group"

    assert Poly1305.verify(msg, key, bytes.fromhex('a8061dc1305136c6c22b8baf0c0127a9'))