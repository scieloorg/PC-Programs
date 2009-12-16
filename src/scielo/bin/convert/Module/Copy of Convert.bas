Attribute VB_Name = "Converter"
Option Explicit

Type TpPosicao
    i As Long
    j As Long
End Type

'Uso de isisdll
Public a    As Long
Public Const delim1 = "<"
Public Const delim2 = ">"
Public SepLinha As String

Public Const TamMaxIdGrp = 5
Public Const GrpLinkCampo = "C"
Public Const GrpLinkSubc = "S"
Public Const GrpLinkIndex = "R"

Public Msg      As New ClMsg
Public DBTitle  As ClTitleDB

Public parser   As ClParser
Public DTDCol   As ColDTD
Public ConvTables As ClTabConv

'Variaveis de configuracao
Public GlVar As Collection
Public ISISTAGS As ColTag
Public Paths As ColPath

Public RecordInfo As ColRecordInfo

Public QtdTotalDocs As Long
    
'Paths
Private PathBody As String
Private PathMarkup As String
Private PathBase As String

'Nome de arquivos de ExitProgram
Private ArqBase As String
Public DirPeriodicos As String

Function DoConversion(DocMarkup As String, DocBody As String) As Boolean
    Dim BD As ClDBDoc
    Dim ret As Boolean
    Dim Documento As ClDoc
    Dim DocConfigRecord As ClDoc
    Dim TxtDoc As ClFullTxt
    Dim order As String
    Dim pii As String
    Dim References() As String
    Dim i As Long
    Dim T As Date
    Dim ConfigRecord As ClIsisDll
    
    Msg.MsgDir = PathBase
    Msg.MsgFile = ArqBase + ".log"
    
    T = Time
    Call Msg.GiveRunInformation(DocMarkup + ": Start.", , True)
    
    Set BD = New ClDBDoc
    If BD.Inicia(PathBase, ArqBase, Paths("Base").label) Then
        Set parser = New ClParser
        parser.ErrQtdMax = GlVar("mkperrdisplayed").value
        If parser.BeforeParsing(PathMarkup, DocMarkup) Then
            
            Call parser.GetConfigRecord(PathMarkup, DocMarkup, ConfigRecord)
            
            Set DocConfigRecord = New ClDoc
            Set DocConfigRecord.registro = ConfigRecord
            Set parser.registro = Nothing
            
            DocConfigRecord.RunProcsForDB
            
            For i = 1 To RecordInfo.Count
                RecordInfo(i).index = 0
            Next
            
            If DocConfigRecord.SortRecords(PathMarkup, DocMarkup, order, pii) Then
                If BD.DocSave(DocMarkup, pii, DocConfigRecord.Records) Then
                    If BD.CheckConfiguration(pii) Then
                        If BD.CheckOrder(DocMarkup, order, pii) Then
                            ret = True
                        Else
                            Call Msg.GiveRunInformation("Invalid value of order.", True)
                        End If
                    Else
                        Call FormConfigRecord.CompareConfigurationRecords(PathBase, ArqBase, DocMarkup)
                        BD.DocDel (pii)
                    End If
                End If
            End If
        
            If ret Then
        
                If parser.Parse(PathMarkup, DocMarkup) Then
            
                    Call parser.PrintParserErrors(Msg.MsgDir, Msg.MsgFile)

                    Set Documento = New ClDoc
                    Set Documento.registro = parser.registro
                    Set parser.registro = Nothing
                    Set parser = Nothing
            
                    Call Msg.GiveRunInformation(DocMarkup + ": Getting contents of the field of database...")
                    Documento.RunProcsForDB
            
                    Set TxtDoc = New ClFullTxt
                    Set TxtDoc.RegParags = New ColRegistro
                    Set TxtDoc.RegParags = Documento.Records
                    If TxtDoc.Ler(PathBody, DocBody) Then
                        ReDim References(Documento.ReferencesCounter)
                        For i = 1 To Documento.ReferencesCounter
                            References(i) = Documento.References(i)
                        Next
                        Call TxtDoc.FindReferences(References, Documento.ReferencesCounter)
                        Documento.ParagCounter = TxtDoc.GetParagraphs
                        If Documento.ParagCounter > 0 Then Set Documento.Records = TxtDoc.RegParags
                    End If
                    Set TxtDoc = Nothing
            
                    For i = 1 To RecordInfo.Count
                        RecordInfo(i).index = 0
                    Next
                    If Documento.SortRecords(PathMarkup, DocMarkup, order, pii) Then
                        If BD.DocSave(DocMarkup, pii, Documento.Records) Then
                            'If BD.CheckOrder(DocMarkup, order, pii) Then
                                Call BD.ChangeFieldContents(pii)
                            'Else
                                Call Msg.GiveRunInformation("Invalid value of order.", True)
                            'End If
                        Else
                            Call Msg.GiveRunInformation("Failure recording database.", True)
                        End If
                    End If
                End If
                Set Documento = Nothing
            Else
                Call parser.PrintParserErrors(PathBase, Msg.MsgFile)
                Set parser = Nothing
            End If
        End If
    Else
        MsgBox "Failure creating Database of Documents."
    End If
    Set BD = Nothing
    
    Call Msg.GiveRunInformation(DocMarkup + ": End.", , True)
    Call Msg.GiveRunInformation("Time in seconds:" + CStr(DateDiff("s", T, Time)))
    Call Msg.GiveRunInformation("", , True)
    
    
    DoConversion = ret
