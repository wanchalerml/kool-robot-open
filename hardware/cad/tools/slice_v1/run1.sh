#!/bin/bash
# $1 = job stl  $2 = profile  -> prints grams
stl="$1"; prof="$2"; out="${stl%.stl}.gcode"
C="--nozzle-diameter 0.4 --filament-diameter 1.75 --bed-shape 0x0,256x0,256x256,0x256 --max-print-height 256 --center 128,128 --skirts 0 --brim-width 0 --support-material --support-material-style organic --support-material-buildplate-only --support-material-threshold 45 --fill-pattern gyroid --top-solid-layers 5 --bottom-solid-layers 4 --first-layer-height 0.2 --dont-arrange"
case $prof in
 pla_shell)     P="--layer-height 0.16 --perimeters 3 --fill-density 15% --filament-density 1.31";;
 pla_black)     P="--layer-height 0.16 --perimeters 3 --fill-density 15% --filament-density 1.26";;
 petgcf_struct) P="--layer-height 0.2 --perimeters 5 --fill-density 40% --filament-density 1.25";;
 petgcf_joint)  P="--layer-height 0.2 --perimeters 4 --fill-density 40% --filament-density 1.25";;
 petgcf_light)  P="--layer-height 0.2 --perimeters 3 --fill-density 20% --filament-density 1.25";;
 pahtcf_beam)   P="--layer-height 0.2 --perimeters 6 --fill-density 60% --filament-density 1.06";;
 pahtcf_struct) P="--layer-height 0.2 --perimeters 4 --fill-density 40% --filament-density 1.06";;
 tpu)           P="--layer-height 0.2 --perimeters 3 --fill-density 20% --filament-density 1.22";;
 pc_face)       P="--layer-height 0.16 --perimeters 3 --fill-density 15% --filament-density 1.20";;
esac
prusa-slicer --export-gcode $C $P --output "$out" "$stl" >"${stl%.stl}.log" 2>&1
g=$(grep -m1 "^; filament used \[g\]" "$out" | awk -F= '{print $2}')
s=$(grep -m1 "^; total filament used for wipe tower\|support" /dev/null)
t=$(grep -m1 "estimated printing time (normal mode)" "$out" | awk -F= '{print $2}')
echo "$stl|$prof|$g|$t"
rm -f "$out"
