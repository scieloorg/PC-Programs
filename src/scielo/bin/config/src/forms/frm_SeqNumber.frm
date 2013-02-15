VERSION 5.00
Object = "{6B7E6392-850A-101B-AFC0-4210102A8DA7}#1.3#0"; "Comctl32.ocx"
Begin VB.Form FrmSeqNumber 
   BorderStyle     =   1  'Fixed Single
   Caption         =   "List of Sequential numbers"
   ClientHeight    =   5655
   ClientLeft      =   2040
   ClientTop       =   1755
   ClientWidth     =   7950
   Icon            =   "frm_SeqNumber.frx":0000
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   ScaleHeight     =   5655
   ScaleWidth      =   7950
   StartUpPosition =   2  'CenterScreen
   Begin ComctlLib.ListView ListView1 
      Height          =   4815
      Left            =   120
      TabIndex        =   0
      Top             =   120
      Width           =   7695
      _ExtentX        =   13573
      _ExtentY        =   8493
      View            =   3
      Arrange         =   1
      LabelEdit       =   1
      Sorted          =   -1  'True
      LabelWrap       =   -1  'True
      HideSelection   =   -1  'True
      _Version        =   327682
      ForeColor       =   -2147483640
      BackColor       =   -2147483643
      Appearance      =   1
      NumItems        =   7
      BeginProperty ColumnHeader(1) {0713E8C7-850A-101B-AFC0-4210102A8DA7} 
         Key             =   ""
         Object.Tag             =   ""
         Text            =   "sequential number"
         Object.Width           =   0
      EndProperty
      BeginProperty ColumnHeader(2) {0713E8C7-850A-101B-AFC0-4210102A8DA7} 
         SubItemIndex    =   1
         Key             =   ""
         Object.Tag             =   ""
         Text            =   "sertitle"
         Object.Width           =   2540
      EndProperty
      BeginProperty ColumnHeader(3) {0713E8C7-850A-101B-AFC0-4210102A8DA7} 
         Alignment       =   1
         SubItemIndex    =   2
         Key             =   ""
         Object.Tag             =   ""
         Text            =   "volume"
         Object.Width           =   0
      EndProperty
      BeginProperty ColumnHeader(4) {0713E8C7-850A-101B-AFC0-4210102A8DA7} 
         Alignment       =   1
         SubItemIndex    =   3
         Key             =   ""
         Object.Tag             =   ""
         Text            =   "volume suppl"
         Object.Width           =   0
      EndProperty
      BeginProperty ColumnHeader(5) {0713E8C7-850A-101B-AFC0-4210102A8DA7} 
         Alignment       =   1
         SubItemIndex    =   4
         Key             =   ""
         Object.Tag             =   ""
         Text            =   "number"
         Object.Width           =   0
      EndProperty
      BeginProperty ColumnHeader(6) {0713E8C7-850A-101B-AFC0-4210102A8DA7} 
         Alignment       =   1
         SubItemIndex    =   5
         Key             =   ""
         Object.Tag             =   ""
         Text            =   "number suppl"
         Object.Width           =   0
      EndProperty
      BeginProperty ColumnHeader(7) {0713E8C7-850A-101B-AFC0-4210102A8DA7} 
         SubItemIndex    =   6
         Key             =   ""
         Object.Tag             =   ""
         Text            =   "id part"
         Object.Width           =   2540
      EndProperty
   End
   Begin VB.CommandButton CmdNext 
      Caption         =   "Next"
      Height          =   375
      Left            =   5640
      TabIndex        =   2
      Top             =   5160
      Width           =   975
   End
   Begin VB.CommandButton CmdClose 
      Caption         =   "Close"
      Height          =   375
      Left            =   6840
      TabIndex        =   1
      Top             =   5160
      Width           =   975
   End
