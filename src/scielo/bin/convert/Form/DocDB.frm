VERSION 5.00
Begin VB.Form FormDocDB 
   Caption         =   "Document Database"
   ClientHeight    =   5325
   ClientLeft      =   270
   ClientTop       =   1290
   ClientWidth     =   9240
   Icon            =   "DocDB.frx":0000
   LinkTopic       =   "Form4"
   PaletteMode     =   1  'UseZOrder
   ScaleHeight     =   5325
   ScaleWidth      =   9240
   Begin VB.TextBox TxtSglPer 
      Height          =   195
      Left            =   1920
      TabIndex        =   20
      Text            =   "Text1"
      Top             =   0
      Visible         =   0   'False
      Width           =   1215
   End
   Begin VB.Frame FrameView 
      Height          =   3495
      Left            =   120
      TabIndex        =   14
      Top             =   1800
      Width           =   9015
      Begin VB.TextBox TxtView 
         Alignment       =   2  'Center
         BeginProperty Font 
            Name            =   "Courier New"
            Size            =   9
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   2775
         Left            =   120
         Locked          =   -1  'True
         MultiLine       =   -1  'True
         TabIndex        =   15
         Top             =   600
         Width           =   8775
      End
      Begin VB.Label LabConfig 
         Caption         =   "Config Record"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   12
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H000000FF&
         Height          =   375
         Left            =   120
         TabIndex        =   17
         Top             =   240
         Width           =   2415
      End
      Begin VB.Label LabDoc 
         Alignment       =   1  'Right Justify
         Caption         =   "Document Configuration"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   12
            Charset         =   0
            Weight          =   400
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         ForeColor       =   &H8000000D&
         Height          =   375
         Left            =   6120
         TabIndex        =   16
         Top             =   240
         Width           =   2775
      End
   End
   Begin VB.CommandButton FascCmdCan 
      Caption         =   "Close"
      Height          =   375
      Left            =   8280
      TabIndex        =   13
      Top             =   840
      Width           =   855
   End
   Begin VB.CommandButton FascCmdAju 
      Caption         =   "Help"
      Height          =   375
      Left            =   8280
      TabIndex        =   12
      Top             =   1320
      Width           =   855
   End
   Begin VB.CommandButton CmdRemMfnLivres 
      Caption         =   "Collect Garbage"
      Height          =   495
      Left            =   8280
      TabIndex        =   11
      Top             =   120
      Width           =   855
   End
   Begin VB.Frame FramPer 
      Caption         =   "Serial"
      Height          =   1575
      Left            =   120
      TabIndex        =   6
      Top             =   120
      Width           =   4095
      Begin VB.TextBox TxtSupplVol 
         Height          =   285
         Left            =   960
         TabIndex        =   18
         Top             =   1080
         Width           =   735
      End
      Begin VB.TextBox TxtVol 
         Height          =   285
         Left            =   240
         TabIndex        =   0
         Top             =   1080
         Width           =   735
      End
      Begin VB.ComboBox ComboPer 
         Height          =   315
         ItemData        =   "DocDB.frx":030A
         Left            =   240
         List            =   "DocDB.frx":030C
         Style           =   2  'Dropdown List
         TabIndex        =   10
         Top             =   360
         Width           =   3735
      End
      Begin VB.TextBox TxtNro 
         Height          =   285
         Left            =   1680
         TabIndex        =   1
         Top             =   1080
         Width           =   735
      End
      Begin VB.CommandButton PerCmdOK 
         Caption         =   "View"
         Height          =   375
         Left            =   3360
         TabIndex        =   3
         Top             =   960
         Width           =   615
      End
      Begin VB.TextBox TxtSupplNo 
         Height          =   285
         Left            =   2400
         TabIndex        =   2
         Top             =   1080
         Width           =   735
      End
      Begin VB.Label labSupplvol 
         Caption         =   "Suppl"
         Height          =   255
         Left            =   960
         TabIndex        =   19
         Top             =   840
         Width           =   615
      End
      Begin VB.Label LabVol 
         Caption         =   "Volume"
         Height          =   255
         Left            =   240
         TabIndex        =   9
         Top             =   840
         Width           =   615
      End
      Begin VB.Label LabNro 
         Caption         =   "Number"
         Height          =   255
         Left            =   1680
         TabIndex        =   8
         Top             =   840
         Width           =   735
      End
      Begin VB.Label LabSupplNo 
         AutoSize        =   -1  'True
         Caption         =   "Suppl"
         Height          =   195
         Left            =   2400
         TabIndex        =   7
         Top             =   840
         Width           =   405
      End
   End
   Begin VB.Frame FramArtigos 
      Caption         =   "Documents"
      Enabled         =   0   'False
      Height          =   1575
      Left            =   4320
      TabIndex        =   5
      Top             =   120
      Width           =   3855
      Begin VB.FileListBox ListArtigos 
         Height          =   1260
         Left            =   120
         TabIndex        =   4
         Top             =   240
         Width           =   3615
      End
   End
End
Attribute VB_Name = "FormDocDB"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Private NormalHeight As Long
Private NormalWidth As Long

Private OldHeight As Long
Private OldWidth As Long

Private PathCurr As String

Private Sub Habilita(Flag As Boolean)
    CmdRemMfnLivres.Enabled = Flag
    FramArtigos.Enabled = Flag
    ListArtigos.Enabled = Flag
    FascCmdAju.Enabled = Flag
    CmdRemMfnLivres.Enabled = Flag
End Sub

Private Sub MostrarPeriodicos()
    Dim i As Long
    
    For i = 1 To DBtitle.SerialCount
        ComboPer.AddItem (DBtitle.SerialTitle(i))
    Next
    ComboPer.ListIndex = 0
