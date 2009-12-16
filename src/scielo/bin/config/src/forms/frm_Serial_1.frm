VERSION 5.00
Begin VB.Form Serial1 
   BorderStyle     =   1  'Fixed Single
   Caption         =   "Config - Serial's database"
   ClientHeight    =   5460
   ClientLeft      =   120
   ClientTop       =   1275
   ClientWidth     =   7710
   Icon            =   "frm_Serial_1.frx":0000
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   Moveable        =   0   'False
   NegotiateMenus  =   0   'False
   ScaleHeight     =   5460
   ScaleWidth      =   7710
   ShowInTaskbar   =   0   'False
   Begin VB.CommandButton CmdClose 
      Caption         =   "Close"
      Height          =   375
      Left            =   6600
      TabIndex        =   14
      Top             =   5040
      Width           =   975
   End
   Begin VB.CommandButton CmdNext 
      Caption         =   "Next"
      Height          =   375
      Left            =   3840
      TabIndex        =   12
      Top             =   5040
      Width           =   975
   End
   Begin VB.CommandButton CmdSave 
      Caption         =   "Save"
      Height          =   375
      Left            =   5520
      TabIndex        =   13
      Top             =   5040
      Width           =   975
   End
   Begin VB.Frame Frame1 
      Caption         =   "Information about the title's journal "
      Height          =   4935
      Left            =   120
      TabIndex        =   15
      Top             =   0
      Width           =   7455
      Begin VB.TextBox TxtISOStitle 
         Height          =   285
         Left            =   1680
         TabIndex        =   4
         Text            =   "Text2"
         Top             =   1560
         Width           =   5655
      End
      Begin VB.TextBox TxtSubtitle 
         Height          =   285
         Left            =   1680
         TabIndex        =   2
         Text            =   "Text2"
         Top             =   840
         Width           =   5655
      End
      Begin VB.TextBox TxtShortTitle 
         Height          =   285
         Left            =   1680
         TabIndex        =   3
         Text            =   "Text2"
         Top             =   1200
         Width           =   5655
      End
      Begin VB.TextBox TxtSectionTitle 
         Height          =   285
         Left            =   1680
         TabIndex        =   5
         Text            =   "Text2"
         Top             =   1920
         Width           =   5655
      End
      Begin VB.TextBox TxtParallel 
         Height          =   525
         Left            =   1680
         MultiLine       =   -1  'True
         TabIndex        =   6
         Text            =   "frm_Serial_1.frx":030A
         Top             =   2280
         Width           =   5655
      End
      Begin VB.TextBox TxtOldTitle 
         Height          =   285
         Left            =   1680
         TabIndex        =   8
         Text            =   "Text2"
         Top             =   3480
         Width           =   5655
      End
      Begin VB.TextBox TxtNewTitle 
         Height          =   285
         Left            =   1680
         TabIndex        =   9
         Text            =   "Text2"
         Top             =   3840
         Width           =   5655
      End
      Begin VB.TextBox TxtIsSuppl 
         Height          =   285
         Left            =   1680
         TabIndex        =   10
         Text            =   "Text2"
         Top             =   4200
         Width           =   5655
      End
      Begin VB.TextBox TxtOthTitle 
         Height          =   525
         Left            =   1680
         MultiLine       =   -1  'True
         TabIndex        =   7
         Text            =   "frm_Serial_1.frx":031B
         Top             =   2880
         Width           =   5655
      End
      Begin VB.TextBox TxtHasSuppl 
         Height          =   285
         Left            =   1680
         TabIndex        =   11
         Text            =   "Text2"
         Top             =   4560
         Width           =   5655
      End
      Begin VB.TextBox TxtSerTitle 
         Height          =   285
         Left            =   1680
         TabIndex        =   1
         Text            =   "Revista do Instituto de Medicina Tropical de São Paulo"
         Top             =   480
         Width           =   5655
      End
      Begin VB.TextBox TxtISSN 
         Enabled         =   0   'False
         Height          =   285
         Left            =   120
         Locked          =   -1  'True
         TabIndex        =   0
         Text            =   "0000-0000"
         Top             =   480
         Width           =   1095
      End
      Begin VB.Label LabISOStitle 
         AutoSize        =   -1  'True
         Caption         =   "ISO Short Title"
         Height          =   195
         Left            =   120
         TabIndex        =   27
         Top             =   1560
         Width           =   1035
      End
      Begin VB.Label LabIsSuppl 
         AutoSize        =   -1  'True
         Caption         =   "Is supplement"
         Height          =   195
         Left            =   120
         TabIndex        =   26
         Top             =   4200
         Width           =   975
      End
      Begin VB.Label LabHasSuppl 
         AutoSize        =   -1  'True
         Caption         =   "Has supplement"
         Height          =   195
         Left            =   120
         TabIndex        =   25
         Top             =   4560
         Width           =   1140
      End
      Begin VB.Label LabISSN 
         Caption         =   "ISSN"
         Height          =   255
         Left            =   120
         TabIndex        =   24
         Top             =   240
         Width           =   495
      End
      Begin VB.Label LabNewTitle 
         AutoSize        =   -1  'True
         Caption         =   "New Title"
         Height          =   195
         Left            =   120
         TabIndex        =   23
         Top             =   3840
         Width           =   675
      End
      Begin VB.Label LabOldTitle 
         AutoSize        =   -1  'True
         Caption         =   "Old Title"
         Height          =   195
         Left            =   120
         TabIndex        =   22
         Top             =   3480
         Width           =   585
      End
      Begin VB.Label LabOthTitle 
         AutoSize        =   -1  'True
         Caption         =   "Other Titles"
         Height          =   195
         Left            =   120
         TabIndex        =   21
         Top             =   2880
         Width           =   810
      End
      Begin VB.Label LabParallel 
         AutoSize        =   -1  'True
         Caption         =   "Parallel Titles"
         Height          =   195
         Left            =   120
         TabIndex        =   20
         Top             =   2280
         Width           =   930
      End
      Begin VB.Label LabShortTitle 
         AutoSize        =   -1  'True
         Caption         =   "Short Title"
         Height          =   195
         Left            =   120
         TabIndex        =   19
         Top             =   1200
         Width           =   720
      End
      Begin VB.Label LabSectionTitle 
         AutoSize        =   -1  'True
         Caption         =   "Section Title"
         Height          =   195
         Left            =   120
         TabIndex        =   18
         Top             =   1920
         Width           =   885
      End
      Begin VB.Label LabSubtitle 
         AutoSize        =   -1  'True
         Caption         =   "Publication Subtitle"
         Height          =   195
         Left            =   120
         TabIndex        =   17
         Top             =   840
         Width           =   1350
      End
      Begin VB.Label LabSerTitle 
         AutoSize        =   -1  'True
         Caption         =   "Publication Title"
         Height          =   195
         Left            =   1680
         TabIndex        =   16
         Top             =   240
         Width           =   1125
      End
   End
   Begin VB.Label LabIndicationMandatoryField 
      Caption         =   "Label1"
      ForeColor       =   &H000000FF&
      Height          =   255
      Left            =   120
      TabIndex        =   28
      Top             =   5040
      Width           =   2415
   End
