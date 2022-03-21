"""
Pure Python implementation of Blake2s.
Sources:
[1] https://www.blake2.net/blake2.pdf
[2] https://github.com/BLAKE2/BLAKE2
"""
import struct

BLOCK_LENGTH = 64
DEFAULT_DIGEST_LENGTH = 32

# The parameter block is specified at page 7 of [1]
STRUCT_PARAMETER_BLOCK = "<BBBBIIHBBQQ"

# Parameters fixed for this sequential implementation
DIGEST_SIZE = 32
FANOUT = 1
DEPTH = 1
LEAF_LENGTH = 0
NODE_OFFSET_LOW = 0
NODE_OFFSET_HIGH = 0
NODE_DEPTH = 0
INNER_LENGTH = 0

MASK_32BIT = 0xffffFFFF


# Permutation table
SIGMA = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
    [14, 10, 4, 8, 9, 15, 13, 6, 1, 12, 0, 2, 11, 7, 5, 3],
    [11, 8, 12, 0, 5, 2, 15, 13, 10, 14, 3, 6, 7, 1, 9, 4],
    [7, 9, 3, 1, 13, 12, 11, 14, 2, 6, 5, 10, 4, 0, 15, 8],
    [9, 0, 5, 7, 2, 4, 10, 15, 14, 1, 11, 12, 6, 8, 3, 13],
    [2, 12, 6, 10, 0, 11, 8, 3, 4, 13, 7, 5, 15, 14, 1, 9],
    [12, 5, 1, 15, 14, 13, 4, 10, 0, 7, 6, 3, 9, 2, 8, 11],
    [13, 11, 7, 14, 12, 1, 3, 9, 5, 0, 15, 4, 8, 6, 2, 10],
    [6, 15, 14, 9, 11, 3, 0, 8, 12, 2, 13, 7, 1, 4, 10, 5],
    [10, 2, 8, 4, 7, 6, 1, 5, 15, 11, 9, 14, 3, 12, 13, 0]
]

# IV is identical to that of SHA-256
IV = [
    0x6a09e667, 0xbb67ae85,
    0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c,
    0x1f83d9ab, 0x5be0cd19
]


def pad_with_zeros(data: bytes, size=BLOCK_LENGTH):
    return data.ljust(size, b"\x00")


def uint32(num):
    return num & MASK_32BIT


def ror_32(num, rot):
    """
    Rotate the 32 bit number `num` right by `rot` bits.
    """
    return uint32(((num >> rot) | (num << (32 - rot))))


def split_32(num):
    """
    Split num into two 32 bit numbers. 
    """
    return (
            num & MASK_32BIT,  # Lower 32b
            (num >> 32) & MASK_32BIT  # Upper 32b
    )


def G(r, i, a, b, c, d, block_m):
    """
    ChaCha quarter round used for mixing.
    :param r: round number
    :param i: offset number in round
    :param a: operand 1
    :param b: operand 2
    :param c: operand 3
    :param d: operand 4
    :param block_m: block as 32 bit integers
    :return:
    """
    raise NotImplementedError("TODO: Implement me plx")

def compress(message_block, chaining_value, byte_counter, final_block):
    """
    BLAKE2s compression function.
    """
    raise NotImplementedError("TODO: Implement me plx")

class BLAKE2s:
    # Have block and digest size as class attribute for compatibility
    # with hash functions from stdlib
    block_size = BLOCK_LENGTH
    digest_size = DEFAULT_DIGEST_LENGTH
    name = "blake2s"

    def __init__(self, data=b"", key=b'', salt=0, personalization=0):
        if len(key) > BLOCK_LENGTH:
            raise ValueError("Maximum key length is {BLOCK_LENGTH}.")

        # Parameters as bytes string, needed for initial XOR
        self.parameter_block = struct.pack(
            STRUCT_PARAMETER_BLOCK,
            DIGEST_SIZE,
            len(key),
            FANOUT,
            DEPTH,
            LEAF_LENGTH,
            NODE_OFFSET_LOW,
            NODE_OFFSET_HIGH,
            NODE_DEPTH,
            INNER_LENGTH,
            salt,
            personalization
        )

        # Parameter bytestring interpreted as 32 bit integers (uint32_t)
        parameter_block_u32 = struct.unpack("<8I", self.parameter_block)

        self.iv = [IV[i] ^ parameter_block_u32[i] for i in range(8)]

        self.byte_counter = 0

        if key:
            key_padded = pad_with_zeros(key)
            data = key_padded + data

        # Internal working buffer, keeping data as it come in
        self.buffer = b""

        self.update(data)

    # Apparently there is no zero padding for messages with length of a multiple of the block size?! 
    def update(self, data):
        self.buffer += data

    def _hash(self):
        num_blocks = len(self.buffer) // BLOCK_LENGTH
        byte_counter = 0
        h = self.iv

        if len(self.buffer) % BLOCK_LENGTH == 0:
            # Buffer is a multiple of the block length
            # so we treat the last block as-is
            num_blocks -= 1

        for i in range(0, num_blocks):
            byte_counter += BLOCK_LENGTH
            counter = split_32(byte_counter)
            msg_block = self.buffer[i * BLOCK_LENGTH:(i + 1) * BLOCK_LENGTH]
            h = compress(msg_block, h, counter, False)

        # Work on last block
        remainder = self.buffer[num_blocks * BLOCK_LENGTH:]

        counter = split_32(byte_counter + len(remainder))
        padded_buffer = pad_with_zeros(remainder)
        h = compress(padded_buffer, h, counter, True)
   
        # Internal words are digest
        digest = struct.pack('<8I', *h)

        return digest

    def digest(self, n_bytes=DEFAULT_DIGEST_LENGTH):
        return self._hash()[:n_bytes]

    def hexdigest(self, n_bytes=DEFAULT_DIGEST_LENGTH):
        return self.digest(n_bytes).hex()


