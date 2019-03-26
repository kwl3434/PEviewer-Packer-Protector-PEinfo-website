# PEviewer
This program is a simple command-line 32bit PE viewer that prints basic information, such as : 
size of Optional Header in PE file, address of Entry Point or number of subsystem.
It also provides data of each section in the executable. 

When analyzing PE files, e.g. to determine whether it is a malicious file, imports play an important role.
Therefore, the program gives information about DLLs being imported.

In the nearest future, I am planning to add a list of functions imported by each DLL. 
