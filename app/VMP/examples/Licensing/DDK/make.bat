@ECHO OFF

set DDK_PATH=C:\WinDDK\7600.16385.1\

set OLDDIR=%CD%

call %DDK_PATH%\bin\setenv.bat %DDK_PATH% wxp free no_oacr

chdir /d %OLDDIR%

nmake
