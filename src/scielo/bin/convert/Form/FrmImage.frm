VERSION 5.00
Object = "{6B7E6392-850A-101B-AFC0-4210102A8DA7}#1.3#0"; "COMCTL32.OCX"
Begin VB.Form FrmImage 
   Caption         =   "Image Transcription"
   ClientHeight    =   6330
   ClientLeft      =   60
   ClientTop       =   345
   ClientWidth     =   6810
   Icon            =   "FrmImage.frx":0000
   LinkTopic       =   "Form1"
   ScaleHeight     =   6330
   ScaleWidth      =   6810
   StartUpPosition =   2  'CenterScreen
   Begin ComctlLib.ListView ListViewImg 
      Height          =   2295
      Left            =   120
      TabIndex        =   12
      Top             =   3480
      Width           =   6615
      _ExtentX        =   11668
      _ExtentY        =   4048
      View            =   3
      LabelWrap       =   -1  'True
      HideSelection   =   -1  'True
      _Version        =   327682
      Icons           =   "ImgList"
      SmallIcons      =   "ImgList"
      ForeColor       =   -2147483640
      BackColor       =   -2147483643
      BorderStyle     =   1
      Appearance      =   1
      NumItems        =   1
      BeginProperty ColumnHeader(1) {0713E8C7-850A-101B-AFC0-4210102A8DA7} 
         Key             =   ""
         Object.Tag             =   ""
         Text            =   "Image Replace"
         Object.Width           =   2540
      EndProperty
   End
   Begin VB.CommandButton CmdCancel 
      Caption         =   "Cancel"
      Height          =   375
      Left            =   5640
      TabIndex        =   4
      Top             =   5880
      Width           =   1095
   End
   Begin VB.CommandButton CmdOk 
      Caption         =   "OK"
      Height          =   375
      Left            =   4440
      TabIndex        =   3
      Top             =   5880
      Width           =   1095
   End
   Begin VB.Frame Frame1 
      Height          =   3255
      Left            =   120
      TabIndex        =   8
      Top             =   120
      Width           =   6615
      Begin VB.PictureBox Img 
         Height          =   1095
         Left            =   120
         Picture         =   "FrmImage.frx":030A
         ScaleHeight     =   1035
         ScaleWidth      =   6315
         TabIndex        =   13
         Top             =   480
         Width           =   6375
      End
      Begin VB.CommandButton CmdFirst 
         Caption         =   "| <"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   13.5
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   495
         Left            =   120
         TabIndex        =   5
         Top             =   2640
         Width           =   735
      End
      Begin VB.CommandButton CmdPrevious 
         Caption         =   "<"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   13.5
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   495
         Left            =   840
         TabIndex        =   6
         Top             =   2640
         Width           =   735
      End
      Begin VB.CommandButton CmdNext 
         Caption         =   ">"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   13.5
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   495
         Left            =   1560
         TabIndex        =   2
         Top             =   2640
         Width           =   735
      End
      Begin VB.CommandButton CmdLast 
         Caption         =   "> |"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   13.5
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   495
         Left            =   2280
         TabIndex        =   7
         Top             =   2640
         Width           =   735
      End
      Begin VB.TextBox TxtReplace 
         Height          =   375
         Left            =   120
         TabIndex        =   0
         Top             =   2040
         Width           =   6375
      End
      Begin VB.CommandButton CmdReplace 
         Caption         =   "Replace "
         Height          =   495
         Left            =   5400
         TabIndex        =   1
         Top             =   2640
         Width           =   975
      End
      Begin VB.Label LabImg 
         AutoSize        =   -1  'True
         Caption         =   "Image"
         Height          =   195
         Left            =   120
         TabIndex        =   11
         Top             =   240
         Width           =   435
      End
      Begin VB.Label LabTranslation 
         AutoSize        =   -1  'True
         Caption         =   "Replace image with"
         Height          =   195
         Left            =   120
         TabIndex        =   10
         Top             =   1800
         Width           =   1395
      End
      Begin VB.Label LabIndex 
         AutoSize        =   -1  'True
         Caption         =   "1/1"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   18
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   435
         Left            =   3960
         TabIndex        =   9
         Top             =   2640
         Width           =   555
      End
   End
   Begin ComctlLib.ImageList ImgList 
      Left            =   240
      Top             =   5760
      _ExtentX        =   1005
      _ExtentY        =   1005
      BackColor       =   -2147483643
      MaskColor       =   12632256
      _Version        =   327682
   End
