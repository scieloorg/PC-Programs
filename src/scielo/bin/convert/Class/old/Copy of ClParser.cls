VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "ClParser"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

Const TagInicialFech = "]"
Const TagInicialAbre = "["
Const TagFinalAbre = "[/"
Const TagFinalFech = "]"

Const MaxStrLen = 60000
Const MaxMsgLen = 999

Private mvarErrQtdMax As Long 'local copy
Private QtdErros As Long
Private PreparationErrors As String
Private MarkupErrors As String

Private CurrDTD As String
Private DocSci As String
Private ExistDocSci As Boolean

Private Text As ClTxt

Private mvarRegistro As ClIsisDll 'local copy
Private mvarOutputFile As String 'local copy
Private mvarPath As String 'local copy
Private mvarCTabPath As String 'local copy
Private SGMLPath As String

Public Property Let CTabPath(ByVal vData As String)
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.CTabPath = 5
    mvarCTabPath = vData
End Property

Public Property Get CTabPath() As String
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: Debug.Print X.CTabPath
    CTabPath = mvarCTabPath
End Property

Public Property Let Path(ByVal vData As String)
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.Path = 5
    mvarPath = vData
End Property

Public Property Get Path() As String
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: Debug.Print X.Path
    Path = mvarPath
End Property

Function BeforeParsing(DocumentoPath As String, DocumentoNome As String) As Boolean
    Dim Fim As Boolean
    
    ExistDocSci = False
    
    Call Msg.GiveRunInformation(DocumentoNome + ": Preparing the document...", , True)
    DocSci = GetTmpDoc(DocumentoPath, DocumentoNome, "sci")
    
    Call ReadFile(DocumentoPath, DocSci)
    
    Call Msg.GiveRunInformation(DocumentoNome + ": Recognizing the document type...", , True)
    If RecognizeDoc(DocumentoPath, DocSci) Then
        SGMLPath = DirPeriodicos + PathSep + Paths("SGMLDecl").DirName
        CTabPath = DirPeriodicos + PathSep + Paths("CTabPath").DirName
        With DTDCol(CurrDTD)
            If Not .IsLoaded Then
                Set .TabConv = New ClTabConv
                .IsLoaded = True
                Fim = .TabConv.Inicia(CTabPath, .ProcTableFile, .CTableFile, .IdTpRegTableFile)
            Else
                Fim = True
            End If
            Set ConvTables = New ClTabConv
            Set ConvTables = .TabConv
        End With
        If Fim Then
            ExistDocSci = True
        End If
    Else
        PreparationErrors = "Document Type was not recognized."
    End If
    
    BeforeParsing = Fim
End Function

Function GetConfigRecord(DocumentoPath As String, DocumentoNome As String, ConfigRecord As ClIsisDll) As Boolean
    Dim Fim As Boolean
    Dim fn As Long
    Dim fn2 As Long
    Dim CTableFile As String
    Dim Line As String
    Dim Indexes() As Long
    Dim q As Long
    Dim i As Long
    
    If Not ExistDocSci Then Call BeforeParsing(DocumentoPath, DocumentoNome)
    If ExistDocSci Then
        'Call Msg.GiveRunInformation(DocumentoNome + ": Analyzing the document...", , True)
        fn = FreeFile(1)
        fn2 = fn + 1
        
        CTableFile = DTDCol(CurrDTD).CTableFile + "0"
        Open CTabPath + PathSep + CTableFile For Output As fn2
        Open CTabPath + PathSep + DTDCol(CurrDTD).ProcTableFile For Input As fn
        
        While Not EOF(fn)
            Line Input #fn, Line
            If (InStr(Line, "h") > 0) Or (InStr(Line, "o") > 0) Then
                Line = Mid(Line, InStr(Line, ",") + 1)
                Line = Mid(Line, 1, InStr(Line, ",") - 1)
                q = DTDCol(CurrDTD).TabConv.tabdtd2bd.Find(Line, "intermedfield", Indexes, vbTextCompare)
                Debug.Print DTDCol(CurrDTD).TabConv.tabdtd2bd.Colunas.Count
                If q > 0 Then
                    Line = ""
                    For i = 1 To 3
                        Line = Line + ";" + DTDCol(CurrDTD).TabConv.tabdtd2bd.Elem(Indexes(q), i)
                    Next
                    Print #fn2, Mid(Line, 2)
                End If
            End If
        Wend
        Close fn, fn2
        
        Fim = ParserDLL(DocumentoPath, DocSci, CTableFile, ConfigRecord)
        Call DelFile(CTabPath, CTableFile)
    End If
    GetConfigRecord = Fim
