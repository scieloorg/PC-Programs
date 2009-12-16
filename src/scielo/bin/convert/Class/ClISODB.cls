VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClISODB"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

Private MfnInfo As Long

Sub ISOUpdate(DatabaseId As String, drv As String, Path As String, File As String)
    
    Dim isodb As ClIsisDll
    Dim Mfn As Long
    Dim IDMfns() As Long
    Dim q1 As Long
    Dim PathMfns() As Long
    Dim q2 As Long
    Dim status As String
    Dim content As String
    Dim fn As Long
    Dim dbclean As Boolean
    
    Dim i As Long
    
    Dim IDMfn As Long
    Dim PathMfn As Long
    
    
    Set isodb = New ClIsisDll
    With BV(Currbv)
    If Not DirExist(.FileTree.DirNodes("iso list database").fullpath) Then MakeDir .FileTree.DirNodes("iso list database").fullpath
    Call FileCopy(ConvertDirTree.DirNodes("ISO fst").fullpath, .FileTree.DirNodes("iso list database").fullpath + "\" + .FileTree.DirNodes("iso list database").text + ".fst")
    If isodb.Initiate(.FileTree.DirNodes("iso list database").fullpath, .FileTree.DirNodes("iso list database").text, .FileTree.DirNodes("iso list database").key) Then
        If isodb.IfCreate(.FileTree.DirNodes("iso list database").text, .FileTree.DirNodes("iso list database").key) Then
            If isodb.MfnQuantity > 0 Then
                q1 = isodb.DoSearch("ID=" + DatabaseId, IDMfns)
                If q1 > 0 Then
                    i = 0
                    While (IDMfn = 0) And (i < q1)
                        i = i + 1
                        If StrComp(DatabaseId, isodb.UsePft(IDMfns(i), "v2"), vbTextCompare) = 0 Then
                            IDMfn = IDMfns(i)
                        End If
                    Wend
                End If
            
                q2 = isodb.DoSearch("PATH=$", PathMfns)
                If q2 > 0 Then
                    If q2 < isodb.MfnQuantity Then
                        i = 0
                        While (PathMfn = 0) And (i < isodb.MfnQuantity)
                            i = i + 1
                            If StrComp(drv + PathSep + Path + PathSep + File, isodb.UsePft(i, "v10"), vbTextCompare) = 0 Then
                                PathMfn = i
                            End If
                        Wend
                    Else
                        q2 = isodb.DoSearch("PATH=" + ReplaceString(drv + PathSep + Path + PathSep + File, "\", "\\", vbBinaryCompare), PathMfns)
                        i = 0
                        While (PathMfn = 0) And (i < q2)
                            i = i + 1
                            If StrComp(drv + PathSep + Path + PathSep + File, isodb.UsePft(PathMfns(i), "v10"), vbTextCompare) = 0 Then
                                PathMfn = PathMfns(i)
                            End If
                        Wend
                        If q2 = 0 Then
                            q2 = isodb.DoSearch("PATH=" + drv + PathSep + Path + PathSep + File, PathMfns)
                            i = 0
                            While (PathMfn = 0) And (i < q2)
                                i = i + 1
                                If StrComp(drv + PathSep + Path + PathSep + File, isodb.UsePft(PathMfns(i), "v10"), vbTextCompare) = 0 Then
                                    PathMfn = PathMfns(i)
                                End If
                            Wend
                        End If
                    End If
                End If
                
                If IDMfn = PathMfn Then
                    Mfn = IDMfn
                Else
                    If (IDMfn > 0) And (PathMfn > 0) Then
                        If isodb.RecordDel(PathMfn) Then
                            If isodb.IfUpdate(PathMfn, PathMfn) Then
                                Mfn = IDMfn
                                dbclean = True
                            End If
                        End If
                    ElseIf IDMfn = 0 Then
                        Mfn = PathMfn
                    ElseIf PathMfn = 0 Then
                        Mfn = IDMfn
                    End If
                End If
                status = isodb.UsePft(Mfn, "v20")
                Select Case status
                Case "0", "1"
                Case "2"
                    status = "1"
                Case Else
                    status = "0"
                End Select
            
            End If
            
            content = content + isodb.TagContents(DatabaseId, 2)
            content = content + isodb.TagContents(status, 20)
            content = content + isodb.TagContents(drv, 11)
            content = content + isodb.TagContents(Path, 12)
            content = content + isodb.TagContents(File, 13)
            content = content + isodb.TagContents(drv + PathSep + Path + PathSep + File, 10)
            content = content + isodb.TagContents(ReplaceString(PathSep + Path + PathSep + File, PathSep, "/", vbBinaryCompare), 15)
            
            If Mfn = 0 Then
                Mfn = isodb.RecordSave(content)
                If Mfn > 0 Then Call isodb.IfUpdate(Mfn, Mfn)
            Else
                If isodb.RecordUpdate(Mfn, content) Then Call isodb.IfUpdate(Mfn, Mfn)
            End If
        End If
    End If
    
    Set isodb = Nothing
    
    If dbclean Then
        Set isodb = New ClIsisDll
        If isodb.Initiate(.FileTree.DirNodes("iso list database").fullpath, .FileTree.DirNodes("iso list database").text, .FileTree.DirNodes("iso list database").key) Then
            If isodb.IfCreate(.FileTree.DirNodes("iso list database").text, .FileTree.DirNodes("iso list database").key) Then
                isodb.BDClean
            End If
        End If
        Set isodb = Nothing
    End If
    
    End With
End Sub

Function ISOSearch(query As String, ResultPft As String, result() As String) As Long
    
    Dim isodb As ClIsisDll
    Dim Mfns() As Long
    Dim q As Long
    Dim i As Long
    
    Set isodb = New ClIsisDll
    With BV(Currbv)
    If isodb.Initiate(.FileTree.DirNodes("iso list database").fullpath, .FileTree.DirNodes("iso list database").text, .FileTree.DirNodes("iso list database").key) Then
        If isodb.IfCreate(.FileTree.DirNodes("iso list database").text, .FileTree.DirNodes("iso list database").key) Then
            q = isodb.DoSearch(query, Mfns)
            For i = 1 To q
                ReDim Preserve result(i)
                result(i) = isodb.UsePft(Mfns(i), ResultPft)
            Next
        End If
    End If
    End With
    Set isodb = Nothing
    ISOSearch = q
End Function

Sub Old_ISOUpdate(DatabaseId As String, drv As String, Path As String, File As String)
    
    Dim isodb As ClIsisDll
    Dim Mfn As Long
    Dim Mfns() As Long
    Dim q As Long
    Dim status As String
    Dim content As String
    Dim fn As Long
    
    Set isodb = New ClIsisDll
    With BV(Currbv)
    If Not DirExist(.FileTree.DirNodes("iso list database").fullpath) Then MakeDir .FileTree.DirNodes("iso list database").fullpath
    Call FileCopy(ConvertDirTree.DirNodes("ISO fst").fullpath, .FileTree.DirNodes("iso list database").fullpath + ".fst")
    If isodb.Initiate(.FileTree.DirNodes("iso list database").fullpath, .FileTree.DirNodes("iso list database").text, .FileTree.DirNodes("iso list database").key) Then
        If isodb.IfCreate(.FileTree.DirNodes("iso list database").text, .FileTree.DirNodes("iso list database").key) Then
            q = isodb.DoSearch("ID=" + DatabaseId, Mfns)
            If q = 1 Then
                status = isodb.UsePft(Mfns(q), "v20")
                Mfn = Mfns(q)
                If status = "2" Then
                    Call isodb.FieldContentUpdate(Mfn, 20, "1")
                    Call isodb.IfUpdate(Mfn, Mfn)
                ElseIf status = "" Then
                    Call isodb.FieldContentAdd(Mfn, 20, "0")
                    Call isodb.IfUpdate(Mfn, Mfn)
                End If
            ElseIf q = 0 Then
                status = "0"
                content = content + isodb.TagContents(DatabaseId, 2)
                content = content + isodb.TagContents(status, 20)
                content = content + isodb.TagContents(drv, 11)
                content = content + isodb.TagContents(Path, 12)
                content = content + isodb.TagContents(File, 13)
                content = content + isodb.TagContents(drv + PathSep + Path + PathSep + File, 10)
                content = content + isodb.TagContents(ReplaceString(PathSep + Path + PathSep + File, PathSep, "/", vbBinaryCompare), 15)
                Mfn = isodb.RecordSave(content)
                If Mfn > 0 Then Call isodb.IfUpdate(Mfn, Mfn)
            Else
                Call Msg.GiveRunInformation("problem in iso file", True)
            End If
        End If
    End If
    End With
    Set isodb = Nothing

End Sub


Sub ISOList(DBList As ListBox, DBInfo As ColPair, InfoPFT As String, TotalCount As Long, Optional SearchExpr As String)
    Dim logDB As ClMsg
    Dim isodb As ClIsisDll
    Dim Mfn As Long
    Dim dbi As ClPair
    Dim DBFullPath As String
    Dim DBPath As String
    Dim DBFile As String
    Dim DBDrive As String
    Dim db As ClIsisDll
    Dim xMfn As String
    Dim p As Long
    
    TotalCount = 0
    
    Set isodb = New ClIsisDll
    DBList.Clear
    Set DBInfo = New ColPair
    
    
    With BV(Currbv)
    
    If isodb.Initiate(.FileTree.DirNodes("iso list database").fullpath, .FileTree.DirNodes("iso list database").text, .FileTree.DirNodes("iso list database").key) Then
        If isodb.IfCreate(.FileTree.DirNodes("iso list database").text) Then
            TotalCount = isodb.MfnQuantity
            If Len(SearchExpr) = 0 Then
                For Mfn = 1 To isodb.MfnQuantity
                    DBFullPath = isodb.UsePft(Mfn, "v10")
                    DBDrive = isodb.UsePft(Mfn, "v11")
                    DBPath = isodb.UsePft(Mfn, "v12")
                    DBFile = isodb.UsePft(Mfn, "v13")
                    
                    If FileExist(DBDrive + "\" + DBPath, DBFile + ".iso") Then
                        Set db = New ClIsisDll
                        If db.Initiate(DBDrive + "\" + DBPath, DBFile, DBFile) Then
                            xMfn = db.UsePft(MfnInfo, InfoPFT)
                        End If
                        
                        Set dbi = New ClPair
                        Set dbi = DBInfo.Add(DBFullPath)
                        DBList.AddItem (DBFullPath)
                        dbi.elem1 = DBFullPath
                        dbi.elem2 = isodb.UsePft(Mfn, "v2")
                        dbi.elem3 = xMfn
                        
                        Set dbi = Nothing
                        Set db = Nothing
                    Else
                        If isodb.RecordDel(Mfn) Then
                            If isodb.IfUpdate(Mfn, Mfn) Then
                                Set logDB = New ClMsg
                                If StrComp(.FileTree.DirNodes("Log Directory").text, .FileTree.DirNodes("Database Directory").text, vbTextCompare) = 0 Then
                                    Call logDB.InitLogDatabase(DBDrive + "\" + DBPath, DBFile + "log")
                                    logDB.DelLogDatabase
                                Else
                                    p = InStr(DBPath, "\" + .FileTree.DirNodes("Database Directory").text)
                                    If p > 0 Then
                                        Call logDB.InitLogDatabase(DBDrive + "\" + Mid(DBPath, 1, p) + .FileTree.DirNodes("Log Directory").text, .FileTree.DirNodes("Log File").text)
                                        logDB.DeleteRecord (DBFile)
                                    End If
                                End If
                                
                                Set logDB = Nothing
                            End If
                        End If
                        
                    End If
                    
                Next
            Else
                For Mfn = 1 To isodb.MfnQuantity
                    DBFullPath = isodb.UsePft(Mfn, "v10")
                    DBDrive = isodb.UsePft(Mfn, "v11")
                    DBPath = isodb.UsePft(Mfn, "v12")
                    DBFile = isodb.UsePft(Mfn, "v13")
                    
                    xMfn = ""
                    
                    If FileExist(DBDrive + "\" + DBPath, DBFile + ".iso") Then
                        Set db = New ClIsisDll
                        If db.Initiate(DBDrive + "\" + DBPath, DBFile, DBFile) Then
                            xMfn = db.UsePft(MfnInfo, SearchExpr)
                        End If
                        
                        If Len(xMfn) > 0 Then
                            Set dbi = New ClPair
                            Set dbi = DBInfo.Add(DBFullPath)
                            DBList.AddItem (DBFullPath)
                            dbi.elem1 = DBFullPath
                            dbi.elem2 = isodb.UsePft(Mfn, "v2")
                            dbi.elem3 = db.UsePft(MfnInfo, InfoPFT)
                            Set dbi = Nothing
                        End If
                        
                        Set db = Nothing
                    Else
                        If isodb.RecordDel(Mfn) Then
                            If isodb.IfUpdate(Mfn, Mfn) Then
                                Set logDB = New ClMsg
                                If StrComp(.FileTree.DirNodes("Log Directory").text, .FileTree.DirNodes("Database Directory").text, vbTextCompare) = 0 Then
                                    Call logDB.InitLogDatabase(DBDrive + "\" + DBPath, DBFile + "log")
                                    logDB.DelLogDatabase
                                Else
                                    p = InStr(DBPath, "\" + .FileTree.DirNodes("Database Directory").text)
                                    If p > 0 Then
                                        Call logDB.InitLogDatabase(DBDrive + "\" + Mid(DBPath, 1, p) + .FileTree.DirNodes("Log Directory").text, .FileTree.DirNodes("Log File").text)
                                        logDB.DeleteRecord (DBFile)
                                    End If
                                End If
                                
                                Set logDB = Nothing
                            End If
                        End If
                        
                    End If
                Next
            End If
            isodb.BDClean
        End If
    End If
    End With
    
    
    
    Set isodb = Nothing

End Sub


Private Sub Class_Initialize()
    If StrComp(BV(Currbv).Flag_CfgRecInDB, "1", vbTextCompare) = 0 Then
        MfnInfo = 1
    Else
        MfnInfo = 2
    End If
    
End Sub
Function DBDelete(DB_ID() As String, DB_Count As Long, TotalCount As Long) As Boolean
    
    Dim isodb As ClIsisDll
    Dim Mfns() As Long
    Dim q As Long
    Dim i As Long
    Dim j As Long
    Dim r As Long
    Dim DBFullPath As String
    Dim DBPath As String
    Dim DBFile As String
    Dim DBDrive As String
    Dim db As ClIsisDll
    Dim logDB As ClMsg
    Dim p As Long
    
    
    Set isodb = New ClIsisDll
    With BV(Currbv)
    
    
    If isodb.Initiate(.FileTree.DirNodes("iso list database").fullpath, .FileTree.DirNodes("iso list database").text, .FileTree.DirNodes("iso list database").key) Then
        If isodb.IfCreate(.FileTree.DirNodes("iso list database").text, .FileTree.DirNodes("iso list database").key) Then
            For i = 1 To DB_Count
                q = isodb.DoSearch("ID=" + DB_ID(i), Mfns)
                For j = 1 To q
                    DBFullPath = isodb.UsePft(Mfns(j), "v10")
                    DBDrive = isodb.UsePft(Mfns(j), "v11")
                    DBPath = isodb.UsePft(Mfns(j), "v12")
                    DBFile = isodb.UsePft(Mfns(j), "v13")
                    If FileExist(DBDrive + "\" + DBPath, DBFile + ".mst") Then
                        On Error Resume Next
                        Kill DBFullPath + ".*"
                    End If
                    If isodb.RecordDel(Mfns(j)) Then
                        If isodb.IfUpdate(Mfns(j), Mfns(j)) Then
                            Set logDB = New ClMsg
                            If StrComp(.FileTree.DirNodes("Log Directory").text, .FileTree.DirNodes("Database Directory").text, vbTextCompare) = 0 Then
                                Call logDB.InitLogDatabase(DBDrive + "\" + DBPath, DBFile + "log")
                                logDB.DelLogDatabase
                            Else
                                p = InStr(DBPath, "\" + .FileTree.DirNodes("Database Directory").text)
                                If p > 0 Then
                                    Call logDB.InitLogDatabase(DBDrive + "\" + Mid(DBPath, 1, p) + .FileTree.DirNodes("Log Directory").text, .FileTree.DirNodes("Log File").text)
                                    logDB.DeleteRecord (DBFile)
                                End If
                            End If
                            
                            Set logDB = Nothing
                            r = r + 1
                        End If
                    End If
                    
                Next
            Next
        End If
    End If
    
    isodb.BDClean
    TotalCount = isodb.MfnQuantity
    
    If TotalCount = 0 Then
        For i = 1 To .WebCount
            If FileExist(.WebBasesPath(i), .WebBasesFile(i) + ".mst") Then
                Call FileCopy(.WebBasesPath(i) + "\" + .WebBasesFile(i) + ".fst", .WebBasesPath(i) + "\bkp" + .WebBasesFile(i) + ".fst")
                If DelFile(.WebBasesPath(i), .WebBasesFile(i) + ".*") Then
                    Call FileCopy(.WebBasesPath(i) + "\bkp" + .WebBasesFile(i) + ".fst", .WebBasesPath(i) + "\" + .WebBasesFile(i) + ".fst")
                End If
            End If
        Next
    Else
        If isodb.FieldContentUpdate(1, 20, "1", 1) Then
            Call isodb.IfUpdate(1, 1)
        End If
    End If
    End With
    Set isodb = Nothing
    DBDelete = (r = DB_Count)

End Function