End
Attribute VB_Name = "FrmSeqNumber"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private SelectedVolid As String
Private SelectedSupplVol As String
Private SelectedIssueno As String
Private SelectedSupplno As String
Private SelectedIseqno As String
Private SelectedIdPart As String
Private OK As Boolean
Public Sub ViewIseqNo(ISSN As String, volid As String, supplvol As String, issueno As String, Supplno As String, iseqno As String, idPart As String)
    Dim item As ListItem
    Dim i As Long
    Dim q As Long
    Dim mfns() As Long
    Dim Mfn As Long
    Dim MfnIseqNo As Long
    Dim MfnIssueId As Long
    Dim issue As ClsIssue
    
    
    SelectedVolid = ""
    SelectedSupplVol = ""
    SelectedIssueno = ""
    SelectedSupplno = ""
    SelectedIseqno = ""
    
    q = Issue0.issueDAO.getIssuesMfnByISSN(volid, iseqno, ISSN, mfns)
    
    For i = 1 To q
        Mfn = 0
        Set issue = Issue0.issueDAO.returnIssue(mfns(i))
        
        If (StrComp(issue.journal.ISSN, ISSN) = 0) Then
            If (Len(volid) > 0) Then
                If (StrComp(issue.volume, volid) = 0) Then
                    Mfn = mfns(i)
                End If
            ElseIf Len(issueno) > 0 Then
                If (StrComp(issue.number, issueno) = 0) Then
                    Mfn = mfns(i)
                End If
            Else
                Mfn = mfns(i)
            End If
        End If
        If Mfn > 0 Then
            Set item = ListView1.ListItems.add(, , issue.issueorder)
            item.SubItems(1) = issue.journal.shorttitle
            item.SubItems(2) = issue.volume
            item.SubItems(3) = issue.vsuppl
            item.SubItems(4) = issue.number
            item.SubItems(5) = issue.suppl
            item.SubItems(6) = issue.idPart
        End If
    Next
    For i = 1 To ListView1.ColumnHeaders.count
        ListView1.ColumnHeaders(i).Width = ListView1.Width / (ListView1.ColumnHeaders.count * 2)
    Next
    
    ListView1.SortKey = 0
    ListView1.SortOrder = lvwDescending
    ListView1.Sorted = True
    'ListView1.ListItems(item.index).selected = True
    
    
    Show vbModal
    If OK Then
        volid = SelectedVolid
        supplvol = SelectedSupplVol
        issueno = SelectedIssueno
        Supplno = SelectedSupplno
        iseqno = SelectedIseqno
        idPart = SelectedIdPart
    End If
End Sub

Public Sub ViewIseqNo_old(ISSN As String, volid As String, supplvol As String, issueno As String, Supplno As String, iseqno As String, idPart As String)
    Dim item As ListItem
    Dim i As Long
    Dim q As Long
    Dim mfns() As Long
    Dim Mfn As Long
    Dim MfnIseqNo As Long
    Dim MfnIssueId As Long
    Dim issue As ClsIssue
    
    
    SelectedVolid = ""
    SelectedSupplVol = ""
    SelectedIssueno = ""
    SelectedSupplno = ""
    SelectedIseqno = ""
    
    q = Issue0.issueDAO.getIssuesMfnByISSN(volid, issueno, ISSN, mfns)
    
    For i = 1 To q
        Mfn = 0
        Set issue = Issue0.issueDAO.returnIssue(mfns(i))
        
        If (StrComp(issue.journal.ISSN, ISSN) = 0) Then
            If (Len(volid) > 0) Then
                If (StrComp(issue.volume, volid) = 0) Then
                    Mfn = mfns(i)
                End If
            ElseIf Len(issueno) > 0 Then
                If (StrComp(issue.number, issueno) = 0) Then
                    Mfn = mfns(i)
                End If
            Else
                Mfn = mfns(i)
            End If
        End If
        If Mfn > 0 Then
            Set item = ListView1.ListItems.add(, , issue.issueorder)
            item.SubItems(1) = issue.journal.shorttitle
            item.SubItems(2) = issue.volume
            item.SubItems(3) = issue.vsuppl
            item.SubItems(4) = issue.number
            item.SubItems(5) = issue.suppl
            item.SubItems(6) = issue.idPart
        End If
    Next
    For i = 1 To ListView1.ColumnHeaders.count
        ListView1.ColumnHeaders(i).Width = ListView1.Width / (ListView1.ColumnHeaders.count * 2)
    Next
    
    ListView1.SortKey = 0
    ListView1.SortOrder = lvwDescending
    ListView1.Sorted = True
    'ListView1.ListItems(item.index).selected = True
    
    
    Show vbModal
    If OK Then
        volid = SelectedVolid
        supplvol = SelectedSupplVol
        issueno = SelectedIssueno
        Supplno = SelectedSupplno
        iseqno = SelectedIseqno
        idPart = SelectedIdPart
    End If
End Sub
Private Sub CmdClose_Click()
    OK = False
    Unload Me
End Sub

Private Sub CmdNext_Click()
    OK = True
    Unload Me
End Sub

Private Sub Form_Load()
    With ConfigLabels
    CmdNext.Caption = .getLabel("ButtonOK")
    CmdClose.Caption = .getLabel("ButtonClose")
    End With
End Sub

Private Sub ListView1_ColumnClick(ByVal ColumnHeader As ComctlLib.ColumnHeader)
    ListView1.SortKey = ColumnHeader.index - 1
    ListView1.SortOrder = lvwDescending
    ListView1.Sorted = True
    
End Sub

Private Sub ListView1_ItemClick(ByVal item As ComctlLib.ListItem)
    
        SelectedVolid = ListView1.ListItems(item.index).SubItems(2)
        SelectedSupplVol = ListView1.ListItems(item.index).SubItems(3)
        SelectedIssueno = ListView1.ListItems(item.index).SubItems(4)
        SelectedSupplno = ListView1.ListItems(item.index).SubItems(5)
        SelectedIdPart = ListView1.ListItems(item.index).SubItems(6)
        SelectedIseqno = ListView1.ListItems(item.index).text
End Sub
