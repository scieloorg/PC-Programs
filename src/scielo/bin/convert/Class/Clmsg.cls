VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClMsg"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

Public MsgFile As String
Public MsgDir As String

Private ContentLogFile() As String
Private LogLineCount As Long

Private PathLog As String
Private DBLog As String

Function InitLogDatabase(Path As String, DatabaseName As String) As Boolean
    PathLog = Path
    DBLog = DatabaseName
    LogLineCount = 0
    Erase ContentLogFile
End Function

Function WriteLogDatabase(DocId As String, PathBase As String, result As Boolean, WarningError As Boolean) As Boolean
    Dim Mfn As Long
    Dim ret As Boolean
    Dim Database As ClIsisDll
    Dim content As String
    Dim i As Long
    Dim drv As String
    Dim Path As String
    Dim dbname As String
    Dim p As Long
    
    Set Database = New ClIsisDll
    With Database
    If .Initiate(PathLog, DBLog, "Log Database") Then
        If .IfCreate(DBLog, "Log Database") Then
            Mfn = .MfnFindOne(DocId)
            
            p = InStr(PathBase, ":")
            If p > 0 Then
                drv = Mid(PathBase, 1, p)
                dbname = Mid(PathBase, p + 1)
                p = InStr(dbname, "\")
                While p > 0
                    Path = Path + Mid(dbname, 1, p)
                    dbname = Mid(dbname, p + 1)
                    p = InStr(dbname, "\")
                Wend
            End If
            content = content + .TagContents(drv, 500)
            content = content + .TagContents(Path, 501)
            content = content + .TagContents(dbname, 502)
            content = content + .TagContents(DocId, 1)
            content = content + .TagContents(GetDateISO(Date), 65)
            If result Then
                content = content + .TagContents("Success", 3)
            Else
                content = content + .TagContents("Failure", 3)
            End If
            If WarningError Then
                content = content + .TagContents("F", 5)
            Else
                content = content + .TagContents("S", 5)
            End If
            
            For i = 1 To LogLineCount
                content = content + .TagContents(ContentLogFile(i), 2)
            Next
            Erase ContentLogFile
            LogLineCount = 0
            
            If Mfn = 0 Then
                Mfn = .RecordSave(content)
                ret = (Mfn > 0)
            ElseIf Mfn > 0 Then
                ret = .RecordUpdate(Mfn, content)
            End If
            If Mfn > 0 Then Call .IfUpdate(Mfn, Mfn)
        End If
    End If
    End With
    Set Database = Nothing
    WriteLogDatabase = ret
End Function

Function ViewLogDatabase(DocId As String) As String
    Dim Mfn As Long
    Dim ret As String
    Dim Database As ClIsisDll
    Dim content() As String
    Dim q As Long
    Dim i As Long
    
    Set Database = New ClIsisDll
    If Database.Initiate(PathLog, DBLog, "Log Database") Then
        If Database.IfCreate(DBLog, "Log Database") Then
            'If database.MfnQuantity > 0 Then Call database.IfUpdate(1, database.MfnQuantity)
            Mfn = Database.MfnFindOne(DocId)
            If Mfn > 0 Then
                q = Database.FieldContentGet(Mfn, 2, content)
                For i = 1 To q
                    ret = ret + content(i) + vbCrLf
                Next
            End If
        End If
    End If
    Set Database = Nothing
    ViewLogDatabase = ret
End Function

Function GetDocLoadStatus(Success() As String, QSuccess As Long, Failure() As String, QFailure As Long, ParserFail() As Boolean) As Long
    Dim Database As ClIsisDll
    Dim q As Long
    Dim content() As String
    Dim status As String
    Dim name As String
    Dim parserOK As String
    Dim p As Long
    Dim p1 As Long
    Dim i As Long
    
    Erase Success
    Erase Failure
    Erase ParserFail
    
    QSuccess = 0
    QFailure = 0
    
    Set Database = New ClIsisDll
    If Database.Initiate(PathLog, DBLog, "Log Database") Then
        If Database.IfCreate(DBLog, "Log Database") Then
            If Database.MfnQuantity > 0 Then
                'q = Database.GetTerms(content, "v3*0.1|:|,v1|::|,v5")
                q = Database.GetTerms(content, "v3*0.1|:|,v1|::|,v5")
                For i = 1 To q
                    p = InStr(content(i), ":")
                    p1 = InStr(content(i), "::")
                    
                    If p > 0 Then
                        status = Mid(content(i), 1, p - 1)
                        name = Mid(content(i), p + 1, p1 - p - 1)
                        parserOK = Mid(content(i), p1 + 2)
                        If status = "S" Then
                            QSuccess = QSuccess + 1
                            ReDim Preserve Success(QSuccess)
                            ReDim Preserve ParserFail(QSuccess)
                            Success(QSuccess) = name
                            ParserFail(QSuccess) = (parserOK = "F")
                        ElseIf status = "F" Then
                            QFailure = QFailure + 1
                            ReDim Preserve Failure(QFailure)
                            Failure(QFailure) = name
                        Else
                            MsgBox name + InterfaceLabels("MsgLogDatabaseStatusMissing").elem2
                        End If
                    End If
                Next
            End If
        End If
    End If
    Set Database = Nothing
    GetDocLoadStatus = q
End Function

'-----------------------------------------------------------------------
'WriteLogFileLine - escreve os passos do processamento em arquivo
'msg    - a mensagem a ser gravada no arquivo
'-----------------------------------------------------------------------
Private Sub WriteLogFileLine(file As String, ByVal Msg As String)
    Dim fnLog As Long
        
    fnLog = FreeFile(1)
    Open file For Append As fnLog
    Print #fnLog, Msg
    
    LogLineCount = LogLineCount + 1
    ReDim Preserve ContentLogFile(LogLineCount)
    ContentLogFile(LogLineCount) = Msg
    Close fnLog
End Sub

Function DelLogDatabase() As Boolean
    Dim ret As Boolean
    Dim Database As ClIsisDll
    
    Set Database = New ClIsisDll
    If Database.Initiate(PathLog, DBLog, "Log Database") Then
        ret = Database.BDDel
    End If
    Set Database = Nothing
    DelLogDatabase = ret
End Function

'-----------------------------------------------------------------------
'MsgInvalidPath - mensagem de caminho inválido
'Label  - identificação do caminho
'Path    - caminho
'-----------------------------------------------------------------------
Sub MsgInvalidPath(Label As String, Path As String)
    If Len(Label) > 0 Then
        MsgBox (Label + InterfaceLabels("MsgNotFoundpath").elem2 + Path)
    Else
        MsgBox (Mid(InterfaceLabels("MsgNotFoundpath").elem2, 3) + Path)
    End If
End Sub

'-----------------------------------------------------------------------
'GiveRunInformation - escreve os passos do processamento em arquivo, em msgbox e no rodapé do form
'Msg - a mensagem a ser gravada no arquivo
'ShowMsgbox - se a mensagem deve ser também mostrada ou não em msgbox
'ShowLabel  - se a mensagem deve ser também mostrada ou não em label
'-----------------------------------------------------------------------
Sub GiveRunInformation(Msg As String, Optional ShowMsgbox As Boolean, Optional ShowLabel As Boolean, Optional WriteLog As Boolean = True)
    Dim file As String
    
    If Len(MsgFile) > 0 Then
        If Len(MsgDir) > 0 Then
            file = MsgDir + PathSep + MsgFile
        Else
            file = MsgFile
        End If
    Else
        file = "warnings.txt"
    End If
    
    If Len(Msg) > 0 Then
        If WriteLog Then Call WriteLogFileLine(file, CStr(Date) + Chr(32) + CStr(Time) + vbTab + Msg)
        If ShowMsgbox Then MsgBox Msg
    Else
        Call WriteLogFileLine(file, "")
    End If
    If ShowLabel Then ShowMsgInForm (Msg)
End Sub

'-----------------------------------------------------------------------
'ExitProgram  - sai do programa
'-----------------------------------------------------------------------
Function ExitProgram() As Boolean
    ExitProgram = (MsgBox(InterfaceLabels("MsgExit").elem2, vbOK) = vbOK)
End Function


Function DeleteRecord(dbname As String) As Boolean
    Dim Mfn As Long
    Dim ret As Boolean
    Dim Database As ClIsisDll
    Dim content() As String
    Dim q As Long
    Dim i As Long
    Dim DocId As String
    
    Set Database = New ClIsisDll
    If Database.Initiate(PathLog, DBLog, "Log Database") Then
        If Database.IfCreate(DBLog, "Log Database") Then
            'If database.MfnQuantity > 0 Then Call database.IfUpdate(1, database.MfnQuantity)
            DocId = dbname + ".htm"
            Mfn = Database.MfnFindOne(DocId)
            If Mfn = 0 Then
                DocId = dbname + ".html"
                Mfn = Database.MfnFindOne(DocId)
            End If
            
            If Mfn > 0 Then
                If Database.RecordDel(Mfn) Then
                    If Database.IfUpdate(Mfn, Mfn) Then
                        ret = True
                    End If
                End If
            End If
        End If
    End If
    Set Database = Nothing
    
    Set Database = New ClIsisDll
    If Database.Initiate(PathLog, DBLog, "Log Database") Then
        If Database.IfCreate(DBLog, "Log Database") Then
            Database.BDClean
        End If
    End If
    Set Database = Nothing
    DeleteRecord = ret
End Function

Private Sub Class_Terminate()
    Erase ContentLogFile
End Sub
