VERSION 5.00
Object = "{6B7E6392-850A-101B-AFC0-4210102A8DA7}#1.3#0"; "Comctl32.ocx"
Object = "{6FBA474E-43AC-11CE-9A0E-00AA0062BB4C}#1.0#0"; "Sysinfo.ocx"
Begin VB.Form FormMenuPrin 
   BorderStyle     =   1  'Fixed Single
   Caption         =   "Config"
   ClientHeight    =   420
   ClientLeft      =   315
   ClientTop       =   945
   ClientWidth     =   4140
   FillStyle       =   0  'Solid
   Icon            =   "frm_Menuprin.frx":0000
   LinkTopic       =   "Form4"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   PaletteMode     =   1  'UseZOrder
   ScaleHeight     =   420
   ScaleWidth      =   4140
   Begin SysInfoLib.SysInfo SysInfo1 
      Left            =   1560
      Top             =   120
      _ExtentX        =   1005
      _ExtentY        =   1005
      _Version        =   393216
   End
   Begin ComctlLib.TreeView DirStruct 
      Height          =   255
      Left            =   2280
      TabIndex        =   0
      Top             =   0
      Visible         =   0   'False
      Width           =   495
      _ExtentX        =   873
      _ExtentY        =   450
      _Version        =   327682
      Style           =   7
      Appearance      =   1
   End
   Begin VB.Menu mnArquivo 
      Caption         =   "&File"
      Begin VB.Menu mnAbrir 
         Caption         =   "Open"
         WindowList      =   -1  'True
         Begin VB.Menu mnSerial 
            Caption         =   "Serials"
            Begin VB.Menu mnNewSerial 
               Caption         =   "New"
            End
            Begin VB.Menu mnExistingSerial 
               Caption         =   "Existing"
            End
            Begin VB.Menu mnRmSerial 
               Caption         =   "Remove"
            End
         End
         Begin VB.Menu mnSection 
            Caption         =   "Sections"
         End
         Begin VB.Menu mnIssues 
            Caption         =   "Issues"
         End
         Begin VB.Menu mnNothing 
            Caption         =   "-"
         End
         Begin VB.Menu mnCodes 
            Caption         =   "Codes"
            Enabled         =   0   'False
         End
      End
      Begin VB.Menu mnsep 
         Caption         =   "-"
      End
      Begin VB.Menu mnSair 
         Caption         =   "Exit"
      End
   End
   Begin VB.Menu mnOpcoes 
      Caption         =   "&Options"
      Begin VB.Menu mnConfig 
         Caption         =   "Configuration"
      End
   End
   Begin VB.Menu mnAjuda 
      Caption         =   "&Help"
      Begin VB.Menu mnContent 
         Caption         =   "Contents"
      End
      Begin VB.Menu mnAbout 
         Caption         =   "About"
      End
   End
End
Attribute VB_Name = "FormMenuPrin"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit


Private Sub Form_Terminate()
    Call IsisAppDelete(AppHandle)
    Close isisfn
End Sub

Private Sub Form_Unload(Cancel As Integer)
    ConfigSet
End Sub

Private Sub mnCodes_Click()
    'Shell
End Sub

Private Sub mnAbout_Click()
    frmAbout.Label2.Caption = Paths("package_version").FileName
    frmAbout.Label3.Caption = FileDateTime("config.exe")
    frmAbout.Show vbModal
End Sub

Private Sub mnContent_Click()
    Call openHelp(Paths("Help of Config").path, Paths("Help of Config").FileName)
End Sub


Private Sub mnConfig_Click()
    FormConfig.OpenConfig
End Sub

Private Sub mnExistingSerial_Click()
    FrmExistingSerial.OpenExistingSerial
End Sub

Private Sub mnIssues_Click()
    'If LoadFiles Then
        Issue0.OpenExistingSerial
        'UnloadFilesIssue
    'Else
    '    FormConfig.Show vbModal
    'End If
End Sub

Private Sub mnNewSerial_Click()
    FrmNewSerial.OpenNewSerial
End Sub

Private Sub mnRmSerial_Click()
    FrmRmSerial.OpenExistingSerial
End Sub

Private Sub mnSair_Click()
    If MsgBox(ConfigLabels.getLabel("MsgExit"), vbYesNo) = vbYes Then
        Unload Me
        End
    End If
End Sub

Sub OpenMenu()
    SetLabels
    Show 'vbModal
End Sub

Sub SetLabels()
    With ConfigLabels
    Caption = Mid(App.Title + " - ", 1, Len(App.Title + " - ") - 2)
    mnArquivo.Caption = .getLabel("mnFile")
    mnOpcoes.Caption = .getLabel("mnOptions")
    mnAbout.Caption = .getLabel("mnAbout")
    mnAbrir.Caption = .getLabel("ButtonOpen")
    mnSair.Caption = .getLabel("mnExit")
    mnAjuda.Caption = .getLabel("mnHelp")
    mnConfig.Caption = .getLabel("mnConfiguration")
    mnContent.Caption = .getLabel("mnContents")
    mnIssues.Caption = .getLabel("mnSerialIssues")
    mnSection.Caption = .getLabel("mnSerialSections")
    mnSerial.Caption = .getLabel("mnSerialTitles")
    mnNewSerial.Caption = .getLabel("mnCreateSerial")
    mnExistingSerial.Caption = .getLabel("mnOpenExistingSerial")
    mnRmSerial.Caption = .getLabel("mnRemoveSerial")
    End With
End Sub

Private Sub mnSection_Click()
    Section1.OpenExistingSerial
End Sub

