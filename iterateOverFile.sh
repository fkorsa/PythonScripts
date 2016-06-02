#!/bin/bash
while read -r p; do
    python ../bakery/phobia.py add "$p"
done < files.txt