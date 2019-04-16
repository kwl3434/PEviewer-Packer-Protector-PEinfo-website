#include <stdio.h>
#include <conio.h>
#include <string.h>
#include <stdlib.h>
#include <basetsd.h>
#include <Windows.h>
#include <winnt.h>
#include <process.h>
#include <direct.h>
#include <io.h>

void textcolor(int color_number) { // 가져온 함수(글자 색 바꾸기)
        SetConsoleTextAttribute(GetStdHandle(STD_OUTPUT_HANDLE), color_number);
}
/*
 * 여기에서 맨 뒤에 두자리, 즉 16진수로 0x0000 ~ 0x00FF까지가 이 함수에서 의미있는 매개 변수 이다.
 * 각 16진수에 해당하는 색은 다음과 같다.
 * 0 - 검정색, 1 - 파랑색, 2 - 초록색, 3 - 옥색, 4 - 빨간색, 5 - 자주색, 6 - 노랑색, 7 - 흰색, 8 - 회색,
 * 9 - 연한 파랑색, A - 연한 초록색, B - 연한 옥색, C - 연한 빨간색, D - 연한 자주색, E - 연한 노랑색, F - 밝은 흰색
 * 즉, [밝은 흰색]의 음영색을 가진 [빨간색]의 글자를 출력하고 싶다면
 * 0x00F4 라는 매개변수 값을 넘겨주면 되는 것이다.
 * */

void intro() {   // 프로그램 초기 화면 : 디자인 다시 해야 함
        printf("          ..........    @ @   @     @    @ @   @                   ..........\n\
                        .........    @   @  @ @   @   @  @   @                   .........\n\
                        ........    @@@@@@ @   @ @  @@@@@@  @                   ........\n\
                        ......     @     @ @     @ @     @  @@@@@@             ........\n\
                        .....      ----------------------------                .......\n\
                        ....        by J U N Y O U N G                        .....\n\
                        ...       ----------------------------                ....\n\
                        ..          &&&         $$$$$                         ...\n\
                        ==          &  &        $                            ==\n\
                        __||__        &&&&        $$$$$                      __||__\n\
                        |      |       &           $                         |      |\n\
                        _________|______|_____  &   ortable $$$$$ xcutable       _____|______|_________\n\n");

        textcolor(0x0f);   // white
        printf("This program view the Windows 32bit Portable Excutable File's struct member. \n");
        printf("I want P.romote E.xperience in this project! \n");

        textcolor(0x0A);   // green
        printf("You can Copy Modify Distribute this program. \n\n");

        textcolor(0x0F);   // white
        printf("usage > AnalPE [option] filename \n\n");

        textcolor(0x0E);   // yellow
        printf("Option \n");

        textcolor(0x0F);   // white
        printf("-s: save the result to file \n");
        printf("-q: shut up \n\n");

        printf("Copyright 2015 \n");
}

void show_Allhex(char* str, FILE* input)   // 추가 할꺼: fseek
{
        unsigned char hex;
        int i, j;

        char temp[17];

        system("cls");

        fseek(input, 0, SEEK_SET);
        i = 0;

        while (!feof(input)) {
                hex = fgetc(input);

                temp[i % 16] = hex;

                if (i % 16 == 0) {
                        printf("%08x ", i);
                }
                printf("%02x ", hex);

                if (i % 8 == 7) {   // fileOffset 8바이트 8바이트 문자열
                        putchar(' ');
                }
                if (i % 16 == 15) {
                        temp[16] = '\0';
                        printf("  ");

                        for (j = 0; j < 17; j++) {
                                if (temp[j] >= 0x21 && temp[j] <= 0x7E) {   // 출력 가능한 문자
                                        putchar(temp[j]);
                                }
                                else {
                                        putchar('.');
                                }
                        }

                        putchar('\n');
                }
                if (i % 336 == 335) {
                        printf("\nPress 'q' to Quit! \n");

                        if (getch() == 'q') {
                                return;
                        }

                        system("cls");
                }

                i++;
        }
}


void show_fileMemMap(char* str, FILE* input)
{
        printf("show file/Memory Map \n");
}

