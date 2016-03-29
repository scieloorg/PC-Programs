VERSION 5.00
Begin VB.Form Issue1 
   BorderStyle     =   1  'Fixed Single
   Caption         =   "Issue"
   ClientHeight    =   5520
   ClientLeft      =   1905
   ClientTop       =   1680
   ClientWidth     =   7875
   Icon            =   "frm_issue_1.frx":0000
   LinkTopic       =   "Form4"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   Moveable        =   0   'False
   PaletteMode     =   1  'UseZOrder
   ScaleHeight     =   5520
   ScaleWidth      =   7875
   StartUpPosition =   2  'CenterScreen
   Begin VB.ListBox ListScheme 
      Height          =   60
      Left            =   480
      Style           =   1  'Checkbox
      TabIndex        =   34
      Top             =   5280
      Visible         =   0   'False
      Width           =   255
   End
   Begin VB.CommandButton CmdClose 
      Caption         =   "Close"
      Height          =   375
      Left            =   5880
      TabIndex        =   11
      Top             =   5040
      Width           =   855
   End
   Begin VB.CommandButton FormCmdAju 
      Caption         =   "Help"
      Height          =   375
      Left            =   6840
      TabIndex        =   12
      Top             =   5040
      Width           =   855
   End
   Begin VB.CommandButton CmdReplace 
      Caption         =   "Replace"
      Height          =   375
      Left            =   120
      TabIndex        =   9
      Top             =   5040
      Visible         =   0   'False
      Width           =   1335
   End
   Begin VB.CommandButton CmdDelete 
      Caption         =   "Delete"
      Height          =   375
      Left            =   4200
      TabIndex        =   10
      Top             =   5040
      Width           =   1335
   End
   Begin VB.CommandButton CmdView 
      Caption         =   "Open"
      Height          =   375
      Left            =   2760
      TabIndex        =   8
      Top             =   5040
      Width           =   1335
   End
   Begin VB.Frame FramPer 
      Height          =   4935
      Left            =   120
      TabIndex        =   16
      Top             =   0
      Width           =   7695
      Begin VB.TextBox TxtParallel 
         BackColor       =   &H00C0C0C0&
         Height          =   735
         Left            =   2280
         Locked          =   -1  'True
         MultiLine       =   -1  'True
         TabIndex        =   29
         Top             =   1800
         Width           =   5295
      End
      Begin VB.Frame FramFascId 
         Height          =   855
         Index           =   0
         Left            =   1800
         TabIndex        =   22
         Top             =   3840
         Width           =   5775
         Begin VB.ComboBox ComboIssueIdPart 
            Height          =   315
            Left            =   3120
            TabIndex        =   5
            Text            =   "Combo1"
            Top             =   480
            Width           =   975
         End
         Begin VB.TextBox TxtSuppl 
            Height          =   285
            Left            =   4800
            TabIndex        =   4
            Text            =   "Text1"
            Top             =   0
            Visible         =   0   'False
            Width           =   855
         End
         Begin VB.TextBox TxtSupplVol 
            Height          =   285
            Left            =   840
            TabIndex        =   1
            Top             =   480
            Width           =   735
         End
         Begin VB.TextBox TxtIseqno 
            Height          =   285
            Left            =   4200
            MaxLength       =   7
            TabIndex        =   6
            Top             =   480
            Width           =   975
         End
         Begin VB.CommandButton CmdViewIseqNo 
            Caption         =   "..."
            Height          =   375
            Left            =   5280
            TabIndex        =   7
            Top             =   360
            Width           =   375
         End
         Begin VB.TextBox TxtVolid 
            Height          =   285
            Left            =   120
            TabIndex        =   0
            Top             =   480
            Width           =   735
         End
         Begin VB.TextBox TxtIssueno 
            Height          =   285
            Left            =   1560
            TabIndex        =   2
            Top             =   480
            Width           =   735
         End
         Begin VB.TextBox TxtSupplNo 
            Height          =   285
            Left            =   2280
            TabIndex        =   3
            Top             =   480
            Width           =   735
         End
         Begin VB.Label LabSupplVol 
            Caption         =   "Suppl"
            Height          =   495
            Left            =   840
            TabIndex        =   36
            Top             =   240
            Width           =   735
         End
         Begin VB.Label LabIssueIdPart 
            Caption         =   "LabIssueIdPart"
            Height          =   255
            Left            =   3120
            TabIndex        =   35
            Top             =   240
            Width           =   735
         End
         Begin VB.Label LabVol 
            Caption         =   "Vol"
            Height          =   255
            Left            =   120
            TabIndex        =   26
            Top             =   240
            Width           =   735
         End
         Begin VB.Label LabNro 
            Caption         =   "No"
            Height          =   255
            Left            =   1560
            TabIndex        =   25
            Top             =   240
            Width           =   615
         End
         Begin VB.Label LabNroSeq 
            Caption         =   "Seq No"
            Height          =   255
            Left            =   4200
            TabIndex        =   24
            Top             =   240
            Width           =   975
         End
         Begin VB.Label LabSupplNro 
            Caption         =   "Suppl"
            Height          =   495
            Left            =   2280
            TabIndex        =   23
            Top             =   240
            Width           =   735
         End
      End
      Begin VB.TextBox TxtPubl 
         BackColor       =   &H00C0C0C0&
         Height          =   645
         Left            =   2280
         Locked          =   -1  'True
         MultiLine       =   -1  'True
         TabIndex        =   15
         TabStop         =   0   'False
         Top             =   2640
         Width           =   5295
      End
      Begin VB.Label LabIndicationMandatoryField 
         Caption         =   "Label1"
         ForeColor       =   &H000000FF&
         Height          =   495
         Left            =   240
         TabIndex        =   33
         Top             =   4200
         Width           =   1455
      End
      Begin VB.Label TxtISOStitle 
         BackColor       =   &H00C0C0C0&
         BorderStyle     =   1  'Fixed Single
         Height          =   255
         Left            =   2280
         TabIndex        =   32
         Top             =   1320
         Width           =   5295
      End
      Begin VB.Label LabISOStitle 
         AutoSize        =   -1  'True
         Caption         =   "ISO Short Title"
         Height          =   195
         Left            =   240
         TabIndex        =   31
         Top             =   1320
         Width           =   1035
      End
      Begin VB.Label TxtSertitle 
         BackColor       =   &H00C0C0C0&
         BorderStyle     =   1  'Fixed Single
         Height          =   255
         Left            =   2280
         TabIndex        =   30
         Top             =   240
         Width           =   5295
      End
      Begin VB.Label LabMedlineStitle 
         AutoSize        =   -1  'True
         Caption         =   "Medline Short Title"
         Height          =   195
         Left            =   240
         TabIndex        =   28
         Top             =   960
         Width           =   1320
      End
      Begin VB.Label TxtMedlineStitle 
         BackColor       =   &H00C0C0C0&
         BorderStyle     =   1  'Fixed Single
         Height          =   255
         Left            =   2280
         TabIndex        =   27
         Top             =   960
         Width           =   5295
      End
      Begin VB.Label TxtStitle 
         BackColor       =   &H00C0C0C0&
         BorderStyle     =   1  'Fixed Single
         Height          =   255
         Left            =   2280
         TabIndex        =   13
         Top             =   600
         Width           =   5295
      End
      Begin VB.Label LabTitulo 
         AutoSize        =   -1  'True
         Caption         =   "Title"
         Height          =   195
         Left            =   240
         TabIndex        =   21
         Top             =   240
         Width           =   300
      End
      Begin VB.Label LabTitAbr 
         AutoSize        =   -1  'True
         Caption         =   "Short Title"
         Height          =   195
         Left            =   240
         TabIndex        =   20
         Top             =   600
         Width           =   720
      End
      Begin VB.Label LabTitAlt 
         AutoSize        =   -1  'True
         Caption         =   "Alternatives Titles"
         Height          =   195
         Left            =   240
         TabIndex        =   19
         Top             =   1800
         Width           =   1245
      End
      Begin VB.Label LabISSN 
         AutoSize        =   -1  'True
         Caption         =   "ISSN"
         Height          =   195
         Left            =   240
         TabIndex        =   18
         Top             =   3480
         Width           =   375
      End
      Begin VB.Label TxtISSN 
         BackColor       =   &H00C0C0C0&
         BorderStyle     =   1  'Fixed Single
         Height          =   255
         Left            =   2280
         TabIndex        =   14
         Top             =   3480
         Width           =   1335
      End
      Begin VB.Label LabPubl 
         AutoSize        =   -1  'True
         Caption         =   "Publisher"
         Height          =   195
         Left            =   240
         TabIndex        =   17
         Top             =   2640
         Width           =   645
      End
   End