End Function

Function RunConversion2(DocMarkup As String, DocBody As String) As Boolean
    Dim BD As ClDBDoc
    Dim ret As Boolean
    Dim Documento As ClDoc
    Dim DocConfigRecord As ClDoc
    Dim TxtDoc As ClFullTxt
    Dim order As String
    Dim pii As String
    Dim References() As String
    Dim i As Long
    Dim T As Date
    Dim ConfigRecord As ClIsisDll
    
    Msg.MsgDir = PathBase
    Msg.MsgFile = ArqBase + ".log"
    
    T = Time
    
    Call Msg.GiveRunInformation("", , True)
    Call Msg.GiveRunInformation(DocMarkup + ": Start.", , True)
    
    Set BD = New ClDBDoc
    If BD.Inicia(PathBase, ArqBase, Paths("Base").label) Then
        Set parser = New ClParser
        parser.ErrQtdMax = GlVar("mkperrdisplayed").value
        If parser.BeforeParsing(PathMarkup, DocMarkup) Then
            
            Call parser.GetConfigRecord(PathMarkup, DocMarkup, ConfigRecord)
            
            Set DocConfigRecord = New ClDoc
            Set DocConfigRecord.registro = ConfigRecord
            Set parser.registro = Nothing
            
            DocConfigRecord.RunProcsForDB
            
            For i = 1 To RecordInfo.Count
                RecordInfo(i).index = 0
            Next
            
            If DocConfigRecord.SortRecords(PathMarkup, DocMarkup, order, pii) Then
                If BD.DocSave(DocMarkup, pii, DocConfigRecord.Records) Then
                    Call FormConfigRecord.CompareConfigurationRecords(PathBase, ArqBase, DocMarkup)
                    If FormConfigRecord.CheckConfiguration Then
                        If BD.CheckOrder(DocMarkup, order, pii) Then
                            ret = True
                        Else
                            Call Msg.GiveRunInformation("Invalid value of order.", True)
                        End If
                    End If
                End If
            End If
        
            If Not FormConfigRecord.Quit Then
        
                If parser.Parse(PathMarkup, DocMarkup) Then
            
                    Call parser.PrintParserErrors(Msg.MsgDir, Msg.MsgFile)

                    Set Documento = New ClDoc
                    Set Documento.registro = parser.registro
                    Set parser.registro = Nothing
                    Set parser = Nothing
            
                    Call Msg.GiveRunInformation(DocMarkup + ": Getting contents of the field of database...")
                    Documento.RunProcsForDB
            
                    Set TxtDoc = New ClFullTxt
                    Set TxtDoc.RegParags = New ColRegistro
                    Set TxtDoc.RegParags = Documento.Records
                    If TxtDoc.Ler(PathBody, DocBody) Then
                        ReDim References(Documento.ReferencesCounter)
                        For i = 1 To Documento.ReferencesCounter
                            References(i) = Documento.References(i)
                        Next
                        Call TxtDoc.FindReferences(References, Documento.ReferencesCounter)
                        Documento.ParagCounter = TxtDoc.GetParagraphs
                        If Documento.ParagCounter > 0 Then Set Documento.Records = TxtDoc.RegParags
                    End If
                    Set TxtDoc = Nothing
            
                    For i = 1 To RecordInfo.Count
                        RecordInfo(i).index = 0
                    Next
                    If Documento.SortRecords(PathMarkup, DocMarkup, order, pii) Then
                        If BD.DocSave(DocMarkup, pii, Documento.Records) Then
                            'If BD.CheckOrder(DocMarkup, order, pii) Then
                                Call BD.ChangeFieldContents(pii)
                            'Else
                                Call Msg.GiveRunInformation("Invalid value of order.", True)
                            'End If
                        Else
                            Call Msg.GiveRunInformation("Failure recording database.", True)
                        End If
                    End If
                End If
                Set Documento = Nothing
            Else
                Call parser.PrintParserErrors(PathBase, Msg.MsgFile)
                Set parser = Nothing
            End If
        End If
    Else
        MsgBox "Failure creating Database of Documents."
    End If
    Set BD = Nothing
    
    Call Msg.GiveRunInformation(DocMarkup + ": End.", , True)
    Call Msg.GiveRunInformation("Time in seconds:" + CStr(DateDiff("s", T, Time)))
    
    
    
    RunConversion2 = ret
