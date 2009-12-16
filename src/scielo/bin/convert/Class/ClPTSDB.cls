VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClPTSDB"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

Sub PTSUpdate(eventdata As String)
    
    Dim PTSDB As ClIsisDll
    Dim Mfn As Long
    Dim P As Long
    Dim PathBase As String
    
    Set PTSDB = New ClIsisDll
    With BV(Currbv)
    If Not DirExist(.FileTree.DirNodes("pts database").FullPath) Then MakeDir .FileTree.DirNodes("pts database").FullPath
    Call FileCopy(ConvertDirTree.DirNodes("Library Directory").FullPath + PathSep + Currbv + PathSep + .FileTree.DirNodes("pts fst file").text + ".fst", .FileTree.DirNodes("pts fst file").FullPath + "\" + .FileTree.DirNodes("pts fst file").text + ".fst")
    
    If PTSDB.Initiate(.FileTree.DirNodes("pts database").FullPath, .FileTree.DirNodes("pts database").text, .FileTree.DirNodes("pts database").key) Then
        If PTSDB.IfCreate(.FileTree.DirNodes("pts fst file").text, .FileTree.DirNodes("pts database").key) Then
            Mfn = PTSDB.RecordSave(eventdata)
            If Mfn > 0 Then Call PTSDB.IfUpdate(1, Mfn)
        End If
    End If
    Set PTSDB = Nothing

    End With

End Sub


Function PTSSearch(query As String, ResultPft As String, result() As String) As Long
    
    Dim PTSDB As ClIsisDll
    Dim Mfns() As Long
    Dim q As Long
    Dim i As Long
    
    Set PTSDB = New ClIsisDll
    With BV(Currbv)
    If PTSDB.Initiate(.FileTree.DirNodes("pts database").FullPath, .FileTree.DirNodes("pts database").text, .FileTree.DirNodes("pts database").key) Then
        If PTSDB.IfCreate(.FileTree.DirNodes("pts fst file").text, .FileTree.DirNodes("pts database").key) Then
            q = PTSDB.DoSearch(query, Mfns)
            For i = 1 To q
                ReDim Preserve result(i)
                result(i) = PTSDB.UsePft(Mfns(i), ResultPft)
            Next
        End If
    End If
    End With
    Set PTSDB = Nothing
    PTSSearch = q
End Function


