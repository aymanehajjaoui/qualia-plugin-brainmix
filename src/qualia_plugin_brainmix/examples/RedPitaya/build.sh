#!/bin/sh

# Copyright 2021 (c) Pierre-Emmanuel Novac <penovac@unice.fr>
# Université Côte d'Azur, CNRS, LEAT. All rights reserved.

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <C model directory>" 1>&2
    exit 1
fi

MODEL_DIR="$1"

# RedPitaya cross-compiler
CFLAGS="-Wall -O3 -mfpu=neon -mfloat-abi=hard -march=armv7-a -mtune=cortex-a9 -ffast-math -funsafe-math-optimizations"

$CXX $CFLAGS -std=c++17 -o main main.cpp "$MODEL_DIR/model.c" -I"$MODEL_DIR" -I"$MODEL_DIR/include" -lm

$CXX $CFLAGS -std=c++17 -o single single.cpp "$MODEL_DIR/model.c" -I"$MODEL_DIR" -I"$MODEL_DIR/include" -lm
