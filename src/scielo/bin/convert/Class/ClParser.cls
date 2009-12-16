VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClParser"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit


Const MaxStrLen = 60000
Const MaxMsgLen = 999

Private mvarErrQtdMax As Long 'local copy

Private MarkupErrors As String

'-----------------------------------------------------------------------
'Parse   - analisa o documento e gera uma base de dados temporária
'DocPath  - caminho do arquivo do documento
'DocName  - arquivo do documento
'DTDCurrent -   input   - current DTD
'Return the result of the parser in format of database
'-----------------------------------------------------------------------
Function Parse(DocPath As String, DocName As String, DTDCurrent As ClDTD, OutputFile As String) As Boolean
    Dim QtdErros As Long
    
    Parse = ParserDLL(DocPath, DocName, DTDCurrent, QtdErros, OutputFile)
    If QtdErros = 0 Then Call DelFile(DocPath, DocName)
    
End Function

'-----------------------------------------------------------------------
'ParserDLL  -   use the paser dll
'DocMarkupPath  - caminho do arquivo do documento
'DocMarkupFile  - arquivo do documento
'DTDCurrent - current DTD
'Return - <True> - no error found, <False> - otherwise
'-----------------------------------------------------------------------
Private Function ParserDLL(DocMarkupPath As String, DocMarkupFile As String, DTDCurrent As ClDTD, QtdErros As Long, OutputFile As String) As Boolean
    Dim DocMarkupFullPath As String
    Dim MarkupErrorsQtd As Long
    Dim ErrorCode As Long
    Dim MsgLen As Long
    Dim ErrorMsg As String * MaxMsgLen
    Dim MaxMarkupErrors As Long
    Dim MarkupErrorsMsgsLen As Long
    Dim MarkupErrorsMsgs As String * MaxStrLen
    Dim ret As Boolean
    'Dim ParserResult As ClIsisDll

    'Set ParserResult = new ClIsisDll
    
    MaxMarkupErrors = ErrQtdMax
    MsgLen = MaxMsgLen
    MarkupErrorsMsgsLen = MaxStrLen
    MarkupErrorsMsgs = ""
    MarkupErrors = ""
    QtdErros = 0
    
    DocMarkupFullPath = DocMarkupPath + PathSep + DocMarkupFile
    ErrorCode = SGMLDocPrepareForParsing(DocMarkupFullPath, BV(Currbv).FileTree.DirNodes("SGML Parser Program Directory").fullpath + PathSep + DTDCurrent.SGMLDecl, DTDCurrent.name, BV(Currbv).FileTree.DirNodes("SGML Parser Program Directory").fullpath + PathSep + DTDCurrent.filename)
    If ErrorCode = 0 Then
        MarkupErrorsQtd = SGMLDocParse(DocMarkupFullPath, MaxMarkupErrors, MsgLen, MarkupErrorsMsgsLen, MarkupErrorsMsgs)
        If MarkupErrorsQtd > 0 Then
            QtdErros = QtdErros + MarkupErrorsQtd
            MarkupErrors = Left(MarkupErrorsMsgs, MarkupErrorsMsgsLen)
        End If
        OutputFile = GetNewTmpFileName(App.Path)
        ErrorCode = SGMLDocParserInfoFile(DocMarkupFullPath, BV(Currbv).BVPath + PathSep + DTDCurrent.CTableFile, App.Path + PathSep + OutputFile)
        If ErrorCode = 0 Then
            'Set ParserResult = GenerateParserDB(OutputFile)
            OutputFile = App.Path + PathSep + OutputFile
            ret = GenerateParserDB(OutputFile)
        Else
            Call SGMLDocGetErrorMsg(ErrorCode, ErrorMsg, MsgLen)
            MsgBox Left(ErrorMsg, MsgLen)
        End If
        'Call DelTmpFile(App.Path, OutputFile)
    Else
        Call SGMLDocGetErrorMsg(ErrorCode, ErrorMsg, MsgLen)
        MsgBox Left(ErrorMsg, MsgLen)
    End If
            
    ParserDLL = ret
End Function

