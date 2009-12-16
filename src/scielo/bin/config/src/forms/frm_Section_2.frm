VERSION 5.00
Object = "{6B7E6392-850A-101B-AFC0-4210102A8DA7}#1.3#0"; "Comctl32.ocx"
Begin VB.Form New_Section2 
   BorderStyle     =   1  'Fixed Single
   Caption         =   "Section"
   ClientHeight    =   5625
   ClientLeft      =   1395
   ClientTop       =   2010
   ClientWidth     =   9045
   Icon            =   "frm_Section_2.frx":0000
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   Moveable        =   0   'False
   ScaleHeight     =   5625
   ScaleWidth      =   9045
   StartUpPosition =   2  'CenterScreen
   Begin VB.CommandButton CmdClose 
      Caption         =   "Close"
      Height          =   375
      Left            =   6960
      TabIndex        =   7
      Top             =   5160
      Width           =   855
   End
   Begin VB.CommandButton CmdSave 
      Caption         =   "Save"
      Height          =   375
      Left            =   5880
      TabIndex        =   6
      Top             =   5160
      Width           =   855
   End
   Begin VB.CommandButton CmdAju 
      Caption         =   "Help"
      Height          =   375
      Left            =   8040
      TabIndex        =   8
      Top             =   5160
      Width           =   855
   End
   Begin VB.Frame FramSum 
      Height          =   5055
      Left            =   0
      TabIndex        =   9
      Top             =   0
      Width           =   9015
      Begin VB.Frame FrameSections 
         Caption         =   "Filled Sections"
         Height          =   2775
         Left            =   120
         TabIndex        =   10
         Top             =   240
         Width           =   8775
         Begin ComctlLib.ListView ListView1 
            Height          =   2295
            Left            =   120
            TabIndex        =   21
            Top             =   360
            Width           =   8535
            _ExtentX        =   15055
            _ExtentY        =   4048
            View            =   3
            Sorted          =   -1  'True
            LabelWrap       =   0   'False
            HideSelection   =   -1  'True
            _Version        =   327682
            ForeColor       =   -2147483640
            BackColor       =   -2147483643
            BorderStyle     =   1
            Appearance      =   1
            NumItems        =   4
            BeginProperty ColumnHeader(1) {0713E8C7-850A-101B-AFC0-4210102A8DA7} 
               Key             =   ""
               Object.Tag             =   ""
               Text            =   "seccode"
               Object.Width           =   2540
            EndProperty
            BeginProperty ColumnHeader(2) {0713E8C7-850A-101B-AFC0-4210102A8DA7} 
               SubItemIndex    =   1
               Key             =   ""
               Object.Tag             =   ""
               Text            =   "idiom 1"
               Object.Width           =   2540
            EndProperty
            BeginProperty ColumnHeader(3) {0713E8C7-850A-101B-AFC0-4210102A8DA7} 
               SubItemIndex    =   2
               Key             =   ""
               Object.Tag             =   ""
               Text            =   "idiom 2"
               Object.Width           =   2540
            EndProperty
            BeginProperty ColumnHeader(4) {0713E8C7-850A-101B-AFC0-4210102A8DA7} 
               SubItemIndex    =   3
               Key             =   ""
               Object.Tag             =   ""
               Text            =   "idiom 3"
               Object.Width           =   2540
            EndProperty
         End
      End
      Begin VB.TextBox TxtSections 
         BackColor       =   &H00C0C0C0&
         Height          =   2175
         Index           =   3
         Left            =   5880
         Locked          =   -1  'True
         MultiLine       =   -1  'True
         TabIndex        =   16
         Top             =   240
         Visible         =   0   'False
         Width           =   2775
      End
      Begin VB.TextBox TxtSections 
         BackColor       =   &H00C0C0C0&
         Height          =   2175
         Index           =   1
         Left            =   120
         Locked          =   -1  'True
         MultiLine       =   -1  'True
         TabIndex        =   15
         Top             =   240
         Visible         =   0   'False
         Width           =   2775
      End
      Begin VB.TextBox TxtSections 
         BackColor       =   &H00C0C0C0&
         Height          =   2175
         Index           =   2
         Left            =   3000
         Locked          =   -1  'True
         MultiLine       =   -1  'True
         TabIndex        =   14
         Top             =   240
         Visible         =   0   'False
         Width           =   2775
      End
      Begin VB.Frame FrameSectionEdition 
         Caption         =   "Section Edition"
         Height          =   1815
         Left            =   120
         TabIndex        =   11
         Top             =   3120
         Width           =   8775
         Begin VB.TextBox TxtHeader 
            BackColor       =   &H00FFFFFF&
            Height          =   285
            Index           =   3
            Left            =   5880
            TabIndex        =   24
            Top             =   1080
            Width           =   2775
         End
         Begin VB.TextBox TxtHeader 
            BackColor       =   &H00FFFFFF&
            DataField       =   "TxtHeader"
            Height          =   285
            Index           =   2
            Left            =   3000
            TabIndex        =   23
            Top             =   1080
            Width           =   2775
         End
         Begin VB.TextBox TxtHeader 
            BackColor       =   &H00FFFFFF&
            Height          =   285
            Index           =   1
            Left            =   120
            TabIndex        =   22
            Top             =   1080
            Width           =   2775
         End
         Begin VB.ListBox ListLockedCodes 
            Height          =   255
            Left            =   6120
            TabIndex        =   17
            Top             =   240
            Visible         =   0   'False
            Width           =   2415
         End
         Begin VB.TextBox TxtSecCode 
            Height          =   315
            Left            =   1920
            TabIndex        =   0
            Top             =   240
            Width           =   1935
         End
         Begin VB.CommandButton CmdNew 
            Caption         =   "New"
            Height          =   375
            Left            =   3960
            TabIndex        =   4
            Top             =   240
            Width           =   855
         End
         Begin VB.CommandButton CmdDel 
            Caption         =   "Delete"
            Height          =   375
            Left            =   4920
            TabIndex        =   5
            Top             =   240
            Width           =   855
         End
         Begin VB.TextBox TxtSecTit 
            Height          =   285
            Index           =   2
            Left            =   3000
            TabIndex        =   2
            Top             =   1440
            Width           =   2775
         End
         Begin VB.TextBox TxtSecTit 
            Height          =   285
            Index           =   3
            Left            =   5880
            TabIndex        =   3
            Top             =   1440
            Width           =   2775
         End
         Begin VB.TextBox TxtSecTit 
            Height          =   285
            Index           =   1
            Left            =   120
            TabIndex        =   1
            Top             =   1440
            Width           =   2775
         End
         Begin VB.Label LabSecTit 
            Height          =   255
            Index           =   3
            Left            =   5880
            TabIndex        =   20
            Top             =   840
            Width           =   2175
         End
         Begin VB.Label LabSecTit 
            Height          =   255
            Index           =   2
            Left            =   3000
            TabIndex        =   19
            Top             =   840
            Width           =   2175
         End
         Begin VB.Label LabSecTit 
            Height          =   255
            Index           =   1
            Left            =   120
            TabIndex        =   18
            Top             =   840
            Width           =   2175
         End
         Begin VB.Label LabTitulo 
            AutoSize        =   -1  'True
            Caption         =   "Titles"
            Height          =   195
            Left            =   120
            TabIndex        =   13
            Top             =   600
            Width           =   375
         End
         Begin VB.Label LabCodigo 
            AutoSize        =   -1  'True
            Caption         =   "Code"
            Height          =   195
            Left            =   120
            TabIndex        =   12
            Top             =   240
            Width           =   375
         End
      End
   End
