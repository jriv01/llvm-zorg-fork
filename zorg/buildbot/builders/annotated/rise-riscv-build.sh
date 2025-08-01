#!/bin/bash

# Enable Error tracing
set -o errtrace

# Print trace for all commands ran before execution
set -x

ANN_SCRIPT_DIR="$(dirname $0)"
. ${ANN_SCRIPT_DIR}/buildbot-helper.sh

# Ensure all commands pass, and no dereferencing of unset variables.
set -eu
halt_on_failure

# We don't want to build within 'build' (where we start by default).
cd ..
rm -rf build

# Set up variables
LLVM_REVISION="${BUILDBOT_REVISION:-origin/main}"

case "$BUILDBOT_BUILDERNAME" in
  "clang-riscv-rva20-2stage")
    TARGET_CFLAGS="-march=rva20u64"
    export BB_IMG_DIR=$(pwd)/..
    export BB_QEMU_CPU="rv64,zfa=false,zba=false,zbb=false,zbc=false,zbs=false"
    export BB_QEMU_SMP=32
    export BB_QEMU_MEM="64G"
    ;;
  "clang-riscv-rva23-evl-vec-2stage")
    TARGET_CFLAGS="-march=rva23u64 -mllvm -prefer-predicate-over-epilogue=predicate-else-scalar-epilogue"
    export BB_IMG_DIR=$(pwd)/..
     # TODO: Switch to specifying rva23u64 once qemu on the builder is
     # upgraded to a version that recognises it.
    export BB_QEMU_CPU="rv64,zba=true,zbb=true,zbc=false,zbs=true,zfhmin=true,v=true,vext_spec=v1.0,zkt=true,zvfhmin=true,zvbb=true,zvkt=true,zihintntl=true,zicond=true,zimop=true,zcmop=true,zcb=true,zfa=true,zawrs=true,rvv_ta_all_1s=true,rvv_ma_all_1s=true,rvv_vl_half_avl=true"
    export BB_QEMU_SMP=32
    export BB_QEMU_MEM="64G"
    ;;
  "clang-riscv-rva23-zvl512b-2stage")
    TARGET_CFLAGS="-march=rva23u64_zvl512b"
    export BB_IMG_DIR=$(pwd)/..
    export BB_QEMU_CPU="rva23s64,vlen=512,rvv_ta_all_1s=true,rvv_ma_all_1s=true,rvv_vl_half_avl=true"
    export BB_QEMU_SMP=32
    export BB_QEMU_MEM="64G"
    ;;
  "clang-riscv-rva23-zvl1024b-2stage")
    TARGET_CFLAGS="-march=rva23u64_zvl1024b"
    export BB_IMG_DIR=$(pwd)/..
    export BB_QEMU_CPU="rva23s64,vlen=1024,rvv_ta_all_1s=true,rvv_ma_all_1s=true,rvv_vl_half_avl=true"
    export BB_QEMU_SMP=32
    export BB_QEMU_MEM="64G"
    ;;
  "clang-riscv-x60-mrvv-vec-bits-2stage")
    TARGET_CFLAGS="-mcpu=spacemit-x60 -mrvv-vector-bits=zvl"
    export BB_IMG_DIR=$(pwd)/..
    export BB_QEMU_CPU="rva22s64,v=true,zbc=true,zbkc=true,zfh=true,zicond=true,zvkt=true,vlen=256,rvv_ta_all_1s=true,rvv_ma_all_1s=true,rvv_vl_half_avl=true"
    export BB_QEMU_SMP=32
    export BB_QEMU_MEM="64G"
    ;;
  *)
    echo "Unrecognised builder name"
    exit 1
esac


# Main builder stages start here

if [ ! -d llvm ]; then
  build_step "Cloning llvm-project repo"
  git clone --progress https://github.com/llvm/llvm-project.git llvm
fi

build_step "Updating llvm-project repo"
git -C llvm fetch --prune origin
git -C llvm reset --hard "${LLVM_REVISION}"

# We unconditionally clean (i.e. don't check BUILDBOT_CLOBBER=1) as the script
# hasn't been tested without cleaning after each build.
build_step "Cleaning last build"
rm -rf stage1 stage2 llvm-test-suite-build

