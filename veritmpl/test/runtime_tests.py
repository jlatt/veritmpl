import unittest
from StringIO import StringIO

from veritmpl import runtime


class TestTemplate(unittest.TestCase):
    def setUp(self):
        super(TestTemplate, self).setUp()
        self.t = runtime.Template()

    def tearDown(self):
        super(TestTemplate, self).tearDown()
        self.t.close()

    def get_encoded(self, value):
        out = StringIO()
        self.t.encode(value, out)
        return out.getvalue()

    def test_encode(self):
        self.assertEqual(self.get_encoded('foo'), 'foo')
        self.assertEqual(self.get_encoded(5), '5')


if __name__ == '__main__':
    unittest.main()
