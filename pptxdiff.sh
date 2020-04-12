#!/bin/bash

python serialize.py $1 > 1.txt
python serialize.py $2 > 2.txt
diff 1.txt 2.txt