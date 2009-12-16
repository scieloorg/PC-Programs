VERSION 5.00
Begin VB.Form Serial3 
   BorderStyle     =   1  'Fixed Single
   Caption         =   "Config - Serial's database"
   ClientHeight    =   5460
   ClientLeft      =   120
   ClientTop       =   1410
   ClientWidth     =   7710
   Icon            =   "frm_Serial_3.frx":0000
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   Moveable        =   0   'False
   NegotiateMenus  =   0   'False
   ScaleHeight     =   5460
   ScaleWidth      =   7710
   ShowInTaskbar   =   0   'False
   Begin VB.CommandButton CmdBack 
      Caption         =   "Back"
      Height          =   375
      Left            =   2760
      TabIndex        =   21
      Top             =   5040
      Width           =   975
   End
   Begin VB.CommandButton CmdClose 
      Caption         =   "Close"
      Height          =   375
      Left            =   6600
      TabIndex        =   24
      Top             =   5040
      Width           =   975
   End
   Begin VB.CommandButton CmdNext 
      Caption         =   "Next"
      Height          =   375
      Left            =   3840
      TabIndex        =   22
      Top             =   5040
      Width           =   975
   End
   Begin VB.CommandButton CmdSave 
      Caption         =   "Save"
      Height          =   375
      Left            =   5520
      TabIndex        =   23
      Top             =   5040
      Width           =   975
   End
   Begin VB.Frame FrameFormalInfo 
      Caption         =   "Formal information"
      Height          =   4935
      Left            =   120
      TabIndex        =   26
      Top             =   0
      Width           =   7455
      Begin VB.Frame FrameInfoHealth 
         Caption         =   "Information for the health area "
         Height          =   1455
         Left            =   3360
         TabIndex        =   45
         Top             =   3120
         Width           =   3975
         Begin VB.TextBox TxtMEDLINE 
            Height          =   285
            Left            =   1680
            TabIndex        =   19
            Text            =   "Text2"
            Top             =   480
            Width           =   1335
         End
         Begin VB.TextBox TxtSECS 
            Height          =   285
            Left            =   120
            TabIndex        =   18
            Text            =   "Text2"
            Top             =   480
            Width           =   1215
         End
         Begin VB.TextBox TxtMEDLINEStitle 
            Height          =   285
            Left            =   120
            TabIndex        =   20
            Text            =   "Text3"
            Top             =   1080
            Width           =   3735
         End
         Begin VB.Label LabSECS 
            AutoSize        =   -1  'True
            Caption         =   "SECS identifier"
            Height          =   195
            Left            =   120
            TabIndex        =   48
            Top             =   240
            Width           =   1050
         End
         Begin VB.Label LabMEDLINE 
            AutoSize        =   -1  'True
            Caption         =   "MEDLINE code"
            Height          =   195
            Left            =   1680
            TabIndex        =   47
            Top             =   240
            Width           =   1125
         End
         Begin VB.Label LabMEDLINEStitle 
            AutoSize        =   -1  'True
            Caption         =   "Short title for MEDLINE"
            Height          =   195
            Left            =   120
            TabIndex        =   46
            Top             =   840
            Width           =   1650
         End
      End
      Begin VB.ComboBox ComboTpLit 
         Height          =   315
         Left            =   120
         Sorted          =   -1  'True
         TabIndex        =   15
         Text            =   "Combo1"
         Top             =   3240
         Width           =   3135
      End
      Begin VB.ComboBox ComboTreatLev 
         Height          =   315
         Left            =   120
         Sorted          =   -1  'True
         TabIndex        =   16
         Text            =   "Combo1"
         Top             =   3840
         Width           =   3135
      End
      Begin VB.ComboBox ComboPubLev 
         Height          =   315
         Left            =   120
         Sorted          =   -1  'True
         TabIndex        =   17
         Text            =   "Combo1"
         Top             =   4440
         Width           =   3135
      End
      Begin VB.ListBox ListScheme 
         Height          =   510
         Left            =   4920
         Style           =   1  'Checkbox
         TabIndex        =   14
         Top             =   2520
         Width           =   2295
      End
      Begin VB.ListBox ListTextIdiom 
         Height          =   510
         Left            =   2520
         Sorted          =   -1  'True
         Style           =   1  'Checkbox
         TabIndex        =   10
         Top             =   1680
         Width           =   2295
      End
      Begin VB.ComboBox ComboStandard 
         Height          =   315
         Left            =   2520
         TabIndex        =   13
         Text            =   "ComboStandard"
         Top             =   2520
         Width           =   2295
      End
      Begin VB.ComboBox ComboPubStatus 
         Height          =   315
         Left            =   2520
         Sorted          =   -1  'True
         TabIndex        =   7
         Text            =   "Combo1"
         Top             =   1080
         Width           =   2295
      End
      Begin VB.ComboBox ComboFreq 
         Height          =   315
         Left            =   120
         Sorted          =   -1  'True
         TabIndex        =   6
         Text            =   "Combo1"
         Top             =   1080
         Width           =   2295
      End
      Begin VB.TextBox TxtClassif 
         Height          =   285
         Left            =   120
         TabIndex        =   9
         Text            =   "Text5"
         Top             =   1800
         Width           =   2175
      End
      Begin VB.ListBox ListAbstIdiom 
         Height          =   510
         Left            =   4920
         Sorted          =   -1  'True
         Style           =   1  'Checkbox
         TabIndex        =   11
         Top             =   1680
         Width           =   2415
      End
      Begin VB.TextBox TxtTermDate 
         Height          =   285
         Left            =   3720
         TabIndex        =   3
         Text            =   "19990000"
         Top             =   480
         Width           =   975
      End
      Begin VB.TextBox TxtInitVol 
         Height          =   285
         Left            =   1320
         TabIndex        =   1
         Text            =   "0000"
         Top             =   480
         Width           =   615
      End
      Begin VB.TextBox TxtInitNo 
         Height          =   285
         Left            =   2520
         TabIndex        =   2
         Text            =   "0000"
         Top             =   480
         Width           =   615
      End
      Begin VB.TextBox TxtFinNo 
         Height          =   285
         Left            =   6360
         TabIndex        =   5
         Text            =   "0000"
         Top             =   480
         Width           =   615
      End
      Begin VB.TextBox TxtNationalcode 
         Height          =   285
         Left            =   120
         TabIndex        =   12
         Text            =   "Text5"
         Top             =   2520
         Width           =   2175
      End
      Begin VB.ComboBox ComboAlphabet 
         Height          =   315
         Left            =   4920
         Sorted          =   -1  'True
         TabIndex        =   8
         Text            =   "Combo2"
         Top             =   1080
         Width           =   2295
      End
      Begin VB.TextBox TxtFinVol 
         Height          =   285
         Left            =   5160
         TabIndex        =   4
         Text            =   "0000"
         Top             =   480
         Width           =   615
      End
      Begin VB.TextBox TxtInitDate 
         Height          =   285
         Left            =   120
         TabIndex        =   0
         Text            =   "19990000"
         Top             =   480
         Width           =   975
      End
      Begin VB.Label LabPubLevel 
         AutoSize        =   -1  'True
         Caption         =   "Level of publication"
         Height          =   195
         Left            =   120
         TabIndex        =   44
         Top             =   4200
         Width           =   1380
      End
      Begin VB.Label LabTpLiterature 
         AutoSize        =   -1  'True
         Caption         =   "Type of literature"
         Height          =   195
         Left            =   120
         TabIndex        =   43
         Top             =   3000
         Width           =   1185
      End
      Begin VB.Label LabTreatLevel 
         AutoSize        =   -1  'True
         Caption         =   "Treatment level"
         Height          =   195
         Left            =   120
         TabIndex        =   42
         Top             =   3600
         Width           =   1095
      End
      Begin VB.Label LabScheme 
         AutoSize        =   -1  'True
         Caption         =   "Scheme"
         Height          =   195
         Left            =   4920
         TabIndex        =   41
         Top             =   2280
         Width           =   1665
      End
      Begin VB.Label LabStandard 
         AutoSize        =   -1  'True
         Caption         =   "Standard"
         Height          =   195
         Left            =   2520
         TabIndex        =   39
         Top             =   2280
         Width           =   645
      End
      Begin VB.Label LabClassif 
         AutoSize        =   -1  'True
         Caption         =   "Classification"
         Height          =   195
         Left            =   120
         TabIndex        =   38
         Top             =   1560
         Width           =   915
      End
      Begin VB.Label LabNationalCode 
         AutoSize        =   -1  'True
         Caption         =   "National code"
         Height          =   195
         Left            =   120
         TabIndex        =   37
         Top             =   2280
         Width           =   990
      End
      Begin VB.Label LabAbstIdiom 
         AutoSize        =   -1  'True
         Caption         =   "Abstract idiom"
         Height          =   195
         Left            =   4920
         TabIndex        =   36
         Top             =   1440
         Width           =   990
      End
      Begin VB.Label LabTextIdiom 
         AutoSize        =   -1  'True
         Caption         =   "Text idiom"
         Height          =   195
         Left            =   2520
         TabIndex        =   35
         Top             =   1440
         Width           =   720
      End
      Begin VB.Label LabAlphabet 
         AutoSize        =   -1  'True
         Caption         =   "Alphabet"
         Height          =   195
         Left            =   4920
         TabIndex        =   34
         Top             =   840
         Width           =   630
      End
      Begin VB.Label LabFrequency 
         AutoSize        =   -1  'True
         Caption         =   "Frequency"
         Height          =   195
         Left            =   120
         TabIndex        =   33
         Top             =   840
         Width           =   750
      End
      Begin VB.Label LabPubStatus 
         AutoSize        =   -1  'True
         Caption         =   "Publication status"
         Height          =   195
         Left            =   2520
         TabIndex        =   32
         Top             =   840
         Width           =   1245
      End
      Begin VB.Label LabFinNo 
         AutoSize        =   -1  'True
         Caption         =   "Final number"
         Height          =   195
         Left            =   6360
         TabIndex        =   31
         Top             =   240
         Width           =   900
      End
      Begin VB.Label LabFinVol 
         AutoSize        =   -1  'True
         Caption         =   "Final volume"
         Height          =   195
         Left            =   5160
         TabIndex        =   30
         Top             =   240
         Width           =   885
      End
      Begin VB.Label LabTermDate 
         AutoSize        =   -1  'True
         Caption         =   "Termination date"
         Height          =   195
         Left            =   3720
         TabIndex        =   29
         Top             =   240
         Width           =   1185
      End
      Begin VB.Label LabInitNo 
         AutoSize        =   -1  'True
         Caption         =   "Initial number"
         Height          =   195
         Left            =   2520
         TabIndex        =   28
         Top             =   240
         Width           =   930
      End
      Begin VB.Label LabInitVol 
         AutoSize        =   -1  'True
         Caption         =   "Initial volume"
         Height          =   195
         Left            =   1320
         TabIndex        =   27
         Top             =   240
         Width           =   915
      End
      Begin VB.Label LabInitDate 
         AutoSize        =   -1  'True
         Caption         =   "Initial date"
         Height          =   195
         Left            =   120
         TabIndex        =   25
         Top             =   240
         Width           =   720
      End
   End
   Begin VB.Label LabIndicationMandatoryField 
      Caption         =   "Label1"
      ForeColor       =   &H000000FF&
      Height          =   255
      Left            =   120
      TabIndex        =   40
      Top             =   5040
      Width           =   2415
   End
