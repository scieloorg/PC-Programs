VERSION 5.00
Begin VB.Form FormLogin 
   Caption         =   "Login"
   ClientHeight    =   1200
   ClientLeft      =   60
   ClientTop       =   450
   ClientWidth     =   3210
   LinkTopic       =   "Form1"
   ScaleHeight     =   1200
   ScaleWidth      =   3210
   StartUpPosition =   3  'Windows Default
   Begin VB.TextBox Text1 
      Height          =   375
      IMEMode         =   3  'DISABLE
      Left            =   120
      PasswordChar    =   "*"
      TabIndex        =   0
      Text            =   "123456789"
      Top             =   240
      Width           =   2895
   End
   Begin VB.CommandButton Command2 
      Caption         =   "OK"
      Height          =   375
      Index           =   1
      Left            =   120
      TabIndex        =   1
      Top             =   720
      Width           =   1455
   End
   Begin VB.CommandButton Command1 
      Caption         =   "Cancel"
      Height          =   375
      Left            =   1680
      TabIndex        =   2
      Top             =   720
      Width           =   1455
   End
End
Attribute VB_Name = "FormLogin"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Private Sub Command1_Click()
    Unload Me
End Sub

Private Sub Command2_Click(index As Integer)
    If StrComp(Text1.text, "2010", vbBinaryCompare) = 0 Then
        Unload Me
        Call FrmCodes.loadForm(DBCODESPATH, DBCODEFILE, DBCODESLABEL)
    End If
End Sub
