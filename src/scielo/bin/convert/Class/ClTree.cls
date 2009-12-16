VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClTree"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

'store the struct directory
Public DirNodes As Nodes

'flag to file required or not
Private FileNotRequired() As Boolean
Private counter As Long

'------------------------------------------------------------------------
'MakeTree - Read the file to build the directory structure
'file - input file name
'DirStruct - input, initiate the directory struct to be built
'Root - output, directory struct root
'------------------------------------------------------------------------
Sub MakeTree(File As String, DirStruct As Nodes, root As String)
    Dim fn As Long
    Dim father As String
    Dim child As String
    Dim Info As String
    Dim NotRequired As Integer
    Dim i As Long
    
    Set DirNodes = DirStruct
    
    counter = 0
    fn = FreeFile
    Open File For Input As fn
        
    If Not EOF(fn) Then
        Input #fn, father, child, Info, NotRequired
        
        If Len(child) > 0 Then root = child
        
        counter = counter + 1
        ReDim Preserve FileNotRequired(counter)
        FileNotRequired(counter) = (NotRequired = 1)
        
        If Len(father) > 0 Then
            Call DirNodes.Add(father, tvwChild, Info, root)
        Else
            Call DirNodes.Add(, , Info, root)
        End If
        DirNodes(Info).Expanded = True
    End If
    
    While Not EOF(fn)
        Input #fn, father, child, Info, NotRequired
        
        counter = counter + 1
        ReDim Preserve FileNotRequired(counter)
        FileNotRequired(counter) = (NotRequired = 1)
        
        If Len(father) > 0 Then
            Call DirNodes.Add(father, tvwChild, Info, child)
        Else
            Call DirNodes.Add(, , Info, child)
        End If
        DirNodes(Info).Expanded = True
    
    Wend
    Close fn
    
End Sub


'------------------------------------------------------------------------
'CheckFilePath - Check wheter the directory struct files exist or not,
'considering whether they are required or not
'Return <TRUE> when all the required files exist
'------------------------------------------------------------------------
Function CheckFilePath() As Boolean
    Dim ret As Boolean
    Dim i As Long
    
    ret = True
        
    For i = 1 To DirNodes.Count
        With DirNodes(i)
        If DirExist(.FullPath) Then
        
        ElseIf FileExist(.Parent.FullPath, .Text) Then
            
        ElseIf FileExist(.Parent.FullPath, .Text + ".mst") Then
        
        ElseIf FileExist(.Parent.FullPath, .Text + ".fst") Then
        
        ElseIf FileNotRequired(.Index) Then
        
        Else
            ret = ret And False
            Call Msg.MsgInvalidPath(.key, .FullPath)
        End If
        End With
    Next
        
    CheckFilePath = ret
End Function

Private Sub Class_Terminate()
    Set DirNodes = Nothing

    Erase FileNotRequired

End Sub