End Function

Function Executar(DocMarkup As String, DocBody As String) As Boolean
    Dim BD As ClDBDoc
    Dim ret As Boolean
    Dim Documento As ClDoc
    Dim TxtDoc As ClFullTxt
    Dim order As String
    Dim pii As String
    Dim References() As String
    Dim i As Long
    Dim T As Date
    
    Msg.MsgDir = PathBase
    Msg.MsgFile = ArqBase + ".log"
    T = Time
    Call Msg.GiveRunInformation(DocMarkup + ": Start.", , True)
    
    Set BD = New ClDBDoc
    If BD.Inicia(PathBase, ArqBase, Paths("Base").label) Then
        Set parser = New ClParser
        parser.ErrQtdMax = GlVar("mkperrdisplayed").value
        
        If parser.Parse(PathMarkup, DocMarkup) Then
            Call parser.PrintParserErrors(Msg.MsgDir, Msg.MsgFile)

            Set Documento = New ClDoc
            Set Documento.registro = parser.registro
            Set parser.registro = Nothing
            Set parser = Nothing
            
            Call Msg.GiveRunInformation(DocMarkup + ": Getting contents of the field of database...")
            Documento.RunProcsForDB
            
            Set TxtDoc = New ClFullTxt
            Set TxtDoc.RegParags = New ColRegistro
            Set TxtDoc.RegParags = Documento.Records
            If TxtDoc.Ler(PathBody, DocBody) Then
                ReDim References(Documento.ReferencesCounter)
                For i = 1 To Documento.ReferencesCounter
                    References(i) = Documento.References(i)
                Next
                Call TxtDoc.FindReferences(References, Documento.ReferencesCounter)
                Documento.ParagCounter = TxtDoc.GetParagraphs
                If Documento.ParagCounter > 0 Then Set Documento.Records = TxtDoc.RegParags
            End If
            Set TxtDoc = Nothing
            
            For i = 1 To RecordInfo.Count
                RecordInfo(i).index = 0
            Next
            If Documento.SortRecords(PathMarkup, DocMarkup, order, pii) Then
                If BD.DocSave(DocMarkup, pii, Documento.Records) Then
                    If BD.CheckOrder(DocMarkup, order, pii) Then
                        Call BD.ChangeFieldContents(pii)
                    Else
                        Call Msg.GiveRunInformation("Invalid value of order.", True)
                    End If
                Else
                    Call Msg.GiveRunInformation("Failure recording database.", True)
                End If
            End If
            Set Documento = Nothing
        Else
            Call parser.PrintParserErrors(PathBase, Msg.MsgFile)
            Set parser = Nothing
        End If
    Else
        MsgBox "Failure creating Database of Documents."
    End If
    Set BD = Nothing
    
    Call Msg.GiveRunInformation(DocMarkup + ": End.", , True)
    Call Msg.GiveRunInformation("Time in seconds:" + CStr(DateDiff("s", T, Time)))
    Call Msg.GiveRunInformation("", , True)
    
    
    Executar = ret
