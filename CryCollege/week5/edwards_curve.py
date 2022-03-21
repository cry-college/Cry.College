from CryCollege.week3.elliptic_curve import AffinePoint, EllipticCurve
from CryCollege.week2.finitefield import PrimeField

class EdwardsCurve(EllipticCurve):

    def __init__(self, d, field, a=1):
        """
        General Edwards Curve.
        If a!=1, the curve is twisted.
        """
        self.field = field
        self.d = field(d)
        self.a = field(a)
        # By definition, so we can do the addition as below
        self.neutral_element = AffinePoint(self, 0, 1)

    def is_on_curve(self, P):
        x_sq = P.x**2
        y_sq = P.y**2
        return (self.a * x_sq + y_sq) == (1 + self.d * x_sq * y_sq)

    def add(self, P, Q):
        """
        Sum of points P and Q.
        https://en.wikipedia.org/wiki/Edwards_curve#The_group_law
        """
        raise NotImplementedError("TODO: Implement me plx")

    def __str__(self):
        return "{}x^2 + y^2 = 1 + {}x^2y^2 mod {}".format(self.a, self.d, self.field.mod)


def test_curve41417():
    # Curve41417 is an edwards curve
    # https://safecurves.cr.yp.to/equation.html
    field = PrimeField(2 ** 414 - 17)
    Curve41417 = EdwardsCurve(3617, field)

    # We can find its base point online
    # https://safecurves.cr.yp.to/base.html
    G = AffinePoint(
        Curve41417,
        # x coordinate
        0x1a334905141443300218c0631c326e5fcd46369f44c03ec7f57ff35498a4ab4d6d6ba111301a73faa8537c64c4fd3812f3cbc595,
        # y coordinate
        0x22,
        # order
        0x7ffffffffffffffffffffffffffffffffffffffffffffffffffeb3cc92414cf706022b36f1c0338ad63cf181b0e71a5e106af79
    )
    assert (Curve41417.is_on_curve(G))
    assert ((G.order + 1) * G == G)