End
Attribute VB_Name = "Serial3"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private MyMfnTitle As Long
Public IsBack As Boolean

Private Sub CmdBack_Click()
    Hide
    IsBack = True
    Serial2.MyOpen (MyMfnTitle)
    
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
    Serial4.MyOpen (MyMfnTitle)
End Sub

Sub MySetLabels()
    
    With Fields
    LabInitDate.Caption = .getLabel("ser3_InitDate")
    LabInitVol.Caption = .getLabel("ser3_InitVol")
    LabInitNo.Caption = .getLabel("ser3_InitNo")
    LabTermDate.Caption = .getLabel("ser3_TermDate")
    LabFinVol.Caption = .getLabel("ser3_FinVol")
    LabFinNo.Caption = .getLabel("ser3_FinNo")
    LabFrequency.Caption = .getLabel("ser3_Freq")
    LabPubStatus.Caption = .getLabel("ser3_PubStatus")
    LabAlphabet.Caption = .getLabel("ser3_Alphabet")
    LabTextIdiom.Caption = .getLabel("ser3_TxtIdiom")
    LabAbstIdiom.Caption = .getLabel("ser3_AbstIdiom")
    LabNationalCode.Caption = .getLabel("ser3_NationalCode")
    LabClassif.Caption = .getLabel("ser3_Classif")
    LabStandard.Caption = .getLabel("Title_standard")
    LabScheme.Caption = .getLabel("Issue_Scheme")
    
    LabSECS.Caption = .getLabel("ser4_secs")
    LabMEDLINE.Caption = .getLabel("ser4_medline")
    LabMEDLINEStitle.Caption = .getLabel("ser4_MedlineStitle")
    
    LabTpLiterature.Caption = .getLabel("ser2_LiterType")
    LabTreatLevel.Caption = .getLabel("ser2_TreatLevel")
    LabPubLevel.Caption = .getLabel("ser2_PubLevel")
    
    End With
    
    With ConfigLabels
    LabIndicationMandatoryField.Caption = .getLabel("MandatoryFieldIndication")
    FrameFormalInfo.Caption = .getLabel("ser3_FormalInfo")
    FrameInfoHealth.Caption = .getLabel("ser4_FrameInfoHealth")
    CmdBack.Caption = .getLabel("ButtonBack")
    CmdNext.Caption = .getLabel("ButtonNext")
    CmdClose.Caption = .getLabel("ButtonClose")
    CmdSave.Caption = .getLabel("ButtonSave")
    End With
    
    Call FillCombo(ComboAlphabet, CodeAlphabet)
    Call FillCombo(ComboFreq, CodeFrequency)
    Call FillCombo(ComboPubStatus, codeStatus)
    Call FillList(ListTextIdiom, CodeTxtLanguage)
    Call FillList(ListAbstIdiom, CodeAbstLanguage)
    Call FillCombo(ComboStandard, CodeStandard)
    Call FillList(ListScheme, CodeScheme)
    Call FillCombo(ComboTpLit, CodeLiteratureType)
    Call FillCombo(ComboTreatLev, CodeTreatLevel)
    Call FillCombo(ComboPubLev, CodePubLevel)
