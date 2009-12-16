VERSION 5.00
Begin VB.Form SERIAL8 
   BorderStyle     =   1  'Fixed Single
   Caption         =   "Config - Serial's database"
   ClientHeight    =   5460
   ClientLeft      =   45
   ClientTop       =   1335
   ClientWidth     =   7710
   Icon            =   "frm_Serial_8.frx":0000
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   Moveable        =   0   'False
   NegotiateMenus  =   0   'False
   ScaleHeight     =   5460
   ScaleWidth      =   7710
   ShowInTaskbar   =   0   'False
   Begin VB.Frame FrameNotes 
      Caption         =   "Notes"
      Height          =   3015
      Left            =   120
      TabIndex        =   18
      Top             =   120
      Width           =   7455
      Begin VB.TextBox TxtNotes 
         Height          =   2655
         Left            =   120
         MultiLine       =   -1  'True
         TabIndex        =   0
         Top             =   240
         Width           =   7215
      End
   End
   Begin VB.CommandButton CmdBack 
      Caption         =   "Back"
      Height          =   375
      Left            =   2760
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
   Begin VB.CommandButton CmdSave 
      Caption         =   "Save"
      Height          =   375
      Left            =   5520
      TabIndex        =   8
      Top             =   5040
      Width           =   975
   End
   Begin VB.Frame FrameCenter 
      Caption         =   "Center's control information "
      Height          =   1695
      Left            =   120
      TabIndex        =   10
      Top             =   3240
      Width           =   7455
      Begin VB.TextBox TxtCreatDate 
         BackColor       =   &H00C0C0C0&
         Height          =   285
         Left            =   2640
         Locked          =   -1  'True
         TabIndex        =   4
         Text            =   "19990000"
         Top             =   1320
         Width           =   855
      End
      Begin VB.TextBox TxtDocCreation 
         Height          =   285
         Left            =   2640
         TabIndex        =   3
         Text            =   "FAPSB"
         Top             =   960
         Width           =   855
      End
      Begin VB.TextBox TxtDocUpdate 
         Height          =   285
         Left            =   6480
         TabIndex        =   5
         Text            =   "FAPSB"
         Top             =   960
         Width           =   855
      End
      Begin VB.TextBox TxtUpdateDate 
         BackColor       =   &H00C0C0C0&
         Height          =   285
         Left            =   6480
         Locked          =   -1  'True
         TabIndex        =   6
         Text            =   "19990000"
         Top             =   1320
         Width           =   855
      End
      Begin VB.TextBox TxtIdNumber 
         Height          =   285
         Left            =   5280
         TabIndex        =   2
         Text            =   "Text5"
         Top             =   480
         Width           =   2055
      End
      Begin VB.ComboBox ComboCCode 
         Height          =   315
         ItemData        =   "frm_Serial_8.frx":030A
         Left            =   120
         List            =   "frm_Serial_8.frx":030C
         Sorted          =   -1  'True
         TabIndex        =   1
         Text            =   "pode digitar também?"
         Top             =   480
         Width           =   5055
      End
      Begin VB.Label LabDocUpdate 
         Alignment       =   1  'Right Justify
         AutoSize        =   -1  'True
         Caption         =   "Documentalist (update)"
         Height          =   195
         Left            =   4800
         TabIndex        =   16
         Top             =   960
         Width           =   1635
      End
      Begin VB.Label LabDocCreation 
         Alignment       =   1  'Right Justify
         AutoSize        =   -1  'True
         Caption         =   "Documentalist (creation)"
         Height          =   195
         Left            =   840
         TabIndex        =   15
         Top             =   960
         Width           =   1710
      End
      Begin VB.Label LabUpdateDate 
         Alignment       =   1  'Right Justify
         AutoSize        =   -1  'True
         Caption         =   "Update date"
         Height          =   195
         Left            =   5520
         TabIndex        =   14
         Top             =   1320
         Width           =   885
      End
      Begin VB.Label LabCreatDate 
         Alignment       =   1  'Right Justify
         AutoSize        =   -1  'True
         Caption         =   "Creation date"
         Height          =   195
         Left            =   1560
         TabIndex        =   13
         Top             =   1320
         Width           =   945
      End
      Begin VB.Label LabIdNumber 
         AutoSize        =   -1  'True
         Caption         =   "Identification number"
         Height          =   195
         Left            =   5280
         TabIndex        =   12
         Top             =   240
         Width           =   1470
      End
      Begin VB.Label LabCCode 
         AutoSize        =   -1  'True
         Caption         =   "Center code"
         Height          =   195
         Left            =   120
         TabIndex        =   11
         Top             =   240
         Width           =   870
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
Attribute VB_Name = "SERIAL8"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Public IsBack As Boolean
Private MyMfnTitle As Long

