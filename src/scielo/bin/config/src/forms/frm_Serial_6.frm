VERSION 5.00
Begin VB.Form SERIAL6 
   BorderStyle     =   1  'Fixed Single
   Caption         =   "Config - Serial's database"
   ClientHeight    =   5460
   ClientLeft      =   45
   ClientTop       =   1335
   ClientWidth     =   7710
   Icon            =   "frm_Serial_6.frx":0000
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
      TabIndex        =   4
      Top             =   5040
      Width           =   975
   End
   Begin VB.CommandButton CmdBack 
      Caption         =   "Back"
      Height          =   375
      Left            =   2760
      TabIndex        =   3
      Top             =   5040
      Width           =   975
   End
   Begin VB.CommandButton CmdClose 
      Caption         =   "Close"
      Height          =   375
      Left            =   6600
      TabIndex        =   6
      Top             =   5040
      Width           =   975
   End
   Begin VB.CommandButton CmdSave 
      Caption         =   "Save"
      Height          =   375
      Left            =   5520
      TabIndex        =   5
      Top             =   5040
      Width           =   975
   End
   Begin VB.Frame FrameSciELO 
      Caption         =   "History of status of publication in SciELO"
      Height          =   4935
      Left            =   120
      TabIndex        =   37
      Top             =   0
      Width           =   7455
      Begin VB.TextBox TextJournalEntryDate 
         Height          =   285
         Index           =   10
         Left            =   120
         TabIndex        =   34
         Top             =   4200
         Width           =   2295
      End
      Begin VB.ComboBox ComboJournalStatus 
         Height          =   315
         Index           =   10
         Left            =   4920
         Style           =   2  'Dropdown List
         TabIndex        =   36
         Top             =   4200
         Width           =   2295
      End
      Begin VB.TextBox TextJournalExitDate 
         Height          =   285
         Index           =   10
         Left            =   2520
         TabIndex        =   35
         Top             =   4200
         Width           =   2295
      End
      Begin VB.TextBox TextJournalEntryDate 
         Height          =   285
         Index           =   9
         Left            =   120
         TabIndex        =   31
         Top             =   3840
         Width           =   2295
      End
      Begin VB.ComboBox ComboJournalStatus 
         Height          =   315
         Index           =   9
         Left            =   4920
         Style           =   2  'Dropdown List
         TabIndex        =   33
         Top             =   3840
         Width           =   2295
      End
      Begin VB.TextBox TextJournalExitDate 
         Height          =   285
         Index           =   9
         Left            =   2520
         TabIndex        =   32
         Top             =   3840
         Width           =   2295
      End
      Begin VB.TextBox TextJournalEntryDate 
         Height          =   285
         Index           =   8
         Left            =   120
         TabIndex        =   28
         Top             =   3480
         Width           =   2295
      End
      Begin VB.ComboBox ComboJournalStatus 
         Height          =   315
         Index           =   8
         Left            =   4920
         Style           =   2  'Dropdown List
         TabIndex        =   30
         Top             =   3480
         Width           =   2295
      End
      Begin VB.TextBox TextJournalExitDate 
         Height          =   285
         Index           =   8
         Left            =   2520
         TabIndex        =   29
         Top             =   3480
         Width           =   2295
      End
      Begin VB.TextBox TextJournalEntryDate 
         Height          =   285
         Index           =   7
         Left            =   120
         TabIndex        =   25
         Top             =   3120
         Width           =   2295
      End
      Begin VB.ComboBox ComboJournalStatus 
         Height          =   315
         Index           =   7
         Left            =   4920
         Style           =   2  'Dropdown List
         TabIndex        =   27
         Top             =   3120
         Width           =   2295
      End
      Begin VB.TextBox TextJournalExitDate 
         Height          =   285
         Index           =   7
         Left            =   2520
         TabIndex        =   26
         Top             =   3120
         Width           =   2295
      End
      Begin VB.TextBox TextJournalEntryDate 
         Height          =   285
         Index           =   6
         Left            =   120
         TabIndex        =   22
         Top             =   2760
         Width           =   2295
      End
      Begin VB.ComboBox ComboJournalStatus 
         Height          =   315
         Index           =   6
         Left            =   4920
         Style           =   2  'Dropdown List
         TabIndex        =   24
         Top             =   2760
         Width           =   2295
      End
      Begin VB.TextBox TextJournalExitDate 
         Height          =   285
         Index           =   6
         Left            =   2520
         TabIndex        =   23
         Top             =   2760
         Width           =   2295
      End
      Begin VB.TextBox TextJournalEntryDate 
         Height          =   285
         Index           =   5
         Left            =   120
         TabIndex        =   19
         Top             =   2400
         Width           =   2295
      End
      Begin VB.ComboBox ComboJournalStatus 
         Height          =   315
         Index           =   5
         Left            =   4920
         Style           =   2  'Dropdown List
         TabIndex        =   21
         Top             =   2400
         Width           =   2295
      End
      Begin VB.TextBox TextJournalExitDate 
         Height          =   285
         Index           =   5
         Left            =   2520
         TabIndex        =   20
         Top             =   2400
         Width           =   2295
      End
      Begin VB.TextBox TextJournalEntryDate 
         Height          =   285
         Index           =   4
         Left            =   120
         TabIndex        =   16
         Top             =   2040
         Width           =   2295
      End
      Begin VB.ComboBox ComboJournalStatus 
         Height          =   315
         Index           =   4
         Left            =   4920
         Style           =   2  'Dropdown List
         TabIndex        =   18
         Top             =   2040
         Width           =   2295
      End
      Begin VB.TextBox TextJournalExitDate 
         Height          =   285
         Index           =   4
         Left            =   2520
         TabIndex        =   17
         Top             =   2040
         Width           =   2295
      End
      Begin VB.TextBox TextJournalEntryDate 
         Height          =   285
         Index           =   3
         Left            =   120
         TabIndex        =   13
         Top             =   1680
         Width           =   2295
      End
      Begin VB.ComboBox ComboJournalStatus 
         Height          =   315
         Index           =   3
         Left            =   4920
         Style           =   2  'Dropdown List
         TabIndex        =   15
         Top             =   1680
         Width           =   2295
      End
      Begin VB.TextBox TextJournalExitDate 
         Height          =   285
         Index           =   3
         Left            =   2520
         TabIndex        =   14
         Top             =   1680
         Width           =   2295
      End
      Begin VB.TextBox TextJournalEntryDate 
         Height          =   285
         Index           =   2
         Left            =   120
         TabIndex        =   10
         Top             =   1320
         Width           =   2295
      End
      Begin VB.ComboBox ComboJournalStatus 
         Height          =   315
         Index           =   2
         Left            =   4920
         Style           =   2  'Dropdown List
         TabIndex        =   12
         Top             =   1320
         Width           =   2295
      End
      Begin VB.TextBox TextJournalExitDate 
         Height          =   285
         Index           =   2
         Left            =   2520
         TabIndex        =   11
         Top             =   1320
         Width           =   2295
      End
      Begin VB.TextBox TextJournalEntryDate 
         Height          =   285
         Index           =   1
         Left            =   120
         TabIndex        =   7
         Top             =   960
         Width           =   2295
      End
      Begin VB.ComboBox ComboJournalStatus 
         Height          =   315
         Index           =   1
         Left            =   4920
         Style           =   2  'Dropdown List
         TabIndex        =   9
         Top             =   960
         Width           =   2295
      End
      Begin VB.TextBox TextJournalExitDate 
         Height          =   285
         Index           =   1
         Left            =   2520
         TabIndex        =   8
         Top             =   960
         Width           =   2295
      End
      Begin VB.TextBox TextJournalExitDate 
         Height          =   285
         Index           =   0
         Left            =   2520
         TabIndex        =   1
         Top             =   600
         Width           =   2295
      End
      Begin VB.ComboBox ComboJournalStatus 
         Height          =   315
         Index           =   0
         Left            =   4920
         Style           =   2  'Dropdown List
         TabIndex        =   2
         Top             =   600
         Width           =   2295
      End
      Begin VB.TextBox TextJournalEntryDate 
         Height          =   285
         Index           =   0
         Left            =   120
         TabIndex        =   0
         Top             =   600
         Width           =   2295
      End
      Begin VB.Label LabJournalExitDate 
         Caption         =   "Data de saída do SciELO"
         Height          =   255
         Left            =   2520
         TabIndex        =   41
         Top             =   360
         Width           =   2295
      End
      Begin VB.Label LabJournalStatus 
         Caption         =   "Causa"
         Height          =   255
         Left            =   4920
         TabIndex        =   40
         Top             =   360
         Width           =   1575
      End
      Begin VB.Label LabJournalEntryDate 
         Caption         =   "Data de entrada no SciELO"
         Height          =   255
         Left            =   120
         TabIndex        =   39
         Top             =   360
         Width           =   2295
      End
   End
   Begin VB.Label LabIndicationMandatoryField 
      Caption         =   "Label1"
      ForeColor       =   &H000000FF&
      Height          =   255
      Left            =   120
      TabIndex        =   38
      Top             =   5040
      Width           =   2415
   End
