from importlib import reload

from buildbot.plugins import util, steps

from zorg.buildbot.builders import ClangBuilder
from zorg.buildbot.builders import FlangBuilder
from zorg.buildbot.builders import PollyBuilder
from zorg.buildbot.builders import LLDBBuilder
from zorg.buildbot.builders import SanitizerBuilder
from zorg.buildbot.builders import OpenMPBuilder
from zorg.buildbot.builders import SphinxDocsBuilder
from zorg.buildbot.builders import ABITestsuitBuilder
from zorg.buildbot.builders import ClangLTOBuilder
from zorg.buildbot.builders import UnifiedTreeBuilder
from zorg.buildbot.builders import AOSPBuilder
from zorg.buildbot.builders import AnnotatedBuilder
from zorg.buildbot.builders import LLDPerformanceTestsuite
from zorg.buildbot.builders import XToolchainBuilder
from zorg.buildbot.builders import TestSuiteBuilder
from zorg.buildbot.builders import BOLTBuilder

from zorg.buildbot.builders import HtmlDocsBuilder
from zorg.buildbot.builders import DoxygenDocsBuilder

from zorg.buildbot.builders import StagedBuilder

reload(ClangBuilder)
reload(FlangBuilder)
reload(PollyBuilder)
reload(LLDBBuilder)
reload(SanitizerBuilder)
reload(OpenMPBuilder)
reload(SphinxDocsBuilder)
reload(ABITestsuitBuilder)
reload(ClangLTOBuilder)
reload(UnifiedTreeBuilder)
reload(AOSPBuilder)
reload(AnnotatedBuilder)
reload(LLDPerformanceTestsuite)
reload(XToolchainBuilder)
reload(TestSuiteBuilder)
reload(BOLTBuilder)

reload(HtmlDocsBuilder)
reload(DoxygenDocsBuilder)

reload(StagedBuilder)

all = [

# Clang fast builders.

    {'name' : "clang-x86_64-debian-fast",
    'tags'  : ["clang", "fast"],
    'collapseRequests': False,
    'workernames':["gribozavr4"],
    'builddir':"clang-x86_64-debian-fast",
    'factory' : UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    llvm_srcdir="llvm.src",
                    obj_dir="llvm.obj",
                    clean=True,
                    depends_on_projects=['llvm','clang','clang-tools-extra','compiler-rt'],
                    extra_configure_args=[
                        "-DLLVM_CCACHE_BUILD=ON",
                        "-DCOMPILER_RT_BUILD_BUILTINS:BOOL=OFF",
                        "-DCOMPILER_RT_BUILD_ORC:BOOL=OFF",
                        "-DCOMPILER_RT_BUILD_SANITIZERS:BOOL=OFF",
                        "-DCOMPILER_RT_BUILD_XRAY:BOOL=OFF",
                        "-DCOMPILER_RT_INCLUDE_TESTS:BOOL=OFF",
                        "-DCOMPILER_RT_BUILD_LIBFUZZER:BOOL=OFF",
                        "-DCMAKE_C_FLAGS=-Wdocumentation -Wno-documentation-deprecated-sync",
                        "-DCMAKE_CXX_FLAGS=-std=c++11 -Wdocumentation -Wno-documentation-deprecated-sync",
                    ],
                    env={
                        'PATH':'/home/llvmbb/bin/clang-latest/bin:/home/llvmbb/bin:/usr/local/bin:/usr/local/bin:/usr/bin:/bin',
                        'CC': 'clang', 'CXX': 'clang++',
                    })},

    {'name' : "llvm-clang-x86_64-win-fast",
    'tags'  : ["clang", "fast"],
    'collapseRequests': False,
    'workernames' : ["as-builder-3"],
    'builddir': "llvm-clang-x86_64-win-fast",
    'factory' : UnifiedTreeBuilder.getCmakeWithNinjaWithMSVCBuildFactory(
                    vs="autodetect",
                    depends_on_projects=['llvm', 'clang'],
                    clean=True,
                    checks=[
                        "check-llvm-unit",
                        "check-clang-unit"
                    ],
                    extra_configure_args=[
                        "-DLLVM_CCACHE_BUILD=ON",
                        "-DLLVM_ENABLE_WERROR=OFF",
                        "-DLLVM_TARGETS_TO_BUILD=ARM",
                        "-DLLVM_DEFAULT_TARGET_TRIPLE=armv7-unknown-linux-eabihf",
                        "-DLLVM_ENABLE_ASSERTIONS=OFF",
                        "-DLLVM_OPTIMIZED_TABLEGEN=OFF",
                        "-DLLVM_LIT_ARGS=-v --threads=32",
                    ],
                    env={
                        'CCACHE_DIR' : util.Interpolate("%(prop:builddir)s/ccache-db"),
                    })},

    {'name': "llvm-clang-x86_64-sie-ubuntu-fast",
    'tags'  : ["clang", "llvm", "clang-tools-extra", "lld", "cross-project-tests"],
    'collapseRequests': False,
    'workernames': ["sie-linux-worker"],
    'builddir': "llvm-clang-x86_64-sie-ubuntu-fast",
    'factory': UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    depends_on_projects=['llvm','clang','clang-tools-extra','lld','cross-project-tests'],
                    extra_configure_args=[
                        "-DCMAKE_C_COMPILER=gcc",
                        "-DCMAKE_CXX_COMPILER=g++",
                        "-DCMAKE_BUILD_TYPE=Release",
                        "-DCLANG_ENABLE_ARCMT=OFF",
                        "-DCLANG_ENABLE_CLANGD=OFF",
                        "-DLLVM_BUILD_RUNTIME=OFF",
                        "-DLLVM_CCACHE_BUILD=ON",
                        "-DLLVM_INCLUDE_EXAMPLES=OFF",
                        "-DLLVM_DEFAULT_TARGET_TRIPLE=x86_64-scei-ps4",
                        "-DLLVM_ENABLE_ASSERTIONS=ON",
                        "-DLLVM_LIT_ARGS=--verbose -j100 --timeout=900",
                        "-DLLVM_TARGETS_TO_BUILD=X86",
                        "-DLLVM_USE_LINKER=gold"])},

    {'name': "llvm-clang-x86_64-sie-ps5-fast",
    'tags'  : ["clang", "llvm", "clang-tools-extra", "lld", "cross-project-tests"],
    'collapseRequests': False,
    'workernames': ["sie-linux-worker4"],
    'builddir': "llvm-ps5-fast",
    'factory': UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    depends_on_projects=['llvm','clang','clang-tools-extra','lld','cross-project-tests'],
                    extra_configure_args=[
                        "-DCMAKE_C_COMPILER=gcc",
                        "-DCMAKE_CXX_COMPILER=g++",
                        "-DCMAKE_BUILD_TYPE=Release",
                        "-DCLANG_ENABLE_ARCMT=OFF",
                        "-DCLANG_ENABLE_CLANGD=OFF",
                        "-DLLVM_BUILD_RUNTIME=OFF",
                        "-DLLVM_CCACHE_BUILD=ON",
                        "-DLLVM_INCLUDE_EXAMPLES=OFF",
                        "-DLLVM_DEFAULT_TARGET_TRIPLE=x86_64-sie-ps5",
                        "-DLLVM_ENABLE_ASSERTIONS=ON",
                        "-DLLVM_LIT_ARGS=--verbose -j100 --timeout=900",
                        "-DLLVM_TARGETS_TO_BUILD=X86",
                        "-DLLVM_USE_LINKER=gold"])},

# Expensive checks builders.

    {'name' : "llvm-clang-x86_64-expensive-checks-ubuntu",
    'tags'  : ["llvm", "expensive-checks"],
    'workernames' : ["as-builder-4"],
    'builddir': "expensive-checks",
    'factory' : UnifiedTreeBuilder.getCmakeExBuildFactory(
                    depends_on_projects = [
                        'llvm',
                        'lld',
                    ],
                    clean = True,
                    checks = [
                        "check-all"
                    ],
                    cmake_definitions = {
                        "LLVM_CCACHE_BUILD"             : "ON",
                        "LLVM_ENABLE_EXPENSIVE_CHECKS"  : "ON",
                        "LLVM_ENABLE_WERROR"            : "OFF",
                        "LLVM_USE_LINKER"               : "lld-21",
                        "LLVM_LIT_ARGS"                 : "-vv --time-tests",
                        "CMAKE_BUILD_TYPE"              : "Release",
                        "CMAKE_CXX_FLAGS"               : "-U_GLIBCXX_DEBUG -Wno-misleading-indentation",
                    },
                    env = {
                        'CC'            : "clang-21",
                        'CXX'           : "clang++-21",
                        'CCACHE_DIR'    : util.Interpolate("%(prop:builddir)s/ccache-db"),
                        # TMP/TEMP within the build dir (to utilize a ramdisk).
                        'TMP'           : util.Interpolate("%(prop:builddir)s/build"),
                        'TEMP'          : util.Interpolate("%(prop:builddir)s/build"),
                    },
                )
        },

    {'name' : "llvm-clang-x86_64-expensive-checks-win",
    'tags'  : ["llvm", "expensive-checks"],
    'workernames' : ["as-worker-93"],
    'builddir': "llvm-clang-x86_64-expensive-checks-win",
    'factory' : UnifiedTreeBuilder.getCmakeWithNinjaWithMSVCBuildFactory(
                    vs="autodetect",
                    depends_on_projects=["llvm", "lld"],
                    clean=True,
                    extra_configure_args=[
                        "-DLLVM_ENABLE_EXPENSIVE_CHECKS=ON",
                        "-DLLVM_ENABLE_WERROR=OFF",
                        "-DCMAKE_BUILD_TYPE=Debug"])},

    {'name' : "llvm-clang-x86_64-expensive-checks-debian",
    'tags'  : ["llvm", "expensive-checks"],
    'collapseRequests' : False,
    'workernames' : ["gribozavr4"],
    'builddir': "llvm-clang-x86_64-expensive-checks-debian",
    'factory' : UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    depends_on_projects=["llvm", "lld"],
                    clean=True,
                    extra_configure_args=[
                        "-DLLVM_CCACHE_BUILD=ON",
                        "-DLLVM_ENABLE_EXPENSIVE_CHECKS=ON",
                        "-DLLVM_ENABLE_WERROR=OFF",
                        "-DCMAKE_BUILD_TYPE=Release",
                        "-DCMAKE_CXX_FLAGS=-U_GLIBCXX_DEBUG",
                        "-DLLVM_LIT_ARGS=-v -vv -j96"],
                    env={
                        'PATH':'/home/llvmbb/bin/clang-latest/bin:/home/llvmbb/bin:/usr/local/bin:/usr/local/bin:/usr/bin:/bin',
                        'CC': 'clang', 'CXX': 'clang++',
                    })},

# Cross builders.

    {'name' : "llvm-clang-win-x-armv7l",
    'tags'  : ["clang", "llvm", "lld", "clang-tools-extra", "compiler-rt", "libc++", "libc++abi", "libunwind", "cross", "armv7"],
    'workernames' : ["as-builder-1"],
    'builddir': "x-armv7l",
    'factory' : UnifiedTreeBuilder.getCmakeExBuildFactory(
                    depends_on_projects = [
                        'llvm',
                        'compiler-rt',
                        'clang',
                        'clang-tools-extra',
                        'libunwind',
                        'libcxx',
                        'libcxxabi',
                        'lld',
                    ],
                    vs="autodetect",
                    clean=True,
                    checks=[
                        "check-llvm",
                        "check-clang",
                        "check-lld",
                        "check-compiler-rt-armv7-unknown-linux-gnueabihf",
                        "check-unwind-armv7-unknown-linux-gnueabihf",
                        "check-cxxabi-armv7-unknown-linux-gnueabihf",
                        "check-cxx-armv7-unknown-linux-gnueabihf",
                    ],
                    cmake_definitions = {
                        "LLVM_TARGETS_TO_BUILD"         : "ARM",
                        "LLVM_INCLUDE_BENCHMARKS"       : "OFF",
                        "LLVM_CCACHE_BUILD"             : "ON",
                        "LLVM_LIT_ARGS"                 : "-v -vv --threads=32 --time-tests",
                        "TOOLCHAIN_TARGET_TRIPLE"       : "armv7-unknown-linux-gnueabihf",
                        "TOOLCHAIN_TARGET_SYSROOTFS"    : util.Interpolate("%(prop:sysroot_path_tk1)s"),
                        "ZLIB_ROOT"                     : util.Interpolate("%(prop:zlib_root_path)s"),
                        "REMOTE_TEST_HOST"              : util.Interpolate("%(prop:remote_host_tk1)s"),
                        "REMOTE_TEST_USER"              : util.Interpolate("%(prop:remote_user_tk1)s"),
                        "CMAKE_CXX_FLAGS"               : "-D__OPTIMIZE__",
                    },
                    cmake_options = [
                        "-C", util.Interpolate("%(prop:srcdir_relative)s/clang/cmake/caches/CrossWinToARMLinux.cmake"),
                    ],
                    install_dir = "install",
                    env = {
                        'CCACHE_DIR' : util.Interpolate("%(prop:builddir)s/ccache-db"),
                        # TMP/TEMP within the build dir (to utilize a ramdisk).
                        'TMP'        : util.Interpolate("%(prop:builddir)s/build"),
                        'TEMP'       : util.Interpolate("%(prop:builddir)s/build"),
                    },
                )
        },

    {'name' : "llvm-clang-win-x-aarch64",
    'tags'  : ["clang", "llvm", "lld", "clang-tools-extra", "compiler-rt", "libc++", "libc++abi", "libunwind", "cross", "aarch64"],
    'workernames' : ["as-builder-2"],
    'builddir': "x-aarch64",
    'factory' : UnifiedTreeBuilder.getCmakeExBuildFactory(
                    depends_on_projects = [
                        'llvm',
                        'compiler-rt',
                        'clang',
                        'clang-tools-extra',
                        'libunwind',
                        'libcxx',
                        'libcxxabi',
                        'lld',
                    ],
                    vs = "autodetect",
                    clean = True,
                    checks = [
                        "check-llvm",
                        "check-clang",
                        "check-lld",
                        "check-compiler-rt-aarch64-unknown-linux-gnu",
                        "check-unwind-aarch64-unknown-linux-gnu",
                        "check-cxxabi-aarch64-unknown-linux-gnu",
                        "check-cxx-aarch64-unknown-linux-gnu",
                    ],
                    cmake_definitions = {
                        "LLVM_TARGETS_TO_BUILD"         : "AArch64",
                        "LLVM_INCLUDE_BENCHMARKS"       : "OFF",
                        "LLVM_LIT_ARGS"                 : "-v -vv --threads=32 --time-tests",
                        "TOOLCHAIN_TARGET_TRIPLE"       : "aarch64-unknown-linux-gnu",
                        "TOOLCHAIN_TARGET_SYSROOTFS"    : util.Interpolate("%(prop:sysroot_path_agx)s"),
                        "REMOTE_TEST_HOST"              : util.Interpolate("%(prop:remote_host_agx)s"),
                        "REMOTE_TEST_USER"              : util.Interpolate("%(prop:remote_user_agx)s"),
                        "ZLIB_ROOT"                     : util.Interpolate("%(prop:zlib_root_path)s"),
                        "CMAKE_CXX_FLAGS"               : "-D__OPTIMIZE__",
                        "CMAKE_C_COMPILER_LAUNCHER"     : "ccache",
                        "CMAKE_CXX_COMPILER_LAUNCHER"   : "ccache",
                    },
                    cmake_options = [
                        "-C", util.Interpolate("%(prop:srcdir_relative)s/clang/cmake/caches/CrossWinToARMLinux.cmake"),
                    ],
                    install_dir = "install",
                    env = {
                        'CCACHE_DIR' : util.Interpolate("%(prop:builddir)s/ccache-db"),
                    },
                )
        },

