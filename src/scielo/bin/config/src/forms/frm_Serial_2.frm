VERSION 5.00
Begin VB.Form Serial2 
   BorderStyle     =   1  'Fixed Single
   Caption         =   "Config - Serial's database"
   ClientHeight    =   5460
   ClientLeft      =   180
   ClientTop       =   1275
   ClientWidth     =   7710
   Icon            =   "frm_Serial_2.frx":0000
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   Moveable        =   0   'False
   NegotiateMenus  =   0   'False
   ScaleHeight     =   5460
   ScaleWidth      =   7710
   ShowInTaskbar   =   0   'False
   Begin VB.CommandButton CmdSave 
      Caption         =   "Save"
      Height          =   375
      Left            =   5520
      TabIndex        =   8
      Top             =   5040
      Width           =   975
   End
   Begin VB.CommandButton CmdNext 
      Caption         =   "Next"
      Height          =   375
      Left            =   3840
      TabIndex        =   7
      Top             =   5040
      Width           =   975
   End
   Begin VB.CommandButton CmdClose 
      Caption         =   "Close"
      Height          =   375
      Left            =   6600
      TabIndex        =   9
      Top             =   5040
      Width           =   975
   End
   Begin VB.CommandButton CmdBack 
      Caption         =   "Back"
      Height          =   375
      Left            =   2760
      TabIndex        =   6
      Top             =   5040
      Width           =   975
   End
   Begin VB.Frame FrameSubject 
      Caption         =   "Subject information"
      Height          =   4815
      Left            =   120
      TabIndex        =   10
      Top             =   120
      Width           =   7455
      Begin VB.Frame FrameIdxRange 
         Caption         =   "Indexation range"
         Height          =   1935
         Left            =   3360
         TabIndex        =   18
         Top             =   2760
         Width           =   3975
         Begin VB.TextBox TxtIdxRange 
            Height          =   1575
            Left            =   120
            MultiLine       =   -1  'True
            TabIndex        =   5
            Text            =   "frm_Serial_2.frx":030A
            Top             =   240
            Width           =   3615
         End
      End
      Begin VB.ListBox ListStudyArea 
         Height          =   735
         Left            =   120
         Style           =   1  'Checkbox
         TabIndex        =   4
         Top             =   3960
         Width           =   3135
      End
      Begin VB.Frame FrameMission 
         Caption         =   "Mission"
         Height          =   2415
         Left            =   120
         TabIndex        =   13
         Top             =   240
         Width           =   7215
         Begin VB.TextBox TxtMission 
            Height          =   615
            Index           =   1
            Left            =   1080
            ScrollBars      =   2  'Vertical
            TabIndex        =   0
            Text            =   "texto não repetitivo com várias linhas"
            Top             =   240
            Width           =   6015
         End
         Begin VB.TextBox TxtMission 
            Height          =   615
            Index           =   3
            Left            =   1080
            ScrollBars      =   2  'Vertical
            TabIndex        =   2
            Text            =   "texto não repetitivo com várias linhas"
            Top             =   1680
            Width           =   6015
         End
         Begin VB.TextBox TxtMission 
            Height          =   615
            Index           =   2
            Left            =   1080
            ScrollBars      =   2  'Vertical
            TabIndex        =   1
            Text            =   "texto não repetitivo com várias linhas"
            Top             =   960
            Width           =   6015
         End
         Begin VB.Label LabIdiom 
            AutoSize        =   -1  'True
            Caption         =   "English"
            Height          =   195
            Index           =   3
            Left            =   120
            TabIndex        =   16
            Top             =   1560
            Width           =   510
         End
         Begin VB.Label LabIdiom 
            AutoSize        =   -1  'True
            Caption         =   "Spanish"
            Height          =   195
            Index           =   2
            Left            =   120
            TabIndex        =   15
            Top             =   840
            Width           =   570
         End
         Begin VB.Label LabIdiom 
            AutoSize        =   -1  'True
            Caption         =   "Portuguese"
            Height          =   195
            Index           =   1
            Left            =   120
            TabIndex        =   14
            Top             =   240
            Width           =   810
         End
      End
      Begin VB.TextBox TxtDescriptors 
         Height          =   615
         Left            =   120
         MultiLine       =   -1  'True
         TabIndex        =   3
         Text            =   "frm_Serial_2.frx":0315
         Top             =   3000
         Width           =   3135
      End
      Begin VB.Label LabSubject 
         AutoSize        =   -1  'True
         Caption         =   "Subject"
         Height          =   195
         Left            =   120
         TabIndex        =   12
         Top             =   2760
         Width           =   540
      End
      Begin VB.Label LabStudyArea 
         AutoSize        =   -1  'True
         Caption         =   "Study area"
         Height          =   195
         Left            =   120
         TabIndex        =   11
         Top             =   3720
         Width           =   765
      End
   End
   Begin VB.Label LabIndicationMandatoryField 
      Caption         =   "Label1"
      ForeColor       =   &H000000FF&
      Height          =   255
      Left            =   120
      TabIndex        =   17
      Top             =   5040
      Width           =   2415
   End
