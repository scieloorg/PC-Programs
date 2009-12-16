VERSION 5.00
Begin VB.Form FormDelete 
   Caption         =   "Form1"
   ClientHeight    =   4320
   ClientLeft      =   60
   ClientTop       =   345
   ClientWidth     =   7305
   LinkTopic       =   "Form1"
   ScaleHeight     =   4320
   ScaleWidth      =   7305
   StartUpPosition =   3  'Windows Default
   Begin VB.Frame Frame1 
      Caption         =   "Frame1"
      Height          =   4095
      Left            =   120
      TabIndex        =   0
      Top             =   120
      Width           =   7095
      Begin VB.CommandButton CmdClose 
         Caption         =   "Command1"
         Height          =   495
         Left            =   5880
         TabIndex        =   4
         Top             =   840
         Width           =   1095
      End
      Begin VB.CommandButton CmdOK 
         Caption         =   "Command1"
         Height          =   495
         Left            =   5880
         TabIndex        =   3
         Top             =   240
         Width           =   1095
      End
      Begin VB.TextBox TxtWarning 
         Height          =   735
         Left            =   120
         TabIndex        =   2
         Text            =   "T"
         Top             =   240
         Width           =   5535
      End
      Begin VB.TextBox TxtDetail 
         Height          =   2895
         Left            =   120
         TabIndex        =   1
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
