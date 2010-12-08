import unittest

from veritmpl import html


class HTMLEscapeTestCase(unittest.TestCase):
    def assert_html_escape(self, expected, s):
        self.assertEqual(expected, html.html_escape(s))

    def test_basic(self):
        """Test the basic functionality of html_escape()."""
        self.assert_html_escape('foobar', 'foobar')
        self.assert_html_escape('foo&amp;bar', 'foo&bar')
        self.assert_html_escape('foo&quot;something&quot;', 'foo"something"')
        self.assert_html_escape('&lt;&gt;', '<>')
        self.assert_html_escape('&raquo;&laquo;', u'\u00BB\u00AB')


if __name__ == '__main__':
    unittest.main()
