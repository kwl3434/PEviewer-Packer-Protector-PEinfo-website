program Project1;

uses {$IFNDEF DARWIN}Windows, Messages, {$ENDIF}Math, StrUtils, Sysutils, VMProtectSDK;

{$IFNDEF DARWIN}
{$R Resource.res}

const
  IDD_DIALOG = 101;
  IDC_BUTTON_CHECKPASSWORD = 102;
  IDC_EDIT = 1000;
{$ENDIF}

{$IFNDEF DARWIN}
function MainHandler(hDlg: HWND; Msg: LongWord; wParam: WPARAM; lParam: LPARAM): LRESULT; stdcall;
{$ENDIF}
  procedure MyMessage(msg: PAnsiChar; error: Boolean);
  var title: AnsiString;
  begin
    title := StrUtils.IfThen(error, 'Error', 'Information');
    {$IFNDEF DARWIN}
    MessageBox(hDlg, msg, PAnsiChar(title), Math.IfThen(error, MB_ICONERROR, MB_ICONINFORMATION) + MB_OK);
    {$ELSE}
    writeln(title + ': ' + msg);
    {$ENDIF}
  end;
  
var Buf: array [0..99] of Char;
begin
  VMProtectBegin('Test marker');
{$IFNDEF DARWIN}
  Result:=0;
  case Msg of
   WM_INITDIALOG: Result:=1;
   WM_COMMAND:
    begin
     if LoWord(wParam) = IDCANCEL then
      begin
       EndDialog(hDlg, LoWord(wParam));
       Result:=1;
      end
     else
     if LoWord(wParam) = IDC_BUTTON_CHECKPASSWORD then
      begin
       GetDlgItemText(hDlg, IDC_EDIT, Buf, SizeOf(Buf));
{$ELSE}
       writeln(VMProtectDecryptStringA('Input password:'));
       readln(Buf); 
{$ENDIF}
       if (StrToIntDef(Buf,0) mod 17 = 13) then
        MyMessage(VMProtectDecryptStringA('Correct password'), False)
       else
        begin
         MyMessage(VMProtectDecryptStringA('Incorrect password'), True);
         {$IFNDEF DARWIN}SetFocus(GetDlgItem(hDlg, IDC_EDIT));{$ENDIF}
        end;
{$IFNDEF DARWIN}
      end;
    end;
  end;
{$ENDIF}
  VMProtectEnd;
{$IFNDEF DARWIN}
end;

begin
  DialogBox(GetModuleHandle(nil),PChar(IDD_DIALOG),0,@MainHandler);
{$ENDIF}
end.