void show_DosHeader(char* str, FILE* input)
{
        int i, j;
        char* ptr;
        unsigned int tempi;
        unsigned short temps;

        char* varName[19] = { "e_magic", "e_cblp", "e_cp", "e_crlc", "e_cparhdr", "e_minalloc", "e_maxalloc", "e_ss", "e_sp", "e_csum", "e_ip", "e_cs", "e_lfarlc", "e_ovno", "e_res[4]", "e_oemid", "e_oeminfo", "e_res2[10]", "e_lfanew" };

        do {
                system("cls");
                printf("typedef struct _IMAGE_DOS_HEADER {   \n");
                for (i = 0; i < sizeof(varName) / sizeof(char *); i++) {
                        if (!strcmp(varName[i], "e_magic")) {
                                printf("%10s %10s = ", "WORD", varName[i]);

                                fseek(input, 0, SEEK_SET);
                                ptr = (char *)&temps;
                                for (j = 0; j < 2; j++) {
                                        *(ptr++) = fgetc(input);
                                }

                                printf("%8X", temps, str);

                                ptr = (char*)&temps;

                                putchar('(');
                                for (j = 0; j < 2; j++) {
                                        putchar(*(ptr++));
                                }
                                printf(") \n");
                        }
                        else if (!strcmp(varName[i], "e_lfanew")) {
                                printf("%10s %10s = ", "LONG", varName[i]);

                                fseek(input, 0x3C, SEEK_SET);
                                ptr = (char *)&tempi;
                                for (j = 0; j < 4; j++) {
                                        *(ptr++) = fgetc(input);
                                }

                                printf("%08X \n", tempi);
                        }
                        else {
                                printf("%10s %10s \n", "WORD", varName[i]);
                        }
                }
                printf("} IMAGE_DOS_HEADER, *PIMAGE_DOS_HEADER   \n\n");

                printf("Press 'q' to Quit! \n");
        } while (getch() != 'q');
}