# Clang builders.

    {'name': "clang-arm64-windows-msvc",
    'tags' : ["llvm", "clang", "lld"],
    'workernames' : ["linaro-armv8-windows-msvc-04"],
    'builddir': "clang-arm64-windows-msvc",
    'factory' : UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    depends_on_projects=['llvm', 'clang', 'clang-tools-extra',
                                         'lld', 'compiler-rt', 'openmp'],
                    checks=['check-all', 'check-runtimes'],
                    extra_configure_args=[
                        "-DLLVM_TARGETS_TO_BUILD=X86;ARM;AArch64",
                        "-DCLANG_DEFAULT_LINKER=lld",
                        "-DCMAKE_TRY_COMPILE_CONFIGURATION=Release",
                        "-DCOMPILER_RT_BUILD_SANITIZERS=OFF",
                        "-DLLVM_CCACHE_BUILD=ON"])},

    ## ARMv8 check-all
    {'name' : "clang-armv8-quick",
    'tags'  : ["clang"],
    'workernames':["linaro-clang-armv8-quick"],
    'builddir':"clang-armv8-quick",
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                    clean=False,
                    checkout_compiler_rt=False,
                    checkout_lld=False,
                    extra_cmake_args=["-DLLVM_TARGETS_TO_BUILD='ARM'"])},

    ## ARMv7 check-all 2-stage
    {'name' : "clang-armv7-2stage",
    'tags'  : ["clang"],
    'workernames': ["linaro-clang-armv7-2stage"],
    'builddir':"clang-armv7-2stage",
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                    clean=True,
                    checkout_compiler_rt=False,
                    checkout_lld=False,
                    useTwoStage=True,
                    testStage1=True,
                    runTestSuite=True,
                    testsuite_flags=[
                        '--cppflags', '-mcpu=cortex-a15 -marm',
                        '--threads=32', '--build-threads=32'],
                    extra_cmake_args=[
                        "-DCMAKE_C_FLAGS='-mcpu=cortex-a15 -marm'",
                        "-DCMAKE_CXX_FLAGS='-mcpu=cortex-a15 -marm'"])},

    ## ARMv7 run test-suite with GlobalISel enabled
    {'name' : "clang-armv7-global-isel",
    'tags'  : ["clang"],
    'workernames':["linaro-clang-armv7-global-isel"],
    'builddir':"clang-armv7-global-isel",
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                    clean=False,
                    checkout_compiler_rt=False,
                    checkout_lld=False,
                    runTestSuite=True,
                    testsuite_flags=[
                        '--cppflags', '-mcpu=cortex-a15 -marm -O0 -mllvm -global-isel -mllvm -global-isel-abort=0',
                        '--threads=32', '--build-threads=32'])},

    ## ARMv7 VFPv3 check-all 2-stage
    {'name' : "clang-armv7-vfpv3-2stage",
    'tags'  : ["clang"],
    'workernames' : ["linaro-clang-armv7-vfpv3-2stage"],
    'builddir': "clang-armv7-vfpv3-2stage",
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                    clean=True,
                    checkout_compiler_rt=False,
                    checkout_lld=False,
                    useTwoStage=True,
                    testStage1=False,
                    extra_cmake_args=[
                        "-DCMAKE_C_FLAGS='-mcpu=cortex-a15 -mfpu=vfpv3 -marm'",
                        "-DCMAKE_CXX_FLAGS='-mcpu=cortex-a15 -mfpu=vfpv3 -marm'"])},

    ## AArch64 check-all
    {'name' : "clang-aarch64-quick",
    'tags'  : ["clang"],
    'workernames' : ["linaro-clang-aarch64-quick"],
    'builddir': "clang-aarch64-quick",
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                    clean=False,
                    checkout_compiler_rt=False,
                    checkout_lld=False,
                    extra_cmake_args=["-DLLVM_TARGETS_TO_BUILD='AArch64'"])},

    # AArch64 2 stage build with lld, flang, compiler-rt, test-suite and SVE/SME
    # mlir integration tests.
    {'name' : "clang-aarch64-lld-2stage",
    'tags'  : ["lld"],
    'workernames' : ["linaro-clang-aarch64-lld-2stage"],
    'builddir':"clang-aarch64-lld-2stage",
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                clean=True,
                checkout_flang=True,
                checkout_lld=True,
                useTwoStage=True,
                runTestSuite=True,
                env={
                        'NO_STOP_MESSAGE':'1', # For Fortran test-suite
                    },
                testsuite_flags=[
                    '--cppflags', '-mcpu=neoverse-n1 -fuse-ld=lld',
                    '--threads=32', '--build-threads=32'],
                extra_cmake_args=[
                    "-DCMAKE_C_FLAGS='-mcpu=neoverse-n1'",
                    "-DCMAKE_CXX_FLAGS='-mcpu=neoverse-n1'",
                    "-DLLVM_ENABLE_LLD=True",
                    "-DLLVM_LIT_ARGS='-v'",
                    "-DMLIR_INCLUDE_INTEGRATION_TESTS=True",
                    "-DMLIR_RUN_ARM_SVE_TESTS=True",
                    "-DMLIR_RUN_ARM_SME_TESTS=True",
                    "-DARM_EMULATOR_EXECUTABLE=qemu-aarch64"])},

    ## AArch64 run test-suite at -O0 (GlobalISel is now default).
    {'name' : "clang-aarch64-global-isel",
    'tags'  : ["clang"],
    'workernames' : ["linaro-clang-aarch64-global-isel"],
    'builddir': "clang-aarch64-global-isel",
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                    clean=False,
                    checkout_compiler_rt=False,
                    checkout_lld=False,
                    runTestSuite=True,
                    testsuite_flags=[
                        '--cppflags', '-O0',
                        '--threads=32', '--build-threads=32'])},

    ## AArch32 Self-hosting Clang+LLVM check-all + LLD + test-suite
    # Sanitizers build disabled due to PR38690
    {'name' : "clang-armv8-lld-2stage",
    'tags'  : ["lld"],
    'workernames' : ["linaro-clang-armv8-lld-2stage"],
    'builddir': "clang-armv8-lld-2stage",
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                    clean=True,
                    useTwoStage=True,
                    runTestSuite=True,
                    testsuite_flags=[
                        '--cppflags', '-mcpu=neoverse-n1 -fuse-ld=lld',
                        '--threads=32', '--build-threads=32'],
                    extra_cmake_args=[
                        "-DCMAKE_C_FLAGS='-mcpu=neoverse-n1'",
                        "-DCMAKE_CXX_FLAGS='-mcpu=neoverse-n1'",
                        "-DCOMPILER_RT_BUILD_SANITIZERS=OFF",
                        "-DLLVM_ENABLE_LLD=True",
                        # lld tests cause us to hit thread limits
                        "-DLLVM_ENABLE_THREADS=OFF"])},

    # All SVE (as opposed to SVE2) builders are using optimisation flags
    # for Graviton 3 "balanced" from
    # https://github.com/aws/aws-graviton-getting-started/blob/main/c-c++.md.

    # AArch64 Clang+LLVM+RT+LLD check-all + flang + test-suite +
    # mlir-integration-tests w/SVE-Vector-Length-Agnostic Note that in this and
    # other clang-aarch64-sve-* builders we set -mllvm
    # -treat-scalable-fixed-error-as-warning=false to make compiler fail on
    # non-critical SVE codegen issues.  This helps us notice and fix SVE
    # problems sooner rather than later.
    {'name' : "clang-aarch64-sve-vla",
    'tags'  : ["clang"],
    'workernames' : ["linaro-g3-01", "linaro-g3-02", "linaro-g3-03", "linaro-g3-04"],
    'builddir': "clang-aarch64-sve-vla",
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                    clean=False,
                    checkout_flang=True,
                    runTestSuite=True,
                    env={
                        'NO_STOP_MESSAGE':'1', # For Fortran test-suite
                    },
                    testsuite_flags=[
                        '--cppflags', '-mcpu=neoverse-512tvb -mllvm -scalable-vectorization=preferred -mllvm -treat-scalable-fixed-error-as-warning=false -O3',
                        '--cmake-define', 'CMAKE_Fortran_FLAGS=-mcpu=neoverse-512tvb -mllvm -scalable-vectorization=preferred -mllvm -treat-scalable-fixed-error-as-warning=false -O3',
                        '--threads=32', '--build-threads=32'],
                    extra_cmake_args=[
                        "-DCMAKE_C_FLAGS='-mcpu=neoverse-512tvb'",
                        "-DCMAKE_CXX_FLAGS='-mcpu=neoverse-512tvb'",
                        "-DLLVM_ENABLE_LLD=True",
                        "-DMLIR_INCLUDE_INTEGRATION_TESTS=True",
                        "-DMLIR_RUN_ARM_SVE_TESTS=True"])},

    # AArch64 Clang+LLVM+RT+LLD check-all + flang + test-suite 2-stage w/SVE-Vector-Length-Agnostic
    {'name' : "clang-aarch64-sve-vla-2stage",
    'tags'  : ["clang"],
    'workernames' : ["linaro-g3-01", "linaro-g3-02", "linaro-g3-03", "linaro-g3-04"],
    'builddir': "clang-aarch64-sve-vla-2stage",
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                    clean=True,
                    checkout_flang=True,
                    useTwoStage=True,
                    testStage1=False,
                    runTestSuite=True,
                    env={
                        'NO_STOP_MESSAGE':'1', # For Fortran test-suite
                    },
                    testsuite_flags=[
                        '--cppflags', '-mcpu=neoverse-512tvb -mllvm -scalable-vectorization=preferred -mllvm -treat-scalable-fixed-error-as-warning=false -O3',
                        '--cmake-define', 'CMAKE_Fortran_FLAGS=-mcpu=neoverse-512tvb -mllvm -scalable-vectorization=preferred -mllvm -treat-scalable-fixed-error-as-warning=false -O3',
                        '--threads=32', '--build-threads=32'],
                    extra_cmake_args=[
                        "-DCMAKE_C_FLAGS='-mcpu=neoverse-512tvb -mllvm -scalable-vectorization=preferred -mllvm -treat-scalable-fixed-error-as-warning=false'",
                        "-DCMAKE_CXX_FLAGS='-mcpu=neoverse-512tvb -mllvm -scalable-vectorization=preferred -mllvm -treat-scalable-fixed-error-as-warning=false'",
                        "-DLLVM_ENABLE_LLD=True",
                        "-DMLIR_INCLUDE_INTEGRATION_TESTS=True",
                        "-DMLIR_RUN_ARM_SVE_TESTS=True"])},

    # AArch64 Clang+LLVM+RT+LLD check-all + flang + test-suite w/SVE-Vector-Length-Specific
    {'name' : "clang-aarch64-sve-vls",
    'tags'  : ["clang"],
    'workernames' : ["linaro-g3-01", "linaro-g3-02", "linaro-g3-03", "linaro-g3-04"],
    'builddir': "clang-aarch64-sve-vls",
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                    clean=False,
                    checkout_flang=True,
                    runTestSuite=True,
                    env={
                        'NO_STOP_MESSAGE':'1', # For Fortran test-suite
                    },
                    testsuite_flags=[
                        '--cppflags', '-mcpu=neoverse-512tvb -msve-vector-bits=256 -mllvm -treat-scalable-fixed-error-as-warning=false -O3',
                        '--cmake-define', 'CMAKE_Fortran_FLAGS=-mcpu=neoverse-512tvb -msve-vector-bits=256 -mllvm -treat-scalable-fixed-error-as-warning=false -O3',
                        '--threads=32', '--build-threads=32'],
                    extra_cmake_args=[
                        "-DCMAKE_C_FLAGS='-mcpu=neoverse-512tvb'",
                        "-DCMAKE_CXX_FLAGS='-mcpu=neoverse-512tvb'",
                        "-DLLVM_ENABLE_LLD=True",
                        "-DMLIR_INCLUDE_INTEGRATION_TESTS=True",
                        "-DMLIR_RUN_ARM_SVE_TESTS=True"])},

    # AArch64 Clang+LLVM+RT+LLD check-all + flang + test-suite 2-stage w/SVE-Vector-Length-Specific
    {'name' : "clang-aarch64-sve-vls-2stage",
    'tags'  : ["clang"],
    'workernames' : ["linaro-g3-01", "linaro-g3-02", "linaro-g3-03", "linaro-g3-04"],
    'builddir': "clang-aarch64-sve-vls-2stage",
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                    clean=True,
                    checkout_flang=True,
                    useTwoStage=True,
                    testStage1=False,
                    runTestSuite=True,
                    env={
                        'NO_STOP_MESSAGE':'1', # For Fortran test-suite
                    },
                    testsuite_flags=[
                        '--cppflags', '-mcpu=neoverse-512tvb -msve-vector-bits=256 -mllvm -treat-scalable-fixed-error-as-warning=false -O3',
                        '--cmake-define', 'CMAKE_Fortran_FLAGS=-mcpu=neoverse-512tvb -msve-vector-bits=256 -mllvm -treat-scalable-fixed-error-as-warning=false -O3',
                        '--threads=32', '--build-threads=32'],
                    extra_cmake_args=[
                        "-DCMAKE_C_FLAGS='-mcpu=neoverse-512tvb -msve-vector-bits=256 -mllvm -treat-scalable-fixed-error-as-warning=false'",
                        "-DCMAKE_CXX_FLAGS='-mcpu=neoverse-512tvb -msve-vector-bits=256 -mllvm -treat-scalable-fixed-error-as-warning=false'",
                        "-DLLVM_ENABLE_LLD=True",
                        "-DMLIR_INCLUDE_INTEGRATION_TESTS=True",
                        "-DMLIR_RUN_ARM_SVE_TESTS=True"])},

    # All SVE2 builders are using optimisation flags for Graviton 4 "performance" from
    # https://github.com/aws/aws-graviton-getting-started/blob/main/c-c++.md
    # (using balanced would not enable the SVE2 extension).

    {'name' : "clang-aarch64-sve2-vla",
    'tags'  : ["clang"],
    'workernames' : ["linaro-g4-01", "linaro-g4-02"],
    'builddir': "clang-aarch64-sve2-vla",
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                    clean=False,
                    checkout_flang=True,
                    runTestSuite=True,
                    env={
                        'NO_STOP_MESSAGE':'1', # For Fortran test-suite
                    },
                    testsuite_flags=[
                        '--cppflags', '-mcpu=neoverse-v2 -mllvm -scalable-vectorization=preferred -mllvm -treat-scalable-fixed-error-as-warning=false -O3',
                        '--cmake-define', 'CMAKE_Fortran_FLAGS=-mcpu=neoverse-v2 -mllvm -scalable-vectorization=preferred -mllvm -treat-scalable-fixed-error-as-warning=false -O3',
                        '--threads=48', '--build-threads=48'],
                    extra_cmake_args=[
                        "-DCMAKE_C_FLAGS='-mcpu=neoverse-v2'",
                        "-DCMAKE_CXX_FLAGS='-mcpu=neoverse-v2'",
                        "-DLLVM_ENABLE_LLD=True",
                        "-DMLIR_INCLUDE_INTEGRATION_TESTS=True",
                        "-DMLIR_RUN_ARM_SVE_TESTS=True"])},

    # AArch64 Clang+LLVM+RT+LLD check-all + flang + test-suite 2-stage with SVE2
    # (not just SVE) Vector Length Agnostic codegen.
    {'name' : "clang-aarch64-sve2-vla-2stage",
    'tags'  : ["clang"],
    'workernames' : ["linaro-g4-01", "linaro-g4-02"],
    'builddir': "clang-aarch64-sve2-vla-2stage",
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                    clean=True,
                    checkout_flang=True,
                    useTwoStage=True,
                    testStage1=False,
                    runTestSuite=True,
                    env={
                        'NO_STOP_MESSAGE':'1', # For Fortran test-suite
                    },
                    testsuite_flags=[
                        '--cppflags', '-mcpu=neoverse-v2 -mllvm -scalable-vectorization=preferred -mllvm -treat-scalable-fixed-error-as-warning=false -O3',
                        '--cmake-define', 'CMAKE_Fortran_FLAGS=-mcpu=neoverse-v2 -mllvm -scalable-vectorization=preferred -mllvm -treat-scalable-fixed-error-as-warning=false -O3',
                        '--threads=48', '--build-threads=48'],
                    extra_cmake_args=[
                        "-DCMAKE_C_FLAGS='-mcpu=neoverse-v2 -mllvm -scalable-vectorization=preferred -mllvm -treat-scalable-fixed-error-as-warning=false'",
                        "-DCMAKE_CXX_FLAGS='-mcpu=neoverse-v2 -mllvm -scalable-vectorization=preferred -mllvm -treat-scalable-fixed-error-as-warning=false'",
                        "-DLLVM_ENABLE_LLD=True",
                        "-DMLIR_INCLUDE_INTEGRATION_TESTS=True",
                        "-DMLIR_RUN_ARM_SVE_TESTS=True"])},

    {'name' : "clang-arm64-windows-msvc-2stage",
    'tags'  : ["clang"],
    'workernames' : ["linaro-armv8-windows-msvc-02", "linaro-armv8-windows-msvc-03"],
    'builddir': "clang-arm64-windows-msvc-2stage",
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                    vs="manual",
                    clean=True,
                    useTwoStage=True,
                    checkout_flang=True,
                    testStage1=False,
                    extra_cmake_args=[
                        "-DCLANG_DEFAULT_LINKER=lld",
                        "-DCMAKE_TRY_COMPILE_CONFIGURATION=Release",
                        "-DLLVM_CCACHE_BUILD=ON",
                        "-DLLVM_ENABLE_RUNTIMES=openmp",
                        "-DCOMPILER_RT_BUILD_SANITIZERS=OFF"])},

    {'name' : 'clang-x64-windows-msvc',
    'tags'  : ["clang"],
    'workernames' : ['windows-gcebot2'],
    'builddir': 'clang-x64-windows-msvc',
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    script="clang-windows.py",
                    depends_on_projects=['llvm', 'clang', 'lld', 'debuginfo-tests'])},

    {'name' : "clang-m68k-linux",
    'tags'  : ["clang"],
    'workernames' : ["debian-akiko-m68k"],
    'builddir': "clang-m68k-linux",
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                    clean=False,
                    checkout_lld=False,
                    useTwoStage=False,
                    enable_runtimes=None,
                    stage1_config='Release',
                    extra_cmake_args=[
                        "-DLLVM_ENABLE_ASSERTIONS=ON",
                        "-DLLVM_EXPERIMENTAL_TARGETS_TO_BUILD=M68k"])},

    {'name' : "clang-m68k-linux-cross",
    'tags'  : ["clang"],
    'workernames' : ["suse-gary-m68k-cross"],
    'builddir': "clang-m68k-linux-cross",
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                    clean=False,
                    checkout_lld=False,
                    checkout_compiler_rt=False,
                    useTwoStage=False,
                    stage1_config='Release',
                    extra_cmake_args=[
                        "-DLLVM_ENABLE_ASSERTIONS=ON",
                        "-DLLVM_TARGETS_TO_BUILD=X86",
                        "-DLLVM_EXPERIMENTAL_TARGETS_TO_BUILD=M68k"])},

    {'name' : "clang-mips64el-linux",
    'tags'  : ["clang"],
    'workernames' : ["debian-tritium-mips64el"],
    'builddir': "clang-mips64el-linux",
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                    clean=False,
                    checkout_lld=False,
                    enable_runtimes=None,
                    useTwoStage=False,
                    stage1_config='Release',
                    extra_cmake_args=['-DLLVM_ENABLE_ASSERTIONS=ON',
                                      '-DLLVM_PARALLEL_LINK_JOBS=4',
                                      '-DCOMPILER_RT_DEFAULT_TARGET_ONLY=ON',
                                      '-DCMAKE_C_COMPILER_TARGET="mips64el-unknown-linux-gnu"',
                                      '-DLLVM_TARGETS_TO_BUILD=Mips'])},

    {'name' : "clang-ppc64le-linux-test-suite",
    'tags'  : ["clang", "ppc", "ppc64le"],
    'workernames' : ["ppc64le-clang-test-suite"],
    'builddir': "clang-ppc64le-test-suite",
    'factory' : TestSuiteBuilder.getTestSuiteBuildFactory(
                    depends_on_projects=["llvm", "clang", "clang-tools-extra",
                                         "compiler-rt"],
                    checks=['check-all', 'check-runtimes'],
                    extra_configure_args=[
                        "-DLLVM_ENABLE_ASSERTIONS=ON",
                        "-DCMAKE_BUILD_TYPE=Release",
                        "-DLLVM_LIT_ARGS=-v",
                        "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                        "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache"])},

    {'name' : "clang-ppc64le-linux-multistage",
    'tags'  : ["clang", "ppc", "ppc64le"],
    'workernames' : ["ppc64le-clang-multistage-test"],
    'builddir': "clang-ppc64le-multistage",
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                    clean=False,
                    checks=['check-all', 'check-runtimes'],
                    checkout_lld=False,
                    useTwoStage=True,
                    stage1_config='Release',
                    stage2_config='Release',
                    extra_cmake_args=[
                        '-DLLVM_ENABLE_ASSERTIONS=ON',
                        '-DBUILD_SHARED_LIBS=ON',
                        '-DCMAKE_C_COMPILER_LAUNCHER=ccache',
                        '-DCMAKE_CXX_COMPILER_LAUNCHER=ccache'])},

    {'name' : "clang-ppc64le-rhel",
    'tags'  : ["clang", "ppc", "ppc64le"],
    'workernames' : ["ppc64le-clang-rhel-test"],
    'builddir': "clang-ppc64le-rhel",
    'factory' : TestSuiteBuilder.getTestSuiteBuildFactory(
                    depends_on_projects=["llvm", "clang", "clang-tools-extra",
                                         "lld", "compiler-rt"],
                    checks=['check-runtimes', 'check-all'],
                    extra_configure_args=[
                        "-DLLVM_ENABLE_ASSERTIONS=On",
                        "-DCMAKE_C_COMPILER=clang",
                        "-DCMAKE_CXX_COMPILER=clang++",
                        "-DCLANG_DEFAULT_LINKER=lld",
                        "-DLLVM_TOOL_GOLD_BUILD=0",
                        "-DCMAKE_C_COMPILER_EXTERNAL_TOOLCHAIN:PATH=/gcc-toolchain/usr",
                        "-DCMAKE_CXX_COMPILER_EXTERNAL_TOOLCHAIN:PATH=/gcc-toolchain/usr",
                        "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                        "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
                        "-DBUILD_SHARED_LIBS=ON", "-DLLVM_ENABLE_WERROR=ON",
                        "-DCMAKE_BUILD_TYPE=Release",
                        "-DLLVM_LIT_ARGS=-vj 20"])},

    {'name' : "clang-ppc64-aix",
    'tags'  : ["clang", "aix", "ppc"],
    'workernames' : ["aix-ppc64"],
    'builddir': "clang-ppc64-aix",
    'factory' : TestSuiteBuilder.getTestSuiteBuildFactory(
                    depends_on_projects=["llvm", "clang", "compiler-rt"],
                    clean=False,
                    extra_configure_args=[
                        "-DLLVM_ENABLE_ASSERTIONS=On",
                        "-DCMAKE_C_COMPILER=clang",
                        "-DCMAKE_CXX_COMPILER=clang++",
                        "-DPython3_EXECUTABLE:FILEPATH=python3",
                        "-DLLVM_ENABLE_ZLIB=OFF", "-DLLVM_APPEND_VC_REV=OFF",
                        "-DLLVM_PARALLEL_LINK_JOBS=2",
                        "-DLLVM_ENABLE_WERROR=ON",
                        "-DSANITIZER_DISABLE_SYMBOLIZER_PATH_SEARCH:BOOL=ON"]),
    'env' : {'OBJECT_MODE': '64'}},

    {'name' : "clang-s390x-linux",
    'tags'  : ["clang"],
    'workernames' : ["systemz-1"],
    'builddir': "clang-s390x-linux",
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                    jobs=4,
                    clean=False,
                    checkout_lld=False,
                    useTwoStage=False,
                    stage1_config='Release',
                    extra_cmake_args=[
                        "-DLLVM_CCACHE_BUILD=ON",
                        "-DLLVM_ENABLE_ASSERTIONS=ON",
                        "-DLLVM_LIT_ARGS=-v -j4 --param run_long_tests=true"])},

    {'name' : "clang-s390x-linux-multistage",
    'tags'  : ["clang"],
    'workernames' : ["systemz-1"],
    'builddir': "clang-s390x-linux-multistage",
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                    jobs=4,
                    clean=True,
                    checkout_lld=False,
                    useTwoStage=True,
                    testStage1=False,
                    stage1_config='Release',
                    stage2_config='Release',
                    extra_cmake_args=[
                        "-DLLVM_CCACHE_BUILD=ON",
                        "-DLLVM_ENABLE_ASSERTIONS=ON"])},

    {'name' : "clang-s390x-linux-lnt",
    'tags'  : ["clang"],
    'workernames' : ["systemz-1"],
    'builddir': "clang-s390x-linux-lnt",
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                    jobs=4,
                    clean=False,
                    checkout_lld=False,
                    useTwoStage=False,
                    runTestSuite=True,
                    stage1_config='Release',
                    testsuite_flags=['--threads=4', '--build-threads=4'],
                    extra_cmake_args=[
                        "-DLLVM_CCACHE_BUILD=ON",
                        "-DLLVM_ENABLE_ASSERTIONS=ON"])},

    {'name' : 'clang-sparc64-linux',
    'tags'  : ['clang'],
    'workernames' : ['debian-stadler-sparc64'],
    'builddir': 'clang-sparc64-linux',
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                    clean=False,
                    timeout=1800,
                    runTestSuite=True,
                    checkout_clang_tools_extra=False,
                    checkout_compiler_rt=False,
                    checkout_lld=False,
                    testsuite_flags=['--threads=32', '--build-threads=32'],
                    extra_cmake_args=['-DLLVM_ENABLE_PROJECTS=clang',
                                      '-DLLVM_USE_LINKER=mold',
                                      '-DLLVM_TARGETS_TO_BUILD=Sparc'])},

    ## LoongArch64 Clang+LLVM build check-all + test-suite
    {'name' : 'clang-loongarch64-linux',
    'tags'  : ['clang'],
    'workernames' : ['loongson-loongarch64-clfs-clang-01'],
    'builddir': 'clang-loongarch64-linux',
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                    clean=False,
                    runTestSuite=True,
                    checkout_clang_tools_extra=False,
                    checkout_compiler_rt=False,
                    checkout_lld=False,
                    testsuite_flags=['--threads=32', '--build-threads=32'],
                    extra_cmake_args=['-DLLVM_TARGETS_TO_BUILD=LoongArch',
                                      '-DCMAKE_C_COMPILER=/usr/local/bin/clang',
                                      '-DCMAKE_CXX_COMPILER=/usr/local/bin/clang++',
                                      '-DLLVM_USE_LINKER=lld',
                                      '-DLLVM_ENABLE_PROJECTS=clang'])},

    {'name' : "clang-hexagon-elf",
    'tags'  : ["clang"],
    'workernames' : ["hexagon-build-02", "hexagon-build-03"],
    'builddir': "clang-hexagon-elf",
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                    jobs=16,
                    checkout_clang_tools_extra=False,
                    checkout_compiler_rt=False,
                    checkout_lld=False,
                    env={'LD_LIBRARY_PATH': '/local/clang+llvm-12.0.0-x86_64-linux-gnu-ubuntu-16.04/lib'},
                    extra_cmake_args=[
                        "-DCMAKE_BUILD_TYPE:STRING=Release",
                        "-DLLVM_TARGETS_TO_BUILD:STRING=Hexagon",
                        "-DTARGET_TRIPLE:STRING=hexagon-unknown-elf",
                        "-DLLVM_DEFAULT_TARGET_TRIPLE:STRING=hexagon-unknown-elf",
                        "-DLLVM_TARGET_ARCH:STRING=hexagon-unknown-elf",
                        "-DLLVM_BUILD_RUNTIME:BOOL=OFF",
                        "-DCMAKE_VERBOSE_MAKEFILE:BOOL=ON",
                        "-DLLVM_ENABLE_PIC:BOOL=ON",
                        "-DLLVM_ENABLE_ASSERTIONS:BOOL=ON",
                        "-DLLVM_INCLUDE_TOOLS:BOOL=ON",
                        "-DLLVM_LIT_ARGS:STRING=-v",
                        "-DLLVM_ENABLE_LIBCXX:BOOL=ON",
                        "-DWITH_POLLY:BOOL=OFF",
                        "-DLINK_POLLY_INTO_TOOLS:BOOL=OFF",
                        "-DPOLLY_BUILD_SHARED_LIB:BOOL=OFF",
                        "-DCMAKE_C_COMPILER:FILEPATH=/local/clang+llvm-12.0.0-x86_64-linux-gnu-ubuntu-16.04/bin/clang",
                        "-DCMAKE_CXX_COMPILER:FILEPATH=/local/clang+llvm-12.0.0-x86_64-linux-gnu-ubuntu-16.04/bin/clang++"])},

    ## X86_64 AVX512 Clang+LLVM check-all + test-suite
    {'name' : "clang-cmake-x86_64-avx512-linux",
    'tags'  : ["clang"],
    'workernames' : ["avx512-intel64"],
    'builddir': "clang-cmake-x86_64-avx512-linux",
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                    clean=False,
                    checkout_clang_tools_extra=False,
                    checkout_compiler_rt=False,
                    checkout_lld=False,
                    useTwoStage=False,
                    runTestSuite=True,
                    testsuite_flags=['--cflag', '-march=cascadelake', '--threads=32', '--build-threads=32'],
                    env={'PATH':'/usr/bin/ccache:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'},
                    extra_cmake_args=[
                        "-DLLVM_ENABLE_ASSERTIONS=ON",
                        "-DCMAKE_C_FLAGS='-march=cascadelake'",
                        "-DCMAKE_CXX_FLAGS='-march=cascadelake'",
                        "-DLLVM_ENABLE_RUNTIMES=compiler-rt",
                        "-DCOMPILER_RT_BUILD_SANITIZERS=OFF",
                        "-DLLVM_TARGETS_TO_BUILD='X86'"])},

    ## Windows X86_64 AVX512 Clang+LLVM check-all + test-suite
    {'name' : "clang-cmake-x86_64-avx512-win",
    'tags'  : ["clang"],
    'workernames' : ["avx512-intel64-win"],
    'builddir': "clang-cmake-x86_64-avx512-win",
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                    vs="autodetect",
                    vs_target_arch='x64',
                    stage1_config='Debug',
                    clean=True,
                    checkout_clang_tools_extra=True,
                    checkout_compiler_rt=False,
                    checkout_lld=False,
                    useTwoStage=False,
                    runTestSuite=False,
                    testsuite_flags=['--cflag', '-march=cascadelake', '--threads=32', '--build-threads=32'],
                    extra_cmake_args=[
                        "-DCMAKE_C_FLAGS='-march=cascadelake'",
                        "-DCMAKE_CXX_FLAGS='-march=cascadelake'",
                        "-DCMAKE_C_COMPILER=icx.EXE",
                        "-DMAKE_CXX_COMPILER=icx.EXE",
                        "-DLLVM_ENABLE_RUNTIMES=compiler-rt",
                        "-DCOMPILER_RT_BUILD_SANITIZERS=OFF",
                        "-DCOMPILER_RT_BUILD_ORC=OFF",
                        "-DLLVM_TARGETS_TO_BUILD=X86"])},

    {'name' : "clang-xcore-ubuntu-20-x64",
    'tags'  : ["clang"],
    'workernames' : ["xcore-ubuntu20-x64"],
    'builddir': "clang-xcore-ubuntu-20-x64",
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                    jobs=4,
                    checkout_clang_tools_extra=False,
                    checkout_compiler_rt=False,
                    checkout_lld=False,
                    testStage1=True,
                    useTwoStage=False,
                    stage1_config='Release',
                    extra_cmake_args=[
                        "-DLLVM_TARGETS_TO_BUILD:STRING=XCore",
                        "-DLLVM_DEFAULT_TARGET_TRIPLE:STRING=xcore-unknown-unknown-elf",
                        "-DLLVM_ENABLE_THREADS:BOOL=OFF"])},

    {'name' : "llvm-clang-x86_64-sie-win",
    'tags'  : ["llvm", "clang", "clang-tools-extra", "lld", "cross-project-tests"],
    'workernames' : ["sie-win-worker"],
    'builddir': "llvm-clang-x86_64-sie-win",
    'factory' : UnifiedTreeBuilder.getCmakeWithNinjaWithMSVCBuildFactory(
                    vs="autodetect",
                    target_arch='x64',
                    depends_on_projects=['llvm','clang','clang-tools-extra','lld','cross-project-tests'],
                    clean=True,
                    extra_configure_args=[
                        "-DCMAKE_BUILD_TYPE=Release",
                        "-DCLANG_ENABLE_ARCMT=OFF",
                        "-DCLANG_ENABLE_CLANGD=OFF",
                        "-DLLVM_CCACHE_BUILD=ON",
                        "-DLLVM_DEFAULT_TARGET_TRIPLE=x86_64-sie-ps5",
                        "-DLLVM_INCLUDE_EXAMPLES=OFF",
                        "-DLLVM_TARGETS_TO_BUILD=X86",
                        "-DLLVM_VERSION_SUFFIX=",
                        "-DLLVM_BUILD_RUNTIME=OFF",
                        "-DLLVM_ENABLE_ASSERTIONS=ON",
                        "-DLLVM_LIT_ARGS=--verbose --timeout=900"])},

    {'name': "cross-project-tests-sie-ubuntu",
    'tags'  : ["clang", "llvm", "lldb", "cross-project-tests"],
    'workernames': ["doug-worker-1a"],
    'builddir': "cross-project-tests-sie-ubuntu",
    'factory': UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    depends_on_projects=['llvm','clang','lldb','cross-project-tests'],
                    checks = ['check-cross-project'],
                    extra_configure_args=[
                        "-DCMAKE_C_COMPILER=gcc",
                        "-DCMAKE_CXX_COMPILER=g++",
                        "-DCMAKE_BUILD_TYPE=Release",
                        "-DCLANG_ENABLE_ARCMT=OFF",
                        "-DLLDB_ENABLE_PYTHON=TRUE",
                        "-DLLVM_INCLUDE_EXAMPLES=OFF",
                        "-DLLVM_ENABLE_ASSERTIONS=ON",
                        "-DLLVM_LIT_ARGS=--verbose --timeout=900",
                        "-DLLVM_PARALLEL_LINK_JOBS=8",
                        "-DLLVM_TARGETS_TO_BUILD=X86",
                        "-DLLVM_USE_LINKER=gold"])},

    {'name': "cross-project-tests-sie-ubuntu-dwarf5",
    'tags'  : ["clang", "llvm", "lldb", "cross-project-tests"],
    'workernames': ["doug-worker-1b"],
    'builddir': "cross-project-tests-sie-ubuntu-dwarf5",
    'factory': UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    depends_on_projects=['llvm','clang','lldb','cross-project-tests'],
                    checks = ['check-cross-project'],
                    extra_configure_args=[
                        "-DCMAKE_C_COMPILER=gcc",
                        "-DCMAKE_CXX_COMPILER=g++",
                        "-DCMAKE_BUILD_TYPE=Release",
                        "-DCLANG_ENABLE_ARCMT=OFF",
                        "-DLLDB_ENABLE_PYTHON=TRUE",
                        "-DLLVM_INCLUDE_EXAMPLES=OFF",
                        "-DLLVM_ENABLE_ASSERTIONS=ON",
                        "-DLLVM_LIT_ARGS=--verbose --timeout=900",
                        "-DLLVM_PARALLEL_LINK_JOBS=8",
                        "-DLLVM_TARGETS_TO_BUILD=X86",
                        "-DLLVM_USE_LINKER=gold"])},

    {'name': "llvm-clang-x86_64-gcc-ubuntu",
    'tags'  : ["llvm", "clang", "clang-tools-extra", "compiler-rt", "lld", "cross-project-tests"],
    'workernames': ["sie-linux-worker3"],
    'builddir': "llvm-clang-x86_64-gcc-ubuntu",
    'factory': UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    depends_on_projects=['llvm','clang','clang-tools-extra','compiler-rt','lld','cross-project-tests'],
                    extra_configure_args=[
                        "-DCMAKE_C_COMPILER=gcc",
                        "-DCMAKE_CXX_COMPILER=g++",
                        "-DCMAKE_BUILD_TYPE=Release",
                        "-DCLANG_ENABLE_CLANGD=OFF",
                        "-DLLVM_BUILD_RUNTIME=ON",
                        "-DLLVM_BUILD_TESTS=ON",
                        "-DLLVM_ENABLE_ASSERTIONS=ON",
                        "-DLLVM_INCLUDE_EXAMPLES=OFF",
                        "-DLLVM_LIT_ARGS=--verbose --timeout=900",
                        "-DLLVM_USE_LINKER=gold"])},

    {'name': "clang-x86_64-linux-abi-test",
     'tags': ["llvm", "clang", "clang-tools-extra", "compiler-rt", "lld", "cross-project-tests"],
     'workernames': ["sie-linux-worker2"],
     'builddir': "abi-test",
     'factory': ABITestsuitBuilder.getABITestsuitBuildFactory(
                    depends_on_projects=['llvm','clang','clang-tools-extra','compiler-rt','lld','cross-project-tests'],
                    extra_configure_args=[
                        "-DCMAKE_C_COMPILER=gcc",
                        "-DCMAKE_CXX_COMPILER=g++",
                        "-DCMAKE_BUILD_TYPE=Release",
                        "-DCLANG_ENABLE_CLANGD=OFF",
                        "-DLLVM_BUILD_RUNTIME=ON",
                        "-DLLVM_BUILD_TESTS=ON",
                        "-DLLVM_ENABLE_ASSERTIONS=ON",
                        "-DLLVM_INCLUDE_EXAMPLES=OFF",
                        "-DLLVM_LIT_ARGS=--verbose --timeout=900",
                        "-DLLVM_USE_LINKER=gold",
                        "-DLLVM_ENABLE_WERROR=OFF"])},

    {'name': "llvm-clang-key-instructions",
    'tags'  : ["llvm", "clang", "compiler-rt", "lld", "cross-project-tests"],
    'workernames': ["sie-linux-worker5"],
    'builddir': "llvm-ki",
    'factory': UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    depends_on_projects=['llvm','clang','compiler-rt','lld','cross-project-tests'],
                    extra_configure_args=[
                        "-DCMAKE_C_COMPILER=gcc",
                        "-DCMAKE_CXX_COMPILER=g++",
                        "-DCMAKE_BUILD_TYPE=Release",
                        "-DCLANG_ENABLE_CLANGD=OFF",
                        "-DLLVM_BUILD_RUNTIME=ON",
                        "-DLLVM_BUILD_TESTS=ON",
                        "-DLLVM_ENABLE_ASSERTIONS=ON",
                        "-DLLVM_EXPERIMENTAL_KEY_INSTRUCTIONS=ON",
                        "-DLLVM_INCLUDE_EXAMPLES=OFF",
                        "-DLLVM_LIT_ARGS=--verbose --timeout=900",
                        "-DLLVM_USE_LINKER=gold"])},

    {'name': "llvm-clang-x86_64-darwin",
    'tags'  : ["llvm", "clang", "clang-tools-extra", "lld", "cross-project-tests"],
    'workernames': ["doug-worker-3"],
    'builddir': "x86_64-darwin",
    'factory': UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    clean=True,
                    depends_on_projects=['llvm','clang','clang-tools-extra','lld','cross-project-tests'],
                    extra_configure_args=[
                        "-DCMAKE_C_COMPILER=clang",
                        "-DCMAKE_CXX_COMPILER=clang++",
                        "-DCMAKE_BUILD_TYPE=Release",
                        "-DLLVM_BUILD_TESTS=ON",
                        "-DLLVM_CCACHE_BUILD=ON",
                        "-DLLVM_ENABLE_ASSERTIONS=ON",
                        "-DLLVM_INCLUDE_EXAMPLES=OFF",
                        "-DLLVM_LIT_ARGS=--verbose --timeout=900",
                        "-DLLVM_TARGETS_TO_BUILD=X86"])},

    {'name': "llvm-clang-aarch64-darwin",
    'tags'  : ["llvm", "clang", "clang-tools-extra", "lld", "cross-project-tests"],
    'workernames': ["doug-worker-4", "doug-worker-5"],
    'builddir': "aarch64-darwin",
    'factory': UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    clean=True,
                    depends_on_projects=['llvm','clang','clang-tools-extra','lld','cross-project-tests'],
                    extra_configure_args=[
                        "-DCMAKE_C_COMPILER=clang",
                        "-DCMAKE_CXX_COMPILER=clang++",
                        "-DCMAKE_BUILD_TYPE=Release",
                        "-DLLVM_BUILD_TESTS=ON",
                        "-DLLVM_CCACHE_BUILD=ON",
                        "-DLLVM_ENABLE_ASSERTIONS=ON",
                        "-DLLVM_INCLUDE_EXAMPLES=OFF",
                        "-DLLVM_LIT_ARGS=--verbose --timeout=900",
                        "-DLLVM_TARGETS_TO_BUILD=AArch64"])},

    {'name': "llvm-clang-x86_64-gcc-ubuntu-no-asserts",
    'tags'  : ["llvm", "clang", "clang-tools-extra", "compiler-rt", "lld", "cross-project-tests"],
    'workernames': ["doug-worker-6"],
    'builddir': "gcc-no-asserts",
    'factory': UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    depends_on_projects=['llvm','clang','clang-tools-extra','compiler-rt','lld','cross-project-tests'],
                    extra_configure_args=[
                        "-DCMAKE_C_COMPILER=gcc",
                        "-DCMAKE_CXX_COMPILER=g++",
                        "-DCMAKE_BUILD_TYPE=Release",
                        "-DCLANG_ENABLE_CLANGD=OFF",
                        "-DLLVM_BUILD_RUNTIME=ON",
                        "-DLLVM_BUILD_TESTS=ON",
                        "-DLLVM_ENABLE_ASSERTIONS=OFF",
                        "-DLLVM_INCLUDE_EXAMPLES=OFF",
                        "-DLLVM_LIT_ARGS=--verbose --timeout=900",
                        "-DLLVM_USE_LINKER=gold"])},

