VERSION 5.00
Begin VB.Form Serial4 
   BorderStyle     =   1  'Fixed Single
   Caption         =   "Config - Serial's database"
   ClientHeight    =   5460
   ClientLeft      =   120
   ClientTop       =   1335
   ClientWidth     =   7710
   Icon            =   "frm_Serial_4.frx":0000
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   Moveable        =   0   'False
   NegotiateMenus  =   0   'False
   ScaleHeight     =   5460
   ScaleWidth      =   7710
   ShowInTaskbar   =   0   'False
   Begin VB.Frame FrameInfoPub 
      Caption         =   "Information about the publisher and the journal "
      Height          =   4815
      Left            =   120
      TabIndex        =   14
      Top             =   120
      Width           =   7455
      Begin VB.TextBox TxtAddress 
         Height          =   855
         Left            =   120
         MultiLine       =   -1  'True
         TabIndex        =   4
         Top             =   1920
         Width           =   3975
      End
      Begin VB.TextBox TxtSponsor 
         Height          =   525
         Left            =   120
         MultiLine       =   -1  'True
         TabIndex        =   8
         Text            =   "frm_Serial_4.frx":030A
         Top             =   3120
         Width           =   5055
      End
      Begin VB.TextBox TxtEmail 
         Height          =   285
         Left            =   4200
         TabIndex        =   5
         Text            =   "Text4"
         Top             =   1920
         Width           =   3135
      End
      Begin VB.TextBox TxtFaxNumber 
         Height          =   285
         Left            =   5760
         TabIndex        =   7
         Top             =   2520
         Visible         =   0   'False
         Width           =   1575
      End
      Begin VB.TextBox TxtPhone 
         Height          =   285
         Left            =   4200
         TabIndex        =   6
         Top             =   2520
         Visible         =   0   'False
         Width           =   1455
      End
      Begin VB.ComboBox ComboState 
         Height          =   315
         Left            =   2640
         TabIndex        =   2
         Text            =   "Combo1"
         Top             =   1320
         Width           =   2175
      End
      Begin VB.ComboBox ComboCountry 
         Height          =   315
         Left            =   120
         Sorted          =   -1  'True
         TabIndex        =   1
         Text            =   "Combo2"
         Top             =   1320
         Width           =   2175
      End
      Begin VB.TextBox TxtPubCity 
         Height          =   285
         Left            =   5160
         TabIndex        =   3
         Text            =   "Text4"
         Top             =   1320
         Width           =   2175
      End
      Begin VB.TextBox TxtPublisher 
         Height          =   555
         Left            =   120
         MultiLine       =   -1  'True
         TabIndex        =   0
         Text            =   "frm_Serial_4.frx":032F
         Top             =   480
         Width           =   7215
      End
      Begin VB.Label LabAddress 
         AutoSize        =   -1  'True
         Caption         =   "Address"
         Height          =   195
         Left            =   120
         TabIndex        =   23
         Top             =   1680
         Width           =   570
      End
      Begin VB.Label LabEmail 
         AutoSize        =   -1  'True
         Caption         =   "Electronic address"
         Height          =   195
         Left            =   4200
         TabIndex        =   22
         Top             =   1680
         Width           =   1305
      End
      Begin VB.Label LabSponsor 
         AutoSize        =   -1  'True
         Caption         =   "Sponsor"
         Height          =   195
         Left            =   120
         TabIndex        =   21
         Top             =   2880
         Width           =   585
      End
      Begin VB.Label LabFax 
         AutoSize        =   -1  'True
         Caption         =   "Fax Number"
         Height          =   195
         Left            =   5760
         TabIndex        =   20
         Top             =   2280
         Visible         =   0   'False
         Width           =   855
      End
      Begin VB.Label LabPhone 
         AutoSize        =   -1  'True
         Caption         =   "Phone Number"
         Height          =   195
         Left            =   4200
         TabIndex        =   19
         Top             =   2280
         Visible         =   0   'False
         Width           =   1065
      End
      Begin VB.Label LabPubCity 
         AutoSize        =   -1  'True
         Caption         =   "Publisher's city"
         Height          =   195
         Left            =   5160
         TabIndex        =   18
         Top             =   1080
         Width           =   1035
      End
      Begin VB.Label LabPubState 
         AutoSize        =   -1  'True
         Caption         =   "Publisher's state"
         Height          =   195
         Left            =   2640
         TabIndex        =   17
         Top             =   1080
         Width           =   1140
      End
      Begin VB.Label LabPubCountry 
         AutoSize        =   -1  'True
         Caption         =   "Publisher's country "
         Height          =   195
         Left            =   120
         TabIndex        =   16
         Top             =   1080
         Width           =   1365
      End
      Begin VB.Label LabPublisher 
         AutoSize        =   -1  'True
         Caption         =   "Publisher"
         Height          =   195
         Left            =   120
         TabIndex        =   15
         Top             =   240
         Width           =   645
      End
   End
   Begin VB.CommandButton CmdBack 
      Caption         =   "Back"
      Height          =   375
      Left            =   2760
      TabIndex        =   9
      Top             =   5040
      Width           =   975
   End
   Begin VB.CommandButton CmdClose 
      Caption         =   "Close"
      Height          =   375
      Left            =   6600
      TabIndex        =   12
      Top             =   5040
      Width           =   975
   End
   Begin VB.CommandButton CmdNext 
      Caption         =   "Next"
      Height          =   375
      Left            =   3840
      TabIndex        =   10
      Top             =   5040
      Width           =   975
   End
   Begin VB.CommandButton CmdSave 
      Caption         =   "Save"
      Height          =   375
      Left            =   5520
      TabIndex        =   11
      Top             =   5040
      Width           =   975
   End
   Begin VB.Label LabIndicationMandatoryField 
      Caption         =   "Label1"
      ForeColor       =   &H000000FF&
      Height          =   255
      Left            =   120
      TabIndex        =   13
      Top             =   5040
      Width           =   2415
   End
