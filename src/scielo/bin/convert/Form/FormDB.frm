VERSION 5.00
Begin VB.Form FormDB 
   Caption         =   "Database"
   ClientHeight    =   4755
   ClientLeft      =   1920
   ClientTop       =   2205
   ClientWidth     =   8025
   LinkTopic       =   "Form1"
   ScaleHeight     =   4755
   ScaleMode       =   0  'User
   ScaleWidth      =   8069.013
   Begin VB.ListBox Listado 
      Height          =   3435
      Left            =   120
      Sorted          =   -1  'True
      Style           =   1  'Checkbox
      TabIndex        =   2
      Top             =   120
      Width           =   7695
   End
   Begin VB.CommandButton CmdOK 
      Caption         =   "Create ISO list"
      Height          =   495
      Left            =   240
      TabIndex        =   1
      Top             =   3960
      Width           =   1455
   End
   Begin VB.CommandButton CmdClose 
      Caption         =   "close"
      Height          =   495
      Left            =   1800
      TabIndex        =   0
      Top             =   3960
      Width           =   1455
   End
   Begin VB.Label LabCount 
      Caption         =   "Label1"
      Height          =   495
      Left            =   3840
      TabIndex        =   3
      Top             =   3960
      Width           =   3975
   End
End
Attribute VB_Name = "FormDB"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Private Sub cmdclose_Click()
    Unload Me
End Sub

Private Sub cmdOK_Click()
    CreateIsoList
    Unload Me
End Sub

Private Sub Form_Load()
    
    Caption = InterfaceLabels("formdb_caption").elem2
    If Len(Currbv) > 0 Then Caption = BV(Currbv).BVname + " - " + Caption
    
    CmdOK.Caption = InterfaceLabels("CmdOK").elem2
    CmdClose.Caption = InterfaceLabels("cmdclose").elem2

End Sub

Private Sub GetFileNames(Path As String, DirName As ColPair, FileName As ColPair, ByVal level As Long)
    Dim MyName As String
    Dim MyPath As String
    Dim MyItem As ClPair
    Dim i As Long
    Dim P As Long
    Dim fn As Long
    
    Debug.Print FileName.Count
    Set MyItem = New ClPair
        
    level = level + 1
    MyPath = Path & PathSep
    MyName = dir(MyPath, vbDirectory)
    Do While MyName <> ""
                
        If MyName <> "." And MyName <> ".." Then
            If (GetAttr(MyPath & MyName) And vbDirectory) = vbDirectory Then
                If (MyName Like BV(Currbv).FileTree.dirnodes("Database Directory").text) Then
                    Set MyItem = DirName.Add(MyName)
                    MyItem.elem1 = "dir"
                    MyItem.elem2 = MyName
                Else
                    If level <= BV(Currbv).Directory.Count Then
                        If (MyName Like BV(Currbv).Directory(level).pattern) Then
                            Set MyItem = DirName.Add(MyName)
                            MyItem.elem1 = "dir"
                            MyItem.elem2 = MyName
                            
                        End If
                    End If
                End If
            Else
                If MyName Like (BV(Currbv).DatabaseNamePattern & ".mst") Then
                    Set MyItem = DirName.Add(MyName)
                    MyItem.elem1 = "file"
                    MyItem.elem2 = MyName
                End If
            End If
        End If
        MyName = dir
    Loop
    For i = 1 To DirName.Count
        Debug.Print DirName(i).elem1, MyPath & DirName(i).elem2
        Set DirName(i).Pointer = New ColPair
        If DirName(i).elem1 = "dir" Then
            DirName(i).elem1 = MyPath
            Call GetFileNames(MyPath & DirName(i).elem2, DirName(i).Pointer, FileName, level)
        ElseIf DirName(i).elem1 = "file" Then
            Set MyItem = FileName.Add(MyPath & DirName(i).elem2)
            MyItem.elem1 = Mid(MyPath, 1, Len(MyPath) - 1)
            P = InStr(DirName(i).elem2, ".mst")
            MyItem.elem2 = Mid(DirName(i).elem2, 1, P - 1)
        End If
    Next
    
End Sub

Private Sub CreateIsoList()
    Dim isisdb As ClDBDoc
    Dim i As Long
    Dim isodb As ClISODB
    Dim Path As String
    Dim File As String
    
    Set isisdb = New ClDBDoc
    Set isodb = New ClISODB
            
    For i = 1 To Listado.ListCount
        If Listado.selected(i - 1) Then
            Call SeparateFileandPath(Listado.List(i - 1), Path, File)
            If isisdb.Initiate(Path, File, "") Then
                Call isodb.ISOUpdate(isisdb.GetDatabaseId, Mid(Path, 1, 2), Mid(Path, 4), File)
            End If
        End If
    Next
    Set isisdb = Nothing
    Set isodb = Nothing
    
    
End Sub
    
Sub GenerateList()
    Dim databases As ColPair
    Dim startdir As String
    Dim i As Long
    Dim isodb As ClISODB
    Dim isisdb As ClDBDoc
    Dim files As ColPair
    Dim result() As String
    Dim DBId As String
    
    
    Set databases = New ColPair
    Set isodb = New ClISODB
    Set files = New ColPair
    
    With BV(Currbv)
    If Not DirExist(.FileTree.dirnodes("iso list database").fullpath) Then MakeDir .FileTree.dirnodes("iso list database").fullpath
    Call FileCopy(ConvertDirTree.dirnodes("ISO fst").fullpath, .FileTree.dirnodes("iso list database").fullpath + ".fst")
    
    startdir = .FileTree.dirnodes("Serial Directory").fullpath
    Call GetFileNames(startdir, databases, files, 0)
    End With
    
    Listado.Clear
    For i = 1 To files.Count
        Set isisdb = New ClDBDoc
        If isisdb.Initiate(files(i).elem1, files(i).elem2, "") Then
            DBId = isisdb.GetDatabaseId
            If Len(DBId) > 0 Then
                If isodb.ISOSearch(Chr(34) + "ID=" + DBId + Chr(34), "mfn", result) = 0 Then
                    Listado.AddItem files.item(i).elem1 & PathSep & files.item(i).elem2
                End If
            End If
        End If
        Set isisdb = Nothing
    Next
    LabCount.Caption = CStr(Listado.ListCount) + " databases"
    
    For i = 1 To Listado.ListCount
        Listado.selected(i - 1) = True
    Next
    
    Set databases = Nothing
    Set isodb = Nothing
    Set files = Nothing
    
    MousePointer = vbArrow
    
    Show vbModal
End Sub

