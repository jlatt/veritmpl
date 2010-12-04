all: examples/templates.py

clean:
	find . -name '*.pyc' -delete
	rm -f examples/templates.py

PYTHONPATH = $(PYTHONPATH):.
example_templates = $(wildcard examples/*.html)

examples/templates.py: $(example_templates)
	python veritmpl/compiler.py -t 'veritmpl.html.HTMLTemplate' $(example_templates) >$@

.PHONY: clean
