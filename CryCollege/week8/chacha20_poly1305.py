from CryCollege.week7.chacha20 import Chacha20
from CryCollege.week8.poly1305 import Poly1305

class Mac_Exception(Exception):
    pass

class Chacha20_Poly1305:
    def __init__(self, key, nonce):
        self.chacha20 = Chacha20(key, nonce)
        self.poly1305_key = self.chacha20.chacha20_block(0)[:32]

    @staticmethod
    def pad16(data):
        if len(data) % 16 == 0:
            return data
        return data + b'\x00' * (16 - (len(data) % 16))
        
    def aead_encrypt(self, aad, plaintext):
        raise NotImplementedError("TODO: Implement me plx")
        return (ciphertext, tag)

    def aead_decrypt(self, aad, ciphertext, tag):
        raise NotImplementedError("TODO: Implement me plx")
        if Poly1305.verify(mac_data, self.poly1305_key, tag):
            return self.chacha20.decrypt(ciphertext)
        else:
            raise Mac_Exception

def test_vector():
    chacha20_poly1305 = Chacha20_Poly1305(
        bytes.fromhex('808182838485868788898a8b8c8d8e8f909192939495969798999a9b9c9d9e9f'),
        bytes.fromhex('070000004041424344454647')
    )

    assert chacha20_poly1305.aead_encrypt(
        bytes.fromhex('50515253c0c1c2c3c4c5c6c7'),
        b"Ladies and Gentlemen of the class of '99: If I could offer you only one tip for the future, sunscreen would be it."
    ) == (
        bytes.fromhex('d31a8d34648e60db7b86afbc53ef7ec2a4aded51296e08fea9e2b5a736ee62d63dbea45e8ca9671282fafb69da92728b1a71de0a9e060b2905d6a5b67ecd3b3692ddbd7f2d778b8c9803aee328091b58fab324e4fad675945585808b4831d7bc3ff4def08e4b7a9de576d26586cec64b6116'),
        bytes.fromhex('1ae10b594f09e26a7e902ecbd0600691')
    )

def test_encrypt_decrypt():
    chacha20_poly1305 = Chacha20_Poly1305(
        bytes.fromhex('0102030405060708090a0b0c0d0e0f1011121314151617181920212223242526'),
        bytes.fromhex('272829303132333435363738')
    )

    c, t = chacha20_poly1305.aead_encrypt(b'FooBar', b'Hallo Welt')
    assert chacha20_poly1305.aead_decrypt(b'FooBar', c, t) == b'Hallo Welt'

def test_wrong_aad():
    chacha20_poly1305 = Chacha20_Poly1305(
        bytes.fromhex('0102030405060708090a0b0c0d0e0f1011121314151617181920212223242526'),
        bytes.fromhex('272829303132333435363738')
    )

    c, t = chacha20_poly1305.aead_encrypt(b'FooBar', b'Hallo Welt')
    try:
        chacha20_poly1305.aead_decrypt(b'BarFoo', c, t)
        assert False
    except:
        assert True

def test_wrong_ciphertext():
    chacha20_poly1305 = Chacha20_Poly1305(
        bytes.fromhex('0102030405060708090a0b0c0d0e0f1011121314151617181920212223242526'),
        bytes.fromhex('272829303132333435363738')
    )

    c, t = chacha20_poly1305.aead_encrypt(b'FooBar', b'Hallo Welt')
    try:
        chacha20_poly1305.aead_decrypt(b'FooBar', b'\x00\x01', t)
        assert False
    except:
        assert True