End
Attribute VB_Name = "SERIAL6"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Public IsBack As Boolean
Private MyMfnTitle As Long
Private JournalStatusAction As New ClsJournalStatusAction
Private Const MAX_LINES_INDEX = 10


Private Sub CmdBack_Click()
    Hide
    IsBack = True
    receiveData
    JOURNAL5.MyOpen (MyMfnTitle)
End Sub

Sub MySetLabels()
    
    With Fields
        FrameSciELO.Caption = .getLabel("ser6_journalStatusHistory")
        LabJournalStatus.Caption = .getLabel("ser6_journalExitStatus")
        LabJournalEntryDate.Caption = .getLabel("ser6_journalEntryDate")
        LabJournalExitDate.Caption = .getLabel("ser6_journalExitDate")
    End With
    
    With ConfigLabels
        LabIndicationMandatoryField.Caption = .getLabel("MandatoryFieldIndication")
        'CommandJournalStatusAdd.Caption = .ser6_Add
        'CommandJournalStatusReplace.Caption = .ser6_Replace
        'CommandJournalStatusModify.Caption = .ser6_Edit
        'CommandJournalStatusRemove.Caption = .ser6_Remove
        
        CmdBack.Caption = .getLabel("ButtonBack")
        CmdClose.Caption = .getLabel("ButtonClose")
        CmdNext.Caption = .getLabel("ButtonNext")
        CmdSave.Caption = .getLabel("ButtonSave")
    End With
    
    Dim i As Long
    Set JournalStatusAction.mycodeStatus = codeHistory
    For i = 0 To MAX_LINES_INDEX
        Call FillCombo(ComboJournalStatus(i), JournalStatusAction.mycodeStatus)
        Call DisplayLine(i, False)
    Next
    