End
Attribute VB_Name = "New_Section2"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Private journal As ClsJournal

Private journalTOCManager As New ClsJournalTOCManager


Private Unlocked As Boolean

Private currentItemClicked As String
Private currentItemClickedIndex As Long
Private currentItemClickedTimes As Long

Sub OpenSection(sertitle As String, IsFromSection As Boolean)
    Dim i As Long
    Dim mfn As Long
    
    
    
    mfn = Serial_CheckExisting(sertitle)
    Set journal = New ClsJournal
    journal.pubid = Serial_TxtContent(mfn, 930)
    
    If Len(journal.pubid) > 0 Then
    
        
        journal.Title = Serial_TxtContent(mfn, 100)
        
        With ConfigLabels
        Caption = App.Title + " - " + SECTION_FORM_CAPTION + sertitle
        CmdAju.Caption = .getLabel("mnHelp")
        CmdClose.Caption = .getLabel("ButtonClose")
        CmdSave.Caption = .getLabel("ButtonSave")
        CmdDel.Caption = .getLabel("Sec_CmdRem")
        CmdNew.Caption = .getLabel("Sec_CmdADD")
        FrameSections.Caption = .getLabel("Sec_FrameFilledSections")
        FrameSectionEdition.Caption = .getLabel("Sec_FrameSectionEdition")
        LabCodigo.Caption = .getLabel("Sec_SectionCode")
        LabTitulo.Caption = .getLabel("Sec_SectionTitle")
        End With
        
        Unlocked = IsFromSection
        CmdDel.Enabled = Unlocked
        
        'Idiomas
        For i = 1 To IdiomsInfo.count
            LabSecTit(i).Caption = IdiomsInfo(i).label + ": "
            ListView1.ColumnHeaders(i + 1).text = IdiomsInfo(i).label
            ListView1.ColumnHeaders(i + 1).Width = ListView1.Width / 5
        Next
        
        
        journal.issn = Serial_TxtContent(mfn, 400)
        journal.shorttitle = Serial_TxtContent(mfn, 150)
        
        Call journalTOCManager.create(journal)
        Call LoadSections(journalTOCManager.toc)
        
        ' reordena e reatribui
        Set journalTOCManager.toc = getNewTOC()
            
        Show vbModal
    Else
        MsgBox ConfigLabels.getLabel("msgTitleIsNotCompleted")
    End If
