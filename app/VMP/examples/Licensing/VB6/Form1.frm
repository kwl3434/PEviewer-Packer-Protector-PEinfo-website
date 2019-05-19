VERSION 5.00
Begin VB.Form Form1 
   BorderStyle     =   1  'Fixed Single
   Caption         =   "License TestApp"
   ClientHeight    =   7110
   ClientLeft      =   45
   ClientTop       =   330
   ClientWidth     =   10620
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   ScaleHeight     =   7110
   ScaleWidth      =   10620
   StartUpPosition =   2  'CenterScreen
   Begin VB.CommandButton btClose 
      Cancel          =   -1  'True
      Caption         =   "Close"
      Default         =   -1  'True
      Height          =   375
      Left            =   9060
      TabIndex        =   6
      Top             =   6600
      Width           =   1395
   End
   Begin VB.CommandButton btTry 
      Caption         =   "Try to execute the protected code"
      Height          =   375
      Left            =   120
      TabIndex        =   5
      Top             =   6600
      Width           =   2895
   End
   Begin VB.TextBox tbHWID 
      BackColor       =   &H8000000F&
      Height          =   365
      Left            =   120
      Locked          =   -1  'True
      TabIndex        =   4
      Top             =   6060
      Width           =   10335
   End
   Begin VB.TextBox tbResult 
      BackColor       =   &H8000000F&
      Height          =   2895
      Left            =   120
      Locked          =   -1  'True
      MultiLine       =   -1  'True
      TabIndex        =   2
      Top             =   2760
      Width           =   10335
   End
   Begin VB.TextBox tbSerial 
      Height          =   2175
      Left            =   120
      MultiLine       =   -1  'True
      TabIndex        =   1
      Top             =   420
      Width           =   10335
   End
   Begin VB.Label Label2 
      AutoSize        =   -1  'True
      Caption         =   "Hardware ID:"
      Height          =   195
      Left            =   120
      TabIndex        =   3
      Top             =   5820
      Width           =   945
   End
   Begin VB.Label Label1 
      AutoSize        =   -1  'True
      Caption         =   "Paste the serial number bellow:"
      Height          =   195
      Left            =   120
      TabIndex        =   0
      Top             =   180
      Width           =   2190
   End
End
Attribute VB_Name = "Form1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private Sub btClose_Click()
Unload Me
End Sub

Private Sub btTry_Click()
VMProtectBeginVirtualizationLockByKey ("")
MsgBox "Protected code successfully executed", vbInformation + vbOKOnly, "ProtectedCode()"
End Sub

Private Sub Form_Load()
Dim HWID As String
HWID = String(2000, 0)
If VMProtectGetCurrentHWID(HWID, Len(HWID)) Then
    tbHWID.Text = HWID
End If
End Sub

Private Sub tbSerial_Change()
Dim status As Long
status = VMProtectSetSerialNumber(tbSerial.Text)
tbResult.Text = ""
tbResult.Text = tbResult.Text & "VMProtectSetSerialNumber() returned: " & status & vbCrLf
If (status And SERIAL_STATE_FLAG_CORRUPTED) = SERIAL_STATE_FLAG_CORRUPTED Then
    tbResult.Text = tbResult.Text & vbTab & "SERIAL_STATE_FLAG_CORRUPTED" & vbCrLf
End If
If (status And SERIAL_STATE_FLAG_INVALID) = SERIAL_STATE_FLAG_INVALID Then
    tbResult.Text = tbResult.Text & vbTab & "SERIAL_STATE_FLAG_INVALID" & vbCrLf
End If
If (status And SERIAL_STATE_FLAG_BLACKLISTED) = SERIAL_STATE_FLAG_BLACKLISTED Then
    tbResult.Text = tbResult.Text & vbTab & "SERIAL_STATE_FLAG_BLACKLISTED" & vbCrLf
End If
If (status And SERIAL_STATE_FLAG_DATE_EXPIRED) = SERIAL_STATE_FLAG_DATE_EXPIRED Then
    tbResult.Text = tbResult.Text & vbTab & "SERIAL_STATE_FLAG_DATE_EXPIRED" & vbCrLf
End If
If (status And SERIAL_STATE_FLAG_RUNNING_TIME_OVER) = SERIAL_STATE_FLAG_RUNNING_TIME_OVER Then
    tbResult.Text = tbResult.Text & vbTab & "SERIAL_STATE_FLAG_RUNNING_TIME_OVER" & vbCrLf
End If
If (status And SERIAL_STATE_FLAG_BAD_HWID) = SERIAL_STATE_FLAG_BAD_HWID Then
    tbResult.Text = tbResult.Text & vbTab & "SERIAL_STATE_FLAG_BAD_HWID" & vbCrLf
End If
If (status And SERIAL_STATE_FLAG_MAX_BUILD_EXPIRED) = SERIAL_STATE_FLAG_MAX_BUILD_EXPIRED Then
    tbResult.Text = tbResult.Text & vbTab & "SERIAL_STATE_FLAG_MAX_BUILD_EXPIRED" & vbCrLf
End If
tbResult.Text = tbResult.Text & vbCrLf

Dim status2 As Long
status2 = VMProtectGetSerialNumberState()
tbResult.Text = tbResult.Text & "VMProtectGetSerialNumberState() returned: " & status2 & vbCrLf
tbResult.Text = tbResult.Text & vbCrLf

Dim sd As VMProtectSerialNumberData
Dim res As Boolean
res = VMProtectGetSerialNumberData(sd, Len(sd))
tbResult.Text = tbResult.Text & "VMProtectGetSerialNumberData() returned: " & res & vbCrLf
If res Then
    tbResult.Text = tbResult.Text & "State = " & sd.nState & vbCrLf
    Dim name As String
    For i = 1 To 256
        If sd.wUserName(i) = 0 Then
            Exit For
        End If
        name = name & ChrW(sd.wUserName(i))
    Next
    tbResult.Text = tbResult.Text & "User Name = " & name & vbCrLf
    Dim email As String
    For i = 1 To 256
        If sd.wEMail(i) = 0 Then
            Exit For
        End If
        email = email & ChrW(sd.wEMail(i))
    Next
    tbResult.Text = tbResult.Text & "E-Mail = " & email & vbCrLf
    tbResult.Text = tbResult.Text & "Date of expiration = " & sd.dtExpire.wYear & "-" & sd.dtExpire.bMonth & "-" & sd.dtExpire.bDay & vbCrLf
    tbResult.Text = tbResult.Text & "Max date of build = " & sd.dtMaxBuild.wYear & "-" & sd.dtMaxBuild.bMonth & "-" & sd.dtMaxBuild.bDay & vbCrLf
    tbResult.Text = tbResult.Text & "Running time limit = " & sd.bRunningTime & " minutes" & vbCrLf
    tbResult.Text = tbResult.Text & "Length of user data = " & sd.nUserDataLength & " bytes" & vbCrLf
End If
End Sub
