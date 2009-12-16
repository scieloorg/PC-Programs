VERSION 5.00
Begin VB.Form FormConfig 
   BorderStyle     =   1  'Fixed Single
   Caption         =   "Configuration"
   ClientHeight    =   1260
   ClientLeft      =   450
   ClientTop       =   735
   ClientWidth     =   8010
   Icon            =   "frmConfig.frx":0000
   LinkTopic       =   "Form5"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   PaletteMode     =   1  'UseZOrder
   ScaleHeight     =   1260
   ScaleWidth      =   8010
   StartUpPosition =   2  'CenterScreen
   Begin VB.Frame Frame1 
      Height          =   1095
      Left            =   120
      TabIndex        =   3
      Top             =   120
      Width           =   6615
      Begin VB.ComboBox ComboBV 
         Height          =   315
         Left            =   3480
         TabIndex        =   5
         Text            =   "Combo1"
         Top             =   480
         Visible         =   0   'False
         Width           =   2895
      End
      Begin VB.ComboBox ComboIdiomHelp 
         Height          =   315
         Left            =   120
         Style           =   2  'Dropdown List
         TabIndex        =   0
         Tag             =   "ComboIdiomHelp"
         Top             =   480
         Width           =   3255
      End
      Begin VB.Label LabBV 
         Caption         =   "Virtual Library"
         Height          =   255
         Left            =   3480
         TabIndex        =   6
         Top             =   240
         Visible         =   0   'False
         Width           =   1575
      End
      Begin VB.Label LabIdiomInterf 
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
      TabIndex        =   2
      Top             =   720
      Width           =   1095
   End
   Begin VB.CommandButton CmdOK 
      Caption         =   "OK"
      Height          =   375
      Left            =   6840
      TabIndex        =   1
      Top             =   240
      Width           =   1095
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

Private Sub cmdOK_Click()
    MousePointer = vbHourglass
    'ChangeInterfaceIdiom = CodeIdiom(ComboIdiomHelp.Text).code
    Currbv = ComboBV.text
    CurrIdiomHelp = ComboIdiomHelp.text
    MousePointer = vbArrow
'    if bv(currbv).LoadFilestoConverterProgram Then
'        Unload Me
'    End If
    ConfigSet
    Unload Me
End Sub

Sub OpenConfig()
    Dim i As Long
    
    ComboIdiomHelp.Clear
    For i = 1 To IdiomHelp.Count
        ComboIdiomHelp.AddItem IdiomHelp(i).Label
    Next
    ComboIdiomHelp.text = CurrIdiomHelp
    
    ComboBV.Clear
    For i = 1 To BV.Count
        ComboBV.AddItem BV(i).BVname
    Next
    If Len(Currbv) > 0 Then ComboBV.text = BV(Currbv).BVname
    'With ConfigLabels
    'Caption = PROGRAM_CAPTION + .mnConfiguration
    'Frame1.Caption = .Config_WebBrowserPath
    'Label1.Caption = .Config_InterfaceIdiom
    'CmdFind.Caption = .Config_FindPath
    'CmdOK.Caption = .ButtonOK
    'CmdCan.Caption = .ButtonCancel
    'CmdAjuda.Caption = .mnHelp
    'End With
    
    Caption = InterfaceLabels("formConfig_Caption").elem2
    If Len(Currbv) > 0 Then Caption = BV(Currbv).BVname + " - " + Caption
    
    LabIdiomInterf.Caption = InterfaceLabels("formConfig_LabIdiomInterf").elem2
    LabBV.Caption = InterfaceLabels("formConfig_LabBV").elem2
    CmdOK.Caption = InterfaceLabels("CmdOK").elem2
    CmdCan.Caption = InterfaceLabels("CmdCancel").elem2
    
    
    
    
    
    'Call FillCombo(ComboIdiomHelp, CodeIdiom)
    'ComboIdiomHelp.ListIndex = 0
    
    Show vbModal
End Sub