End Function

'-----------------------------------------------------------------------
'Parse   - analisa o documento e gera uma base de dados temporária
'DocumentoPath  - caminho do arquivo do documento
'DocumentoNome  - arquivo do documento
'-----------------------------------------------------------------------
Public Function Parse(DocumentoPath As String, DocumentoNome As String) As Boolean
    Dim Fim As Boolean
     
    If Not ExistDocSci Then Call BeforeParsing(DocumentoPath, DocumentoNome)
    If ExistDocSci Then
        Call Msg.GiveRunInformation(DocumentoNome + ": Analyzing the document...", , True)
        Fim = ParserDLL(DocumentoPath, DocSci, DTDCol(CurrDTD).CTableFile, mvarRegistro)
    End If
    
    If QtdErros = 0 Then Call DelFile(DocumentoPath, DocSci)
    Parse = Fim
End Function
'-----------------------------------------------------------------------
'Parse2   - analisa o documento e gera uma base de dados temporária
'DocumentoPath  - caminho do arquivo do documento
'DocumentoNome  - arquivo do documento
'-----------------------------------------------------------------------
Public Function Parse2(DocumentoPath As String, DocumentoNome As String) As Boolean
    Dim DocTmpFile As String
    Dim i As Long
    Dim Fim As Boolean
    
    Call Msg.GiveRunInformation(DocumentoNome + ": Preparing the document...", , True)
    
    DocTmpFile = GetTmpDoc(DocumentoPath, DocumentoNome, "sci")
    Call ReadFile(DocumentoPath, DocTmpFile)
    
    Call Msg.GiveRunInformation(DocumentoNome + ": Recognizing the document type...", , True)
    Fim = PlaceInitialTag(DocumentoPath, DocTmpFile)
    
    i = 0
    While (i < DTDCol.Count) And (Not Fim)
        i = i + 1
        CurrDTD = DTDCol(i).Name + " " + DTDCol(i).Version
        Fim = PlaceInitialTag(DocumentoPath, DocTmpFile)
    Wend
    SGMLPath = DirPeriodicos + PathSep + Paths("SGMLDecl").DirName
    CTabPath = DirPeriodicos + PathSep + Paths("CTabPath").DirName
    If i > 0 Then
        With DTDCol(i)
        If Not .IsLoaded Then
            Set .TabConv = New ClTabConv
            .IsLoaded = True
            Fim = .TabConv.Inicia(CTabPath, .ProcTableFile, .CTableFile, .IdTpRegTableFile)
        End If
        Set ConvTables = New ClTabConv
        Set ConvTables = .TabConv
        End With
    End If
    
    If Fim Then
        Call Msg.GiveRunInformation(DocumentoNome + ": Analyzing the document...", , True)
        Fim = ParserDLL(DocumentoPath, DocTmpFile)
    Else
        PreparationErrors = "Document Type was not recognized"
    End If
    
    If QtdErros = 0 Then Call DelFile(DocumentoPath, DocTmpFile)
    Parse2 = Fim