End Sub

Private Sub CmdClose_Click()
    Unload Me
End Sub

Private Sub CmdNew_Click()
    
    If IslockedCode(TxtSecCode.text) Then
        
    Else
        UpdateTable
        CmdDel.Enabled = True
    End If
    
    'If Unlocked Or (Not IslockedCode(TxtSecCode.text)) Then
    '    UpdateTable
    'Else
    '    MsgBox ConfigLabels.MsgUnchangeableCode
    'End If
    'UpdateTempSections
    clearForm
End Sub

Private Sub CmdAju_Click()
    Call openHelp(Paths("Help of Section").path, Paths("Help of Section").FileName)
End Sub

Private Sub CmdDel_Click()
    Dim i As Long
    Dim k As Long
    Dim message As String
    Dim lvi As ListItem
    
    If Not IslockedCode(TxtSecCode.text) Then
        message = ConfigLabels.getLabel("sec_deletequestion") + vbCrLf
        
        For i = 1 To IdiomsInfo.count
            If Len(TxtSecTit(i).text) > 0 Then message = message + TxtSecCode.text + "-" + TxtSecTit(i).text + vbCrLf
        Next
    
        If MsgBox(message, vbYesNo + vbDefaultButton2) = vbYes Then
            ListView1.ListItems.Remove (ListView1.FindItem(TxtSecCode.text).Index)
        End If
    End If
    clearForm
    
End Sub

Private Sub TXTsecCode_Change()
    ShowSelectedSectitle
End Sub

Private Sub TXTsecCode_Click()
    'ShowSelectedSectitle
    clearForm
End Sub

Private Sub ShowSelectedSectitle()
    Dim i As Long
    Dim k As Long
    Dim l As ListItem
    
    Set l = ListView1.FindItem(TxtSecCode.text)
    If l Is Nothing Then
    
    Else
        k = ListView1.FindItem(TxtSecCode.text).Index
        If TxtSecCode.text = ListView1.ListItems(k).text Then
            For i = 1 To IdiomsInfo.count
                TxtSecTit(i).text = ListView1.ListItems(k).SubItems(i)
            Next
        End If
    End If
    
End Sub