build_step "llvm-project cmake stage 1"
cmake -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DLLVM_ENABLE_ASSERTIONS=True \
  -DLLVM_LIT_ARGS="-v" \
  -DCMAKE_C_COMPILER=clang \
  -DCMAKE_CXX_COMPILER=clang++ \
  -DLLVM_ENABLE_LLD=True \
  -DLLVM_TARGETS_TO_BUILD="RISCV" \
  -DCMAKE_C_COMPILER_LAUNCHER=ccache \
  -DCMAKE_CXX_COMPILER_LAUNCHER=ccache \
  -DLLVM_ENABLE_PROJECTS="lld;clang;llvm" \
  -B stage1 \
  -S llvm/llvm

build_step "llvm-project build stage 1"
cmake --build stage1

build_step "llvm-project cmake stage 2"
cat - <<EOF > stage1-toolchain.cmake
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSROOT $(pwd)/../rvsysroot)
set(CMAKE_C_COMPILER_TARGET riscv64-linux-gnu)
set(CMAKE_CXX_COMPILER_TARGET riscv64-linux-gnu)
set(CMAKE_C_FLAGS_INIT "$TARGET_CFLAGS")
set(CMAKE_CXX_FLAGS_INIT "$TARGET_CFLAGS")
set(CMAKE_LINKER_TYPE LLD)
set(CMAKE_C_COMPILER $(pwd)/stage1/bin/clang)
set(CMAKE_CXX_COMPILER $(pwd)/stage1/bin/clang++)
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)
EOF
cmake -G Ninja \
  -DCMAKE_BUILD_TYPE=Release \
  -DLLVM_ENABLE_ASSERTIONS=True \
  -DLLVM_LIT_ARGS="-v" \
  -DLLVM_NATIVE_TOOL_DIR=$(pwd)/stage1/bin \
  -DLLVM_BUILD_TESTS=True \
  -DPython3_EXECUTABLE=/usr/bin/python3 \
  -DLLVM_EXTERNAL_LIT="$(pwd)/llvm-zorg/buildbot/riscv-rise/lit-on-qemu" \
  -DLLVM_ENABLE_PROJECTS="lld;clang;clang-tools-extra;llvm" \
  -DCMAKE_TOOLCHAIN_FILE=$(pwd)/stage1-toolchain.cmake \
  -DLLVM_HOST_TRIPLE=riscv64-unknown-linux-gnu \
  -S llvm/llvm \
  -B stage2

build_step "llvm-project build stage 2"
cmake --build stage2

build_step "llvm-project check-all"
cmake --build stage2 --target check-all

# TODO: Evaluate running the test suite immediately after stage1 as it
# executes very quickly and could provide rapid "fail fast" feedback.
if [ ! -d llvm-test-suite ]; then
  build_step "Cloning llvm-test-suite repo"
  git clone --progress https://github.com/llvm/llvm-test-suite.git
fi

build_step "Updating llvm-test-suite repo"
git -C llvm-test-suite fetch --prune origin
git -C llvm-test-suite reset --hard origin/main

build_step "llvm-test-suite cmake"
export QEMU_LD_PREFIX="$(pwd)/../rvsysroot"
export QEMU_CPU="$BB_QEMU_CPU"
cmake -G Ninja \
  --toolchain=$(pwd)/stage1-toolchain.cmake \
  -DCMAKE_BUILD_TYPE=Release \
  -DTEST_SUITE_LIT=$(pwd)/stage1/bin/llvm-lit \
  -DTEST_SUITE_LIT_FLAGS=-v \
  -DTEST_SUITE_COLLECT_CODE_SIZE=OFF \
  -DTEST_SUITE_COLLECT_COMPILE_TIME=OFF \
  -DTEST_SUITE_USER_MODE_EMULATION=ON \
  -S llvm-test-suite \
  -B llvm-test-suite-build

build_step "llvm-test-suite build"
cmake --build llvm-test-suite-build

build_step "llvm-test-suite check"
cmake --build llvm-test-suite-build --target check
