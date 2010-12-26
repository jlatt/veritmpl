import unittest
from StringIO import StringIO

from veritmpl import runtime


class TestTemplate(unittest.TestCase):
    def test_init(self):
        """Test template instantiation."""
        t = runtime.Template()

    def get_encoded(self, t, value):
        out = StringIO()
        t.encode(value, out)
        return out.getvalue()

    encode_tests = (
        ('foo', 'foo'),
        (5, '5'),
        ('', ''),
        (None, ''),
        )

    def test_encode(self):
        """Test string encoding in a standard template."""
        t = runtime.Template()
        for s, expected in self.encode_tests:
            self.assertEqual(self.get_encoded(t, s), expected)


class TestLiteral(unittest.TestCase):
    def test_init(self):
        """Test literal instantiation."""
        l = runtime.Literal()

    def test_redundant_cast(self):
        """Test redundant casting of a literal."""
        l = runtime.Literal()
        self.assertEqual(l, runtime.Literal(l))


if __name__ == '__main__':
    unittest.main()
