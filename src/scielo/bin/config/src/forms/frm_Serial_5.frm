VERSION 5.00
Begin VB.Form SERIAL7 
   BorderStyle     =   1  'Fixed Single
   Caption         =   "Config - Serial's database"
   ClientHeight    =   5460
   ClientLeft      =   45
   ClientTop       =   1335
   ClientWidth     =   7710
   Icon            =   "frm_Serial_5.frx":0000
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
      TabIndex        =   12
      Top             =   5040
      Width           =   975
   End
   Begin VB.CommandButton CmdBack 
      Caption         =   "Back"
      Height          =   375
      Left            =   2760
      TabIndex        =   11
      Top             =   5040
      Width           =   975
   End
   Begin VB.CommandButton CmdClose 
      Caption         =   "Close"
      Height          =   375
      Left            =   6600
      TabIndex        =   14
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
   Begin VB.Frame FrameSciELO 
      Height          =   4815
      Left            =   120
      TabIndex        =   15
      Top             =   120
      Width           =   7455
      Begin VB.TextBox Text1 
         Height          =   285
         Left            =   120
         TabIndex        =   4
         Text            =   "Text4"
         Top             =   1080
         Width           =   3855
      End
      Begin VB.TextBox Text_CurrentISSN 
         Height          =   285
         Left            =   5520
         TabIndex        =   3
         Top             =   480
         Width           =   1815
      End
      Begin VB.TextBox Text_SubmissionOnline 
         Height          =   285
         Left            =   120
         TabIndex        =   6
         Text            =   "Text1"
         Top             =   1680
         Width           =   3855
      End
      Begin VB.ComboBox ComboISSNType 
         Height          =   315
         Left            =   3000
         TabIndex        =   2
         Text            =   "ComboISSNType"
         Top             =   480
         Width           =   2415
      End
      Begin VB.ListBox ListSciELONet 
         Height          =   3435
         Left            =   4080
         Sorted          =   -1  'True
         Style           =   1  'Checkbox
         TabIndex        =   5
         Top             =   1080
         Width           =   3255
      End
      Begin VB.TextBox TxtPubId 
         BackColor       =   &H00C0C0C0&
         Height          =   285
         Left            =   1320
         Locked          =   -1  'True
         TabIndex        =   1
         Text            =   "mmmmmmmm"
         Top             =   480
         Width           =   1455
      End
      Begin VB.ComboBox ComboUserSubscription 
         Height          =   315
         Left            =   120
         Sorted          =   -1  'True
         TabIndex        =   9
         Text            =   "Combo1"
         Top             =   3480
         Width           =   3855
      End
      Begin VB.TextBox TxtSiteLocation 
         Height          =   285
         Left            =   120
         TabIndex        =   7
         Text            =   "Text4"
         Top             =   2280
         Width           =   3855
      End
      Begin VB.TextBox TxtSep 
         Height          =   285
         Left            =   120
         TabIndex        =   10
         Text            =   "Text3"
         Top             =   4320
         Visible         =   0   'False
         Width           =   3735
      End
      Begin VB.ComboBox ComboFTP 
         Height          =   315
         Left            =   120
         Sorted          =   -1  'True
         TabIndex        =   8
         Text            =   "Combo1"
         Top             =   2880
         Width           =   3855
      End
      Begin VB.TextBox TxtSiglum 
         Height          =   285
         Left            =   120
         TabIndex        =   0
         Text            =   "mmmmmmmm"
         Top             =   480
         Width           =   1095
      End
      Begin VB.Label Label1 
         AutoSize        =   -1  'True
         Caption         =   "Site location"
         Height          =   195
         Left            =   120
         TabIndex        =   27
         Top             =   840
         Width           =   870
      End
      Begin VB.Label label_currentissue 
         Caption         =   "LabCurrentISSN"
         Height          =   255
         Left            =   5520
         TabIndex        =   26
         Top             =   240
         Width           =   1455
      End
      Begin VB.Label Lab_SubmissionOnline 
         Caption         =   "URL de SciELO Submission Online"
         Height          =   255
         Left            =   120
         TabIndex        =   25
         Top             =   1440
         Width           =   2895
      End
      Begin VB.Label LabISSNType 
         Caption         =   "LabISSNType"
         Height          =   255
         Left            =   3000
         TabIndex        =   24
         Top             =   240
         Width           =   1455
      End
      Begin VB.Label LabScieloNET 
         AutoSize        =   -1  'True
         Caption         =   "Scielo net"
         Height          =   195
         Left            =   4080
         TabIndex        =   22
         Top             =   840
         Width           =   705
      End
      Begin VB.Label LabSep 
         AutoSize        =   -1  'True
         Caption         =   "Separator"
         Height          =   195
         Left            =   120
         TabIndex        =   21
         Top             =   4080
         Visible         =   0   'False
         Width           =   690
      End
      Begin VB.Label LabSiteLocation 
         AutoSize        =   -1  'True
         Caption         =   "Site location"
         Height          =   195
         Left            =   120
         TabIndex        =   20
         Top             =   2040
         Width           =   870
      End
      Begin VB.Label LabUserSubscription 
         AutoSize        =   -1  'True
         Caption         =   "User's subscription"
         Height          =   195
         Left            =   120
         TabIndex        =   19
         Top             =   3240
         Width           =   1320
      End
      Begin VB.Label LabFTP 
         AutoSize        =   -1  'True
         Caption         =   "FTP"
         Height          =   195
         Left            =   120
         TabIndex        =   18
         Top             =   2640
         Width           =   300
      End
      Begin VB.Label LabPubId 
         AutoSize        =   -1  'True
         Caption         =   "Publisher's identifier"
         Height          =   195
         Left            =   1320
         TabIndex        =   17
         Top             =   240
         Width           =   1380
      End
      Begin VB.Label LabSiglum 
         AutoSize        =   -1  'True
         Caption         =   "Siglum"
         Height          =   195
         Left            =   120
         TabIndex        =   16
         Top             =   240
         Width           =   465
      End
   End
   Begin VB.Label LabIndicationMandatoryField 
      Caption         =   "Label1"
      ForeColor       =   &H000000FF&
      Height          =   255
      Left            =   120
      TabIndex        =   23
      Top             =   5040
      Width           =   2415
   End