End Sub

Private Sub ObtemArqSel(arquivos() As String, j As Long)
    Dim i As Long
    
    For i = 0 To ListArtigos.ListCount - 1
        If ListArtigos.Selected(i) Then
            j = j + 1
            ReDim Preserve arquivos(j)
            arquivos(j) = ListArtigos.List(i)
        End If
    Next
End Sub

Sub SelecionaPeriodico()
    Dim Sigla() As String
    Dim q As Long
    
    LimpaCampos
    q = DBtitle.GetFieldContents(ComboPer.Text, ISISTAGS("siglum").value, Sigla)
    If q > 0 Then TxtSglPer.Text = Sigla(q)
    If Len(TxtSglPer.Text) > 0 Then MsgBox ("Serial Siglum is missing in title database.")
End Sub

Private Sub CmdRemMfnLivres_Click()
    CleanDocDB
End Sub

Private Sub ComboPer_Click()
    SelecionaPeriodico
End Sub

Private Sub ComboPer_Change()
    SelecionaPeriodico
End Sub

Private Sub ListArtigos_Click()
    CompareConfigurationRecords (ListArtigos.List(ListArtigos.ListIndex))
End Sub

Private Sub PerCmdOk_Click()
    
    If SetCurrentIssuePath(TxtSglPer.Text, TxtVol.Text, TxtSupplVol.Text, TxtNro.Text, TxtSupplNo.Text, PathCurr) Then
        ListArtigos.Path = PathCurr + Paths("Markup").DirName
        Habilita (True)
    End If
End Sub


Private Sub FascCmdCan_Click()
    Sair
End Sub

Private Function CompareConfigurationRecords(DocMarkup As String) As Boolean
    Dim BD  As ClDBDoc
    Dim ret As Boolean
    Dim i   As Long
    Dim label As String
    Dim ValIssue As String
    Dim ValDoc As String
    Dim j As Long
    
    QtdTotalDocs = ListArtigos.ListCount
    
    Set BD = New ClDBDoc
    If BD.Inicia(PathCurr + Paths("Base").DirName, Paths("Base").FileName, Paths("Base").label) Then
        BD.CheckConfiguration (DocMarkup)
        
        LabDoc.Caption = DocMarkup
        TxtView.Text = ""
        i = 1
        Call BD.GetValuesForComparing(i, label, ValIssue, ValDoc)
        While Len(label) > 0
            For j = 1 To Len(ValIssue) - Len(ValDoc)
                ValDoc = ValDoc + " "
            Next
            For j = 1 To Len(ValDoc) - Len(ValIssue)
                ValIssue = " " + ValIssue
            Next
            
            TxtView.Text = TxtView.Text + ValIssue + " [" + label + "] " + ValDoc + SepLinha
            i = i + 1
            Call BD.GetValuesForComparing(i, label, ValIssue, ValDoc)
        Wend
    End If
    Set BD = Nothing
    
    CompareConfigurationRecords = ret
End Function


Private Sub TxtVol_Change()
    Habilita (False)
End Sub

Private Sub TxtNro_Change()
    Habilita (False)
End Sub

Private Sub LimpaCampos()
    TxtNro.Text = ""
    TxtVol.Text = ""
    TxtSupplNo.Text = ""
    TxtSupplVol.Text = ""
End Sub
Private Sub Form_Load()
    Habilita (False)
    ListArtigos.Pattern = "*.htm;*.html"
    MostrarPeriodicos
    ComboPer.Text = ComboPer.List(0)
    OldHeight = Height
    OldWidth = Width
    NormalHeight = Height
    NormalWidth = Width
End Sub
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
Private Sub Posicionar(x As Double, Y As Double)
    Dim i As Long
    Dim atual As Long
    
    Call Redimensionar(FascCmdCan, x, Y, 1, 1)
    Call Redimensionar(FascCmdAju, x, Y, 1, 1)
    Call Redimensionar(CmdRemMfnLivres, x, Y, 1, 1)
    
    Call Redimensionar(ComboPer, x, Y, x, 1)
        Call Redimensionar(FramPer, x, Y, x, Y)
        Call Redimensionar(LabVol, x, Y, 1, 1)
        Call Redimensionar(LabNro, x, Y, 1, 1)
        Call Redimensionar(labSupplvol, x, Y, 1, 1)
        Call Redimensionar(LabSupplNo, x, Y, 1, 1)
        Call Redimensionar(TxtSupplVol, x, Y, 1, 1)
        Call Redimensionar(TxtSupplNo, x, Y, 1, 1)
        Call Redimensionar(TxtVol, x, Y, x, 1)
        Call Redimensionar(TxtNro, x, Y, x, 1)
    Call Redimensionar(PerCmdOK, x, Y, 1, 1)
    
    
        Call Redimensionar(FramArtigos, x, Y, x, Y)
        Call Redimensionar(ListArtigos, x, Y, x, Y)
    
    Call Redimensionar(LabDoc, x, Y, 1, 1)
    Call Redimensionar(LabConfig, x, Y, 1, 1)
    Call Redimensionar(FrameView, x, Y, x, Y)
    Call Redimensionar(TxtView, x, Y, x, Y)

    
    
        
    
End Sub
Private Sub Redimensionar(obj As Object, Left As Double, Top As Double, Width As Double, Height As Double)
    obj.Left = Left * obj.Left
    obj.Top = Top * obj.Top
    If Height <> 1 Then obj.Height = CLng(Height * obj.Height)
    If Width <> 1 Then obj.Width = Width * obj.Width
End Sub
Private Sub Sair()
    Unload Me
End Sub

