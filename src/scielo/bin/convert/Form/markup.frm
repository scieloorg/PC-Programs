VERSION 5.00
Object = "{831FDD16-0C5C-11D2-A9FC-0000F8754DA1}#2.0#0"; "Mscomctl.ocx"
Begin VB.Form FormMarkup 
   Caption         =   "Markup"
   ClientHeight    =   5115
   ClientLeft      =   1275
   ClientTop       =   1020
   ClientWidth     =   8250
   Icon            =   "markup.frx":0000
   LinkTopic       =   "Form4"
   PaletteMode     =   1  'UseZOrder
   ScaleHeight     =   5115
   ScaleWidth      =   8250
   StartUpPosition =   2  'CenterScreen
   Begin MSComctlLib.ProgressBar ProgressBar1 
      Height          =   255
      Left            =   4560
      TabIndex        =   39
      Top             =   4800
      Width           =   3615
      _ExtentX        =   6376
      _ExtentY        =   450
      _Version        =   393216
      Appearance      =   1
   End
   Begin VB.CommandButton CmdHelp 
      Caption         =   "Help"
      Height          =   375
      Left            =   2280
      TabIndex        =   16
      Top             =   3840
      Width           =   855
   End
   Begin VB.CommandButton CmdClose 
      Caption         =   "Close"
      Height          =   375
      Left            =   1320
      TabIndex        =   15
      Top             =   3840
      Width           =   855
   End
   Begin VB.CommandButton CmdOK 
      Caption         =   "OK"
      Height          =   375
      Left            =   360
      TabIndex        =   14
      Top             =   3840
      Width           =   855
   End
   Begin VB.Frame FramDoc 
      Caption         =   "Documents"
      Enabled         =   0   'False
      Height          =   4215
      Left            =   3600
      TabIndex        =   22
      Top             =   120
      Width           =   2175
      Begin VB.FileListBox ListDoc 
         Height          =   2820
         Left            =   120
         MultiSelect     =   2  'Extended
         TabIndex        =   17
         Top             =   720
         Width           =   1935
      End
      Begin VB.CommandButton CmdLoad 
         Caption         =   "Load"
         Height          =   375
         Left            =   480
         TabIndex        =   18
         Top             =   3720
         Width           =   1335
      End
      Begin VB.Label Label1 
         AutoSize        =   -1  'True
         Caption         =   "Label4"
         Height          =   195
         Left            =   120
         TabIndex        =   40
         Top             =   480
         Width           =   600
      End
      Begin VB.Label LabDocCounter 
         AutoSize        =   -1  'True
         Caption         =   "Label4"
         Height          =   195
         Left            =   120
         TabIndex        =   29
         Top             =   240
         Width           =   600
      End
   End
   Begin VB.Frame FramDB 
      Caption         =   "Results"
      Height          =   4215
      Left            =   5880
      TabIndex        =   26
      Top             =   120
      Width           =   2295
      Begin VB.ListBox ListOutDB 
         Height          =   840
         Left            =   120
         MultiSelect     =   2  'Extended
         Sorted          =   -1  'True
         TabIndex        =   21
         Top             =   2760
         Width           =   2055
      End
      Begin VB.CommandButton CmdViewLog 
         Caption         =   "View"
         Height          =   375
         Left            =   600
         TabIndex        =   19
         Top             =   3720
         Width           =   1215
      End
      Begin VB.ListBox ListInDB 
         Height          =   1425
         ItemData        =   "markup.frx":000C
         Left            =   120
         List            =   "markup.frx":000E
         Sorted          =   -1  'True
         TabIndex        =   20
         Top             =   720
         Width           =   2055
      End
      Begin VB.Label LabFailCount 
         AutoSize        =   -1  'True
         Caption         =   "Label4"
         Height          =   195
         Left            =   120
         TabIndex        =   31
         Top             =   2520
         Width           =   480
      End
      Begin VB.Label LabSuccessCount 
         AutoSize        =   -1  'True
         Caption         =   "Label4"
         Height          =   195
         Left            =   120
         TabIndex        =   30
         Top             =   480
         Width           =   480
      End
      Begin VB.Label LabNotLoaded 
         AutoSize        =   -1  'True
         Caption         =   "Not Loaded"
         Height          =   195
         Left            =   120
         TabIndex        =   28
         Top             =   2280
         Width           =   840
      End
      Begin VB.Label LabLoaded 
         AutoSize        =   -1  'True
         Caption         =   "Loaded"
         Height          =   195
         Left            =   120
         TabIndex        =   27
         Top             =   240
         Width           =   540
      End
   End
   Begin VB.Frame FrameId 
      Height          =   4215
      Left            =   120
      TabIndex        =   23
      Top             =   120
      Width           =   3375
      Begin VB.TextBox TextEPubDate 
         Height          =   285
         Left            =   1440
         MaxLength       =   8
         TabIndex        =   41
         Text            =   "20080000"
         Top             =   2880
         Visible         =   0   'False
         Width           =   1815
      End
      Begin VB.ComboBox ComboFolder 
         Height          =   315
         Index           =   5
         Left            =   1440
         Sorted          =   -1  'True
         Style           =   2  'Dropdown List
         TabIndex        =   8
         Top             =   1800
         Width           =   1800
      End
      Begin VB.ComboBox ComboFolder 
         Height          =   315
         Index           =   6
         Left            =   1440
         Sorted          =   -1  'True
         Style           =   2  'Dropdown List
         TabIndex        =   10
         Top             =   2160
         Width           =   1800
      End
      Begin VB.ComboBox ComboFolder 
         Height          =   315
         Index           =   7
         Left            =   1440
         Sorted          =   -1  'True
         Style           =   2  'Dropdown List
         TabIndex        =   12
         Top             =   2520
         Width           =   1800
      End
      Begin VB.TextBox TxtFolder 
         Height          =   285
         Index           =   5
         Left            =   1440
         TabIndex        =   9
         Text            =   "Text1"
         Top             =   1800
         Width           =   1800
      End
      Begin VB.ComboBox ComboFolder 
         Height          =   315
         Index           =   4
         Left            =   1440
         Sorted          =   -1  'True
         Style           =   2  'Dropdown List
         TabIndex        =   6
         Top             =   1440
         Width           =   1800
      End
      Begin VB.ComboBox ComboFolder 
         Height          =   315
         Index           =   3
         Left            =   1440
         Sorted          =   -1  'True
         Style           =   2  'Dropdown List
         TabIndex        =   5
         Top             =   1080
         Width           =   1800
      End
      Begin VB.ComboBox ComboFolder 
         Height          =   315
         Index           =   2
         Left            =   1440
         Sorted          =   -1  'True
         Style           =   2  'Dropdown List
         TabIndex        =   3
         Top             =   720
         Width           =   1800
      End
      Begin VB.ComboBox ComboFolder 
         Height          =   315
         Index           =   1
         Left            =   120
         Sorted          =   -1  'True
         Style           =   2  'Dropdown List
         TabIndex        =   0
         Top             =   240
         Width           =   3015
      End
      Begin VB.TextBox TxtFolder 
         Height          =   285
         Index           =   1
         Left            =   120
         TabIndex        =   1
         Text            =   "Text1"
         Top             =   240
         Width           =   3015
      End
      Begin VB.TextBox TxtFolder 
         Height          =   285
         Index           =   7
         Left            =   1440
         TabIndex        =   13
         Text            =   "Text1"
         Top             =   2520
         Width           =   1800
      End
      Begin VB.TextBox TxtFolder 
         Height          =   285
         Index           =   6
         Left            =   1440
         TabIndex        =   11
         Text            =   "Text1"
         Top             =   2160
         Width           =   1800
      End
      Begin VB.TextBox TxtFolder 
         Height          =   285
         Index           =   4
         Left            =   1440
         TabIndex        =   7
         Text            =   "Text1"
         Top             =   1440
         Width           =   1800
      End
      Begin VB.TextBox TxtFolder 
         Height          =   285
         Index           =   3
         Left            =   1440
         TabIndex        =   4
         Text            =   "Text1"
         Top             =   1080
         Width           =   1800
      End
      Begin VB.TextBox TxtFolder 
         Height          =   285
         Index           =   2
         Left            =   1440
         TabIndex        =   2
         Text            =   "Text1"
         Top             =   720
         Width           =   1800
      End
      Begin VB.Label labEPubDate 
         Alignment       =   1  'Right Justify
         Caption         =   "EpubDate"
         Height          =   495
         Left            =   120
         TabIndex        =   42
         Top             =   2880
         Visible         =   0   'False
         Width           =   1215
      End
      Begin VB.Label LabFolder 
         Alignment       =   1  'Right Justify
         Caption         =   "label"
         Height          =   375
         Index           =   7
         Left            =   120
         TabIndex        =   38
         Top             =   2520
         Width           =   1215
      End
      Begin VB.Label LabFolder 
         Alignment       =   1  'Right Justify
         Caption         =   "Label1"
         Height          =   255
         Index           =   3
         Left            =   120
         TabIndex        =   37
         Top             =   1080
         Width           =   1215
      End
      Begin VB.Label LabFolder 
         AutoSize        =   -1  'True
         Caption         =   "Label1"
         Height          =   195
         Index           =   1
         Left            =   120
         TabIndex        =   36
         Top             =   0
         Width           =   480
      End
      Begin VB.Label LabFolder 
         Alignment       =   1  'Right Justify
         Caption         =   "Label1"
         Height          =   375
         Index           =   2
         Left            =   240
         TabIndex        =   35
         Top             =   720
         Width           =   1095
      End
      Begin VB.Label LabFolder 
         Alignment       =   1  'Right Justify
         Caption         =   "Label1"
         Height          =   255
         Index           =   4
         Left            =   120
         TabIndex        =   34
         Top             =   1440
         Width           =   1215
      End
      Begin VB.Label LabFolder 
         Alignment       =   1  'Right Justify
         Caption         =   "Label1"
         Height          =   255
         Index           =   5
         Left            =   120
         TabIndex        =   33
         Top             =   1800
         Width           =   1215
      End
      Begin VB.Label LabFolder 
         Alignment       =   1  'Right Justify
         Caption         =   "label"
         Height          =   255
         Index           =   6
         Left            =   120
         TabIndex        =   32
         Top             =   2160
         Width           =   1215
      End
   End
   Begin VB.Label LabLeftMsg 
      AutoSize        =   -1  'True
      Caption         =   "Label1"
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   9.75
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H80000002&
      Height          =   240
      Left            =   120
      TabIndex        =   25
      Top             =   4800
      Width           =   2055
   End
   Begin VB.Label LabRightMsg 
      Alignment       =   1  'Right Justify
      BackColor       =   &H00C0C0C0&
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   9.75
         Charset         =   0
         Weight          =   400
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H80000002&
      Height          =   240
      Left            =   120
      TabIndex        =   24
      Top             =   4440
      Width           =   8085
   End