End
Attribute VB_Name = "Serial4"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private MyMfnTitle As Long
Public IsBack As Boolean

Private Sub CmdBack_Click()
    Hide
    IsBack = True
    Serial3.MyOpen (MyMfnTitle)
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
    JOURNAL5.MyOpen (MyMfnTitle)
End Sub



Sub MySetLabels()
    With Fields
    LabAddress.Caption = .getLabel("ser4_Address")
    LabPhone.Caption = .getLabel("ser4_Phone")
    LabFax.Caption = .getLabel("ser4_Fax")
    LabEmail.Caption = .getLabel("ser4_email")
    LabSponsor.Caption = .getLabel("ser4_sponsor")
    LabPublisher.Caption = .getLabel("ser3_Publisher")
    LabPubCountry.Caption = .getLabel("ser3_PubCountry")
    LabPubState.Caption = .getLabel("ser3_PubState")
    LabPubCity.Caption = .getLabel("ser3_PubCity")
        
    End With
    
    Call FillCombo(ComboCountry, CodeCountry)
    Call FillCombo(ComboState, CodeState)
    
    With ConfigLabels
    LabIndicationMandatoryField.Caption = .getLabel("MandatoryFieldIndication")
    FrameInfoPub.Caption = .getLabel("ser4_FrameInfoPubJournal_2")
    '
    
    CmdBack.Caption = .getLabel("ButtonBack")
    CmdNext.Caption = .getLabel("ButtonNext")
    CmdClose.Caption = .getLabel("ButtonClose")
    CmdSave.Caption = .getLabel("ButtonSave")
    End With
    
    
End Sub

Sub MyClearContent()
        TxtAddress.text = ""
        TxtPhone.text = ""
        TxtFaxNumber.text = ""
        TxtEmail.text = ""
        TxtSponsor.text = ""
        
                TxtPublisher.text = ""
        ComboCountry.text = ""
        ComboState.text = ""
        'TxtPubState.Text = ""
        TxtPubCity.text = ""


End Sub

Sub MyGetContentFromBase(MfnTitle As Long)
        TxtAddress.text = Serial_TxtContent(MfnTitle, 63)
        TxtPhone.text = Serial_TxtContent(MfnTitle, 631)
        TxtFaxNumber.text = Serial_TxtContent(MfnTitle, 632)
        TxtEmail.text = Serial_TxtContent(MfnTitle, 64)
        TxtSponsor.text = Serial_TxtContent(MfnTitle, 140)
        
        
        TxtPublisher.text = Serial_TxtContent(MfnTitle, 480)
        ComboCountry.text = Serial_ComboContent(CodeCountry, MfnTitle, 310)
        ComboState.text = Serial_ComboContent(CodeState, MfnTitle, 320)
        TxtPubCity.text = Serial_TxtContent(MfnTitle, 490)
        
        
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

Private Sub TxtAddress_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser4_Address")
End Sub


Private Sub TxtEmail_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser4_email")
End Sub

Private Sub TxtFaxNumber_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser4_Fax")
End Sub

Private Sub TxtPhone_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser4_Phone")
End Sub

Private Sub TxtSponsor_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser4_sponsor")
End Sub
Private Sub TxtPubCity_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser3_PubCity")
End Sub

Private Sub TxtPublisher_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser3_Publisher")
End Sub

'Private Sub TxtPubState_gotfocus()
 '    FrmInfo.ShowHelpMessage fields.getHelp("ser3_PubState, 2
 'End Sub

Private Sub ComboPubState_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser3_PubState")
End Sub
Private Sub ComboCountry_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser3_PubCountry")
End Sub

