VERSION 5.00
Object = "{6B7E6392-850A-101B-AFC0-4210102A8DA7}#1.1#0"; "COMCTL32.OCX"
Object = "{EAB22AC0-30C1-11CF-A7EB-0000C05BAE0B}#1.1#0"; "SHDOCVW.DLL"
Begin VB.Form frmBrowser 
   BackColor       =   &H00C0C0C0&
   ClientHeight    =   6240
   ClientLeft      =   2940
   ClientTop       =   1440
   ClientWidth     =   6495
   LinkTopic       =   "Form1"
   MDIChild        =   -1  'True
   ScaleHeight     =   6240
   ScaleWidth      =   6495
   ShowInTaskbar   =   0   'False
   Begin ComctlLib.Toolbar tbToolBar 
      Align           =   2  'Align Bottom
      Height          =   540
      Left            =   0
      TabIndex        =   1
      Top             =   5700
      Width           =   6495
      _ExtentX        =   11456
      _ExtentY        =   953
      ButtonWidth     =   820
      ButtonHeight    =   794
      Wrappable       =   0   'False
      ImageList       =   "imlIcons"
      _Version        =   327680
      BeginProperty Buttons {0713E452-850A-101B-AFC0-4210102A8DA7} 
         NumButtons      =   6
         BeginProperty Button1 {0713F354-850A-101B-AFC0-4210102A8DA7} 
            Key             =   "Back"
            Object.ToolTipText     =   "Back"
            Object.Tag             =   ""
            ImageIndex      =   1
         EndProperty
         BeginProperty Button2 {0713F354-850A-101B-AFC0-4210102A8DA7} 
            Key             =   "Forward"
            Object.ToolTipText     =   "Forward"
            Object.Tag             =   ""
            ImageIndex      =   2
         EndProperty
         BeginProperty Button3 {0713F354-850A-101B-AFC0-4210102A8DA7} 
            Key             =   "Stop"
            Object.ToolTipText     =   "Stop"
            Object.Tag             =   ""
            ImageIndex      =   3
         EndProperty
         BeginProperty Button4 {0713F354-850A-101B-AFC0-4210102A8DA7} 
            Key             =   "Refresh"
            Object.ToolTipText     =   "Refresh"
            Object.Tag             =   ""
            ImageIndex      =   4
         EndProperty
         BeginProperty Button5 {0713F354-850A-101B-AFC0-4210102A8DA7} 
            Key             =   "Home"
            Object.ToolTipText     =   "Home"
            Object.Tag             =   ""
            ImageIndex      =   5
         EndProperty
         BeginProperty Button6 {0713F354-850A-101B-AFC0-4210102A8DA7} 
            Key             =   "Search"
            Object.ToolTipText     =   "Search"
            Object.Tag             =   ""
            ImageIndex      =   6
         EndProperty
      EndProperty
      BorderStyle     =   1
      MouseIcon       =   "frmBrowser.frx":0000
   End
   Begin VB.PictureBox picWBStatus 
      Height          =   375
      Left            =   0
      ScaleHeight     =   315
      ScaleWidth      =   6435
      TabIndex        =   6
      Top             =   5280
      Width           =   6495
      Begin VB.Label wbstatus 
         AutoSize        =   -1  'True
         BackColor       =   &H00C0C0C0&
         Height          =   315
         Left            =   120
         TabIndex        =   7
         Top             =   0
         Width           =   3525
      End
   End
   Begin VB.PictureBox picAddress 
      BackColor       =   &H00C0C0C0&
      BorderStyle     =   0  'None
      Height          =   615
      Left            =   0
      ScaleHeight     =   615
      ScaleWidth      =   6420
      TabIndex        =   3
      TabStop         =   0   'False
      Top             =   1800
      Width           =   6420
      Begin VB.ComboBox cboAddress 
         Height          =   315
         Left            =   120
         TabIndex        =   4
         Text            =   "¯¯END!"
         Top             =   240
         Width           =   5475
      End
      Begin VB.Label lblAddress 
         BackColor       =   &H00C0C0C0&
         Caption         =   "&Address:"
         Height          =   255
         Left            =   120
         TabIndex        =   5
         Tag             =   "&Address:"
         Top             =   0
         Width           =   3075
      End
   End
   Begin SHDocVwCtl.WebBrowser brwWebBrowser 
      Height          =   2535
      Left            =   0
      TabIndex        =   0
      Top             =   2400
      Width           =   6480
      ExtentX         =   11430
      ExtentY         =   4471
      ViewMode        =   1
      Offline         =   0
      Silent          =   0
      RegisterAsBrowser=   0
      RegisterAsDropTarget=   0
      AutoArrange     =   -1  'True
      NoClientEdge    =   -1  'True
      AlignLeft       =   0   'False
      ViewID          =   "{0057D0E0-3573-11CF-AE69-08002B2E1262}"
      Location        =   ""
   End
   Begin VB.Timer timTimer 
      Enabled         =   0   'False
      Interval        =   5
      Left            =   5880
      Top             =   3120
   End
   Begin VB.Frame FrmScielo 
      BackColor       =   &H00FFFFFF&
      Height          =   1815
      Left            =   0
      TabIndex        =   2
      Top             =   0
      Width           =   6495
      Begin VB.Image Image2 
         Height          =   285
         Left            =   2640
         Picture         =   "frmBrowser.frx":001C
         Top             =   840
         Width           =   3180
      End
      Begin VB.Image Image1 
         Height          =   1635
         Left            =   120
         Picture         =   "frmBrowser.frx":073D
         Top             =   120
         Width           =   1710
      End
   End
   Begin ComctlLib.ImageList imlIcons 
      Left            =   5760
      Top             =   3600
      _ExtentX        =   1005
      _ExtentY        =   1005
      BackColor       =   -2147483643
      ImageWidth      =   24
      ImageHeight     =   24
      MaskColor       =   12632256
      _Version        =   327680
      BeginProperty Images {0713E8C2-850A-101B-AFC0-4210102A8DA7} 
         NumListImages   =   6
         BeginProperty ListImage1 {0713E8C3-850A-101B-AFC0-4210102A8DA7} 
            Picture         =   "frmBrowser.frx":11C2
            Key             =   ""
         EndProperty
         BeginProperty ListImage2 {0713E8C3-850A-101B-AFC0-4210102A8DA7} 
            Picture         =   "frmBrowser.frx":1854
            Key             =   ""
         EndProperty
         BeginProperty ListImage3 {0713E8C3-850A-101B-AFC0-4210102A8DA7} 
            Picture         =   "frmBrowser.frx":1EE6
            Key             =   ""
         EndProperty
         BeginProperty ListImage4 {0713E8C3-850A-101B-AFC0-4210102A8DA7} 
            Picture         =   "frmBrowser.frx":2578
            Key             =   ""
         EndProperty
         BeginProperty ListImage5 {0713E8C3-850A-101B-AFC0-4210102A8DA7} 
            Picture         =   "frmBrowser.frx":2C0A
            Key             =   ""
         EndProperty
         BeginProperty ListImage6 {0713E8C3-850A-101B-AFC0-4210102A8DA7} 
            Picture         =   "frmBrowser.frx":329C
            Key             =   ""
         EndProperty
      EndProperty
   End