End
Attribute VB_Name = "FormMarkup"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Private Const TextBoxCounter = 7

Private NormalHeight As Long
Private NormalWidth As Long

Private OldHeight As Long
Private OldWidth As Long


Private Sub displayEpubDate(s As Boolean)
    TextEPubDate.Visible = s
    labEPubDate.Visible = s
    If s Then
        Dim epubdate As String
        epubdate = Date$
        TextEPubDate.text = Mid(epubdate, 7, 4) & Mid(epubdate, 1, 2) & Mid(epubdate, 4, 2)
    Else
        TextEPubDate.text = ""
    End If
End Sub
Private Sub checkEPubDateIsMandatory()
    Dim i As Long
    Dim x As Boolean
    For i = 1 To TxtFolder.Count
        If TxtFolder(i).text = "ahead" Or TxtFolder(i).text = "review" Then
            x = True
        End If
    Next
    Call displayEpubDate(x)
End Sub
'-----------------------------------------------------------------------
'MarkupForm_Open - Open the form used to select the files to
'convert/load the database
'-----------------------------------------------------------------------
Public Sub MarkupForm_Open()
    OldHeight = Height
    OldWidth = Width
    NormalHeight = Height
    NormalWidth = Width
    
    Caption = InterfaceLabels("formMarkup_caption").elem2
    If Len(Currbv) > 0 Then Caption = BV(Currbv).BVname + " - " + Caption
    
    CmdOK.Caption = InterfaceLabels("CmdOK").elem2
    CmdClose.Caption = InterfaceLabels("cmdclose").elem2
    CmdHelp.Caption = InterfaceLabels("cmdhelp").elem2
    FramDoc.Caption = InterfaceLabels("formMarkup_FramDoc").elem2
    CmdLoad.Caption = InterfaceLabels("formMarkup_CmdLoad").elem2
    FramDB.Caption = InterfaceLabels("formMarkup_FramDB").elem2
    LabLoaded.Caption = InterfaceLabels("formMarkup_LabLoaded").elem2
    LabNotLoaded.Caption = InterfaceLabels("formMarkup_LabNotLoaded").elem2
    CmdViewLog.Caption = InterfaceLabels("formMarkup_CmdViewLog").elem2
    labEPubDate.Caption = InterfaceLabels("formMarkup_epubdate").elem2
    Call Components_View(True)
    Components_Show
    Components_Enable (False)
    InputBox_Clean
    
    LabLeftMsg.Caption = ""
    ListDoc.pattern = "*.htm;*.html"
    Show vbModal
