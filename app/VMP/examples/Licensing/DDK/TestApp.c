#include <ntddk.h>
#include "VMProtectDDK.h"

VOID DriverUnload(IN PDRIVER_OBJECT DriverObject)
{

}

NTSTATUS DriverEntry(IN PDRIVER_OBJECT DriverObject, PUNICODE_STRING RegistryPath)
{ 
	int size, status, status2, res;
	char *hwid;
	VMProtectSerialNumberData sd = {0};

	VMProtectBegin("DriverEntry");

	size = VMProtectGetCurrentHWID(NULL, 0);
	hwid = ExAllocatePool(NonPagedPool, size);
	VMProtectGetCurrentHWID(hwid, size);
	DbgPrint("HWID: %s\n", hwid);
	ExFreePool(hwid);
	DbgPrint("\n");

	status = VMProtectSetSerialNumber("IOtjdo0yTQFhExs0hoDu7Y6O3jQgsJqSu2eytTmlsFI1+XJdPXdhRJmSkqzld/RSGes7wqxmxtFQUakrHxkAruXPgOPRZX1Mr/d717LlpDW1DvJJ7ndD/fAziYcKGiQ1HfWjwXWAzjM/A1zT0X333E8zCYmGrWHPC0u94UqjabJ2EF4Wu5K+6zZX8Gy+msV8BarrW1VdGCcEIMA/wVD5t1nrhU4PMAsqzZHkmXuH9RT8AWCBz2n1RWqnk3YOCNFJ8Oywi7YBjVnyzTTHTOojBXo77xmMFoncxUoUzFA6P5653KK14nZ2A4yXb4t2Ia5XOFMcfEQ4HOfLK9dnD2BeGA==");
	DbgPrint("VMProtectSetSerialNumber() returned: 0x%08X\n", status);
	if (status & SERIAL_STATE_FLAG_CORRUPTED)
		DbgPrint("\tSERIAL_STATE_FLAG_CORRUPTED\n");
	if (status & SERIAL_STATE_FLAG_INVALID)
		DbgPrint("\tSERIAL_STATE_FLAG_INVALID\n");
	if (status & SERIAL_STATE_FLAG_BLACKLISTED)
		DbgPrint("\tSERIAL_STATE_FLAG_BLACKLISTED\n");
	if (status & SERIAL_STATE_FLAG_DATE_EXPIRED)
		DbgPrint("\tSERIAL_STATE_FLAG_DATE_EXPIRED\n");
	if (status & SERIAL_STATE_FLAG_RUNNING_TIME_OVER)
		DbgPrint("\tSERIAL_STATE_FLAG_RUNNING_TIME_OVER\n");
	if (status & SERIAL_STATE_FLAG_BAD_HWID)
		DbgPrint("\tSERIAL_STATE_FLAG_BAD_HWID\n");
	if (status & SERIAL_STATE_FLAG_MAX_BUILD_EXPIRED)
		DbgPrint("\tSERIAL_STATE_FLAG_MAX_BUILD_EXPIRED\n");
	DbgPrint("\n");

	status2 = VMProtectGetSerialNumberState();
	DbgPrint("VMProtectGetSerialNumberState() returned: 0x%08X\n", status2);
	DbgPrint("\n");

	res = VMProtectGetSerialNumberData(&sd, sizeof(sd));
	DbgPrint("VMProtectGetSerialNumberData() returned: %s\n", res ? "TRUE" : "FALSE");
	if (res) {
		DbgPrint("State = 0x%08X\n", sd.nState);
		DbgPrint("User Name = %ws\n", sd.wUserName);
		DbgPrint("E-Mail = %ws\n", sd.wEMail);
		DbgPrint("Date of expiration = %04d-%02d-%02d\n", sd.dtExpire.wYear, sd.dtExpire.bMonth, sd.dtExpire.bDay);
		DbgPrint("Max date of build = %04d-%02d-%02d\n", sd.dtMaxBuild.wYear, sd.dtMaxBuild.bMonth, sd.dtMaxBuild.bDay);
		DbgPrint("Running time limit = %d minutes\n", sd.bRunningTime);
		DbgPrint("Length of user data = %d bytes\n", sd.nUserDataLength);
	}

	DriverObject->DriverUnload = DriverUnload;

	return STATUS_SUCCESS;
}