VERSION 5.00
Begin VB.Form frmFindBrowser 
   Caption         =   "Find Web Browser Program"
   ClientHeight    =   3315
   ClientLeft      =   60
   ClientTop       =   345
   ClientWidth     =   4740
   Icon            =   "FindFile.frx":0000
   LinkTopic       =   "Form1"
   ScaleHeight     =   3315
   ScaleWidth      =   4740
   StartUpPosition =   1  'CenterOwner
   Begin VB.CommandButton CmdCancel 
      Caption         =   "Cancel"
      Height          =   375
      Left            =   3600
      TabIndex        =   3
      Top             =   720
      Width           =   1095
   End
   Begin VB.CommandButton CmdOK 
      Caption         =   "OK"
      Height          =   375
      Left            =   3600
      TabIndex        =   2
      Top             =   240
      Width           =   1095
   End
   Begin VB.Frame Frame1 
      Height          =   3255
      Left            =   0
      TabIndex        =   4
      Top             =   0
      Width           =   3495
      Begin VB.FileListBox File1 
         Height          =   1260
         Left            =   120
         Pattern         =   "*.exe"
         TabIndex        =   5
         Top             =   1920
         Width           =   3255
      End
      Begin VB.DriveListBox Drive1 
         Height          =   315
         Left            =   120
         TabIndex        =   0
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
Private NormalHeight As Long
Private NormalWidth As Long

Private OldHeight As Long
Private OldWidth As Long

Private BrowserPath As String
Private Canceled As Boolean

Private Sub CmdCancel_Click()
    Canceled = True
    Unload Me
End Sub

Private Sub cmdOK_Click()
    If Len(File1.FileName) > 0 Then
        BrowserPath = File1.Path + "\" + File1.FileName
        Unload Me
    Else
        MsgBox InterfaceLabels("MsgNotFoundFile").elem2
    End If
End Sub

Private Sub Dir1_Change()
    File1.Path = Dir1.Path
    File1.pattern = "*.exe"
End Sub

Private Sub Drive1_Change()
    Dir1.Path = Drive1.Drive
End Sub

Sub ViewPath()
    Dim Path As String
    Dim File As String
    Dim P As Long
    
    Path = DEFAULTBROWSERPATH
    
    If (Len(dir(Path)) > 0) And (Len(Path) > 0) Then
        Drive1.Drive = Mid(Path, 1, 2)
        
        File = Path
        
        P = InStr(File, "\")
        While P > 0
            File = Mid(File, P + 1)
            P = InStr(File, "\")
        Wend
        P = InStr(Path, File)
        
        Dir1.Path = Mid(Path, 1, P - 2)
        File1.FileName = File
    End If
    
    Me.Show vbModal
        
    DEFAULTBROWSERPATH = BrowserPath
    
End Sub

Function FindBrowserPath() As String
    BrowserPath = DEFAULTBROWSERPATH
    
    If (Len(dir(BrowserPath)) = 0) Or (Len(BrowserPath) = 0) Then
        BrowserPath = ""
        While (Len(BrowserPath) = 0) And (Not Canceled)
            Me.Show vbModal
        Wend
        
    End If
    DEFAULTBROWSERPATH = BrowserPath
    FindBrowserPath = BrowserPath
End Function


Private Sub Form_Load()
    Caption = InterfaceLabels("frmFindBrowser_Caption").elem2
    If Len(Currbv) > 0 Then Caption = BV(Currbv).BVname + " - " + Caption
    
    CmdOK.Caption = InterfaceLabels("CmdOK").elem2
    CmdCancel.Caption = InterfaceLabels("frmFindBrowser_CmdCancel").elem2
    
    OldHeight = Height
    OldWidth = Width
    NormalHeight = Height
    NormalWidth = Width
        
End Sub

Private Sub Form_Resize()
    ResizeForm
End Sub

'-----------------------------------------------------------------------
'ResizeForm - Change the size of all form objects
'-----------------------------------------------------------------------
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

'-----------------------------------------------------------------------
'Components_Position - Position the form objects
'x  - coeficient to dimension the width object
'y  - coeficient to dimension the height object
'-----------------------------------------------------------------------
Private Sub Components_Position(x As Double, Y As Double)
    
    Call Components_ChangeSize(Frame1, x, Y, x, Y)
    Call Components_ChangeSize(File1, x, Y, x, Y)
    Call Components_ChangeSize(Dir1, x, Y, x, Y)
    Call Components_ChangeSize(Drive1, x, Y, x, 1)
    Call Components_ChangeSize(CmdOK, x, Y, x, 1)
    Call Components_ChangeSize(CmdCancel, x, Y, x, 1)
    
End Sub

'-----------------------------------------------------------------------
'Components_ChangeSize  - Change the size of a object of the form
'obj    - the form object
'Left   -
'Top    -
'Width  -
'Height -
'-----------------------------------------------------------------------
Private Sub Components_ChangeSize(obj As Object, Left As Double, Top As Double, Width As Double, Height As Double)
    obj.Left = Left * obj.Left
    obj.Top = Top * obj.Top
    If Height <> 1 Then obj.Height = CLng(Height * obj.Height)
    If Width <> 1 Then obj.Width = Width * obj.Width
End Sub