End
Attribute VB_Name = "Serial1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private MyMfnTitle As Long
Public FillingNewSerial As Boolean

Sub MySetLabels()
    With Fields
    LabParallel.Caption = .getLabel("ser1_ParallelTitles")
    LabSerTitle.Caption = .getLabel("ser1_Title")
    LabISSN.Caption = .getLabel("ser1_issn")
    LabSubtitle.Caption = .getLabel("ser1_Subtitle")
    LabShortTitle.Caption = .getLabel("ser1_ShortTitle")
    LabISOStitle.Caption = .getLabel("ser1_ISOStitle")
    LabOthTitle.Caption = .getLabel("ser1_OtherTitles")
    LabIsSuppl.Caption = .getLabel("ser1_IsSuppl")
    LabHasSuppl.Caption = .getLabel("ser1_HasSuppl")
    LabSectionTitle.Caption = .getLabel("ser1_SectionTitle")
    LabOldTitle.Caption = .getLabel("ser1_OldTitle")
    LabNewTitle.Caption = .getLabel("ser1_NewTitle")
    End With
    
    With ConfigLabels
    LabIndicationMandatoryField.Caption = .getLabel("MandatoryFieldIndication")
    Frame1.Caption = .getLabel("ser1_FrameTitle")
    CmdNext.Caption = .getLabel("ButtonNext")
    CmdClose.Caption = .getLabel("ButtonClose")
    CmdSave.Caption = .getLabel("ButtonSave")
    End With
End Sub

Sub MyClearContent()
        TxtISSN.text = ""
        TxtISSN.Enabled = True
        TxtISSN.Locked = False
        TxtSubtitle.text = ""
        TxtShortTitle.text = ""
        TxtISOStitle.text = ""
        TxtSectionTitle.text = ""
        TxtParallel.text = ""
        TxtOthTitle.text = ""
        TxtOldTitle.text = ""
        TxtNewTitle.text = ""
        TxtIsSuppl.text = ""
        TxtHasSuppl.text = ""
End Sub
Sub MyGetContentFromBase(MfnTitle As Long)

        TxtISSN.text = Serial_TxtContent(MfnTitle, 400)
        If TxtISSN.text = "" Then
            TxtISSN.Locked = False
            TxtISSN.Enabled = True
        Else
            TxtISSN.Locked = True
            TxtISSN.Enabled = True
        End If
        TxtSerTitle.text = Serial_TxtContent(MfnTitle, 100)
        TxtSubtitle.text = Serial_TxtContent(MfnTitle, 110)
        TxtShortTitle.text = Serial_TxtContent(MfnTitle, 150)
        TxtISOStitle.text = Serial_TxtContent(MfnTitle, 151)
        TxtSectionTitle.text = Serial_TxtContent(MfnTitle, 130)
        TxtParallel.text = Serial_TxtContent(MfnTitle, 230)
        TxtOthTitle.text = Serial_TxtContent(MfnTitle, 240)
        TxtOldTitle.text = Serial_TxtContent(MfnTitle, 610)
        TxtNewTitle.text = Serial_TxtContent(MfnTitle, 710)
        TxtIsSuppl.text = Serial_TxtContent(MfnTitle, 560)
        TxtHasSuppl.text = Serial_TxtContent(MfnTitle, 550)