def test_blake2s_testvector():
    # Test vector from https://github.com/BLAKE2/BLAKE2/blob/master/testvectors/blake2s-kat.txt#L227
    input = bytes.fromhex("000102030405060708090a0b0c0d0e0f10111213"
                          "1415161718191a1b1c1d1e1f2021222324252627"
                          "28292a2b2c2d2e2f3031323334353637")
    key = bytes.fromhex("000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f")
    output = bytes.fromhex("2966b3cfae1e44ea996dc5d686cf25fa053fb6f67201b9e46eade85d0ad6b806")

    digest = BLAKE2s(input, key=key).digest()

    assert digest == output


def test_blake2s():
    import hashlib

    data = b"Howdy, Partner" * 50
    blake = BLAKE2s(data=data)

    blake_std = hashlib.blake2s(data)

    assert blake.digest() == blake_std.digest()
    assert blake.hexdigest() == blake_std.hexdigest()


def test_blake2s_shortmsg():
    import hashlib

    data = b"A"
    blake = BLAKE2s(data=data)

    blake_std = hashlib.blake2s(data)

    assert blake.digest() == blake_std.digest()
    assert blake.hexdigest() == blake_std.hexdigest()


def test_blake2s_emptymsg():
    import hashlib

    data = b""
    blake = BLAKE2s(data=data)

    blake_std = hashlib.blake2s(data)

    assert blake.digest() == blake_std.digest()
    assert blake.hexdigest() == blake_std.hexdigest()


def test_blake2s_keyed():
    import hashlib

    data = b"Howdy, Partner" * 50
    key = b"trololo"
    blake = BLAKE2s(data=data, key=key)

    blake_std = hashlib.blake2s(data, key=key)

    assert blake.digest() == blake_std.digest()


def test_blake2s_updated():
    import hashlib

    data = b"Howdy, Partner"
    update_data = b"test1234"
    blake = BLAKE2s(data)
    blake.update(update_data)

    blake_std = hashlib.blake2s(data)
    blake_std.update(update_data)

    assert blake.digest() == blake_std.digest()


def test_blake2s_updated():
    import hashlib

    data = b"XXX, Partner" * 123
    update_data = b"test1234"
    blake = BLAKE2s(data)
    blake.update(update_data)

    blake_std = hashlib.blake2s(data)
    blake_std.update(update_data)

    assert blake.digest() == blake_std.digest()

    blake.update(update_data * 12)
    blake_std.update(update_data * 12)

    assert blake.digest() == blake_std.digest()


def test_blake2s_updated_keyed():
    import hashlib

    data = b"Howdy, Partner"
    update_data = b"test1234"
    key = b"trololo"
    blake = BLAKE2s(data=data, key=key)
    blake.update(update_data)

    blake_std = hashlib.blake2s(data, key=key)
    blake_std.update(update_data)

    assert blake.digest() == blake_std.digest()


def test_blake2s_input_with_blocklen():
    import hashlib

    data = b"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" \
    b"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"

    assert len(data) % 64 == 0

    blake = BLAKE2s(data=data)
    blake_std = hashlib.blake2s(data)

    assert blake.digest() == blake_std.digest()


def test_blake2s_empty():
    import hashlib

    blake = BLAKE2s()
    blake_std = hashlib.blake2s()

    assert blake.digest() == blake_std.digest()