End Sub

Sub MyGetContentFromBase(MfnTitle As Long)
    'JournalStatusAction.setLanguage (CurrCodeIdiom)
    'Set JournalStatusAction.ErrorMessages = ErrorMessages
    'Set JournalStatusAction.myHistory = journalDAO.getHistory(MfnTitle)
    
    JournalStatusAction.loadHistory (MfnTitle)
    
    Call PresentsData
End Sub
Sub MyClearContent()
    Dim i As Long
    
    For i = 0 To MAX_LINES_INDEX
        TextJournalExitDate(lineCount).text = ""
        ComboJournalStatus(lineCount).ListIndex = 0
        TextJournalEntryDate(lineCount).text = ""
    Next
    Call DisplayLine(0, True)
End Sub

Function changed(MfnTitle As Long) As Boolean
    receiveData

    changed = JournalStatusAction.changed(MfnTitle)
End Function
Sub MyOpen(MfnTitle As Long)
    MyMfnTitle = MfnTitle
    
    Left = FormMenuPrin.SysInfo1.WorkAreaWidth / 2 - (Width + FrmInfo.Width) / 2
    Top = FormMenuPrin.SysInfo1.WorkAreaHeight / 2 - Height / 2
    FrmInfo.Top = Top
    FrmInfo.Left = Left + Width
    
    Show
    
    Set JournalStatusAction.mycodeStatus = codeHistory
    Call FrmInfo.ShowHelpMessage(Fields.getHelp("ser6_journalStatusHistory"))
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
    SERIAL7.MyOpen (MyMfnTitle)

End Sub

Private Sub CmdSave_Click()
    MousePointer = vbHourglass
    
    MyMfnTitle = Serial_Save(MyMfnTitle)
    MousePointer = vbArrow
End Sub

