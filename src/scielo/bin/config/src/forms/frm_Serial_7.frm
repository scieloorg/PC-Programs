VERSION 5.00
Begin VB.Form JOURNAL5 
   BorderStyle     =   1  'Fixed Single
   Caption         =   "Config - Serial's database"
   ClientHeight    =   5460
   ClientLeft      =   45
   ClientTop       =   1335
   ClientWidth     =   7710
   Icon            =   "frm_Serial_7.frx":0000
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   Moveable        =   0   'False
   NegotiateMenus  =   0   'False
   ScaleHeight     =   5460
   ScaleWidth      =   7710
   ShowInTaskbar   =   0   'False
   Begin VB.CommandButton CmdNext 
      Caption         =   "Next"
      Height          =   375
      Left            =   3840
      TabIndex        =   5
      Top             =   5040
      Width           =   975
   End
   Begin VB.CommandButton CmdBack 
      Caption         =   "Back"
      Height          =   375
      Left            =   2760
      TabIndex        =   4
      Top             =   5040
      Width           =   975
   End
   Begin VB.CommandButton CmdClose 
      Caption         =   "Close"
      Height          =   375
      Left            =   6600
      TabIndex        =   7
      Top             =   5040
      Width           =   975
   End
   Begin VB.CommandButton CmdSave 
      Caption         =   "Save"
      Height          =   375
      Left            =   5520
      TabIndex        =   6
      Top             =   5040
      Width           =   975
   End
   Begin VB.Frame Frame1 
      Height          =   975
      Left            =   120
      TabIndex        =   13
      Top             =   3960
      Width           =   7455
      Begin VB.TextBox TxtCprighter 
         Height          =   285
         Left            =   120
         TabIndex        =   3
         Text            =   "Text4"
         Top             =   480
         Width           =   5055
      End
      Begin VB.TextBox TxtCprightDate 
         Height          =   285
         Left            =   5280
         TabIndex        =   14
         Text            =   "Text4"
         Top             =   480
         Visible         =   0   'False
         Width           =   1215
      End
      Begin VB.Label LabCprighter 
         AutoSize        =   -1  'True
         Caption         =   "Copyrighter"
         Height          =   195
         Left            =   120
         TabIndex        =   16
         Top             =   240
         Width           =   795
      End
      Begin VB.Label LabCprightDate 
         AutoSize        =   -1  'True
         Caption         =   "Copyright (Date)"
         Height          =   195
         Left            =   5280
         TabIndex        =   15
         Top             =   240
         Visible         =   0   'False
         Width           =   1140
      End
   End
   Begin VB.Frame FrameCreativeCommons 
      Caption         =   "Creative Commons"
      Height          =   3855
      Left            =   120
      TabIndex        =   9
      Top             =   120
      Width           =   7455
      Begin VB.ComboBox ComboLicVersion 
         Height          =   315
         Left            =   4560
         TabIndex        =   18
         Text            =   "Combo1"
         Top             =   600
         Width           =   1815
      End
      Begin VB.ComboBox ComboLicText 
         Height          =   315
         ItemData        =   "frm_Serial_7.frx":030A
         Left            =   1200
         List            =   "frm_Serial_7.frx":030C
         Style           =   2  'Dropdown List
         TabIndex        =   17
         Top             =   600
         Width           =   3135
      End
      Begin VB.TextBox TextCreativeCommons 
         Height          =   855
         Index           =   0
         Left            =   1200
         Locked          =   -1  'True
         MultiLine       =   -1  'True
         TabIndex        =   0
         Top             =   1080
         Visible         =   0   'False
         Width           =   6135
      End
      Begin VB.TextBox TextCreativeCommons 
         Height          =   735
         Index           =   1
         Left            =   1200
         Locked          =   -1  'True
         MultiLine       =   -1  'True
         TabIndex        =   1
         Top             =   2040
         Visible         =   0   'False
         Width           =   6135
      End
      Begin VB.TextBox TextCreativeCommons 
         Height          =   855
         Index           =   2
         Left            =   1200
         Locked          =   -1  'True
         MultiLine       =   -1  'True
         TabIndex        =   2
         Top             =   2880
         Visible         =   0   'False
         Width           =   6135
      End
      Begin VB.Label LabLicVersion 
         Caption         =   "Label2"
         Height          =   255
         Left            =   4560
         TabIndex        =   20
         Top             =   360
         Width           =   1695
      End
      Begin VB.Label LabLicText 
         Caption         =   "Label1"
         Height          =   255
         Left            =   1200
         TabIndex        =   19
         Top             =   360
         Width           =   2295
      End
      Begin VB.Label Label10 
         Caption         =   "Inglês"
         Height          =   255
         Index           =   0
         Left            =   120
         TabIndex        =   12
         Top             =   1080
         Visible         =   0   'False
         Width           =   1335
      End
      Begin VB.Label Label10 
         Caption         =   "Português"
         Height          =   255
         Index           =   1
         Left            =   120
         TabIndex        =   11
         Top             =   2040
         Visible         =   0   'False
         Width           =   1335
      End
      Begin VB.Label Label10 
         Caption         =   "Espanhol"
         Height          =   255
         Index           =   2
         Left            =   120
         TabIndex        =   10
         Top             =   2880
         Visible         =   0   'False
         Width           =   1335
      End
   End
   Begin VB.Label LabIndicationMandatoryField 
      Caption         =   "Label1"
      ForeColor       =   &H000000FF&
      Height          =   255
      Left            =   120
      TabIndex        =   8
      Top             =   5040
      Width           =   2415
   End
