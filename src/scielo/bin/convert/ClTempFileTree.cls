VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClTempFileTree"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Public dirnodes As Collection
'------------------------------------------------------------------------
'CheckFilePath - Check wheter the directory struct files exist or not,
'considering whether they are required or not
'Return <TRUE> when all the required files exist
'------------------------------------------------------------------------
Function CheckFilePath() As Boolean
    Dim ret As Boolean
    Dim i As Long
    
    ret = True
        
    For i = 1 To dirnodes.Count
        With dirnodes(i)
        Debug.Print dirnodes(i).key
        
        If dirnodes(i).fullpath = "" Then
        
        Else
            If DirExist(.fullpath) Then
            
            ElseIf FileExist(.fullpath, .text) Then
                
            ElseIf FileExist(.fullpath, .text + ".mst") Then
            
            ElseIf FileExist(.fullpath, .text + ".fst") Then
                        
            ElseIf Not .required Then
            Else
                ret = ret And False
                Call Msg.MsgInvalidPath(.key, .fullpath)
            End If
        End If
        End With
    Next
        
    CheckFilePath = ret
End Function