Private Sub LoadSections(toc As ClsTOC)
    Dim i As Long
    Dim j As Long
    
    If toc Is Nothing Then
    
    Else
    For i = 1 To IdiomsInfo.count
        TxtHeader(i).text = toc.names.getItemByLang(IdiomsInfo(i).Code).text
    Next
    For j = 1 To toc.sections.count
        TxtSecCode.text = toc.sections.item(j).sectionCode
        For i = 1 To IdiomsInfo.count
            If toc.sections.item(j).sectionNames.getItemByLang(IdiomsInfo(i).Code) Is Nothing Then
            
            Else
                TxtSecTit(i).text = toc.sections.item(j).sectionNames.getItemByLang(IdiomsInfo(i).Code).text
            End If
            
        Next
        UpdateTable
    Next
    End If
    'ListLockedCodes.Clear
    'For i = 1 To ListView1.ListItems.count
    '    ListLockedCodes.AddItem ListView1.ListItems(i).text
    'Next
    
End Sub




Private Sub ListView1_BeforeLabelEdit(Cancel As Integer)
    Cancel = 1
End Sub

Private Sub ListView1_ColumnClick(ByVal ColumnHeader As ComctlLib.ColumnHeader)
ListView1.SortKey = ColumnHeader.Index - 1
    ListView1.Sorted = True
    ListView1.SortOrder = lvwAscending
End Sub

Private Sub ListView1_ItemClick(ByVal item As ComctlLib.ListItem)
    Dim i As Long
    Dim k As Long
    Dim doit As Boolean
    
    Dim issues As ClsIssues
    Dim Code As String
    
    If currentItemClicked <> item.text Then
        currentItemClicked = item.text
        currentItemClickedTimes = 1
        doit = True
    Else
        currentItemClickedTimes = currentItemClickedTimes + 1
        If currentItemClickedTimes Mod 2 <> 0 Then
            doit = True
        End If
    End If
    
        
    If doit Then
        Code = item.text
        currentItemClickedIndex = item.Index
        If IslockedCode(Code) Then
            clearForm
        Else
            k = item.Index
            TxtSecCode.text = item.text
            For i = 1 To IdiomsInfo.count
                TxtSecTit(i).text = item.SubItems(i)
            Next
        End If
    End If
End Sub

Private Function IslockedCode(Code As String, Optional display As Boolean = True) As Boolean
    Dim issues As ClsIssues
    
    If isValidSectionCode(Code) Then
    If journalTOCManager.whereSectionInUse(Code, "all", issues) Then
        If display Then
            Call displayMsgLockedCode(issues)
        End If
        IslockedCode = True
    End If
    End If
End Function

Private Sub displayMsgLockedCode(issues As ClsIssues)
    Dim Msg As String
    Dim i As Long
    
    Msg = ConfigLabels.getLabel("Sec_UnabledtoChange") & vbCrLf
            
    For i = 1 To issues.count
        Msg = Msg & issues.item(i).issueId & "; "
    Next
    MsgBox Msg
            
End Sub

'-----------------------------------------------------------------------
'-----------------------------------------------------------------------
'--- REVISADOS
'-----------------------------------------------------------------------
'-----------------------------------------------------------------------

Private Sub UpdateTable(Optional argue As Boolean = True)
    Dim i As Long
    Dim lvitem As ListItem
    Dim DONTASK As Boolean
    Dim Replace As Boolean
    Dim answer As VbMsgBoxResult
            
    If areValidSectionTitles(argue) Then
        If isValidSectionCode(TxtSecCode.text) Then
            Set lvitem = ListView1.FindItem(TxtSecCode.text)
            If lvitem Is Nothing Then
                Set lvitem = ListView1.ListItems.add(, TxtSecCode.text, TxtSecCode.text)
            End If
            
            
            For i = 1 To IdiomsInfo.count
                If Len(lvitem.SubItems(i)) > 0 Then
                    If StrComp(lvitem.SubItems(i), TxtSecTit(i).text, vbTextCompare) <> 0 Then
                        answer = MsgBox(ConfigLabels.getLabel("Sec_QMsgReplaceSection") + vbCrLf + "CODE:" + TxtSecCode.text + vbCrLf + "CORRENTE:" + lvitem.SubItems(i) + vbCrLf + "NOVO:" + TxtSecTit(i).text, vbYesNo + vbDefaultButton2)
                        If answer = vbYes Then
                            Replace = True
                        End If
                    Else
                        Replace = True
                    End If
                Else
                    Replace = True
                End If
                If Replace Then
                    lvitem.SubItems(i) = TxtSecTit(i).text
                End If
                TxtSecTit(i).text = ""
            Next
            TxtSecCode.text = ""
        
        End If
    
    End If
    
