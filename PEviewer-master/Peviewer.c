#include <stdio.h>
#include <string.h>
#include <windows.h>

#define PE "It is not a PE file\n"

int RAW2offset(int input);

IMAGE_DOS_HEADER DosHeader;
IMAGE_FILE_HEADER FileHeader;
IMAGE_SECTION_HEADER SectionHeader;
IMAGE_OPTIONAL_HEADER32 OptionalHeader;	
IMAGE_IMPORT_DESCRIPTOR ImportDescriptor;
DWORD PointerToPeHeader = 0;
DWORD Size_Of_File = 0;
DWORD Pe_Signature = 0;
WORD Size_Of_Opt_Header = 0;
WORD subsys = 0;
DWORD Addr_of_EP = 0;
DWORD PtrIdata = 0;
DWORD ImageBase = 0;
DWORD ImportsVA = 0;
DWORD ImportsSize = 0;
DWORD ImportDirAddr = 0;
int NrOfSections = 0;
//char buf[NrOfSections][8];

struct SectionInfo{
	char name[10];
	int VA;
	int VirtualSize;
	int SizeOfRAW;
	int Ptr2RAW;
	DWORD characteristics;
	};

void print_section(struct SectionInfo *sinfo){
	printf("%s\n", sinfo->name);
	printf("\tVirtual Address : %x\n", sinfo->VA);
	printf("\tVirtual Size : %x\n", sinfo->VirtualSize);
	printf("\tPointer To Raw Data : %x\n", sinfo->Ptr2RAW);
	printf("\tSize of Raw Data : %x\n", sinfo->SizeOfRAW);
	printf("\tCharacteristics : %lx\n", sinfo->characteristics);
}

int main(int argc, char *argv[])
{
	char buffer[20];

	if(argc<2){
		printf("Usage:\nPEviewer.exe FILE.exe");
		return 1;
	}

	strncpy(buffer,argv[1],20);
	printf("Opened the file: %s\n", buffer);

	FILE* p;

	p = fopen(buffer, "rb");
	if(p == NULL){
		perror("Cannot open the file test.exe");
		return 2;
	}
	puts("File opened successfully");
	fseek(p,0,SEEK_END);
	Size_Of_File = ftell(p);
	fseek(p,0,SEEK_SET);
	fread(&DosHeader,1,sizeof(DosHeader),p);

	if(DosHeader.e_magic != 'M' + 'Z' * 256){
		printf(PE);
		fclose(p);
		return -1;
	}

	PointerToPeHeader = DosHeader.e_lfanew;
	printf("PE header available at: %lx\n",PointerToPeHeader);
	fseek(p,PointerToPeHeader,SEEK_SET);
	fread(&Pe_Signature,1,sizeof(Pe_Signature),p);
	
	if(Pe_Signature != 'P' + 'E' * 256){
		printf(PE);
		fclose(p);
		return -1;
	}

	fread(&FileHeader,1,sizeof(FileHeader),p);
	NrOfSections = FileHeader.NumberOfSections;
	printf("# of Sections: %d\n", NrOfSections);

	struct SectionInfo sinfo[NrOfSections];

	Size_Of_Opt_Header = FileHeader.SizeOfOptionalHeader;
	printf("Size of Optional Header is: %d\n", Size_Of_Opt_Header);
	//fseek(p,Size_Of_Opt_Header,SEEK_CUR);
	fread(&OptionalHeader,1,Size_Of_Opt_Header,p);
	subsys = OptionalHeader.Subsystem;
	printf("# of subsystem: %d\n", subsys);
	Addr_of_EP = OptionalHeader.AddressOfEntryPoint;
	printf("Address of entry point: %lx\n", Addr_of_EP);

	ImportsVA = OptionalHeader.DataDirectory[1].VirtualAddress;
	ImportsSize = OptionalHeader.DataDirectory[1].Size;
	printf("Virtual Address of Import table %lx\n", ImportsVA);
	printf("Import table size %lx\n", ImportsSize);
	ImageBase = OptionalHeader.ImageBase;
	printf("ImageBase equals %lx\n\n", ImageBase);
	
	int i=0;
	do{
	fread(&SectionHeader,1,sizeof(SectionHeader),p);
	
	memcpy(sinfo[i].name,SectionHeader.Name,10);
	sinfo[i].VA = SectionHeader.VirtualAddress;
	sinfo[i].VirtualSize = SectionHeader.Misc.VirtualSize;
	sinfo[i].SizeOfRAW = SectionHeader.SizeOfRawData;
	sinfo[i].Ptr2RAW = SectionHeader.PointerToRawData;
	sinfo[i].characteristics = SectionHeader.Characteristics;
	print_section(&sinfo[i]);

	/*if(strcmp(".idata",sinfo[i].name)==0){
		puts("Match\n");
		PtrIdata = SectionHeader.PointerToRawData;
		printf("Pointer to .idata section: %lx\n", PtrIdata);
		}*/

	i++;
	}while(i<NrOfSections);

	int RAW2offset(int input){
		int i;
		int output = 0;
		for(i=0; i<NrOfSections; i++){
			if((input >= sinfo[i].VA) && (input <= (sinfo[i].VirtualSize+sinfo[i].VA))){
				output = input-sinfo[i].VA+sinfo[i].Ptr2RAW;
				return output;
			}
					
		}
		return -1;
	}

	//ImportDirAddr = ImportsVA-SectVA+SectPtrRAW;
	
	ImportDirAddr = RAW2offset(ImportsVA);
	printf("\nImports at %lx\n", ImportDirAddr);
	fseek(p, ImportDirAddr, SEEK_SET);
	fread(&ImportDescriptor,1,20,p); //read the first Import
	int count = 1;

	while(ImportDescriptor.Name!=0){
		fread(&ImportDescriptor,1,20,p);	
		count++;
	}

	IMAGE_IMPORT_DESCRIPTOR Imported[count-1];
	fseek(p, ImportDirAddr, SEEK_SET);

	for(i=0;i<(count-1);i++){
		fread(&Imported[i],1,20,p);
		printf("[%d] Import Descriptor Name at %lx\n", i, Imported[i].Name);
	}
	
	DWORD filename;
	
	puts("\nList of imported dll's\n");	
	for(i=0;i<(count-1);i++){	
		filename = RAW2offset(Imported[i].Name);
		fseek(p, filename, SEEK_SET);
	do{
		int c;
		c = fgetc(p);
		if(c==0){
			printf("\n");
			break;
		}
		printf("%c",c);
	}while(1);

}
	fclose(p);	
	return 0;
}



