VERSION 5.00
Begin VB.Form Issue0 
   BorderStyle     =   1  'Fixed Single
   Caption         =   "Config - Open Existing Serial"
   ClientHeight    =   5460
   ClientLeft      =   2040
   ClientTop       =   1620
   ClientWidth     =   7710
   Icon            =   "frm_Issue_0.frx":0000
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   Moveable        =   0   'False
   ScaleHeight     =   5460
   ScaleWidth      =   7710
   StartUpPosition =   2  'CenterScreen
   Begin VB.CommandButton CmdNext 
      Caption         =   "Next"
      Height          =   375
      Left            =   5400
      TabIndex        =   1
      Top             =   5040
      Width           =   975
   End
   Begin VB.CommandButton CmdClose 
      Caption         =   "Close"
      Height          =   375
      Left            =   6600
      TabIndex        =   2
      Top             =   5040
      Width           =   975
   End
   Begin VB.Frame FrameOpenSerial 
      Caption         =   "Select Serial to Open"
      Height          =   4815
      Left            =   120
      TabIndex        =   3
      Top             =   120
      Width           =   7455
      Begin VB.ListBox ListExistingSerial 
         Height          =   4155
         Left            =   120
         Sorted          =   -1  'True
         TabIndex        =   0
         Top             =   360
         Width           =   7215
      End
   End
End
Attribute VB_Name = "Issue0"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Public issueDAO As ClsIssueDAO

Private Sub CmdClose_Click()
    
    UpdateIssueTable
    Set issueDAO = Nothing
    
    Unload Me
End Sub

Private Sub CmdNext_Click()
    If Len(ListExistingSerial.text) > 0 Then
        Call Issue1.OpenIssue(ListExistingSerial.text)
    Else
        MsgBox ConfigLabels.getLabel("Select_to_Open")
    End If
End Sub

Sub OpenExistingSerial()
    
    MousePointer = vbHourglass
    
    With Paths("Issue Database")
    Set issueDAO = New ClsIssueDAO
    Call issueDAO.create(.Path, .FileName, .key)
    End With

    
    
    With ConfigLabels
    Caption = App.Title + " - " + .getLabel("mnSerialIssues")
    FrameOpenSerial.Caption = .getLabel("Select_to_Open")
    CmdNext.Caption = .getLabel("ButtonOpen")
    CmdClose.Caption = .getLabel("ButtonClose")
    End With
    
    Call Serial_GetExisting(ListExistingSerial)
    
    MousePointer = vbArrow
    Show vbModal
End Sub

Private Function UpdateIssueTable() As Boolean
    Dim i As Long
    Dim originalPft As String
    Dim configuredPft As String
    
    MousePointer = vbHourglass
    
    With Paths("Markup Issue Table")
        For i = 1 To idiomsinfo.count
            originalPft = idiomsinfo(i).Code + "_" + Paths("Markup Issue Table Format").FileName
            configuredPft = "cfg_" + originalPft
            Call ConfigurePft(originalPft, configuredPft, "c:\scielo\code\code", Paths("Code Database").Path + "\" + Paths("Code Database").FileName)
            Call issueDAO.UpdateIssueTable(.Path + "\" + idiomsinfo(i).Code + "_" + .FileName, configuredPft)
        Next
    Call issueDAO.UpdateIssueTable(.Path + "\" + .FileName, App.Path + "\misc\issue.xml.pft")
    End With
    MousePointer = vbArrow
End Function
Private Function ConfigurePft(originalPft As String, configuredPft As String, find As String, newPath As String) As Boolean
    Dim content As String
    Dim i As Long
    Dim fn As Long
    Dim fn2 As Long
        
    fn = FreeFile
    
    Open "langs\" + originalPft For Input As fn
    content = Input(LOF(fn), fn)
    Close fn
    
    content = Replace(content, find, newPath)
    
    fn = FreeFile
    Open configuredPft For Output As fn
    Print #fn, content
    Close fn
        
    ConfigurePft = True
End Function

