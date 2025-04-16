cmake_minimum_required(VERSION 3.15)

project(RedPitaya_Metrics C CXX)

# --- Cross-compilation setup for RedPitaya ---
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR arm)
set(CMAKE_SYSROOT $ENV{HOME}/redpitaya-sysroot)
set(CMAKE_C_COMPILER arm-linux-gnueabihf-gcc)
set(CMAKE_CXX_COMPILER arm-linux-gnueabihf-g++)

# --- Python discovery for libqualia-neuralnetwork ---
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

# --- ARM Cortex-A9 + NEON optimization flags ---
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

# --- Linker optimizations ---
add_link_options(
  -Wl,--gc-sections
  -Wl,--print-memory-usage
)

# --- Add libqualia-neuralnetwork ---
add_subdirectory(${LIBQUALIA_NEURALNETWORK_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR}/libqualia-neuralnetwork)

# --- Executable: main ---
add_executable(main main.cpp)
target_compile_features(main PRIVATE cxx_std_17)
target_link_libraries(main PUBLIC qualia-neuralnetwork)

# --- Executable: single ---
add_executable(single single.cpp)
target_compile_features(single PRIVATE cxx_std_17)
target_link_libraries(single PUBLIC qualia-neuralnetwork)

# --- Executable: main_metrics (RedPitaya runtime integration) ---
add_executable(main_metrics main_metrics.cpp)
target_compile_features(main_metrics PRIVATE cxx_std_17)

# Include directories
target_include_directories(main_metrics PRIVATE
  $ENV{HOME}/redpitaya-sysroot/usr/include
  $ENV{HOME}/redpitaya-sysroot/opt/redpitaya/include
  ${MODEL_DIR}
  ${MODEL_DIR}/include
)

# Link directories
target_link_directories(main_metrics PRIVATE
  $ENV{HOME}/redpitaya-sysroot/usr/lib
  $ENV{HOME}/redpitaya-sysroot/usr/lib/arm-linux-gnueabihf
  $ENV{HOME}/redpitaya-sysroot/opt/redpitaya/lib
)

# Link libraries
target_link_libraries(main_metrics PRIVATE
  qualia-neuralnetwork
  m
  pthread
  rt
  i2c
  rp
  rp-i2c
  rp-hw
  rp-hw-calib
  rp-hw-profiles
)

# RPath-link to help resolve indirect dependencies
add_link_options(
  -Wl,-rpath-link=$ENV{HOME}/redpitaya-sysroot/usr/lib
  -Wl,-rpath-link=$ENV{HOME}/redpitaya-sysroot/usr/lib/arm-linux-gnueabihf
  -Wl,-rpath-link=$ENV{HOME}/redpitaya-sysroot/opt/redpitaya/lib
)