void show_NTHeaders(char* str, FILE* input)   // 보류할 점: Characteristics 보여 주기, DLLCharacteristics
{
        int i, j, tempi, flag;
        unsigned char* ptr;

        union temp {
                short temps;
                int temp4;
        } Temp;

        char* NtHeaders[3] = { "Signature", "FileHeader", "OptionalHeader" };
        char* NtType[3] = { "DWORD", "IMAGE_FILE_HEADER", "IMAGE_OPTIONAL_HEADER32" };

        char* FileHeader[7] = { "Machine", "NumberOfSections", "TimeDateStamp", "PointerToSymbolTable", "NumberOfSymbols", "SizeOfOptionalHeader", "Characteristics" };
        char* FileType[7] = { "WORD", "WORD", "DWORD", "DWORD", "DWORD", "WORD", "WORD" };

        char* OptionalHeader[] = { "Magic", "MajorLinkerVersion", "MinorLinkerVersion", "SizeOfCode", "SizeOfInitializedData", "SizeOfUnInitionalizedData", "AddressOfEntryPoint", "BaseOfCode", "BaseOfData", "ImageBase", "SectionAlignment", "FileAlignment", "MajorOperatingSystemVersion", "MinorOperatingSystemVersion", "MajorImageVersion", "MinorImageVersion", "MajorSubsystemVersion", "MinorSubsystemVersion", "Win32VersionValue", "SizeOfImage", "SizeOfHeaders", "Checksum", "Subsystem", "DllCharacteristics", "SizeOfStackReserve", "SizeOfStackCommit", "SizeOfHeapReserver", "SizeOfHeapCommit", "LoaderFlags", "NumberOfRvaAndSizes", "DataDirectory[16]" };
        char* OptionalType[] = { "WORD", "BYTE", "BYTE", "DWORD", "DWORD", "DWORD", "DWORD", "DWORD", "DWORD", "DWORD", "DWORD", "DWORD", "WORD", "WORD", "WORD", "WORD", "WORD", "WORD", "DWORD", "DWORD", "DWORD", "DWORD", "WORD", "WORD", "DWORD", "DWORD", "DWORD", "DWORD", "DWORD", "DWORD", "IMAGE_DATA_DIRECTORY" };

        char* core[] = { "Magic", "AddressOfEntryPoint", "ImageBase", "SectionAlignment", "FileAlignment", "SizeOfImage", "SizeOfHeaders", "Subsystem", "NumberOfRvaAndSizes" };

        char* Directory[16] = { "EXPORT Directory", "IMPORT Directory", "RESOURCE Directory", "EXCEPTION Directory", "SECURITY Directory", "BASERELOC Directory", "DEBUG Directory", "COPYRIGHT Directory", "GLOBALPTR Directory", "TLS Directory", "LOAD_CONFIG Directory", "BOUND_IMPORT Directory", "IAT Directory", "DELAY Directory", "COM_DESCRIPTOR Directory", "Reserved Directory" };

        fseek(input, 0x3C, SEEK_SET);

        ptr = (unsigned char*)&tempi;
        for (i = 0; i < 4; i++) {
                *(ptr++) = fgetc(input);
        }

        fseek(input, tempi, SEEK_SET);

        ptr = (unsigned char*)&tempi;
        for (i = 0; i < 4; i++) {
                *(ptr++) = fgetc(input);
        }

        system("cls");
        printf("typedef strunct _IMAGE_NT_HEADERS {  \n");
        for (i = 0; i < 3; i++) {
                if (!strcmp("Signature", NtHeaders[i])) {
                        ptr = (unsigned char*)&tempi;
                        printf("   %-30s %-10s ", NtType[i], NtHeaders[i]);
                        printf("= %08x(%s) \n", tempi, ptr);
                }
                else {
                        printf("   %-30s %10s \n", NtType[i], NtHeaders[i]);
                }
        }
        printf("} IMAGE_NT_HEADER32, *PIMAGE_NT_HEADER32 \n\n");
        printf("Press 'q' to Quit!!! \n");

        if (getch() == 'q') {
                return;
        }

        system("cls");

        fseek(input, 0x3C, SEEK_SET);

        ptr = (unsigned char*)&tempi;
        for (i = 0; i < 4; i++) {
                *(ptr++) = fgetc(input);
        }
        fseek(input, tempi += 4, SEEK_SET);
        printf("typedef struct _IMAGE_FILE_HEADER { \n");
        for (i = 0; i < 7; i++) {
                if (!strcmp(FileType[i], "WORD")) {
                        fseek(input, tempi, SEEK_SET);
                        printf("   %-10s %-20s = ", FileType[i], FileHeader[i]);

                        ptr = (unsigned char*) &(Temp.temps);
                        for (j = 0; j < 2; j++) {
                                *(ptr++) = fgetc(input);
                        }
                        printf("%04X \n", Temp.temps);

                        tempi += 2;
                }
                else {
                        printf("   %-10s %-20s \n", FileType[i], FileHeader[i]);
                        tempi += 4;
                }
        }
        printf("} IMAGE_FILE_HEADER, *PIMAGE_FILE_HEADER; \n\n");
        printf("Press 'q' to Quit!!! \n");

        if (getch() == 'q') {
                return;
        }

        system("cls");

        fseek(input, 0x3C, SEEK_SET);
        ptr = (unsigned char*)&tempi;
        for (i = 0; i < 4; i++) {
                *(ptr++) = fgetc(input);
        }
        fseek(input, tempi += 4 + sizeof(IMAGE_FILE_HEADER), SEEK_SET);

        printf("typedef struct _IMAGE_OPTIONAL_HEADER { \n");
        for (i = 0; i < sizeof(OptionalHeader) / sizeof(char*); i++) {
                flag = 0;
                for (j = 0; j < sizeof(core) / sizeof(char*); j++) {
                        if (!strcmp(OptionalHeader[i], core[j])) {
                                flag = 1;
                                break;
                        }
                }

                if (flag) {   // 중요 멤버이면
                        if (!strcmp(OptionalType[i], "WORD")) {
                                fseek(input, tempi, SEEK_SET);
                                printf("   %-10s %-30s = ", OptionalType[i], OptionalHeader[i]);

                                ptr = (unsigned char*) &(Temp.temps);
                                for (j = 0; j < 2; j++) {
                                        *(ptr++) = fgetc(input);
                                }
                                printf("%04X \n", Temp.temps);

                                tempi += 2;
                        }
                        else {
                                fseek(input, tempi, SEEK_SET);
                                printf("   %-10s %-30s = ", OptionalType[i], OptionalHeader[i]);

                                ptr = (unsigned char*)&tempi;
                                for (j = 0; j < 4; j++) {
                                        *(ptr++) = fgetc(input);
                                }
                                printf("%08X \n", tempi);

                                tempi = ftell(input);
                        }
                }
                else {
                        printf("   %-10s %s \n", OptionalType[i], OptionalHeader[i]);
                        if (!strcmp(OptionalType[i], "WORD")) {
                                tempi += 2;
                        }
                        else if (!strcmp(OptionalType[i], "BYTE")) {
                                tempi += 1;
                        }
                        else {
                                tempi += 4;
                        }
                }
        }
        printf("} IMAGE_OPTIONAL_HEADER32, *PIMAGE_OPTIONAL_HEADER32; \n\n");
        printf("Press 'q' to Quit!!! \n");

        if (getch() == 'q') {
                return;
        }

        system("cls");
        /*
         *      e_lfanew + (0xF8 - 0x80)
         *              */
        fseek(input, 0x3C, SEEK_SET);
        ptr = (unsigned char*)&tempi;
        for (i = 0; i < 4; i++) {
                *(ptr++) = fgetc(input);
        }
        fseek(input, tempi + (0xF8 - 0x80) - 4, SEEK_SET);

        ptr = (unsigned char*)&(Temp.temp4);
        for (i = 0; i < 4; i++) {
                *(ptr++) = fgetc(input);
        }
        fseek(input, tempi + (0xF8 - 0x80), SEEK_SET);

        for (i = 0; i < Temp.temp4; i++) {
                printf("typedef struct _IMAGE_DATA_DIRECTORY {   // %s \n", Directory[i]);

                ptr = (unsigned char*)&tempi;
                for (j = 0; j < 4; j++) {
                        *(ptr++) = fgetc(input);
                }
                printf("   DWORD   VirtualAddress = %08X; \n", tempi);

                ptr = (unsigned char*)&tempi;
                for (j = 0; j < 4; j++) {
                        *(ptr++) = fgetc(input);
                }
                printf("   DWORD   Size           = %08X; \n", tempi);

                printf("} IMAGE_DATA_DIRECTORY, *PIMAGE_DATA_DIRECTORY; \n\n");
        }

        getch();
}

