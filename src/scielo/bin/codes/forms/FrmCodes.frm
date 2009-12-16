VERSION 5.00
Object = "{BDC217C8-ED16-11CD-956C-0000C04E4C0A}#1.1#0"; "TABCTL32.OCX"
Begin VB.Form FrmCodes 
   BorderStyle     =   3  'Fixed Dialog
   Caption         =   "Codes"
   ClientHeight    =   5925
   ClientLeft      =   45
   ClientTop       =   330
   ClientWidth     =   8145
   Icon            =   "FrmCodes.frx":0000
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   ScaleHeight     =   5925
   ScaleWidth      =   8145
   ShowInTaskbar   =   0   'False
   StartUpPosition =   2  'CenterScreen
   Begin VB.CommandButton CmdHelp 
      Caption         =   "Command4"
      Height          =   375
      Left            =   5880
      TabIndex        =   26
      Top             =   5520
      Width           =   975
   End
   Begin VB.CommandButton CmdClose 
      Caption         =   "Command3"
      Height          =   375
      Left            =   6960
      TabIndex        =   27
      Top             =   5520
      Width           =   975
   End
   Begin TabDlg.SSTab SSTab1 
      Height          =   5295
      Left            =   120
      TabIndex        =   28
      Top             =   120
      Width           =   7935
      _ExtentX        =   13996
      _ExtentY        =   9340
      _Version        =   393216
      TabHeight       =   520
      TabCaption(0)   =   "ccode"
      TabPicture(0)   =   "FrmCodes.frx":030A
      Tab(0).ControlEnabled=   -1  'True
      Tab(0).Control(0)=   "CcodeToFill"
      Tab(0).Control(0).Enabled=   0   'False
      Tab(0).Control(1)=   "FilledCCode"
      Tab(0).Control(1).Enabled=   0   'False
      Tab(0).ControlCount=   2
      TabCaption(1)   =   "sponsor"
      TabPicture(1)   =   "FrmCodes.frx":0326
      Tab(1).ControlEnabled=   0   'False
      Tab(1).Control(0)=   "FilledSponsor"
      Tab(1).Control(0).Enabled=   0   'False
      Tab(1).Control(1)=   "SponsorToFill"
      Tab(1).Control(1).Enabled=   0   'False
      Tab(1).ControlCount=   2
      TabCaption(2)   =   "study area"
      TabPicture(2)   =   "FrmCodes.frx":0342
      Tab(2).ControlEnabled=   0   'False
      Tab(2).Control(0)=   "StudyAreaToFill"
      Tab(2).Control(0).Enabled=   0   'False
      Tab(2).Control(1)=   "FilledStudyArea"
      Tab(2).Control(1).Enabled=   0   'False
      Tab(2).ControlCount=   2
      Begin VB.Frame FilledSponsor 
         Caption         =   "Frame2"
         Height          =   3015
         Left            =   -74880
         TabIndex        =   39
         Top             =   480
         Width           =   7695
         Begin VB.ListBox ListSponsor 
            Height          =   2400
            Index           =   2
            Left            =   2640
            Sorted          =   -1  'True
            TabIndex        =   7
            Top             =   480
            Width           =   2415
         End
         Begin VB.ListBox ListSponsor 
            Height          =   2400
            Index           =   3
            Left            =   5160
            Sorted          =   -1  'True
            TabIndex        =   8
            Top             =   480
            Width           =   2415
         End
         Begin VB.ListBox ListSponsor 
            Height          =   2400
            Index           =   1
            Left            =   120
            Sorted          =   -1  'True
            TabIndex        =   6
            Top             =   480
            Width           =   2415
         End
         Begin VB.Label LabIdiomSponsor 
            Caption         =   "Label3"
            Height          =   255
            Index           =   2
            Left            =   2640
            TabIndex        =   42
            Top             =   240
            Width           =   2055
         End
         Begin VB.Label LabIdiomSponsor 
            Caption         =   "Label3"
            Height          =   255
            Index           =   3
            Left            =   5160
            TabIndex        =   41
            Top             =   240
            Width           =   2055
         End
         Begin VB.Label LabIdiomSponsor 
            Caption         =   "Label3"
            Height          =   255
            Index           =   1
            Left            =   120
            TabIndex        =   40
            Top             =   240
            Width           =   2055
         End
      End
      Begin VB.Frame SponsorToFill 
         Caption         =   "Frame1"
         Height          =   1575
         Left            =   -74880
         TabIndex        =   38
         Top             =   3600
         Width           =   7695
         Begin VB.TextBox TxtValSponsor 
            Height          =   285
            Index           =   3
            Left            =   5160
            TabIndex        =   12
            Text            =   "Text2"
            Top             =   1200
            Width           =   2415
         End
         Begin VB.TextBox TxtValSponsor 
            Height          =   285
            Index           =   2
            Left            =   2640
            TabIndex        =   11
            Text            =   "Text2"
            Top             =   1200
            Width           =   2415
         End
         Begin VB.CommandButton CmdSave 
            Caption         =   "Command3"
            Height          =   375
            Index           =   1
            Left            =   6600
            TabIndex        =   15
            Top             =   360
            Width           =   975
         End
         Begin VB.CommandButton CmdDel 
            Caption         =   "Command2"
            Height          =   375
            Index           =   1
            Left            =   5520
            TabIndex        =   14
            Top             =   360
            Width           =   975
         End
         Begin VB.CommandButton CmdNew 
            Caption         =   "Command1"
            Height          =   375
            Index           =   1
            Left            =   4440
            TabIndex        =   13
            Top             =   360
            Width           =   975
         End
         Begin VB.TextBox TxtCodeSponsor 
            Height          =   285
            Left            =   120
            TabIndex        =   9
            Text            =   "Text1"
            Top             =   480
            Width           =   3735
         End
         Begin VB.TextBox TxtValSponsor 
            Height          =   285
            Index           =   1
            Left            =   120
            TabIndex        =   10
            Text            =   "Text2"
            Top             =   1200
            Width           =   2415
         End
         Begin VB.Label LabIdiomSponsorEdit 
            Caption         =   "Label3"
            Height          =   255
            Index           =   3
            Left            =   5160
            TabIndex        =   47
            Top             =   960
            Width           =   2055
         End
         Begin VB.Label LabIdiomSponsorEdit 
            Caption         =   "Label3"
            Height          =   255
            Index           =   2
            Left            =   2640
            TabIndex        =   46
            Top             =   960
            Width           =   2055
         End
         Begin VB.Label LabIdiomSponsorEdit 
            Caption         =   "Label3"
            Height          =   255
            Index           =   1
            Left            =   120
            TabIndex        =   45
            Top             =   960
            Width           =   2055
         End
         Begin VB.Label labCode 
            Caption         =   "Label1"
            Height          =   255
            Index           =   1
            Left            =   120
            TabIndex        =   44
            Top             =   240
            Width           =   1455
         End
      End
      Begin VB.Frame StudyAreaToFill 
         Caption         =   "Frame1"
         Height          =   1575
         Left            =   -74880
         TabIndex        =   34
         Top             =   3600
         Width           =   7695
         Begin VB.TextBox TxtValStudyArea 
            Height          =   285
            Index           =   3
            Left            =   5160
            TabIndex        =   22
            Text            =   "Text2"
            Top             =   1200
            Width           =   2415
         End
         Begin VB.TextBox TxtValStudyArea 
            Height          =   285
            Index           =   2
            Left            =   2640
            TabIndex        =   21
            Text            =   "Text2"
            Top             =   1200
            Width           =   2415
         End
         Begin VB.TextBox TxtValStudyArea 
            Height          =   285
            Index           =   1
            Left            =   120
            TabIndex        =   20
            Text            =   "Text2"
            Top             =   1200
            Width           =   2415
         End
         Begin VB.TextBox TxtCodeStudyArea 
            Height          =   285
            Left            =   120
            TabIndex        =   19
            Text            =   "Text1"
            Top             =   480
            Width           =   3735
         End
         Begin VB.CommandButton CmdNew 
            Caption         =   "Command1"
            Height          =   375
            Index           =   2
            Left            =   4440
            TabIndex        =   23
            Top             =   360
            Width           =   975
         End
         Begin VB.CommandButton CmdDel 
            Caption         =   "Command2"
            Height          =   375
            Index           =   2
            Left            =   5520
            TabIndex        =   24
            Top             =   360
            Width           =   975
         End
         Begin VB.CommandButton CmdSave 
            Caption         =   "Command3"
            Height          =   375
            Index           =   2
            Left            =   6600
            TabIndex        =   25
            Top             =   360
            Width           =   975
         End
         Begin VB.Label LabIdiomEdit 
            Caption         =   "Label3"
            Height          =   255
            Index           =   3
            Left            =   5160
            TabIndex        =   50
            Top             =   960
            Width           =   2055
         End
         Begin VB.Label LabIdiomEdit 
            Caption         =   "Label3"
            Height          =   255
            Index           =   2
            Left            =   2640
            TabIndex        =   49
            Top             =   960
            Width           =   2055
         End
         Begin VB.Label LabIdiomEdit 
            Caption         =   "Label3"
            Height          =   255
            Index           =   1
            Left            =   120
            TabIndex        =   48
            Top             =   960
            Width           =   2055
         End
         Begin VB.Label labCode 
            Caption         =   "Label1"
            Height          =   255
            Index           =   2
            Left            =   120
            TabIndex        =   43
            Top             =   240
            Width           =   1455
         End
      End
      Begin VB.Frame FilledStudyArea 
         Caption         =   "Frame2"
         Height          =   3015
         Left            =   -74880
         TabIndex        =   33
         Top             =   480
         Width           =   7695
         Begin VB.ListBox ListStudyArea 
            Height          =   2400
            Index           =   3
            Left            =   5160
            Sorted          =   -1  'True
            TabIndex        =   18
            Top             =   480
            Width           =   2415
         End
         Begin VB.ListBox ListStudyArea 
            Height          =   2400
            Index           =   2
            Left            =   2640
            Sorted          =   -1  'True
            TabIndex        =   17
            Top             =   480
            Width           =   2415
         End
         Begin VB.ListBox ListStudyArea 
            Height          =   2400
            Index           =   1
            Left            =   120
            Sorted          =   -1  'True
            TabIndex        =   16
            Top             =   480
            Width           =   2415
         End
         Begin VB.Label LabIdiom 
            Caption         =   "Label3"
            Height          =   255
            Index           =   3
            Left            =   5160
            TabIndex        =   37
            Top             =   240
            Width           =   2055
         End
         Begin VB.Label LabIdiom 
            Caption         =   "Label3"
            Height          =   255
            Index           =   2
            Left            =   2640
            TabIndex        =   36
            Top             =   240
            Width           =   2055
         End
         Begin VB.Label LabIdiom 
            Caption         =   "Label3"
            Height          =   255
            Index           =   1
            Left            =   120
            TabIndex        =   35
            Top             =   240
            Width           =   2055
         End
      End
      Begin VB.Frame FilledCCode 
         Caption         =   "Frame2"
         Height          =   3015
         Left            =   120
         TabIndex        =   30
         Top             =   480
         Width           =   7695
         Begin VB.ListBox ListFilledCCode 
            Height          =   2400
            Left            =   120
            Sorted          =   -1  'True
            TabIndex        =   0
            Top             =   360
            Width           =   7455
         End
      End
      Begin VB.Frame CcodeToFill 
         Caption         =   "Frame1"
         Height          =   1575
         Left            =   120
         TabIndex        =   29
         Top             =   3600
         Width           =   7695
         Begin VB.CommandButton CmdSave 
            Caption         =   "Command3"
            Height          =   375
            Index           =   0
            Left            =   2280
            TabIndex        =   5
            Top             =   1080
            Width           =   975
         End
         Begin VB.CommandButton CmdDel 
            Caption         =   "Command2"
            Height          =   375
            Index           =   0
            Left            =   1200
            TabIndex        =   4
            Top             =   1080
            Width           =   975
         End
         Begin VB.CommandButton CmdNew 
            Caption         =   "Command1"
            Height          =   375
            Index           =   0
            Left            =   120
            TabIndex        =   3
            Top             =   1080
            Width           =   975
         End
         Begin VB.TextBox TxtValCCode 
            Height          =   285
            Left            =   1800
            TabIndex        =   2
            Text            =   "Text2"
            Top             =   480
            Width           =   5775
         End
         Begin VB.TextBox TxtCodeCCode 
            Height          =   285
            Left            =   120
            TabIndex        =   1
            Text            =   "Text1"
            Top             =   480
            Width           =   1575
         End
         Begin VB.Label LabValCCode 
            Caption         =   "Label2"
            Height          =   255
            Left            =   1800
            TabIndex        =   32
            Top             =   240
            Width           =   3375
         End
         Begin VB.Label labCode 
            Caption         =   "Label1"
            Height          =   255
            Index           =   0
            Left            =   120
            TabIndex        =   31
            Top             =   240
            Width           =   1455
         End
      End
   End