End Function

Function RunConversion(DocMarkup As String, DocBody As String) As Boolean
    Dim BD As ClDBDoc
    Dim ret As Boolean
    Dim Documento As ClDoc
    Dim TxtDoc As ClFullTxt
    Dim order As String
    Dim pii As String
    Dim References() As String
    Dim i As Long
    Dim T As Date
    Dim DocConfig As ColRegistro
    
    Msg.MsgDir = PathBase
    Msg.MsgFile = ArqBase + ".log"
    T = Time
    Call Msg.GiveRunInformation(DocMarkup + ": Start.", , True)
    
    Set BD = New ClDBDoc
    If BD.Inicia(PathBase, ArqBase, Paths("Base").label) Then
        Set parser = New ClParser
        parser.ErrQtdMax = GlVar("mkperrdisplayed").value
        If parser.BeforeParsing(PathMarkup, DocMarkup) Then
            If parser.Parse(PathMarkup, DocMarkup) Then
            Call parser.PrintParserErrors(Msg.MsgDir, Msg.MsgFile)

            Set Documento = New ClDoc
            Set Documento.registro = parser.registro
            Set parser.registro = Nothing
            Set parser = Nothing
            
            Call Msg.GiveRunInformation(DocMarkup + ": Getting contents of the field of database...")
            Documento.RunProcsForDB
            
            Set TxtDoc = New ClFullTxt
            Set TxtDoc.RegParags = New ColRegistro
            Set TxtDoc.RegParags = Documento.Records
            If TxtDoc.Ler(PathBody, DocBody) Then
                ReDim References(Documento.ReferencesCounter)
                For i = 1 To Documento.ReferencesCounter
                    References(i) = Documento.References(i)
                Next
                Call TxtDoc.FindReferences(References, Documento.ReferencesCounter)
                Documento.ParagCounter = TxtDoc.GetParagraphs
                If Documento.ParagCounter > 0 Then Set Documento.Records = TxtDoc.RegParags
            End If
            Set TxtDoc = Nothing
            
            
            If Documento.SortRecords(PathMarkup, DocMarkup, order, pii) Then
                Set DocConfig = New ColRegistro
                For i = 1 To 2
                    With Documento.Records.Item(i)
                    DocConfig.Add
                    DocConfig(i).Campo = .Campo
                    DocConfig(i).conteudo = .conteudo
                    DocConfig(i).Contexto = .Contexto
                    DocConfig(i).Id = .Id
                    DocConfig(i).Tipo = .Tipo
                    End With
                Next
                
                If BD.DocSave(DocMarkup, pii, DocConfig) Then
                    Set DocConfig = Nothing
                    If BD.CheckOrder(DocMarkup, order, pii) Then
                        If BD.CheckConfigurationRecord(pii) Then
                            ret = True
                        End If
                    Else
                        Call Msg.GiveRunInformation("Invalid value of order.", True)
                    End If
                End If
                
                If ret Then
                    If BD.DocSave(DocMarkup, pii, Documento.Records) Then
                        Call BD.ChangeFieldContents(pii)
                    End If
                Else
                    Call Msg.GiveRunInformation("Failure recording database.", True)
                End If
            End If
            Set Documento = Nothing
        Else
            Call parser.PrintParserErrors(PathBase, Msg.MsgFile)
            Set parser = Nothing
        End If
    Else
        MsgBox "Failure creating Database of Documents."
    End If
    Set BD = Nothing
    
    Call Msg.GiveRunInformation(DocMarkup + ": End.", , True)
    Call Msg.GiveRunInformation("Time in seconds:" + CStr(DateDiff("s", T, Time)))
    Call Msg.GiveRunInformation("", , True)
    
    RunConversion = ret
