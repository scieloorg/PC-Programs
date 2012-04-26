VERSION 5.00
Begin VB.Form FormConfig 
   BorderStyle     =   1  'Fixed Single
   Caption         =   "Configuration"
   ClientHeight    =   1200
   ClientLeft      =   450
   ClientTop       =   735
   ClientWidth     =   7800
   Icon            =   "frm_config.frx":0000
   LinkTopic       =   "Form5"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   PaletteMode     =   1  'UseZOrder
   ScaleHeight     =   1200
   ScaleWidth      =   7800
   StartUpPosition =   2  'CenterScreen
   Begin VB.Frame Frame1 
      Height          =   975
      Left            =   120
      TabIndex        =   2
      Top             =   120
      Width           =   6495
      Begin VB.ComboBox ComboIdiomHelp 
         Height          =   315
         Left            =   120
         Style           =   2  'Dropdown List
         TabIndex        =   3
         Tag             =   "ComboIdiomHelp"
         Top             =   480
         Width           =   3255
      End
      Begin VB.Label Label1 
         AutoSize        =   -1  'True
         Caption         =   "Idiom of interface"
         Height          =   195
         Left            =   120
         TabIndex        =   4
         Top             =   240
         Width           =   1215
      End
   End
   Begin VB.CommandButton CmdCan 
      Caption         =   "Cancel"
      Height          =   375
      Left            =   6840
      TabIndex        =   1
      Top             =   720
      Width           =   855
   End
   Begin VB.CommandButton CmdOK 
      Caption         =   "OK"
      Height          =   375
      Left            =   6840
      TabIndex        =   0
      Top             =   240
      Width           =   855
   End
End
Attribute VB_Name = "FormConfig"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Private BrPath As String

Private NormalHeight As Long
Private NormalWidth As Long

Private OldHeight As Long
Private OldWidth As Long


Private Sub Form_Load()
    
    OldHeight = Height
    OldWidth = Width
    NormalHeight = Height
    NormalWidth = Width
    
End Sub



Private Sub CmdCan_Click()
    Unload Me
End Sub

Private Sub CmdOK_Click()
    MousePointer = vbHourglass
    ChangeInterfaceIdiom = CodeIdiom(ComboIdiomHelp.text).code
    MousePointer = vbArrow
    Unload Me
End Sub

Sub OpenConfig()

    With ConfigLabels
    Caption = App.Title + " - " + .getLabel("mnConfiguration")
    Label1.Caption = .getLabel("Config_InterfaceIdiom")
    CmdOK.Caption = .getLabel("ButtonOK")
    CmdCan.Caption = .getLabel("ButtonCancel")
    End With
    Call FillCombo(ComboIdiomHelp, CodeIdiom)
    ComboIdiomHelp.text = CodeIdiom(CurrIdiomHelp).value
    
    Show vbModal
End Sub