End
Attribute VB_Name = "Issue1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Private MyMfnTitle As Long

Private NormalHeight As Long
Private NormalWidth As Long
Private OldHeight As Long
Private OldWidth As Long

Public Cidade As String
Public SiglaPeriodico As String
Public Title_Standard As String
Public Title_Scheme As String
Public Title_Freq As String
Public year As String
Public issn_id As String
Public pissn As String
Public eissn As String

Private Sub CmdClose_Click()
    Unload Me
End Sub

Private Sub CmdDelete_Click()
    Dim resp As VbMsgBoxResult
    Dim Mfn As Long
    
    'If Len(Trim(TxtSuppl.text)) > 0 Then
    '    If Len(Trim(TxtIssueno.text)) > 0 Then
    '        TxtSupplNo.text = TxtSuppl.text
    '    Else
    '        TxtSupplVol.text = TxtSuppl.text
    '    End If
    'End If
    If CheckIssueId Then
        Mfn = Issue0.issueDAO.getIssueMfnByIssueId(TxtISSN.Caption, TxtVolid.text, TxtSupplVol.text, TxtIssueno.text, TxtSupplNo.text, ComboIssueIdPart.text, TxtIseqNo.text)
        If Mfn > 0 Then
            resp = MsgBox(ConfigLabels.getLabel("MsgDeleteIssue"), vbYesNo + vbDefaultButton2)
            If resp = vbYes Then
                If Issue0.issueDAO.deleteRecord(Mfn) Then
                    
                    TxtVolid.text = ""
                    TxtSupplVol.text = ""
                    TxtIssueno.text = ""
                    TxtSupplNo.text = ""
                    TxtIseqNo.text = ""
                    ComboIssueIdPart.text = ""
                End If
            End If
        Else
            MsgBox ConfigLabels.getLabel("MSGISSUENOEXIST")
        End If
    Else
    End If
    