# Polly builders.

    {'name' : "polly-arm-linux",
    'tags'  : ["polly"],
    'workernames' : ["hexagon-build-02", "hexagon-build-03"],
    'builddir': "polly-arm-linux",
    'factory' : PollyBuilder.getPollyBuildFactory(
                    clean=True,
                    install=True,
                    make='ninja',
                    jobs=16,
                    env={'LD_LIBRARY_PATH': '/local/clang+llvm-12.0.0-x86_64-linux-gnu-ubuntu-16.04/lib'},
                    extraCmakeArgs=[
                        "-G", "Ninja",
                        "-DLLVM_TARGETS_TO_BUILD='ARM;AArch64'",
                        "-DLLVM_DEFAULT_TARGET_TRIPLE=arm-linux-gnueabi",
                        "-DLLVM_TARGET_ARCH=arm-linux-gnueabi",
                        "-DLLVM_ENABLE_ASSERTIONS=True",
                        "-DLLVM_ENABLE_LIBCXX:BOOL=ON",
                        "-DPOLLY_ENABLE_GPGPU_CODEGEN=OFF",
                        "-DCMAKE_C_COMPILER:FILEPATH=/local/clang+llvm-12.0.0-x86_64-linux-gnu-ubuntu-16.04/bin/clang",
                        "-DCMAKE_CXX_COMPILER:FILEPATH=/local/clang+llvm-12.0.0-x86_64-linux-gnu-ubuntu-16.04/bin/clang++"])},

    {'name' : "polly-x86_64-linux",
    'tags'  : ["polly"],
    'workernames' : ["polly-x86_64-gce1"],
    'builddir': "polly-x86_64-linux",
    'factory' : PollyBuilder.getPollyBuildFactory(
                    clean=False,
                    install=False,
                    make='ninja',
                    extraCmakeArgs=[
                        "-G", "Ninja",
                        "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                        "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
                        "-DLLVM_ENABLE_ASSERTIONS=True",
                        "-DLLVM_TARGETS_TO_BUILD='X86;NVPTX'",
                        "-DCLANG_ENABLE_ARCMT=OFF",
                        "-DCLANG_ENABLE_STATIC_ANALYZER=OFF",
                        "-DCLANG_ENABLE_OBJC_REWRITER=OFF",
                        "-DLLVM_ENABLE_LLD=ON",
                        "-DPOLLY_ENABLE_GPGPU_CODEGEN=ON"
                        ])},

    {'name' : "polly-x86_64-linux-plugin",
    'tags'  : ["polly"],
    'workernames' : ["polly-x86_64-gce1"],
    'builddir': "polly-x86_64-linux-plugin",
    'factory' : PollyBuilder.getPollyBuildFactory(
                    clean=False,
                    install=False,
                    make='ninja',
                    extraCmakeArgs=[
                        "-G", "Ninja",
                        "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                        "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
                        "-DLLVM_ENABLE_ASSERTIONS=True",
                        "-DLLVM_TARGETS_TO_BUILD='X86;NVPTX'",
                        "-DCLANG_ENABLE_ARCMT=OFF",
                        "-DCLANG_ENABLE_STATIC_ANALYZER=OFF",
                        "-DCLANG_ENABLE_OBJC_REWRITER=OFF",
                        "-DLLVM_ENABLE_LLD=ON",
                        "-DLLVM_POLLY_LINK_INTO_TOOLS=OFF",
                        "-DPOLLY_ENABLE_GPGPU_CODEGEN=OFF"  # Not all required symbols available in opt executable
                        ])},

    {'name' : "polly-x86_64-linux-noassert",
    'tags'  : ["polly"],
    'workernames' : ["polly-x86_64-gce1"],
    'builddir': "polly-x86_64-linux-noassert",
    'factory' : PollyBuilder.getPollyBuildFactory(
                    clean=False,
                    install=False,
                    make='ninja',
                    extraCmakeArgs=[
                        "-G", "Ninja",
                        "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                        "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
                        "-DLLVM_ENABLE_ASSERTIONS=False",
                        "-DLLVM_TARGETS_TO_BUILD='X86;NVPTX'",
                        "-DCLANG_ENABLE_ARCMT=OFF",
                        "-DCLANG_ENABLE_STATIC_ANALYZER=OFF",
                        "-DCLANG_ENABLE_OBJC_REWRITER=OFF",
                        "-DLLVM_ENABLE_LLD=ON",
                        "-DPOLLY_ENABLE_GPGPU_CODEGEN=ON"
                        ])},

    {'name' : "polly-x86_64-linux-shared",
    'tags'  : ["polly"],
    'workernames' : ["polly-x86_64-gce2"],
    'builddir': "polly-x86_64-linux-shared",
    'factory' : PollyBuilder.getPollyBuildFactory(
                    clean=False,
                    install=False,
                    make='ninja',
                    extraCmakeArgs=[
                        "-G", "Ninja",
                        "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                        "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
                        "-DLLVM_ENABLE_ASSERTIONS=True",
                        "-DLLVM_TARGETS_TO_BUILD='X86;NVPTX'",
                        "-DCLANG_ENABLE_ARCMT=OFF",
                        "-DCLANG_ENABLE_STATIC_ANALYZER=OFF",
                        "-DCLANG_ENABLE_OBJC_REWRITER=OFF",
                        "-DLLVM_ENABLE_LLD=ON",
                        "-DBUILD_SHARED_LIBS=ON",
                        "-DPOLLY_ENABLE_GPGPU_CODEGEN=ON"
                        ])},

    {'name' : "polly-x86_64-linux-shared-plugin",
    'tags'  : ["polly"],
    'workernames' : ["polly-x86_64-gce2"],
    'builddir': "polly-x86_64-linux-shared-plugin",
    'factory' : PollyBuilder.getPollyBuildFactory(
                    clean=False,
                    install=False,
                    make='ninja',
                    extraCmakeArgs=[
                        "-G", "Ninja",
                        "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                        "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
                        "-DLLVM_ENABLE_ASSERTIONS=True",
                        "-DLLVM_TARGETS_TO_BUILD='X86;NVPTX'",
                        "-DCLANG_ENABLE_ARCMT=OFF",
                        "-DCLANG_ENABLE_STATIC_ANALYZER=OFF",
                        "-DCLANG_ENABLE_OBJC_REWRITER=OFF",
                        "-DLLVM_ENABLE_LLD=ON",
                        "-DBUILD_SHARED_LIBS=ON",
                        "-DLLVM_POLLY_LINK_INTO_TOOLS=OFF",
                        "-DPOLLY_ENABLE_GPGPU_CODEGEN=ON"
                        ])},

    {'name' : "polly-x86_64-linux-shlib",
    'tags'  : ["polly"],
    'workernames' : ["polly-x86_64-gce2"],
    'builddir': "polly-x86_64-linux-shlib",
    'factory' : PollyBuilder.getPollyBuildFactory(
                    clean=False,
                    install=False,
                    make='ninja',
                    extraCmakeArgs=[
                        "-G", "Ninja",
                        "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                        "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
                        "-DLLVM_ENABLE_ASSERTIONS=True",
                        "-DLLVM_TARGETS_TO_BUILD='X86;NVPTX'",
                        "-DCLANG_ENABLE_ARCMT=OFF",
                        "-DCLANG_ENABLE_STATIC_ANALYZER=OFF",
                        "-DCLANG_ENABLE_OBJC_REWRITER=OFF",
                        "-DLLVM_ENABLE_LLD=ON",
                        "-DLLVM_BUILD_LLVM_DYLIB=ON",
                        "-DLLVM_LINK_LLVM_DYLIB=ON",
                        "-DPOLLY_ENABLE_GPGPU_CODEGEN=ON"
                        ])},

    {'name' : "polly-x86_64-linux-shlib-plugin",
    'tags'  : ["polly"],
    'workernames' : ["polly-x86_64-gce2"],
    'builddir': "polly-x86_64-linux-shlib-plugin",
    'factory' : PollyBuilder.getPollyBuildFactory(
                    clean=False,
                    install=False,
                    make='ninja',
                    extraCmakeArgs=[
                        "-G", "Ninja",
                        "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                        "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
                        "-DLLVM_ENABLE_ASSERTIONS=True",
                        "-DLLVM_TARGETS_TO_BUILD='X86;NVPTX'",
                        "-DCLANG_ENABLE_ARCMT=OFF",
                        "-DCLANG_ENABLE_STATIC_ANALYZER=OFF",
                        "-DCLANG_ENABLE_OBJC_REWRITER=OFF",
                        "-DLLVM_ENABLE_LLD=ON",
                        "-DLLVM_BUILD_LLVM_DYLIB=ON",
                        "-DLLVM_LINK_LLVM_DYLIB=ON",
                        "-DLLVM_POLLY_LINK_INTO_TOOLS=OFF",
                        "-DPOLLY_ENABLE_GPGPU_CODEGEN=ON"
                        ])},

    {'name' : "polly-x86_64-linux-test-suite",
    'tags'  : ["polly"],
    'workernames' : ["polly-x86_64-fdcserver", "minipc-1050ti-linux"],
    'builddir': "polly-x86_64-linux-test-suite",
    'factory' : PollyBuilder.getPollyBuildFactory(
                    clean=False,
                    install=False,
                    make='ninja',
                    extraCmakeArgs=[
                        "-G", "Ninja",
                        "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                        "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
                        "-DLLVM_ENABLE_ASSERTIONS=True",
                        "-DLLVM_TARGETS_TO_BUILD='X86;NVPTX'",
                        "-DCLANG_ENABLE_ARCMT=OFF",
                        "-DCLANG_ENABLE_STATIC_ANALYZER=OFF",
                        "-DCLANG_ENABLE_OBJC_REWRITER=OFF"
                        ],
                    testsuite=True,
                    extraTestsuiteCmakeArgs=[
                        "-G", "Ninja",
                        "-DTEST_SUITE_COLLECT_COMPILE_TIME=OFF",
                        "-DTEST_SUITE_COLLECT_STATS=OFF",
                        "-DTEST_SUITE_COLLECT_CODE_SIZE=OFF",
                        util.Interpolate("-DTEST_SUITE_EXTERNALS_DIR=%(prop:builddir)s/../../test-suite-externals"),
                      ]
                    )},

# AOSP builders.

    {'name' : "aosp-O3-polly-before-vectorizer-unprofitable",
    'tags'  : ["polly", "aosp"],
    'workernames' : ["hexagon-build-03"],
    'builddir': "aosp",
    'factory' : AOSPBuilder.getAOSPBuildFactory(
                    device="arm64",
                    extra_cmake_args=[
                        "-G", "Ninja",
                        "-DLLVM_TARGETS_TO_BUILD='ARM;AArch64'",
                        "-DLLVM_DEFAULT_TARGET_TRIPLE=arm-linux-androideabi",
                        "-DLLVM_TARGET_ARCH=arm-linux-androideabi",
                        "-DLLVM_ENABLE_ASSERTIONS=True",
                        "-DLLVM_ENABLE_LIBCXX:BOOL=ON",
                        "-DPOLLY_ENABLE_GPGPU_CODEGEN=OFF",
                        "-DCMAKE_C_COMPILER:FILEPATH=/local/clang+llvm-12.0.0-x86_64-linux-gnu-ubuntu-16.04/bin/clang",
                        "-DCMAKE_CXX_COMPILER:FILEPATH=/local/clang+llvm-12.0.0-x86_64-linux-gnu-ubuntu-16.04/bin/clang++"],
                    timeout=240,
                    target_clang=None,
                    target_flags="-Wno-error -O3 -mllvm -polly -mllvm -polly-position=before-vectorizer -mllvm -polly-process-unprofitable -fcommon",
                    jobs=32,
                    extra_make_args=None,
                    env={'LD_LIBRARY_PATH': '/local/clang+llvm-12.0.0-x86_64-linux-gnu-ubuntu-16.04/lib'},
                    clean=False,
                    sync=False,
                    patch=None)},

# Reverse iteration builders.

    {'name' : "reverse-iteration",
    'tags'  : ["rev_iter"],
    'workernames' : ["hexagon-build-02", "hexagon-build-03"],
    'builddir': "reverse-iteration",
    'factory' : PollyBuilder.getPollyBuildFactory(
                    depends_on_projects=["llvm", "clang", "polly", "lld"],
                    clean=True,
                    make='ninja',
                    jobs=16,
                    checkAll=True,
                    env={'LD_LIBRARY_PATH': '/local/clang+llvm-12.0.0-x86_64-linux-gnu-ubuntu-16.04/lib'},
                    extraCmakeArgs=[
                        "-G", "Ninja",
                        "-DLLVM_REVERSE_ITERATION:BOOL=ON",
                        "-DLLVM_ENABLE_ASSERTIONS=True",
                        "-DLLVM_ENABLE_LIBCXX:BOOL=ON",
                        "-DPOLLY_ENABLE_GPGPU_CODEGEN=ON",
                        "-DCMAKE_C_COMPILER:FILEPATH=/local/clang+llvm-12.0.0-x86_64-linux-gnu-ubuntu-16.04/bin/clang",
                        "-DCMAKE_CXX_COMPILER:FILEPATH=/local/clang+llvm-12.0.0-x86_64-linux-gnu-ubuntu-16.04/bin/clang++"])},