End Sub
Private Function areValidSectionTitles(argue As Boolean) As Boolean
    Dim i As Long
    Dim validsectit As Boolean
    Dim x As String
    Dim Code As String
    
    For i = 1 To IdiomsInfo.count
        x = x + TxtSecTit(i).text
    Next
        
    If Len(x) > 0 Then
        If journalTOCManager.checkSectionTitles(TxtSecCode.text, x, Code) Then
            validsectit = True
        Else
            MsgBox Replace(ConfigLabels.getLabel("sec_TitlesAlreadyRegistered"), "REPLACE-BY-SECCODE", Code)
        End If
    Else
        MsgBox ConfigLabels.getLabel("Sec_InvalidSecTit")
    End If
    
    areValidSectionTitles = validsectit
End Function
Private Function isValidSectionCode(Code As String, Optional display As Boolean = True) As Boolean
    Dim validseccode As Boolean
    Dim p As Long

    If Len(Code) > 0 Then
        p = InStr(Code, journal.pubid)
        If p = 1 Then
            If Len(Code) = (Len(journal.pubid) + 3) Then
                validseccode = True
            End If
        End If
    End If
    If display And Not validseccode Then
        MsgBox ConfigLabels.getLabel("Sec_InvalidSecCode")
    End If
    isValidSectionCode = validseccode
End Function

Sub clearForm()
    Dim i As Long

    For i = 1 To IdiomsInfo.count
        TxtSecTit(i).text = ""
    Next
    TxtSecCode.text = ""
End Sub

Private Sub CmdSave_Click()
    Section_Save
End Sub

Private Function Section_Save() As Boolean
    Dim r As Boolean
    MousePointer = vbHourglass
    
   Set journalTOCManager.toc = getNewTOC
    journalTOCManager.save
    
    MousePointer = vbArrow
    Section_Save = r
        
End Function

Function Section_ChangedContents() As Boolean
    Section_ChangedContents = Not journalTOCManager.compare(journalTOCManager.toc, getNewTOC())
End Function

Private Sub Form_Unload(Cancel As Integer)
    Dim res As VbMsgBoxResult
    
    If Section_ChangedContents Then
        res = MsgBox(ConfigLabels.getLabel("MsgSaveChanges"), vbYesNoCancel)
        If res = vbYes Then
            Section_Save
            'Unload Me
        ElseIf res = vbNo Then
            'Unload Me
        Else
            Cancel = 1
        End If
    Else
        'Unload Me
    End If
End Sub
Private Function getNewTOC() As ClsTOC
    Dim toc As New ClsTOC
    Dim section As ClsSection
    Dim titleAndLang As ClsTextByLang
    Dim i As Long
    Dim k As Long
    
    ListView1.SortKey = 0
    ListView1.Sorted = True
    ListView1.SortOrder = lvwAscending
    
    Set toc.names = New ColTextByLang
    For i = 1 To IdiomsInfo.count
        Set titleAndLang = New ClsTextByLang
        titleAndLang.lang = IdiomsInfo(i).Code
        titleAndLang.text = TxtHeader(i).text
                
        Call toc.names.add(titleAndLang)
            
    Next
    
    
    For k = 1 To ListView1.ListItems.count
        Set section = New ClsSection
        section.sectionCode = ListView1.ListItems(k).text
        
        For i = 1 To IdiomsInfo.count
            Set titleAndLang = New ClsTextByLang
            titleAndLang.lang = IdiomsInfo(i).Code
            titleAndLang.text = ListView1.ListItems(k).SubItems(i)
    
            section.sectionNames.add titleAndLang
        Next
        toc.sections.add section, section.sectionCode
    Next
    Set getNewTOC = toc
End Function
