#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from veritmpl import html


class HTMLEscapeTestCase(unittest.TestCase):
    def assert_html_escape(self, expected, s):
        self.assertEqual(expected, html.escape(s))

    def test_basic(self):
        """Test the basic functionality of html.escape()."""
        self.assert_html_escape('foobar', 'foobar')
        self.assert_html_escape('foo&amp;bar', 'foo&bar')
        self.assert_html_escape('foo&quot;something&quot;', 'foo"something"')
        self.assert_html_escape('&lt;&gt;', '<>')
        self.assert_html_escape('&raquo;&laquo;', '»«')


class HTMLAttrsTestCase(unittest.TestCase):
    def assert_attrs(self, expected, *args, **kwargs):
        self.assertEqual(expected, html.attrs(*args, **kwargs))

    def test_basic(self):
        """Test basic functionality of attrs()."""
        self.assert_attrs('foo="bar"', foo='bar')
        self.assert_attrs('foo', 'foo')
        self.assert_attrs('foo', foo=True)

    def test_lists(self):
        """Test conversion of lists/tuples to space-separated strings."""
        self.assert_attrs('class="foo bar baz"', class_=('foo', 'bar', 'baz'))


    def test_tag(self):
        """Test tag generation.
        This is basically attrs(), so the test is short.

        """
        self.assertEqual('<ol class="flat prefix">', html.tag('ol', class_=('flat', 'prefix')))


if __name__ == '__main__':
    unittest.main()