End
Attribute VB_Name = "frmBrowser"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Public StartingAddress As String
Dim mbDontNavigateNow As Boolean

Private Sub Form_Load()
    On Error Resume Next
    Me.Show
    tbToolBar.Refresh
    Form_Resize

    cboAddress.Move 50, lblAddress.Top + lblAddress.Height + 15

    If Len(StartingAddress) > 0 Then
        cboAddress.Text = StartingAddress
        cboAddress.AddItem cboAddress.Text
        'try to navigate to the starting address
        timTimer.Enabled = True
        brwWebBrowser.Navigate StartingAddress
    End If

End Sub



Private Sub brwWebBrowser_DownloadComplete()
    On Error Resume Next
    wbstatus.Caption = brwWebBrowser.LocationName
End Sub

Private Sub brwWebBrowser_NavigateComplete(ByVal URL As String)
    Dim i As Integer
    Dim bFound As Boolean
    wbstatus.Caption = brwWebBrowser.LocationName
    For i = 0 To cboAddress.ListCount - 1
        If cboAddress.List(i) = brwWebBrowser.LocationURL Then
            bFound = True
            Exit For
        End If
    Next i
    mbDontNavigateNow = True
    If bFound Then
        cboAddress.RemoveItem i
    End If
    cboAddress.AddItem brwWebBrowser.LocationURL, 0
    cboAddress.ListIndex = 0
    mbDontNavigateNow = False
End Sub

Private Sub cboAddress_Click()
    If mbDontNavigateNow Then Exit Sub
    timTimer.Enabled = True
    brwWebBrowser.Navigate cboAddress.Text
End Sub

Private Sub cboAddress_KeyPress(KeyAscii As Integer)
    On Error Resume Next
    If KeyAscii = vbKeyReturn Then
        cboAddress_Click
    End If
End Sub

Private Sub Form_Resize()
    If Me.ScaleWidth > 0 Then
        cboAddress.Width = Me.ScaleWidth - 200
        picAddress.Width = Me.ScaleWidth - 100
        picWBStatus.Width = Me.ScaleWidth - 100
        picWBStatus.Top = Me.ScaleHeight - (picAddress.Height + picWBStatus.Height) - 50
        FrmScielo.Width = Me.ScaleWidth - 100
        brwWebBrowser.Width = Me.ScaleWidth - 100
        brwWebBrowser.Height = Me.ScaleHeight - (FrmScielo.Height + picAddress.Height + picWBStatus.Height + tbToolBar.Height) - 200
    End If
End Sub

Private Sub timTimer_Timer()
    If brwWebBrowser.Busy = False Then
        timTimer.Enabled = False
        wbstatus.Caption = brwWebBrowser.LocationName
    Else
        wbstatus.Caption = "Working..."
    End If
End Sub

Private Sub tbToolBar_ButtonClick(ByVal Button As Button)
    On Error Resume Next
     
    timTimer.Enabled = True
     
    Select Case Button.Key
        Case "Back"
            brwWebBrowser.GoBack
        Case "Forward"
            brwWebBrowser.GoForward
        Case "Refresh"
            brwWebBrowser.Refresh
        Case "Home"
            brwWebBrowser.GoHome
        Case "Search"
            brwWebBrowser.GoSearch
        Case "Stop"
            timTimer.Enabled = False
            brwWebBrowser.Stop
            wbstatus.Caption = brwWebBrowser.LocationName
    End Select

End Sub

