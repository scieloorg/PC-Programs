VERSION 5.00
Begin VB.Form FormDelete 
   ClientHeight    =   4320
   ClientLeft      =   60
   ClientTop       =   345
   ClientWidth     =   7305
   LinkTopic       =   "Form1"
   ScaleHeight     =   4320
   ScaleWidth      =   7305
   StartUpPosition =   1  'CenterOwner
   Begin VB.Frame Frame1 
      Height          =   4095
      Left            =   120
      TabIndex        =   4
      Top             =   120
      Width           =   7095
      Begin VB.CommandButton CmdCancel 
         Caption         =   "Command1"
         Height          =   495
         Left            =   5880
         TabIndex        =   0
         Top             =   840
         Width           =   1095
      End
      Begin VB.CommandButton CmdDelete 
         Caption         =   "Command1"
         Height          =   495
         Left            =   5880
         TabIndex        =   1
         Top             =   240
         Width           =   1095
      End
      Begin VB.TextBox TxtWarning 
         Height          =   735
         Left            =   120
         MultiLine       =   -1  'True
         ScrollBars      =   2  'Vertical
         TabIndex        =   2
         Top             =   240
         Width           =   5535
      End
      Begin VB.TextBox TxtDetail 
         Height          =   2895
         Left            =   120
         MultiLine       =   -1  'True
         ScrollBars      =   2  'Vertical
         TabIndex        =   3
         Top             =   1080
         Width           =   5535
      End
   End
End
Attribute VB_Name = "FormDelete"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit


Private NormalHeight As Long
Private NormalWidth As Long

Private OldHeight As Long
Private OldWidth As Long

Private returnDelete As Boolean
Function Delete(dbname As String, DBInfo As String) As Boolean
    
    Caption = InterfaceLabels("formdelete_Caption").elem2
    TxtWarning.Text = InterfaceLabels("formdelete_warning").elem2 + Chr(13) + Chr(10) + dbname
    TxtDetail.Text = DBInfo
    CmdDelete.Caption = InterfaceLabels("CmdDelete").elem2
    CmdCancel.Caption = InterfaceLabels("cmdcancel").elem2
    
    Show vbModal
    Delete = returnDelete
End Function

Private Sub CmdCancel_Click()
    returnDelete = False
    Unload Me
End Sub

Private Sub CmdDelete_Click()
    returnDelete = True
    Unload Me
End Sub

Private Sub Form_Resize()
    ResizeForm
End Sub

'-----------------------------------------------------------------------
'ResizeForm - Change the size of all form objects
'-----------------------------------------------------------------------
Private Sub ResizeForm()
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
            Call Components_Position(x, Y)
            OldHeight = Height
            OldWidth = Width
        End If
    End If
End Sub

'-----------------------------------------------------------------------
'Components_Position - Position the form objects
'x  - coeficient to dimension the width object
'y  - coeficient to dimension the height object
'-----------------------------------------------------------------------
Private Sub Components_Position(x As Double, Y As Double)
    
    Call Components_ChangeSize(Frame1, x, Y, x, Y)
    Call Components_ChangeSize(CmdDelete, x, Y, x, 1)
    Call Components_ChangeSize(CmdCancel, x, Y, x, 1)
    Call Components_ChangeSize(TxtWarning, x, Y, x, Y)
    Call Components_ChangeSize(TxtDetail, x, Y, x, Y)
End Sub

'-----------------------------------------------------------------------
'Components_ChangeSize  - Change the size of a object of the form
'obj    - the form object
'Left   -
'Top    -
'Width  -
'Height -
'-----------------------------------------------------------------------
Private Sub Components_ChangeSize(obj As Object, Left As Double, Top As Double, Width As Double, Height As Double)
    obj.Left = Left * obj.Left
    obj.Top = Top * obj.Top
    If Height <> 1 Then obj.Height = CLng(Height * obj.Height)
    If Width <> 1 Then obj.Width = Width * obj.Width
End Sub
Private Sub Form_Load()
    
    OldHeight = Height
    OldWidth = Width
    NormalHeight = Height
    NormalWidth = Width
    
End Sub



