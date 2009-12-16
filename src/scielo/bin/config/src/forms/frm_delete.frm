VERSION 5.00
Begin VB.Form FormDel 
   Caption         =   "Fields to Delete"
   ClientHeight    =   3885
   ClientLeft      =   60
   ClientTop       =   345
   ClientWidth     =   6420
   Icon            =   "frm_delete.frx":0000
   LinkTopic       =   "Form1"
   ScaleHeight     =   3885
   ScaleWidth      =   6420
   StartUpPosition =   1  'CenterOwner
   Begin VB.CommandButton CmdOK 
      Caption         =   "OK"
      Height          =   375
      Left            =   4320
      TabIndex        =   2
      Top             =   3360
      Width           =   855
   End
   Begin VB.CommandButton Command2 
      Caption         =   "Cancel"
      Height          =   375
      Left            =   5400
      TabIndex        =   1
      Top             =   3360
      Width           =   855
   End
   Begin VB.ListBox ListDel 
      Height          =   2985
      Left            =   120
      Style           =   1  'Checkbox
      TabIndex        =   0
      Top             =   120
      Width           =   6255
   End
End
Attribute VB_Name = "FormDel"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False

Private DelItens() As Long
Private CountDelItens As Long

Private Sub CmdOK_Click()
    Dim i As Long
    CountDelItens = 0
    For i = 1 To ListDel.ListCount
        If ListDel.selected(i - 1) Then
            CountDelItens = CountDelItens + 1
            ReDim Preserve DelItens(CountDelItens)
            DelItens(CountDelItens) = i
        End If
    Next
    Unload Me
End Sub

Private Sub Command2_Click()
    Unload Me
End Sub

Function DeleteItens(Itens() As Long) As Long
    Dim i As Long
    
    Me.Show vbModal
    
    If CountDelItens > 0 Then
        ReDim Itens(CountDelItens)
        For i = 1 To CountDelItens
            Itens(i) = DelItens(i)
        Next
    End If
    DeleteItens = CountDelItens
End Function