End
Attribute VB_Name = "FrmCodes"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Private MyCodes As ClCodes

Private Sub CmdClose_Click()
    Unload Me
End Sub

Private Sub CmdDel_Click(index As Integer)
    Dim i As Long
    
    If index = 0 Then
        Call MyCodes.RemoveElem(ListFilledCCode, TxtCodeCCode.Text, TxtValCCode.Text)
    ElseIf index = 1 Then
        For i = 1 To IdiomsInfo.Count
            Call MyCodes.RemoveElem(ListSponsor(i), TxtCodeSponsor.Text, TxtValSponsor(i).Text)
        Next
    Else
        For i = 1 To IdiomsInfo.Count
            Call MyCodes.RemoveElem(ListStudyArea(i), TxtCodeStudyArea.Text, TxtValStudyArea(i).Text)
        Next
    End If
End Sub

Private Sub CmdSave_Click(index As Integer)
    Dim i As Long
    
    If index = 0 Then
        Call MyCodes.SaveCodes(ListFilledCCode, "ccode")
    ElseIf index = 1 Then
        For i = 1 To IdiomsInfo.Count
            Call MyCodes.SaveCodes(ListSponsor(i), "sponsor", IdiomsInfo(i).Code)
        Next
    Else
        For i = 1 To IdiomsInfo.Count
            Call MyCodes.SaveCodes(ListStudyArea(i), "study area", IdiomsInfo(i).Code)
        Next
    End If