End Function
Function ExistConfigurationRecord(SerialId As String, IssueId As String) As Boolean
    Dim BD As ClDBDoc
    Dim ret As Boolean
    Dim ISSN() As String
    Dim ISSNCount As Long
    Dim q As Long
    Dim MfnIssue() As Long
    Dim DBIssue  As ClIsisDll
    
    Set BD = New ClDBDoc
    Paths("Issue").NotChecked = True
    If LoadIsisDB("Issue", DBIssue) Then
        If BD.Inicia(PathBase, ArqBase, Paths("Base").label) Then
            If BD.ConfigRecordExist Then
                ret = True
            Else
                ISSNCount = DBTitle.GetFieldContents(SerialId, ISISTAGS("ISSNTitle").value, ISSN)
                If ISSNCount > 0 Then
                    q = DBIssue.MfnFind(ISSN(1) + IssueId, MfnIssue)
                    If q > 0 Then
                        BD.Isis.BDDel
                        ret = DBIssue.RecordCopy(MfnIssue(1), BD.Isis, 1)
                    ElseIf q = 0 Then
                        Call Msg.GiveRunInformation("Configuration record is missing in database Issue", True)
                    End If
                End If
            End If
        End If
    End If
    Set DBIssue = Nothing
    Set BD = Nothing
    ExistConfigurationRecord = ret
End Function

Function TagContents(ByVal conteudo As String, ByVal Tag As Long) As String
    Dim ComTag As String
    Dim aux As String
    Dim P As Long
    
    If Tag = 0 Then
        MsgBox "TagContents: tag=0. Conteudo=" + conteudo
    ElseIf Len(conteudo) = 0 Then
        'MsgBox "TagContents: Conteudo=" + conteudo
    Else
        conteudo = RmNewLineInStr(conteudo)
        ComTag = delim1 + CStr(Tag) + delim2 + conteudo + delim1 + "/" + CStr(Tag) + delim2 + SepLinha
    End If
    TagContents = ComTag
End Function

Sub ShowMsgInForm(ByVal mens As String)
    FormMarkup.LabMsg.Caption = mens
    FormMarkup.LabMsg.Refresh
End Sub

Public Function CheckConfigvars(i As Long) As Boolean
    Dim ret As Boolean
    Dim Invalid As Boolean
    
    ret = True
    
        Select Case GlVar(i).Tipo
        Case "n"
            Invalid = (GlVar(i).value = 0)
        Case "s"
            Invalid = (GlVar(i).value = "")
        Case Else
            Invalid = False
        End Select
        If Invalid Then
            MsgBox (GlVar(i).value + " - Invalid value of " + GlVar(i).Nome)
            ret = False
        End If
    CheckConfigvars = ret
End Function

Function LoadFilesMarkup() As Boolean
    Dim ret As Boolean
    
    DirPeriodicos = GlVar("workdrv").value + PathSep + Paths("work").DirName
    If Paths.CheckPaths(DirPeriodicos, Paths("work").label) Then
        ret = True
        ret = ret And LoadTitleDB
        ret = ret And LoadHTMLTagsTable
        ret = ret And LoadHTML2ASCIITable
        'ret = ret And LoadConvTables
    End If
    LoadFilesMarkup = ret
    
End Function
Sub UnloadTitle()
    Paths("Title").NotChecked = True
    Set DBTitle = Nothing