Private Sub Check1_Click()

End Sub

Private Sub CmdBack_Click()
    Hide
    IsBack = True
    SERIAL7.MyOpen (MyMfnTitle)
End Sub

Sub MySetLabels()
    With Fields
    LabCCode.Caption = .getLabel("ser5_CCode")
    LabIdNumber.Caption = .getLabel("ser5_IdNumber")
    LabDocCreation.Caption = .getLabel("ser5_DocCreation")
    LabCreatDate.Caption = .getLabel("ser5_CreatDate")
    LabDocUpdate.Caption = .getLabel("ser5_DocUpdate")
    LabUpdateDate.Caption = .getLabel("ser5_UpdateDate")
    End With
    
    With ConfigLabels
    LabIndicationMandatoryField.Caption = .getLabel("MandatoryFieldIndication")
    FrameCenter.Caption = .getLabel("ser5_FrameCenterControl")
    CmdBack.Caption = .getLabel("ButtonBack")
        

    CmdClose.Caption = .getLabel("ButtonClose")
    'CmdCancel.Caption = .ButtonCancel
    CmdSave.Caption = .getLabel("ButtonSave")
    End With
    
    Call FillCombo(ComboCCode, CodeCCode)
End Sub

Sub MyGetContentFromBase(MfnTitle As Long)
        
                TxtNotes.text = Serial_TxtContent(MfnTitle, 900)

        ComboCCode.text = Serial_ComboContent(CodeCCode, MfnTitle, 10)
        TxtIdNumber.text = Serial_TxtContent(MfnTitle, 30)
        TxtDocCreation.text = Serial_TxtContent(MfnTitle, 950)
                
        TxtCreatDate.text = Serial_TxtContent(MfnTitle, 940)
        If Len(TxtCreatDate.text) = 0 Then TxtCreatDate.text = getDateIso(Date)
        
        TxtDocUpdate.text = Serial_TxtContent(MfnTitle, 951)
        TxtUpdateDate.text = Serial_TxtContent(MfnTitle, 941)
End Sub
Sub MyClearContent()
        ComboCCode.text = ""
        TxtIdNumber.text = ""
        TxtDocCreation.text = ""
        TxtCreatDate.text = getDateIso(Date)
        TxtDocUpdate.text = ""
        TxtUpdateDate.text = ""
End Sub

Sub MyOpen(MfnTitle As Long)
    MyMfnTitle = MfnTitle
    
    Left = FormMenuPrin.SysInfo1.WorkAreaWidth / 2 - (Width + FrmInfo.Width) / 2
    Top = FormMenuPrin.SysInfo1.WorkAreaHeight / 2 - Height / 2
    FrmInfo.Top = Top
    FrmInfo.Left = Left + Width
    
    Show
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
    'WarnMandatoryFields
    'SERIAL6.MyOpen (MyMfnTitle)
End Sub


Private Sub CmdSave_Click()
    MousePointer = vbHourglass
    MyMfnTitle = Serial_Save(MyMfnTitle)
    MousePointer = vbArrow
End Sub


Private Sub Form_QueryUnload(Cancel As Integer, UnloadMode As Integer)
    Call FormQueryUnload(Cancel, UnloadMode)
End Sub



Private Sub listscielonet_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser5_SciELONet")
End Sub

Private Sub Text1_Change()

End Sub

Private Sub TxtCreatDate_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser5_CreatDate")
End Sub

Private Sub TxtDocCreation_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser5_DocCreation")
End Sub

Private Sub TxtDocUpdate_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser5_DocUpdate")
End Sub

Private Sub TxtIdNumber_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser5_IdNumber")
End Sub
Private Sub TxtNotes_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser5_notes")
End Sub


Private Sub TxtUpdateDate_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser5_UpdateDate")
End Sub

Private Sub ComboCCode_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser5_CCode")
End Sub
