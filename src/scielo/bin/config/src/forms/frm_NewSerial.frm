VERSION 5.00
Begin VB.Form FrmNewSerial 
   BorderStyle     =   1  'Fixed Single
   Caption         =   "Config - New Serial"
   ClientHeight    =   5460
   ClientLeft      =   45
   ClientTop       =   330
   ClientWidth     =   7710
   Icon            =   "frm_NewSerial.frx":0000
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
      TabIndex        =   6
      Top             =   5040
      Width           =   975
   End
   Begin VB.CommandButton CmdClose 
      Caption         =   "Close"
      Height          =   375
      Left            =   6600
      TabIndex        =   5
      Top             =   5040
      Width           =   975
   End
   Begin VB.Frame FrameExistingSerial 
      Caption         =   "Existing Serial"
      Height          =   3735
      Left            =   120
      TabIndex        =   3
      Top             =   1200
      Width           =   7455
      Begin VB.ListBox ListExistingSerial 
         Height          =   3375
         Left            =   120
         Sorted          =   -1  'True
         TabIndex        =   4
         Top             =   240
         Width           =   7215
      End
   End
   Begin VB.Frame Frame1 
      Height          =   975
      Left            =   120
      TabIndex        =   0
      Top             =   120
      Width           =   7455
      Begin VB.TextBox TxtNewSerial 
         Height          =   285
         Left            =   120
         TabIndex        =   2
         Top             =   480
         Width           =   7095
      End
      Begin VB.Label LabNewSerial 
         AutoSize        =   -1  'True
         Caption         =   "New Serial"
         Height          =   195
         Left            =   120
         TabIndex        =   1
         Top             =   240
         Width           =   765
      End
   End
End
Attribute VB_Name = "FrmNewSerial"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Private Sub CmdClose_Click()
    Unload Me
End Sub

Private Sub CmdNext_Click()
    If Len(TxtNewSerial.text) > 0 Then
        'ListExistingSerial.AddItem TxtNewSerial.Text
        FrmNewSerial.Hide
        Call Serial1.MyOpenSerial(TxtNewSerial.text, True)
        'Call Serial_GetExisting(ListExistingSerial)
    Else
        MsgBox "Complete the new title."
    End If
End Sub

Sub OpenNewSerial()
    
    With ConfigLabels
    Caption = App.Title + " - " + .getLabel("NewSerial")
    LabNewSerial.Caption = .getLabel("NewSerial")
    FrameExistingSerial.Caption = .getLabel("ExistingSerial")
    CmdNext.Caption = .getLabel("ButtonOpen")
    CmdClose.Caption = .getLabel("ButtonClose")
    End With
    
    Call Serial_GetExisting(ListExistingSerial)
    Show vbModal
End Sub

Private Sub Form_Unload(Cancel As Integer)
generateSciELOURL
End Sub
