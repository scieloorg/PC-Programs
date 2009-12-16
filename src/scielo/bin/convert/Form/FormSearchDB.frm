VERSION 5.00
Begin VB.Form FormSearchDB 
   BorderStyle     =   3  'Fixed Dialog
   Caption         =   "Form1"
   ClientHeight    =   4185
   ClientLeft      =   45
   ClientTop       =   330
   ClientWidth     =   3615
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   ScaleHeight     =   4185
   ScaleWidth      =   3615
   ShowInTaskbar   =   0   'False
   StartUpPosition =   2  'CenterScreen
   Begin VB.Frame FrameId 
      Height          =   3975
      Left            =   120
      TabIndex        =   0
      Top             =   120
      Width           =   3375
      Begin VB.ComboBox ComboFolder 
         Height          =   315
         Index           =   5
         Left            =   1560
         Sorted          =   -1  'True
         Style           =   2  'Dropdown List
         TabIndex        =   16
         Top             =   2040
         Width           =   1695
      End
      Begin VB.ComboBox ComboFolder 
         Height          =   315
         Index           =   6
         Left            =   1560
         Sorted          =   -1  'True
         Style           =   2  'Dropdown List
         TabIndex        =   15
         Top             =   2400
         Width           =   1695
      End
      Begin VB.ComboBox ComboFolder 
         Height          =   315
         Index           =   7
         Left            =   1560
         Sorted          =   -1  'True
         Style           =   2  'Dropdown List
         TabIndex        =   14
         Top             =   2760
         Width           =   1695
      End
      Begin VB.TextBox TxtFolder 
         Height          =   285
         Index           =   5
         Left            =   1560
         TabIndex        =   13
         Text            =   "Text1"
         Top             =   2040
         Width           =   1695
      End
      Begin VB.ComboBox ComboFolder 
         Height          =   315
         Index           =   4
         Left            =   1560
         Sorted          =   -1  'True
         Style           =   2  'Dropdown List
         TabIndex        =   12
         Top             =   1680
         Width           =   1695
      End
      Begin VB.ComboBox ComboFolder 
         Height          =   315
         Index           =   3
         Left            =   1560
         Sorted          =   -1  'True
         Style           =   2  'Dropdown List
         TabIndex        =   11
         Top             =   1320
         Width           =   1695
      End
      Begin VB.ComboBox ComboFolder 
         Height          =   315
         Index           =   2
         Left            =   1560
         Sorted          =   -1  'True
         Style           =   2  'Dropdown List
         TabIndex        =   10
         Top             =   960
         Width           =   1695
      End
      Begin VB.ComboBox ComboFolder 
         Height          =   315
         Index           =   1
         Left            =   120
         Sorted          =   -1  'True
         Style           =   2  'Dropdown List
         TabIndex        =   9
         Top             =   240
         Width           =   3015
      End
      Begin VB.TextBox TxtFolder 
         Height          =   285
         Index           =   1
         Left            =   120
         TabIndex        =   8
         Text            =   "Text1"
         Top             =   240
         Width           =   3015
      End
      Begin VB.TextBox TxtFolder 
         Height          =   285
         Index           =   7
         Left            =   1560
         TabIndex        =   7
         Text            =   "Text1"
         Top             =   2760
         Width           =   1695
      End
      Begin VB.TextBox TxtFolder 
         Height          =   285
         Index           =   6
         Left            =   1560
         TabIndex        =   6
         Text            =   "Text1"
         Top             =   2400
         Width           =   1695
      End
      Begin VB.TextBox TxtFolder 
         Height          =   285
         Index           =   4
         Left            =   1560
         TabIndex        =   5
         Text            =   "Text1"
         Top             =   1680
         Width           =   1695
      End
      Begin VB.TextBox TxtFolder 
         Height          =   285
         Index           =   3
         Left            =   1560
         TabIndex        =   4
         Text            =   "Text1"
         Top             =   1320
         Width           =   1695
      End
      Begin VB.TextBox TxtFolder 
         Height          =   285
         Index           =   2
         Left            =   1560
         TabIndex        =   3
         Text            =   "Text1"
         Top             =   960
         Width           =   1695
      End
      Begin VB.CommandButton CmdSearch 
         Caption         =   "Command1"
         Height          =   495
         Left            =   600
         TabIndex        =   2
         Top             =   3360
         Width           =   975
      End
      Begin VB.CommandButton CmdCancel 
         Caption         =   "Command1"
         Height          =   495
         Left            =   1680
         TabIndex        =   1
         Top             =   3360
         Width           =   975
      End
      Begin VB.Label LabFolder 
         Alignment       =   1  'Right Justify
         Caption         =   "label"
         Height          =   375
         Index           =   7
         Left            =   120
         TabIndex        =   23
         Top             =   2760
         Width           =   1335
      End
      Begin VB.Label LabFolder 
         Alignment       =   1  'Right Justify
         Caption         =   "Label1"
         Height          =   255
         Index           =   3
         Left            =   120
         TabIndex        =   22
         Top             =   1320
         Width           =   1335
      End
      Begin VB.Label LabFolder 
         AutoSize        =   -1  'True
         Caption         =   "Label1"
         Height          =   195
         Index           =   1
         Left            =   120
         TabIndex        =   21
         Top             =   0
         Width           =   480
      End
      Begin VB.Label LabFolder 
         Alignment       =   1  'Right Justify
         Caption         =   "Label1"
         Height          =   375
         Index           =   2
         Left            =   120
         TabIndex        =   20
         Top             =   960
         Width           =   1335
      End
      Begin VB.Label LabFolder 
         Alignment       =   1  'Right Justify
         Caption         =   "Label1"
         Height          =   255
         Index           =   4
         Left            =   120
         TabIndex        =   19
         Top             =   1680
         Width           =   1335
      End
      Begin VB.Label LabFolder 
         Alignment       =   1  'Right Justify
         Caption         =   "Label1"
         Height          =   255
         Index           =   5
         Left            =   120
         TabIndex        =   18
         Top             =   2040
         Width           =   1335
      End
      Begin VB.Label LabFolder 
         Alignment       =   1  'Right Justify
         Caption         =   "label"
         Height          =   255
         Index           =   6
         Left            =   120
         TabIndex        =   17
         Top             =   2400
         Width           =   1335
      End
   End