End
Attribute VB_Name = "SERIAL7"
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
    SERIAL6.MyOpen (MyMfnTitle)
End Sub

Sub MySetLabels()
    With Fields
    Label1.Caption = .getLabel("ser5_MainCollectionLocation")
    LabScieloNET.Caption = .getLabel("ser5_SciELONet")
    LabSiglum.Caption = .getLabel("ser5_siglum")
    LabPubId.Caption = .getLabel("ser5_PubId")
    LabSep.Caption = .getLabel("ser5_Sep")
    LabSiteLocation.Caption = .getLabel("ser5_SiteLocation")
    LabFTP.Caption = .getLabel("ser5_FTP")
    LabISSNType.Caption = .getLabel("ser5_issntype")
    LabUserSubscription.Caption = .getLabel("ser5_UserSubscription")
    label_currentissue.Caption = .getLabel("currentISSN")
    Lab_SubmissionOnline.Caption = .getLabel("ser5_SubmissionOnline")
    End With
    
    With ConfigLabels
    LabIndicationMandatoryField.Caption = .getLabel("MandatoryFieldIndication")
    FrameSciELO.Caption = .getLabel("ser5_FrameSciELOControl")
    CmdBack.Caption = .getLabel("ButtonBack")
        CmdNext.Caption = .getLabel("ButtonNext")

    CmdClose.Caption = .getLabel("ButtonClose")
    'CmdCancel.Caption = .ButtonCancel
    CmdSave.Caption = .getLabel("ButtonSave")
    End With
    
    Call FillCombo(ComboFTP, CodeFTP)
    Call FillCombo(ComboUserSubscription, CodeUsersubscription)
    
    Call FillCombo(ComboISSNType, CodeISSNType)
    Call FillList(ListSciELONet, CodeScieloNet)
    
    
End Sub