void show_SectionHeaders(char* str, FILE* input)   // 출력 형식/소스 코드 등 보수 필요
{
        char* Section[] = { "NAME[8]", "PhysicalAddress", "VirtualSize", "VirtualAddress", "SizeOfRawData", "PointerToRawData", "PointerToRelocations", "PointerToLinenumbers", "NumberOfRelocations", "Characteristics" };
        char* type[] = { "BYTE", "DWORD", "DWORD", "DWORD", "DWORD", "DWORD", "DWORD", "WORD", "WORD", "DWORD" };
        char size[] = { 8, 4, 4, 4, 4, 4, 4, 2, 2, 4 };

        char* ptr, name[9];

        int temp1, temp2, i, j, k;
        short temps;

        // 1. e_lfanew + 미지수 -> FILE_HEADER_OFFSET + sizeOfOptionalHeader
        fseek(input, 0x3C, SEEK_SET);
        ptr = (char*)&temp1;
        for (i = 0; i < 4; i++) {
                *(ptr++) = fgetc(input);
        }

        fseek(input, temp1 + 0x6, SEEK_SET);   // number of sections
        ptr = (char*)&temps;
        for (i = 0; i < 2; i++) {
                *(ptr++) = fgetc(input);
        }

        fseek(input, temp1 + 0x14, SEEK_SET);   // Optional Header
        temp2 = 0;
        ptr = (char*)&temp2;
        for (i = 0; i < 2; i++) {
                *(ptr++) = fgetc(input);
        }

        system("cls");

        fseek(input, temp1 + 0x18 + temp2, SEEK_SET);   // section header 구조체 배열 첫 번째 멤버 변수
        for (i = 0; i < temps; i++) {
                printf("typedef struct _IMAGE_SECTION_HEADER { \n");
                for (j = 0; j < sizeof(Section) / sizeof(char*); j++) {
                        if (j == 0) {
                                printf("   %8s  Name[8] = '", type[j]);
                                for (k = 0; k < 8; k++) {
                                        name[k] = fgetc(input);
                                }
                                name[k] = '\0';

                                printf("%s \n", name);
                        }
                        else if (j == 1) {   // union 구조체
                                printf("   union { \n");
                                printf("   %8s  PhysicalAddress \n", type[j]);
                                printf("   %8s  VirtualSize = ", type[j]);

                                ptr = (char*)&temp1;
                                for (k = 0; k < 4; k++) {
                                        *(ptr++) = fgetc(input);
                                }

                                printf("%08X \n", temp1);
                                printf("   } \n");
                        }
                        else {
                                printf("   %-6s  %s ", type[j], Section[j]);

                                temp1 = 0;
                                ptr = (char*)&temp1;
                                for (k = 0; k < size[j]; k++) {
                                        *(ptr++) = fgetc(input);
                                }

                                if (size[j] == 2) {
                                        printf("%04X \n", temp1);
                                }
                                else {
                                        printf("%08X \n", temp1);
                                }
                        }
                }
                printf("} IMAGE_SECTION_HEADER, *PIMAGE_SECTION_HEADER; \n\n");

                getch();
        }

}