Sub fillComoJournalStatus(index As Integer)
    Dim status As String
    
    If Len(ComboJournalStatus(index).text) > 0 Then
        status = getCode(JournalStatusAction.mycodeStatus, ComboJournalStatus(index).text).Code
    Else
        status = "C"
    End If
    
    If status = "C" Then
        If Len(TextJournalExitDate(index).text) > 0 Then
            JournalStatusAction.showWarning ("MISSING_STATUS")
            ComboJournalStatus(index).SetFocus
        End If
    Else
        If Len(TextJournalExitDate(index).text) > 0 Then
            
        Else
            'TextJournalExitDate(index).SetFocus
            ComboJournalStatus(index).ListIndex = 0
        End If
    End If
    If index < MAX_LINES_INDEX Then
        Call DisplayLine(index + 1, (status <> "D"))
    End If

End Sub
Private Sub ComboJournalStatus_LostFocus(index As Integer)
    Call fillComoJournalStatus(index)
End Sub
Private Sub combojournalstatus_change(index As Integer)
    Call fillComoJournalStatus(index)
End Sub
Private Sub ComboJournalStatus_DblClick(index As Integer)
Debug.Print "ComboJournalStatus_DblClick"
End Sub

Private Sub ComboJournalStatus_KeyPress(index As Integer, KeyAscii As Integer)
    Debug.Print "key_press"
End Sub

Private Sub ComboJournalStatus_OLESetData(index As Integer, Data As DataObject, DataFormat As Integer)
    Debug.Print "ComboJournalStatus_OLESetData"
End Sub

Private Sub ComboJournalStatus_Validate(index As Integer, Cancel As Boolean)
    Debug.Print "ComboJournalStatus_Validate"
End Sub

Private Sub Form_QueryUnload(Cancel As Integer, UnloadMode As Integer)
    Call FormQueryUnload(Cancel, UnloadMode)
End Sub

