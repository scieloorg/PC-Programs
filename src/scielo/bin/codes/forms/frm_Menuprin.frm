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
         Begin VB.Menu mnRestrictArea 
            Caption         =   "Restrict Area"
         End
         Begin VB.Menu mnCodesCustomization 
            Caption         =   "Customized codes"
         End
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
    'Close isisfn
End Sub

Private Sub mnAbout_Click()
'FIXME
    frmAbout.Label2.Caption = paths("package_version").filename
    frmAbout.Label3.Caption = FileDateTime("codes.exe")
    frmAbout.Show vbModal
End Sub

Private Sub Form_Unload(Cancel As Integer)
    GenerateCodeFile
    
    saveConfig
End Sub


Private Sub mnCodesCustomization_Click()
    Call FrmCodes.loadForm(DBCODESPATH, DBNEWCODEFILE, DBCODESLABEL)
End Sub

Private Sub mnConfig_Click()
    FormConfig.OpenConfig
End Sub

Private Sub mnRestrictArea_Click()
    FormLogin.Show
End Sub

Private Sub mnSair_Click()
    If MsgBox(ConfigLabels.getLabel("msgAskexit"), vbYesNo) = vbYes Then
    
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
    
    mnArquivo.Caption = .getLabel("menuFile")
    mnOpcoes.Caption = .getLabel("menuOptions")
    mnAbout.Caption = .getLabel("menuAbout")
    mnAbrir.Caption = .getLabel("menuOpen")
    mnSair.Caption = .getLabel("menuExit")
    mnConfig.Caption = .getLabel("menuConfiguration")
    mnCodesCustomization.Caption = .getLabel("menuCodesCustomization")
    mnRestrictArea.Caption = .getLabel("menuRestrictArea")
    End With
End Sub

