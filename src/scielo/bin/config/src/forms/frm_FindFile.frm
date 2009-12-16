VERSION 5.00
Begin VB.Form frmFindBrowser 
   BorderStyle     =   1  'Fixed Single
   Caption         =   "Find Web Browser Program"
   ClientHeight    =   3315
   ClientLeft      =   45
   ClientTop       =   330
   ClientWidth     =   4830
   Icon            =   "frm_FindFile.frx":0000
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   ScaleHeight     =   3315
   ScaleWidth      =   4830
   StartUpPosition =   2  'CenterScreen
   Begin VB.CommandButton CmdCancel 
      Caption         =   "Cancel"
      Height          =   375
      Left            =   3720
      TabIndex        =   5
      Top             =   720
      Width           =   975
   End
   Begin VB.CommandButton CmdOK 
      Caption         =   "OK"
      Height          =   375
      Left            =   3720
      TabIndex        =   4
      Top             =   240
      Width           =   975
   End
   Begin VB.Frame Frame1 
      Height          =   3255
      Left            =   0
      TabIndex        =   0
      Top             =   0
      Width           =   3495
      Begin VB.FileListBox File1 
         Height          =   1260
         Left            =   120
         Pattern         =   "*.exe"
         TabIndex        =   3
         Top             =   1920
         Width           =   3255
      End
      Begin VB.DriveListBox Drive1 
         Height          =   315
         Left            =   120
         TabIndex        =   2
         Top             =   240
         Width           =   3255
      End
      Begin VB.DirListBox Dir1 
         Height          =   1215
         Left            =   120
         TabIndex        =   1
         Top             =   600
         Width           =   3255
      End
   End
End
Attribute VB_Name = "frmFindBrowser"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Private BrwPath As String
Private Canceled As Boolean

Private Sub CmdCancel_Click()
    Canceled = True
    Unload Me
End Sub

Private Sub CmdOK_Click()
    If Len(File1.FileName) > 0 Then
        BrwPath = File1.Path + "\" + File1.FileName
        Unload Me
    End If
End Sub

Private Sub Dir1_Change()
    File1.Path = Dir1.Path
    File1.Pattern = "*.exe"
End Sub

Private Sub Drive1_Change()
    Dir1.Path = Drive1.Drive
End Sub

Sub ViewPath()
    Dim Path As String
    Dim File As String
    Dim p As Long
    
    Path = BrwPath
    
    If (Len(Dir(Path)) > 0) And (Len(Path) > 0) Then
        Drive1.Drive = Mid(Path, 1, 2)
        
        File = Path
        
        p = InStr(File, "\")
        While p > 0
            File = Mid(File, p + 1)
            p = InStr(File, "\")
        Wend
        p = InStr(Path, File)
        
        Dir1.Path = Mid(Path, 1, p - 2)
        File1.FileName = File
    End If
    
    Me.Show vbModal
        
    BrowserPath = BrwPath
    
End Sub

Function FindBrowserPath() As String
    BrwPath = BrowserPath
    
    If (Len(Dir(BrwPath)) = 0) Or (Len(BrwPath) = 0) Then
        BrwPath = ""
        While (Len(BrwPath) = 0) And (Not Canceled)
            Me.Show vbModal
        Wend
        
    End If
    BrowserPath = BrwPath
    FindBrowserPath = BrwPath
End Function

Sub CallBrowser(helpPath As String, helpFile As String)
    Dim BrowserEXE As String
    
    BrowserEXE = FindBrowserPath
    If Len(BrowserEXE) > 0 Then
        'If FileExist(helpPath, IdiomsInfo(CurrIdiomHelp).Code + helpFile) Then
            Shell BrowserEXE + " " + helpPath + "\" + IdiomsInfo(CurrIdiomHelp).Code + helpFile
        
        'End If
    Else
        MsgBox "No Web Browser was selected."
    End If
End Sub

Private Sub Form_Load()
    Caption = App.Title + " - " + ConfigLabels.getLabel("Config_WebBrowserPath")
    CmdOK.Caption = ConfigLabels.getLabel("ButtonOK")
    CmdCancel.Caption = ConfigLabels.getLabel("ButtonCancel")
    
End Sub