End Function
'-----------------------------------------------------------------------
'ParserDLL  -   aplica a DLL parser
'DocMarkupPath  - caminho do arquivo do documento
'DocMarkupFile  - arquivo do documento
'-----------------------------------------------------------------------
Public Function ParserDLL(DocMarkupPath As String, DocMarkupFile As String, CTableFile As String, Record As ClIsisDll) As Boolean
    Dim DocMarkupFullPath As String
    Dim NoMarkupErrorsFound As Boolean
    Dim MarkupErrorsQtd As Long
    Dim ErrorCode As Long
    Dim MsgLen As Long
    Dim ErrorMsg As String * MaxMsgLen
    Dim MaxMarkupErrors As Long
    Dim MarkupErrorsMsgsLen As Long
    Dim MarkupErrorsMsgs As String * MaxStrLen
    
    MaxMarkupErrors = ErrQtdMax
    MsgLen = MaxMsgLen
    MarkupErrorsMsgsLen = MaxStrLen
    MarkupErrorsMsgs = ""
    
    QtdErros = 0
    DocMarkupFullPath = DocMarkupPath + PathSep + DocMarkupFile
    ErrorCode = SGMLDocPrepareForParsing(DocMarkupFullPath, SGMLPath + PathSep + Paths("SGMLDecl").FileName, DTDCol(CurrDTD).Name, SGMLPath + PathSep + DTDCol(CurrDTD).FileName)
    If ErrorCode = 0 Then
        MarkupErrorsQtd = SGMLDocParse(DocMarkupFullPath, MaxMarkupErrors, MsgLen, MarkupErrorsMsgsLen, MarkupErrorsMsgs)
        
        If MarkupErrorsQtd > 0 Then
            QtdErros = QtdErros + MarkupErrorsQtd
            MarkupErrors = Left(MarkupErrorsMsgs, MarkupErrorsMsgsLen)
        End If
        OutputFile = GetNewTmpFileName(CTabPath)
        ErrorCode = SGMLDocParserInfoFile(DocMarkupFullPath, CTabPath + PathSep + CTableFile, CTabPath + PathSep + OutputFile)
        If ErrorCode = 0 Then
            NoMarkupErrorsFound = GenerateParserDB(Record)
        Else
            Call SGMLDocGetErrorMsg(ErrorCode, ErrorMsg, MsgLen)
            MsgBox Left(ErrorMsg, MsgLen)
        End If
        Call DelTmpFile(CTabPath, OutputFile)
    Else
        Call SGMLDocGetErrorMsg(ErrorCode, ErrorMsg, MsgLen)
        MsgBox Left(ErrorMsg, MsgLen)
    End If
    
    ParserDLL = NoMarkupErrorsFound
End Function

'-----------------------------------------------------------------------
'GetTmpDoc    - faz uma cópia temporária do documento
'DocumentoPath  - caminho do arquivo do documento
'DocumentoNome  - arquivo do documento
'-----------------------------------------------------------------------
Public Function GetTmpDoc(DocumentoPath As String, DocumentoNome As String, Extensao As String) As String
    Dim DocTmpFile As String
    Dim DocTmpFullPath As String
    Dim P As Long
    
    'Cria uma cópia do documento
    P = InStr(DocumentoNome, ".")
    DocTmpFile = Mid(DocumentoNome, 1, P) + Extensao
    DocTmpFullPath = DocumentoPath + PathSep + DocTmpFile
    FileCopy DocumentoPath + PathSep + DocumentoNome, DocTmpFullPath
    
    GetTmpDoc = DocTmpFile
End Function

'-----------------------------------------------------------------------
'ReadFile   - le o arquivo
'PathDoc    - caminho do arquivo do documento
'File       - arquivo do documento
'-----------------------------------------------------------------------
Private Sub ReadFile(PathDoc As String, file As String)
    Dim fn As Long
    Dim aux As String
    
    Set Text = New ClTxt
    fn = FreeFile(1)
    Open PathDoc + PathSep + file For Input As fn
    Do Until EOF(fn)
        Line Input #fn, aux
        Text.AddLines ConvertHTML2ASCII(aux)
    Loop
    Close fn
    
End Sub