End Sub
' FIXED_20070115 ahead of print
' verificar a quantidade de arquivos dentro do diretorio ex-ahead e ahead;
' a soma deve ser igual ao valor informado no issue record
Private Sub cmdOK_Click()
    Dim FileCounter As Long
    Dim ret As Boolean
    Dim Id As String
    Dim base As String
    Dim i As Long
    Dim inputdataOk As Boolean
    Dim PathCurr As String
    Dim totalOfFiles As Long
    Dim xmlFilesCounter As Long
    Dim pListDoc As FileListBox
    
    Dim ArchiveFilesCounter As Long

    Dim journalDirstructure As ClJournalDirStructure
    
    Set pListDoc = ListDoc
    With BV(Currbv)
    inputdataOk = True
    For i = 1 To .Directory.Count
        Select Case .Directory(i).ObjTypeDir
        Case "combo"
            If Len(Trim(ComboFolder(i).text)) > 0 Then
                .Directory(i).Value = .Directory(i).ContentListFull(ComboFolder(i).text).elem2
                .Directory(i).cfgkey_key = ComboFolder(i).text
            Else
                .Directory(i).Value = ""
            End If
        Case "text", "label"
            .Directory(i).Value = TxtFolder(i).text
        End Select
        If .Directory(i).Value Like .Directory(i).pattern Then
            inputdataOk = True
        Else
            Call Msg.GiveRunInformation(InterfaceLabels(.Directory(i).MsgInvalidData).elem2, True)
            inputdataOk = False
        End If
    Next
    
    If inputdataOk Then
        PathCurr = .FileTree.DirNodes("Serial Directory").fullpath + .Directory.ReturnDataPath + PathSep
        
        'Find/Create the files/database related to the selected issue to convert
        If SetSelectedDir(PathCurr, FileCounter) Then
            
            If DirExist(PathCurr + "xml") Then
            
                pListDoc.pattern = "*.xml"
                pListDoc.Path = PathCurr + "xml"
                xmlFilesCounter = pListDoc.ListCount
            End If
            
        
            pListDoc.pattern = "*.htm;*.html"
            
            Set journalDirstructure = New ClJournalDirStructure
                
            Call journalDirstructure.setDirStructure(PathCurr + .FileTree.DirNodes("Markup Directory").text)
            
            If Not (journalDirstructure.relatedissues.archive Is Nothing) Then
                ' Possui ex-ahead
                If DirExist(journalDirstructure.relatedissues.archive.getMarkupFile()) Then
                    
                    pListDoc.Path = journalDirstructure.relatedissues.archive.getMarkupFile()
                    ArchiveFilesCounter = pListDoc.ListCount
                End If
            End If
            
            Label1.Caption = ""
            pListDoc.Path = PathCurr + .FileTree.DirNodes("Markup Directory").text
            totalOfFiles = pListDoc.ListCount + ArchiveFilesCounter + xmlFilesCounter
            
            LabDocCounter.Caption = InterfaceLabels("LabFileCount").elem2 + CStr(pListDoc.ListCount)
            If Not (journalDirstructure.relatedissues.archive Is Nothing) Then
                LabDocCounter.Caption = journalDirstructure.relatedissues.Issue.issueDir + ": " + CStr(pListDoc.ListCount) + "/" + CStr(totalOfFiles)
                Label1.Caption = journalDirstructure.relatedissues.archive.issueDir + ": " + CStr(ArchiveFilesCounter) + "/" + CStr(totalOfFiles)
            End If
            
            If xmlFilesCounter > 0 Then
                Label1.Caption = Label1.Caption & vbCrLf & "xml: " + CStr(xmlFilesCounter) + "/" + CStr(totalOfFiles)
                pListDoc.Top = pListDoc.Top - (0.1 * pListDoc.Top)
                
                pListDoc.Height = pListDoc.Height * 0.9
            End If
            
            List_SelectAll
            ViewSuccessAndFailure
            'Check the number of documents listed on the form and the number of documents previously  inserted in the issue database
            'If they are different, there must be an error in issue database or in the markup directory
            If Len(.Directory.ReturnCfgRecKey) > 0 Then
                If FileCounter = totalOfFiles Then
                    ret = True
                Else
                    Call Msg.GiveRunInformation(InterfaceLabels("MsgInvalidNumberofDoc").elem2 + vbCrLf + InterfaceLabels("MsgInvalidNumberofDocInMarkup").elem2 + CStr(totalOfFiles) + vbCrLf + InterfaceLabels("MsgInvalidNumberofDocInCfgRec").elem2 + CStr(FileCounter), True)
                End If
            Else
                ret = True
            End If
        End If
        If ret Then Components_Enable (True)
    End If
    End With