# LLDB builders.

    {'name' : "lldb-x86_64-debian",
    'tags'  : ["lldb"],
    'workernames' : ["lldb-x86_64-debian"],
    'builddir': "lldb-x86_64-debian",
    'factory' : LLDBBuilder.getLLDBCMakeBuildFactory(
                    test=True,
                    extra_cmake_args=[
                        '-DLLVM_ENABLE_ASSERTIONS=True',
                        '-DLLVM_USE_LINKER=gold',
                        '-DLLDB_ENABLE_PYTHON=True',
                        '-DLLDB_TEST_USER_ARGS=-t',
                        '-DPYTHON_EXECUTABLE=/usr/bin/python3',
                        '-DCMAKE_C_COMPILER=clang',
                        '-DCMAKE_CXX_COMPILER=clang++'])},

    {'name' : "lldb-aarch64-ubuntu",
    'tags'  : ["lldb"],
    'workernames' : ["linaro-lldb-aarch64-ubuntu"],
    'builddir': "lldb-aarch64-ubuntu",
    'factory' : LLDBBuilder.getLLDBCMakeBuildFactory(
                    test=True,
                    clean=True,
                    extra_cmake_args=[
                        '-DLLVM_ENABLE_ASSERTIONS=True',
                        '-DLLVM_USE_LINKER=lld',
                        '-DLLDB_ENFORCE_STRICT_TEST_REQUIREMENTS=ON'])},

    {'name' : "lldb-arm-ubuntu",
    'tags'  : ["lldb"],
    'workernames' : ["linaro-lldb-arm-ubuntu"],
    'builddir': "lldb-arm-ubuntu",
    'factory' : LLDBBuilder.getLLDBCMakeBuildFactory(
                    test=True,
                    clean=True,
                    extra_cmake_args=[
                        '-DLLVM_ENABLE_ASSERTIONS=True',
                        '-DLLVM_LIT_ARGS=-vj 4',
                        '-DLLVM_USE_LINKER=lld',
                        '-DCLANG_DEFAULT_LINKER=lld',
                        '-DLLDB_ENFORCE_STRICT_TEST_REQUIREMENTS=ON'])},

    {'name' : "lldb-aarch64-windows",
    'tags'  : ["lldb"],
    'workernames' : ["linaro-armv8-windows-msvc-05"],
    'builddir': "lldb-aarch64-windows",
    'factory' : LLDBBuilder.getLLDBCMakeBuildFactory(
                    clean=True,
                    test=True,
                    extra_cmake_args=[
                        "-DLLVM_CCACHE_BUILD=ON",
                        # Hardware breakpoints and watchpoints are not yet supported,
                        # https://github.com/llvm/llvm-project/issues/80665.
                        '-DLLDB_TEST_USER_ARGS=--skip-category=watchpoint',
                        '-DLLDB_ENFORCE_STRICT_TEST_REQUIREMENTS=ON'])},

    {'name': "lldb-x86_64-win",
    'tags'  : ["lldb"],
    'workernames': ["as-builder-10"],
    'builddir': "lldb-x86-64",
    'factory': UnifiedTreeBuilder.getCmakeExBuildFactory(
                    depends_on_projects = ["llvm", "clang", "lld", "lldb"],
                    enable_runtimes = None,
                    checks = [
                        "check-lldb-unit",
                        "check-lldb-api",
                        "check-lldb-shell",
                    ],
                    vs = "autodetect",
                    clean = True,
                    cmake_definitions = {
                        "CMAKE_BUILD_TYPE"              : "Release",
                        "CMAKE_C_COMPILER_LAUNCHER"     : "ccache",
                        "CMAKE_CXX_COMPILER_LAUNCHER"   : "ccache",
                        "CMAKE_CXX_FLAGS"               : "-D__OPTIMIZE__",
                        "CMAKE_MSVC_RUNTIME_LIBRARY"    : "MultiThreadedDLL",

                        "LLVM_ENABLE_ASSERTIONS"        : "ON",    
                        "LLVM_INCLUDE_BENCHMARKS"       : "OFF",
                        "LLVM_PARALLEL_LINK_JOBS"       : 8,
                        "LLVM_LIT_ARGS"                 : "-v -vv --threads=32 --time-tests",
                        
                        "LLDB_ENFORCE_STRICT_TEST_REQUIREMENTS" : "ON",
                        "LLDB_ENABLE_SWIG"              : "ON ",
                        "LLDB_ENABLE_LIBEDIT"           : "OFF",
                        "LLDB_ENABLE_CURSES"            : "OFF",
                        "LLDB_ENABLE_LZMA"              : "OFF",
                        "LLDB_ENABLE_LIBXML2"           : "OFF",
                        "LLDB_CAN_USE_LLDB_SERVER"      : "ON",
                        "LLDB_TEST_USER_ARGS"           : "--skip-category=lldb-dap",
                    },
                    env = {
                        'LLDB_USE_LLDB_SERVER' : "1",
                        'CCACHE_DIR'    : util.Interpolate("%(prop:builddir)s/ccache-db"),
                        # TMP/TEMP within the build dir (to utilize a ramdisk).
                        'TMP'           : util.Interpolate("%(prop:builddir)s/build"),
                        'TEMP'          : util.Interpolate("%(prop:builddir)s/build"),
                    },
                )
        },

# LLD builders.

    {'name' : "ppc64le-lld-multistage-test",
    'tags'  : ["lld", "ppc", "ppc64le"],
    'workernames' : ["ppc64le-lld-multistage-test"],
    'builddir': "ppc64le-lld-multistage-test",
    'factory' : UnifiedTreeBuilder.getCmakeWithNinjaMultistageBuildFactory(
                    extra_configure_args=[
                        '-DLLVM_ENABLE_ASSERTIONS=ON',
                        '-DLLVM_LIT_ARGS=-svj 256',
                        '-DCMAKE_C_COMPILER_LAUNCHER=ccache',
                        '-DCMAKE_CXX_COMPILER_LAUNCHER=ccache'],
                    depends_on_projects=['llvm', 'clang', 'lld'])},

    {'name' : "lld-x86_64-ubuntu-fast",
    'tags'  : ["lld"],
    'collapseRequests': False,
    'workernames' : ["as-builder-4"],
    'builddir' : "lld-x86_64",
    'factory': UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    depends_on_projects=['llvm', 'lld'],
                    clean=True,
                    extra_configure_args=[
                        "-DLLVM_CCACHE_BUILD=ON",
                        '-DLLVM_ENABLE_WERROR=OFF'],
                    env={
                        'CCACHE_DIR' : util.Interpolate("%(prop:builddir)s/ccache-db"),
                        # TMP/TEMP within the build dir (to utilize a ramdisk).
                        'TMP'        : util.Interpolate("%(prop:builddir)s/build"),
                        'TEMP'       : util.Interpolate("%(prop:builddir)s/build"),
                    })},

# LTO and ThinLTO builders.

    {'name' : "clang-with-thin-lto-ubuntu",
    'tags'  : ["clang","lld","LTO"],
    'workernames' : ["as-worker-92"],
    'builddir': "clang-with-thin-lto-ubuntu",
    'factory' : ClangLTOBuilder.getClangWithLTOBuildFactory(
                    jobs=72,
                    lto='thin',
                    )},

    {'name' : "clang-with-thin-lto-wpd-ubuntu",
    'tags'  : ["clang","lld","LTO"],
    'workernames' : ["thinlto-x86-64-bot1", "thinlto-x86-64-bot2"],
    'builddir': "clang-with-thin-lto-wpd-ubuntu",
    'factory' : ClangLTOBuilder.getClangWithLTOBuildFactory(
                    jobs=72,
                    lto='thin',
                    extra_configure_args=[
                        '-DLLVM_CCACHE_BUILD=ON',
                    ],
                    extra_configure_args_lto_stage=[
                        '-DCMAKE_CXX_FLAGS=-O3 -Xclang -fwhole-program-vtables -fno-split-lto-unit',
                        '-DCMAKE_C_FLAGS=-O3 -Xclang -fwhole-program-vtables -fno-split-lto-unit',
                        '-DCMAKE_EXE_LINKER_FLAGS=-Wl,--lto-whole-program-visibility -fuse-ld=lld'])},

    {'name' : "clang-with-lto-ubuntu",
    'tags'  : ["clang","lld","LTO"],
    'workernames' : ["as-worker-91"],
    'builddir': "clang-with-lto-ubuntu",
    'factory' : ClangLTOBuilder.getClangWithLTOBuildFactory(
                    jobs=72,
                    extra_configure_args_lto_stage=[
                        '-DLLVM_PARALLEL_LINK_JOBS=14',
                    ])},
]

# Common builders options for MLIR.
mlir_default_cmake_options = [
  '-DLLVM_CCACHE_BUILD=ON',
  '-DLLVM_ENABLE_PROJECTS=mlir',
  '-DLLVM_TARGETS_TO_BUILD=host;NVPTX;AMDGPU',
  '-DLLVM_BUILD_EXAMPLES=ON',
  '-DMLIR_INCLUDE_INTEGRATION_TESTS=ON',
  '-DMLIR_ENABLE_BINDINGS_PYTHON=ON',
]

all += [

    {'name' : "mlir-nvidia",
    'tags'  : ["mlir"],
    'workernames' : ["mlir-nvidia"],
    'builddir': "mlir-nvidia",
    'factory' : UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    llvm_srcdir="llvm.src",
                    obj_dir="llvm.obj",
                    clean=True,
                    install_pip_requirements=True,
                    targets = ['check-mlir-build-only'],
                    checks = ['check-mlir'],
                    depends_on_projects=['llvm','mlir'],
                    extra_configure_args=mlir_default_cmake_options + [
                        '-DLLVM_TARGETS_TO_BUILD=host;NVPTX',
                        '-DMLIR_ENABLE_CUDA_RUNNER=1',
                        '-DCMAKE_CUDA_COMPILER=/usr/local/cuda/bin/nvcc',
                        '-DMLIR_ENABLE_VULKAN_RUNNER=1',
                        '-DBUILD_SHARED_LIBS=ON',
                        '-DMLIR_RUN_CUDA_TENSOR_CORE_TESTS=ON',
                        '-DLLVM_ENABLE_LLD=ON',
                    ],
                    env={
                        'CC':'clang',
                        'CXX': 'clang++',
                    })},

    {'name' : "mlir-nvidia-gcc7",
    'tags'  : ["mlir"],
    'workernames' : ["mlir-nvidia"],
    'builddir': "mlir-nvidia-gcc7",
    'factory' : UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    llvm_srcdir="llvm.src",
                    obj_dir="llvm.obj",
                    clean=True,
                    install_pip_requirements=True,
                    targets = ['check-mlir-build-only'],
                    checks = ['check-mlir'],
                    depends_on_projects=['llvm','mlir'],
                    extra_configure_args=mlir_default_cmake_options + [
                        '-DLLVM_TARGETS_TO_BUILD=host;NVPTX',
                        '-DMLIR_ENABLE_CUDA_RUNNER=1',
                        '-DCMAKE_CUDA_COMPILER=/usr/local/cuda/bin/nvcc',
                        '-DMLIR_ENABLE_VULKAN_RUNNER=1',
                        '-DMLIR_RUN_CUDA_TENSOR_CORE_TESTS=ON',
                        '-DLLVM_ENABLE_LLD=ON',
                    ],
                    env={
                        'CC':'gcc-7',
                        'CXX': 'g++-7',
                    })},

    {'name' : 'ppc64le-mlir-rhel-clang',
    'tags'  : ["mlir", "ppc", "ppc64le"],
    'collapseRequests' : False,
    'workernames' : ['ppc64le-mlir-rhel-test'],
    'builddir': 'ppc64le-mlir-rhel-clang-build',
    'factory' : UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    clean=True,
                    depends_on_projects=['llvm', 'mlir'],
                    targets = ['check-mlir-build-only'],
                    checks = ['check-mlir'],
                    extra_configure_args=[
                        '-DLLVM_TARGETS_TO_BUILD=PowerPC',
                        '-DLLVM_INSTALL_UTILS=ON',
                        '-DCMAKE_CXX_STANDARD=17',
                        '-DLLVM_ENABLE_PROJECTS=mlir',
                        '-DLLVM_LIT_ARGS=-vj 256',
                        '-DCMAKE_C_COMPILER_LAUNCHER=ccache',
                        '-DCMAKE_CXX_COMPILER_LAUNCHER=ccache',
                    ],
                    env={
                            'CC': 'clang',
                            'CXX': 'clang++',
                            'LD': 'lld',
                            'LD_LIBRARY_PATH': '/usr/lib64',
                    })},

    {'name' : 'mlir-s390x-linux',
    'tags'  : ["mlir", "s390x"],
    'workernames' : ["systemz-1"],
    'builddir': 'mlir-s390x-linux',
    'factory' : UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    clean=True,
                    depends_on_projects=['llvm', 'mlir'],
                    checks=['check-mlir'],
                    extra_configure_args=[
                        "-DLLVM_CCACHE_BUILD=ON",
                        '-DLLVM_TARGETS_TO_BUILD=SystemZ',
                        '-DLLVM_ENABLE_PROJECTS=mlir',
                        '-DLLVM_LIT_ARGS=-vj 4',
                    ])},

    {'name' : "mlir-s390x-linux-werror",
    'tags'  : ["mlir", "s390x"],
    'workernames' : ["onnx-mlir-nowarn-linux-s390x"],
    'builddir': "onnx-mlir-nowarn-linux-s390x",
    'factory' : UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    clean=True,
                    checks = ['check-mlir'],
                    targets = ['check-mlir-build-only'],
                    depends_on_projects=['llvm','mlir'],
                    extra_configure_args=[
                        "-DCMAKE_BUILD_TYPE=Release",
                        "-DLLVM_ENABLE_PROJECTS=mlir",
                        "-DLLVM_ENABLE_ASSERTIONS=ON",
                        "-DLLVM_ENABLE_RTTI=ON",
                        "-DLLVM_ENABLE_WERROR=ON",
                        "-DLLVM_TARGETS_TO_BUILD=host",
                    ])},

# Sanitizer builders.
#
# bootstrap-asan, bootstrap-msan, and sanitizer-x86_64-linux-fast have steps
# with large memory usage, so assign them to different workers.

    {'name' : "sanitizer-x86_64-linux",
    'tags'  : ["sanitizer", "compiler-rt"],
    'workernames' : [
        "sanitizer-buildbot1",
        "sanitizer-buildbot2",
    ],
    'builddir': "sanitizer-x86_64-linux",
    'factory' : SanitizerBuilder.getSanitizerBuildFactory()},

    {'name' : "sanitizer-x86_64-linux-fast",
    'tags'  : ["sanitizer"],
    'workernames' : [
        "sanitizer-buildbot3",
        "sanitizer-buildbot4",
    ],
    'builddir': "sanitizer-x86_64-linux-fast",
    'factory' : SanitizerBuilder.getSanitizerBuildFactory(
        extra_depends_on_projects=["mlir", "clang-tools-extra"]
    )},

    {'name' : "sanitizer-x86_64-linux-bootstrap-asan",
    'tags'  : ["sanitizer"],
    'workernames' : [
        "sanitizer-buildbot1",
        "sanitizer-buildbot2",
    ],
    'builddir': "sanitizer-x86_64-linux-bootstrap-asan",
    'factory' : SanitizerBuilder.getSanitizerBuildFactory(
        clean=True,
        extra_depends_on_projects=["mlir", "clang-tools-extra"]
    )},

    {'name' : "sanitizer-x86_64-linux-bootstrap-msan",
    'tags'  : ["sanitizer"],
    'workernames' : [
        "sanitizer-buildbot5",
        "sanitizer-buildbot6",
    ],
    'builddir': "sanitizer-x86_64-linux-bootstrap-msan",
    'factory' : SanitizerBuilder.getSanitizerBuildFactory(
        clean=True,
        extra_depends_on_projects=["mlir", "clang-tools-extra"]
    )},

    {'name' : "sanitizer-x86_64-linux-bootstrap-ubsan",
    'tags'  : ["sanitizer"],
    'workernames' : [
        "sanitizer-buildbot3",
        "sanitizer-buildbot4",
    ],
    'builddir': "sanitizer-x86_64-linux-bootstrap-ubsan",
    'factory' : SanitizerBuilder.getSanitizerBuildFactory(
        clean=True,
        extra_depends_on_projects=["mlir", "clang-tools-extra"]
    )},

    {'name' : "sanitizer-x86_64-linux-qemu",
    'tags'  : ["sanitizer"],
    'workernames' : [
        "sanitizer-buildbot3",
        "sanitizer-buildbot4",
    ],
    'builddir': "sanitizer-x86_64-linux-qemu",
    'factory' : SanitizerBuilder.getSanitizerBuildFactory()},

    {'name' : "sanitizer-x86_64-linux-fuzzer",
    'tags'  : ["sanitizer"],
    'workernames' : [
        "sanitizer-buildbot5",
        "sanitizer-buildbot6",
    ],
    'builddir': "sanitizer-x86_64-linux-fuzzer",
    'factory' : SanitizerBuilder.getSanitizerBuildFactory()},

    {'name' : "sanitizer-x86_64-linux-android",
    'tags'  : ["sanitizer"],
    'workernames' : [
        "sanitizer-buildbot-android",
    ],
    'builddir': "sanitizer-x86_64-linux-android",
    'factory' : SanitizerBuilder.getSanitizerBuildFactory()},

    {'name' : "sanitizer-aarch64-linux",
    'tags'  : ["sanitizer", "aarch64", "compiler-rt"],
    'workernames' : [
        "sanitizer-buildbot7",
        "sanitizer-buildbot8",
    ],
    'builddir': "sanitizer-aarch64-linux",
    'factory' : SanitizerBuilder.getSanitizerBuildFactory()},

    {'name' : "sanitizer-aarch64-linux-bootstrap-asan",
    'tags'  : ["sanitizer", "aarch64"],
    'workernames' : [
        "sanitizer-buildbot7",
        "sanitizer-buildbot8",
    ],
    'builddir': "sanitizer-aarch64-linux-bootstrap-asan",
    'factory' : SanitizerBuilder.getSanitizerBuildFactory(
        clean=True,
        extra_depends_on_projects=["mlir", "clang-tools-extra"]
    )},

    {'name' : "sanitizer-aarch64-linux-bootstrap-hwasan",
    'tags'  : ["sanitizer", "aarch64"],
    'workernames' : [
        "sanitizer-buildbot11",
        "sanitizer-buildbot12",
    ],
    'builddir': "sanitizer-aarch64-linux-bootstrap-hwasan",
    'factory' : SanitizerBuilder.getSanitizerBuildFactory(
        clean=True,
        extra_depends_on_projects=["mlir", "clang-tools-extra"]
    )},

    {'name' : "sanitizer-aarch64-linux-bootstrap-msan",
    'tags'  : ["sanitizer", "aarch64"],
    'workernames' : [
        "sanitizer-buildbot9",
        "sanitizer-buildbot10",
    ],
    'builddir': "sanitizer-aarch64-linux-bootstrap-msan",
    'factory' : SanitizerBuilder.getSanitizerBuildFactory(
        clean=True,
        extra_depends_on_projects=["mlir", "clang-tools-extra"]
    )},

    {'name' : "sanitizer-aarch64-linux-bootstrap-ubsan",
    'tags'  : ["sanitizer", "aarch64"],
    'workernames' : [
        "sanitizer-buildbot9",
        "sanitizer-buildbot10",
    ],
    'builddir': "sanitizer-aarch64-linux-bootstrap-ubsan",
    'factory' : SanitizerBuilder.getSanitizerBuildFactory(
        clean=True,
        extra_depends_on_projects=["mlir", "clang-tools-extra"]
    )},

    {'name' : "sanitizer-aarch64-linux-fuzzer",
    'tags'  : ["sanitizer", "aarch64"],
    'workernames' : [
        "sanitizer-buildbot11",
        "sanitizer-buildbot12",
    ],
    'builddir': "sanitizer-aarch64-linux-fuzzer",
    'factory' : SanitizerBuilder.getSanitizerBuildFactory()},

    {'name' : "sanitizer-ppc64le-linux",
    'tags'  : ["sanitizer", "ppc", "ppc64le"],
    'workernames' : ["ppc64le-sanitizer"],
    'builddir': "sanitizer-ppc64le",
    'factory' : SanitizerBuilder.getSanitizerBuildFactory(timeout=1800)},

    {'name' : "sanitizer-windows",
    'tags'  : ["sanitizer"],
    'workernames' : ["sanitizer-windows"],
    'builddir': "sanitizer-windows",
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    script="sanitizer-windows.py",
                    depends_on_projects=["llvm", "clang", "lld", "compiler-rt"],
                    # FIXME: Restore `timeout` to default when fixed https://github.com/llvm/llvm-project/issues/102513
                    timeout=2400)},

# OpenMP builders.

    {'name' : "openmp-gcc-x86_64-linux-debian",
    'tags'  : ["openmp"],
    'workernames' : ["gribozavr4"],
    'builddir': "openmp-gcc-x86_64-linux-debian",
    'factory' : OpenMPBuilder.getOpenMPCMakeBuildFactory(
                    extraCmakeArgs=[
                        '-DLLVM_CCACHE_BUILD=ON',
                    ],
                    env={
                        'PATH':'/home/llvmbb/bin/clang-latest/bin:/home/llvmbb/bin:/usr/local/bin:/usr/local/bin:/usr/bin:/bin',
                        'CC': 'clang', 'CXX': 'clang++',
                    })},

    {'name' : "openmp-clang-x86_64-linux-debian",
    'tags'  : ["openmp"],
    'workernames' : ["gribozavr4"],
    'builddir': "openmp-clang-x86_64-linux-debian",
    'factory' : OpenMPBuilder.getOpenMPCMakeBuildFactory(
                    extraCmakeArgs=[
                        '-DLLVM_CCACHE_BUILD=ON',
                    ],
                    env={
                        'PATH':'/home/llvmbb/bin/clang-latest/bin:/home/llvmbb/bin:/usr/local/bin:/usr/local/bin:/usr/bin:/bin',
                        'CC': 'clang', 'CXX': 'clang++',
                    })},

    {'name' : "openmp-s390x-linux",
    'tags'  : ["openmp"],
    'workernames' : ["systemz-1"],
    'builddir': "openmp-s390x-linux",
    'factory' : OpenMPBuilder.getOpenMPCMakeBuildFactory(
                    jobs=4,
                    extraCmakeArgs=[
                        '-DLLVM_CCACHE_BUILD=ON',
                        "-DLLVM_ENABLE_ASSERTIONS=ON",
                    ])},

    {'name' : "openmp-offload-cuda-project",
    'tags'  : ["openmp"],
    'workernames' : ["minipc-1050ti-linux"],
    'builddir': "openmp-offload-cuda-project",
    'factory' : OpenMPBuilder.getOpenMPCMakeBuildFactory(
                        clean=True,
                        enable_runtimes=['offload'],
                        extraCmakeArgs=[
                                "-DCUDAToolkit_ROOT=/opt/cuda",
                                "-DCLANG_ENABLE_STATIC_ANALYZER=OFF",
                                "-DCLANG_ENABLE_ARCMT=OFF",
                                "-DCLANG_ENABLE_OBJC_REWRITER=OFF",
                                "-DLLVM_TARGETS_TO_BUILD=X86;NVPTX",
                                "-DLLVM_ENABLE_LLD=ON",
                                '-DLLVM_PARALLEL_LINK_JOBS=2',
                                "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                                "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
                            ],
                        install=True,
                        add_lit_checks=["check-offload"],
                        testsuite=True,
                        testsuite_sollvevv=True,
                        extraTestsuiteCmakeArgs=[
                            "-DTEST_SUITE_OFFLOADING_C_FLAGS=--offload-arch=native;--cuda-path=/opt/cuda",
                            "-DTEST_SUITE_OFFLOADING_C_LDFLAGS=--offload-arch=native;--cuda-path=/opt/cuda",
                            "-DTEST_SUITE_OFFLOADING_CXX_FLAGS=--offload-arch=native;--cuda-path=/opt/cuda",
                            "-DTEST_SUITE_OFFLOADING_CXX_LDFLAGS=--offload-arch=native;--cuda-path=/opt/cuda",
                            "-DSYSTEM_GPU=nvidia", "-DTEST_SUITE_SYSTEM_GPU=nvidia",
                        ],
                        add_openmp_lit_args=["--time-tests"],
                    )},

    {'name' : "openmp-offload-cuda-runtime",
    'tags'  : ["openmp"],
    'workernames' : ["minipc-1050ti-linux"],
    'builddir': "openmp-offload-cuda-runtime",
    'factory' : OpenMPBuilder.getOpenMPCMakeBuildFactory(
                        clean=True,
                        enable_runtimes=['openmp', 'offload'],
                        extraCmakeArgs=[
                                "-DCUDAToolkit_ROOT=/opt/cuda",
                                "-DCLANG_ENABLE_STATIC_ANALYZER=OFF",
                                "-DCLANG_ENABLE_ARCMT=OFF",
                                "-DCLANG_ENABLE_OBJC_REWRITER=OFF",
                                "-DLLVM_TARGETS_TO_BUILD=X86;NVPTX",
                                "-DLLVM_ENABLE_LLD=ON",
                                '-DLLVM_PARALLEL_LINK_JOBS=2',
                                "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                                "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
                            ],
                        install=True,
                        add_lit_checks=["check-offload"],
                        testsuite=True,
                        testsuite_sollvevv=True,
                        extraTestsuiteCmakeArgs=[
                            "-DTEST_SUITE_OFFLOADING_C_FLAGS=--offload-arch=native;--cuda-path=/opt/cuda",
                            "-DTEST_SUITE_OFFLOADING_C_LDFLAGS=--offload-arch=native;--cuda-path=/opt/cuda",
                            "-DTEST_SUITE_OFFLOADING_CXX_FLAGS=--offload-arch=native;--cuda-path=/opt/cuda",
                            "-DTEST_SUITE_OFFLOADING_CXX_LDFLAGS=--offload-arch=native;--cuda-path=/opt/cuda",
                            "-DSYSTEM_GPU=nvidia", "-DTEST_SUITE_SYSTEM_GPU=nvidia",
                        ],
                        add_openmp_lit_args=["--time-tests"],
                    )},

