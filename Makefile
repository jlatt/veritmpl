python = python2.6
PYTHONPATH = .
example_templates = $(wildcard examples/*.html)
python_unittests = $(wildcard veritmpl/test/*_tests.py)


all: examples/templates.py


clean:
	find . -name '*.pyc' -delete
	rm -f examples/templates.py



examples/templates.py: $(example_templates)
	$(python) veritmpl/compiler.py -t 'veritmpl.html.HTMLTemplate' $(example_templates) >$@


unittest: $(python_unittests)
	PYTHONPATH=$(PYTHONPATH) $(python) veritmpl/test/__init__.py


.PHONY: clean test
