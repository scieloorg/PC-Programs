VERSION 5.00
Begin VB.Form FormSeqNo 
   BorderStyle     =   1  'Fixed Single
   Caption         =   "Issue and Sequential Number"
   ClientHeight    =   4575
   ClientLeft      =   2325
   ClientTop       =   2100
   ClientWidth     =   8310
   Icon            =   "frm_iseqno.frx":0000
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   ScaleHeight     =   4575
   ScaleWidth      =   8310
   StartUpPosition =   1  'CenterOwner
   Begin VB.CommandButton CmdCancel 
      Caption         =   "Cancel"
      Height          =   375
      Left            =   6000
      TabIndex        =   1
      Top             =   4080
      Width           =   975
   End
   Begin VB.CommandButton CmdOK 
      Caption         =   "OK"
      Height          =   375
      Left            =   4800
      TabIndex        =   0
      Top             =   4080
      Width           =   975
   End
   Begin VB.Frame Frame1 
      Height          =   3255
      Left            =   120
      TabIndex        =   2
      Top             =   720
      Width           =   8055
      Begin VB.OptionButton OptionIssue 
         Caption         =   "New issue"
         Height          =   615
         Index           =   0
         Left            =   120
         TabIndex        =   27
         Top             =   1560
         Width           =   6615
      End
      Begin VB.OptionButton OptionIssue 
         Caption         =   "Existing issue in database"
         Height          =   255
         Index           =   1
         Left            =   120
         TabIndex        =   26
         Top             =   360
         Width           =   4575
      End
      Begin VB.Frame FramFascId 
         Height          =   855
         Index           =   0
         Left            =   360
         TabIndex        =   15
         Top             =   2280
         Width           =   7455
         Begin VB.TextBox TextIdPart 
            Height          =   285
            Index           =   0
            Left            =   4920
            TabIndex        =   29
            Text            =   "Text2"
            Top             =   480
            Width           =   1095
         End
         Begin VB.TextBox TxtSupplVol 
            Height          =   285
            Index           =   0
            Left            =   1320
            Locked          =   -1  'True
            TabIndex        =   20
            Top             =   480
            Width           =   1215
         End
         Begin VB.TextBox TxtVolid 
            Height          =   285
            Index           =   0
            Left            =   120
            Locked          =   -1  'True
            TabIndex        =   19
            Top             =   480
            Width           =   1215
         End
         Begin VB.TextBox TxtIssueno 
            Height          =   285
            Index           =   0
            Left            =   2520
            Locked          =   -1  'True
            TabIndex        =   18
            Top             =   480
            Width           =   1215
         End
         Begin VB.TextBox TxtIseqno 
            BackColor       =   &H8000000F&
            Height          =   285
            Index           =   0
            Left            =   6120
            Locked          =   -1  'True
            TabIndex        =   17
            Top             =   480
            Width           =   1215
         End
         Begin VB.TextBox TxtSupplNo 
            Height          =   285
            Index           =   0
            Left            =   3720
            Locked          =   -1  'True
            TabIndex        =   16
            Top             =   480
            Width           =   1215
         End
         Begin VB.Label Label1 
            Caption         =   "Label1"
            Height          =   255
            Index           =   0
            Left            =   4920
            TabIndex        =   30
            Top             =   240
            Width           =   975
         End
         Begin VB.Label LabSupplVol 
            AutoSize        =   -1  'True
            Caption         =   "Suppl"
            Height          =   195
            Index           =   0
            Left            =   1320
            TabIndex        =   25
            Top             =   240
            Width           =   405
         End
         Begin VB.Label LabVol 
            AutoSize        =   -1  'True
            Caption         =   "Vol"
            Height          =   195
            Index           =   0
            Left            =   120
            TabIndex        =   24
            Top             =   240
            Width           =   225
         End
         Begin VB.Label LabNro 
            AutoSize        =   -1  'True
            Caption         =   "No"
            Height          =   195
            Index           =   0
            Left            =   2520
            TabIndex        =   23
            Top             =   240
            Width           =   210
         End
         Begin VB.Label LabNroSeq 
            AutoSize        =   -1  'True
            Caption         =   "Seq No"
            Height          =   195
            Index           =   0
            Left            =   6120
            TabIndex        =   22
            Top             =   240
            Width           =   540
         End
         Begin VB.Label LabSupplNro 
            AutoSize        =   -1  'True
            Caption         =   "Suppl"
            Height          =   195
            Index           =   0
            Left            =   3720
            TabIndex        =   21
            Top             =   240
            Width           =   405
         End
      End
      Begin VB.Frame FramFascId 
         Height          =   855
         Index           =   1
         Left            =   360
         TabIndex        =   3
         Top             =   600
         Width           =   7455
         Begin VB.TextBox TextIdPart 
            Height          =   285
            Index           =   1
            Left            =   4920
            TabIndex        =   28
            Text            =   "Text1"
            Top             =   480
            Width           =   975
         End
         Begin VB.TextBox TxtSupplNo 
            Height          =   285
            Index           =   1
            Left            =   3720
            Locked          =   -1  'True
            TabIndex        =   8
            Top             =   480
            Width           =   1215
         End
         Begin VB.TextBox TxtIseqno 
            BackColor       =   &H8000000F&
            Height          =   285
            Index           =   1
            Left            =   6120
            Locked          =   -1  'True
            TabIndex        =   7
            Top             =   480
            Width           =   1215
         End
         Begin VB.TextBox TxtIssueno 
            Height          =   285
            Index           =   1
            Left            =   2520
            Locked          =   -1  'True
            TabIndex        =   6
            Top             =   480
            Width           =   1215
         End
         Begin VB.TextBox TxtVolid 
            Height          =   285
            Index           =   1
            Left            =   120
            Locked          =   -1  'True
            TabIndex        =   5
            Top             =   480
            Width           =   1215
         End
         Begin VB.TextBox TxtSupplVol 
            Height          =   285
            Index           =   1
            Left            =   1320
            Locked          =   -1  'True
            TabIndex        =   4
            Top             =   480
            Width           =   1215
         End
         Begin VB.Label Label1 
            Caption         =   "Label1"
            Height          =   255
            Index           =   1
            Left            =   4920
            TabIndex        =   31
            Top             =   240
            Width           =   975
         End
         Begin VB.Label LabSupplNro 
            AutoSize        =   -1  'True
            Caption         =   "Suppl"
            Height          =   195
            Index           =   1
            Left            =   3720
            TabIndex        =   13
            Top             =   240
            Width           =   405
         End
         Begin VB.Label LabNroSeq 
            AutoSize        =   -1  'True
            Caption         =   "Seq No"
            Height          =   195
            Index           =   1
            Left            =   6120
            TabIndex        =   12
            Top             =   240
            Width           =   540
         End
         Begin VB.Label LabNro 
            AutoSize        =   -1  'True
            Caption         =   "No"
            Height          =   195
            Index           =   1
            Left            =   2520
            TabIndex        =   11
            Top             =   240
            Width           =   210
         End
         Begin VB.Label LabVol 
            AutoSize        =   -1  'True
            Caption         =   "Vol"
            Height          =   195
            Index           =   1
            Left            =   120
            TabIndex        =   10
            Top             =   240
            Width           =   225
         End
         Begin VB.Label LabSupplVol 
            AutoSize        =   -1  'True
            Caption         =   "Suppl"
            Height          =   195
            Index           =   1
            Left            =   1320
            TabIndex        =   9
            Top             =   240
            Width           =   405
         End
      End
   End
   Begin VB.Label LabMsg 
      Caption         =   "Select the issue you want to edit. If its informations are wrong, correct them."
      Height          =   375
      Left            =   120
      TabIndex        =   14
      Top             =   240
      Width           =   6855
   End