Function WarnMandatoryFields() As Boolean
    Dim warning As String
    Dim i As Long
    
    
    With Fields
    
    warning = warning + .isA_mandatoryField(Serial1.TxtISSN.text, "ser1_issn")
    warning = warning + .isA_mandatoryField(Serial1.TxtSerTitle.text, "ser1_Title")
    warning = warning + .isA_mandatoryField(Serial1.TxtShortTitle.text, "ser1_ShortTitle")
    warning = warning + .isA_mandatoryField(Serial1.TxtISOStitle.text, "ser1_ISOStitle")
    
    
    For i = 1 To idiomsinfo.count
        warning = warning + .isA_mandatoryField(Serial2.TxtMission(i).text, "ser2_Mission")
    Next

    warning = warning + .isA_mandatoryField(Serial2.TxtDescriptors.text, "ser2_Subject")
    
    If Serial2.ListStudyArea.SelCount = 0 Then
        warning = warning + .isA_mandatoryField("", "ser2_StudyArea")
    End If
    If Serial2.List_wok_area.SelCount = 0 Then
        warning = warning + .isA_mandatoryField("", "ser2_wok_subjects")
    End If
    If Serial2.check_wok_scie.value + Serial2.check_wok_ssci.value + Serial2.check_wok_aehci.value = 0 Then
        warning = warning + .isA_mandatoryField("", "ser2_wok_db")
    End If
    
    warning = warning + .isA_mandatoryField(Serial3.ComboTpLit.text, "ser2_LiterType")
    warning = warning + .isA_mandatoryField(Serial3.ComboTreatLev.text, "ser2_TreatLevel")
    warning = warning + .isA_mandatoryField(Serial3.ComboPubLev.text, "ser2_PubLevel")
    
    warning = warning + .isA_mandatoryField(Serial3.TxtInitDate.text, "ser3_InitDate")
    warning = warning + .isA_mandatoryField(Serial3.ComboFreq.text, "ser3_Freq")
    warning = warning + .isA_mandatoryField(Serial3.ComboPubStatus.text, "ser3_PubStatus")
    warning = warning + .isA_mandatoryField(Serial3.ComboAlphabet.text, "ser3_Alphabet")
    If Serial3.ListTextIdiom.SelCount = 0 Then
        warning = warning + .isA_mandatoryField("", "ser3_TxtIdiom")
    End If
    If Serial3.ListAbstIdiom.SelCount = 0 Then
        warning = warning + .isA_mandatoryField("", "ser3_AbstIdiom")
    End If
    warning = warning + .isA_mandatoryField(Serial3.ComboStandard.text, "Issue_Standard")
    If Serial3.ListScheme.SelCount = 0 Then
        warning = warning + .isA_mandatoryField("", "Issue_Scheme")
    End If
    warning = warning + .isA_mandatoryField(Serial4.TxtPublisher.text, "ser3_Publisher")
    warning = warning + .isA_mandatoryField(Serial4.ComboCountry.text, "ser3_PubCountry")
    warning = warning + .isA_mandatoryField(Serial4.TxtPubCity.text, "ser3_PubCity")

    
    warning = warning + .isA_mandatoryField(Serial4.TxtAddress.text, "ser4_Address")
    warning = warning + .isA_mandatoryField(Serial4.TxtEmail.text, "ser4_email")
    warning = warning + .isA_mandatoryField(JOURNAL5.TxtCprighter.text, "ser4_cprighter")
    
    
    warning = warning + .isA_mandatoryField(SERIAL7.TxtSiglum.text, "ser5_siglum")
    warning = warning + .isA_mandatoryField(SERIAL7.TxtPubId.text, "ser5_PubId")
    warning = warning + .isA_mandatoryField(SERIAL7.TxtSiteLocation.text, "ser5_SiteLocation")
    warning = warning + .isA_mandatoryField(SERIAL7.ComboFTP.text, "ser5_FTP")
    
    warning = warning + .is_mandatory_at_least_one(SERIAL7.Text_PISSN.text, "PISSN", SERIAL7.Text_EISSN.text, "EISSN")
    
    warning = warning + .isA_mandatoryField(SERIAL7.ComboUserSubscription.text, "ser5_UserSubscription")
    warning = warning + .isA_mandatoryField(SERIAL7.ComboPublishingModel.text, "ser5_PublishingModel")
    If SERIAL7.ListSciELONet.SelCount = 0 Then warning = warning + .isA_mandatoryField("", "ser5_SciELONet")
    warning = warning + .isA_mandatoryField(SERIAL8.ComboCCode.text, "ser5_CCode")
    warning = warning + .isA_mandatoryField(SERIAL8.TxtDocCreation.text, "ser5_DocCreation")
    warning = warning + .isA_mandatoryField(SERIAL8.TxtCreatDate.text, "ser5_CreatDate")
    warning = warning + .isA_mandatoryField(SERIAL8.TxtDocUpdate.text, "ser5_DocUpdate")
    warning = warning + .isA_mandatoryField(SERIAL8.TxtUpdateDate.text, "ser5_UpdateDate")
    
    warning = warning + .isA_mandatoryField(SERIAL6.TextJournalEntryDate(0).text, "ser6_journalStatusHistory")
    End With
    If Len(warning) > 0 Then
        MsgBox ConfigLabels.getLabel("MsgMandatoryContent") + vbCrLf + warning, vbCritical
    End If
    WarnMandatoryFields = (Len(warning) > 0)
End Function

Private Sub PresentsData()
    Dim lineCount As Long
    Dim i As Long
    
    Dim myHistory As ClsHistory
    Set myHistory = JournalStatusAction.myHistory
    
    lineCount = -1
    For i = 1 To myHistory.count
        If myHistory.item(i).status <> "C" Then
            TextJournalExitDate(lineCount).text = myHistory.item(i).statusDate
            ComboJournalStatus(lineCount).text = getCode(JournalStatusAction.mycodeStatus, myHistory.item(i).status).value
        Else
            lineCount = lineCount + 1
            TextJournalEntryDate(lineCount).text = myHistory.item(i).statusDate
            
            DisplayLine (lineCount)
        End If
    Next
    DisplayLine (0)
    If lineCount < MAX_LINES_INDEX And lineCount >= 0 Then
        If Len(ComboJournalStatus(lineCount).text) > 0 Then
            If getCode(JournalStatusAction.mycodeStatus, ComboJournalStatus(lineCount).text).Code = "S" Then
                DisplayLine (lineCount + 1)
            End If
        End If
    End If
End Sub

