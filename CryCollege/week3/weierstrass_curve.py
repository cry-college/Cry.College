import pytest

from CryCollege.week3.elliptic_curve import EllipticCurve, AffinePoint
from CryCollege.week2.finitefield import PrimeField


class WeierstrassCurve(EllipticCurve):

    def __init__(self, a, b, field, generator=None, generator_order=None):
        self.field = field
        self.a = self.field(a)
        self.b = self.field(b)
        self.poif = AffinePoint(self, "infinity", "infinity")
        self.singular = (-16 * (4 * self.a ** 3 + 27 * self.b ** 2)) == 0
        
        if generator is not None:
            gen = AffinePoint(self, generator[0], generator[1], generator_order)
            if not self.is_on_curve(gen):
                raise ValueError("Supplied generator is not on curve!")
            self.gen = gen

    def __call__(self, x, y, order=None):
        return AffinePoint(self, x, y, order)

    def calc_y_sq(self, x):
        return x**3 + self.a * x + self.b

    def is_on_curve(self, point):
        return point is self.poif or self.calc_y_sq(point.x) == point.y**2

    def add(self, P, Q):
        """
         Sum of the points P and Q.
         Rules: https://en.wikipedia.org/wiki/Elliptic_curve_point_multiplication
        """
        if not (self.is_on_curve(P) and self.is_on_curve(Q)):
            raise ValueError(
                "Points not on basic_curves {}: {}, {}: {}".format(P, self.is_on_curve(P), Q, self.is_on_curve(Q)))

        raise NotImplementedError("TODO: Implement me plx")

    def __str__(self):
        return "y^2 = x^3 + {}x + {} over {}".format(self.a, self.b, self.field)




def test_tinycurve():
    field = PrimeField(65537)
    a = 13
    b = 1337
    # Define curve
    curve = WeierstrassCurve(a, b, field)
    # Define a point on the curve with order 65198
    gen = curve(9377, 16650, order=65198)
    (gen.order + 1) * gen == gen


def test_NIST_P_256():
    # NIST's Curve P-256
    p = 2**256 - 2**224 + 2**192 + 2**96 - 1
    field = PrimeField(p)
    curveP256 = WeierstrassCurve(
        -3, 
        41058363725152142129326129780047268409114441015993725554835256314039467401291, 
        field,
        generator=(
            48439561293906451759052585252797914202762949526041747995844080717082404635286,
            36134250956749795798585127919587881956611106672985015071877198253568414405109
        ),
        generator_order=115792089210356248762697446949407573529996955224135760342422259061068512044369
    )

    # If we do a scalar multiplication of the generators
    # order with the generator point, we should end up
    # at the neutral element, the point at infinity
    X = curveP256.gen.order * curveP256.gen
    assert(X is curveP256.poif)

    # Since the point at infinity is the neutral element,
    # with order+1 we should en up at the generator.
    X = (curveP256.gen.order + 1) * curveP256.gen
    assert(X == curveP256.gen)