# OpenMP AMDGPU Builders
    {'name' : "openmp-offload-amdgpu-runtime",
    'tags'  : ["openmp"],
    'workernames' : ["omp-vega20-0"],
    'builddir': "openmp-offload-amdgpu-runtime",
    'factory' : OpenMPBuilder.getOpenMPCMakeBuildFactory(
                        clean=True,
                        enable_runtimes=['compiler-rt', 'openmp', 'offload'],
                        depends_on_projects=['llvm','clang','lld', 'offload', 'openmp', 'compiler-rt'],
                        extraCmakeArgs=[
                            "-DCMAKE_BUILD_TYPE=Release",
                            "-DCLANG_DEFAULT_LINKER=lld",
                            "-DLLVM_TARGETS_TO_BUILD=X86;AMDGPU",
                            "-DLLVM_ENABLE_ASSERTIONS=ON",
                            "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                            "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
                            ],
                        env={
                            'HSA_ENABLE_SDMA':'0',
                            },
                        install=True,
                        testsuite=False,
                        testsuite_sollvevv=False,
                        extraTestsuiteCmakeArgs=[
                            "-DTEST_SUITE_SOLLVEVV_OFFLOADING_CFLAGS=-fopenmp-targets=amdgcn-amd-amdhsa;-Xopenmp-target=amdgcn-amd-amdhsa",
                            "-DTEST_SUITE_SOLLVEVV_OFFLOADING_LDLAGS=-fopenmp-targets=amdgcn-amd-amdhsa;-Xopenmp-target=amdgcn-amd-amdhsa",
                        ],
                        add_lit_checks=['check-offload'],
                        add_openmp_lit_args=["--time-tests", "--timeout 100", "--xfail=affinity/format/proc_bind.c"],
                    )},

    {'name' : "openmp-offload-amdgpu-runtime-2",
    'tags'  : ["openmp"],
    'workernames' : ["rocm-worker-hw-02"],
    'builddir': "openmp-offload-amdgpu-runtime-2",
    'factory' : OpenMPBuilder.getOpenMPCMakeBuildFactory(
                        clean=True,
                        enable_runtimes=['compiler-rt', 'libunwind', 'libc', 'libcxx', 'libcxxabi', 'openmp', 'offload'],
                        depends_on_projects=['llvm','clang','lld', 'offload', 'openmp', 'compiler-rt', 'libunwind', 'libcxx', 'libcxxabi', 'libc'],
                        extraCmakeArgs=[
                            "-DCMAKE_BUILD_TYPE=Release",
                            "-DCLANG_DEFAULT_LINKER=lld",
                            "-DLLVM_TARGETS_TO_BUILD=X86;AMDGPU",
                            "-DLLVM_ENABLE_ASSERTIONS=ON",
                            "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                            "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
                            "-DLIBCXX_ENABLE_SHARED=OFF",
                            "-DLIBCXX_ENABLE_STATIC=ON",
                            "-DLIBCXX_INSTALL_LIBRARY=OFF",
                            "-DLIBCXX_INSTALL_HEADERS=OFF",
                            "-DLIBCXXABI_ENABLE_SHARED=OFF",
                            "-DLIBCXXABI_ENABLE_STATIC=ON",
                            "-DLIBCXXABI_INSTALL_STATIC_LIBRARY=OFF",
                            "-DLLVM_ENABLE_ZLIB=ON",
                            "-DLLVM_ENABLE_Z3_SOLVER=OFF",
                            "-DLLVM_ENABLE_PER_TARGET_RUNTIME_DIR=ON",
                            "-DCMAKE_CXX_STANDARD=17",
                            "-DBUILD_SHARED_LIBS=ON",
                            "-DLLVM_ENABLE_LIBCXX=ON",
                            "-DCLANG_DEFAULT_RTLIB=compiler-rt",
                            "-DCLANG_DEFAULT_UNWINDLIB=libgcc",
                            "-DLIBOMPTARGET_PLUGINS_TO_BUILD=amdgpu;host",
                            "-DRUNTIMES_amdgcn-amd-amdhsa_LLVM_ENABLE_RUNTIMES=libc",
                            "-DLLVM_RUNTIME_TARGETS=default;amdgcn-amd-amdhsa",
                            "-DRUNTIMES_amdgcn-amd-amdhsa_LIBC_GPU_TEST_JOBS=4",
                            ],
                        env={
                            'HSA_ENABLE_SDMA':'0',
                            },
                        install=True,
                        testsuite=False,
                        testsuite_sollvevv=False,
                        extraTestsuiteCmakeArgs=[
                            "-DTEST_SUITE_SOLLVEVV_OFFLOADING_CFLAGS=-fopenmp-targets=amdgcn-amd-amdhsa;-Xopenmp-target=amdgcn-amd-amdhsa",
                            "-DTEST_SUITE_SOLLVEVV_OFFLOADING_LDLAGS=-fopenmp-targets=amdgcn-amd-amdhsa;-Xopenmp-target=amdgcn-amd-amdhsa",
                        ],
                        add_lit_checks=["check-clang", "check-llvm", "check-lld", "check-libc-amdgcn-amd-amdhsa"],
                        add_openmp_lit_args=["--time-tests", "--timeout 100"],
                        )},

    {'name' : "amdgpu-offload-ubuntu-22-cmake-build-only",
    'tags'  : ["openmp"],
    'workernames' : ["rocm-docker-ubu-22"],
    'builddir': "amdgpu-offload-ubuntu-22-cmake-build-only",
    'collapseRequests' : False,
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    depends_on_projects=["llvm", "clang", "flang", "flang-rt", "mlir", "lld", "compiler-rt", "libcxx", "libcxxabi", "openmp", "offload", "libunwind"],
                    script="amdgpu-offload-cmake.py",
                    checkout_llvm_sources=True,
                    script_interpreter=None
                )},

    {'name' : "amdgpu-offload-rhel-9-cmake-build-only",
    'tags'  : ["openmp"],
    'workernames' : ["rocm-docker-rhel-9"],
    'builddir': "amdgpu-offload-rhel-9-cmake-build-only",
    'collapseRequests' : False,
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    depends_on_projects=["llvm", "clang", "flang", "flang-rt", "mlir", "lld", "compiler-rt", "libcxx", "libcxxabi", "openmp", "offload", "libunwind"],
                    script="amdgpu-offload-cmake.py",
                    checkout_llvm_sources=True,
                    script_interpreter=None
                )},

    {'name' : "amdgpu-offload-rhel-8-cmake-build-only",
    'tags'  : ["amdgpu", "offload", "openmp"],
    'workernames' : ["rocm-docker-rhel-8"],
    'builddir': "amdgpu-offload-rhel-8-cmake-build-only",
    'collapseRequests' : False,
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    depends_on_projects=["llvm", "clang", "flang", "flang-rt", "mlir", "lld", "compiler-rt", "libcxx", "libcxxabi", "offload", "openmp", "libunwind"],
                    script="amdgpu-offload-cmake.py",
                    checkout_llvm_sources=True,
                    script_interpreter=None
                )},

    # This one has a longer turn-around time, so we cannot disallow collapsing requests
    {'name' : "hip-third-party-libs-test",
    'tags'  : ["amdgpu", "offload", "openmp"],
    'workernames' : ["ext_buildbot_hw_05-hip-docker"],
    'builddir': "hip-third-party-libs-test",
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    depends_on_projects=['llvm', 'clang', 'compiler-rt', 'lld'],
                    script="hip-tpl.py",
                    checkout_llvm_sources=True,
                    script_interpreter=None
                )},

    {'name' : "openmp-offload-libc-amdgpu-runtime",
    'tags'  : ["openmp"],
    'workernames' : ["omp-vega20-1"],
     # We would like to never collapse, but it seems the load is too high on that system to keep up.
    'builddir': "openmp-offload-libc-amdgpu-runtime",
    'factory' : OpenMPBuilder.getOpenMPCMakeBuildFactory(
                        clean=True,
                        depends_on_projects=['llvm', 'clang', 'compiler-rt', 'libc', 'lld', 'offload', 'openmp'],
                        # Special case this bot to account for new (verbose) libc build syntax
                        enable_runtimes=['openmp', 'compiler-rt', 'offload'],
                        extraCmakeArgs=[
                            "-DCMAKE_BUILD_TYPE=Release",
                            "-DCLANG_DEFAULT_LINKER=lld",
                            "-DLLVM_TARGETS_TO_BUILD=X86;AMDGPU",
                            "-DLLVM_ENABLE_ASSERTIONS=ON",
                            "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                            "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
                            "-DLIBOMPTARGET_FOUND_AMDGPU_GPU=ON",
                            "-DLIBOMP_ARCHER_SUPPORT=OFF",
                            "-DRUNTIMES_amdgcn-amd-amdhsa_LLVM_ENABLE_RUNTIMES=libc",
                            "-DLLVM_RUNTIME_TARGETS=default;amdgcn-amd-amdhsa",
                            "-DRUNTIMES_amdgcn-amd-amdhsa_LIBC_GPU_TEST_ARCHITECTURE=gfx906",
                            ],
                        env={
                            'HSA_ENABLE_SDMA':'0',
                            },
                        install=True,
                        testsuite=False,
                        testsuite_sollvevv=False,
                        extraTestsuiteCmakeArgs=[
                            "-DTEST_SUITE_SOLLVEVV_OFFLOADING_CFLAGS=-fopenmp;-fopenmp-targets=amdgcn-amd-amdhsa;-Xopenmp-target=amdgcn-amd-amdhsa;-march=gfx906",
                            "-DTEST_SUITE_SOLLVEVV_OFFLOADING_LDLAGS=-fopenmp;-fopenmp-targets=amdgcn-amd-amdhsa;-Xopenmp-target=amdgcn-amd-amdhsa;-march=gfx906",
                        ],
                        add_lit_checks=["check-offload", "check-libc-amdgcn-amd-amdhsa"],
                        add_openmp_lit_args=["--filter-out=offloading/pgo1.c"],
                    )},

    {'name' : "openmp-offload-amdgpu-clang-flang",
    'tags'  : ["openmp,flang"],
    'workernames' : ["rocm-worker-hw-01"],
    'builddir': "openmp-offload-amdgpu-clang-flang",
    'factory' : OpenMPBuilder.getOpenMPCMakeBuildFactory(
                        clean=True,
                        enable_runtimes=['compiler-rt', 'openmp', 'offload', 'flang-rt'],
                        depends_on_projects=['llvm','clang','lld', 'offload', 'openmp', 'mlir', 'flang', 'flang-rt', 'compiler-rt'],
                        extraCmakeArgs=[
                            "-DCMAKE_BUILD_TYPE=Release",
                            "-DCLANG_DEFAULT_LINKER=lld",
                            "-DLLVM_TARGETS_TO_BUILD=X86;AMDGPU",
                            "-DLLVM_ENABLE_ASSERTIONS=ON",
                            "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                            "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
                            "-DFLANG_RUNTIME_F128_MATH_LIB=libquadmath",
                            "-DLLVM_ENABLE_PER_TARGET_RUNTIME_DIR=ON",
                            "-DCMAKE_CXX_STANDARD=17",
                            "-DBUILD_SHARED_LIBS=ON",
                            "-DLIBOMPTARGET_PLUGINS_TO_BUILD=amdgpu;host",
                            "-DCOMPILER_RT_BUILD_ORC=OFF",
                            "-DCOMPILER_RT_BUILD_XRAY=OFF",
                            "-DCOMPILER_RT_BUILD_MEMPROF=OFF",
                            "-DCOMPILER_RT_BUILD_LIBFUZZER=OFF",
                            "-DCOMPILER_RT_BUILD_SANITIZERS=ON",
                            ],
                        env={
                            'HSA_ENABLE_SDMA':'0',
                            },
                        install=True,
                        testsuite=False,
                        testsuite_sollvevv=False,
                        extraTestsuiteCmakeArgs=[
                            "-DTEST_SUITE_SOLLVEVV_OFFLOADING_CFLAGS=-fopenmp-targets=amdgcn-amd-amdhsa;-Xopenmp-target=amdgcn-amd-amdhsa",
                            "-DTEST_SUITE_SOLLVEVV_OFFLOADING_LDLAGS=-fopenmp-targets=amdgcn-amd-amdhsa;-Xopenmp-target=amdgcn-amd-amdhsa",
                        ],
                        add_lit_checks=["check-flang", "check-flang-rt", "check-offload"],
                        add_openmp_lit_args=["--time-tests", "--timeout 100"],
                    )},

    # This bot, for now does not run OpenMP/Offload runtime tests, as we have no GPU yet
    {'name' : "openmp-offload-sles-build-only",
    'tags'  : ["openmp"],
    'workernames' : ["rocm-worker-hw-04-sles"],
    'builddir': "openmp-offload-sles-build",
    'factory' : OpenMPBuilder.getOpenMPCMakeBuildFactory(
                        clean=True,
                        test=False, # we have no GPU avail, skip runtime tests
                        enable_runtimes=['openmp', 'compiler-rt', 'offload', 'flang-rt'],
                        depends_on_projects=['llvm','clang', 'flang', 'flang-rt', 'lld', 'mlir', 'offload', 'openmp', 'compiler-rt'],
                        extraCmakeArgs=[
                            "-DCMAKE_BUILD_TYPE=Release",
                            "-DCLANG_DEFAULT_LINKER=lld",
                            "-DLLVM_TARGETS_TO_BUILD=X86;AMDGPU",
                            "-DLLVM_ENABLE_ASSERTIONS=ON",
                            "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                            "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
                            ],
                        env={
                            'HSA_ENABLE_SDMA':'0',
                            'LD_LIBRARY_PATH':'/opt/rocm/lib',
                            },
                        install=True,
                        testsuite=False,
                        testsuite_sollvevv=False,
                        extraTestsuiteCmakeArgs=[
                            "-DTEST_SUITE_SOLLVEVV_OFFLOADING_CFLAGS=-fopenmp-targets=amdgcn-amd-amdhsa;-Xopenmp-target=amdgcn-amd-amdhsa",
                            "-DTEST_SUITE_SOLLVEVV_OFFLOADING_LDLAGS=-fopenmp-targets=amdgcn-amd-amdhsa;-Xopenmp-target=amdgcn-amd-amdhsa",
                        ],
                        add_lit_checks=["check-clang", "check-flang", "check-flang-rt", "check-llvm", "check-lld", "check-mlir"],
                        add_openmp_lit_args=["--time-tests", "--timeout 100"],
                    )},

    {'name' : "openmp-offload-rhel-9_4",
    'tags'  : ["openmp"],
    'workernames' : ["rocm-worker-hw-04-rhel-9_4"],
    'builddir': "openmp-offload-rhel-9.4-build",
    'factory' : OpenMPBuilder.getOpenMPCMakeBuildFactory(
                        clean=True,
                        test=True,
                        enable_runtimes=['openmp', 'compiler-rt', 'offload', 'flang-rt'],
                        depends_on_projects=['llvm','clang', 'flang', 'flang-rt', 'lld', 'mlir', 'offload', 'openmp', 'compiler-rt'],
                        extraCmakeArgs=[
                            "-DCMAKE_BUILD_TYPE=Release",
                            "-DCLANG_DEFAULT_LINKER=lld",
                            "-DLLVM_TARGETS_TO_BUILD=X86;AMDGPU",
                            "-DLLVM_ENABLE_ASSERTIONS=ON",
                            "-DLIBOMP_ARCHER_SUPPORT=OFF",
                            "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                            "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
                            ],
                        env={
                            'HSA_ENABLE_SDMA':'0',
                            'LD_LIBRARY_PATH':'/opt/rocm/lib',
                            },
                        install=True,
                        testsuite=False,
                        testsuite_sollvevv=False,
                        extraTestsuiteCmakeArgs=[
                            "-DTEST_SUITE_SOLLVEVV_OFFLOADING_CFLAGS=-fopenmp-targets=amdgcn-amd-amdhsa;-Xopenmp-target=amdgcn-amd-amdhsa",
                            "-DTEST_SUITE_SOLLVEVV_OFFLOADING_LDLAGS=-fopenmp-targets=amdgcn-amd-amdhsa;-Xopenmp-target=amdgcn-amd-amdhsa",
                        ],
                        add_lit_checks=["check-clang", "check-flang", "check-flang-rt", "check-llvm", "check-lld", "check-mlir", "check-offload"],
                        add_openmp_lit_args=["--time-tests", "--timeout 100", "--xfail=affinity/format/proc_bind.c"],
                    )},

    {'name' : "openmp-offload-rhel-8_8",
    'tags'  : ["openmp"],
    'workernames' : ["rocm-worker-hw-04-rhel-8_8"],
    'builddir': "openmp-offload-rhel-8.8-build",
    'factory' : OpenMPBuilder.getOpenMPCMakeBuildFactory(
                        clean=True,
                        test=True,
                        enable_runtimes=['openmp', 'compiler-rt', 'offload', 'flang-rt'],
                        depends_on_projects=['llvm','clang', 'flang', 'flang-rt', 'lld', 'mlir', 'offload', 'openmp', 'compiler-rt'],
                        extraCmakeArgs=[
                            "-DCMAKE_BUILD_TYPE=Release",
                            "-DCLANG_DEFAULT_LINKER=lld",
                            "-DLLVM_TARGETS_TO_BUILD=X86;AMDGPU",
                            "-DLLVM_ENABLE_ASSERTIONS=ON",
                            "-DLIBOMP_ARCHER_SUPPORT=OFF",
                            "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                            "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
                            ],
                        env={
                            'HSA_ENABLE_SDMA':'0',
                            'LD_LIBRARY_PATH':'/opt/rocm/lib',
                            },
                        install=True,
                        testsuite=False,
                        testsuite_sollvevv=False,
                        extraTestsuiteCmakeArgs=[
                            "-DTEST_SUITE_SOLLVEVV_OFFLOADING_CFLAGS=-fopenmp-targets=amdgcn-amd-amdhsa;-Xopenmp-target=amdgcn-amd-amdhsa",
                            "-DTEST_SUITE_SOLLVEVV_OFFLOADING_LDLAGS=-fopenmp-targets=amdgcn-amd-amdhsa;-Xopenmp-target=amdgcn-amd-amdhsa",
                        ],
                        add_lit_checks=["check-clang", "check-flang", "check-flang-rt", "check-llvm", "check-lld", "check-mlir", "check-offload"],
                        add_openmp_lit_args=["--time-tests", "--timeout 100", "--xfail=affinity/format/proc_bind.c"],
                    )},


# Whole-toolchain builders.

    {'name': "fuchsia-x86_64-linux",
    'tags'  : ["toolchain"],
    'workernames' :["fuchsia-debian-64-us-central1-a-1", "fuchsia-debian-64-us-central1-b-1"],
    'builddir': "fuchsia-x86_64-linux",
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    script="fuchsia-linux.py",
                    depends_on_projects=[
                        'bolt',
                        'clang',
                        'clang-tools-extra',
                        'compiler-rt',
                        'libc',
                        'libcxx',
                        'libcxxabi',
                        'libunwind',
                        'lld',
                        'lldb',
                        'llvm',
                        'polly'
                    ])},

    {'name': "fuchsia-x86_64-linux-staging",
    'tags'  : ["toolchain"],
    'workernames' :["fuchsia-debian-64-staging-1", "fuchsia-debian-64-staging-2"],
    'builddir': "fuchsia-x86_64-linux-staging",
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    script="fuchsia-linux-staging.py",
                    depends_on_projects=[
                        'bolt',
                        'clang',
                        'clang-tools-extra',
                        'compiler-rt',
                        'libc',
                        'libcxx',
                        'libcxxabi',
                        'libunwind',
                        'lld',
                        'lldb',
                        'llvm',
                        'polly'
                    ])},

# libc Builders.

    {'name' : 'libc-x86_64-windows-dbg',
    'tags'  : ["libc"],
    'workernames' : ['libc-x86_64-windows'],
    'builddir': 'libc-x86_64-windows',
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    script="libc-windows.py",
                    depends_on_projects=['llvm', 'libc', 'clang', 'clang-tools-extra'],
                    extra_args=['--debug'])},

    {'name' : 'libc-arm32-qemu-debian-dbg',
    'tags'  : ["libc"],
    'workernames' : ['libc-arm32-qemu-debian'],
    'builddir': 'libc-arm32-qemu-debian-dbg',
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    script="libc-linux.py",
                    depends_on_projects=['llvm', 'libc', 'clang', 'clang-tools-extra'],
                    extra_args=['--debug'])},

    {'name' : 'libc-aarch64-ubuntu-dbg',
    'tags'  : ["libc"],
    'workernames' : ['libc-aarch64-ubuntu'],
    'builddir': 'libc-aarch64-ubuntu',
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    script="libc-linux.py",
                    depends_on_projects=['llvm', 'libc', 'clang', 'clang-tools-extra'],
                    extra_args=['--debug'])},

    {'name' : "libc-aarch64-ubuntu-fullbuild-dbg",
    'tags'  : ["libc"],
    'workernames' : ["libc-aarch64-ubuntu"],
    'builddir': "libc-aarch64-ubuntu-fullbuild-dbg",
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    script="libc-linux.py",
                    depends_on_projects=['llvm', 'libc', 'clang', 'clang-tools-extra'],
                    extra_args=['--debug'])},

    {'name' : 'libc-x86_64-debian',
    'tags'  : ["libc"],
    'workernames' : ['libc-x86_64-debian'],
    'builddir': 'libc-x86_64-debian',
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    script="libc-linux.py",
                    depends_on_projects=['llvm', 'libc', 'clang', 'clang-tools-extra'])},

    {'name' : "libc-x86_64-debian-dbg",
    'tags'  : ["libc"],
    'workernames' : ["libc-x86_64-debian"],
    'builddir': "libc-x86_64-debian-dbg",
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    script="libc-linux.py",
                    depends_on_projects=['llvm', 'libc', 'clang', 'clang-tools-extra'],
                    extra_args=['--debug'])},

    {'name' : "libc-x86_64-debian-dbg-asan",
    'tags'  : ["libc"],
    'workernames' : ["libc-x86_64-debian"],
    'builddir': "libc-x86_64-debian-dbg-asan",
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    script="libc-linux.py",
                    depends_on_projects=['llvm', 'libc', 'clang', 'clang-tools-extra'],
                    extra_args=['--debug', '--asan'])},

    {'name' : "libc-x86_64-debian-dbg-bootstrap-build",
    'tags'  : ["libc"],
    'workernames' : ["libc-x86_64-debian"],
    'builddir': "libc-x86_64-debian-dbg-bootstrap-build",
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    script="libc-linux.py",
                    depends_on_projects=['llvm', 'libc', 'clang', 'clang-tools-extra'],
                    extra_args=['--debug'])},

    {'name' : "libc-x86_64-debian-fullbuild-dbg",
    'tags'  : ["libc"],
    'workernames' : ["libc-x86_64-debian-fullbuild"],
    'builddir': "libc-x86_64-debian-fullbuild-dbg",
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    script="libc-linux.py",
                    depends_on_projects=['llvm', 'libc', 'clang', 'clang-tools-extra'],
                    extra_args=['--debug'])},

    {'name' : "libc-x86_64-debian-gcc-fullbuild-dbg",
    'tags'  : ["libc"],
    'workernames' : ["libc-x86_64-debian-fullbuild"],
    'builddir': "libc-x86_64-debian-gcc-fullbuild-dbg",
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    script="libc-linux.py",
                    depends_on_projects=['llvm', 'libc', 'clang', 'clang-tools-extra'],
                    extra_args=['--debug'])},

    {'name' : "libc-x86_64-debian-fullbuild-dbg-asan",
    'tags'  : ["libc"],
    'workernames' : ["libc-x86_64-debian-fullbuild"],
    'builddir': "libc-x86_64-debian-fullbuild-dbg-asan",
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    script="libc-linux.py",
                    depends_on_projects=['llvm', 'libc', 'clang', 'clang-tools-extra'],
                    extra_args=['--debug', '--asan'])},

    {'name' : "libc-x86_64-debian-dbg-lint",
    'tags'  : ["libc"],
    'workernames' : ["libc-lint-worker"],
    'builddir': "libc-x86_64-debian-dbg-lint",
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    script="libc-linux.py",
                    depends_on_projects=['llvm', 'libc'],
                    extra_args=['--debug'])},

    {'name' : 'libc-riscv64-debian-dbg',
    'tags'  : ["libc"],
    'workernames' : ['libc-riscv64-debian'],
    'builddir': 'libc-riscv64-debian-dbg',
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    script="libc-linux.py",
                    depends_on_projects=['llvm', 'libc'],
                    extra_args=['--debug'])},

    {'name' : "libc-riscv64-debian-fullbuild-dbg",
    'tags'  : ["libc"],
    'workernames' : ["libc-riscv64-debian"],
    'builddir': "libc-riscv64-debian-fullbuild-dbg",
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    script="libc-linux.py",
                    depends_on_projects=['llvm', 'libc'],
                    extra_args=['--debug'])},

    {'name' : "libc-riscv32-qemu-yocto-fullbuild-dbg",
    'tags'  : ["libc"],
    'workernames' : ["rv32gc-qemu-system"], # TODO: workername?
    'builddir': "libc-riscv32-qemu-yocto-fullbuild-dbg",
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    script="libc-linux.py",
                    depends_on_projects=['llvm', 'libc'],
                    extra_args=['--debug'])},