End Sub

Private Sub Form_Initialize()
    Set MyCodes = New ClCodes
End Sub

Private Sub Form_Terminate()
    Set MyCodes = Nothing
End Sub

Public Sub OpenCodes()
    Dim i As Long
    
    With ConfigLabels
    CcodeToFill.Caption = .Ccode_Edit
    FilledCCode.Caption = .Ccode_Filled
    StudyAreaToFill.Caption = .StudyArea_Edit
    FilledStudyArea.Caption = .StudyArea_Filled
    SponsorToFill.Caption = .Sponsor_Edit
    FilledSponsor.Caption = .Sponsor_filled
    
    For i = 0 To SSTab1.Tabs - 1
        CmdNew(i).Caption = .ButtonNew
        CmdDel(i).Caption = .ButtonRemove
        CmdSave(i).Caption = .ButtonSave
        labCode(i).Caption = .Code
    Next
    CmdClose.Caption = .ButtonClose
    CmdHelp.Caption = .ButtonHelp
    LabValCCode.Caption = .Center
    End With
    
    TxtCodeCCode.Text = ""
    TxtValCCode.Text = ""
    
    TxtCodeSponsor.Text = ""
    TxtCodeStudyArea.Text = ""
    
    Call MyCodes.OpenCodes(ListFilledCCode, "ccode")
    'Call MyCodes.SaveCodes(ListFilledCCode, "ccode")
    
    For i = 1 To IdiomsInfo.Count
        LabIdiomSponsor(i).Caption = IdiomsInfo(i).label
        LabIdiomSponsorEdit(i).Caption = IdiomsInfo(i).label
        Call MyCodes.OpenCodes(ListSponsor(i), "sponsor", IdiomsInfo(i).Code)
        TxtValSponsor(i).Text = ""
        'Call MyCodes.SaveCodes(ListSponsor(i), "sponsor", IdiomsInfo(i).Code)
        
        LabIdiom(i).Caption = IdiomsInfo(i).label
        LabIdiomEdit(i).Caption = IdiomsInfo(i).label
        Call MyCodes.OpenCodes(ListStudyArea(i), "study area", IdiomsInfo(i).Code)
        TxtValStudyArea(i).Text = ""
        'Call MyCodes.SaveCodes(ListStudyArea(i), "study area", IdiomsInfo(i).Code)
    Next
    
    Show vbModal