Sub receiveData()
    Dim i As Long
    Dim prevStatus As String
    Dim prevStatusDate As String
    
    Dim continue As Boolean
    
    i = -1
    continue = True
    prevStatus = "_"
    prevStatusDate = "00000000"
    JournalStatusAction.myHistory.clean
    
    While continue And i < MAX_LINES_INDEX
        i = i + 1
        If Len(TextJournalEntryDate(i).text) > 0 Then
            Call ValidateAndSet(prevStatusDate, prevStatus, TextJournalEntryDate(i).text, "C")
        End If
        If Len(TextJournalExitDate(i).text) > 0 Then
            Call ValidateAndSet(prevStatusDate, prevStatus, TextJournalExitDate(i).text, getCode(JournalStatusAction.mycodeStatus, ComboJournalStatus(i).text).Code)
        Else
            continue = False
        End If
    Wend
End Sub

Private Sub ValidateAndSet(prevStatusDate As String, prevStatus As String, statusDate As String, status As String)
    If JournalStatusAction.validate(prevStatusDate, prevStatus, statusDate, status) Then
        Call JournalStatusAction.addNewStatus(statusDate, status)
        prevStatusDate = statusDate
        prevStatus = status
    Else
    
    End If
End Sub

Private Sub TextJournalEntryDate_LostFocus(index As Integer)
    Dim prevDate As String
    Dim previousStatus As String
    
    If Len(TextJournalEntryDate(index).text) > 0 Then
        If index > 0 Then
            prevDate = TextJournalExitDate(index - 1).text
            previousStatus = getCode(JournalStatusAction.mycodeStatus, ComboJournalStatus(index - 1).text).Code
        Else
            prevDate = "00000000"
            previousStatus = "_"
        End If
        ' verifica status anterior
        If JournalStatusAction.checkStatus(previousStatus, "C") Then
            If JournalStatusAction.checkDate(prevDate, TextJournalEntryDate(index).text) Then
                If Len(TextJournalExitDate(index).text) > 0 Then
                    If Not JournalStatusAction.checkDate(TextJournalEntryDate(index).text, TextJournalExitDate(index).text) Then
                        TextJournalEntryDate(index).SetFocus
                    End If
                End If
            Else
                TextJournalEntryDate(index).SetFocus
            End If
        Else
            TextJournalEntryDate(index).text = ""
        End If
    End If
End Sub
Private Sub TextJournalEntryDate_change(index As Integer)
    If index > 0 Then
        ComboJournalStatus(index - 1).Enabled = (Len(TextJournalEntryDate(index).text) = 0)
    End If
End Sub
Private Sub TextJournalExitDate_LostFocus(index As Integer)
    Dim prevDate As String
    Dim checkedDates As Boolean
    
    If Len(TextJournalExitDate(index).text) > 0 Then
        If Len(TextJournalEntryDate(index).text) > 0 Then
            prevDate = TextJournalEntryDate(index).text
            
            If JournalStatusAction.checkDate(TextJournalEntryDate(index).text, TextJournalExitDate(index).text) Then
                If index < MAX_LINES_INDEX Then
                    If Len(TextJournalEntryDate(index + 1).text) > 0 Then
                        If JournalStatusAction.checkDate(TextJournalExitDate(index).text, TextJournalEntryDate(index + 1).text) Then
                            checkedDates = True
                        End If
                    Else
                        checkedDates = True
                    End If
                Else
                    checkedDates = True
                End If
            End If
            If checkedDates Then
                If ComboJournalStatus(index).text = "" Then
                    ComboJournalStatus(index).SetFocus
                End If
            Else
                TextJournalExitDate(index).SetFocus
            End If
        Else
            JournalStatusAction.showWarning ("MISSING_ENTRY_DATE")
            TextJournalExitDate(index).text = ""
            TextJournalEntryDate(index).SetFocus
        End If
    Else
        If ComboJournalStatus(index).text <> "" Then
            ComboJournalStatus(index).ListIndex = 0
        End If
    End If
End Sub


Function getDataToSave() As String
    getDataToSave = JournalStatusAction.getDataToSave()
End Function
Sub DisplayLine(index As Long, Optional visible As Boolean = True)
    If Not visible Then
        If Len(TextJournalEntryDate(index).text) > 0 Or Len(TextJournalExitDate(index).text) > 0 Or Len(ComboJournalStatus(index).text) > 0 Then
            visible = True
        End If
    End If

    
    TextJournalEntryDate(index).visible = visible
    TextJournalExitDate(index).visible = visible
    ComboJournalStatus(index).visible = visible

End Sub