# Flang builders.

    {'name' : "flang-aarch64-dylib",
    'tags'  : ["flang"],
    'workernames' : ["linaro-flang-aarch64-dylib"],
    'builddir': "flang-aarch64-dylib",
    'factory' : UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    clean=True,
                    checks=['check-flang','check-flang-rt'],
                    depends_on_projects=['llvm','mlir','clang','flang','flang-rt','openmp'],
                    extra_configure_args=[
                        "-DLLVM_TARGETS_TO_BUILD=AArch64",
                        "-DLLVM_BUILD_LLVM_DYLIB=ON",
                        "-DLLVM_LINK_LLVM_DYLIB=ON",
                        "-DCMAKE_CXX_STANDARD=17",
                    ])},

    {'name' : "flang-aarch64-sharedlibs",
    'tags'  : ["flang"],
    'workernames' : ["linaro-flang-aarch64-sharedlibs"],
    'builddir': "flang-aarch64-sharedlibs",
    'factory' : UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    clean=True,
                    checks=['check-flang','check-flang-rt'],
                    depends_on_projects=['llvm','mlir','clang','flang','flang-rt','openmp'],
                    extra_configure_args=[
                        "-DLLVM_TARGETS_TO_BUILD=AArch64",
                        "-DBUILD_SHARED_LIBS=ON",
                        "-DLLVM_BUILD_EXAMPLES=ON",
                        "-DCMAKE_CXX_STANDARD=17",
                    ])},

    {'name' : "flang-aarch64-out-of-tree",
    'tags'  : ["flang"],
    'workernames' : ["linaro-flang-aarch64-out-of-tree"],
    'builddir': "flang-aarch64-out-of-tree",
    'factory' : FlangBuilder.getFlangOutOfTreeBuildFactory(
                    checks=['check-flang'],
                    llvm_extra_configure_args=[
                        "-DLLVM_TARGETS_TO_BUILD=AArch64",
                        "-DCMAKE_CXX_STANDARD=17",
                        "-DLLVM_ENABLE_WERROR=OFF",
                        "-DLLVM_ENABLE_ASSERTIONS=ON",
                        "-DCMAKE_BUILD_TYPE=Release",
                    ],
                    flang_extra_configure_args=[
                        "-DFLANG_ENABLE_WERROR=ON",
                        "-DCMAKE_BUILD_TYPE=Release",
                    ],
                    flang_rt_extra_configure_args=[
                        "-DCMAKE_BUILD_TYPE=Release",
                    ])},

    {'name' : "flang-aarch64-debug-reverse-iteration",
    'tags'  : ["flang", "rev_iter"],
    'workernames' : ["linaro-flang-aarch64-debug-reverse-iteration"],
    'builddir': "flang-aarch64-debug-reverse-iteration",
    'factory' : UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    clean=True,
                    checks=['check-flang','check-flang-rt'],
                    depends_on_projects=['llvm','mlir','clang','flang','flang-rt','openmp'],
                    extra_configure_args=[
                        "-DLLVM_TARGETS_TO_BUILD=AArch64",
                        "-DCMAKE_BUILD_TYPE=Debug",
                        "-DCMAKE_CXX_STANDARD=17",
                        "-DLLVM_USE_LINKER=lld",
                        "-DLLVM_REVERSE_ITERATION:BOOL=ON",
                    ])},

    {'name' : "flang-aarch64-libcxx",
    'tags'  : ['flang'],
    'workernames' : ["linaro-flang-aarch64-libcxx"],
    'builddir': "flang-aarch64-libcxx",
    'factory' : FlangBuilder.getFlangOutOfTreeBuildFactory(
                    checks=['check-flang'],
                    llvm_extra_configure_args=[
                        "-DLLVM_TARGETS_TO_BUILD=AArch64",
                        "-DCMAKE_CXX_STANDARD=17",
                        "-DLLVM_ENABLE_WERROR=OFF",
                        "-DLLVM_ENABLE_ASSERTIONS=ON",
                        "-DLLVM_ENABLE_LIBCXX=On",
                        "-DCMAKE_BUILD_TYPE=Release",
                    ],
                    flang_extra_configure_args=[
                        "-DFLANG_ENABLE_WERROR=ON",
                        "-DLLVM_ENABLE_ASSERTIONS=ON",
                        "-DLLVM_ENABLE_LIBCXX=On",
                        "-DCMAKE_BUILD_TYPE=Release",
                    ],
                    flang_rt_extra_configure_args=[
                        "-DLLVM_ENABLE_ASSERTIONS=ON",
                        "-DLLVM_ENABLE_LIBCXX=On",
                        "-DCMAKE_BUILD_TYPE=Release",
                    ])},

    {'name' : "flang-aarch64-release",
    'tags'  : ["flang"],
    'workernames' : ["linaro-flang-aarch64-release"],
    'builddir': "flang-aarch64-release",
    'factory' : UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    clean=True,
                    checks=['check-flang','check-flang-rt'],
                    depends_on_projects=['llvm','mlir','clang','flang','flang-rt','openmp'],
                    extra_configure_args=[
                        "-DLLVM_TARGETS_TO_BUILD=AArch64",
                        "-DCMAKE_BUILD_TYPE=Release",
                        "-DLLVM_ENABLE_ASSERTIONS=OFF",
                        "-DCMAKE_CXX_STANDARD=17",
                    ])},

    {'name' : "flang-aarch64-rel-assert",
    'tags'  : ["flang"],
    'workernames' : ["linaro-flang-aarch64-rel-assert"],
    'builddir': "flang-aarch64-rel-assert",
    'factory' : UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    clean=True,
                    checks=['check-flang','check-flang-rt'],
                    depends_on_projects=['llvm','mlir','clang','flang','flang-rt','openmp'],
                    extra_configure_args=[
                        "-DLLVM_TARGETS_TO_BUILD=AArch64",
                        "-DLLVM_ENABLE_ASSERTIONS=ON",
                        "-DLLVM_BUILD_EXAMPLES=ON",
                        "-DCMAKE_BUILD_TYPE=Release",
                        "-DCMAKE_CXX_STANDARD=17",
                    ])},

    {'name' : "flang-aarch64-latest-gcc",
    'tags'  : ['flang'],
    'workernames' : ["linaro-flang-aarch64-latest-gcc"],
    'builddir': "flang-aarch64-latest-gcc",
    'factory' : UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    clean=True,
                    checks=['check-flang','check-flang-rt'],
                    depends_on_projects=['llvm','mlir','clang','flang','flang-rt','openmp'],
                    extra_configure_args=[
                        "-DLLVM_TARGETS_TO_BUILD=AArch64",
                        "-DLLVM_INSTALL_UTILS=ON",
                        "-DCMAKE_CXX_STANDARD=17",
                        "-DLLVM_ENABLE_WERROR=OFF",
                        "-DBUILD_SHARED_LIBS=ON",
                        "-DLLVM_ENABLE_ASSERTIONS=ON",
                        "-DCMAKE_BUILD_TYPE=Release",
                    ])},

    {'name' : "flang-x86_64-knl-linux",
    'tags'  : ["flang"],
    'workernames' : ["alcf-theta-flang"],
    'builddir': "flang-x86_64-knl-linux",
    'factory' : UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    depends_on_projects=['llvm','mlir','clang','flang'],
                    extra_configure_args=[
                        "-DLLVM_TARGETS_TO_BUILD=X86",
                        "-DCMAKE_C_COMPILER=gcc",
                        "-DCMAKE_CXX_COMPILER=g++",
                        "-DLLVM_INSTALL_UTILS=ON",
                        "-DCMAKE_CXX_STANDARD=17",
                    ])},

    {'name' : 'ppc64le-flang-rhel-clang',
    'tags'  : ["flang", "ppc", "ppc64le"],
    'collapseRequests' : False,
    'workernames' : ['ppc64le-flang-rhel-test'],
    'builddir': 'ppc64le-flang-rhel-clang-build',
    'factory' : UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    clean=True,
                    depends_on_projects=['llvm', 'mlir', 'clang', 'flang','flang-rt','openmp'],
                    checks=['check-flang','check-flang-rt'],
                    extra_configure_args=[
                        '-DLLVM_TARGETS_TO_BUILD=PowerPC',
                        '-DLLVM_INSTALL_UTILS=ON',
                        '-DCMAKE_CXX_STANDARD=17',
                        '-DLLVM_LIT_ARGS=-vj 256',
                        '-DFLANG_ENABLE_WERROR=ON',
                        '-DLLVM_ENABLE_ASSERTIONS=ON',
                        '-DCMAKE_C_COMPILER_LAUNCHER=ccache',
                        '-DCMAKE_CXX_COMPILER_LAUNCHER=ccache'
                    ],
                    env={
                        'CC': 'clang',
                        'CXX': 'clang++',
                        'LD': 'lld'
                    })},

    {'name' : "flang-x86_64-windows",
    'tags'  : ["flang"],
    'workernames' : ["minipc-ryzen-win"],
    'builddir': "flang-x86_64-windows",
    'factory' : UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    depends_on_projects=['llvm','mlir','clang','compiler-rt','flang','flang-rt'],
                    checks=['check-flang','check-flang-rt'],
                    install_dir="flang.install",
                    extra_configure_args=[
                        "-DCLANG_ENABLE_STATIC_ANALYZER=OFF",
                        "-DCLANG_ENABLE_ARCMT=OFF",
                        "-DCLANG_ENABLE_OBJC_REWRITER=OFF",
                        "-DLLVM_TARGETS_TO_BUILD=X86",
                        "-DLLVM_INSTALL_UTILS=ON",
                        "-DCMAKE_C_COMPILER=cl",
                        "-DCMAKE_CXX_COMPILER=cl",
                        "-DCMAKE_CXX_STANDARD=17",
                        '-DLLVM_PARALLEL_COMPILE_JOBS=4',
                    ])},

    {'name': "flang-arm64-windows-msvc",
    'tags' : ["mlir", "flang"],
    'workernames' : ["linaro-armv8-windows-msvc-01"],
    'builddir': "flang-arm64-windows-msvc",
    'factory' : UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    depends_on_projects=['llvm', 'clang', 'lld', 'mlir', 'compiler-rt', 'openmp', 'flang','flang-rt'],
                    checks=['check-mlir', 'check-flang', 'check-flang-rt'],
                    extra_configure_args=[
                        "-DLLVM_TARGETS_TO_BUILD=X86;AArch64",
                        "-DCLANG_DEFAULT_LINKER=lld",
                        "-DCMAKE_TRY_COMPILE_CONFIGURATION=Release",
                        "-DCOMPILER_RT_BUILD_SANITIZERS=OFF",
                        "-DLLVM_CCACHE_BUILD=ON"])},

    {'name' : 'ppc64-flang-aix',
    'tags'  : ["flang", "ppc", "ppc64", "aix"],
    'workernames' : ['ppc64-flang-aix-test'],
    'builddir': 'ppc64-flang-aix-build',
    'factory' : UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    clean=False,
                    depends_on_projects=['llvm', 'mlir', 'clang', 'flang', 'flang-rt', 'compiler-rt', 'openmp'],
                    checks=['check-flang', 'check-flang-rt'],
                    extra_configure_args=[
                        '-DLLVM_DEFAULT_TARGET_TRIPLE=powerpc64-ibm-aix',
                        '-DLLVM_INSTALL_UTILS=ON',
                        '-DCMAKE_CXX_STANDARD=17',
                        '-DLLVM_LIT_ARGS=--threads=20 -v --time-tests',
                        '-DFLANG_ENABLE_WERROR=ON',
                        '-DLLVM_ENABLE_ASSERTIONS=ON',
                        "-DPython3_EXECUTABLE:FILEPATH=python3",
                        "-DLLVM_ENABLE_ZLIB=OFF", "-DLLVM_APPEND_VC_REV=OFF",
                        "-DLLVM_PARALLEL_LINK_JOBS=2",
                        "-DSANITIZER_DISABLE_SYMBOLIZER_PATH_SEARCH:BOOL=ON",
                    ],
                    env={
                        'CC': 'clang',
                        'CXX': 'clang++',
                        'LD': 'lld',
                        'OBJECT_MODE': '64'
                    })},

# Builders responsible building Sphinx documentation.

    {'name' : "lld-sphinx-docs",
    'tags'  : ["lld", "doc"],
    'workernames' : ["gribozavr3"],
    'builddir': "lld-sphinx-docs",
    'factory' : SphinxDocsBuilder.getSphinxDocsBuildFactory(lld_html=True)},

    {'name':"libunwind-sphinx-docs",
    'tags'  : ["libunwind", "doc"],
    'workernames':["gribozavr3"],
    'builddir':"libunwind-sphinx-docs",
    'factory': SphinxDocsBuilder.getSphinxRuntimesDocsBuildFactory(libunwind_html=True)},

    {'name' : "polly-sphinx-docs",
    'tags'  : ["llvm", "doc"],
    'workernames' : ["polly-x86_64-gce1"],
    'builddir': "polly-sphinx-docs",
    'factory': SphinxDocsBuilder.getSphinxDocsBuildFactory(polly_html=True)},

    # Sphinx doc Publisher
    {'name' : "publish-sphinx-docs",
    'tags'  : ["doc"],
    'workernames' : ["as-worker-4"],
    'builddir': "publish-sphinx-docs",
    'factory' : SphinxDocsBuilder.getLLVMDocsBuildFactory(clean=True)},

    {'name' : "publish-runtimes-sphinx-docs",
    'tags'  : ["doc"],
    'workernames' : ["as-worker-4"],
    'builddir': "publish-runtimes-sphinx-docs",
    'factory' : SphinxDocsBuilder.getLLVMRuntimesDocsBuildFactory(
                    clean=True,
                    extra_configure_args=[
                        "-DLIBCXX_INCLUDE_BENCHMARKS=OFF",
                    ])},

    {'name' : "publish-lnt-sphinx-docs",
    'tags'  : ["doc"],
    'workernames' : ["as-worker-4"],
    'builddir': "publish-lnt-sphinx-docs",
    'factory' : HtmlDocsBuilder.getHtmlDocsBuildFactory()},

    {'name' : "publish-doxygen-docs",
    'tags'  : ["doc"],
    'workernames' : ["as-worker-4"], #FIXME: Temporarily disabled failing doxygen build - as-builder-8.
    'builddir': "publish-doxygen-docs",
    'factory' : DoxygenDocsBuilder.getLLVMDocsBuildFactory(
                    # Doxygen builds the final result for really
                    # long time without any output.
                    # We have to have a long timeout here.
                    timeout=172800)},

# CUDA builders.

    {'name' : "clang-cuda-l4",
    'tags'  : ["clang", "silent"],
    'workernames' : ["cuda-l4-0"],
    'builddir': "clang-cuda-l4",
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    script="/buildbot/cuda-build",
                    depends_on_projects=['llvm', 'clang', 'compiler-rt',
                                         'libc', 'libcxx', 'libcxxabi',
                                         'libunwind', 'lld', 'offload'],
                    checkout_llvm_sources=False)},

    {'name' : "clang-cuda-p4",
    'tags'  : ["clang", "silent"],
    'workernames' : ["cuda-p4-0"],
    'builddir': "clang-cuda-p4",
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    script="/buildbot/cuda-build",
                    depends_on_projects=['llvm', 'clang', 'compiler-rt',
                                         'libc', 'libcxx', 'libcxxabi',
                                         'libunwind', 'lld', 'offload'],
                    checkout_llvm_sources=False)},

    {'name' : "clang-cuda-t4",
    'tags'  : ["clang", "silent"],
    'workernames' : ["cuda-t4-0"],
    'builddir': "clang-cuda-t4",
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    script="/buildbot/cuda-build",
                    depends_on_projects=['llvm', 'clang', 'compiler-rt',
                                         'libc', 'libcxx', 'libcxxabi',
                                         'libunwind', 'lld', 'offload'],
                    checkout_llvm_sources=False)},

# HIP builders.
    {'name' : "clang-hip-vega20",
    'tags'  : ["clang"],
    'workernames' : ["hip-vega20-0"],
    'builddir': "clang-hip-vega20",
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    script="hip-build.sh",
                    checkout_llvm_sources=False,
                    script_interpreter=None)},

# VE builders.
    {'name' : "clang-ve-ninja",
    'tags'  : ["clang"],
    'workernames':["hpce-ve-main"],
    'builddir':"clang-ve-ninja",
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    script="ve-linux.py",
                    depends_on_projects=['llvm', 'clang', 'compiler-rt', 'libcxx'])},
    {'name' : "clang-ve-staging",
    'tags'  : ["clang"],
    'workernames':["hpce-ve-staging"],
    'builddir':"clang-ve-staging",
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    script="ve-linux.py",
                    depends_on_projects=['llvm', 'clang', 'compiler-rt', 'libcxx'])},

    # Build the LLVM dylib .so with all backends and link tools to it
    {'name' : 'llvm-x86_64-debian-dylib',
    'tags'  : ['llvm'],
    'collapseRequests': False,
    'workernames': ['gribozavr4'],
    'builddir': 'llvm-x86_64-debian-dylib',
    'factory' : UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    clean=True,
                    depends_on_projects=['llvm', 'clang', 'lldb', 'lld', 'clang-tools-extra'],
                    checks=['check-clang', 'check-llvm', 'check-lld', 'check-clang-extra'],
                    extra_configure_args=[
                        '-DCMAKE_BUILD_TYPE=Release',
                        '-DLLVM_ENABLE_ASSERTIONS=On',
                        '-DLLVM_BUILD_EXAMPLES=Off',
                        "-DLLVM_LIT_ARGS=-v --xunit-xml-output test-results.xml",
                        '-DLLVM_TARGETS_TO_BUILD=all',
                        '-DCMAKE_EXPORT_COMPILE_COMMANDS=1',
                        '-DLLVM_BUILD_LLVM_DYLIB=On',
                        '-DLLVM_LINK_LLVM_DYLIB=On',
                        '-DCLANG_BUILD_CLANG_DYLIB=On',
                        '-DCLANG_LINK_CLANG_DYLIB=On',
                        '-DBUILD_SHARED_LIBS=Off',
                        '-DLLVM_ENABLE_LLD=Off',
                        '-DLLVM_ENABLE_BINDINGS=Off',
                        '-DLLVM_CCACHE_BUILD=ON',
                    ],
                    env={
                        'PATH':'/home/llvmbb/bin/clang-latest/bin:/home/llvmbb/bin:/usr/local/bin:/usr/local/bin:/usr/bin:/bin',
                        'CC': 'clang', 'CXX': 'clang++',
                    })},

    {'name' : "clang-solaris11-amd64",
    'tags' : ["clang"],
    'workernames' : ["solaris11-amd64"],
    'builddir': "clang-solaris11-amd64",
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                    jobs=8,
                    clean=False,
                    timeout=1800,
                    checkout_lld=False,
                    enable_runtimes=None,
                    extra_cmake_args=['-DLLVM_ENABLE_ASSERTIONS=ON',
                                    '-DLLVM_TARGETS_TO_BUILD=X86',
                                    '-DLLVM_HOST_TRIPLE=amd64-pc-solaris2.11',
                                    '-DLLVM_PARALLEL_LINK_JOBS=4'])},

    {'name' : "clang-solaris11-sparcv9",
    'tags' : ["clang"],
    'workernames' : ["solaris11-sparcv9"],
    'builddir': "clang-solaris11-sparcv9",
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                    jobs=8,
                    clean=False,
                    timeout=1800,
                    checkout_lld=False,
                    enable_runtimes=None,
                    extra_cmake_args=['-DLLVM_ENABLE_ASSERTIONS=ON',
                                    '-DLLVM_TARGETS_TO_BUILD=Sparc',
                                    '-DLLVM_HOST_TRIPLE=sparcv9-sun-solaris2.11',
                                    '-DLLVM_PARALLEL_LINK_JOBS=4'])},

