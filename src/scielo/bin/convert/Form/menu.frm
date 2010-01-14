VERSION 5.00
Object = "{831FDD16-0C5C-11D2-A9FC-0000F8754DA1}#2.0#0"; "Mscomctl.ocx"
Begin VB.Form FormMenu 
   Caption         =   "Converter"
   ClientHeight    =   390
   ClientLeft      =   330
   ClientTop       =   960
   ClientWidth     =   3795
   Icon            =   "menu.frx":0000
   LinkTopic       =   "Form4"
   MaxButton       =   0   'False
   PaletteMode     =   1  'UseZOrder
   ScaleHeight     =   390
   ScaleWidth      =   3795
   Begin VB.DirListBox WorkDir 
      Enabled         =   0   'False
      Height          =   315
      Left            =   3240
      TabIndex        =   0
      Top             =   0
      Visible         =   0   'False
      Width           =   495
   End
   Begin MSComctlLib.TreeView BVDirStruct 
      Height          =   255
      Left            =   2160
      TabIndex        =   1
      Top             =   0
      Visible         =   0   'False
      Width           =   255
      _ExtentX        =   450
      _ExtentY        =   450
      _Version        =   393217
      Style           =   7
      Appearance      =   1
   End
   Begin MSComctlLib.TreeView DirStruct 
      Height          =   255
      Left            =   2760
      TabIndex        =   2
      Top             =   0
      Visible         =   0   'False
      Width           =   255
      _ExtentX        =   450
      _ExtentY        =   450
      _Version        =   393217
      Style           =   7
      Appearance      =   1
   End
   Begin VB.Menu mnArquivo 
      Caption         =   "&File"
      Begin VB.Menu mnAbrirMarkup 
         Caption         =   "Open Markup"
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
Attribute VB_Name = "FormMenu"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Sub SetLabels()
    Caption = InterfaceLabels("formmenu_caption").elem2
    If Len(Currbv) > 0 Then
        Caption = BV(Currbv).BVname + " - " + Caption
        'mnOpenDBList.Enabled = (StrComp(BV(Currbv).Flag_ISODB, "1", vbTextCompare) = 0)
    End If
    
    mnArquivo.Caption = InterfaceLabels("formmenu_file").elem2
    mnAbrirMarkup.Caption = InterfaceLabels("formmenu_openmarkup").elem2
    mnSair.Caption = InterfaceLabels("formmenu_exit").elem2
    mnOpcoes.Caption = InterfaceLabels("formmenu_options").elem2
    mnConfig.Caption = InterfaceLabels("formmenu_config").elem2
    mnAjuda.Caption = InterfaceLabels("formmenu_help").elem2
    mnAbout.Caption = InterfaceLabels("formmenu_about").elem2
    mnContent.Caption = InterfaceLabels("formmenu_content").elem2
    'mnOpenDBList.Caption = InterfaceLabels("formdb_caption").elem2
    
End Sub

Sub OpenMenu()


    SetLabels
    
    Show
End Sub

Private Sub Form_Unload(Cancel As Integer)
    TerminateConverterProgram (False)
    Call IsisAppDelete(AppHandle)
End Sub

Private Sub mnAbout_Click()
    If BV(Currbv).LoadFilestoConverterProgram Then
   
    
    
    frmAbout.Label2.Caption = mainConfig.Item("package_version").elem2
    frmAbout.Label3.Caption = FileDateTime("convert.exe")
    frmAbout.Show vbModal

    End If
    
End Sub

Private Sub mnAbrirMarkup_Click()
    MousePointer = vbHourglass
    If BV(Currbv).LoadFilestoConverterProgram Then FormMarkup.MarkupForm_Open
End Sub

Private Sub mnConfig_Click()
    FormConfig.OpenConfig
End Sub

Private Sub mnContent_Click()
'FIXME_2010
    Call openHelp(mainConfig.Item("Help of Converter").elem2, mainConfig.Item("Help of Converter").elem3)
End Sub

Private Sub mnOpenDB_Click()
    'if bv(currbv).LoadFilestoConverterProgram Then FormBase.OpenBase
End Sub

Private Sub mnOpenDBList_Click()
    If BV(Currbv).LoadFilestoConverterProgram Then FormAdm.OpenForm
End Sub

Private Sub mnSair_Click()
    If Msg.ExitProgram Then TerminateConverterProgram (True)
End Sub