'-----------------------------------------------------------------------
'GenerateParserDB   - gera uma base de dados dos elementos encontrados no documento
'ParserOutputFile   - parser output file name
'
'       (See technical documentation)
'
'-----------------------------------------------------------------------
Private Function GenerateParserDB(ParserOutputFile As String) As Boolean
    Dim fn As Long
    Dim i As Long
    Dim pA As Long
    Dim p2 As Long
    Dim fi As Long
    Dim fj As Long
    Dim TAG1 As String
    Dim TAG2 As String
    Dim s As String
    Dim a As String
    Dim P As TpPosition
    Dim ParserOutput As New ClTxt
    Dim ret As Boolean
    
    fn = FreeFile(1)
    Open ParserOutputFile For Input As fn
    While Not EOF(fn)
        Line Input #fn, s
        ParserOutput.AddLines s
    Wend
    Close fn
    Kill ParserOutputFile
    
    If ParserOutput.Qtd = 0 Then
        ret = False
        Call Msg.GiveRunInformation(InterfaceLabels("NoParserOutput").elem2)
    Else
        ret = True
        
        ParserOutputFile = ParserOutputFile + ".txt"
        Open ParserOutputFile For Output As fn
        
        Call ParserOutput.GetEnd(fi, fj)
        While (i < ParserOutput.Qtd)
            i = i + 1
            s = ParserOutput.GetLine(i)
            'Find the start tag
            If InStr(s, "<") = 1 Then
                p2 = InStr(2, s, ">", vbBinaryCompare)
                If p2 > 0 Then
                    TAG1 = Mid(s, 2, p2 - 2)
                    If IsNumber(TAG1) Then
                        TAG2 = "</" + TAG1 + ">"
                        'Find the end tag
                        Call ParserOutput.InString(i, 1, fi, fj, TAG2, P.i, P.j, vbBinaryCompare)
                        If P.j > 0 Then
                            'End Tag was found
                            s = ParserOutput.GetSubstrRange(i, 1, P.i, P.j - 1)
                            pA = InStr(s, "^a")
                            If pA > 0 Then
                                'Get the content and the scope
                                a = LCase(Mid(s, pA + Len("^a")))
                                s = Mid(s, Len(TAG2), pA - Len(TAG2))
                                
                                's = CloseOpenedTags(s)
                                If Len(s) > 0 Then
                                
                                    s = CvtTables("Conversion sgml to windows 2").Convert(s)
                                    s = RmNewLineInStr(s)
                                    s = StandardFontFaceSymbol(s)
                                    s = ReplaceString(s, CONST_SUBFIELDINDICATOR, "&#094;", vbBinaryCompare)
                                    s = ReplaceString(s, "  ", " ", vbBinaryCompare)
                                    s = Entities.myEnt2entNum(s)
                                    Print #fn, TAG1
                                    Print #fn, a
                                    Print #fn, s
                                    Print #fn,
                                    
                                End If
                                i = P.i
                            Else
                                Msg.GiveRunInformation (InterfaceLabels("MsgParserResultProblemNoScope").elem2)
                                ret = False
                            End If
                        Else
                            Msg.GiveRunInformation (InterfaceLabels("MsgParserResultProblemNoEndofTag").elem2 + TAG1)
                            ret = False
                        End If
                    Else
                        Msg.GiveRunInformation (InterfaceLabels("MsgParserResultProblemNoStartofTag").elem2 + TAG1)
                        ret = False
                    End If
                Else
                    Msg.GiveRunInformation (InterfaceLabels("MsgParserResultProblemNoTag").elem2)
                    ret = False
                End If
            Else
                Msg.GiveRunInformation (InterfaceLabels("MsgParserResultProblemFilenotOK").elem2)
                ret = False
            End If
        Wend
        Close fn
    End If
    GenerateParserDB = ret
End Function

'-----------------------------------------------------------------------
'PrintParserErrors  - escreve em arquivo os erros do parser
'Path   - caminho do arquivo do documento
'File   - arquivo do documento
'-----------------------------------------------------------------------
Function PrintParserErrors(Path As String, File As String) As Long
    Dim fn As Long
    Dim P As Long
    Dim p1 As Long
    Dim aux As String
    Dim ErrorCount As Long
    
    P = InStr(MarkupErrors, vbLf)
    While P > 0
        ErrorCount = ErrorCount + 1
        aux = Mid(MarkupErrors, 1, P - 1)
        p1 = InStr(aux, ":")
        aux = Mid(aux, p1 + 1)
        p1 = InStr(aux, ":")
        aux = Mid(aux, p1 + 1)
        Msg.GiveRunInformation (InterfaceLabels("MsgMarkupErrors").elem2 + aux)
        
        MarkupErrors = Mid(MarkupErrors, P + 1)
        P = InStr(MarkupErrors, vbLf)
    Wend
    If Len(MarkupErrors) > 0 Then
        Msg.GiveRunInformation InterfaceLabels("MsgMarkupErrors").elem2 + aux
    End If
    MarkupErrors = ""
    PrintParserErrors = ErrorCount
End Function


Public Property Let ErrQtdMax(ByVal vData As Long)
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.ErrQtdMax = 5
    
    mvarErrQtdMax = MaxStrLen / MaxMsgLen
    If vData < mvarErrQtdMax Then mvarErrQtdMax = vData
End Property

Public Property Get ErrQtdMax() As Long
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: 'Debug.Print X.ErrQtdMax
    If mvarErrQtdMax = 0 Then
        ErrQtdMax = MaxStrLen / MaxMsgLen
    Else
        ErrQtdMax = mvarErrQtdMax
    End If
End Property