End
Attribute VB_Name = "Serial2"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private MyMfnTitle As Long
Public IsBack As Boolean

Private Sub CmdBack_Click()
    Hide
    IsBack = True
    Serial1.OpenAgain (MyMfnTitle)
End Sub

Private Sub CmdClose_Click()
    Dim respClose As Integer
    
    respClose = Serial_Close(MyMfnTitle)
    Select Case respClose
    Case 1
        UnloadSerialForms
    Case 2
        CmdSave_Click
        UnloadSerialForms
    End Select
End Sub

Private Sub CmdNext_Click()
    'WarnMandatoryFields
    Serial3.MyOpen (MyMfnTitle)
End Sub



Sub MySetLabels()
    Dim i As Long
    
    For i = 1 To IdiomsInfo.count
        LabIdiom(i).Caption = IdiomsInfo(i).label
    Next
    
    With Fields
    
    FrameMission.Caption = .getLabel("ser2_Mission")
    LabSubject.Caption = .getLabel("ser2_Subject")
    LabStudyArea.Caption = .getLabel("ser2_StudyArea")
    FrameIdxRange.Caption = .getLabel("ser4_idxRange")
    
    
    End With
    
    With ConfigLabels
    LabIndicationMandatoryField.Caption = .getLabel("MandatoryFieldIndication")
    FrameSubject.Caption = .getLabel("ser2_SubjectInfo")
    CmdBack.Caption = .getLabel("ButtonBack")
    CmdNext.Caption = .getLabel("ButtonNext")
    CmdClose.Caption = .getLabel("ButtonClose")
    CmdSave.Caption = .getLabel("ButtonSave")
    End With
    
    
    'Call FillListStudyArea(ListStudyArea, CodeStudyArea)
    Call FillList(ListStudyArea, CodeStudyArea)


End Sub

Sub MyClearContent()
    Dim i As Long
    
    For i = 1 To IdiomsInfo.count
        TxtMission(i).text = ""
    Next
    
    TxtDescriptors.text = ""
    
    Call UnselectList(ListStudyArea)
    
    TxtIdxRange.text = ""
    
End Sub

Sub MyGetContentFromBase(MfnTitle As Long)
    Dim aux As String
    Dim i As Long
    
    For i = 1 To IdiomsInfo.count
        TxtMission(i).text = Serial_TxtContent(MfnTitle, 901, IdiomsInfo(i).Code)
    Next

    TxtDescriptors.text = UCase(Serial_TxtContent(MfnTitle, 440))
    Call Serial_ListContent(ListStudyArea, CodeStudyArea, MfnTitle, 441)
        
    TxtIdxRange.text = Serial_TxtContent(MfnTitle, 450)

End Sub

Sub MyOpen(MfnTitle As Long)
    MyMfnTitle = MfnTitle
    
    Left = FormMenuPrin.SysInfo1.WorkAreaWidth / 2 - (Width + FrmInfo.Width) / 2
    Top = FormMenuPrin.SysInfo1.WorkAreaHeight / 2 - Height / 2
    FrmInfo.Top = Top
    FrmInfo.Left = Left + Width
    
    Show
End Sub


Private Sub CmdSave_Click()
    MousePointer = vbHourglass
    MyMfnTitle = Serial_Save(MyMfnTitle)
    MousePointer = vbArrow
End Sub



Private Sub Form_QueryUnload(Cancel As Integer, UnloadMode As Integer)
    Call FormQueryUnload(Cancel, UnloadMode)
End Sub


Private Sub TxtDescriptors_Gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser2_Subject")
End Sub

Private Sub TxtMission_GotFocus(Index As Integer)
    FrmInfo.ShowHelpMessage Fields.getHelp("ser2_Mission")
End Sub

Private Sub ListStudyArea_GotFocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser2_StudyArea")
End Sub

Private Sub TxtIdxRange_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser4_idxRange")
End Sub

