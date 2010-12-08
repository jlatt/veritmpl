python = python2.6
PYTHONPATH = .
python_unittests = $(wildcard veritmpl/test/*_tests.py)


all:
	(cd examples && make all)


clean:
	find . -name '*.pyc' -delete
	(cd examples && make clean)


unittest: $(python_unittests)
	@PYTHONPATH=$(PYTHONPATH) $(python) veritmpl/test/__init__.py -v


.PHONY: all clean unittest