End Sub

Private Sub CmdReplace_Click()
    
    If MousePointer = vbArrowQuestion Then
        MousePointer = vbArrow
    Else
        'If Len(Trim(TxtSuppl.text)) > 0 Then
         '   If Len(Trim(TxtIssueno.text)) > 0 Then
         '       TxtSupplNo.text = TxtSuppl.text
        '    Else
        '        TxtSupplVol.text = TxtSuppl.text
        '    End If
        'End If
        If CheckIssueId Then
            Call FrmReplaceIssue.ReplaceIssue(TxtISSN.Caption, TxtVolid, TxtSupplVol, TxtIssueno, TxtSupplNo, ComboIssueIdPart, TxtIseqNo)
        Else
        End If
    End If
    
End Sub

Private Sub CmdView_Click()
    Dim mfnIssue As Long
    
    If MousePointer = vbArrowQuestion Then
        MousePointer = vbArrow
    Else
        If CheckIssueId_Iseqno Then
        
            'If Len(Trim(TxtSuppl.text)) > 0 Then
             '   If Len(Trim(TxtIssueno.text)) > 0 Then
             '       TxtSupplNo.text = TxtSuppl.text
             '   Else
            '        TxtSupplVol.text = TxtSuppl.text
            '    End If
            'End If
            If FindIssueToOpen(mfnIssue, TxtISSN.Caption, TxtVolid.text, TxtSupplVol.text, TxtIssueno.text, TxtSupplNo.text, TxtIseqNo.text, ComboIssueIdPart.text) Then
                Issue2.OpenIssueForm (mfnIssue)
            End If
        End If
    End If
