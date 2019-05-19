VERSION 5.00
Begin VB.Form Form1 
   BorderStyle     =   1  'Fixed Single
   Caption         =   "VMProtect test [Visual Basic]"
   ClientHeight    =   690
   ClientLeft      =   45
   ClientTop       =   330
   ClientWidth     =   4530
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   ScaleHeight     =   690
   ScaleWidth      =   4530
   StartUpPosition =   2  'CenterScreen
   Begin VB.CommandButton Command1 
      Caption         =   "Check password"
      Default         =   -1  'True
      Height          =   375
      Left            =   2850
      TabIndex        =   2
      Top             =   165
      Width           =   1500
   End
   Begin VB.TextBox Text1 
      Height          =   315
      Left            =   915
      TabIndex        =   1
      Top             =   195
      Width           =   1815
   End
   Begin VB.Label Label1 
      Caption         =   "Password:"
      Height          =   255
      Left            =   135
      TabIndex        =   0
      Top             =   240
      Width           =   810
   End
End
Attribute VB_Name = "Form1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private Sub Command1_Click()
  VMProtectBegin (StrPtr("Test marker"))
  If Val(Text1.Text) Mod 17 = 13 Then
   MsgBox StrFromPtr(VMProtectDecryptString(StrPtr("Correct password"))), vbInformation + vbOKOnly, "Information"
  Else
   MsgBox StrFromPtr(VMProtectDecryptString(StrPtr("Incorrect password"))), vbCritical + vbOKOnly, "Error"
   Text1.SetFocus
  End If
  VMProtectEnd
End Sub