'-----------------------------------------------------------------------
'RecognizeDoc    - coloca a tag inicial no local correto no arquivo
'PathDoc    - caminho do arquivo do documento
'File       - arquivo do documento
'-----------------------------------------------------------------------
Private Function RecognizeDoc(PathDoc As String, file As String) As Boolean
    Dim P1 As TpPosicao
    Dim P2 As TpPosicao
    Dim Inicio As TpPosicao
    Dim final As TpPosicao
    Dim Tag As String
    Dim ret As Boolean
    Dim fn As Long
    Dim i As Long
    Dim aux As String
    Dim acabou As Boolean
    Dim TagFinal As String
    Dim FimTxt As TpPosicao
        
    Dim P As TpPosicao
       
        
    With Text
    Inicio.i = 1
    Inicio.j = 1
    Call .GetEnd(final.i, final.j)
    If .GetLen(Inicio.i, Inicio.j, final.i, final.j) > 0 Then
        Call .InString(Inicio.i, Inicio.j, final.i, final.j, "<body", P.i, P.j, 1)
        If P.j > 0 Then
            Call .InString(P.i, P.j, final.i, final.j, ">", Inicio.i, Inicio.j, 1)
            Call .ForwardPosition(Inicio.i, Inicio.j, 1)
        End If
    End If
    
    
    If .GetLen(Inicio.i, Inicio.j, final.i, final.j) > 0 Then
        While (Not ret) And (Not acabou)
            ret = FindInitialTag(Inicio, final, P1, P2, Tag)
            acabou = (final.i < Inicio.i) Or (final.i = Inicio.i) And (Inicio.j > final.j)
        Wend
    
        If ret Then
            TagFinal = TagFinalAbre + DTDCol(CurrDTD).Name + TagFinalFech
            Call Text.InString(P2.i, P2.j, final.i, final.j, TagFinal, FimTxt.i, FimTxt.j)
            Call Text.ForwardPosition(FimTxt.i, FimTxt.j, Len(TagFinal) - 1)
                      
            fn = FreeFile(1)
            Open PathDoc + PathSep + file For Output As fn
            Print #fn, Tag
            
            aux = Mid(Text.GetLine(P1.i), 1, P1.j - 1)
            aux = aux + Mid(Text.GetLine(P2.i), P2.j + 1)
            If Len(aux) > 0 Then Print #fn, aux
            
            i = P2.i
            While i < (FimTxt.i - 1)
                i = i + 1
                aux = Text.GetLine(i)
                Print #fn, aux
            Wend
            aux = Mid(Text.GetLine(FimTxt.i), 1, FimTxt.j)
            Print #fn, aux
            Close fn
        End If
    End If
    End With
    RecognizeDoc = ret
End Function

'-----------------------------------------------------------------------
'GenerateParserDB   - gera uma base de dados dos elementos encontrados no documento
'-----------------------------------------------------------------------
Private Function GenerateParserDB(Record As ClIsisDll) As Boolean
    Dim fn As Long
    Dim Texto As New ClTxt
    Dim i As Long
    Dim Tag As String
    Dim P As TpPosicao
    Dim s As String
    Dim ret As Boolean
    Dim P1 As Long
    Dim P2 As Long
    Dim fi As Long
    Dim fj As Long
    Dim Check As Long
    
    Set Record = New ClIsisDll
    If Record.Inicia(CTabPath, OutputFile, "Record generated by parser.", True) Then
        fn = FreeFile(1)
        Open CTabPath + PathSep + OutputFile For Input As fn
        While Not EOF(fn)
            Line Input #fn, s
            Texto.AddLines s
        Wend
        Close
        
        ret = True
        Call Texto.GetEnd(fi, fj)
        While (i < Texto.Qtd)
            i = i + 1
            s = Texto.GetLine(i)
            P1 = InStr(s, "<")
            P2 = InStr(s, ">")
            
            If (P1 = 1) And (P1 < P2) Then
                Tag = Mid(s, 2, P2 - 2)
                
                If DTDCol(CurrDTD).TabConv.IsFieldTag(Tag) Then
                    Tag = "</" + Tag + ">"
                    Call Texto.InString(i, 1, fi, fj, Tag, P.i, P.j, 1)
                    If P.j > 0 Then
                        s = Texto.GetSubstrRange(i, 1, P.i, P.j + Len(Tag) - 1)
                        Check = Check + 1
                        If Record.RecordSave(s) = 0 Then Msg.GiveRunInformation ("Failure writing database generated by parser: " + s)
                        i = P.i
                    End If
                End If
            End If
        Wend
        ret = (Check = Record.MfnQuantity)
    End If
    If Not ret Then Call Msg.GiveRunInformation("Invalid result generated by parser.", True)
    GenerateParserDB = ret
End Function