End Sub

Private Sub ComboFolder_Change(Index As Integer)
    If Index = 1 Then InputBox_Clean
End Sub

Private Sub Form_Load()
    CmdHelp.Visible = (help <> "0")
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
    Dim i As Long
    
    Call Components_ChangeSize(FrameId, x, Y, x, Y)
    Call Components_ChangeSize(CmdOK, x, Y, x, 1)
    Call Components_ChangeSize(CmdClose, x, Y, x, 1)
    Call Components_ChangeSize(CmdHelp, x, Y, x, 1)
    
    For i = 1 To TextBoxCounter
        Call Components_ChangeSize(LabFolder(i), x, Y, 1, 1)
        Call Components_ChangeSize(TxtFolder(i), x, Y, x, 1)
        Call Components_ChangeSize(ComboFolder(i), x, Y, x, 1)
    Next
    Call Components_ChangeSize(labEPubDate, x, Y, 1, 1)
    Call Components_ChangeSize(TextEPubDate, x, Y, x, 1)
            
    Call Components_ChangeSize(FramDoc, x, Y, x, Y)
    Call Components_ChangeSize(LabDocCounter, x, Y, 1, 1)
    Call Components_ChangeSize(ListDoc, x, Y, x, Y)
    Call Components_ChangeSize(CmdLoad, x, Y, x, 1)
        
    Call Components_ChangeSize(FramDB, x, Y, x, Y)
    Call Components_ChangeSize(LabLoaded, x, Y, 1, 1)
    Call Components_ChangeSize(LabSuccessCount, x, Y, 1, 1)
    Call Components_ChangeSize(ListInDB, x, Y, x, Y)
    Call Components_ChangeSize(LabNotLoaded, x, Y, 1, 1)
    Call Components_ChangeSize(LabFailCount, x, Y, 1, 1)
    Call Components_ChangeSize(ListOutDB, x, Y, x, Y)
    Call Components_ChangeSize(CmdViewLog, x, Y, x, 1)
    
    Call Components_ChangeSize(ProgressBar1, x, Y, x, 1)
    Call Components_ChangeSize(LabRightMsg, x, Y, x, 1)
    Call Components_ChangeSize(LabLeftMsg, x, Y, x, 1)
    
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

