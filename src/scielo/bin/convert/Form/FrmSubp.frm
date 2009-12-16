VERSION 5.00
Object = "{6B7E6392-850A-101B-AFC0-4210102A8DA7}#1.3#0"; "COMCTL32.OCX"
Begin VB.Form FrmSubp 
   Caption         =   "Subscript/Supscript Transcription"
   ClientHeight    =   6330
   ClientLeft      =   60
   ClientTop       =   345
   ClientWidth     =   6810
   Icon            =   "FrmSubp.frx":0000
   LinkTopic       =   "Form1"
   ScaleHeight     =   6330
   ScaleWidth      =   6810
   StartUpPosition =   2  'CenterScreen
   Begin ComctlLib.ListView ListViewImg 
      Height          =   3255
      Left            =   120
      TabIndex        =   12
      Top             =   2520
      Width           =   6615
      _ExtentX        =   11668
      _ExtentY        =   5741
      View            =   3
      LabelWrap       =   0   'False
      HideSelection   =   -1  'True
      _Version        =   327682
      ForeColor       =   -2147483640
      BackColor       =   -2147483643
      BorderStyle     =   1
      Appearance      =   1
      NumItems        =   3
      BeginProperty ColumnHeader(1) {0713E8C7-850A-101B-AFC0-4210102A8DA7} 
         Key             =   "tagsubp"
         Object.Tag             =   "tagtagsubp"
         Text            =   "SUB/SUP"
         Object.Width           =   2540
      EndProperty
      BeginProperty ColumnHeader(2) {0713E8C7-850A-101B-AFC0-4210102A8DA7} 
         SubItemIndex    =   1
         Key             =   ""
         Object.Tag             =   ""
         Text            =   "Replace"
         Object.Width           =   2540
      EndProperty
      BeginProperty ColumnHeader(3) {0713E8C7-850A-101B-AFC0-4210102A8DA7} 
         SubItemIndex    =   2
         Key             =   ""
         Object.Tag             =   ""
         Text            =   "Context"
         Object.Width           =   2540
      EndProperty
   End
   Begin VB.CommandButton CmdCancel 
      Caption         =   "Cancel"
      Height          =   375
      Left            =   5640
      TabIndex        =   4
      Top             =   5880
      Width           =   1095
   End
   Begin VB.CommandButton CmdOk 
      Caption         =   "OK"
      Height          =   375
      Left            =   4440
      TabIndex        =   3
      Top             =   5880
      Width           =   1095
   End
   Begin VB.Frame Frame1 
      Height          =   2295
      Left            =   120
      TabIndex        =   8
      Top             =   120
      Width           =   6615
      Begin VB.TextBox TxtSubp 
         Height          =   375
         Left            =   120
         TabIndex        =   13
         Top             =   480
         Width           =   6375
      End
      Begin VB.CommandButton CmdFirst 
         Caption         =   "| <"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   13.5
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   495
         Left            =   240
         TabIndex        =   5
         Top             =   1680
         Width           =   735
      End
      Begin VB.CommandButton CmdPrevious 
         Caption         =   "<"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   13.5
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   495
         Left            =   960
         TabIndex        =   6
         Top             =   1680
         Width           =   735
      End
      Begin VB.CommandButton CmdNext 
         Caption         =   ">"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   13.5
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   495
         Left            =   1680
         TabIndex        =   2
         Top             =   1680
         Width           =   735
      End
      Begin VB.CommandButton CmdLast 
         Caption         =   "> |"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   13.5
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   495
         Left            =   2400
         TabIndex        =   7
         Top             =   1680
         Width           =   735
      End
      Begin VB.TextBox TxtReplace 
         Height          =   375
         Left            =   120
         TabIndex        =   0
         Top             =   1200
         Width           =   6375
      End
      Begin VB.CommandButton CmdReplace 
         Caption         =   "Replace "
         Height          =   495
         Left            =   5520
         TabIndex        =   1
         Top             =   1680
         Width           =   975
      End
      Begin VB.Label LabImg 
         AutoSize        =   -1  'True
         Caption         =   "Subscript and/or Supscript"
         Height          =   195
         Left            =   120
         TabIndex        =   11
         Top             =   240
         Width           =   1890
      End
      Begin VB.Label LabTranslation 
         AutoSize        =   -1  'True
         Caption         =   "Replace image with"
         Height          =   195
         Left            =   120
         TabIndex        =   10
         Top             =   960
         Width           =   1395
      End
      Begin VB.Label LabIndex 
         AutoSize        =   -1  'True
         Caption         =   "1/1"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   18
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   435
         Left            =   4080
         TabIndex        =   9
         Top             =   1680
         Width           =   555
      End
   End
