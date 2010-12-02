Simple Python Templates
=======================

This is a template system in the most literal sense. Templates are compiled to a class with a method that serializes the template to a file object. All the interesting and useful features reside a runtime library tailored specifically to the target language. For now, this is Python.

The only feature of the template language is syntax for variable substitution. Substitutions may be anything stringable or a subclass of the runtime's Template base class. During the substitution, an optional filter callable can modify the strings before they are written to the output stream. For example, an HTML template could use a filter function that encodes strings as HTML.
