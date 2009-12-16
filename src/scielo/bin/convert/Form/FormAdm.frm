VERSION 5.00
Begin VB.Form FormAdm 
   ClientHeight    =   4755
   ClientLeft      =   60
   ClientTop       =   345
   ClientWidth     =   8250
   LinkTopic       =   "Form1"
   ScaleHeight     =   4755
   ScaleWidth      =   8250
   StartUpPosition =   2  'CenterScreen
   Begin VB.TextBox TxtDetails 
      Height          =   1695
      Left            =   4200
      Locked          =   -1  'True
      MultiLine       =   -1  'True
      ScrollBars      =   2  'Vertical
      TabIndex        =   6
      Text            =   "FormAdm.frx":0000
      Top             =   2880
      Width           =   3855
   End
   Begin VB.Frame Frame2 
      Caption         =   "Frame2"
      Height          =   3495
      Left            =   120
      TabIndex        =   9
      Top             =   1200
      Width           =   8055
      Begin VB.CommandButton CmdSelectAll 
         Caption         =   "Command1"
         Height          =   615
         Left            =   6840
         TabIndex        =   10
         Top             =   240
         Width           =   1095
      End
      Begin VB.CommandButton CmdDelete 
         Caption         =   "Command1"
         Height          =   615
         Left            =   6840
         TabIndex        =   4
         Top             =   960
         Width           =   1095
      End
      Begin VB.TextBox TxtReport 
         Height          =   1695
         Left            =   120
         Locked          =   -1  'True
         MultiLine       =   -1  'True
         ScrollBars      =   2  'Vertical
         TabIndex        =   5
         Text            =   "FormAdm.frx":0006
         Top             =   1680
         Width           =   3855
      End
      Begin VB.ListBox DBList 
         Height          =   1185
         Left            =   120
         Sorted          =   -1  'True
         Style           =   1  'Checkbox
         TabIndex        =   3
         Top             =   360
         Width           =   6615
      End
   End
   Begin VB.Frame Frame1 
      Height          =   975
      Left            =   120
      TabIndex        =   7
      Top             =   120
      Width           =   8055
      Begin VB.CommandButton CmdClose 
         Caption         =   "Command1"
         Height          =   375
         Left            =   6840
         TabIndex        =   2
         Top             =   480
         Width           =   1095
      End
      Begin VB.CommandButton CmdFind 
         Caption         =   "Cmd"
         Height          =   375
         Left            =   5640
         TabIndex        =   1
         Top             =   480
         Width           =   1095
      End
      Begin VB.ComboBox ComboSearchType 
         Height          =   315
         Left            =   120
         Style           =   2  'Dropdown List
         TabIndex        =   0
         Top             =   480
         Width           =   5295
      End
      Begin VB.Label LabSearchType 
         Caption         =   "Search Type"
         Height          =   255
         Left            =   120
         TabIndex        =   8
         Top             =   240
         Width           =   1575
      End
   End
End
Attribute VB_Name = "FormAdm"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit


Private NormalHeight As Long
Private NormalWidth As Long

Private OldHeight As Long
Private OldWidth As Long


Private SearchTypes As ColPair
Private DBInfo As ColPair
Private TotalCount As Long
Private info_pft As String
    
    
Sub OpenForm()
    Dim i As Long
    Dim fn As Long
    Dim st As ClPair
    Dim code As String
    Dim Value As String
    
    
    Set SearchTypes = New ColPair
    Set st = New ClPair
    
    ComboSearchType.Clear
    TxtReport.text = ""
    TxtDetails.text = ""
    
    info_pft = BV(Currbv).SearchOptions.ReturnInfoPft
        
    fn = FreeFile
    Open ConvertDirTree.DirNodes("Search Types").Parent.fullpath + "\" + IdiomHelp(CurrIdiomHelp).code + "_" + ConvertDirTree.DirNodes("Search Types").text For Input As fn
    While Not EOF(fn)
        Input #fn, code, Value
        Set st = SearchTypes.Add(Value)
        st.elem1 = code
        st.elem2 = Value
        ComboSearchType.AddItem Value
    Wend
    Close fn
    ComboSearchType.ListIndex = 0
    
    Caption = InterfaceLabels("formadm_Caption").elem2
    Frame1.Caption = InterfaceLabels("formadm_FrameFind").elem2
    LabSearchType.Caption = InterfaceLabels("formadm_labsearchtype").elem2
    CmdFind.Caption = InterfaceLabels("CmdFind").elem2
    CmdClose.Caption = InterfaceLabels("cmdclose").elem2
    Frame2.Caption = InterfaceLabels("formadm_FrameDelete").elem2
    CmdDelete.Caption = InterfaceLabels("CmdDelete").elem2
    CmdSelectAll.Caption = InterfaceLabels("CmdSelectAll").elem2
    
    Show vbModal
End Sub

Private Sub CreateReport()
    
    
End Sub