Sub MyGetContentFromBase(MfnTitle As Long)
        
        TxtSiglum.text = Serial_TxtContent(MfnTitle, 930)
        TxtPubId.text = Serial_TxtContent(MfnTitle, 68)
        TxtSep.text = Serial_TxtContent(MfnTitle, 65)
        TxtSiteLocation.text = Serial_TxtContent(MfnTitle, 69)
        ComboFTP.text = Serial_ComboContent(CodeFTP, MfnTitle, 66)
        ComboISSNType.text = Serial_ComboContent(CodeISSNType, MfnTitle, 35)
        ComboUserSubscription.text = Serial_ComboContent(CodeUsersubscription, MfnTitle, 67)
        Call ScieloNetRead(MfnTitle)
        Text_SubmissionOnline.text = Serial_TxtContent(MfnTitle, 692)
        Text1.text = Serial_TxtContent(MfnTitle, 690)
        Text_CurrentISSN.text = Serial_TxtContent(MfnTitle, 935)
        
End Sub
Sub MyClearContent()
        Call UnselectList(ListSciELONet)
        TxtSiglum.text = ""
        TxtPubId.text = ""
        TxtSep.text = ""
        TxtSiteLocation.text = ""
        ComboFTP.text = ""
        ComboISSNType.text = ""
        Text_SubmissionOnline.text = ""
        ComboUserSubscription.text = ""
        Text_CurrentISSN.text = ""
        Text1.text = ""
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
    SERIAL8.MyOpen (MyMfnTitle)
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

Private Sub Text1_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser5_MainCollectionLocation")
End Sub

Private Sub TxtPubId_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser5_PubId")
End Sub

Private Sub TxtSep_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser5_Sep")
End Sub

Private Sub TxtSiglum_Change()
    TxtPubId.text = LCase(TxtSiglum.text)
End Sub

Private Sub TxtSiglum_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser5_siglum")
End Sub

Private Sub TxtSiteLocation_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser5_SiteLocation")
End Sub

Private Sub ComboFTP_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser5_FTP")
End Sub

Private Sub Comboissntype_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser5_issntype")
End Sub

Private Sub ComboUserSubscription_gotfocus()
    FrmInfo.ShowHelpMessage Fields.getHelp("ser5_UserSubscription")
End Sub

Function ScieloNetRead(MfnTitle As Long) As String
    Dim i As Long
    Dim item As ClCode
    Dim exist As Boolean
    Dim idx As Long
    Dim content As String
    
    content = Serial_TxtContent(MfnTitle, 691)
    If Len(content) > 0 Then
        Set item = New ClCode
        For i = 0 To ListSciELONet.ListCount - 1
            Set item = CodeScieloNet(ListSciELONet.list(i), exist)
            If exist Then
                idx = CLng(item.Code)
                If idx <= Len(content) Then
                    ListSciELONet.selected(i) = (Mid(content, idx, 1) = 1)
                Else
                    ListSciELONet.selected(i) = False
                End If
            Else
                ListSciELONet.selected(i) = False
            End If
        Next
    Else
        For i = 0 To ListSciELONet.ListCount - 1
            ListSciELONet.selected(i) = False
        Next
    End If
        
    For i = Len(content) + 1 To ListSciELONet.ListCount
        content = content + "0"
    Next
    
    ScieloNetRead = content
End Function



Function ScieloNetWrite() As String
    Dim i As Long
    Dim item As ClCode
    Dim exist As Boolean
    Dim s() As String
    Dim q As Long
    Dim content As String
    
    
    With SERIAL7
    q = .ListSciELONet.ListCount
    ReDim s(q)
    
    Set item = New ClCode
    For i = 0 To .ListSciELONet.ListCount - 1
        Set item = CodeScieloNet(.ListSciELONet.list(i), exist)
        If exist Then
            If .ListSciELONet.selected(i) Then
                s(CLng(item.Code)) = "1"
            Else
                s(CLng(item.Code)) = "0"
            End If
        End If
    Next
    End With
    For i = 1 To q
        content = content + s(i)
    Next
    ScieloNetWrite = content
End Function

    