End Sub

Function LoadFilesBD() As Boolean
    DirPeriodicos = GlVar("workdrv").value + PathSep + Paths("work").DirName
    If Paths.CheckPaths(DirPeriodicos, Paths("work").label) Then
        LoadFilesBD = LoadTitleDB
    End If
End Function

Function LoadTitleDB() As Boolean
    If Paths("Title").NotChecked Then
        Set DBTitle = New ClTitleDB
        If DBTitle.Inicia(DirPeriodicos + PathSep + Paths("Title").DirName, Paths("Title").FileName, Paths("Inverted Title").FileName, Paths("FBPE").FileName) Then
            Paths("Title").NotChecked = False
        End If
    End If
    LoadTitleDB = Not Paths("Title").NotChecked
End Function

Function LoadIsisDB(IsisKey As String, IsisDB As ClIsisDll) As Boolean
    If Paths(IsisKey).NotChecked Then
        Set IsisDB = New ClIsisDll
        If IsisDB.Inicia(DirPeriodicos + PathSep + Paths(IsisKey).DirName, Paths(IsisKey).FileName, Paths(IsisKey).label) Then
            If IsisDB.IfCreate(Paths(IsisKey).FileName) Then
                Paths(IsisKey).NotChecked = False
                If IsisDB.MfnQuantity > 0 Then Call IsisDB.IfUpdate(1, IsisDB.MfnQuantity)
            End If
        End If
    End If
    LoadIsisDB = Not Paths(IsisKey).NotChecked
End Function
'remover
Function LoadConvTables() As Boolean
    With DTDCol(CurrDTD)
    If Paths(.ProcTableFile).NotChecked Or Paths(.CTableFile).NotChecked Or Paths(.IdTpRegTableFile).NotChecked Then
        Set .TabConv = New ClTabConv
        .IsLoaded = True
        
        If .TabConv.Inicia(DirPeriodicos + PathSep + Paths("CTabPath").DirName, .ProcTableFile, .CTableFile, .IdTpRegTableFile) Then
            Set ConvTables = New ClTabConv
            Set ConvTables = .TabConv
            Paths(.IdTpRegTableFile).NotChecked = False
            Paths(.ProcTableFile).NotChecked = False
            Paths(.CTableFile).NotChecked = False
        End If
    End If
    
    LoadConvTables = Not Paths(.ProcTableFile).NotChecked
    End With
End Function

Sub SetOrdReg(Ordem As String)
    Dim q As Long
    Dim aux() As String
    
    Set RecordInfo = New ColRecordInfo
    q = GetElemStr(Ordem, ",", aux)
    Call RecordInfo.Add(, aux(1), 1, "outline")
    Call RecordInfo.Add(, aux(2), 2, "header")
    Call RecordInfo.Add(, aux(3), 3, "font")
    Call RecordInfo.Add(, aux(4), 4, "paragraph")
    Call RecordInfo.Add(, aux(5), 5, "citation")
    Call RecordInfo.Add(, aux(6), 6, "reference")
    If q <> RecordInfo.Count Then MsgBox "Wrong number of record type."
End Sub

Private Sub Main()
    Dim ret As Boolean
    Dim i As Long
    
    If ConfigGet Then
        SepLinha = Chr(13) + Chr(10)
        SetOrdReg (GlVar("rec_order").value)
        ret = True
        For i = 1 To ISISTAGS.Count
            ret = ret And ISISTAGS.CheckTags(i)
        Next
        For i = 1 To GlVar.Count
            ret = ret And CheckConfigvars(i)
        Next

        FormMenu.Show
        If Not (ret) Then FormConfig.Show vbModal
        
    End If
End Sub

