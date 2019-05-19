//---------------------------------------------------------------------------

#include <vcl.h>
#pragma hdrstop

#include "Unit1.h"
#include "VMProtectSDK.h"
//---------------------------------------------------------------------------
#pragma package(smart_init)
#pragma resource "*.dfm"
TForm1 *Form1;
//---------------------------------------------------------------------------
__fastcall TForm1::TForm1(TComponent* Owner)
	: TForm(Owner)
{
	AnsiChar buf[128];
	memset(buf, 0, sizeof(buf));
	VMProtectGetCurrentHWID(buf, sizeof(buf));
	edHWID->Text = buf;
}
//---------------------------------------------------------------------------
void __fastcall TForm1::btTryClick(TObject *Sender)
{
	Application->MessageBox(L"Protected code succesfully executed", ExtractFileName(Application->ExeName).c_str(), MB_OK | MB_ICONINFORMATION);
}
//---------------------------------------------------------------------------
void __fastcall TForm1::btCloseClick(TObject *Sender)
{
	Close();
}
//---------------------------------------------------------------------------
void __fastcall TForm1::edSerialNumberChange(TObject *Sender)
{
	Integer nState, nState2;
	VMProtectSerialNumberData sd;
	Boolean res;

	edInfo->Lines->BeginUpdate();

	// set the serial number
	nState = VMProtectSetSerialNumber(AnsiString(edSerialNumber->Text).c_str());

	// parse serial number state
	edInfo->Lines->Clear();
	edInfo->Lines->Add(Format("VMProtectSetSerialNumber() returned: 0x%.8X", ARRAYOFCONST((nState))));
	if (nState & SERIAL_STATE_FLAG_CORRUPTED)
		edInfo->Lines->Add("\tSERIAL_STATE_FLAG_CORRUPTED");
	if (nState & SERIAL_STATE_FLAG_INVALID)
		edInfo->Lines->Add("\tSERIAL_STATE_FLAG_INVALID");
	if (nState & SERIAL_STATE_FLAG_BLACKLISTED)
		edInfo->Lines->Add("\tSERIAL_STATE_FLAG_BLACKLISTED");
	if (nState & SERIAL_STATE_FLAG_DATE_EXPIRED)
		edInfo->Lines->Add("\tSERIAL_STATE_FLAG_DATE_EXPIRED");
	if (nState & SERIAL_STATE_FLAG_RUNNING_TIME_OVER)
		edInfo->Lines->Add("\tSERIAL_STATE_FLAG_RUNNING_TIME_OVER");
	if (nState & SERIAL_STATE_FLAG_BAD_HWID)
		edInfo->Lines->Add("\tSERIAL_STATE_FLAG_BAD_HWID");
	if (nState & SERIAL_STATE_FLAG_MAX_BUILD_EXPIRED)
		edInfo->Lines->Add("\tSERIAL_STATE_FLAG_MAX_BUILD_EXPIRED");

	// another way to get a state
	nState2 = VMProtectGetSerialNumberState();
	edInfo->Lines->Add(Format("\r\nVMProtectGetSerialNumberState() returned: 0x%.8X", ARRAYOFCONST((nState2))));

	// try to read serial number data
	memset(&sd, 0, sizeof(sd));
	res = VMProtectGetSerialNumberData(&sd, sizeof(sd));
	edInfo->Lines->Add(Format("\r\nVMProtectGetSerialNumberData() returned: %s", ARRAYOFCONST((res ? "TRUE" : "FALSE"))));
	if (res) {
		edInfo->Lines->Add(Format("State = 0x%.8X", ARRAYOFCONST((sd.nState))));
		edInfo->Lines->Add(Format("User Name = %s", ARRAYOFCONST((sd.wUserName))));
		edInfo->Lines->Add(Format("E-Mail = %s", ARRAYOFCONST((sd.wEMail))));
		edInfo->Lines->Add(Format("Date of expiration = %.4d-%.2d-%.2d", ARRAYOFCONST((sd.dtExpire.wYear, sd.dtExpire.bMonth, sd.dtExpire.bDay))));
		edInfo->Lines->Add(Format("Max date of build = %.4d-%.2d-%.2d", ARRAYOFCONST((sd.dtMaxBuild.wYear, sd.dtMaxBuild.bMonth, sd.dtMaxBuild.bDay))));
		edInfo->Lines->Add(Format("Running time limit = %d minutes", ARRAYOFCONST((sd.bRunningTime))));
		edInfo->Lines->Add(Format("Length of user data = %d bytes", ARRAYOFCONST((sd.nUserDataLength))));
	}
	edInfo->Lines->EndUpdate();
}
//---------------------------------------------------------------------------
