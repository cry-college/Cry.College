import pytest

import hashlib
from CryCollege.week3.elliptic_curve import AffinePoint
from CryCollege.week5.edwards_curve import EdwardsCurve
from CryCollege.week2.finitefield import PrimeField

FIELD = PrimeField(2 ** 255 - 19)
CURVE = EdwardsCurve(37095705934669439343138083508754565189542113879843219016388785533085940283555, FIELD, -1)
B = AffinePoint(CURVE, 
            15112221349535400772501151409588531511454012693041857206046113283949847762202, 
            46316835694926478169428394003475163141307993866256225615783033603165251855960, 
            2 ** 252 + 27742317777372353535851937790883648493)
b = 256
n = 254


def calculate_secret_scalar(sk):
    """
    Calculate secret scalar of private point from provided secret key
    """
    h = bytearray(hashlib.sha512(sk).digest()[:32])
    h[0] &= 248
    h[31] &= 127
    h[31] |= 64
    return int.from_bytes(h, 'little')


def encode_point(P):
    """
    Encode point as bytes (point compression)
    """
    y = P.y.elem
    x = P.x.elem

    if x & 1:
        y |= 1 << (32 * 8 - 1)
    else:
        y &= ~(1 << (32 * 8 - 1))

    return y.to_bytes(32, 'little')


def decode_point(P):
    """
    Inverse operation of encode_point
    """
    y = FIELD(int.from_bytes(P, 'little') & ~(1 << (32 * 8 - 1)))

    u = y ** 2 - 1
    v = CURVE.d * y ** 2 + 1

    x = (u * v ** -1) ** ((FIELD.mod+3) * FIELD(8) ** -1)

    if v * x ** 2 == u * -1:
        x = x * FIELD(2) ** ((FIELD.mod-1) * FIELD(4) ** -1).elem
    elif v * x ** 2 != u:
        raise ValueError("Point can't be decoded")

    x_0 = (int.from_bytes(P, 'little') & 1 << (32 * 8 - 1)) >> (32 * 8 - 1)
    if x == 0 and x_0 == 1:
        raise ValueError("Point can't be decoded")
    if x_0 != x.elem % 2:
        x = x * -1

    return AffinePoint(CURVE, x, y)


def hash_digest(input_bytes):
    return hashlib.sha512(input_bytes).digest()


def bytes_to_int(input_bytes):
    return int.from_bytes(input_bytes, "little")


def int_from_hash(input_bytes):
    return bytes_to_int(
        hash_digest(input_bytes)
    )


class ED25519PublicKey:

    def __init__(self, pk_bytes):
        self.pk_bytes = pk_bytes
        self.pk = decode_point(pk_bytes)

    def verify(self, message, signature):
        """
        Verify a signature
        :return: True if valid, False else
        """
        raise NotImplementedError("TODO: Implement me plx")


class ED25519PrivateKey:

    def __init__(self, sk):
        if not (isinstance(sk, bytes) and len(sk) == 32):
            raise ValueError("Only 32B byte strings allowed as secret key.")
        self.sk_raw = sk
        self.sk = calculate_secret_scalar(sk)
        pk_encoded = encode_point(self.sk * B)
        self.public_key = ED25519PublicKey(pk_encoded)

    def sign(self, message):
        """
        Create a signature
        """
        raise NotImplementedError("TODO: Implement me plx")


@pytest.fixture
def ed25519priv():
    return ED25519PrivateKey(
        bytes.fromhex("c5aa8df43f9f837bedb7442f31dcb7b166d38535076f094b85ce3a2e0b4458f7")
    )


def test_ed25519(ed25519priv):
    # Test vector from: https://tools.ietf.org/html/rfc8032#section-7.1
    PK = bytes.fromhex("fc51cd8e6218a1a38da47ed00230f0580816ed13ba3303ac5deb911548908025")
    SIG = bytes.fromhex("6291d657deec24024827e69c3abe01a30ce548a284743a445e3680d7db5ac3a"
                        "c18ff9b538d16f290ae67f760984dc6594a7c15e9716ed28dc027beceea1ec40a")

    assert ed25519priv.public_key.pk_bytes == PK
    signature = ed25519priv.sign(b"\xaf\x82")
    assert signature == SIG
    assert ed25519priv.public_key.verify(b"\xaf\x82", signature)

    # test own pubkey instance
    pubkey = ED25519PublicKey(ed25519priv.public_key.pk_bytes)
    assert pubkey.verify(b"\xaf\x82", signature)


def test_point_encoding(ed25519priv):
    assert calculate_secret_scalar(ed25519priv.sk_raw) * B == decode_point(ed25519priv.public_key.pk_bytes)


def test_invalid_signature(ed25519priv):
    BAD_SIG = b"6291d657deec24024827e69c3abe01a30ce548a284743a445e3680d7db5ac3ac18ff9b538d16f2" \
              b"90ae67f760984dc6594a7c15e9716ed28dc027beceea1ec40a"
    assert not ed25519priv.public_key.verify(b"1337", BAD_SIG)