'-----------------------------------------------------------------------
'GetContents   - gera uma base de dados dos elementos encontrados no documento
'-----------------------------------------------------------------------
Private Function GetContents(Contents() As String) As Long
    Dim fn As Long
    Dim Texto As New ClTxt
    Dim i As Long
    Dim Tag As String
    Dim P As TpPosicao
    Dim s As String
    Dim P1 As Long
    Dim P2 As Long
    Dim fi As Long
    Dim fj As Long
    Dim ret As Long
    
        fn = FreeFile(1)
        Open CTabPath + PathSep + OutputFile For Input As fn
        While Not EOF(fn)
            Line Input #fn, s
            Texto.AddLines s
        Wend
        Close
        
        Call Texto.GetEnd(fi, fj)
        While (i < Texto.Qtd)
            i = i + 1
            s = Texto.GetLine(i)
            P1 = InStr(s, "<")
            P2 = InStr(s, ">")
            
            If (P1 = 1) And (P1 < P2) Then
                Tag = Mid(s, 2, P2 - 2)
                
                If DTDCol(CurrDTD).TabConv.IsFieldTag(Tag) Then
                    Tag = "</" + Tag + ">"
                    Call Texto.InString(i, 1, fi, fj, Tag, P.i, P.j, 1)
                    If P.j > 0 Then
                        s = Texto.GetSubstrRange(i, 1, P.i, P.j + Len(Tag) - 1)
                        ret = ret + 1
                        ReDim Preserve Contents(ret)
                        Contents(ret) = s
                        i = P.i
                    End If
                End If
            End If
        Wend

    If ret = 0 Then Call Msg.GiveRunInformation("Invalid result generated by parser.", True)
    GetContents = ret
End Function

'-----------------------------------------------------------------------
'PrintParserErrors  - escreve em arquivo os erros do parser
'Path   - caminho do arquivo do documento
'File   - arquivo do documento
'-----------------------------------------------------------------------
Sub PrintParserErrors(Path As String, file As String)
    Dim fn As Long
    Dim P As Long
    Dim P1 As Long
    Dim aux As String
    Dim aux1 As String
    
    fn = FreeFile(1)
    Open Path + PathSep + file For Append As #fn
    
    If Len(PreparationErrors) > 0 Then
        Print #fn, " Preparation Errors: " + PreparationErrors
        PreparationErrors = ""
    End If
    
    P = InStr(MarkupErrors, Chr(10))
    While P > 0
        aux = Mid(MarkupErrors, 1, P - 1)
        P1 = InStr(aux, ":")
        aux = Mid(aux, P1 + 1)
        P1 = InStr(aux, ":")
        aux = Mid(aux, P1 + 1)
        Print #fn, " Markup Errors: " + aux
        MarkupErrors = Mid(MarkupErrors, P + 1)
        P = InStr(MarkupErrors, Chr(10))
    Wend
    If Len(MarkupErrors) > 0 Then Print #fn, MarkupErrors
    MarkupErrors = ""
    Close fn
    
End Sub

