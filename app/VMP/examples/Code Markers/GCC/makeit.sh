#!/bin/bash
set -ex
OS=`uname`

if [[ $OS == "Linux" ]]; then
 echo make for Linux
 gcc Project1.cpp -Wl,-rpath,\$ORIGIN,-rpath-link,./ -L ./ -lVMProtectSDK32 -m32 -o Project1-linux-x86 && echo 32 bit OK!
 gcc Project1.cpp -Wl,-rpath,\$ORIGIN,-rpath-link,./ -L ./ -lVMProtectSDK64 -m64 -o Project1-linux-x64 && echo 64 bit OK!
else
 echo make for OS X
 gcc Project1.cpp libVMProtectSDK.dylib -o Project1 && echo OK!
fi
