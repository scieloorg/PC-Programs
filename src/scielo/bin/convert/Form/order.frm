VERSION 5.00
Begin VB.Form FormOrder 
   BorderStyle     =   1  'Fixed Single
   Caption         =   "Order"
   ClientHeight    =   1800
   ClientLeft      =   1395
   ClientTop       =   2625
   ClientWidth     =   6450
   Icon            =   "order.frx":0000
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   ScaleHeight     =   1800
   ScaleWidth      =   6450
   StartUpPosition =   2  'CenterScreen
   Begin VB.ComboBox ComboOrd2 
      Height          =   315
      Left            =   5400
      Sorted          =   -1  'True
      Style           =   2  'Dropdown List
      TabIndex        =   8
      Top             =   360
      Width           =   975
   End
   Begin VB.ComboBox ComboOrd1 
      Height          =   315
      Left            =   5400
      Sorted          =   -1  'True
      Style           =   2  'Dropdown List
      TabIndex        =   7
      Top             =   720
      Width           =   975
   End
   Begin VB.CommandButton CmdAju 
      Caption         =   "Help"
      Height          =   375
      Left            =   5520
      TabIndex        =   6
      Top             =   1320
      Width           =   855
   End
   Begin VB.CommandButton CmdCan 
      Caption         =   "Cancel"
      Height          =   375
      Left            =   4560
      TabIndex        =   5
      Top             =   1320
      Width           =   855
   End
   Begin VB.CommandButton CmdOK 
      Caption         =   "OK"
      Height          =   375
      Left            =   3600
      TabIndex        =   4
      Top             =   1320
      Width           =   855
   End
   Begin VB.TextBox TxtArq2 
      Height          =   285
      Left            =   840
      Locked          =   -1  'True
      TabIndex        =   1
      Text            =   "Text2"
      Top             =   360
      Width           =   4455
   End
   Begin VB.TextBox TxtArq1 
      Height          =   285
      Left            =   840
      Locked          =   -1  'True
      TabIndex        =   0
      Text            =   "Text1"
      Top             =   720
      Width           =   4455
   End
   Begin VB.Label Label4 
      AutoSize        =   -1  'True
      Caption         =   "Other"
      Height          =   195
      Left            =   240
      TabIndex        =   10
      Top             =   720
      Width           =   390
   End
   Begin VB.Label Label3 
      AutoSize        =   -1  'True
      Caption         =   "Current"
      Height          =   195
      Left            =   120
      TabIndex        =   9
      Top             =   360
      Width           =   510
   End
   Begin VB.Label Label2 
      AutoSize        =   -1  'True
      Caption         =   "Document"
      Height          =   195
      Left            =   840
      TabIndex        =   3
      Top             =   120
      Width           =   735
   End
   Begin VB.Label Label1 
      AutoSize        =   -1  'True
      Caption         =   "Order"
      Height          =   195
      Left            =   5400
      TabIndex        =   2
      Top             =   120
      Width           =   390
   End
End
Attribute VB_Name = "FormOrder"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Public Ord1 As String
Public Ord2 As String
Public Feito As Boolean

Private Sub CmdCan_Click()
    Unload Me
End Sub

Private Sub cmdOK_Click()
    If StrComp(ComboOrd1.Text, ComboOrd2.Text, vbTextCompare) = 0 Then
        MsgBox "Invalid orders."
    Else
        Ord1 = ComboOrd1.Text
        Ord2 = ComboOrd2.Text
        Feito = True
        Unload Me
    End If
End Sub