# Builders for ML-driven compiler optimizations.

    # Development mode build bot: tensorflow C APIs are present, and
    # we can dynamically load models, and produce training logs.
    {'name' : "ml-opt-dev-x86-64",
    'tags'  : ['ml_opt'],
    'collapseRequests': False,
    'workernames' : ["ml-opt-dev-x86-64-b1", "ml-opt-dev-x86-64-b2"],
    'builddir': "ml-opt-dev-x86-64-b1",
    'factory' : UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    clean=True,
                    depends_on_projects=['llvm'],
                    extra_configure_args=[
                        "-DCMAKE_BUILD_TYPE=Release",
                        "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                        "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
                        "-DLLVM_ENABLE_ASSERTIONS=ON",
                        "-DTENSORFLOW_C_LIB_PATH=/tmp/tensorflow",
                        "-C", "/tmp/tflitebuild/tflite.cmake",
                        "-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=ON"
                    ])},

    # Both tensorflow C library, and the pip package, are present.
    {'name' : "ml-opt-devrel-x86-64",
    'tags'  : ["ml_opt"],
    'collapseRequests': False,
    'workernames' : ["ml-opt-devrel-x86-64-b1", "ml-opt-devrel-x86-64-b2"],
    'builddir': "ml-opt-devrel-x86-64-b1",
    'factory' : UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    clean=True,
                    depends_on_projects=['llvm'],
                    extra_configure_args= [
                        "-DCMAKE_BUILD_TYPE=Release",
                        "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                        "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
                        "-DLLVM_ENABLE_ASSERTIONS=ON",
                        "-DTENSORFLOW_C_LIB_PATH=/tmp/tensorflow",
                        "-C", "/tmp/tflitebuild/tflite.cmake",
                        "-DTENSORFLOW_AOT_PATH=/var/lib/buildbot/.local/lib/python3.7/site-packages/tensorflow",
                        "-DCMAKE_INSTALL_RPATH_USE_LINK_PATH=ON"
                    ])},

    # Release mode build bot: the model is pre-built and linked in the
    # compiler. Only the tensorflow pip package is needed, and out of it,
    # only saved_model_cli (the model compiler) and the thin C++ wrappers
    # in xla_aot_runtime_src (and include files)
    {'name' : "ml-opt-rel-x86-64",
    'tags'  : ["ml_opt"],
    'collapseRequests': False,
    'workernames' : ["ml-opt-rel-x86-64-b1", "ml-opt-rel-x86-64-b2"],
    'builddir': "ml-opt-rel-x86-64-b1",
    'factory' : UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    clean=True,
                    depends_on_projects=['llvm'],
                    extra_configure_args= [
                        "-DCMAKE_BUILD_TYPE=Release",
                        "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                        "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
                        "-DLLVM_ENABLE_ASSERTIONS=ON",
                        "-DTENSORFLOW_AOT_PATH=/var/lib/buildbot/.local/lib/python3.7/site-packages/tensorflow"
                    ])},

    # build clangd with remote-index enabled and check with TSan
    {'name': "clangd-ubuntu-tsan",
     'tags': ["clangd"],
     'workernames': ["clangd-ubuntu-clang"],
     'builddir': "clangd-ubuntu-tsan",
     'factory': UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
         clean=True,
         depends_on_projects=["llvm", "clang", "clang-tools-extra"],
         checks=["check-clangd"],
         targets=["clangd", "clangd-index-server", "clangd-indexer"],
         extra_configure_args=[
             "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
             "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
             "-DLLVM_USE_SANITIZER=Thread",
             "-DCMAKE_BUILD_TYPE=Release",
             "-DCLANGD_ENABLE_REMOTE=ON",
             "-DLLVM_ENABLE_ASSERTIONS=ON",
             "-DGRPC_INSTALL_PATH=/usr/local/lib/grpc",
             "-DLLVM_OPTIMIZED_TABLEGEN=ON"
         ])},

    # Build in C++20 configuration.
    {'name': "clang-debian-cpp20",
     'tags': ["clang", "c++20"],
     'workernames': ["clang-debian-cpp20"],
     'builddir': "clang-debian-cpp20",
     'factory': UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
         clean=True,
         depends_on_projects=["llvm", "clang", "clang-tools-extra"],
         extra_configure_args=[
             "-DCMAKE_CXX_STANDARD=20",
             "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
             "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
             "-DCMAKE_BUILD_TYPE=Release",
             "-DLLVM_ENABLE_ASSERTIONS=ON",
             # FIXME: Re-enable after cleaning up LLVM.
             #        https://github.com/llvm/llvm-project/issues/60101
             "-DCMAKE_CXX_FLAGS=-Wno-deprecated-enum-enum-conversion -Wno-deprecated-declarations -Wno-deprecated-anon-enum-enum-conversion -Wno-ambiguous-reversed-operator",
         ])},

    # Target ARC from Synopsys
    {'name': "arc-builder",
     'tags': ["clang", "lld"],
     'workernames' : ["arc-worker"],
     'builddir': "arc-folder",
     'factory': UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
        depends_on_projects=["llvm", "clang", "lld"],
        extra_configure_args=[
             "-DCMAKE_EXPORT_COMPILE_COMMANDS:BOOL=ON",
             "-DLLVM_ENABLE_ASSERTIONS:BOOL=ON",
             "-DLLVM_TOOL_CLANG_TOOLS_EXTRA_BUILD=0",
             "-DLLVM_ENABLE_LIBPFM=OFF",
             "-DLLVM_TARGETS_TO_BUILD=X86",
             "-DLLVM_EXPERIMENTAL_TARGETS_TO_BUILD=ARC",
         ])},


    # BOLT builders managed by Meta
    {'name' : 'bolt-x86_64-ubuntu-nfc',
    'tags'  : ["bolt"],
    'collapseRequests': False,
    'workernames' : ['bolt-worker'],
    'builddir': "bolt-x86_64-ubuntu-nfc",
    'factory' : BOLTBuilder.getBOLTCmakeBuildFactory(
                    bolttests=True,
                    depends_on_projects=['bolt', 'llvm'],
                    extra_configure_args=[
                        "-DLLVM_APPEND_VC_REV=OFF",
                        "-DCMAKE_EXE_LINKER_FLAGS='-Wl,--build-id=none'"
                        "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                        "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
                        "-DLLVM_ENABLE_PROJECTS=clang;lld;bolt",
                        "-DLLVM_TARGETS_TO_BUILD=X86;AArch64;RISCV",
                        ],
                    is_nfc=True,
                    )},

    {'name': "bolt-x86_64-ubuntu-clang",
    'tags': ["bolt"],
    'workernames':["bolt-worker"],
    'builddir': "bolt-x86_64-ubuntu-clang",
    'factory' : BOLTBuilder.getBOLTCmakeBuildFactory(
                    bolttests=False,
                    clean=True,
                    depends_on_projects=['bolt', 'clang', 'lld', 'llvm'],
                    caches=[
                        'clang/cmake/caches/BOLT.cmake',
                        'clang/cmake/caches/BOLT-PGO.cmake',
                    ],
                    targets=['clang-bolt'],
                    checks=['stage2-clang-bolt'],
                    extra_configure_args=[
                        "-DCMAKE_C_COMPILER=gcc",
                        "-DCMAKE_CXX_COMPILER=g++",
                        "-DLLVM_APPEND_VC_REV=OFF",
                        "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                        "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
                        "-DLLVM_ENABLE_LLD=ON",
                        "-DBOOTSTRAP_LLVM_ENABLE_LLD=ON",
                        "-DBOOTSTRAP_BOOTSTRAP_LLVM_ENABLE_LLD=ON",
                        "-DPGO_INSTRUMENT_LTO=Thin",
                        ],
                    )},

    {'name': "bolt-x86_64-ubuntu-dylib",
    'tags': ["bolt"],
    'workernames':["bolt-worker"],
    'builddir': "bolt-x86_64-ubuntu-dylib",
    'factory' : BOLTBuilder.getBOLTCmakeBuildFactory(
                    bolttests=False,
                    depends_on_projects=['bolt', 'lld', 'llvm'],
                    extra_configure_args=[
                        "-DLLVM_APPEND_VC_REV=OFF",
                        "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                        "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
                        "-DLLVM_ENABLE_PROJECTS=bolt;clang;lld",
                        "-DLLVM_TARGETS_TO_BUILD=X86;AArch64;RISCV",
                        "-DLLVM_LINK_LLVM_DYLIB=ON",
                        "-DLLVM_ENABLE_LLD=ON",
                        ],
                    )},

    {'name': "bolt-x86_64-ubuntu-shared",
    'tags': ["bolt"],
    'workernames':["bolt-worker"],
    'builddir': "bolt-x86_64-ubuntu-shared",
    'factory' : BOLTBuilder.getBOLTCmakeBuildFactory(
                    bolttests=False,
                    depends_on_projects=['bolt', 'lld', 'llvm'],
                    extra_configure_args=[
                        "-DLLVM_APPEND_VC_REV=OFF",
                        "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                        "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
                        "-DLLVM_ENABLE_PROJECTS=bolt;clang;lld",
                        "-DLLVM_TARGETS_TO_BUILD=X86;AArch64;RISCV",
                        "-DBUILD_SHARED_LIBS=ON",
                        "-DLLVM_ENABLE_LLD=ON",
                        ],
                    )},

    {'name': "bolt-aarch64-ubuntu-clang-shared-meta",
    'tags': ["bolt"],
    'workernames':["bolt-worker-aarch64-meta"],
    'builddir': "bolt-aarch64-ubuntu-clang-shared-meta",
    'factory' : BOLTBuilder.getBOLTCmakeBuildFactory(
                    bolttests=True,
                    depends_on_projects=['bolt', 'lld', 'llvm'],
                    extra_configure_args=[
                        "-DCMAKE_C_COMPILER=clang",
                        "-DCMAKE_CXX_COMPILER=clang++",
                        "-DLLVM_APPEND_VC_REV=OFF",
                        "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                        "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
                        "-DLLVM_ENABLE_PROJECTS=bolt;clang;lld",
                        "-DLLVM_TARGETS_TO_BUILD=X86;AArch64;RISCV",
                        "-DBUILD_SHARED_LIBS=ON",
                        "-DLLVM_USE_LINKER=mold",
                        ],
                    )},

    # BOLT builders managed by Arm.
    {'name' : 'bolt-aarch64-ubuntu-nfc',
    'tags'  : ["bolt", "aarch64"],
    'collapseRequests': False,
    'workernames' : ['bolt-worker-aarch64'],
    'builddir': "bolt-aarch64-ubuntu-nfc",
    'factory' : BOLTBuilder.getBOLTCmakeBuildFactory(
                    bolttests=True,
                    depends_on_projects=['bolt', 'llvm'],
                    extra_configure_args=[
                        "-DLLVM_APPEND_VC_REV=OFF",
                        "-DCMAKE_EXE_LINKER_FLAGS='-Wl,--build-id=none'"
                        "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                        "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
                        "-DLLVM_ENABLE_PROJECTS=clang;lld;bolt",
                        "-DLLVM_TARGETS_TO_BUILD=X86;AArch64;RISCV",
                        ],
                    is_nfc=True,
                    )},

    {'name': "bolt-aarch64-ubuntu-clang",
    'tags' : ["bolt", "aarch64"],
    'workernames':["bolt-worker-aarch64"],
    'builddir': "bolt-aarch64-ubuntu-clang",
    'factory' : BOLTBuilder.getBOLTCmakeBuildFactory(
                    bolttests=False,
                    clean=True,
                    depends_on_projects=['bolt', 'clang', 'lld', 'llvm'],
                    caches=[
                        'clang/cmake/caches/BOLT.cmake',
                        'clang/cmake/caches/BOLT-PGO.cmake',
                    ],
                    targets=['clang-bolt'],
                    checks=['stage2-clang-bolt'],
                    extra_configure_args=[
                        "-DCMAKE_C_COMPILER=gcc",
                        "-DCMAKE_CXX_COMPILER=g++",
                        "-DLLVM_APPEND_VC_REV=OFF",
                        "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                        "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
                        "-DLLVM_ENABLE_LLD=ON",
                        "-DBOOTSTRAP_LLVM_ENABLE_LLD=ON",
                        "-DBOOTSTRAP_BOOTSTRAP_LLVM_ENABLE_LLD=ON",
                        "-DPGO_INSTRUMENT_LTO=Thin",
                        ],
                    )},

    {'name': "bolt-aarch64-ubuntu-dylib",
    'tags' : ["bolt", "aarch64"],
    'workernames':["bolt-worker-aarch64"],
    'builddir': "bolt-aarch64-ubuntu-dylib",
    'factory' : BOLTBuilder.getBOLTCmakeBuildFactory(
                    bolttests=False,
                    depends_on_projects=['bolt', 'lld', 'llvm'],
                    extra_configure_args=[
                        "-DLLVM_APPEND_VC_REV=OFF",
                        "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                        "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
                        "-DLLVM_ENABLE_PROJECTS=bolt;clang;lld",
                        "-DLLVM_TARGETS_TO_BUILD=X86;AArch64;RISCV",
                        "-DLLVM_LINK_LLVM_DYLIB=ON",
                        "-DLLVM_ENABLE_LLD=ON",
                        ],
                    )},

    {'name': "bolt-aarch64-ubuntu-shared",
    'tags'  : ["bolt", "aarch64"],
    'workernames':["bolt-worker-aarch64"],
    'builddir': "bolt-aarch64-ubuntu-shared",
    'factory' : BOLTBuilder.getBOLTCmakeBuildFactory(
                    bolttests=False,
                    depends_on_projects=['bolt', 'lld', 'llvm'],
                    extra_configure_args=[
                        "-DLLVM_APPEND_VC_REV=OFF",
                        "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                        "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
                        "-DLLVM_ENABLE_PROJECTS=bolt;clang;lld",
                        "-DLLVM_TARGETS_TO_BUILD=X86;AArch64;RISCV",
                        "-DBUILD_SHARED_LIBS=ON",
                        "-DLLVM_ENABLE_LLD=ON",
                        ],
                    )},

    # AMD ROCm support.
    {'name' : 'mlir-rocm-mi200',
     'tags'  : ["mlir"],
     'workernames' : ['mi200-buildbot'],
     'builddir': 'mlir-rocm-mi200',
     'factory' : UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
         clean=True,
         depends_on_projects=['llvm', 'mlir'],
         targets = ['check-mlir-build-only'],
         checks = ['check-mlir'],
         install_pip_requirements=True,
         extra_configure_args= mlir_default_cmake_options + [
             '-DLLVM_CCACHE_BUILD=ON',
             '-DLLVM_ENABLE_ASSERTIONS=ON',
             '-DLLVM_ENABLE_LLD=ON',
             '-DMLIR_ENABLE_ROCM_RUNNER=ON',
             '-DMLIR_ENABLE_ROCM_CONVERSIONS=ON',
             '-DMLIR_INCLUDE_INTEGRATION_TESTS=ON',
         ],
         env={
             'CC': 'clang',
             'CXX': 'clang++',
             'LD': 'lld',
         })},

    # Standalone builder
    {'name' : "standalone-build-x86_64",
    'tags'  : ["clang"],
    'workernames':["standalone-build-x86_64"],
    'builddir':"standalone-build-x86_64",
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    script="standalone-build.sh",
                    checkout_llvm_sources=False,
                    script_interpreter=None)},

    ## CSKY check-all + test-suite in soft-float
    {'name' : "clang-csky-soft",
    'tags'  : ["clang"],
    'workernames' : ["thead-clang-csky"],
    'builddir':"clang-csky-softfp",
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                clean=False,
                checkout_clang_tools_extra=False,
                checkout_compiler_rt=False,
                checkout_lld=False,
                testStage1=True,
                useTwoStage=False,
                stage1_config='Release',
                runTestSuite=True,
                testsuite_flags=[
                    '--cflags', '-mcpu=c860 -latomic -DSMALL_PROBLEM_SIZE',
                    '--cppflags', '-mcpu=c860 -latomic -DSMALL_PROBLEM_SIZE',
                    '--run-under=/mnt/qemu/bin/qemu-cskyv2 -cpu c860 -csky-extend denormal=on -L /mnt/gcc-csky/csky-linux-gnuabiv2/libc/ck860 -E LD_LIBRARY_PATH=/mnt/gcc-csky/csky-linux-gnuabiv2/lib/ck860',
                    '--cmake-define=SMALL_PROBLEM_SIZE=On',
                    '--cmake-define=TEST_SUITE_USER_MODE_EMULATION=True',
                    '--threads=32', '--build-threads=32'],
                extra_cmake_args=[
                    "-DLLVM_EXPERIMENTAL_TARGETS_TO_BUILD='CSKY'",
                    "-DLLVM_DEFAULT_TARGET_TRIPLE='csky-unknown-linux'",
                    "-DGCC_INSTALL_PREFIX=/mnt/gcc-csky/"])},

    ## CSKY check-all + test-suite in hard-float
    {'name' : "clang-csky-hardfp",
    'tags'  : ["clang"],
    'workernames' : ["thead-clang-csky"],
    'builddir':"clang-csky-hardfp",
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                clean=False,
                checkout_clang_tools_extra=False,
                checkout_compiler_rt=False,
                checkout_lld=False,
                testStage1=True,
                useTwoStage=False,
                stage1_config='Release',
                runTestSuite=True,
                testsuite_flags=[
                    '--cflags', '-mcpu=c860 -latomic -mhard-float -DSMALL_PROBLEM_SIZE',
                    '--cppflags', '-mcpu=c860 -latomic -mhard-float -DSMALL_PROBLEM_SIZE',
                    '--run-under=/mnt/qemu/bin/qemu-cskyv2 -cpu c860 -csky-extend denormal=on -L /mnt/gcc-csky/csky-linux-gnuabiv2/libc/ck860/hard-fp -E LD_LIBRARY_PATH=/mnt/gcc-csky/csky-linux-gnuabiv2/lib/ck860/hard-fp',
                    '--cmake-define=SMALL_PROBLEM_SIZE=On',
                    '--cmake-define=TEST_SUITE_USER_MODE_EMULATION=True',
                    '--threads=32', '--build-threads=32'],
                extra_cmake_args=[
                    "-DLLVM_EXPERIMENTAL_TARGETS_TO_BUILD='CSKY'",
                    "-DLLVM_DEFAULT_TARGET_TRIPLE='csky-unknown-linux'",
                    "-DGCC_INSTALL_PREFIX=/mnt/gcc-csky/"])},

    # NVPTX builders
    {'name' : "llvm-nvptx-nvidia-ubuntu",
    'tags'  : ["llvm", "nvptx"],
    'collapseRequests': False,
    'workernames' : ["as-builder-7"],
    'builddir': "llvm-nvptx-nvidia-ubuntu",
    'factory' : UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    depends_on_projects=["llvm"],
                    clean=True,
                    checks=["check-llvm"],
                    extra_configure_args=[
                        "-DLLVM_CCACHE_BUILD=ON",
                        "-DLLVM_TARGETS_TO_BUILD=X86;NVPTX",
                        "-DLLVM_DEFAULT_TARGET_TRIPLE=nvptx-nvidia-cuda",
                        "-DLLVM_ENABLE_ASSERTIONS=ON",
                        "-DLLVM_LIT_ARGS=-vv",
                        "-DLLVM_USE_LINKER=gold",
                        "-DBUILD_SHARED_LIBS=ON",
                        "-DLLVM_OPTIMIZED_TABLEGEN=ON"],
                    env={
                        'CCACHE_DIR' : util.Interpolate("%(prop:builddir)s/ccache-db"),
                        # TMP/TEMP within the build dir (to utilize a ramdisk).
                        'TMP'        : util.Interpolate("%(prop:builddir)s/build"),
                        'TEMP'       : util.Interpolate("%(prop:builddir)s/build"),
                        # Allow Lit to use 'ptxas' tool to validate generated PTX.
                        'LLVM_PTXAS_EXECUTABLE' : "/usr/local/cuda/bin/ptxas",
                    })},

    {'name' : "llvm-nvptx64-nvidia-ubuntu",
    'tags'  : ["llvm", "nvptx"],
    'collapseRequests': False,
    'workernames' : ["as-builder-7"],
    'builddir': "llvm-nvptx64-nvidia-ubuntu",
    'factory' : UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    depends_on_projects=["llvm"],
                    clean=True,
                    checks=["check-llvm"],
                    extra_configure_args=[
                        "-DLLVM_CCACHE_BUILD=ON",
                        "-DLLVM_TARGETS_TO_BUILD=X86;NVPTX",
                        "-DLLVM_DEFAULT_TARGET_TRIPLE=nvptx64-nvidia-cuda",
                        "-DLLVM_ENABLE_ASSERTIONS=ON",
                        "-DLLVM_LIT_ARGS=-vv",
                        "-DLLVM_USE_LINKER=gold",
                        "-DBUILD_SHARED_LIBS=ON",
                        "-DLLVM_OPTIMIZED_TABLEGEN=ON"],
                    env={
                        'CCACHE_DIR' : util.Interpolate("%(prop:builddir)s/ccache-db"),
                        # TMP/TEMP within the build dir (to utilize a ramdisk).
                        'TMP'        : util.Interpolate("%(prop:builddir)s/build"),
                        'TEMP'       : util.Interpolate("%(prop:builddir)s/build"),
                        # Allow Lit to use 'ptxas' tool to validate generated PTX.
                        'LLVM_PTXAS_EXECUTABLE' : "/usr/local/cuda/bin/ptxas",
                    })},

    {'name' : "llvm-nvptx-nvidia-win",
    'tags'  : ["llvm", "nvptx"],
    'workernames' : ["as-builder-8"],
    'builddir': "llvm-nvptx-nvidia-win",
    'factory' : UnifiedTreeBuilder.getCmakeWithNinjaWithMSVCBuildFactory(
                    vs="autodetect",
                    depends_on_projects=["llvm"],
                    clean=True,
                    checks=["check-llvm"],
                    extra_configure_args=[
                        "-DLLVM_CCACHE_BUILD=ON",
                        "-DLLVM_TARGETS_TO_BUILD=X86;NVPTX",
                        "-DLLVM_DEFAULT_TARGET_TRIPLE=nvptx-nvidia-cuda",
                        "-DLLVM_ENABLE_ASSERTIONS=ON",
                        "-DLLVM_LIT_ARGS=-vv",
                        "-DLLVM_OPTIMIZED_TABLEGEN=ON"],
                    env={
                        'CCACHE_DIR' : util.Interpolate("%(prop:builddir)s/ccache-db"),
                        # TMP/TEMP within the build dir (to utilize a ramdisk).
                        'TMP'        : util.Interpolate("%(prop:builddir)s/build"),
                        'TEMP'       : util.Interpolate("%(prop:builddir)s/build"),
                        # Allow Lit to use 'ptxas' tool to validate generated PTX.
                        'LLVM_PTXAS_EXECUTABLE' : "c:/buildbot/latest-cuda/bin/ptxas.exe",
                    })},

    {'name' : "llvm-nvptx64-nvidia-win",
    'tags'  : ["llvm", "nvptx"],
    'workernames' : ["as-builder-8"],
    'builddir': "llvm-nvptx64-nvidia-win",
    'factory' : UnifiedTreeBuilder.getCmakeWithNinjaWithMSVCBuildFactory(
                    vs="autodetect",
                    depends_on_projects=["llvm"],
                    clean=True,
                    checks=["check-llvm"],
                    extra_configure_args=[
                        "-DLLVM_CCACHE_BUILD=ON",
                        "-DLLVM_TARGETS_TO_BUILD=X86;NVPTX",
                        "-DLLVM_DEFAULT_TARGET_TRIPLE=nvptx64-nvidia-cuda",
                        "-DLLVM_ENABLE_ASSERTIONS=ON",
                        "-DLLVM_LIT_ARGS=-vv",
                        "-DLLVM_OPTIMIZED_TABLEGEN=ON"],
                    env={
                        'CCACHE_DIR' : util.Interpolate("%(prop:builddir)s/ccache-db"),
                        # TMP/TEMP within the build dir (to utilize a ramdisk).
                        'TMP'        : util.Interpolate("%(prop:builddir)s/build"),
                        'TEMP'       : util.Interpolate("%(prop:builddir)s/build"),
                        # Allow Lit to use 'ptxas' tool to validate generated PTX.
                        'LLVM_PTXAS_EXECUTABLE' : "c:/buildbot/latest-cuda/bin/ptxas.exe",
                    })},

    # flang FortranRuntime CUDA Offload builders.
    {'name' : "flang-runtime-cuda-gcc",
    'tags'  : ["flang", "runtime"],
    'workernames' : ["as-builder-7"],
    'builddir': "flang-runtime-cuda-gcc",
    'factory' : UnifiedTreeBuilder.getCmakeExBuildFactory(
                    depends_on_projects = ["llvm", "clang", "mlir", "flang"],
                    enable_runtimes = ["flang-rt", "openmp"],
                    clean = True,
                    checks = [],
                    targets = ["flang-rt"],
                    cmake_definitions = {
                        "CMAKE_BUILD_TYPE"              : "Release",
                        "CMAKE_EXPORT_COMPILE_COMMANDS" : "ON",
                        "LLVM_ENABLE_ASSERTIONS"        : "ON",
                        "BUILD_SHARED_LIBS"             : "OFF",
                        "FLANG_RT_EXPERIMENTAL_OFFLOAD_SUPPORT" : "CUDA",
                        "FLANG_PARALLEL_COMPILE_JOBS"   : 12,
                        "CMAKE_CUDA_COMPILER"           : "/usr/local/cuda/bin/nvcc",
                        "CMAKE_CXX_COMPILER"            : "/usr/bin/g++",
                        "CMAKE_C_COMPILER"              : "/usr/bin/gcc",
                        "CMAKE_CUDA_HOST_COMPILER"      : "/usr/bin/g++",
                        "CMAKE_CUDA_ARCHITECTURES"      : "80",
                        "CMAKE_CUDA_FLAGS"              : "-G -g",
                        "CMAKE_CUDA_COMPILER_LAUNCHER"  : "ccache",
                        "CMAKE_CXX_COMPILER_LAUNCHER"   : "ccache",
                        "CMAKE_C_COMPILER_LAUNCHER"     : "ccache",
                        "FLANG_RT_LIBCUDACXX_PATH"      : util.Interpolate("%(prop:nv_cccl_root_path)s/libcudacxx"),
                    },
                    jobs = 64,
                    env = {
                        'CCACHE_DIR' : util.Interpolate("%(prop:builddir)s/ccache-db"),
                        # TMP/TEMP within the build dir (to utilize a ramdisk).
                        'TMP'        : util.Interpolate("%(prop:builddir)s/build"),
                        'TEMP'       : util.Interpolate("%(prop:builddir)s/build"),
                    })},

    {'name' : "flang-runtime-cuda-clang",
    'tags'  : ["flang", "runtime"],
    'workernames' : ["as-builder-7"],
    'builddir': "flang-runtime-cuda-clang",
    'factory' : UnifiedTreeBuilder.getCmakeExBuildFactory(
                    depends_on_projects = ["llvm", "clang", "lld", "flang"],
                    enable_runtimes = ["flang-rt", "openmp"],
                    clean = True,
                    checks = [],
                    cmake_definitions = {
                        "CMAKE_BUILD_TYPE"              : "Release",
                        "CMAKE_EXPORT_COMPILE_COMMANDS" : "ON",
                        "LLVM_CCACHE_BUILD"             : "ON",
                        "LLVM_ENABLE_ASSERTIONS"        : "ON",
                        "LLVM_TARGETS_TO_BUILD"         : "Native",
                        "CLANG_DEFAULT_LINKER"          : "lld",

                        "FLANG_RT_EXPERIMENTAL_OFFLOAD_SUPPORT" : "OpenMP",
                        "FLANG_RT_DEVICE_ARCHITECTURES" : "sm_50;sm_60;sm_70;sm_80",
                        "FLANG_PARALLEL_COMPILE_JOBS"   : 12,
                        "FLANG_RT_INCLUDE_CUF"          : "OFF",
                        "FLANG_RT_INCLUDE_TESTS"        : "OFF",
                    },
                    env = {
                        'CCACHE_DIR' : util.Interpolate("%(prop:builddir)s/ccache-db"),
                        # TMP/TEMP within the build dir (to utilize a ramdisk).
                        'TMP'        : util.Interpolate("%(prop:builddir)s/build"),
                        'TEMP'       : util.Interpolate("%(prop:builddir)s/build"),
                    })},

    ## RISC-V RV64GC check-all running under qemu-user.
    {'name' : "clang-rv64gc-qemu-user-single-stage",
    'tags'  : ["llvm", "clang"],
    'workernames' : ["rv64gc-qemu-user"],
    'builddir': "clang-rv64gc",
    'factory' : UnifiedTreeBuilder.getCmakeWithNinjaBuildFactory(
                    depends_on_projects=["llvm", "clang", "clang-tools-extra", "lld"],
                    checks=['check-all'],
                    extra_configure_args=[
                        "-DCMAKE_BUILD_TYPE=Release",
                        "-DLLVM_ENABLE_ASSERTIONS=ON",
                        "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                        "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache",
                        "-DLLVM_TARGETS_TO_BUILD=all"],
                    env={
                        'CC':'clang',
                        'CXX': 'clang++',
                    })},

    ## RISC-V RVA20 profile check-all 2-stage. The second stage is
    # cross-compiled on the x86 host and then lit runs under a qemu-system image
    # using the just-built artifacts.
    {'name' : "clang-riscv-rva20-2stage",
    'tags'  : ["clang"],
    'workernames' : ["rise-clang-riscv-rva20-2stage"],
    'builddir':"clang-riscv-rva20-2stage",
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    script="rise-riscv-build.sh",
                    checkout_llvm_sources=False,
                    script_interpreter=None,
                    clean=True)},

    ## RISC-V RVA23 profile check-all 2-stage
    {'name' : "clang-riscv-rva23-2stage",
    'workernames' : ["rise-clang-riscv-rva23-2stage"],
    'builddir':"clang-riscv-rva23-2stage",
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                clean=True,
                useTwoStage=True,
                runTestSuite=False,
                testStage1=False,
                extra_cmake_args=[
                    "-DCMAKE_C_COMPILER=clang",
                    "-DCMAKE_CXX_COMPILER=clang++",
                    "-DLLVM_ENABLE_LLD=True",
                    "-DLLVM_TARGETS_TO_BUILD=RISCV",
                    "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                    "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache"],
                extra_stage2_cmake_args=[
                    "-DLLVM_ENABLE_LLD=True",
                    "-DCOMPILER_RT_BUILD_SANITIZERS=OFF",
                    "-DCMAKE_C_FLAGS='-menable-experimental-extensions -march=rva23u64'",
                    "-DCMAKE_CXX_FLAGS='-menable-experimental-extensions -march=rva23u64'"]
                )},

    ## RISC-V RVA23 profile with -mrvv-vector-bits=zvl check-all 2-stage
    {'name' : "clang-riscv-rva23-mrvv-vec-bits-2stage",
    'workernames' : ["rise-clang-riscv-rva23-mrvv-vec-bits-2stage"],
    'builddir':"clang-riscv-rva23-mrvv-vec-bits-2stage",
    'factory' : ClangBuilder.getClangCMakeBuildFactory(
                clean=False,
                useTwoStage=True,
                runTestSuite=False,
                testStage1=False,
                extra_cmake_args=[
                    "-DCMAKE_C_COMPILER=clang",
                    "-DCMAKE_CXX_COMPILER=clang++",
                    "-DLLVM_ENABLE_LLD=True",
                    "-DLLVM_TARGETS_TO_BUILD=RISCV",
                    "-DCMAKE_C_COMPILER_LAUNCHER=ccache",
                    "-DCMAKE_CXX_COMPILER_LAUNCHER=ccache"],
                extra_stage2_cmake_args=[
                    "-DLLVM_ENABLE_LLD=True",
                    "-DCMAKE_C_FLAGS='-menable-experimental-extensions -march=rva23u64 -mrvv-vector-bits=zvl'",
                    "-DCMAKE_CXX_FLAGS='-menable-experimental-extensions -march=rva23u64 -mrvv-vector-bits=zvl'"]
                )},

    ## RISC-V RVA23 profile with EVL vectorizer check-all 2-stage
    ## (cross-compile and then test under qemu-system).
    {'name' : "clang-riscv-rva23-evl-vec-2stage",
    'workernames' : ["rise-clang-riscv-rva23-evl-vec-2stage"],
    'builddir':"clang-riscv-rva23-evl-vec-2stage",
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    script="rise-riscv-build.sh",
                    checkout_llvm_sources=False,
                    script_interpreter=None,
                    clean=True)},

    ## Simple single-stage build of clang, then cross-building and running the
    ## llvm-test-suite under qemu-user for a number of configurations. If
    ## there is a failure, do a check-all of the native (x86_64) LLVM, to provide
    ## an indicator as to whether the problem is likely RISC-V specific or not.
    {'name' : "clang-riscv-gauntlet",
    'workernames' : ["rise-worker-1"],
    'builddir':"clang-riscv-gauntlet",
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    script="rise-riscv-gauntlet-build.sh",
                    checkout_llvm_sources=False,
                    script_interpreter=None,
                    clean=True)},

    ## RISC-V RVA23 profile with zvl512b check-all 2-stage
    ## (cross-compile and then test under qemu-system).
    {'name' : "clang-riscv-rva23-zvl512b-2stage",
    'workernames' : ["rise-worker-2"],
    'builddir':"clang-riscv-rva23-zvl512b-2stage",
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    script="rise-riscv-build.sh",
                    checkout_llvm_sources=False,
                    script_interpreter=None,
                    clean=True)},

    ## RISC-V RVA23 profile with zvl1024b check-all 2-stage
    ## (cross-compile and then test under qemu-system).
    {'name' : "clang-riscv-rva23-zvl1024b-2stage",
    'workernames' : ["rise-worker-3"],
    'builddir':"clang-riscv-rva23-zvl1024b-2stage",
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    script="rise-riscv-build.sh",
                    checkout_llvm_sources=False,
                    script_interpreter=None,
                    clean=True)},

    ## RISC-V -mcpu=spacemit-x60 with -mrvv-vector-bits=zvl check-all 2-stage
    ## (cross-compile and then test under qemu-system).
    {'name' : "clang-riscv-x60-mrvv-vec-bits-2stage",
    'workernames' : ["rise-worker-4"],
    'builddir':"clang-riscv-x60-mrvv-vec-bits-2stage",
    'factory' : AnnotatedBuilder.getAnnotatedBuildFactory(
                    script="rise-riscv-build.sh",
                    checkout_llvm_sources=False,
                    script_interpreter=None,
                    clean=True)},

]