'-----------------------------------------------------------------------
'MarkupForm_Close - Close the form
'-----------------------------------------------------------------------
Private Sub MarkupForm_Close()
    Unload Me
End Sub

'-----------------------------------------------------------------------
'Components_Enable - Enable the objects of the form according to their use permission
'Flag   - to set enabled or not to the objects
'-----------------------------------------------------------------------
Private Sub Components_Enable(Flag As Boolean)
    If Not Flag Then
        LabDocCounter.Caption = ""
        LabSuccessCount.Caption = ""
        LabFailCount.Caption = ""
        Label1.Caption = ""
        
    End If
    
    FramDoc.Enabled = Flag
    ListDoc.Enabled = Flag
    CmdLoad.Enabled = Flag
    CmdViewLog.Enabled = Flag
    FramDB.Enabled = Flag
    ListInDB.Enabled = Flag
    ListOutDB.Enabled = Flag
    LabLoaded.Enabled = Flag
    LabNotLoaded.Enabled = Flag
    
End Sub
'-----------------------------------------------------------------------
'Components_Show - Show the group of documents to be converted
'depends on the BV, for instance, for scielo is serial list, for noticias
'is newspaper list
'-----------------------------------------------------------------------
Private Sub Components_Show()
    Dim i As Long
    Dim j As Long
    Dim q As Long
    
    
    With BV(Currbv)
    q = .Directory.Count
    For i = 1 To q
        LabFolder(i).Caption = InterfaceLabels(.Directory(i).LabDir).elem2
        
        Select Case .Directory(i).ObjTypeDir
        Case "combo"
            ComboFolder(i).Clear
            For j = 1 To .Directory(i).ContentListAbbr.Count
                ComboFolder(i).AddItem (.Directory(i).ContentListAbbr(j).elem2)
            Next
            ComboFolder(i).ListIndex = 0
        Case "text"
            TxtFolder(i).Enabled = True
        Case "label"
            TxtFolder(i).Enabled = False
        End Select
    Next
    End With