End
Attribute VB_Name = "FrmImage"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Private ImgAddr() As String
Private ImgShortAddr() As String
Private ImgRepl() As String
Private ImgCount As Long
Private mvarCurrImgIdx As Long
Private OKChoice As Boolean

Property Let CurrImgIdx(idx As Long)
    If (idx > 0) And (idx <= ImgCount) Then
        Img.Picture = LoadPicture(ImgShortAddr(idx))
        TxtReplace.Text = ImgRepl(idx)
        mvarCurrImgIdx = idx
        LabIndex.Caption = CStr(idx) + PathSepUnix + CStr(ImgCount)
    End If
End Property
Property Get CurrImgIdx() As Long
    CurrImgIdx = mvarCurrImgIdx
End Property

Private Sub CmdCancel_Click()
    Dim i As Long
    Dim ok As Boolean
    Dim r As VbMsgBoxResult
    
    r = MsgBox("Are you sure you want to cancel?", vbYesNo + vbDefaultButton2)
    If r = vbYes Then
        Hide
    ElseIf r = vbNo Then
    
    End If
    OKChoice = False
End Sub

Private Sub CmdFirst_Click()
    CurrImgIdx = 1
End Sub

Private Sub CmdLast_Click()
    CurrImgIdx = ImgCount
End Sub

Private Sub CmdNext_Click()
    CurrImgIdx = CurrImgIdx + 1
End Sub

Private Sub cmdOK_Click()
    Dim i As Long
    Dim ok As Boolean
    Dim r As VbMsgBoxResult
    
    ok = True
    For i = 1 To ImgCount
        If Len(ImgRepl(i)) = 0 Then
            ok = False
            MsgBox "Invalid replace value to image " + CStr(i) + ". They will not be replaced."
        End If
    Next
    
    If ok Then
        Hide
    Else
        r = MsgBox("Do you want to complete the missing images?", vbYesNo + vbDefaultButton1)
        If r = vbYes Then
        ElseIf r = vbNo Then
            Hide
        End If
    End If
    OKChoice = True
End Sub

Private Sub CmdPrevious_Click()
    CurrImgIdx = CurrImgIdx - 1
End Sub

Private Sub CmdReplace_Click()
    ImgRepl(CurrImgIdx) = TxtReplace.Text
    ListImages
End Sub

Sub setImages(ImageAddress() As String, ImageShortAddress() As String, ImageReplace() As String, ImageCounter As Long)
    Dim i As Long
    Dim k As String
        
    
    OKChoice = False
    ImgCount = ImageCounter
    ReDim ImgAddr(ImgCount)
    ReDim ImgShortAddr(ImgCount)
    ReDim ImgRepl(ImgCount)
    For i = 1 To ImageCounter
        ImgAddr(i) = ImageAddress(i)
        ImgShortAddr(i) = ImageShortAddress(i)
        ImgRepl(i) = ImageReplace(i)
    Next
    CurrImgIdx = 1
    
    ImgList.ListImages.Clear
    For i = 1 To ImgCount
        Call ImgList.ListImages.Add(i, "img" + CStr(i), LoadPicture(ImgShortAddr(i)))
    Next
    
    ListImages
    
    Show vbModal
    
    If OKChoice Then
        ImageCounter = 0
        For i = 1 To ImgCount
            If Len(ImgRepl(i)) > 0 Then
                ImageCounter = ImageCounter + 1
                ReDim Preserve ImageReplace(ImageCounter)
                ReDim Preserve ImageReplace(ImageCounter)
                ReDim Preserve ImageReplace(ImageCounter)
            
                ImageReplace(ImageCounter) = ImgRepl(i)
                ImageAddress(ImageCounter) = ImgAddr(i)
                ImageShortAddress(ImageCounter) = ImgShortAddr(i)
            End If
        Next
    End If
    Unload Me
End Sub


Sub ListImages()
    Dim i As Long
    Dim k As String
    
    ListViewImg.ListItems.Clear
    For i = 1 To ImgCount
        Call ListViewImg.ListItems.Add(i, ("img" + CStr(i)), ImgRepl(i), "img" + CStr(i), "img" + CStr(i))
    Next
    
    
End Sub


Private Sub ListViewImg_BeforeLabelEdit(Cancel As Integer)
    Cancel = True
End Sub