End Sub

Private Sub CmdNew_Click(index As Integer)
    Dim i As Long
    
    If index = 0 Then
        Call MyCodes.InsertElem(ListFilledCCode, TxtCodeCCode.Text, TxtValCCode.Text)
    ElseIf index = 1 Then
        For i = 1 To IdiomsInfo.Count
            Call MyCodes.InsertElem(ListSponsor(i), TxtCodeSponsor.Text, TxtValSponsor(i).Text)
        Next
    ElseIf index = 2 Then
        For i = 1 To IdiomsInfo.Count
            Call MyCodes.InsertElem(ListStudyArea(i), TxtCodeStudyArea.Text, TxtValStudyArea(i).Text)
        Next
    End If
End Sub

Private Sub ListFilledCCode_Click()
    Dim Code As String
    Dim value As String
    
    Call MyCodes.SelectedCodeValue(ListFilledCCode, Code, value)
    TxtCodeCCode.Text = Code
    TxtValCCode.Text = value
End Sub

Private Sub Listsponsor_Click(index As Integer)
    Dim Code As String
    Dim value As String
    Dim i As Long
    Dim k As Long
    
    Call MyCodes.SelectedCodeValue(ListSponsor(index), Code, value)
    TxtCodeSponsor.Text = Code
    TxtValSponsor(index).Text = value
    
    For i = 1 To IdiomsInfo.Count
        If index <> i Then
            k = FindCodeInList(ListSponsor(i), Code)
            If k >= 0 Then
                ListSponsor(i).Selected(k) = True
            End If
            'if listsponsor(i).se
        End If
    Next