End Sub

Sub MyOpenSerial(SERIALTITLE As String, IsNewSerial As Boolean)

    Set journal = New ClsJournal
    
    FillingNewSerial = IsNewSerial
    
    MySetLabels
    Serial2.MySetLabels
    Serial3.MySetLabels
    Serial4.MySetLabels
    SERIAL7.MySetLabels
    SERIAL6.MySetLabels
    JOURNAL5.MySetLabels
    SERIAL8.MySetLabels
    
    TxtSerTitle.text = SERIALTITLE
    Caption = App.Title + " - " + TITLE_FORM_CAPTION + TxtSerTitle.text
    Serial2.Caption = Caption
    Serial3.Caption = Caption
    Serial4.Caption = Caption
    SERIAL7.Caption = Caption
    SERIAL6.Caption = Caption
    
    JOURNAL5.Caption = Caption
    SERIAL8.Caption = Caption
    
    MyMfnTitle = Serial_CheckExisting(SERIALTITLE)
    
    Serial2.IsBack = False
    Serial3.IsBack = False
    Serial4.IsBack = False
    SERIAL7.IsBack = False
    SERIAL6.IsBack = False
    JOURNAL5.IsBack = False
    SERIAL8.IsBack = False
    MyMfnTitle = Serial_CheckExisting(SERIALTITLE)
    If MyMfnTitle > 0 Then
        MyGetContentFromBase (MyMfnTitle)
        Serial2.MyGetContentFromBase (MyMfnTitle)
        Serial3.MyGetContentFromBase (MyMfnTitle)
        Serial4.MyGetContentFromBase (MyMfnTitle)
        SERIAL7.MyGetContentFromBase (MyMfnTitle)
        SERIAL6.MyGetContentFromBase (MyMfnTitle)
        JOURNAL5.MyGetContentFromBase (MyMfnTitle)
        SERIAL8.MyGetContentFromBase (MyMfnTitle)
    Else
        MyClearContent
        Serial2.MyClearContent
        Serial3.MyClearContent
        Serial4.MyClearContent
        SERIAL7.MyClearContent
        SERIAL6.MyClearContent
        JOURNAL5.MyClearContent
        SERIAL8.MyClearContent
    End If
    
    
    Left = FormMenuPrin.SysInfo1.WorkAreaWidth / 2 - (Width + FrmInfo.Width) / 2
    Top = FormMenuPrin.SysInfo1.WorkAreaHeight / 2 - Height / 2
    FrmInfo.Top = Top
    FrmInfo.Left = Left + Width
    
    FrmInfo.Show
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
    Serial2.MyOpen (MyMfnTitle)
End Sub

Private Sub CmdSave_Click()
    MousePointer = vbHourglass
    MyMfnTitle = Serial_Save(MyMfnTitle)
    MousePointer = vbArrow
End Sub


Private Sub Form_QueryUnload(Cancel As Integer, UnloadMode As Integer)
    Call FormQueryUnload(Cancel, UnloadMode)
End Sub

Private Sub TxtISOStitle_GotFocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser1_ISOStitle")
End Sub

Private Sub TxtISSN_GotFocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser1_issn")
End Sub

Private Sub TxtISSN_LostFocus()
    If Not TxtISSN.Locked Then
        If journalDAO.existISSN(TxtISSN.text) > 0 Then
            MsgBox "ISSN already exists" ' FIXME
            TxtISSN.SetFocus
        Else
            If Len(TxtISSN.text) <> 9 Or Mid(TxtISSN.text, 5, 1) <> "-" Then
                MsgBox "ISSN - bad format"
            End If
        End If
        
    End If
End Sub

Private Sub Txtsertitle_GotFocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser1_Title")
End Sub
Private Sub TxtSubTitle_GotFocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser1_Subtitle")
End Sub
Private Sub Txtshorttitle_GotFocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser1_ShortTitle")
End Sub
Private Sub TxtSectionTitle_GotFocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser1_SectionTitle")
End Sub

Private Sub TxtParallel_GotFocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser1_ParallelTitles")
End Sub

Private Sub TxtOthTitle_GotFocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser1_OtherTitles")
End Sub

Private Sub TxtNewTitle_GotFocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser1_NewTitle")
End Sub

Private Sub TxtOldTitle_GotFocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser1_OldTitle")
End Sub

Private Sub TxtIsSuppl_GotFocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser1_IsSuppl")
End Sub
Private Sub TxtHasSuppl_GotFocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser1_HasSuppl")
End Sub

Sub OpenAgain(mfn As Long)
    MyMfnTitle = mfn
End Sub
