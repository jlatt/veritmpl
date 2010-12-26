#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from veritmpl import compiler


class CompilerTestCase(unittest.TestCase):
    """Test functions in the compiler module."""

    def test_parse(self):
        """Test parsing a simple template."""
        tokens = compiler.parse('foo{{ bar }}baz')
        tokens = list(tokens)
        self.assertEquals(len(tokens), 3)

        tokens = compiler.parse('{{ foo }}bar')
        tokens = list(tokens)
        self.assertEquals(len(tokens), 2)

        tokens = compiler.parse('foo{{ bar }}')
        tokens = list(tokens)
        self.assertEquals(len(tokens), 2)

    def test_compile_empty_template(self):
        """Test compilation of an empty token stream."""
        out = compiler.compile_template(class_name='Test', tokens=[])
        self.assertEquals(
            out.getvalue(),
            """import veritmpl.runtime


class Test(veritmpl.runtime.Template):
	def __call__(self, out):
		return out

	expected_kwargs = set([])
""")
