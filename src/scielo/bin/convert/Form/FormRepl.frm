VERSION 5.00
Begin VB.Form FormRepl 
   Caption         =   "Replace"
   ClientHeight    =   4740
   ClientLeft      =   60
   ClientTop       =   345
   ClientWidth     =   7335
   LinkTopic       =   "Form1"
   ScaleHeight     =   4740
   ScaleWidth      =   7335
   StartUpPosition =   2  'CenterScreen
   Begin VB.TextBox TxtDocName 
      Height          =   285
      Left            =   120
      Locked          =   -1  'True
      TabIndex        =   10
      Top             =   480
      Width           =   2175
   End
   Begin VB.CommandButton CmdFindNext 
      Caption         =   "Find Next"
      Height          =   375
      Left            =   1440
      TabIndex        =   6
      Top             =   4200
      Width           =   1215
   End
   Begin VB.TextBox TxtEnd 
      BackColor       =   &H00FFFFFF&
      ForeColor       =   &H00000000&
      Height          =   735
      Left            =   120
      Locked          =   -1  'True
      MultiLine       =   -1  'True
      ScrollBars      =   2  'Vertical
      TabIndex        =   5
      Top             =   2400
      Width           =   7095
   End
   Begin VB.TextBox TxtMiddle 
      BackColor       =   &H80000000&
      ForeColor       =   &H000000FF&
      Height          =   495
      Left            =   120
      Locked          =   -1  'True
      MultiLine       =   -1  'True
      TabIndex        =   4
      Top             =   1920
      Width           =   7095
   End
   Begin VB.TextBox TxtRepl 
      Height          =   435
      Left            =   120
      TabIndex        =   0
      Top             =   3600
      Width           =   3855
   End
   Begin VB.CommandButton CmdUndo 
      Caption         =   "Undo"
      Height          =   375
      Left            =   2760
      TabIndex        =   7
      Top             =   4200
      Width           =   1215
   End
   Begin VB.CommandButton CmdReplace 
      Caption         =   "Replace"
      Height          =   375
      Left            =   120
      TabIndex        =   1
      Top             =   4200
      Width           =   1215
   End
   Begin VB.TextBox TxtStart 
      Height          =   735
      Left            =   120
      Locked          =   -1  'True
      MultiLine       =   -1  'True
      ScrollBars      =   2  'Vertical
      TabIndex        =   3
      Top             =   1200
      Width           =   7095
   End
   Begin VB.Label LabDocName 
      Caption         =   "Document Name"
      Height          =   255
      Left            =   120
      TabIndex        =   9
      Top             =   240
      Width           =   1215
   End
   Begin VB.Label Label2 
      Caption         =   "Replace with"
      Height          =   255
      Left            =   120
      TabIndex        =   8
      Top             =   3360
      Width           =   1575
   End
   Begin VB.Label LabField 
      Caption         =   "Field"
      Height          =   255
      Left            =   120
      TabIndex        =   2
      Top             =   960
      Width           =   1215
   End
End
Attribute VB_Name = "FormRepl"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private InitPos As Long
Private new_content As String

Private Sub CmdFindNext_Click()
    If Not FindNext(TxtStart.Text + TxtMiddle.Text + TxtEnd.Text) Then
        Unload Me
    End If
End Sub

Private Sub CmdReplace_Click()
    If Len(TxtRepl.Text) > 0 Then
        TxtMiddle.Text = TxtRepl.Text
        new_content = TxtStart.Text + TxtRepl.Text + TxtEnd.Text
        If Not FindNext(new_content) Then
            Unload Me
        End If
    End If
End Sub

Function Replace(Tag As Long, content As String) As String
    
    Select Case Tag
    Case 12, 18
        LabField.Caption = "title"
    Case 10, 16, 11, 17
        LabField.Caption = "author"
    Case 30
        LabField.Caption = "sertitle/stitle"
    Case 83
        LabField.Caption = "abstract"
    Case 85
        LabField.Caption = "keyword"
    Case Else
        LabField.Caption = "field " + CStr(Tag)
    End Select
    
    InitPos = 1
    new_content = content
    If FindNext(content) Then
        FormRepl.Show vbModal
    Else
        Unload Me
    End If
    Replace = new_content
    
End Function

Function FindNext(content As String) As Boolean
    Dim plt1 As Long
    Dim plt2 As Long
    Dim pgt1 As Long
    Dim pgt2 As Long
    Dim HTMLTag As String
    Dim found As Boolean
    
    
    plt1 = InStr(InitPos, content, "<")
    If (plt1 > 0) Then
        pgt1 = InStr(plt1, content, ">", vbTextCompare)
        HTMLTag = Mid(content, plt1 + 1, pgt1 - plt1 - 1)
        If InStr(1, HTMLTag, "img", vbTextCompare) = 1 Then
            plt2 = plt1
        ElseIf InStr(1, HTMLTag, "font", vbTextCompare) = 1 Then
            plt2 = InStr(pgt1, content, "</font>", vbTextCompare)
        Else
            plt2 = InStr(pgt1, content, "</" + HTMLTag + ">", vbTextCompare)
        End If
        pgt2 = InStr(plt2, content, ">", vbTextCompare)
        TxtStart.Text = Mid(content, 1, plt1 - 1)
        TxtMiddle.Text = Mid(content, plt1, pgt2 - plt1 + 1)
        TxtEnd.Text = Mid(content, pgt2 + 1)
        TxtRepl.Text = ""
        
        InitPos = plt1 + 1
        found = True
    End If
    
    FindNext = found
End Function

