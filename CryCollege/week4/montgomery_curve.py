from CryCollege.week3.elliptic_curve import AffinePoint, EllipticCurve
from CryCollege.week2.finitefield import PrimeField


class MontgommeryCurve(EllipticCurve):

    def __init__(self, A, B, field):
        """
        Montgommery Curve, equivalent to twisted edwards basic_curves.
        """
        self.field = field
        self.A = field(A)
        self.B = field(B)
        self.poif = AffinePoint(self, "infinity", "infinity")
        if B * (A ** 2 - 4) == 0:
            raise ValueError("Parameters do not form a montgommery basic_curves")

    def is_on_curve(self, P):
        return self.B * P.y ** 2 == (P.x ** 3 + self.A * P.x ** 2 + P.x)

    def add(self, P, Q):
        """
        Point addition of P and Q on this Montgommery Curve
        """
        if not (self.is_on_curve(P) and self.is_on_curve(Q)):
            raise ValueError("Points not on curve.")
        
        raise NotImplementedError("TODO: Implement me plx")

        return AffinePoint(self, x_new, y_new)

    def __str__(self):
        return "{}y^2 = x^3 + {}x^2 + x mod {}".format(self.B, self.A, self.field.mod)


def test_curve25519():
    # Curve25519 is a Montgommery Curve
    # Every montgommery curves is birationally equivalent
    # to a twisted edwards curve.
    # Which means every montgommery curve can be converted
    # to a twisted edwards curve.
    # Which means Curve25519 can be converted to ed25519 and vice versa.
    field = PrimeField(2 ** 255 - 19)
    Curve25519 = MontgommeryCurve(486662, 1, field)

    # Generator
    G = AffinePoint(
        Curve25519,
        # x coordinate
        9,
        # y coordinate, note that in the actual ECDH setting, we don't need the y coordinate
        # which is a feature of montgommery curves
        14781619447589544791020593568409986887264606134616475288964881837755586237401,
        # order
        0x1000000000000000000000000000000014def9dea2f79cd65812631a5cf5d3ed
    )
    N = AffinePoint(
        Curve25519,
        # x coordinate
        0,
        # y coordinate, note that in the actual ECDH setting, we don't need the y coordinate
        # which is a feature of montgommery curves
        1,
        # order
        0x1000000000000000000000000000000014def9dea2f79cd65812631a5cf5d3ed
    )


    assert (Curve25519.is_on_curve(G))
    assert ((G.order + 1) * G == G)
    print(G, N)
    print(G.order * G)

test_curve25519()
