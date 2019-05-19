\Dev-Cpp\bin\windres Resource.rc Resource.o
\Dev-Cpp\bin\c++ -mwindows Project1.cpp Resource.o VMProtectSDK32.a -o Project1.exe -Os -Wl,-Map=Project1.map