End Sub

Private Sub CmdAju_Click()
    Call openHelp(Paths("Help of Issue").Path, Paths("Help of Issue").FileName)
End Sub

Private Sub CmdViewIseqNo_Click()
    Dim volid As String
    Dim issueno As String
    Dim supplvol As String
    Dim Supplno As String
    Dim iseqno As String
    Dim x As String
    
    MousePointer = vbHourglass
    volid = TxtVolid.text
    
    'If Len(Trim(TxtSuppl.text)) > 0 Then
    '    If Len(Trim(TxtIssueno.text)) > 0 Then
    '        TxtSupplNo.text = TxtSuppl.text
    '    Else
    '        TxtSupplVol.text = TxtSuppl.text
    '    End If
   ' End If
    supplvol = TxtSupplVol.text
    Supplno = TxtSupplNo.text
    
    issueno = TxtIssueno.text
    
    iseqno = TxtIseqNo.text
    x = ComboIssueIdPart.text
    
    Call FrmSeqNumber.ViewIseqNo(TxtISSN.Caption, volid, supplvol, issueno, Supplno, iseqno, x)
    TxtVolid.text = volid
    TxtSupplVol.text = supplvol
    TxtIssueno.text = issueno
    TxtSupplNo.text = Supplno
    TxtIseqNo.text = iseqno
    ComboIssueIdPart.text = x
    
    'TxtSuppl.text = TxtSupplNo.text
    'If Len(TxtSuppl.text) = 0 Then
    '    TxtSuppl.text = TxtSupplVol.text
    'End If
    
    
    MousePointer = vbArrow
End Sub

Private Sub Form_Load()
    OldHeight = Height
    OldWidth = Width
    NormalHeight = Height
    NormalWidth = Width
    'TxtSuppl.text = ""
End Sub

Private Function CheckIssueId_Iseqno() As Boolean
    Dim retorno As Boolean
    Dim n As String
    
    n = Mid(TxtIseqNo.text, 5)
    
    If Len(Trim(TxtVolid.text)) > 0 Then
        retorno = True
    ElseIf Len(Trim(TxtIssueno.text)) > 0 Then
        retorno = True
    End If
    
    If Not retorno Then MsgBox ConfigLabels.getLabel("MsgMissingIssueId")
    
    If Len(Trim(TxtIseqNo.text)) < 5 Or Len(Trim(TxtIseqNo.text)) > 7 Then
        retorno = False
    ElseIf Not (TxtIseqNo.text Like String(Len(TxtIseqNo.text), "#")) Then
        retorno = False
    ElseIf CInt(n) < 1 Or CInt(n) > 999 Then
        retorno = False
    End If
    
    If Not retorno Then
        MsgBox (ConfigLabels.getLabel("MsgInvalidFormatSeqNumber"))
        TxtIseqNo.SetFocus
    Else
        year = Mid(TxtIseqNo.text, 1, 4)
    End If
    
    CheckIssueId_Iseqno = retorno
End Function

Private Function CheckIssueId() As Boolean
    Dim retorno As Boolean

    If Len(Trim(TxtVolid.text)) > 0 Then
        retorno = True
    ElseIf Len(Trim(TxtIssueno.text)) > 0 Then
        retorno = True
    ElseIf Len(Trim(TxtSupplNo.text)) > 0 Then
        retorno = True
    ElseIf Len(Trim(TxtSupplVol.text)) > 0 Then
        retorno = True
    End If
    If TxtIssueno.text = "ahead" Then
        If Len(Trim(TxtIseqNo.text)) > 0 Then
            retorno = True
        End If
    End If
    If Not retorno Then MsgBox ConfigLabels.getLabel("MsgMissingIssueId")
    
    
    CheckIssueId = retorno
End Function

Private Sub Form_Resize()
    Resize
End Sub

Private Sub Resize()
    Dim x As Double
    Dim Y As Double
    
    If WindowState <> vbMinimized Then
        If Height < NormalHeight Then
            'OldHeight = Height
            Height = NormalHeight
        ElseIf Width < NormalWidth Then
            'OldWidth = Width
            Width = NormalWidth
        Else
            x = Width / OldWidth
            Y = Height / OldHeight
            Call Posicionar(x, Y)
            OldHeight = Height
            OldWidth = Width
        End If
    End If
