VERSION 5.00
Begin VB.Form FrmInfo 
   AutoRedraw      =   -1  'True
   BorderStyle     =   1  'Fixed Single
   Caption         =   "Info"
   ClientHeight    =   5505
   ClientLeft      =   7950
   ClientTop       =   1275
   ClientWidth     =   1920
   Icon            =   "frm_FrmInfo.frx":0000
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   ScaleHeight     =   5505
   ScaleWidth      =   1920
   Begin VB.TextBox TxtHelp 
      Height          =   5295
      Left            =   120
      Locked          =   -1  'True
      MultiLine       =   -1  'True
      ScrollBars      =   2  'Vertical
      TabIndex        =   0
      Top             =   120
      Width           =   1695
   End
End
Attribute VB_Name = "FrmInfo"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Sub ShowHelpMessage(HelpText As String, Optional Position As Integer)
    'Static EnableEdition As Boolean
    
    'If EnableEdition Then
    '    EnableEdition = False
    'Else
        'EnableEdition = True
        TxtHelp.text = ReplaceString(HelpText, "vbCrlf", vbCrLf)
        'Me.Show
        'Me.SetFocus
        Select Case Position
        Case 1
            'Call FrmInfo.Move(Serial1.Left + Serial1.Width / 3, Serial1.Top + Serial1.Height / 1.5)
        Case 2
            'Call FrmInfo.Move(Serial1.Left + Serial1.Width / 3, (Serial1.Top) / 1.5)
        End Select
    'End If
End Sub


Private Sub Form_QueryUnload(Cancel As Integer, UnloadMode As Integer)
    If UnloadMode = vbFormControlMenu Then
        Cancel = 1
        'MsgBox ConfigLabels.MsgClosebyCancelorClose
    End If
End Sub

Private Sub Form_Resize()
    TxtHelp.Width = Width * 0.85
End Sub

