#!/bin/bash

for i in {1..8}; do
    python compareTimeResolution_vs_Vov.py -n $i
done
