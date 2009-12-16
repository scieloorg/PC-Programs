VERSION 5.00
Begin VB.Form FormConfigRecord 
   Caption         =   "Check of Configuration"
   ClientHeight    =   3825
   ClientLeft      =   270
   ClientTop       =   1290
   ClientWidth     =   9240
   Icon            =   "ConfigRec.frx":0000
   LinkTopic       =   "Form4"
   PaletteMode     =   1  'UseZOrder
   ScaleHeight     =   3825
   ScaleWidth      =   9240
   Begin VB.Frame FrameView 
      Height          =   3615
      Left            =   120
      TabIndex        =   0
      Top             =   120
      Width           =   9015
      Begin VB.CommandButton Command2 
         Caption         =   "Continue"
         Height          =   375
         Left            =   4320
         TabIndex        =   6
         Top             =   240
         Width           =   855
      End
      Begin VB.CommandButton Command1 
         Caption         =   "Quit"
         Height          =   375
         Left            =   3360
         TabIndex        =   5
         Top             =   240
         Width           =   855
      End
      Begin VB.CommandButton FascCmdAju 
         Caption         =   "Help"
         Height          =   375
         Left            =   2400
         TabIndex        =   4
         Top             =   240
         Width           =   855
      End
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
         TabIndex        =   1
         Top             =   720
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
         TabIndex        =   3
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
         TabIndex        =   2
         Top             =   240
         Width           =   2775
      End
   End
End
Attribute VB_Name = "FormConfigRecord"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Private NormalHeight As Long
Private NormalWidth As Long

Private OldHeight As Long
Private OldWidth As Long

Public Quit As Boolean
Public CheckConfiguration As Boolean

Function CompareConfigurationRecords(PathBase As String, Base As String, DocMarkup As String) As Boolean
    Dim BD  As ClDBDoc
    Dim ret As Boolean
    Dim i   As Long
    Dim label As String
    Dim ValIssue As String
    Dim ValDoc As String
    Dim j As Long
    
  
    Set BD = New ClDBDoc
    If BD.Inicia(PathBase, Base, "Base") Then
        If BD.CheckConfiguration(DocMarkup) Then
            CheckConfiguration = True
        Else
            BD.DocDel (DocMarkup)
        End If
        
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
    Show vbModal
    
    CompareConfigurationRecords = ret
End Function

Private Sub Command1_Click()
    Quit = True
End Sub

Private Sub Command2_Click()
    Quit = False
End Sub

Private Sub Form_Load()
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
    Call Redimensionar(TxtView, x, Y, x, Y)
    
    Call Redimensionar(LabDoc, x, Y, 1, 1)
    Call Redimensionar(LabConfig, x, Y, 1, 1)
    Call Redimensionar(FrameView, x, Y, x, Y)
    Call Redimensionar(FascCmdAju, x, Y, 1, 1)

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

