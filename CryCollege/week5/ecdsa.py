import pytest

from CryCollege.week2.finitefield import PrimeField
from CryCollege.week3.elliptic_curve import AffinePoint
from CryCollege.week3.curves import CurveP256
import hashlib
import random

rng = random.SystemRandom()


class ECDSA:
    def __init__(self, curve, G, sk=None):
        self.curve = curve
        self.G = G
        try:
            self.qfield = PrimeField(G.order)
        except AttributeError:
            raise ValueError("Generator does not have an `order` attribute.")
        self.qfield = PrimeField(G.order)
        self.sk = sk

    def _bits2int(self, message):
        message = int.from_bytes(message, 'big')
        blen = message.bit_length()
        qlen = self.qfield.mod.bit_length()
        if blen > qlen:
            return message >> blen-qlen
        return message

    def public_key(self):
        """
        :return: public key
        """
        if not self.sk:
            raise ValueError("Secret key not set")
        p = self.sk * self.G
        return p.x, p.y

    def sign(self, message, nonce=None, hashfunction=hashlib.sha256):
        """
        Create a signature for the provided message using the provided hashfunction and nonce.
        If the nonce is None a random nonce should be created using the secure random number generator rng.
        """
        if not self.sk:
            raise ValueError("Secret key not set")

        h = self.qfield(self._bits2int(hashfunction(message).digest()))

        if nonce is None:
            nonce = rng.randint(1, self.qfield.mod-1)

        nonce = self.qfield(nonce)

        raise NotImplementedError("TODO: Implement me plx")

    def verify(self, message, signature, public_key, hashfunction=hashlib.sha256):
        """
        Verify the provided signature using the provided public key.
        :return: True if signature is valid, False else
        """
        if isinstance(public_key, tuple) and len(public_key) == 2:
            public_key = AffinePoint(self.curve, public_key[0], public_key[1])
        
        raise NotImplementedError("TODO: Implement me plx")


# Tests Start here
@pytest.fixture
def curve_params():
    # Taken from official test vectors
    curve = CurveP256
    generator = CurveP256.gen
    sk = 0xC9AFA9D845BA75166B5C215767B1D6934E50C3DB36E89B127B8A622B120F6721
    return curve, generator, sk


def test_ecdsa(curve_params):
    curve, generator, sk = curve_params
    ecdsa = ECDSA(
        curve,
        generator,
        sk=sk
    )

    public_key = ecdsa.public_key()

    assert public_key == (0x60FED4BA255A9D31C961EB74C6356D68C049B8923B61FA6CE669622E60F29FB6, 0x7903FE1008B8BC99A41AE9E95628BC64F2F1B20C2D7E9F5177A3C294D4462299)
    signature = ecdsa.sign(b"sample", 0xA6E3C57DD01ABE90086538398355DD4C3B17AA873382B0F24D6129493D8AAD60)
    assert signature == (0xEFD48B2AACB6A8FD1140DD9CD45E81D69D2C877B56AAF991C34D0EA84EAF3716, 0xF7CB1C942D657C41D436C7A1B6E29F65F3E900DBB9AFF4064DC4AB2F843ACDA8)


def test_pubkey_verif_withou_sk(curve_params):
    curve, generator, _ = curve_params
    ecdsa = ECDSA(curve, generator)

    signature = (0xEFD48B2AACB6A8FD1140DD9CD45E81D69D2C877B56AAF991C34D0EA84EAF3716, 0xF7CB1C942D657C41D436C7A1B6E29F65F3E900DBB9AFF4064DC4AB2F843ACDA8)
    pubkey = (0x60FED4BA255A9D31C961EB74C6356D68C049B8923B61FA6CE669622E60F29FB6, 0x7903FE1008B8BC99A41AE9E95628BC64F2F1B20C2D7E9F5177A3C294D4462299)
    assert ecdsa.verify(b"sample", signature, pubkey)