Function ConfigGet() As Boolean
    Dim Var As ClVarConfig
    Dim NewDTD As ClDTD
    Dim Section As String
    Dim fn As Long
    Dim Linha As String
    Dim Key As String
    Dim P As Long
    Dim i As Long
    Dim value() As String
    Dim q As Long
    Dim Fim As Boolean
    
    Set GlVar = New Collection
    Set DTDCol = New ColDTD
    Set Paths = New ColPath
    Set ISISTAGS = New ColTag
    
    fn = FreeFile(1)
    Open "Conversor.ini" For Input As fn
    While Not EOF(fn) And (Not Fim)
        Line Input #fn, Linha
        
        P = InStr(Linha, "=")
        If P > 0 Then
            Key = Mid(Linha, 1, P - 1)
            Linha = Mid(Linha, P + 1)
        End If
        
        q = GetElemStr(Linha, ",", value)
        
        Select Case q
        Case 1
            If Len(Linha) = 0 Then
            
            ElseIf (InStr(Linha, "[") = 1) And (InStr(Linha, "]") = Len(Linha)) Then
                Section = Linha
            Else
                Fim = True
            End If
        Case 3
            Select Case Section
            Case "[Tags]"
                Call ISISTAGS.Add(value(3), Key, CLng(value(1)), value(2), Key)
            Case "[Variables]"
                Set Var = New ClVarConfig
                Var.Key = Key
                Var.value = value(1)
                Var.Nome = value(2)
                Var.Tipo = value(3)
                Call GlVar.Add(Var, Var.Key)
            Case Else
                Fim = True
            End Select
        Case 4
            Select Case Section
            Case "[Files]"
                Call Paths.Add(value(1), value(2), value(3), value(4), True, Key)
            End Select
        Case 7
            If Section = "[DTDs]" Then
                Set NewDTD = New ClDTD
                Set NewDTD = DTDCol.Add(value(1) + " " + value(2))
                NewDTD.Name = value(1)
                NewDTD.Version = value(2)
                NewDTD.FileName = value(3)
                NewDTD.IniTagAtrs = value(4)
                NewDTD.CTableFile = value(5)
                NewDTD.ProcTableFile = value(6)
                NewDTD.IdTpRegTableFile = value(7)
            Else
                Fim = True
            End If
        Case Else
            Fim = True
        End Select
    Wend
    Close fn
    If Fim Then
        MsgBox "Linha:" + Linha, , "Failure in CONVERSOR.INI"
    Else
    End If
    ConfigGet = Not Fim
End Function


Sub ConfigSet()
    Dim Var As ClVarConfig
    Dim fn As Long
    Dim i As Long
    
    fn = FreeFile(1)
    
    Open "conversor.ini" For Output As fn
    Print #fn, "[Variables]"
    For i = 1 To GlVar.Count
        Set Var = GlVar.Item(i)
        Var.value = PutAspas(Var.value, ",")
        Print #fn, Var.Key + "=" + Var.value + "," + Var.Nome + "," + Var.Tipo
    Next
    If DTDCol.Count > 0 Then
        Print #fn,
        Print #fn, "[DTDs]"
        For i = 1 To DTDCol.Count
            With DTDCol(i)
            Print #fn, .Name + "," + .Version + "," + .FileName + "," + PutAspas(.IniTagAtrs, ",") + "," + .CTableFile + "," + .ProcTableFile + "," + .IdTpRegTableFile
            End With
        Next
    End If
    
    If Paths.Count > 0 Then
        Print #fn,
        Print #fn, "[Files]"
        For i = 1 To Paths.Count
            With Paths(i)
            Print #fn, .Key + "=" + .DirName + "," + .FileName + "," + .label + "," + .PType
            End With
        Next
    End If
    
    If ISISTAGS.Count > 0 Then
        Print #fn,
        Print #fn, "[Tags]"
        For i = 1 To ISISTAGS.Count
            With ISISTAGS(i)
            Print #fn, .Key + "=" + CStr(.value) + "," + .Subf + "," + .label
            End With
        Next
    End If
    
    Close fn
End Sub

