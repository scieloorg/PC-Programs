VERSION 5.00
Begin VB.Form FormViewLog 
   Caption         =   "View"
   ClientHeight    =   4545
   ClientLeft      =   60
   ClientTop       =   345
   ClientWidth     =   8790
   Icon            =   "ViewLog.frx":0000
   LinkTopic       =   "Form1"
   ScaleHeight     =   4545
   ScaleWidth      =   8790
   StartUpPosition =   1  'CenterOwner
   Begin VB.TextBox TxtViewLog 
      Height          =   4335
      Left            =   120
      Locked          =   -1  'True
      MultiLine       =   -1  'True
      ScrollBars      =   3  'Both
      TabIndex        =   0
      Text            =   "ViewLog.frx":000C
      Top             =   120
      Width           =   8535
   End
End
Attribute VB_Name = "FormViewLog"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private NormalHeight As Long
Private NormalWidth As Long

Private OldHeight As Long
Private OldWidth As Long

Private Sub Form_Load()
    OldHeight = Height
    OldWidth = Width
    NormalHeight = Height
    NormalWidth = Width
    Caption = InterfaceLabels("formViewLog_Caption").elem2
    If Len(Currbv) > 0 Then Caption = BV(Currbv).BVname + " - " + Caption
    
End Sub

Private Sub Form_Resize()
    ResizeForm
End Sub

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

Private Sub Components_Position(x As Double, Y As Double)
    Call Components_ChangeSize(TxtViewLog, x, Y, x, Y)
End Sub

Private Sub Components_ChangeSize(obj As Object, Left As Double, Top As Double, Width As Double, Height As Double)
    obj.Left = Left * obj.Left
    obj.Top = Top * obj.Top
    If Height <> 1 Then obj.Height = CLng(Height * obj.Height)
    If Width <> 1 Then obj.Width = Width * obj.Width
End Sub