# LLDB remote-linux builder env variables.
# Currently identical for Linux and Windows build hosts.
lldb_remote_linux_env = {
    'CCACHE_DIR' : util.Interpolate("%(prop:builddir)s/ccache-db"),
    # TMP/TEMP within the build dir (to utilize a ramdisk).
    'TMP'        : util.Interpolate("%(prop:builddir)s/build"),
    'TEMP'       : util.Interpolate("%(prop:builddir)s/build"),
}

all += [
    # LLDB remote-linux builders.

    # LLDB remote-linux on Ubuntu Linux host.
    # The first stage uses pre-installed latest released Clang (see apt.llvm.org for details).
    # The second stage uses pre-built cross Aarch64 Clang toolchain from the latest release branch
    # (see llvm-clang-win-x-aarch64 builder configuration for the details).
    # The remote host is ARM Cortex A76/A78 board with Ubuntu Linux.
    {'name': "lldb-remote-linux-ubuntu",
    'tags'  : ["llvm", "clang", "lldb", "cross", "aarch64"],
    'workernames': ["as-builder-9"],
    'builddir': "lldb-remote-linux-ubuntu",
    'factory': UnifiedTreeBuilder.getCmakeExBuildFactory(
                    depends_on_projects = ["llvm", "clang", "lld", "lldb"],
                    enable_runtimes = None,
                    checks = [
                        "check-lldb-unit",
                        "check-lldb-api",
                        "check-lldb-shell",
                    ],
                    clean = True,
                    cmake_definitions = {
                        "CMAKE_BUILD_TYPE"              : "Release",
                        "CMAKE_C_COMPILER_LAUNCHER"     : "ccache",
                        "CMAKE_CXX_COMPILER_LAUNCHER"   : "ccache",
                        "CMAKE_CXX_FLAGS"               : "-D__OPTIMIZE__",
                        "LLVM_TARGETS_TO_BUILD"         : "AArch64",
                        #Note: needs for some LLDB tests.
                        "LLVM_TARGET_TRIPLE"            : "aarch64-unknown-linux-gnu",
                        "LLVM_INCLUDE_BENCHMARKS"       : "OFF",
                        "LLVM_PARALLEL_LINK_JOBS"       : 8,
                        "CLANG_DEFAULT_LINKER"          : "lld",
                        "LLVM_LIT_ARGS"                 : "-v -vv --threads=8 --time-tests",

                        "TOOLCHAIN_TARGET_TRIPLE"       : "aarch64-unknown-linux-gnu",
                        "TOOLCHAIN_TARGET_COMPILER_FLAGS"   :  "-mcpu=cortex-a78",
                        "TOOLCHAIN_TARGET_SYSROOTFS"    : util.Interpolate("%(prop:sysroot_path_aarch64)s"),
                        "LIBCXX_ABI_VERSION"            : "1",
                        "LLVM_INSTALL_TOOLCHAIN_ONLY"   : "OFF",

                        "LLDB_TEST_ARCH"                : "aarch64",
                        "LLDB_TEST_COMPILER"            : util.Interpolate("%(prop:builddir)s/build/bin/clang"),
                        "LLDB_TEST_PLATFORM_URL"        : util.Interpolate("connect://%(prop:remote_test_host)s:1234"),
                        "LLDB_TEST_PLATFORM_WORKING_DIR": "/home/ubuntu/lldb-tests",
                        "LLDB_TEST_SYSROOT"             : util.Interpolate("%(prop:sysroot_path_aarch64)s"),
                        "LLDB_ENABLE_PYTHON"            : "ON",
                        "LLDB_ENABLE_SWIG"              : "ON",
                        "LLDB_ENABLE_LIBEDIT"           : "OFF",
                        "LLDB_ENABLE_CURSES"            : "OFF",
                        "LLDB_ENABLE_LZMA"              : "OFF",
                        "LLDB_ENABLE_LIBXML2"           : "OFF",
                        # No need to build lldb-server during the first stage.
                        # We are going to build it for the target platform later.
                        "LLDB_CAN_USE_LLDB_SERVER"      : "OFF",
                        "LLDB_TEST_USER_ARGS"           : util.Interpolate(
                                                            "--env;ARCH_CFLAGS=-mcpu=cortex-a78;" \
                                                            "--platform-name;remote-linux;" \
                                                            "--skip-category=lldb-server"),
                    },
                    cmake_options = [
                        "-C", util.Interpolate("%(prop:srcdir_relative)s/clang/cmake/caches/CrossWinToARMLinux.cmake"),
                    ],
                    install_dir = "native",
                    post_build_steps =
                        # Stage 2.
                        # Build the target's lldb-server (cross compilation with pre-installed/pre-built aarch64 clang).
                        UnifiedTreeBuilder.getCmakeExBuildFactory(
                            depends_on_projects = ["clang", "lldb"],
                            enable_runtimes = None,
                            checks = None,
                            clean = True,
                            repo_profiles = None,
                            allow_cmake_defaults = False,
                            hint = "aarch64-lldb",
                            cmake_definitions = {
                                "CMAKE_BUILD_TYPE"              : "Release",
                                "CMAKE_C_COMPILER_LAUNCHER"     : "ccache",
                                "CMAKE_CXX_COMPILER_LAUNCHER"   : "ccache",
                                "CMAKE_CXX_FLAGS"               : "-mcpu=cortex-a78 -D__OPTIMIZE__ -fPIC --stdlib=libc++",
                                "CMAKE_C_FLAGS"                 : "-mcpu=cortex-a78 -D__OPTIMIZE__ -fPIC",
                                "CMAKE_EXE_LINKER_FLAGS"        : "-Wl,-l:libc++abi.a -Wl,-l:libc++.a -Wl,-l:libunwind.a",
                                "CMAKE_SHARED_LINKER_FLAGS"     : "-Wl,-l:libc++abi.a -Wl,-l:libc++.a -Wl,-l:libunwind.a",
                                "CMAKE_CXX_COMPILER"            : util.Interpolate("%(prop:builddir)s/build/bin/clang++"),
                                "CMAKE_C_COMPILER"              : util.Interpolate("%(prop:builddir)s/build/bin/clang"),
                                "CMAKE_ASM_COMPILER"            : util.Interpolate("%(prop:builddir)s/build/bin/clang"),
                                "CMAKE_SYSTEM_NAME"             : "Linux",
                                "CMAKE_SYSTEM_PROCESSOR"        : "aarch64",
                                "CMAKE_CROSSCOMPILING"          : "ON",

                                # Required for the native table-gen
                                "LLVM_NATIVE_TOOL_DIR"          : util.Interpolate("%(prop:builddir)s/build/bin"),

                                "LLVM_DEFAULT_TARGET_TRIPLE"    : "aarch64-unknown-linux-gnu",
                                "LLVM_HOST_TRIPLE"              : "aarch64-unknown-linux-gnu",
                                "LLVM_TARGETS_TO_BUILD"         : "AArch64",
                                "LLVM_ENABLE_ASSERTIONS"        : "ON",
                                "LLVM_INCLUDE_BENCHMARKS"       : "OFF",
                                "LLVM_PARALLEL_LINK_JOBS"       : 8,
                                "CLANG_DEFAULT_LINKER"          : "lld",

                                "LLDB_INCLUDE_TESTS"            : "OFF",
                                "LLDB_ENABLE_PYTHON"            : "OFF",
                                "LLDB_ENABLE_LIBEDIT"           : "OFF",
                                "LLDB_ENABLE_CURSES"            : "OFF",
                                "LLDB_ENABLE_LZMA"              : "OFF",

                                "LLVM_ENABLE_ZLIB"              : "OFF",
                            },
                            obj_dir = "build-lldb-server",
                            targets = ["lldb-server"],
                            install_dir = util.Interpolate("%(prop:builddir)s/lldb-server-install"),
                            install_targets = ["install-lldb-server"],
                            post_finalize_steps = [
                                steps.ShellSequence(name = "exec-lldb-server",
                                    commands = [
                                        util.ShellArg(command=[ "ssh", util.Interpolate("%(prop:remote_test_user)s@%(prop:remote_test_host)s"), "killall lldb-server ; exit 0;" ], logname="stdio"),
                                        util.ShellArg(command=[ "scp", "lldb-server", util.Interpolate("%(prop:remote_test_user)s@%(prop:remote_test_host)s:~/lldb-server") ], logname="stdio"),
                                        util.ShellArg(command=[ "ssh", util.Interpolate("%(prop:remote_test_user)s@%(prop:remote_test_host)s"), "chmod +x ~/lldb-server" ], logname="stdio"),
                                        util.ShellArg(command=[ "ssh", util.Interpolate("%(prop:remote_test_user)s@%(prop:remote_test_host)s"),
                                                                    "~/lldb-server p --listen '*:1234' --server > /dev/null 2>&1 &" ], logname="stdio"),
                                    ],
                                    workdir = util.Interpolate("%(prop:builddir)s/lldb-server-install/bin"),
                                    description = "execute lldb-server on remote target",
                                    haltOnFailure = True,
                                ),
                            ],
                            env = lldb_remote_linux_env.copy(),
                        ), # ]] post_build_steps
                    env = lldb_remote_linux_env.copy(),
                )
        },

    # LLDB remote-linux on Windows host.
    # The first stage builds the latest cross Aarch64 toolchain.
    # The second stage uses just-built cross Aarch64 Clang toolchain
    # (see llvm-clang-win-x-aarch64 builder configuration for the details).
    # The remote host is ARM Cortex A76/A78 board with Ubuntu Linux.
    {'name': "lldb-remote-linux-win",
    'tags'  : ["llvm", "clang", "lldb", "cross", "aarch64"],
    'workernames': ["as-builder-10"],
    'builddir': "lldb-x-aarch64",
    'factory': UnifiedTreeBuilder.getCmakeExBuildFactory(
                    depends_on_projects = ["llvm", "clang", "lld", "lldb"],
                    enable_runtimes = None,
                    checks = [
                        "check-lldb-unit",
                        "check-lldb-api",
                        "check-lldb-shell",
                    ],
                    vs = "autodetect",
                    clean = True,
                    cmake_definitions = {
                        "CMAKE_BUILD_TYPE"              : "Release",
                        "CMAKE_C_COMPILER_LAUNCHER"     : "ccache",
                        "CMAKE_CXX_COMPILER_LAUNCHER"   : "ccache",
                        "CMAKE_CXX_FLAGS"               : "-D__OPTIMIZE__",
                        "LLVM_TARGETS_TO_BUILD"         : "AArch64",
                        #Note: needs for some LLDB tests.
                        "LLVM_TARGET_TRIPLE"            : "aarch64-unknown-linux-gnu",
                        "LLVM_INCLUDE_BENCHMARKS"       : "OFF",
                        "LLVM_PARALLEL_LINK_JOBS"       : 8,
                        "LLVM_LIT_ARGS"                 : "-v -vv --threads=8 --time-tests",

                        "TOOLCHAIN_TARGET_TRIPLE"       : "aarch64-unknown-linux-gnu",
                        "TOOLCHAIN_TARGET_COMPILER_FLAGS"   :  "-mcpu=cortex-a78",
                        "TOOLCHAIN_TARGET_SYSROOTFS:PATH"   : util.Interpolate("%(prop:sysroot_path_aarch64)s"),
                        "LIBCXX_ABI_VERSION"            : "1",
                        "LLVM_INSTALL_TOOLCHAIN_ONLY"   : "OFF",

                        "LLDB_TEST_ARCH"                : "aarch64",
                        "LLDB_TEST_PLATFORM_URL"        : util.Interpolate("connect://%(prop:remote_test_host)s:1234"),
                        "LLDB_TEST_PLATFORM_WORKING_DIR": "/home/ubuntu/lldb-tests",
                        "LLDB_TEST_SYSROOT:PATH"        : util.Interpolate("%(prop:sysroot_path_aarch64)s"),
                        "LLDB_ENABLE_PYTHON"            : "ON",
                        "LLDB_ENABLE_SWIG"              : "ON",
                        "LLDB_ENABLE_LIBEDIT"           : "OFF",
                        "LLDB_ENABLE_CURSES"            : "OFF",
                        "LLDB_ENABLE_LZMA"              : "OFF",
                        "LLDB_ENABLE_LIBXML2"           : "OFF",
                        # No need to build lldb-server during the first stage.
                        # We are going to build it for the target platform later.
                        "LLDB_CAN_USE_LLDB_SERVER"      : "OFF",
                        "LLDB_TEST_USER_ARGS"           : util.Interpolate(
                                                            "--env;ARCH_CFLAGS=-mcpu=cortex-a78;" \
                                                            "--platform-name;remote-linux;" \
                                                            "--skip-category=lldb-server"),
                    },
                    cmake_options = [
                        "-C", util.Interpolate("%(prop:srcdir_relative)s/clang/cmake/caches/CrossWinToARMLinux.cmake"),
                    ],
                    install_dir = "native",
                    post_build_steps =
                        # Stage 2.
                        # Build the target's lldb-server (cross compilation with pre-installed/pre-built aarch64 clang).
                        UnifiedTreeBuilder.getCmakeExBuildFactory(
                            depends_on_projects = ["clang", "lldb"],
                            enable_runtimes = None,
                            checks = None,
                            clean = True,
                            repo_profiles = None,
                            allow_cmake_defaults = False,
                            hint = "aarch64-lldb",
                            cmake_definitions = {
                                "CMAKE_BUILD_TYPE"              : "Release",
                                "CMAKE_C_COMPILER_LAUNCHER"     : "ccache",
                                "CMAKE_CXX_COMPILER_LAUNCHER"   : "ccache",
                                "CMAKE_CXX_FLAGS"               : "-mcpu=cortex-a78 -D__OPTIMIZE__ -fPIC --stdlib=libc++",
                                "CMAKE_C_FLAGS"                 : "-mcpu=cortex-a78 -D__OPTIMIZE__ -fPIC",
                                "CMAKE_EXE_LINKER_FLAGS"        : "-Wl,-l:libc++abi.a -Wl,-l:libc++.a -Wl,-l:libunwind.a",
                                "CMAKE_SHARED_LINKER_FLAGS"     : "-Wl,-l:libc++abi.a -Wl,-l:libc++.a -Wl,-l:libunwind.a",
                                "CMAKE_CXX_COMPILER:PATH"       : util.Interpolate("%(prop:builddir)s/build/bin/clang++.exe"),
                                "CMAKE_C_COMPILER:PATH"         : util.Interpolate("%(prop:builddir)s/build/bin/clang.exe"),
                                "CMAKE_ASM_COMPILER:PATH"       : util.Interpolate("%(prop:builddir)s/build/bin/clang.exe"),
                                "CMAKE_SYSTEM_NAME"             : "Linux",
                                "CMAKE_SYSTEM_PROCESSOR"        : "aarch64",
                                "CMAKE_CROSSCOMPILING"          : "ON",

                                # Required for the native table-gen
                                "LLVM_NATIVE_TOOL_DIR:PATH"     : util.Interpolate("%(prop:builddir)s/build/bin"),

                                "LLVM_DEFAULT_TARGET_TRIPLE"    : "aarch64-unknown-linux-gnu",
                                "LLVM_HOST_TRIPLE"              : "aarch64-unknown-linux-gnu",
                                "LLVM_TARGETS_TO_BUILD"         : "AArch64",
                                "LLVM_ENABLE_ASSERTIONS"        : "ON",
                                "LLVM_INCLUDE_BENCHMARKS"       : "OFF",
                                "LLVM_PARALLEL_LINK_JOBS"       : 8,
                                "CLANG_DEFAULT_LINKER"          : "lld",

                                "LLDB_INCLUDE_TESTS"            : "OFF",
                                "LLDB_ENABLE_PYTHON"            : "OFF",
                                "LLDB_ENABLE_LIBEDIT"           : "OFF",
                                "LLDB_ENABLE_CURSES"            : "OFF",
                                "LLDB_ENABLE_LZMA"              : "OFF",

                                "LLVM_ENABLE_ZLIB"              : "OFF",
                            },
                            obj_dir = "build-lldb-server",
                            targets = ["lldb-server"],
                            install_dir = util.Interpolate("%(prop:builddir)s/lldb-server-install"),
                            install_targets = ["install-lldb-server"],
                            post_finalize_steps = [
                                steps.ShellSequence(name = "exec-lldb-server",
                                    commands = [
                                        util.ShellArg(command=[ "ssh", util.Interpolate("%(prop:remote_test_user)s@%(prop:remote_test_host)s"), "killall lldb-server ; exit 0;" ], logname="stdio"),
                                        util.ShellArg(command=[ "scp", "lldb-server", util.Interpolate("%(prop:remote_test_user)s@%(prop:remote_test_host)s:~/lldb-server") ], logname="stdio"),
                                        util.ShellArg(command=[ "ssh", util.Interpolate("%(prop:remote_test_user)s@%(prop:remote_test_host)s"), "chmod +x ~/lldb-server" ], logname="stdio"),
                                        util.ShellArg(command=[ "ssh", util.Interpolate("%(prop:remote_test_user)s@%(prop:remote_test_host)s"),
                                                                    "$(nohup ~/lldb-server p --listen '*:1234' --server > /dev/null 2>&1 &)" ], logname="stdio"),
                                    ],
                                    workdir = util.Interpolate("%(prop:builddir)s/lldb-server-install/bin"),
                                    description = "execute lldb-server on remote target",
                                    haltOnFailure = True,
                                ),
                            ],
                            env = lldb_remote_linux_env.copy(),
                        ), # ]] post_build_steps
                    env = lldb_remote_linux_env.copy(),
                )
        },
]