End Sub

Private Sub ListStudyArea_Click(index As Integer)
    Dim Code As String
    Dim value As String
    Dim i As Long
    Dim k As Long
    
    Call MyCodes.SelectedCodeValue(ListStudyArea(index), Code, value)
    TxtCodeStudyArea.Text = Code
    TxtValStudyArea(index).Text = value
    
    For i = 1 To IdiomsInfo.Count
        If index <> i Then
            k = FindCodeInList(ListStudyArea(i), Code)
            If k >= 0 Then
                ListStudyArea(i).Selected(k) = True
            End If
            'if liststudyarea(i).se
        End If
    Next
End Sub
Private Function FindCodeInList(List As ListBox, Code As String) As Long
    Dim k As Long
    Dim found As Boolean
    Dim i As Long
    
    k = -1
    While (Not found) And (k < List.ListCount)
        k = k + 1
        If InStr(List.List(k), Code) = 1 Then
            found = True
            i = k
        End If
    Wend
    FindCodeInList = i
End Function
Private Sub TxtCodeCCode_Change()
    TxtValCCode.Text = MyCodes.GetValue(ListFilledCCode, TxtCodeCCode.Text)
End Sub
Private Sub TxtCodeSponsor_Change()
    Dim i As Long
    
    For i = 1 To IdiomsInfo.Count
        TxtValSponsor(i).Text = MyCodes.GetValue(ListSponsor(i), TxtCodeSponsor.Text)
    Next
End Sub
Private Sub TxtCodestudyarea_Change()
    Dim i As Long
    
    For i = 1 To IdiomsInfo.Count
        TxtValStudyArea(i).Text = MyCodes.GetValue(ListStudyArea(i), TxtCodeStudyArea.Text)
    Next
End Sub

Private Sub Form_Unload(Cancel As Integer)
    Dim res As VbMsgBoxResult
    Dim change As Boolean
    Dim i As Long
    Dim fn As Long
    
    change = change Or MyCodes.Codes_ChangedContents(ListFilledCCode, "ccode")
    For i = 1 To IdiomsInfo.Count
        change = change Or MyCodes.Codes_ChangedContents(ListSponsor(i), "sponsor", IdiomsInfo(i).Code)
        change = change Or MyCodes.Codes_ChangedContents(ListStudyArea(i), "study area", IdiomsInfo(i).Code)
    Next
        
    If change Then
        res = MsgBox(ConfigLabels.MsgSaveChanges, vbYesNoCancel)
        If res = vbYes Then
            Call MyCodes.SaveCodes(ListFilledCCode, "ccode")
            For i = 1 To IdiomsInfo.Count
                Call MyCodes.SaveCodes(ListSponsor(i), "sponsor", IdiomsInfo(i).Code)
                Call MyCodes.SaveCodes(ListStudyArea(i), "study area", IdiomsInfo(i).Code)
            Next
            GenerateCodeFile
            Unload Me
        ElseIf res = vbNo Then
            GenerateCodeFile
            Unload Me
        Else
            Cancel = 1
        End If
    Else
        GenerateCodeFile
        Unload Me
    End If
End Sub

Sub GenerateCodeFile()
    Dim i As Long
    Dim j As Long
    Dim fn As Long
    Dim fn2 As Long
    Dim dbtype As String
    Dim attr As String
    Dim idiom As String
    Dim dbname As String
    
    fn = 1
    fn2 = 2
    For i = 1 To IdiomsInfo.Count
        Open MARKUPPATH + PathSep + IdiomsInfo(i).Code + ATTB_FILE For Output As fn
        Open "values.lst" For Input As fn2
        While Not EOF(fn2)
            Input #fn2, dbtype, attr, idiom
            If dbtype = "new" Then
                dbname = DBNEWCODEFILE
            ElseIf dbtype = "curr" Then
                dbname = DBCODEFILE
            End If
            If idiom = "yes" Then
                Print #fn, MyCodes.GenerateFile(dbname, attr, IdiomsInfo(i).Code)
            Else
                Print #fn, MyCodes.GenerateFile(dbname, attr)
            End If
        Wend
        Close fn2
        Close fn
    Next
End Sub