def test_long_message(curve_params):
    curve, generator, sk = curve_params
    ecdsa = ECDSA(curve, generator, sk=sk)

    message = b"""
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. In egestas erat imperdiet sed euismod nisi porta lorem mollis. Sapien pellentesque habitant morbi tristique senectus et netus. Massa tempor nec feugiat nisl pretium fusce id velit ut. Adipiscing enim eu turpis egestas pretium aenean pharetra. Dictumst vestibulum rhoncus est pellentesque elit. Felis eget nunc lobortis mattis aliquam faucibus. Ullamcorper malesuada proin libero nunc consequat interdum. Tortor at risus viverra adipiscing at in tellus integer feugiat. Turpis in eu mi bibendum neque.

Ut etiam sit amet nisl purus. Nec tincidunt praesent semper feugiat nibh sed pulvinar. Sed viverra tellus in hac habitasse platea dictumst vestibulum. Et tortor at risus viverra adipiscing. Faucibus et molestie ac feugiat. Morbi tristique senectus et netus et malesuada fames ac turpis. Cursus risus at ultrices mi tempus imperdiet. Vitae tortor condimentum lacinia quis vel eros donec ac odio. Egestas pretium aenean pharetra magna. Aliquet porttitor lacus luctus accumsan tortor posuere ac ut. Neque aliquam vestibulum morbi blandit. Laoreet id donec ultrices tincidunt arcu non sodales neque sodales. Proin libero nunc consequat interdum varius sit amet mattis vulputate. Ultricies tristique nulla aliquet enim tortor at auctor urna nunc. Eget est lorem ipsum dolor. Risus viverra adipiscing at in. At elementum eu facilisis sed odio morbi quis commodo odio. Elit at imperdiet dui accumsan sit amet nulla. Facilisis leo vel fringilla est ullamcorper. Et netus et malesuada fames ac turpis egestas sed.

Mauris rhoncus aenean vel elit. Id leo in vitae turpis. Sodales neque sodales ut etiam. Sit amet consectetur adipiscing elit ut. Gravida quis blandit turpis cursus in hac habitasse platea dictumst. Vivamus arcu felis bibendum ut tristique. Lorem ipsum dolor sit amet consectetur adipiscing elit ut aliquam. Ipsum consequat nisl vel pretium lectus quam id leo. Gravida quis blandit turpis cursus in hac. Arcu dui vivamus arcu felis bibendum. Et odio pellentesque diam volutpat commodo sed egestas egestas. At augue eget arcu dictum. Sed faucibus turpis in eu mi bibendum neque egestas.

Neque convallis a cras semper auctor neque vitae tempus. Sit amet risus nullam eget felis eget nunc lobortis. Venenatis a condimentum vitae sapien pellentesque habitant morbi. Nulla pellentesque dignissim enim sit amet. Fames ac turpis egestas integer eget aliquet. Eget velit aliquet sagittis id. Malesuada fames ac turpis egestas sed tempus. Imperdiet dui accumsan sit amet nulla facilisi morbi. Nullam eget felis eget nunc lobortis mattis aliquam faucibus. Risus nullam eget felis eget nunc lobortis mattis.

Urna duis convallis convallis tellus id interdum velit laoreet id. Lectus quam id leo in. Viverra mauris in aliquam sem fringilla. Id volutpat lacus laoreet non curabitur. Tempor nec feugiat nisl pretium fusce id velit. Mauris nunc congue nisi vitae suscipit tellus mauris a. Duis tristique sollicitudin nibh sit amet commodo nulla. Massa placerat duis ultricies lacus sed turpis tincidunt id aliquet. Amet consectetur adipiscing elit duis tristique sollicitudin nibh. Nullam non nisi est sit amet facilisis. Bibendum at varius vel pharetra vel turpis nunc eget. Et leo duis ut diam quam nulla porttitor massa. Scelerisque eu ultrices vitae auctor eu augue. Mattis molestie a iaculis at erat.

Diam maecenas ultricies mi eget mauris pharetra et. Sit amet porttitor eget dolor morbi non arcu. Pellentesque habitant morbi tristique senectus et netus et. Elit ut aliquam purus sit amet luctus venenatis. Blandit volutpat maecenas volutpat blandit aliquam. Porttitor leo a diam sollicitudin tempor id eu. Vitae aliquet nec ullamcorper sit amet risus nullam eget felis. Massa ultricies mi quis hendrerit. Amet massa vitae tortor condimentum lacinia quis. Eu ultrices vitae auctor eu. Blandit massa enim nec dui. Integer quis auctor elit sed. Ut consequat semper viverra nam libero. Donec ultrices tincidunt arcu non. Dignissim cras tincidunt lobortis feugiat vivamus. Ultrices in iaculis nunc sed augue lacus viverra. Gravida cum sociis natoque penatibus. Nec ultrices dui sapien eget mi proin.

A iaculis at erat pellentesque adipiscing commodo elit at. Amet risus nullam eget felis eget. Porttitor rhoncus dolor purus non. Hac habitasse platea dictumst quisque sagittis purus sit amet volutpat. Mauris vitae ultricies leo integer malesuada nunc vel risus commodo. Aenean et tortor at risus viverra adipiscing. Ipsum dolor sit amet consectetur adipiscing elit. Proin nibh nisl condimentum id. Sit amet consectetur adipiscing elit ut aliquam purus. Id diam vel quam elementum. Orci eu lobortis elementum nibh tellus molestie. Odio ut enim blandit volutpat maecenas volutpat blandit. Enim praesent elementum facilisis leo vel. Suspendisse in est ante in nibh. Fringilla urna porttitor rhoncus dolor purus non enim. Fermentum leo vel orci porta. Arcu non sodales neque sodales. Gravida in fermentum et sollicitudin.

Maecenas sed enim ut sem viverra aliquet eget. Risus nullam eget felis eget. Orci eu lobortis elementum nibh tellus molestie nunc non. Lorem sed risus ultricies tristique nulla aliquet enim tortor at. Morbi non arcu risus quis varius. Eu feugiat pretium nibh ipsum consequat nisl vel pretium. Donec massa sapien faucibus et molestie ac feugiat sed lectus. Massa ultricies mi quis hendrerit dolor. Enim lobortis scelerisque fermentum dui faucibus. Vitae semper quis lectus nulla at volutpat diam ut. In dictum non consectetur a. Sit amet tellus cras adipiscing enim. Et malesuada fames ac turpis. Augue lacus viverra vitae congue eu consequat ac felis donec. Egestas quis ipsum suspendisse ultrices gravida. Consectetur lorem donec massa sapien faucibus et molestie ac feugiat.

Pulvinar sapien et ligula ullamcorper malesuada proin libero nunc. Ultricies lacus sed turpis tincidunt id aliquet risus feugiat in. Ligula ullamcorper malesuada proin libero. Ac tincidunt vitae semper quis. Nam libero justo laoreet sit amet cursus. Tincidunt nunc pulvinar sapien et. Feugiat sed lectus vestibulum mattis ullamcorper. Bibendum est ultricies integer quis. Scelerisque fermentum dui faucibus in ornare quam viverra. Porta nibh venenatis cras sed felis eget velit. Cursus mattis molestie a iaculis at erat pellentesque adipiscing commodo. Nunc eget lorem dolor sed. Consequat id porta nibh venenatis cras sed felis eget.

Nibh sed pulvinar proin gravida hendrerit. Pellentesque habitant morbi tristique senectus et. Velit aliquet sagittis id consectetur purus ut faucibus pulvinar elementum. Non quam lacus suspendisse faucibus interdum. Est sit amet facilisis magna etiam. Massa massa ultricies mi quis hendrerit dolor. Suspendisse ultrices gravida dictum fusce ut placerat orci. Tortor at risus viverra adipiscing at in. Lorem dolor sed viverra ipsum nunc aliquet bibendum. Tempus iaculis urna id volutpat lacus. Enim eu turpis egestas pretium aenean pharetra magna. Sit amet nisl suscipit adipiscing bibendum est ultricies integer quis. Suspendisse interdum consectetur libero id faucibus nisl. Placerat orci nulla pellentesque dignissim enim sit amet venenatis. Molestie nunc non blandit massa enim nec dui nunc. Suspendisse ultrices gravida dictum fusce ut placerat orci nulla pellentesque. Sed elementum tempus egestas sed sed. Blandit cursus risus at ultrices mi tempus. Bibendum neque egestas congue quisque.
"""

    signature = ecdsa.sign(message)

    assert ecdsa.verify(message, signature, ecdsa.public_key())


def test_invalid_signature(curve_params):
    curve, generator, sk = curve_params
    ecdsa = ECDSA(curve, generator, sk=sk)

    assert not ecdsa.verify(b"invalid", (0x1337, 0x1337), ecdsa.public_key())