//---------------------------------------------------------------------------

#ifndef Unit1H
#define Unit1H
//---------------------------------------------------------------------------
#include <System.Classes.hpp>
#include <Vcl.Controls.hpp>
#include <Vcl.StdCtrls.hpp>
#include <Vcl.Forms.hpp>
//---------------------------------------------------------------------------
class TForm1 : public TForm
{
__published:	// IDE-managed Components
	TLabel *Label1;
	TMemo *edSerialNumber;
	TMemo *edInfo;
	TButton *btTry;
	TButton *btClose;
	TEdit *edHWID;
	TLabel *Label2;
	void __fastcall btTryClick(TObject *Sender);
	void __fastcall btCloseClick(TObject *Sender);
	void __fastcall edSerialNumberChange(TObject *Sender);
private:	// User declarations
public:		// User declarations
	__fastcall TForm1(TComponent* Owner);
};
//---------------------------------------------------------------------------
extern PACKAGE TForm1 *Form1;
//---------------------------------------------------------------------------
#endif