End Sub

Sub MyClearContent()
        TxtInitDate.text = ""
        TxtInitVol.text = ""
        TxtInitNo.text = ""
        TxtTermDate.text = ""
        TxtFinVol.text = ""
        TxtFinNo.text = ""
        
        ComboFreq.text = ""
        ComboPubStatus.text = ""
        ComboAlphabet.text = ""
        Call UnselectList(ListAbstIdiom)
        Call UnselectList(ListTextIdiom)
        Call UnselectList(ListScheme)
        ComboStandard.text = ""
        TxtNationalcode.text = ""
        TxtClassif.text = ""
        
TxtSECS.text = ""
        TxtMEDLINE.text = ""
        TxtMEDLINEStitle.text = ""
        ComboTpLit.text = Serial_ComboDefaultValue(CodeLiteratureType, ConfigLabels.getLabel("ser2_LiterTypeDefVal"))
    ComboTreatLev.text = Serial_ComboDefaultValue(CodeTreatLevel, ConfigLabels.getLabel("ser2_TreatLevelDefVal"))
    ComboPubLev.text = ""
    
End Sub

Sub MyGetContentFromBase(MfnTitle As Long)
        TxtInitDate.text = Serial_TxtContent(MfnTitle, 301)
        TxtInitVol.text = Serial_TxtContent(MfnTitle, 302)
        TxtInitNo.text = Serial_TxtContent(MfnTitle, 303)
        TxtTermDate.text = Serial_TxtContent(MfnTitle, 304)
        TxtFinVol.text = Serial_TxtContent(MfnTitle, 305)
        TxtFinNo.text = Serial_TxtContent(MfnTitle, 306)
        
        ComboFreq.text = Serial_ComboContent(CodeFrequency, MfnTitle, 380)
        ComboPubStatus.text = Serial_ComboContent(codeStatus, MfnTitle, 50)
        ComboAlphabet.text = Serial_ComboContent(CodeAlphabet, MfnTitle, 340)
        Call Serial_ListContent(ListTextIdiom, CodeTxtLanguage, MfnTitle, 350)
        Call Serial_ListContent(ListAbstIdiom, CodeAbstLanguage, MfnTitle, 360)
        
        TxtNationalcode.text = Serial_TxtContent(MfnTitle, 20)
        TxtClassif.text = Serial_TxtContent(MfnTitle, 430)
        ComboStandard.text = Serial_ComboContent(CodeStandard, MfnTitle, 117)
        
        Call Serial_ListContent(ListScheme, CodeScheme, MfnTitle, 85)
        
        
        TxtSECS.text = Serial_TxtContent(MfnTitle, 37)
        TxtMEDLINE.text = Serial_TxtContent(MfnTitle, 420)
        TxtMEDLINEStitle.text = Serial_TxtContent(MfnTitle, 421)
        
        ComboTpLit.text = Serial_ComboContent(CodeLiteratureType, MfnTitle, 5, ConfigLabels.getLabel("ser2_LiterTypeDefVal"))
    ComboTreatLev.text = Serial_ComboContent(CodeTreatLevel, MfnTitle, 6, ConfigLabels.getLabel("ser2_TreatLevelDefVal"))
    ComboPubLev.text = Serial_ComboContent(CodePubLevel, MfnTitle, 330)
    
        
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


