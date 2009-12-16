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
   StartUpPosition =   3  'Windows Default
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
      TabIndex        =   3
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
      TabIndex        =   8
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
      TabIndex        =   7
      Top             =   1920
      Width           =   7095
   End
   Begin VB.TextBox TxtRepl 
      Height          =   435
      Left            =   120
      TabIndex        =   1
      Top             =   3600
      Width           =   3855
   End
   Begin VB.CommandButton CmdUndo 
      Caption         =   "Undo"
      Height          =   375
      Left            =   2760
      TabIndex        =   4
      Top             =   4200
      Width           =   1215
   End
   Begin VB.CommandButton CmdReplace 
      Caption         =   "Replace"
      Height          =   375
      Left            =   120
      TabIndex        =   2
      Top             =   4200
      Width           =   1215
   End
   Begin VB.TextBox TxtStart 
      Height          =   735
      Left            =   120
      Locked          =   -1  'True
      MultiLine       =   -1  'True
      TabIndex        =   5
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
      TabIndex        =   6
      Top             =   3360
      Width           =   1575
   End
   Begin VB.Label LabField 
      Caption         =   "Field"
      Height          =   255
      Left            =   120
      TabIndex        =   0
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

Private Sub CmdFindNext_Click()
    Dim StartText As String
    Dim EndText As String
    
    TxtMiddle.Text = FindNext(content, StartText, EndText)
    TxtStart.Text = StartText
    TxtEnd.Text = EndText
End Sub

Private Sub CmdReplace_Click()
    Dim content As String
    Dim StartText As String
    Dim EndText As String
    Dim MiddleText As String
    
    If Len(TxtRepl.Text) > 0 Then
        TxtMiddle.Text = TxtRepl.Text
        content = TxtStart.Text + TxtRepl.Text + TxtEnd.Text
        MiddleText = FindNext(content, StartText, EndText)
        If Len(MiddleText) > 0 Then
            TxtMiddle.Text = MiddleText
            TxtStart.Text = StartText
            TxtEnd.Text = EndText
        End If
    End If
End Sub

Private Sub Form_Load()

End Sub

Function Replace(Tag As Long, content As String) As String
    Dim StartText As String
    Dim EndText As String
    
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
    
    TxtMiddle.Text = FindNext(content, StartText, EndText)
    TxtStart.Text = StartText
    TxtEnd.Text = EndText
        
    If Len(TxtMiddle.Text) > 0 Then
        FormRepl.Show vbModal
        
    End If
    
    
End Function

Function FindNext(content As String, StartText As String, EndText As String) As String
    Dim plt1 As Long
    Dim plt2 As Long
    Dim pgt1 As Long
    Dim pgt2 As Long
    Dim HTMLTag As String
    Dim FindWhat As String
    
    
    plt1 = InStr(InitPos, content, "<")
    If (plt1 > 0) Then
        pgt1 = InStr(plt1, content, ">", vbTextCompare)
        HTMLTag = Mid(content, plt1 + 1, pgt1 - plt1 - 1)
        If InStr(1, HTMLTag, "<img", vbTextCompare) > 0 Then
            plt2 = plt1
        ElseIf InStr(HTMLTag, "<font", vbTextCompare) > 0 Then
            plt2 = InStr(pgt1, content, "</font>", vbTextCompare)
        Else
            plt2 = InStr(pgt1, content, "</" + HTMLTag + ">", vbTextCompare)
        End If
        pgt2 = InStr(plt2, content, ">", vbTextCompare)
        
        StartText = Mid(content, 1, plt1 - 1)
        FindWhat = Mid(content, plt1, pgt2 - plt1 + 1)
        EndText = Mid(content, pgt2 + 1)
        
        InitPos = pgt2 + 1
    End If
    
    FindNext = FindWhat
End Function

