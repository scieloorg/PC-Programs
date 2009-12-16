VERSION 5.00
Begin VB.Form FrmRmSerial 
   BorderStyle     =   1  'Fixed Single
   Caption         =   "Config - Remove Serial"
   ClientHeight    =   5460
   ClientLeft      =   45
   ClientTop       =   330
   ClientWidth     =   7710
   Icon            =   "frm_RmSerial.frx":0000
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   Moveable        =   0   'False
   ScaleHeight     =   5460
   ScaleWidth      =   7710
   StartUpPosition =   2  'CenterScreen
   Begin VB.CommandButton CmdRem 
      Caption         =   "Next"
      Height          =   375
      Left            =   5400
      TabIndex        =   3
      Top             =   5040
      Width           =   975
   End
   Begin VB.CommandButton CmdClose 
      Caption         =   "Cancel"
      Height          =   375
      Left            =   6600
      TabIndex        =   2
      Top             =   5040
      Width           =   975
   End
   Begin VB.Frame FrameRmSerial 
      Caption         =   "Select the serials to remove"
      Height          =   4815
      Left            =   120
      TabIndex        =   0
      Top             =   120
      Width           =   7455
      Begin VB.ListBox ListExistingSerial 
         Height          =   4110
         Left            =   120
         Sorted          =   -1  'True
         Style           =   1  'Checkbox
         TabIndex        =   1
         Top             =   360
         Width           =   7215
      End
   End
End
Attribute VB_Name = "FrmRmSerial"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Private Sub CmdClose_Click()
    Unload Me
End Sub

Sub OpenExistingSerial()
    
    With ConfigLabels
    Caption = App.Title + " - " + .getLabel("mnRemoveSerial")
    FrameRmSerial.Caption = .getLabel("Select_to_Remove")
    CmdRem.Caption = .getLabel("ButtonRemove")
    CmdClose.Caption = .getLabel("ButtonClose")
    End With
    
    Call Serial_GetExisting(ListExistingSerial)
    Show vbModal
End Sub

Private Sub Cmdrem_Click()
    Dim i As Long
    Dim mfns() As Long
    Dim q As Long
    Dim issn As String
    
    If ListExistingSerial.SelCount = 0 Then
        MsgBox ConfigLabels.getLabel("Select_to_Open")
    Else
        MousePointer = vbHourglass
        
        For i = 0 To ListExistingSerial.ListCount - 1
            If ListExistingSerial.selected(i) Then
                ListExistingSerial.selected(i) = False
                If MsgBox(ConfigLabels.getLabel("MsgRemoveSerial") + " " + ListExistingSerial.list(i) + "?", vbYesNo + vbDefaultButton2) = vbYes Then
                    issn = ListExistingSerial.list(i)
                    issn = Mid(issn, InStr(issn, "[") + 1, 9)
                    journalDAO.delete (issn)
                End If
           
            End If
        Next
        
        Call Serial_GetExisting(ListExistingSerial)
        MousePointer = vbArrow
    End If
End Sub