'-----------------------------------------------------------------------
'FindInitialTag - procura a tag inicial
'LimInf - limite inferior
'LimSup - limite superior
'Tag    - tag inicial
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Private Function FindInitialTag(LimInf As TpPosicao, LimSup As TpPosicao, ini As TpPosicao, Fim As TpPosicao, Tag As String) As Boolean
    Dim iAbre As Long
    Dim jAbre As Long
    Dim iFech As Long
    Dim jFech As Long
    Dim achou As Boolean
    Dim P As Long
    Dim Version As String
    Dim Name As String
    
    With Text
    While .ExisteStr(LimInf.i, LimInf.j, LimSup.i, LimSup.j) And (Not achou)
        Call .InString(LimInf.i, LimInf.j, LimSup.i, LimSup.j, TagInicialAbre, iAbre, jAbre)
        Call .InString(LimInf.i, LimInf.j, LimSup.i, LimSup.j, TagInicialFech, iFech, jFech)
        Tag = RmHTMLTotal(.GetSubstrRange(iAbre, jAbre, iFech, jFech, SepLinha))
        If Not ExisteVisibleChars(Tag) Then
            'Nenhum tag encontrado
            If (jAbre = 0) Or (jFech = 0) Then
                LimInf = LimSup
                Call .ForwardPosition(LimInf.i, LimInf.j, 1)
            Else 'foi encontrado ] antes de [
                LimInf.i = iAbre
                LimInf.j = jAbre
            End If
        Else
            'Suposto tag encontrado
            If InStr(Mid(Tag, 2), TagInicialAbre) > 0 Then
                achou = False
            Else
                
                P = InStr(Tag, "version=")
                If P > 0 Then
                    
                    Version = Mid(Tag, P + Len("version="))
                    P = InStr(Version, " ")
                    If P > 0 Then
                        Version = Mid(Version, 1, P - 1)
                    Else
                        P = InStr(Version, "]")
                        If P > 0 Then
                            Version = Mid(Version, 1, P - 1)
                        Else
                            Version = ""
                        End If
                    End If
                    
                    P = InStr(Tag, " ")
                    If P > 0 Then Name = Mid(Tag, 2, P - 2)
                
                    If (Len(Name) > 0) And (Len(Version) > 0) Then
                        Dim x As ClDTD
                        Set x = New ClDTD
                        Set x = DTDCol(Name + " " + Version, achou)
                        Set x = Nothing
                        If achou Then
                            CurrDTD = Name + " " + Version
                            FormMarkup.
                        Else
                            Call Msg.GiveRunInformation("Indefined document type: " + Name + " " + Version)
                        End If
                    End If
                End If
            End If
            If achou Then
                'Encontrado
                LimInf.i = iFech
                LimInf.j = jFech
                Call .ForwardPosition(LimInf.i, LimInf.j, 1)
                
                ini.i = iAbre
                ini.j = jAbre
                Fim.i = iFech
                Fim.j = jFech
            Else
                'Pega uma posicao apos "["
                LimInf.i = iAbre
                LimInf.j = jAbre
                Call .ForwardPosition(LimInf.i, LimInf.j, 1)
            End If
        End If
    Wend
    End With
    FindInitialTag = achou
End Function

'-----------------------------------------------------------------------
'FindInitialTag2 - procura a tag inicial
'LimInf - limite inferior
'LimSup - limite superior
'Tag    - tag inicial
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Private Function FindInitialTag2(LimInf As TpPosicao, LimSup As TpPosicao, ini As TpPosicao, Fim As TpPosicao, Tag As String) As Boolean
    Dim iAbre As Long
    Dim jAbre As Long
    Dim iFech As Long
    Dim jFech As Long
    Dim achou As Boolean
    
    With Text
    While .ExisteStr(LimInf.i, LimInf.j, LimSup.i, LimSup.j) And (Not achou)
        Call .InString(LimInf.i, LimInf.j, LimSup.i, LimSup.j, TagInicialAbre, iAbre, jAbre)
        Call .InString(LimInf.i, LimInf.j, LimSup.i, LimSup.j, TagInicialFech, iFech, jFech)
        Tag = RmHTMLTotal(.GetSubstrRange(iAbre, jAbre, iFech, jFech, SepLinha))
        If Not ExisteVisibleChars(Tag) Then
            'Nenhum tag encontrado
            If (jAbre = 0) Or (jFech = 0) Then
                LimInf = LimSup
                Call .ForwardPosition(LimInf.i, LimInf.j, 1)
            Else 'foi encontrado ] antes de [
                LimInf.i = iAbre
                LimInf.j = jAbre
            End If
        Else
            'Suposto tag encontrado
            If InStr(Mid(Tag, 2), TagInicialAbre) > 0 Then
                achou = False
            Else
                achou = IsTag(Tag)
            End If
            If achou Then
                'Encontrado
                LimInf.i = iFech
                LimInf.j = jFech
                Call .ForwardPosition(LimInf.i, LimInf.j, 1)
                
                ini.i = iAbre
                ini.j = jAbre
                Fim.i = iFech
                Fim.j = jFech
            Else
                'Pega uma posicao apos "["
                LimInf.i = iAbre
                LimInf.j = jAbre
                Call .ForwardPosition(LimInf.i, LimInf.j, 1)
            End If
        End If
    Wend
    End With
    FindInitialTag2 = achou
End Function