Public Function SetCurrentIssuePath(Sgl As String, Vol As String, VolSuppl As String, No As String, NoSuppl As String, Path As String) As Boolean
    Dim ret As Boolean
    
    ArqBase = IssueId(Vol, VolSuppl, No, NoSuppl)
    Path = DirPeriodicos + PathSep + Sgl + PathSep + ArqBase + PathSep
        
    PathBody = Path + Paths("Body").DirName
    PathMarkup = Path + Paths("Markup").DirName
    PathBase = Path + Paths("Base").DirName
        
        If DirExist(PathBase, Paths("Base").label) Then
            If DirExist(PathBody, Paths("Body").label) Then
                If DirExist(PathMarkup, Paths("Markup").label) Then
                    If Not FileExist(PathBase + PathSep + ArqBase + ".fst", "fst file of " + Paths("Base").label) Then Call FileCopy(DirPeriodicos + PathSep + Paths("CTabPath").DirName + PathSep + "article.fst", PathBase + PathSep + ArqBase + ".fst")
                    ret = True
                End If
            End If
        End If
    SetCurrentIssuePath = ret
End Function

Public Function BodyFileName(file As String) As String
    Dim file2 As String
    
    If FileExist(PathBody, file) Then
        file2 = file
    Else
        If (InStr(1, file, ".html", vbTextCompare) > 0) Then
            file2 = Mid(file, 1, Len(file) - 1)
        ElseIf InStr(1, file, ".htm", vbTextCompare) > 0 Then
            file2 = file + "l"
        End If
    End If
    If Len(file2) > 0 Then
        If Not FileExist(PathBody, file2, "Body Document") Then file2 = ""
    End If
    BodyFileName = file2
End Function


Function IssueId(Vol As String, SupplVol As String, Num As String, SupplNum As String) As String
    Dim ret As String
    
    If Len(Vol) > 0 Then ret = ret + GlVar("volsgl").value + Vol
    If Len(SupplVol) > 0 Then ret = ret + GlVar("volsupplsgl").value + SupplVol
    If Len(Num) > 0 Then ret = ret + GlVar("nosgl").value + Num
    If Len(SupplNum) > 0 Then ret = ret + GlVar("nosupplsgl").value + SupplNum
    
    IssueId = ret
End Function
Function IssueKey(Vol As String, SupplVol As String, Num As String, SupplNum As String) As String
    Dim ret As String
    
    ret = ret + GlVar("volsgl").value + Vol
    ret = ret + GlVar("volsupplsgl").value + SupplVol
    ret = ret + GlVar("nosgl").value + Num
    ret = ret + GlVar("nosupplsgl").value + SupplNum
    
    IssueKey = ret
End Function

Function MsgIssueId(Vol As String, SupplVol As String, Num As String, SupplNum As String, Iseqno As String) As String
    Dim ret As String
    
    If Len(Vol) > 0 Then ret = ret + "Volume = " + Vol + SepLinha
    If Len(SupplVol) > 0 Then ret = ret + "Volume Suppl = " + SupplVol + SepLinha
    If Len(Num) > 0 Then ret = ret + "Number = " + Num + SepLinha
    If Len(SupplNum) > 0 Then ret = ret + "Number Suppl = " + SupplNum + SepLinha
    If Len(Iseqno) > 0 Then ret = ret + "Seq. Number = " + Iseqno + SepLinha
    MsgIssueId = ret
End Function


Sub CleanDocDB()
    Dim BD  As ClDBDoc
    
    Set BD = New ClDBDoc
    If BD.Inicia(PathBase, ArqBase, Paths("Base").label) Then
        If BD.GarbageCollection Then
            MsgBox "Success."
        Else
            MsgBox "Failure."
        End If
    End If
    Set BD = Nothing
End Sub


Property Let LoadAgain(v As Boolean)
    Dim i As Long
    
    For i = 1 To Paths.Count
        Paths(i).NotChecked = v
    Next
End Property
Property Get LoadAgain() As Boolean
    Dim i As Long
    Dim v As Boolean
    
    v = True
    For i = 1 To Paths.Count
        v = v And Paths(i).NotChecked
    Next
    LoadAgain = v
End Property