Private Sub CmdDelete_Click()
    Dim i As Long
    Dim iso As ClISODB
    Dim deldb() As String
    Dim delcount As Long
    
    While DBList.SelCount > 0
        If DBList.selected(i) Then
            If FormDelete.Delete(DBList.List(i), DBInfo(DBList.List(i)).elem3) Then
                delcount = delcount + 1
                ReDim Preserve deldb(delcount)
                deldb(delcount) = DBInfo(DBList.List(i)).elem2
                DBInfo.Remove (DBList.List(i))
                DBList.RemoveItem (i)
            Else
                DBList.selected(i) = False
                i = i + 1
            End If
        Else
            i = i + 1
        End If
    Wend
    
    Set iso = New ClISODB
    Call iso.DBDelete(deldb, delcount, TotalCount)
    Set iso = Nothing
                
    TxtReport.text = InterfaceLabels("formadm_FoundDB").elem2 + CStr(DBList.ListCount) + Chr(13) + Chr(10)
    TxtReport.text = TxtReport.text + InterfaceLabels("formadm_TotalDB").elem2 + CStr(TotalCount) + Chr(13) + Chr(10)
    TxtReport.text = TxtReport.text + InterfaceLabels("formadm_SelectedDB").elem2 + CStr(DBList.SelCount) + Chr(13) + Chr(10)
    TxtReport.text = TxtReport.text + InterfaceLabels("formadm_DeletedDB").elem2 + CStr(delcount) + Chr(13) + Chr(10)
    
    TxtDetails.text = ""
                
                
End Sub

Private Sub CmdFind_Click()
    Dim chosen_option As String
    Dim i As Long
    Dim fn As Long
    
    MousePointer = vbHourglass
    While (i < SearchTypes.Count) And (Len(chosen_option) = 0)
        i = i + 1
        If StrComp(SearchTypes(i).elem2, ComboSearchType.text, vbTextCompare) = 0 Then
            chosen_option = SearchTypes(i).elem1
        End If
    Wend
    Select Case chosen_option
    Case "ALL"
        ListAll
    Case "PARTIAL"
        ListPartially
    Case "RECREATE"
        RecreateList
        ListAll
    Case Else
        ListAll
    End Select
    'SelectOptions
    
    TxtReport.text = InterfaceLabels("formadm_FoundDB").elem2 + CStr(DBInfo.Count) + Chr(13) + Chr(10)
    TxtReport.text = TxtReport.text + InterfaceLabels("formadm_TotalDB").elem2 + CStr(TotalCount) + Chr(13) + Chr(10)
    TxtReport.text = TxtReport.text + InterfaceLabels("formadm_SelectedDB").elem2 + CStr(DBList.SelCount) + Chr(13) + Chr(10)
    
    If DBList.ListIndex >= 0 Then
      TxtDetails.text = DBList.List(DBList.ListIndex) + Chr(13) + Chr(10) + DBInfo.Item(DBList.List(DBList.ListIndex)).elem3
    Else
      TxtDetails.text = ""
    End If
    MousePointer = vbArrow
End Sub

Private Sub CmdSelectAll_Click()
    SelectOptions
End Sub

Private Sub DBList_Click()
    
    TxtReport.text = InterfaceLabels("formadm_FoundDB").elem2 + CStr(DBInfo.Count) + Chr(13) + Chr(10)
    TxtReport.text = TxtReport.text + InterfaceLabels("formadm_TotalDB").elem2 + CStr(TotalCount) + Chr(13) + Chr(10)
    TxtReport.text = TxtReport.text + InterfaceLabels("formadm_SelectedDB").elem2 + CStr(DBList.SelCount) + Chr(13) + Chr(10)
    
    TxtDetails.text = DBList.List(DBList.ListIndex) + Chr(13) + Chr(10) + DBInfo.Item(DBList.List(DBList.ListIndex)).elem3
    
End Sub

Private Sub DBList_ItemCheck(Item As Integer)
    TxtReport.text = InterfaceLabels("formadm_FoundDB").elem2 + CStr(DBInfo.Count) + Chr(13) + Chr(10)
    TxtReport.text = TxtReport.text + InterfaceLabels("formadm_TotalDB").elem2 + CStr(TotalCount) + Chr(13) + Chr(10)
    TxtReport.text = TxtReport.text + InterfaceLabels("formadm_SelectedDB").elem2 + CStr(DBList.SelCount) + Chr(13) + Chr(10)
End Sub

Private Sub Form_Load()
    
    OldHeight = Height
    OldWidth = Width
    NormalHeight = Height
    NormalWidth = Width
    
End Sub


Private Sub cmdclose_Click()
    Unload Me
End Sub

Private Sub ListAll()
    Dim iso As ClISODB
    
    Set iso = New ClISODB
    Call iso.ISOList(DBList, DBInfo, info_pft, TotalCount)
    Set iso = Nothing
    
End Sub
Private Sub ListPartially()
    Dim iso As ClISODB
    Dim expr As String
    
    MousePointer = vbHourglass
    Set iso = New ClISODB
    If FormSearchDB.ReturnSearchExpression(expr) Then
        Call iso.ISOList(DBList, DBInfo, info_pft, TotalCount, expr)
    End If
    Set iso = Nothing
    MousePointer = vbArrow
End Sub
Private Sub RecreateList()
    FormDB.GenerateList
End Sub
Private Sub SelectOptions()
    Dim i As Long
    
    For i = 1 To DBList.ListCount
        DBList.selected(i - 1) = True
    Next
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
    Call Components_ChangeSize(LabSearchType, x, Y, 1, 1)
    Call Components_ChangeSize(ComboSearchType, x, Y, x, 1)
    Call Components_ChangeSize(CmdFind, x, Y, x, 1)
    Call Components_ChangeSize(CmdClose, x, Y, x, 1)
    Call Components_ChangeSize(Frame2, x, Y, x, Y)
    Call Components_ChangeSize(CmdDelete, x, Y, x, 1)
    Call Components_ChangeSize(DBList, x, Y, x, Y)
    Call Components_ChangeSize(TxtReport, x, Y, x, Y)
    Call Components_ChangeSize(TxtDetails, x, Y, x, Y)
    Call Components_ChangeSize(CmdSelectAll, x, Y, x, 1)
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