End
Attribute VB_Name = "JOURNAL5"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Public IsBack As Boolean
Private MyMfnTitle As Long
Private savedlicense As New clsCreativeCommons
'Private currentLicText As ColIdiom
Private Const MAX_LINES_INDEX = 10



Private Sub CmdBack_Click()
    Hide
    IsBack = True
    Serial4.MyOpen (MyMfnTitle)
End Sub

Sub MySetLabels()
    
    With Fields
    'LabelCreativeCommonsInstructions.Caption = .getLabel("issue_creativecommons")
    For i = 1 To idiomsinfo.count
        Label10(i - 1).Caption = idiomsinfo(i).label
    Next
    LabLicText.Caption = .getLabel("title_license")
    LabLicVersion.Caption = .getLabel("title_licversion")
    
    LabCprightDate.Caption = .getLabel("ser4_cprightDate")
    LabCprighter.Caption = .getLabel("ser4_cprighter")
    Call FillCombo(ComboLicText, CodeLicText, True)
    Call FillCombo(ComboLicVersion, CodeLicversion, True)
    End With
    
    With ConfigLabels
        CmdBack.Caption = .getLabel("ButtonBack")
        CmdClose.Caption = .getLabel("ButtonClose")
        CmdSave.Caption = .getLabel("ButtonSave")
        LabIndicationMandatoryField.Caption = .getLabel("MandatoryFieldIndication")
    End With
    
End Sub

Sub MyGetContentFromBase(MfnTitle As Long)
    'JournalStatusAction.setLanguage (CurrCodeIdiom)
    'Set JournalStatusAction.ErrorMessages = ErrorMessages
    'Set JournalStatusAction.myHistory = journalDAO.getHistory(MfnTitle)
    Dim customized As Boolean
    
    Set savedlicense = New clsCreativeCommons
    Set savedlicense = journalDAO.getJournalCreativeCommons(MfnTitle)
    If Len(savedlicense.Code) > 0 Then
        ComboLicText.text = savedlicense.Code
    Else
        ComboLicText.text = "nd"
    End If
    ComboLicVersion.text = Serial_TxtContent(MfnTitle, 542)
    TxtCprightDate.text = Serial_TxtContent(MfnTitle, 621)
    TxtCprighter.text = Serial_TxtContent(MfnTitle, 62)

End Sub


Sub MyClearContent()
    Dim i As Long
    
    For i = 1 To 3
        TextCreativeCommons(i - 1).text = ""
    Next
            TxtCprightDate.text = ""
        TxtCprighter.text = ""

End Sub

Function changed(MfnTitle As Long) As Boolean
    'FIXME
    Dim temp As clsCreativeCommons
    Dim change As Boolean
    
    
    Set temp = journalDAO.getJournalCreativeCommons(MfnTitle)
    
    changed = (temp.Code <> ComboLicText.text) Or (temp.version <> ComboLicVersion.text)
    
End Function
Sub MyOpen(MfnTitle As Long)
    MyMfnTitle = MfnTitle
    
    Left = FormMenuPrin.SysInfo1.WorkAreaWidth / 2 - (Width + FrmInfo.Width) / 2
    Top = FormMenuPrin.SysInfo1.WorkAreaHeight / 2 - Height / 2
    FrmInfo.Top = Top
    FrmInfo.Left = Left + Width
    
    Show
    'FIXME
    
End Sub

Private Sub CmdCancel_Click()
    CancelFilling
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
    SERIAL6.MyOpen (MyMfnTitle)

End Sub

Private Sub CmdSave_Click()
    MousePointer = vbHourglass
    
    
    MyMfnTitle = Serial_Save(MyMfnTitle)
    MousePointer = vbArrow
End Sub

Private Sub Form_QueryUnload(Cancel As Integer, UnloadMode As Integer)
    Call FormQueryUnload(Cancel, UnloadMode)
End Sub


Function getCreativeCommons() As clsCreativeCommons
    Set getCreativeCommons = savedlicense
End Function

Private Sub TextCreativeCommons_GotFocus(index As Integer)
Call FrmInfo.ShowHelpMessage(Fields.getLabel("title_creativecommons"), 2)

End Sub

Private Sub TxtCprightDate_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser4_cprightDate")
End Sub

Private Sub TxtCprighter_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser4_cprighter")
End Sub
