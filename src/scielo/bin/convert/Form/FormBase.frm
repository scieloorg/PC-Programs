VERSION 5.00
Begin VB.Form FormBase 
   Caption         =   "Form1"
   ClientHeight    =   5355
   ClientLeft      =   60
   ClientTop       =   345
   ClientWidth     =   8190
   LinkTopic       =   "Form1"
   ScaleHeight     =   5355
   ScaleWidth      =   8190
   StartUpPosition =   3  'Windows Default
   Begin VB.FileListBox File1 
      Height          =   285
      Left            =   7560
      TabIndex        =   4
      Top             =   1080
      Width           =   495
   End
   Begin VB.DirListBox Dir1 
      Height          =   315
      Left            =   7560
      TabIndex        =   3
      Top             =   600
      Width           =   495
   End
   Begin VB.DriveListBox Drive1 
      Height          =   315
      Left            =   7560
      TabIndex        =   2
      Top             =   120
      Width           =   495
   End
   Begin VB.Frame Frame1 
      Caption         =   "Frame1"
      Height          =   4935
      Left            =   120
      TabIndex        =   0
      Top             =   240
      Width           =   6615
      Begin VB.ListBox List1 
         Height          =   3765
         Left            =   240
         TabIndex        =   5
         Top             =   960
         Width           =   6255
      End
      Begin VB.ComboBox Combo1 
         Height          =   315
         Left            =   2040
         TabIndex        =   1
         Text            =   "Combo1"
         Top             =   360
         Width           =   2295
      End
   End
End
Attribute VB_Name = "FormBase"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Sub OpenBase()
    Dim path As String
    Dim files() As String
    Dim filecount As Long
    
    Caption = "Database"
    
    path = BV(Currbv).FileTree.DirNodes("Serial Directory").FullPath
    Call ReturnFiles(path, "????????.mst") ', files, filecount)
    Show
    
End Sub

Private Function ReturnFile(path As String, pattern As String) As String
    Dim file As String
         
    file = dir(path + "\" + pattern, vbArchive)
    If Len(file) = 0 Then
        
    End If
    ReturnFile = file
End Function


Sub ReturnFiles(path As String, pattern As String) ', files() As String, filescount As Long)
    Dim file As String
    Dim folder As String
    Dim path2 As String
 
    file = ReturnFile(path, pattern)
    If Len(file) > 0 Then
        'filescount = filescount + 1
        'ReDim Preserve files(filescount)
        'files(filescount) = path + "\" + file
        List1.AddItem file
    Else
        path = path + "\"
        folder = dir(path, vbDirectory)
        
        While (Len(folder) > 0)
            If folder <> "." And folder <> ".." Then
                If (GetAttr(path & folder) And vbDirectory) = vbDirectory Then
                    path2 = path + folder
                    Call ReturnFiles(path2, pattern)  ', files, filescount)
                End If
            End If
            folder = dir
        Wend
    End If
End Sub