'-----------------------------------------------------------------------
'IsTag  - verifica se é uma tag
'Tag    - suposta tag
'Retorno    - verdadeiro ou falso
'-----------------------------------------------------------------------
Function IsTag(Tag As String) As Boolean
    Dim ret As Boolean
    Dim P1 As Long
    Dim P2 As Long
    Dim ComEspaco As String
    Dim SemEspaco As String
    
    P1 = 1
    P2 = InStr(Tag, SepLinha)
    While P2 > 0
        ComEspaco = ComEspaco + Mid(Tag, P1, P2 - P1) + " "
        SemEspaco = SemEspaco + Mid(Tag, P1, P2 - P1)
        P1 = P2 + 2
        P2 = InStr(P1, Tag, SepLinha, 0)
    Wend
    If P2 = 0 Then
        ComEspaco = ComEspaco + Mid(Tag, P1)
        SemEspaco = SemEspaco + Mid(Tag, P1)
    End If
    If P1 = 1 Then
        ret = IsTagAux(Tag)
    Else
        ret = IsTagAux(ComEspaco)
        If ret = 0 Then
            ret = IsTagAux(SemEspaco)
            Tag = SemEspaco
        Else
            Tag = ComEspaco
        End If
    End If
    IsTag = ret
End Function

'-----------------------------------------------------------------------
'IsTagAux   - (função auxiliar) verifica se é uma tag
'Tag        - suposta tag
'Retorno    - verdadeiro ou falso
'-----------------------------------------------------------------------
Private Function IsTagAux(Tag As String) As Boolean
    Dim P As Long
    Dim Key As String
    Dim existe As Boolean
    
    If StrComp(Tag, TagInicialAbre + DTDCol(CurrDTD).Name + TagInicialFech) = 0 Then
        existe = True
    Else
        Key = Mid(Tag, 2, Len(Tag) - 2)
        P = InStr(Key, DTDCol(CurrDTD).Name + " ")
        
        If P = 1 Then existe = AreInitialTagAtributes(Mid(Key, Len(DTDCol(CurrDTD).Name) + 1))
    End If
    IsTagAux = existe
End Function

'-----------------------------------------------------------------------
'AreInitialTagAtributes   - verifica se são MaybeAtributes da tag inicial
'MaybeAtributes  - supostos atributos

'Retorno    - verdadeiro ou falso
'-----------------------------------------------------------------------
Private Function AreInitialTagAtributes(MaybeAtributes As String) As Boolean
    Dim Suspeitos As String
    Dim patr As Long
    Dim ret As Boolean
    Dim j As Long
    Dim Atribs() As String
    Dim QtdAtribs As Long
    
    QtdAtribs = GetElemStr(DTDCol(CurrDTD).IniTagAtrs, ",", Atribs)
    If Len(MaybeAtributes) = 0 Then
        ret = True
    Else
        If QtdAtribs > 0 Then
            Suspeitos = MaybeAtributes
            For j = 1 To QtdAtribs
                patr = InStr(Suspeitos, " " + Atribs(j) + "=")
                If patr > 0 Then
                    Suspeitos = Mid(Suspeitos, 1, patr - 1) + Mid(Suspeitos, patr + Len(Atribs(j)) + 2)
                    ret = True
                End If
            Next
            If InStr(Suspeitos, "=") > 0 Then ret = False
        End If
    End If
    
    AreInitialTagAtributes = ret
End Function

Public Property Let ErrQtdMax(ByVal vData As Long)
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.ErrQtdMax = 5
    
    mvarErrQtdMax = MaxStrLen / MaxMsgLen
    If vData < mvarErrQtdMax Then mvarErrQtdMax = vData
End Property

Public Property Get ErrQtdMax() As Long
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: Debug.Print X.ErrQtdMax
    If mvarErrQtdMax = 0 Then
        ErrQtdMax = MaxStrLen / MaxMsgLen
    Else
        ErrQtdMax = mvarErrQtdMax
    End If
End Property

Public Property Set registro(ByVal vData As Object)
'used when assigning an Object to the property, on the left side of a Set statement.
'Syntax: Set x.Registro = Form1
    Set mvarRegistro = vData
End Property

Public Property Get registro() As ClIsisDll
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: Debug.Print X.Registro
    Set registro = mvarRegistro
End Property

Public Property Let OutputFile(ByVal vData As String)
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.OutputFile = 5
    mvarOutputFile = vData
End Property

Public Property Get OutputFile() As String
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: Debug.Print X.OutputFile
    OutputFile = mvarOutputFile
End Property

