python = python2.6
PYTHONPATH = ..
example_templates = $(wildcard *.html)


all: templates.py


templates.py: $(example_templates)
	$(python) ../veritmpl/compiler.py $(example_templates) >$@


clean:
	rm -f templates.py


.PHONY: all clean