End
Attribute VB_Name = "FormSeqNo"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private selected As Long
Private Sub CmdCancel_Click()
    Unload Me
End Sub

Private Sub CmdOK_Click()
    
        If OptionIssue(1).value Then
            'existente, entao quer abrir, informou por engano  o num seq
            
            selected = 1
        Else
            ' novo, trocar o num seq
            selected = 0
        End If
        
        Issue1.TxtVolid.text = TxtVolid(selected).text
        Issue1.TxtIssueno.text = TxtIssueno(selected).text
        Issue1.TxtSupplNo.text = TxtSupplNo(selected).text
        Issue1.TxtSupplVol.text = TxtSupplVol(selected).text
        Issue1.TxtIseqNo.text = TxtIseqNo(selected).text
        Issue1.ComboIssueIdPart.text = TextIdPart(selected).text
        
        Unload Me
        
       
End Sub

Function ReplaceSeqNo(Question2 As String, vol As String, VolSuppl As String, No As String, NoSuppl As String, SeqNo As String, idPart As String, Optional Vol2 As String, Optional VolSuppl2 As String, Optional No2 As String, Optional NoSuppl2 As String, Optional SeqNo2 As String, Optional idPart2 As String) As Boolean
    Dim i As Long
    
    With ConfigLabels
    LabMsg.Caption = .getLabel("IseqNo_MsgIseqNo")
    OptionIssue(1).Caption = .getLabel("ISEQNO_OPENEXISTINGISSUE")
    'OptionIssue(2).Caption = .ISEQNO_OPENEXISTINGISSUE
    OptionIssue(0).Caption = Question2
    CmdCancel.Caption = .getLabel("ButtonCancel")
    CmdOK.Caption = .getLabel("ButtonOK")
    
    For i = 0 To 1
        LabVol(i).Caption = .getLabel("volume")
        Label1(i).Caption = .getLabel("VolSuppl")
        LabNro(i).Caption = .getLabel("issueno")
        LabSupplNro(i).Caption = .getLabel("IssueSuppl")
        LabNroSeq(i).Caption = .getLabel("SequentialNumber")
        Label1(i).Caption = Fields.getLabel("IssueIdPart")
    Next
    
    End With
    
    
    'New
        TxtVolid(0).text = Issue1.TxtVolid.text
        TxtIssueno(0).text = Issue1.TxtIssueno.text
        TxtSupplNo(0).text = Issue1.TxtSupplNo.text
        TxtSupplVol(0).text = Issue1.TxtSupplVol.text
        TxtIseqNo(0).text = Issue1.TxtIseqNo.text
        TextIdPart(0).text = Issue1.ComboIssueIdPart.text
        OptionIssue(1).value = True
    
    'Current
        TxtVolid(1).text = vol
        TxtIssueno(1).text = No
        TxtSupplNo(1).text = NoSuppl
        TxtSupplVol(1).text = VolSuppl
        TxtIseqNo(1).text = SeqNo
        TextIdPart(1).text = idPart
        
        Me.Show vbModal
        ReplaceSeqNo = (selected = 0)
End Function