End Sub

'-----------------------------------------------------------------------
'LoadDocDatabase    - Load the Document database with the selected files
'-----------------------------------------------------------------------
Private Sub LoadDocDatabase(Optional epubdate As String)
    Dim i As Long
    Dim FileIndex() As Long
    Dim SelCount As Long
    Dim T0 As Date
    Dim Success As Long
    Dim result As String
    Dim BodyFile As String
    Dim BaseFile As String
    Dim MissingBody As String
    Dim InvalidBaseName As String
    Dim isBodyOK As Boolean
    Dim isBaseNameOK As Boolean
    Dim isConversionOK As Boolean
    
    MousePointer = vbHourglass
    
    'Get the selected files to convert into the database
    SelCount = List_GetSelectedItem(ListDoc, FileIndex)
    If SelCount > 0 Then
        T0 = Time
        EXISTDELETEDRECORDS = False
        For i = 1 To SelCount
            LabLeftMsg.Caption = CStr(i) + "/" + CStr(SelCount) + " in execution: " + ListDoc.List(FileIndex(i))
                
            'Check the body files existence
            isBodyOK = True
            If BV(Currbv).HasFulltext Then
                BodyFile = BodyFileName(ListDoc.List(FileIndex(i)))
                If Len(BodyFile) = 0 Then isBodyOK = False
            End If
            
            isBaseNameOK = True
            If (BV(Currbv).DatabaseNameFormat = "FILENAME") Then
                BaseFile = NoExtensionFileName(ListDoc.List(FileIndex(i)))
                If Len(BaseFile) > 8 Then
                    isBaseNameOK = False
                End If
            Else
                BaseFile = ""
            End If
                
            isConversionOK = False
            If isBodyOK And isBaseNameOK Then
                'Make the conversion
                If MakeConversion(ListDoc.List(FileIndex(i)), BodyFile, BaseFile, epubdate) Then
                    isConversionOK = True
                End If
            Else
                If Not isBodyOK Then MissingBody = MissingBody + vbCrLf + ListDoc.List(FileIndex(i))
                If Not isBaseNameOK Then InvalidBaseName = InvalidBaseName + vbCrLf + BaseFile
            End If
            
            If isConversionOK Then
                Success = Success + 1
                result = result + ListDoc.List(FileIndex(i)) + vbTab + "[Success]" + vbCrLf
            Else
                result = result + ListDoc.List(FileIndex(i)) + vbTab + "[Failure]" + vbCrLf
            End If
                            
            ListDoc.selected(FileIndex(i)) = False
            LabLeftMsg.Caption = ""
            ViewSuccessAndFailure
        Next
        
        If Len(MissingBody) > 0 Then Call Msg.GiveRunInformation(InterfaceLabels("MsgMissingBodyFiles").elem2 + MissingBody, True)
        If Len(InvalidBaseName) > 0 Then Call Msg.GiveRunInformation(InterfaceLabels("formmarkup_invaliddbname").elem2 + InvalidBaseName, True)
        If Len(BV(Currbv).DatabaseNameFormat) = 0 Then
            FinishDBConversion
        End If
        
        Call Msg.GiveRunInformation(InterfaceLabels("MsgTakenTotalTime").elem2 + CStr(DateDiff("s", T0, Time)))
            
        result = vbCrLf + result + vbCrLf + InterfaceLabels("MsgSucessPercent").elem2 + CStr(Success) + "/" + CStr(SelCount)
        FrmResult.Text1.text = result
        FrmResult.Show vbModal
    End If
    MousePointer = vbArrow
            
