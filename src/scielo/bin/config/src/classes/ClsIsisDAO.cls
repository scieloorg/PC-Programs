VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClsIsisDAO"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit


Function reinvertIfNecessary(Path As String, File As String, newfst As String, log As String) As Boolean

    Dim Ret As Boolean
    Dim sfile As New ClsFile
    Dim FileName As String
    Dim xpath As String
    Dim full As String
    Dim invert As String
    
    Dim backupPath As String
    Dim backupFile As String
    Dim backupFull As String
    
    
    backupPath = App.Path
    backupFile = File
    backupFull = backupPath & "\" + backupFile
    
    full = Path + "\" + File
    
    
    If sfile.getFileContent(newfst) = sfile.getFileContent(full + ".fst") Then
        log = log & vbCrLf & "It is not necessary to reinvert."
        Ret = True
    Else
        log = log & vbCrLf & "It is necessary to reinvert."
        If copyMstAndInvertedFiles(full, backupPath, backupFile) Then
            log = log & vbCrLf & "Backup done."
            
            
            invert = "mx " + full + " fst=@" + newfst + " fullinv=" + full
            
            'Ret = executeShellScript(invert, 999999)
            If Ret Then Call FileCopy(newfst, full + ".fst")
        End If
    End If
    
   reinvertIfNecessary = Ret
End Function


Function copyMstAndInvertedFiles(srcFiles As String, destPath As String, destFileName As String) As Boolean
    
    Dim destFile As String
    
    On Error GoTo DeuErro
    destFile = destPath & "\" & destFileName
    
    Call FileCopy(srcFiles + ".mst", destFile + ".mst")
    Call FileCopy(srcFiles + ".xrf", destFile + ".xrf")
    Call FileCopy(srcFiles + ".fst", destFile + ".fst")
    Call FileCopy(srcFiles + ".cnt", destFile + ".cnt")
    Call FileCopy(srcFiles + ".ifp", destFile + ".ifp")
    Call FileCopy(srcFiles + ".l01", destFile + ".l01")
    Call FileCopy(srcFiles + ".l02", destFile + ".l02")
    Call FileCopy(srcFiles + ".n01", destFile + ".n01")
    Call FileCopy(srcFiles + ".n02", destFile + ".n02")
    
    copyMstAndInvertedFiles = FileExist(destPath, destFileName + ".mst") And _
    FileExist(destPath, destFileName + ".xrf") And _
    FileExist(destPath, destFileName + ".fst") And _
    FileExist(destPath, destFileName + ".cnt") And _
    FileExist(destPath, destFileName + ".ifp") And _
    FileExist(destPath, destFileName + ".l01") And _
    FileExist(destPath, destFileName + ".l02") And _
    FileExist(destPath, destFileName + ".n01") And _
    FileExist(destPath, destFileName + ".n02")
    Exit Function
DeuErro:
    MsgBox err.Description & " " & destFile
End Function

