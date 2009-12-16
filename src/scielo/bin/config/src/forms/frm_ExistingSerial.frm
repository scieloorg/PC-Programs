VERSION 5.00
Begin VB.Form FrmExistingSerial 
   BorderStyle     =   1  'Fixed Single
   Caption         =   "Config - Open Existing Serial"
   ClientHeight    =   5460
   ClientLeft      =   930
   ClientTop       =   1275
   ClientWidth     =   7710
   Icon            =   "frm_ExistingSerial.frx":0000
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   Moveable        =   0   'False
   ScaleHeight     =   5460
   ScaleWidth      =   7710
   StartUpPosition =   2  'CenterScreen
   Begin VB.CommandButton CmdNext 
      Caption         =   "Next"
      Height          =   375
      Left            =   5400
      TabIndex        =   3
      Top             =   5040
      Width           =   975
   End
   Begin VB.CommandButton CmdClose 
      Caption         =   "Close"
      Height          =   375
      Left            =   6600
      TabIndex        =   2
      Top             =   5040
      Width           =   975
   End
   Begin VB.Frame FrameOpenSerial 
      Caption         =   "Select Serial to Open"
      Height          =   4815
      Left            =   120
      TabIndex        =   0
      Top             =   120
      Width           =   7455
      Begin VB.ListBox ListExistingSerial 
         Height          =   4155
         Left            =   120
         Sorted          =   -1  'True
         TabIndex        =   1
         Top             =   360
         Width           =   7215
      End
   End
End
Attribute VB_Name = "FrmExistingSerial"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit


Private Sub CmdClose_Click()
    Unload Me
End Sub

Private Sub CmdNext_Click()
    If Len(ListExistingSerial.text) > 0 Then
        Me.Hide
        Call Serial1.MyOpenSerial(ListExistingSerial.text, False)
    Else
        MsgBox ConfigLabels.getLabel("Select_to_Open")
    End If
End Sub

Sub OpenExistingSerial()
    
    With ConfigLabels
    Caption = App.Title + " - " + .getLabel("ExistingSerial")
    FrameOpenSerial.Caption = .getLabel("Select_to_Open")
    CmdNext.Caption = .getLabel("ButtonOpen")
    CmdClose.Caption = .getLabel("ButtonClose")
    End With
    
    Call Serial_GetExisting(ListExistingSerial)
    Show vbModal
    
End Sub

Private Sub Form_Unload(Cancel As Integer)
generateSciELOURL
End Sub