End Sub

Private Sub Redimensionar(obj As Object, Left As Double, Top As Double, Width As Double, Height As Double)
    
End Sub

Private Sub Posicionar(x As Double, Y As Double)
    Call Redimensionar(FramPer, x, Y, x, Y)
    Call Redimensionar(LabTitulo, x, Y, 1, 1)
    Call Redimensionar(TxtSerTitle, x, Y, x, 1)
    Call Redimensionar(LabTitAbr, x, Y, 1, 1)
    Call Redimensionar(TxtStitle, x, Y, x, 1)
    Call Redimensionar(LabTitAlt, x, Y, 1, 1)
    Call Redimensionar(TxtParallel, x, Y, x, 1)
    Call Redimensionar(LabISSN, x, Y, 1, 1)
    Call Redimensionar(TxtISSN, x, Y, x, 1)
    Call Redimensionar(LabPubl, x, Y, 1, 1)
    Call Redimensionar(TxtPubl, x, Y, x, 1)
    
    Call Redimensionar(FramFascId, x, Y, x, Y)
    
    Call Redimensionar(LabVol, x, Y, 1, 1)
    Call Redimensionar(TxtVolid, x, Y, x, 1)
    Call Redimensionar(LabNro, x, Y, 1, 1)
    Call Redimensionar(TxtIssueno, x, Y, x, 1)
    Call Redimensionar(LabIssueIdPart, x, Y, 1, 1)
    Call Redimensionar(TxtSupplVol, x, Y, x, 1)
    Call Redimensionar(LabSupplNro, x, Y, 1, 1)
    Call Redimensionar(TxtSupplNo, x, Y, x, 1)
    Call Redimensionar(LabNroSeq, x, Y, 1, 1)
    Call Redimensionar(TxtIseqNo, x, Y, x, 1)
    
    'Call Redimensionar(CmdGarbageCollection, x, Y, x, Y)
    Call Redimensionar(CmdView, x, Y, x, Y)
    'Call Redimensionar(CmdClose, x, Y, x, Y)
    'Call Redimensionar(CmdAju, x, Y, x, Y)
    
End Sub

Private Sub FormCmdAju_Click()
    Call openHelp(Paths("Help of Issue").Path, Paths("Help of Issue").FileName)
End Sub


Private Sub txtparallel_Click()
    If MousePointer = vbArrowQuestion Then
        MousePointer = vbArrow
    End If
End Sub
Private Sub txtIssueno_Change()
    If MousePointer = vbArrowQuestion Then
        MousePointer = vbArrow
    End If
End Sub

Private Sub TxtSupplNo_Change()
    If Len(Trim(Issue1.TxtIssueno.text)) = 0 Then
        TxtSupplVol.text = Issue1.TxtIssueno.text
        Issue1.TxtIssueno.text = ""
    End If
End Sub

Private Sub TxtVolid_Change()
    If MousePointer = vbArrowQuestion Then
        MousePointer = vbArrow
    End If
End Sub