Private Sub ListAbstIdiom_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser3_AbstIdiom")
End Sub

Private Sub ListTextIdiom_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser3_TxtIdiom")
End Sub

Private Sub TxtClassif_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser3_Classif")
End Sub

Private Sub TxtFinNo_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser3_FinNo")
End Sub

Private Sub TxtFinVol_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser3_FinVol")
End Sub
    
Private Sub TxtInitDate_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser3_InitDate")
End Sub

Private Sub TxtInitNo_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser3_InitNo")
End Sub

Private Sub TxtInitVol_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser3_InitVol")
End Sub

Private Sub TxtNationalcode_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser3_NationalCode")
End Sub


Private Sub TxtTermDate_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser3_TermDate")
End Sub
Private Sub ComboAlphabet_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser3_Alphabet")
End Sub


Private Sub ComboFreq_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser3_Freq")
End Sub

Private Sub ComboPubStatus_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser3_PubStatus")
End Sub

Private Sub ComboStandard_GotFocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("Title_Standard")
    End Sub
    

Private Sub ListScheme_GotFocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("title_Scheme")
End Sub

Private Sub TxtMEDLINE_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser4_medline")
End Sub

Private Sub TxtMEDLINEStitle_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser4_MedlineStitle")
End Sub
Private Sub TxtSECS_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser4_secs")
End Sub
Private Sub combotpLit_GotFocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser2_LiterType")
End Sub

Private Sub comboTreatLev_GotFocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser2_TreatLevel")
End Sub
Private Sub ComboPubLev_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser2_PubLevel")
End Sub
