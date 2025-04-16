#!/bin/sh

# Copyright 2021 (c) Pierre-Emmanuel Novac <penovac@unice.fr>
# Université Côte d'Azur, CNRS, LEAT. All rights reserved.

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <C model directory>" 1>&2
    exit 1
fi

MODEL_DIR="$1"

# RedPitaya cross-compiler
CXX=arm-linux-gnueabihf-g++
SYSROOT="$HOME/redpitaya-sysroot"

CFLAGS="-Wall -O3 -mfpu=neon -mfloat-abi=hard -march=armv7-a -mtune=cortex-a9 -ffast-math -funsafe-math-optimizations"
CFLAGS="$CFLAGS --sysroot=$SYSROOT"
CFLAGS="$CFLAGS -I$SYSROOT/opt/redpitaya/include"

LDFLAGS="--sysroot=$SYSROOT -L$SYSROOT/opt/redpitaya/lib -lrp -lrp-i2c -lrp-hw -lrp-hw-calib -lrp-hw-profiles -lpthread -lrt -lm"

# Build main
$CXX $CFLAGS -std=c++17 -o main main.cpp "$MODEL_DIR/model.c" \
  -I"$MODEL_DIR" -I"$MODEL_DIR/include" -lm

# Build single
$CXX $CFLAGS -std=c++17 -o single single.cpp "$MODEL_DIR/model.c" \
  -I"$MODEL_DIR" -I"$MODEL_DIR/include" -lm

# Build rp (with Red Pitaya headers/libs)
$CXX $CFLAGS -std=c++17 -o main_metrics main_metrics.cpp "$MODEL_DIR/model.c" \
  -I"$MODEL_DIR" -I"$MODEL_DIR/include" $LDFLAGS
