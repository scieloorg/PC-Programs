VERSION 5.00
Begin VB.Form FrmReplaceIssue 
   BorderStyle     =   3  'Fixed Dialog
   Caption         =   "Form1"
   ClientHeight    =   4200
   ClientLeft      =   45
   ClientTop       =   330
   ClientWidth     =   6600
   Icon            =   "frm_ReplaceIssue.frx":0000
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   ScaleHeight     =   4200
   ScaleWidth      =   6600
   ShowInTaskbar   =   0   'False
   StartUpPosition =   1  'CenterOwner
   Begin VB.CommandButton CmdCancel 
      Caption         =   "Cancel"
      Height          =   375
      Left            =   4440
      TabIndex        =   5
      Top             =   3480
      Width           =   975
   End
   Begin VB.CommandButton CmdOK 
      Caption         =   "OK"
      Height          =   375
      Left            =   3360
      TabIndex        =   4
      Top             =   3480
      Width           =   975
   End
   Begin VB.Frame FramFascId 
      Height          =   855
      Index           =   1
      Left            =   120
      TabIndex        =   15
      Top             =   2520
      Width           =   6375
      Begin VB.TextBox TxtIseqNo 
         Height          =   285
         Index           =   1
         Left            =   120
         MaxLength       =   7
         TabIndex        =   27
         Top             =   480
         Width           =   1095
      End
      Begin VB.TextBox TxtIdPart 
         Height          =   285
         Index           =   1
         Left            =   5160
         TabIndex        =   21
         Top             =   480
         Width           =   975
      End
      Begin VB.TextBox TxtSupplNo 
         Height          =   285
         Index           =   1
         Left            =   4200
         TabIndex        =   3
         Top             =   480
         Width           =   975
      End
      Begin VB.TextBox TxtIssueno 
         Height          =   285
         Index           =   1
         Left            =   3240
         TabIndex        =   2
         Top             =   480
         Width           =   975
      End
      Begin VB.TextBox TxtVolid 
         Height          =   285
         Index           =   1
         Left            =   1320
         TabIndex        =   0
         Top             =   480
         Width           =   975
      End
      Begin VB.TextBox TxtSupplVol 
         Height          =   285
         Index           =   1
         Left            =   2280
         TabIndex        =   1
         Top             =   480
         Width           =   975
      End
      Begin VB.Label LabIseqNo 
         Caption         =   "Label1"
         Height          =   255
         Index           =   1
         Left            =   120
         TabIndex        =   28
         Top             =   240
         Width           =   1095
      End
      Begin VB.Label LabIdPart 
         Caption         =   "ID"
         Height          =   255
         Index           =   1
         Left            =   5160
         TabIndex        =   22
         Top             =   240
         Width           =   855
      End
      Begin VB.Label LabSupplNro 
         Caption         =   "Suppl"
         Height          =   255
         Index           =   1
         Left            =   4200
         TabIndex        =   19
         Top             =   240
         Width           =   855
      End
      Begin VB.Label LabNro 
         Caption         =   "No"
         Height          =   255
         Index           =   1
         Left            =   3240
         TabIndex        =   18
         Top             =   240
         Width           =   855
      End
      Begin VB.Label LabVol 
         Caption         =   "Vol"
         Height          =   255
         Index           =   1
         Left            =   1320
         TabIndex        =   17
         Top             =   240
         Width           =   855
      End
      Begin VB.Label LabSupplVol 
         Caption         =   "Suppl"
         Height          =   255
         Index           =   1
         Left            =   2280
         TabIndex        =   16
         Top             =   240
         Width           =   855
      End
   End
   Begin VB.Frame FramFascId 
      Height          =   855
      Index           =   0
      Left            =   120
      TabIndex        =   10
      Top             =   1440
      Width           =   6375
      Begin VB.TextBox TxtIseqNo 
         BackColor       =   &H8000000C&
         Height          =   285
         Index           =   0
         Left            =   120
         Locked          =   -1  'True
         TabIndex        =   25
         Top             =   480
         Width           =   1095
      End
      Begin VB.TextBox TxtIdPart 
         BackColor       =   &H8000000C&
         Height          =   285
         Index           =   0
         Left            =   5160
         Locked          =   -1  'True
         TabIndex        =   23
         Top             =   480
         Width           =   975
      End
      Begin VB.TextBox TxtSupplNo 
         BackColor       =   &H8000000C&
         Height          =   285
         Index           =   0
         Left            =   4200
         Locked          =   -1  'True
         TabIndex        =   9
         Top             =   480
         Width           =   975
      End
      Begin VB.TextBox TxtIssueno 
         BackColor       =   &H8000000C&
         Height          =   285
         Index           =   0
         Left            =   3240
         Locked          =   -1  'True
         TabIndex        =   8
         Top             =   480
         Width           =   975
      End
      Begin VB.TextBox TxtVolid 
         BackColor       =   &H8000000C&
         Height          =   285
         Index           =   0
         Left            =   1320
         TabIndex        =   6
         Top             =   480
         Width           =   975
      End
      Begin VB.TextBox TxtSupplVol 
         BackColor       =   &H8000000C&
         Height          =   285
         Index           =   0
         Left            =   2280
         Locked          =   -1  'True
         TabIndex        =   7
         Top             =   480
         Width           =   975
      End
      Begin VB.Label LabIseqNo 
         Caption         =   "Label1"
         Height          =   255
         Index           =   0
         Left            =   120
         TabIndex        =   26
         Top             =   240
         Width           =   1095
      End
      Begin VB.Label LabIdPart 
         Caption         =   "ID"
         Height          =   255
         Index           =   0
         Left            =   5160
         TabIndex        =   24
         Top             =   240
         Width           =   855
      End
      Begin VB.Label LabSupplNro 
         Caption         =   "Suppl"
         Height          =   255
         Index           =   0
         Left            =   4200
         TabIndex        =   14
         Top             =   240
         Width           =   855
      End
      Begin VB.Label LabNro 
         Caption         =   "No"
         Height          =   255
         Index           =   0
         Left            =   3240
         TabIndex        =   13
         Top             =   240
         Width           =   855
      End
      Begin VB.Label LabVol 
         Caption         =   "Vol"
         Height          =   255
         Index           =   0
         Left            =   1320
         TabIndex        =   12
         Top             =   240
         Width           =   855
      End
      Begin VB.Label LabSupplVol 
         Caption         =   "Suppl"
         Height          =   255
         Index           =   0
         Left            =   2280
         TabIndex        =   11
         Top             =   240
         Width           =   855
      End
   End
   Begin VB.Label LabMsg 
      Caption         =   "Label1"
      Height          =   855
      Left            =   240
      TabIndex        =   20
      Top             =   240
      Width           =   4935
   End
