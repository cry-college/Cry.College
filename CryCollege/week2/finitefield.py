import pytest


def input_to_element(func):
    def cast_wrapper(self, arg, *args, **kwargs):
        if isinstance(arg, int):
            arg = FieldElement(self.field, arg)
        elif not isinstance(arg, FieldElement):
            raise ValueError("Can't cast type {} to FieldElement.".format(arg))
        elif self.field != arg.field:
            raise ValueError("Elements are in different fields!")
        return func(self, arg)
    return cast_wrapper


class PrimeField:
    def __init__(self, mod):
        self.mod = mod

    def __call__(self, *args, **kwargs):
        return FieldElement(self, args[0])

    def add(self, a, b):
        """
        Add two numbers in the field and return the reduced field element.
        """
        raise NotImplementedError("TODO: Implement me plx")

    def sub(self, a, b):
        """
        Subtract two numbers in the field and return the reduced field element.
        """
        raise NotImplementedError("TODO: Implement me plx")

    def mul(self, a, b):
        """
        Multiply two numbers in the field and return the reduced field element.
        """
        raise NotImplementedError("TODO: Implement me plx")

    def div(self, a, b):
        """
        Divide a by b
        """
        raise NotImplementedError("TODO: Implement me plx")

    def equiv(self, a, b):
        """
        Check if two numbers are equivalent in the field.
        """
        raise NotImplementedError("TODO: Implement me plx")

    def pow(self, base, exponent):
        """
        Calculate the exponentiation base**exponent within the field.
        Uses square and multiply.
        """
        if isinstance(exponent, FieldElement):
            exponent = exponent.elem
        if not isinstance(exponent, int):
            raise ValueError("Only integers allowed as exponents.")
        
        raise NotImplementedError("TODO: Implement me plx")

    def reduce(self, a):
        """
        Return the smallest representative of number a within the field.
        """
        raise NotImplementedError("TODO: Implement me plx")

    def __str__(self):
        return f"F_{self.mod}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if not isinstance(other, PrimeField):
            return False
        return self.mod == other.mod


class FieldElement:
    def __init__(self, field, elem):
        if isinstance(elem, FieldElement):
            elem = elem.elem
        self.field = field
        self.elem = self.field.reduce(elem)

    @input_to_element
    def __add__(self, other):
        return FieldElement(
            self.field,
            self.field.add(self.elem, other.elem)
        )

    def __radd__(self, other):
        return self.__add__(other)

    @input_to_element
    def __sub__(self, other):
        return FieldElement(
            self.field,
            self.field.sub(self.elem, other.elem)
        )

    @input_to_element
    def __rsub__(self, other):
        return FieldElement(
            self.field,
            self.field.sub(other.elem, self.elem)
        )

    def __mul__(self, other):
        if isinstance(other, int):
            other = FieldElement(self.field, other)
        elif not isinstance(other, FieldElement):
            # Maybe the "other" has a working __rmul__ implementation
            return other.__rmul__(self.elem)

        return FieldElement(
            self.field,
            self.field.mul(self.elem, other.elem)
        )

    @input_to_element
    def __rdiv__(self, other):
        return FieldElement(
            self.field,
            self.field.div(other.elem, self.elem)
        )

    def __rmul__(self, other):
        return self.__mul__(other)

    def __eq__(self, other):
        if isinstance(other, int):
            other = self.field(other)
        elif not isinstance(other, FieldElement):
            return False
        return self.field == other.field and self.field.equiv(self.elem, other.elem)

    def __pow__(self, power, modulo=None):
        return FieldElement(
            self.field,
            self.field.pow(self.elem, power)
        )
    
    def to_bytes(self, lenght, byteorder):
        return self.elem.to_bytes(lenght, byteorder)

    def __str__(self):
        return f"{self.elem}"

    def __repr__(self):
        return self.__str__()


# Usage Example
if __name__ == "__main__":
    field = PrimeField(7)
    element_four = field(4)
    print(5 + element_four)
    print(25 * element_four)
    print(element_four ** 18)
    print(element_four ** -1)


# Tests Start here
@pytest.fixture
def fp_seven():
    F = PrimeField(7)
    three = F(3)
    four = F(4)
    return F, three, four


def test_equiv(fp_seven):
    F, three, four = fp_seven
    assert three == F(3)
    assert three == 3
    assert three != four
    assert 3 == three
    assert three == 10


def test_add(fp_seven):
    F, three, four = fp_seven
    assert three + four == F(7)
    assert three + four == F(0)
    assert three + 4 == 7
    assert 4 + three == 7
    assert 4 + four == four + 4


def test_sub(fp_seven):
    F, three, four = fp_seven
    assert three - four - three == F(-4)
    assert 4 - three + four == 5
    assert 4 - three == 1
    assert three - 4 == -1


def test_mul(fp_seven):
    F, three, four = fp_seven
    assert three * four == F(12)
    assert three * four == four * three
    assert three * 4 == 12
    assert four * 5 == 6


def test_pow(fp_seven):
    F, three, four = fp_seven
    assert three**4 == four
    # Element multiplied by its inverse is one
    assert three * three**-1 == 1
    assert three**3 == F(27)
