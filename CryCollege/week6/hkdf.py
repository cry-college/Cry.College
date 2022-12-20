from CryCollege.week6.hmac import HMAC
from CryCollege.week6.blake2s import BLAKE2s
import math


def _get_digest_size(hashfunc):
    try:
        return hashfunc.digest_size
    except AttributeError:
        return hashfunc().digest_size


# Function definitions as in RFC5869
def hkdf_extract(salt, ikm, hashfunc=BLAKE2s):
    raise NotImplementedError("TODO: Implement me plx")


def hkdf_expand(prk, info, length, hashfunc=BLAKE2s):
    raise NotImplementedError("TODO: Implement me plx")


def hkdf(ikm, salt, info, output_length, hashfunc=BLAKE2s):
    prk = hkdf_extract(salt, ikm, hashfunc)
    print("prk: ", prk)
    return hkdf_expand(prk, info, output_length, hashfunc)


def test_hkdf():
    target = bytes.fromhex("5b429114d70756a16527934cce271d75eff53ce211f8577fe4e7c5ce0f4b23f2")
    
    outp = hkdf(b"ikm", b"salt", b"info", 32)

    assert target == outp


def test_hkdf_long_input():
    target = bytes.fromhex("107c39dc1dad31851bcdb44ae14dcf96e4bf5f05230c8c6ee88507ba1cd369aa")
    
    outp = hkdf(b"ikm"*100, b"salt"*100, b"info"*100, 32)

    assert target == outp


def test_hkdf_extract_expand():
    IKM = b"ikm"*123
    SALT = b"salt"*321
    INFO = b"info"*444
    LEN = 33

    outp = hkdf(IKM, SALT, INFO, LEN)

    prk = hkdf_extract(SALT, IKM)
    outp2 = hkdf_expand(prk, INFO, LEN)

    assert outp == outp2


def test_hkdf_sha256():
    import hashlib
    IKM = bytes.fromhex("2fe3b0d24f7abdfab31665e4ac822603df5d8414e78f98148f948870a6b7f0bc")
    SALT = b"salt"
    INFO = b"INFO"
    LEN = 32

    TARGET_PRK = bytes.fromhex("8f1fcce45bf8bcc8c213f1440a4284268f995b6c91e6769323698019639edcfd")
    TARGET_KEY = bytes.fromhex("5db6b1bf56139c2e09fd4de55bb233461046389adf3c9307baeb54cc90b09093")

    prk = hkdf_extract(SALT, IKM, hashfunc=hashlib.sha256)
    key = hkdf_expand(prk, INFO, LEN, hashfunc=hashlib.sha256)

    assert prk == TARGET_PRK
    assert key == TARGET_KEY