End Sub

'-----------------------------------------------------------------------
'List_GetSelectedItem    - Get the indexes of the selected files on the list
'List   - input
'ItemIndex  - output, indexes of the documents selected in <List>
'Return - number of selected document indexes
'-----------------------------------------------------------------------
Private Function List_GetSelectedItem(List As Object, ItemIndex() As Long) As Long
    Dim i As Long
    Dim j As Long
    
    Erase ItemIndex
    For i = 0 To List.ListCount - 1
        If List.selected(i) Then
            j = j + 1
            ReDim Preserve ItemIndex(j)
            ItemIndex(j) = i
        End If
    Next
    List_GetSelectedItem = j
End Function


'-----------------------------------------------------------------------
'List_SelectAll - Select all documents
'-----------------------------------------------------------------------
Private Sub List_SelectAll()
    Dim i As Long
    
    For i = 0 To ListDoc.ListCount - 1
        ListDoc.selected(i) = True
    Next

End Sub

'--------------------------------------------------------------------------------
'CmdViewLog_Click   - Show the conversion process steps of the selected
'documents on the list of documents loaded and/or failed
'--------------------------------------------------------------------------------
Private Sub CmdViewLog_Click()
    Dim i As Long
    Dim FileIndex() As Long
    Dim SelCount As Long
    Dim content As String
    Dim DocInDB As String
    
    SelCount = List_GetSelectedItem(ListInDB, FileIndex)
    
    For i = 1 To SelCount
        DocInDB = Mid(ListInDB.List(FileIndex(i)), 5)
        content = Msg.ViewLogDatabase(DocInDB)
        If Len(content) > 0 Then
            FormViewLog.TxtViewLog.text = content
            FormViewLog.Show vbModal
        Else
            MsgBox DocInDB + InterfaceLabels("MsgDocisnotloaded").elem2
        End If
        ListInDB.selected(FileIndex(i)) = False
    Next

    SelCount = List_GetSelectedItem(ListOutDB, FileIndex)
    
    For i = 1 To SelCount
        content = Msg.ViewLogDatabase(ListOutDB.List(FileIndex(i)))
        If Len(content) > 0 Then
            FormViewLog.TxtViewLog.text = content
            FormViewLog.Show vbModal
        Else
            MsgBox ListOutDB.List(FileIndex(i)) + InterfaceLabels("MsgDocisnotloaded").elem2
        End If
        ListOutDB.selected(FileIndex(i)) = False
    Next

End Sub