void show(char* str, FILE* input)   // 키보드 인터럽트 멀티 쓰레딩으로 처리하기 예정
{
        char* details[] = { " allhex", " file/memory map", " dosheader", " ntheaders", " sectionheaders" };
        void(*subDetail[])(char* str, FILE* input) = { show_Allhex, show_fileMemMap, show_DosHeader, show_NTHeaders, show_SectionHeaders };

        char flag = 1;
        int i;

        for (i = 0; i < sizeof(details) / sizeof(char*); i++) {
                if (!strcmp(str, details[i])) {
                        subDetail[i](str + strlen(details[i]), input);
                        flag = 0;

                        system("cls");
                }
        }

        if (flag) {   // show ? 도 마지막에 구현 예정
                printf("Illegal Instruction!!! \n");
        }
}

DWORD WINAPI save_all(LPVOID lpParam)   // 미완성
{
        int i, j, nResult;
        char* ptr, path[] = "C:\\PEview\\";

        FILE * output;
        nResult = access(path, 0);
        if (nResult == -1) {   // 디렉토리 없으면 생성 : 드라이브 명 수정 필요
                //                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              mkdir(path);
                //                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      }
                //
                //                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              output = fopen("C:\PEview\\", "rt");
                //                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      if (output == NULL) {
                //                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      printf("Failed to open the file \n");
                return;
}
fprintf(output, "Hello?");

MessageBoxA(NULL, "Saved all in the one file completely!!!", "Complete", NULL);

return 0;
}

DWORD WINAPI save_modules(LPVOID lpParam)   // 미완성
{
        MessageBoxA(NULL, "Saved the result in modules completely!!!", "Complete", NULL);
}

void save(char* str, FILE* input)
{
        char* details[] = { " all", " modules" };
        HANDLE hthread = NULL;

        int i;

        for (i = 0; i < sizeof(details) / sizeof(char*); i++) {
                if (!strcmp(str, details[i])) {
                        if (i == 0) {   // save_all : 결과를 하나의 파일에 저장
                                hthread = CreateThread(NULL, 0, save_all, NULL, 0, NULL);
                        }
                        else {   // save_modules : 결과를 여러 개의 파일로 저장
                                hthread = CreateThread(NULL, 0, save_modules, NULL, 0, NULL);
                        }
                }
        }

        if (hthread != NULL) {
                CloseHandle(hthread);
        }
        else {   // 입력 오류나 thread 오류임 : 수정 해야 됨.
                printf("Illegal Instruction!!! \n");
        }
}

int main(int argc, char * argv[])   // 입력된 옵션 처리 기능 추가
{
        FILE * input;

        void(*inst[])(char* str, FILE* input) = { show, save };

        char buffer[50] = "Hello";
        char* instName[] = { "show", "save" };

        int len, i;

        if (argc < 2) {
                intro();
                return -1;
        }

        input = fopen(argv[argc - 1], "rb");

        if (input == NULL) {
                printf("usage > PEview [option] filename \n");

                return -1;
        }

        do {
                printf("input: ");
                fgets(buffer, sizeof(buffer), stdin);   // 실행할 명령어 입력

                len = strlen(buffer);
                buffer[len - 1] = '\0';

                for (i = 0; i < strlen(buffer); i++) {   // 대문자 -> 소문자 : 대소문자 구분 안 함
                        if (buffer[i] >= 'A' && buffer[i] <= 'Z') {
                                buffer[i] += 'a' - 'A';
                        }
                }

                for (i = 0; i < sizeof(instName) / sizeof(char *); i++) {   // 명령어 찾기 & 실행
                        if (!strncmp(buffer, instName[i], strlen(instName[i]))) {
                                inst[i](buffer + strlen(instName[i]), input);
                        }
                }
        } while (strncmp(buffer, "quit", sizeof(buffer)) && strncmp(buffer, "\\q", sizeof(buffer)));

        printf("\n~bye! \n");

        return 0;
}
