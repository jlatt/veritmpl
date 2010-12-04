#!/bin/bash
PYTHONPATH="$PYTHONPATH:../"
python ../veritmpl/compiler.py -t 'veritmpl.html.HTMLTemplate' base.html default.html