'--------------------------------------------------------------------------------
'ViewSuccessAndFailure - Show the documents which were successfully loaded and also
'the failed documents
'--------------------------------------------------------------------------------
Private Sub ViewSuccessAndFailure()
    Dim Success() As String
    Dim Failure() As String
    Dim ParserFail() As Boolean
    Dim QSuccess As Long
    Dim QFailure As Long
    Dim q As Long
    Dim i As Long
    Dim StatusParser As String
    Dim msgStatusParser As String
    
    q = Msg.GetDocLoadStatus(Success, QSuccess, Failure, QFailure, ParserFail)
    ListInDB.Clear
    For i = 1 To QSuccess
        If ParserFail(i) Then
            StatusParser = "[X] "
            msgStatusParser = "Markup errors in [X] Loaded Document(s)."
        Else
            StatusParser = "[ ] "
        End If
        
        If ListDocExistFile(Success(i)) Then ListInDB.AddItem (StatusParser + Success(i))
    Next
    LabSuccessCount.Caption = InterfaceLabels("LabFileCount").elem2 + CStr(ListInDB.ListCount)
    ListOutDB.Clear
    For i = 1 To QFailure
        If ListDocExistFile(Failure(i)) Then ListOutDB.AddItem (Failure(i))
    Next
    LabFailCount.Caption = InterfaceLabels("LabFileCount").elem2 + CStr(ListOutDB.ListCount)
    If Len(msgStatusParser) > 0 Then
        Call Msg.GiveRunInformation(msgStatusParser, , True)
    End If
End Sub

Private Function ListDocExistFile(FileName As String) As Boolean
    Dim i As Long
    Dim found As Boolean
    
    i = 0
    While (i < ListDoc.ListCount) And (Not found)
        found = (StrComp(ListDoc.List(i), FileName, vbTextCompare) = 0)
        i = i + 1
    Wend
    ListDocExistFile = found
End Function



Private Sub ListDoc_Click()
    Dim i As Long
    Dim selected As Boolean
    
    i = 0
    While (i < ListDoc.ListCount) And (Not selected)
        selected = ListDoc.selected(i)
        i = i + 1
    Wend
    CmdLoad.Enabled = selected
End Sub

Private Sub ListInDB_Click()
    CmdViewLog.Enabled = ((ListInDB.SelCount > 0) Or (ListOutDB.SelCount > 0))
End Sub

Private Sub ListOutDB_Click()
    CmdViewLog.Enabled = ((ListInDB.SelCount > 0) Or (ListOutDB.SelCount > 0))
End Sub

Private Sub CmdHelp_Click()
    Call openHelp(ConvertDirTree.DirNodes("Help of Markup").Parent.fullpath, ConvertDirTree.DirNodes("Help of Markup").text)
End Sub

Private Sub cmdclose_Click()
    MarkupForm_Close
End Sub

Private Sub cmdLoad_Click()
    Call LoadDocDatabase(TextEPubDate.text)
End Sub

Private Sub InputBox_Changed()
    Components_Enable (False)
    ListInDB.Clear
    ListOutDB.Clear
End Sub

Private Sub InputBox_Clean()
    Dim i As Long
    
    For i = 1 To TextBoxCounter
        TxtFolder(i).text = ""
    Next
    TextEPubDate.Visible = False
    labEPubDate.Visible = False
    
End Sub

Private Sub Components_View(Flag As Boolean)
    Dim i As Long
    Dim j As Long
    Dim q As Long
    
    
    With BV(Currbv)
    q = .Directory.Count
    While i < q
        i = i + 1
        Select Case .Directory(i).ObjTypeDir
        Case "combo"
            ComboFolder(i).Visible = Flag
            TxtFolder(i).Visible = Not Flag
        Case "text", "label"
            ComboFolder(i).Visible = Not Flag
            TxtFolder(i).Visible = Flag
        End Select
    Wend
    While i < TextBoxCounter
        i = i + 1
        ComboFolder(i).Visible = Not Flag
        TxtFolder(i).Visible = Not Flag
        LabFolder(i).Visible = Not Flag
    Wend
    End With
End Sub

Private Sub TxtFolder_Change(Index As Integer)
    InputBox_Changed
    checkEPubDateIsMandatory
End Sub
