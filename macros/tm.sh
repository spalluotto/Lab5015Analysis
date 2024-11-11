#!/bin/bash

for N in {1..30}
do
  # Esegui il comando python con l'argomento -n N
  python plot_tRes_irr.py -n $N
done