End
Attribute VB_Name = "FrmSubp"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Private SUBSUP_tag() As String
Private SUBSUPContext() As String
Private SUBSUPRepl() As String
Private SUBSUPCount As Long
Private mvarCurrSUBSUPIdx As Long
Private OKChoice As Boolean

Property Let CurrSUBSUPIdx(idx As Long)
    If (idx > 0) And (idx <= SUBSUPCount) Then
        TxtSubp.Text = SUBSUP_tag(idx)
        TxtReplace.Text = SUBSUPRepl(idx)
        mvarCurrSUBSUPIdx = idx
        LabIndex.Caption = CStr(idx) + PathSepUnix + CStr(SUBSUPCount)
    End If
End Property
Property Get CurrSUBSUPIdx() As Long
    CurrSUBSUPIdx = mvarCurrSUBSUPIdx
End Property

Private Sub CmdCancel_Click()
    Dim i As Long
    Dim ok As Boolean
    Dim r As VbMsgBoxResult
    
    r = MsgBox("Are you sure you want to cancel?", vbYesNo + vbDefaultButton2)
    If r = vbYes Then
        Hide
    ElseIf r = vbNo Then
    
    End If
    OKChoice = False
End Sub

Private Sub CmdFirst_Click()
    CurrSUBSUPIdx = 1
End Sub

Private Sub CmdLast_Click()
    CurrSUBSUPIdx = SUBSUPCount
End Sub

Private Sub CmdNext_Click()
    CurrSUBSUPIdx = CurrSUBSUPIdx + 1
End Sub

Private Sub cmdOK_Click()
    Dim i As Long
    Dim ok As Boolean
    Dim r As VbMsgBoxResult
    
    ok = True
    For i = 1 To SUBSUPCount
        If Len(SUBSUPRepl(i)) = 0 Then
            ok = False
            MsgBox "Invalid replace value to TAGSUBSUP " + CStr(i) + ". They will not be replaced."
        End If
    Next
    
    If ok Then
        Hide
    Else
        r = MsgBox("Do you want to complete the missing TAGSUBSUPs?", vbYesNo + vbDefaultButton1)
        If r = vbYes Then
        ElseIf r = vbNo Then
            Hide
        End If
    End If
    OKChoice = True
End Sub

Private Sub CmdPrevious_Click()
    CurrSUBSUPIdx = CurrSUBSUPIdx - 1
End Sub

Private Sub CmdReplace_Click()
    SUBSUP_tag(CurrSUBSUPIdx) = TxtSubp.Text
    SUBSUPRepl(CurrSUBSUPIdx) = TxtReplace.Text
    ListTAGSUBSUPs
End Sub

Sub setTAGSUBSUPs(TAGSUBSUP() As String, TAGSUBSUPReplace() As String, TAGSUBSUPContext() As String, TAGSUBSUPCounter As Long)
    Dim i As Long
    Dim k As String
        
    
    OKChoice = False
    SUBSUPCount = TAGSUBSUPCounter
    ReDim SUBSUP_tag(SUBSUPCount)
    ReDim SUBSUPContext(SUBSUPCount)
    ReDim SUBSUPRepl(SUBSUPCount)
    For i = 1 To TAGSUBSUPCounter
        SUBSUP_tag(i) = TAGSUBSUP(i)
        SUBSUPRepl(i) = TAGSUBSUPReplace(i)
        SUBSUPContext(i) = TAGSUBSUPContext(i)
    Next
    CurrSUBSUPIdx = 1
    
    ListTAGSUBSUPs
    
    Show vbModal
    
    If OKChoice Then
        TAGSUBSUPCounter = 0
        For i = 1 To SUBSUPCount
            If Len(SUBSUPRepl(i)) > 0 Then
                TAGSUBSUPCounter = TAGSUBSUPCounter + 1
                ReDim Preserve TAGSUBSUP(TAGSUBSUPCounter)
                ReDim Preserve TAGSUBSUPReplace(TAGSUBSUPCounter)
                
                TAGSUBSUPReplace(TAGSUBSUPCounter) = SUBSUPRepl(i)
                TAGSUBSUP(TAGSUBSUPCounter) = SUBSUP_tag(i)
                
            End If
        Next
    End If
    Unload Me
End Sub


Sub ListTAGSUBSUPs()
    Dim i As Long
    Dim k As ListItem
    
    ListViewImg.ListItems.Clear
    For i = 1 To SUBSUPCount
        Set k = ListViewImg.ListItems.Add(, , SUBSUP_tag(i))
        k.SubItems(1) = SUBSUPRepl(i)
        k.SubItems(2) = SUBSUPContext(i)
    Next
    
End Sub


Private Sub ListViewSUBSUP_BeforeLabelEdit(Cancel As Integer)
    Cancel = True
End Sub

Private Sub ListViewImg_ItemClick(ByVal Item As ComctlLib.ListItem)
    CurrSUBSUPIdx = Item.Index
End Sub