Sub OpenIssue(sertitle As String)
    
    
    loadIssueIdPart
    MyMfnTitle = Serial_CheckExisting(sertitle)
    If isTitleFormCompleted(MyMfnTitle) Then
        
        TxtSerTitle.Caption = Serial_TxtContent(MyMfnTitle, 100)
        TxtPubl.text = Serial_TxtContent(MyMfnTitle, 480)
        Cidade = Serial_TxtContent(MyMfnTitle, 490)
        SiglaPeriodico = Serial_TxtContent(MyMfnTitle, 930)
        Title_Standard = Serial_ComboContent(CodeStandard, MyMfnTitle, 117)
        Title_Scheme = Serial_TxtContent(MyMfnTitle, 85)
        
        Call FillList(ListScheme, CodeScheme)
        Call Serial_ListContent(ListScheme, CodeScheme, MyMfnTitle, 85)
        Title_Freq = Serial_TxtContent(MyMfnTitle, 380)
        
        TxtISOStitle.Caption = Serial_TxtContent(MyMfnTitle, 151)
        TxtStitle.Caption = Serial_TxtContent(MyMfnTitle, 150)
        TxtMEDLINEStitle.Caption = Serial_TxtContent(MyMfnTitle, 421)
        issn_id = Serial_TxtContent(MyMfnTitle, 400)
        
        Call serial_issn_get(MyMfnTitle, pissn, eissn)
        
        '???
        TxtParallel.text = Serial_TxtContent(MyMfnTitle, 230)
        
        TxtISSN.Caption = issn_id
        With Fields
        LabISSN.Caption = .getLabel("ser1_issn")
        LabNro.Caption = .getLabel("Issueno")
        LabNroSeq.Caption = .getLabel("SequentialNumber")
        LabPubl.Caption = .getLabel("ser3_Publisher")
        LabSupplNro.Caption = .getLabel("IssueSuppl")
        LabIssueIdPart.Caption = .getLabel("IssueIdPart")
        LabTitAbr.Caption = .getLabel("ser1_ShortTitle")
        LabISOStitle.Caption = .getLabel("ser1_ISOStitle")
        LabMEDLINEStitle.Caption = .getLabel("ser4_MedlineStitle")
        LabTitAlt.Caption = .getLabel("ser1_ParallelTitles")
        LabTitulo.Caption = .getLabel("ser1_Title")
        LabVol.Caption = .getLabel("Volume")
        
        End With
        
        With ConfigLabels
        Caption = App.Title + " - " + ISSUE_FORM_CAPTION + sertitle
        LabIndicationMandatoryField.Caption = .getLabel("MandatoryFieldIndication")
        CmdClose.Caption = .getLabel("ButtonClose")
        FormCmdAju.Caption = .getLabel("mnHelp")
        CmdView.Caption = .getLabel("ButtonOpen")
        CmdReplace.Caption = .getLabel("ButtonReplace")
        CmdDelete.Caption = .getLabel("ButtonDelete")
        End With
    
        Show vbModal
    Else
        MsgBox ConfigLabels.getLabel("msgTitleIsNotCompleted")
    End If
End Sub

Private Function FindIssueToOpen(FoundMfn As Long, journalKey As String, vol As String, SVol As String, No As String, SNo As String, iseqno As String, IssueIdPart As String) As Boolean
    Dim resp As Boolean
    Dim resp1 As Boolean
    Dim MfnIseqNo As Long
    Dim MfnIssueId As Long
    Dim issue As ClsIssue
    
    
    Call Issue0.issueDAO.getIssueMfn(journalKey, vol, SVol, No, SNo, iseqno, IssueIdPart, MfnIseqNo, MfnIssueId)
    If MfnIssueId = MfnIseqNo Then
        FoundMfn = MfnIssueId
        resp = True
    ElseIf (MfnIseqNo > 0) Then
        MsgBox ConfigLabels.getLabel("msgSeqNumBelongsToAnotherIssue")
        TxtIseqNo.SetFocus
        
        'CmdViewIseqNo_Click
    ElseIf (MfnIssueId > 0) Then
        'perguntar se deseja alterar o num seq deste issue
        Set issue = Issue0.issueDAO.returnIssue(MfnIssueId)
            
        resp1 = FormSeqNo.ReplaceSeqNo(ConfigLabels.getLabel("ISEQNO_CHANGEISEQNO"), vol, SVol, No, SNo, issue.issueorder, IssueIdPart)
        If resp1 Then
            FoundMfn = Issue0.issueDAO.UpdateIssueId(MfnIssueId, vol, SVol, No, SNo, iseqno, IssueIdPart)
        Else
            FoundMfn = MfnIssueId
        End If
        resp = True
    End If
    
    
    FindIssueToOpen = resp
End Function

Private Sub loadIssueIdPart()
    Dim i As Long
    
    Dim key As String
    Dim value As String
    
    ComboIssueIdPart.Clear
    For i = 1 To issueidparts.count
        ComboIssueIdPart.AddItem issueidparts.item(i).Code
    Next
End Sub
