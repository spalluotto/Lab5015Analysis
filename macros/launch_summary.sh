#!/bin/bash

# Vov definitions
declare -A DM_VOVS
#DM_VOVS["DM_9001"]="0.90 1.20 2.00 3.00"
DM_VOVS["DM_9000"]="2.00 3.00"
DM_VOVS["DM_9005"]="2.00 3.00"

for DM in "${!DM_VOVS[@]}"; do
  VOVS=(${DM_VOVS[$DM]})
  echo "=== Processing $DM ==="
  ## single summary plot
  for vov in "${VOVS[@]}"; do
    python3 moduleCharacterizationSummaryPlots.py \
      -m 2 \
      -i ${DM}_Vov${vov}_T18C \
      -o ${DM}_Vov${vov}_T18C \
      -minEn ${DM}
  done
  # many input files
  inputs=$(printf "${DM}_Vov%s_T18C," "${VOVS[@]}")
  inputs=${inputs%,}
  python3 moduleCharacterizationSummaryPlots.py \
    -m 2 \
    -i $inputs \
    -o ${DM}_T18C \
    -minEn ${DM}

  # refBar scan for maximum Vov
  maxVov=${VOVS[-1]}
  for i in {0..15}; do
    python3 moduleCharacterizationSummaryPlots.py \
      -m 2 \
      -i ${DM}_Vov${maxVov}_T18C_refBar${i} \
      -o ${DM}_Vov${maxVov}_T18C_refBar${i} \
      -minEn ${DM}
  done
done

# python3 moduleCharacterizationSummaryPlots.py -m 2 -i DM_FE4587_Vov3.00_T18C_angle40_tripleThreshold_vth2_20 -o DM_FE4587_Vov3.00_T18C_angle40_tripleThreshold_vth2_20 -r 10 -minEn DM_FE4587
