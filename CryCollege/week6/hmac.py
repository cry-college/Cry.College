from CryCollege.week6.blake2s import BLAKE2s, pad_with_zeros
from CryCollege.week1.cipher import xor


def HMAC(key, msg, hashfunc=BLAKE2s):
    """
    Create a HMAC of the provided message with the provided key using the provided hashfunktion
    """
    raise NotImplementedError("TODO: Implement me plx")


def test_blake2s_short_key():
    import hmac
    import hashlib

    key = b"Test1234"
    msg = b"A" * 200

    std_hmac = hmac.new(key, msg, hashlib.blake2s)
    own_hmac = HMAC(key, msg, BLAKE2s)

    assert std_hmac.digest() == own_hmac


def test_blake2s_long_key():
    import hmac
    import hashlib

    key = b"B" * 123
    msg = b"A" * 200

    std_hmac = hmac.new(key, msg, hashlib.blake2s)
    own_hmac = HMAC(key, msg, BLAKE2s)

    assert std_hmac.digest() == own_hmac


def test_blake2s_blocksize_key():
    import hmac
    import hashlib

    key = b"C" * BLAKE2s.block_size
    msg = b"A" * 200

    std_hmac = hmac.new(key, msg, hashlib.blake2s)
    own_hmac = HMAC(key, msg, BLAKE2s)

    assert std_hmac.digest() == own_hmac


def test_blake2s_digestsize_key():
    import hmac
    import hashlib

    key = b"C" * BLAKE2s.digest_size
    msg = b"A" * BLAKE2s.digest_size

    std_hmac = hmac.new(key, msg, hashlib.blake2s)
    own_hmac = HMAC(key, msg, BLAKE2s)

    assert std_hmac.digest() == own_hmac


def test_blake2s_hkdf():
    import hmac
    import hashlib

    key = b"\x00" * 32
    msg = bytes.fromhex("88c2e07343aba6936066225955bd1d4aa9ce00e8f6b2f84bfeb3405ed86e0912")

    std_hmac = hmac.new(key, msg, hashlib.blake2s)
    own_hmac = HMAC(key, msg, BLAKE2s)

    assert std_hmac.digest() == own_hmac


def test_hmac_sha256():
    import hmac
    import hashlib

    key = b"A" * 32
    msg = bytes.fromhex("88c2e07343aba6936066225955bd1d4aa9ce00e8f6b2f84bfeb3405ed86e0912")

    std_hmac = hmac.new(key, msg, hashlib.sha256)
    own_hmac = HMAC(key, msg, hashfunc=hashlib.sha256)

    assert std_hmac.digest() == own_hmac