End
Attribute VB_Name = "FrmReplaceIssue"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private JOURNAL_KEY As String
Private MfnSource As Long
Private SourceIssue As ClsIssue
Private replaced As Boolean

Private Sub CmdCancel_Click()
    Unload Me
End Sub

Private Sub CmdOK_Click()
    Dim MfnIssueId As Long
    Dim resp As VbMsgBoxResult
    Dim issue As ClsIssue
    
    replaced = False
    
    If Len(issueId(TxtVolid(1).text, TxtSupplVol(1).text, TxtIssueno(1).text, TxtSupplNo(1).text, TxtIdPart(1).text)) > 0 Then
    
        MfnIssueId = Issue0.issueDAO.getIssueMfnByIssueId(JOURNAL_KEY, TxtVolid(1).text, TxtSupplVol(1).text, TxtIssueno(1).text, TxtSupplNo(1).text, TxtIdPart(1).text, TxtIseqNo(1).text)
        
        If MfnIssueId > 0 Then
            Call MsgBox(ConfigLabels.getLabel("MsgReplaceIssueAlreadyExists"), vbOKOnly)
        Else
            resp = MsgBox(ConfigLabels.getLabel("MsgReplaceIssue"), vbYesNoCancel + vbDefaultButton2)
            If resp = vbYes Then
                replaced = (Issue0.issueDAO.UpdateIssueId(MfnSource, TxtVolid(1).text, TxtSupplVol(1).text, TxtIssueno(1).text, TxtSupplNo(1).text, SourceIssue.issueorder, TxtIdPart(1).text) > 0)
                Set SourceIssue = Issue0.issueDAO.returnIssue(MfnSource)
                Unload Me
            ElseIf resp = vbNo Then
                Unload Me
            Else
        
            End If
        End If
    Else
        MsgBox ConfigLabels.getLabel("MsgMissingIssueId")
    End If
End Sub

Private Sub Form_Load()
    With ConfigLabels
    FramFascId(0) = .getLabel("Issue_Current")
    FramFascId(1) = .getLabel("Issue_Changeto")
    
    Caption = .getLabel("Issue_Replace")
    
    CmdCancel.Caption = .getLabel("ButtonCancel")
    CmdOK.Caption = .getLabel("ButtonOK")
    LabMsg.Caption = .getLabel("MsgReplaceIssue")
    
    Dim i As Long
    
    For i = 0 To 1
    LabVol(i).Caption = .getLabel("volume")
    LabIdPart(i).Caption = Fields.getLabel("IssueIdPart")
    LabNro(i).Caption = .getLabel("issueno")
    LabSupplNro(i).Caption = .getLabel("IssueSuppl")
    LabSupplVol(i).Caption = .getLabel("VolSuppl")
    LabIseqNo(i).Caption = .getLabel("SequentialNumber")
    Next
    End With
End Sub

Sub ReplaceIssue(journalKey As String, vol As TextBox, supplvol As TextBox, issueno As TextBox, Supplno As TextBox, ComboIdPart As ComboBox, iseqno As TextBox)
    
    MfnSource = Issue0.issueDAO.getIssueMfnByIssueId(journalKey, vol.text, supplvol.text, issueno.text, Supplno.text, ComboIdPart.text, iseqno.text)
    
    Set SourceIssue = Issue0.issueDAO.returnIssue(MfnSource)
    
    If MfnSource > 0 Then
        JOURNAL_KEY = SourceIssue.journal.ISSN
        TxtVolid(0).text = SourceIssue.volume
        TxtSupplVol(0).text = SourceIssue.vsuppl
        TxtIssueno(0).text = SourceIssue.number
        TxtSupplNo(0).text = SourceIssue.suppl
        TxtIdPart(0).text = SourceIssue.idPart
        TxtIseqNo(0).text = SourceIssue.issueorder
        Show vbModal
        
        If replaced Then
            vol.text = SourceIssue.volume
            supplvol.text = SourceIssue.vsuppl
            issueno.text = SourceIssue.number
            Supplno.text = SourceIssue.suppl
            iseqno.text = SourceIssue.issueorder
            ComboIdPart.text = SourceIssue.idPart
        End If
    Else
        MsgBox ConfigLabels.getLabel("MSGISSUENOEXIST")
    End If
End Sub



