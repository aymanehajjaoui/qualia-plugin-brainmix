cmake_minimum_required(VERSION 3.15)

project(RedPitaya C CXX)

# Use RedPitaya cross-compiler
set(CMAKE_C_COMPILER arm-linux-gnueabihf-gcc)
set(CMAKE_CXX_COMPILER arm-linux-gnueabihf-g++)

# Python discovery to locate libqualia-neuralnetwork
set(Python3_FIND_STRATEGY "LOCATION")
set(Python3_FIND_UNVERSIONED_NAMES FIRST)
find_package(Python3 REQUIRED COMPONENTS Interpreter)

message(STATUS "Searching for libqualia-neuralnetwork sources")
execute_process(
  COMMAND ${Python3_EXECUTABLE} -c "from importlib.resources import files; print(files('libqualia-neuralnetwork'))"
  RESULT_VARIABLE LIBQUALIA_NEURALNETWORK_RESULT
  OUTPUT_VARIABLE LIBQUALIA_NEURALNETWORK_SOURCE_DIR
  ERROR_VARIABLE LIBQUALIA_NEURALNETWORK_ERROR
  OUTPUT_STRIP_TRAILING_WHITESPACE
  ERROR_STRIP_TRAILING_WHITESPACE
)

if (NOT "${LIBQUALIA_NEURALNETWORK_ERROR}" STREQUAL "")
  message(FATAL_ERROR ${LIBQUALIA_NEURALNETWORK_ERROR})
endif()
if (NOT ${LIBQUALIA_NEURALNETWORK_RESULT} EQUAL 0)
  message(FATAL_ERROR ${LIBQUALIA_NEURALNETWORK_RESULT})
endif()
message(STATUS "Found libqualia-neuralnetwork: ${LIBQUALIA_NEURALNETWORK_SOURCE_DIR}")

# Optimization flags for ARM Cortex-A9 + NEON
add_compile_options(
  -Wall
  -O3
  -mfpu=neon
  -mfloat-abi=hard
  -march=armv7-a
  -mtune=cortex-a9
  -ffast-math
  -funsafe-math-optimizations
  -fdata-sections
  -ffunction-sections
)

add_link_options(
  -Wl,--gc-sections
  -Wl,--print-memory-usage
)

# Add libqualia-neuralnetwork
add_subdirectory(${LIBQUALIA_NEURALNETWORK_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR}/libqualia-neuralnetwork)