End
Attribute VB_Name = "FormSearchDB"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private Const TextBoxCounter = 7

Private SearchExpr As String
Private result As Boolean

Function ReturnSearchExpression(SearchExprResult) As Boolean
    SearchExpr = ""
    SearchExprResult = ""
    OpenForm
    If Len(SearchExpr) > 0 Then SearchExprResult = "if " + SearchExpr + " then mfn fi"
    ReturnSearchExpression = result
End Function
Private Sub OpenForm()
    SetLabels
    Components_Show
    Call Components_View(True)
    Show vbModal
End Sub
Private Sub SetLabels()
    Caption = InterfaceLabels("formsearch_caption").elem2
    CmdSearch.Caption = InterfaceLabels("CmdFind").elem2
    CmdCancel.Caption = InterfaceLabels("CmdCancel").elem2
End Sub
Private Sub Components_Show()
    Dim i As Long
    Dim j As Long
    Dim q As Long
    
    
    With BV(Currbv)
    q = .SearchOptions.Count
    For i = 1 To q
        LabFolder(i).Caption = InterfaceLabels(.SearchOptions(i).LabelKey).elem2
        
        Select Case .SearchOptions(i).ComponentType
        Case "combo"
            ComboFolder(i).Clear
            For j = 1 To .Directory(.SearchOptions(i).ValueListId).ContentListAbbr.Count
                ComboFolder(i).AddItem (.Directory(.SearchOptions(i).ValueListId).ContentListAbbr(j).elem2)
            Next
            ComboFolder(i).AddItem ("")
            ComboFolder(i).ListIndex = 0
        Case "text"
            TxtFolder(i).Enabled = True
        Case "label"
            TxtFolder(i).Enabled = False
        End Select
    Next
    End With
End Sub

Private Sub Components_View(Flag As Boolean)
    Dim i As Long
    Dim j As Long
    Dim q As Long
    
    
    With BV(Currbv)
    q = .SearchOptions.Count
    While i < q
        i = i + 1
        Select Case .SearchOptions(i).ComponentType
        Case "combo"
            ComboFolder(i).Visible = Flag
            TxtFolder(i).Visible = Not Flag
        Case "text", "label"
            ComboFolder(i).Visible = Not Flag
            TxtFolder(i).Visible = Flag
            TxtFolder(i).Text = ""
        End Select
    Wend
    While i < TextBoxCounter
        i = i + 1
        ComboFolder(i).Visible = Not Flag
        TxtFolder(i).Visible = Not Flag
        LabFolder(i).Visible = Not Flag
    Wend
    End With
End Sub


Private Sub CmdCancel_Click()
    result = False
    Unload Me
End Sub

Private Sub CmdSearch_Click()
    Dim i As Long
    Dim Value As String
    
    With BV(Currbv)
    For i = 1 To .SearchOptions.Count
        Value = ""
        Select Case .SearchOptions(i).ComponentType
        Case "combo"
            If Len(ComboFolder(i).Text) > 0 Then Value = .Directory(.SearchOptions(i).ValueListId).ContentListFull(ComboFolder(i).Text).elem2
        Case "text", "label"
            Value = TxtFolder(i).Text
        Case Else
            Value = ""
        End Select
        If Len(Value) > 0 Then
            Value = .SearchOptions(i).GetCompareExpression(Value, Len(Value))
            If Len(SearchExpr) = 0 Then
                SearchExpr = Value
            Else
                SearchExpr = SearchExpr + " and " + Value
            End If
        End If
    Next
    End With
    result = True
    Unload Me
End Sub

