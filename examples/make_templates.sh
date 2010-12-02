#!/bin/bash

echo "import runtime" >templates.py
python parser.py Main <base.html >>templates.py
python parser.py Default <default.html >>templates.py
