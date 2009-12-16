VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "ClDBDoc"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

Private mvarRegistros As ColRegistro  'local copy
Private mvarDBPath As String 'local copy
Private mvarDBName As String 'local copy
Private mvarDocName As String 'local copy
Private mvarIsis As ClIsisDll 'local copy

Private ValuesForCheckingCount   As Long
Private Labels() As String
Private ValueInIssueRecord() As String
Private ValueInDocument() As String


Public Property Set Isis(ByVal vData As Object)
'used when assigning an Object to the property, on the left side of a Set statement.
'Syntax: Set x.Isis = Form1
    Set mvarIsis = vData
End Property

Public Property Get Isis() As ClIsisDll
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: Debug.Print X.Isis
    Set Isis = mvarIsis
End Property

Public Property Get FullPath() As String
    FullPath = mvarDBPath + PathSep + mvarDBName
End Property

Public Property Let DocName(ByVal vData As String)
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.DocName = 5
    mvarDocName = vData
End Property

Public Property Get DocName() As String
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: Debug.Print X.DocName
    DocName = mvarDocName
End Property

Public Property Let DBName(ByVal vData As String)
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.DBName = 5
    mvarDBName = vData
End Property

Public Property Get DBName() As String
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: Debug.Print X.DBName
    DBName = mvarDBName
End Property

Public Property Let DBPath(ByVal vData As String)
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.DBPath = 5
    mvarDBPath = vData
End Property

Public Property Get DBPath() As String
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: Debug.Print X.DBPath
    DBPath = mvarDBPath
End Property

Public Property Set Records(ByVal vData As Object)
'used when assigning an Object to the property, on the left side of a Set statement.
'Syntax: Set x.Records = Form1
    Set mvarRegistros = vData
End Property

Public Property Get Records() As ColRegistro
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: Debug.Print X.Records
    Set Records = mvarRegistros
End Property

'-----------------------------------------------------------------------
'Inicia - Inicia a base de dados de documentos
'Path   - caminho da base
'FileName   - FileName do arquivo da base
'Retorno        - sucesso ou fracasso
'-----------------------------------------------------------------------
Function Inicia(Path As String, FileName As String, label As String) As Boolean
    Dim ret As Boolean
    
    If Isis.Inicia(Path, FileName, label) Then
        'If Not FileExist(Path + PathSep + FileName + ".fst", "fst file of " + Paths("Base").label) Then Call FileCopy(PathParser + PathSep + parser.DTDName + ".fst", Path + PathSep + FileName + ".fst")
        If Isis.IfCreate(FileName) Then
            If Isis.MfnQuantity > 0 Then Call Isis.IfUpdate(1, Isis.MfnQuantity)
            ret = True
            DBPath = Path
            DBName = FileName
        End If
    End If
    Inicia = ret
End Function

'-----------------------------------------------------------------------
'ConfigRecordExist  - Verifica a existência do registro de configuração
'Retorno            - verdadeiro ou falso
'-----------------------------------------------------------------------
Function ConfigRecordExist() As Boolean
    Dim QtdMfn1 As Long
    Dim xMfn1() As Long
    
    QtdMfn1 = Isis.MfnFind("i", xMfn1)
    If QtdMfn1 > 0 Then ConfigRecordExist = (QtdMfn1 = 1) And (xMfn1(1) = 1)
End Function

'-----------------------------------------------------------------------
'LetValuesForComparing - armazena a configuração para comparação
'Label  - nome dos Valuees
'ValInIssueRecord   - Value no registro de configuração
'ValInDoc   - Value no documento
'-----------------------------------------------------------------------
Private Sub LetValuesForComparing(label As String, ValInIssueRecord As String, ValInDoc As String)
    ValuesForCheckingCount = ValuesForCheckingCount + 1
    ReDim Preserve Labels(ValuesForCheckingCount)
    ReDim Preserve ValueInIssueRecord(ValuesForCheckingCount)
    ReDim Preserve ValueInDocument(ValuesForCheckingCount)
    
    Labels(ValuesForCheckingCount) = label
    ValueInIssueRecord(ValuesForCheckingCount) = ValInIssueRecord
    ValueInDocument(ValuesForCheckingCount) = ValInDoc
End Sub

'-----------------------------------------------------------------------
'GetValuesForComparing - obtém as comparações dos Valuees
'i  - índice do Value
'Label  - nome dos Valuees
'ValInIssueRecord   - Value no registro de configuração
'ValInDoc   - Value no documento
'-----------------------------------------------------------------------
Sub GetValuesForComparing(i As Long, label As String, ValInIssueRecord As String, ValInDoc As String)
    If (i > 0) And (i <= ValuesForCheckingCount) Then
        label = Labels(i)
        ValInIssueRecord = ValueInIssueRecord(i)
        ValInDoc = ValueInDocument(i)
    Else
        label = ""
        ValInIssueRecord = ""
        ValInDoc = ""
    End If
End Sub

'-----------------------------------------------------------------------
'CheckConfigurationField   - verifica a configuração de um elemento
'Label  - nome dos Valuees
'Tag    - tag do campo
'MfnConfigRecord    - mfn da base de dados (registro de configuração)
'MfnDoc - mfn do documento (registro do documento)
'Retorno - configuração correta ou não
'-----------------------------------------------------------------------
Private Function CheckConfigurationField(label As String, Tag As Long, MfnConfigRecord As Long, MfnDoc As Long) As Boolean
    Dim ret As Boolean
    Dim FromDoc As String
    Dim FromDB As String
    
    FromDoc = Isis.FieldContentOccGet(MfnDoc, Tag, 1)
    FromDB = Isis.FieldContentOccGet(MfnConfigRecord, Tag, 1)
    If StrComp(FromDB, FromDoc) = 0 Then
        ret = True
    ElseIf MfnConfigRecord = 0 Then
        Call Msg.GiveRunInformation(DocName + ": Value of " + label + " in document: " + FromDoc + ".")
    Else
        Call Msg.GiveRunInformation(DocName + ": Invalid value of " + label + " in document: " + FromDoc + ". In config record: " + FromDB + ".")
    End If
    
    Call LetValuesForComparing(label, FromDB, FromDoc)
    
    CheckConfigurationField = ret
End Function '-----------------------------------------------------------------------
'CheckField   - verifica a configuração de um elemento
'Label  - nome dos Valuees
'Tag    - tag do campo
'MfnConfigRecord    - mfn da base de dados (registro de configuração)
'MfnDoc - mfn do documento (registro do documento)
'Retorno - configuração correta ou não
'-----------------------------------------------------------------------
Private Function CheckField(DocId As String, label As String, Tag As Long, MfnConfigRecord As Long, MfnDoc As Long) As Boolean
    Dim ret As Boolean
    Dim FromDoc As String
    Dim FromDB As String
    
    FromDoc = Isis.FieldContentOccGet(MfnDoc, Tag, 1)
    FromDB = Isis.FieldContentOccGet(MfnConfigRecord, Tag, 1)
    If Len(FromDoc) > 0 Then
        If StrComp(FromDB, FromDoc) = 0 Then
            ret = True
        ElseIf Len(FromDB) = 0 Then
            Call Msg.GiveRunInformation(label + " is missing in Database. " + DocId + ": Value of " + label + " in document: " + FromDoc + ".")
        Else
            Call Msg.GiveRunInformation(DocId + ": Invalid value of " + label + " in document: " + FromDoc + ". In config record: " + FromDB + ".")
        End If
    Else
        ret = True
    End If
    
    CheckField = ret
End Function

'-----------------------------------------------------------------------
'CheckConfigurationSeccode - verifica a configuração de seccode
'MfnConfigRecord    - mfn da base de dados (registro de configuração)
'MfnDoc - mfn do documento (registro do documento)
'Retorno - configuração correta ou não
'-----------------------------------------------------------------------
Function CheckConfigurationSeccode(MfnConfigRecord As Long, MfnDoc As Long) As Boolean
    Dim QtdSec As Long
    Dim SeccodeInDoc As String
    Dim i As Long
    Dim achou As Boolean
    Dim CodeIssue() As String
    Dim SeccodeInConfigRecord As String
    
    SeccodeInDoc = Isis.FieldContentOccGet(MfnDoc, ISISTAGS("seccode").value, 1)
    If Len(SeccodeInDoc) > 0 Then
        QtdSec = Isis.SubfieldContentGet(MfnConfigRecord, ISISTAGS("seccode").value, ISISTAGS("seccode").Subf, CodeIssue)
        achou = (QtdSec = 0)
        While (i < QtdSec) And (Not achou)
            i = i + 1
            SeccodeInConfigRecord = SeccodeInConfigRecord + "," + CodeIssue(i)
            achou = (StrComp(CodeIssue(i), SeccodeInDoc) = 0)
        Wend
        If Len(SeccodeInConfigRecord) > 0 Then SeccodeInConfigRecord = Mid(SeccodeInConfigRecord, 2)
    Else
        achou = True
    End If
    
    If achou Then
        SeccodeInConfigRecord = SeccodeInDoc
    Else
        Call Msg.GiveRunInformation(DocName + ": Invalid value of seccode:" + SeccodeInDoc)
    End If
    
    Call LetValuesForComparing("Seccode", SeccodeInConfigRecord, SeccodeInDoc)
    CheckConfigurationSeccode = achou
End Function

'-----------------------------------------------------------------------
'CheckSeccode - verifica a configuração de seccode
'MfnConfigRecord    - mfn da base de dados (registro de configuração)
'MfnDoc - mfn do documento (registro do documento)
'Retorno - configuração correta ou não
'-----------------------------------------------------------------------
Private Function CheckSeccode(DocId As String, MfnConfigRecord As Long, MfnDoc As Long) As Boolean
    Dim QtdSec As Long
    Dim SeccodeInDoc As String
    Dim i As Long
    Dim achou As Boolean
    Dim CodeIssue() As String
    Dim SeccodeInConfigRecord As String
    
    SeccodeInDoc = Isis.FieldContentOccGet(MfnDoc, ISISTAGS("seccode").value, 1)
    If Len(SeccodeInDoc) > 0 Then
        QtdSec = Isis.SubfieldContentGet(MfnConfigRecord, ISISTAGS("seccode").value, ISISTAGS("seccode").Subf, CodeIssue)
        achou = (QtdSec = 0)
        While (i < QtdSec) And (Not achou)
            i = i + 1
            SeccodeInConfigRecord = SeccodeInConfigRecord + "," + CodeIssue(i)
            achou = (StrComp(CodeIssue(i), SeccodeInDoc) = 0)
        Wend
        If Len(SeccodeInConfigRecord) > 0 Then SeccodeInConfigRecord = Mid(SeccodeInConfigRecord, 2)
    Else
        achou = True
    End If
    
    If achou Then
        SeccodeInConfigRecord = SeccodeInDoc
    Else
        Call Msg.GiveRunInformation(DocId + ": Invalid value of seccode:" + SeccodeInDoc)
    End If
    
    CheckSeccode = achou
End Function

'-----------------------------------------------------------------------
'RecordSave    - grava os Records e retorna o Mfn inicial e a quantidade de Records gravada
'MfnINI    - mfn inicial
'qtd    - quantidade gravada
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Private Function RecordSave(MfnIni As Long, Qtd As Long) As Boolean
    Dim Mfn As Long
    Dim aux As Double
    Dim ret As Boolean
    Dim i As Long
    
    aux = 100 / Records.Count
    Mfn = 1
    ShowMsgInForm (DocName + ": " + CStr(CInt(aux)) + "% loaded.")

    MfnIni = Isis.RecordSave(Records(Mfn).conteudo)
        
    ret = (MfnIni > 0)
    While (Mfn < Records.Count) And ret
        Mfn = Mfn + 1
        ShowMsgInForm (DocName + ": " + CStr(CInt(Mfn * aux)) + "% loaded.")
        ret = (Isis.RecordSave(TagContents(DBName, ISISTAGS("database").value) + Records(Mfn).conteudo) > 0)
    Wend
    If Not ret Then
        Call Msg.GiveRunInformation(DocName + ": Mfn=" + CStr(MfnIni + Mfn - 1))
    End If
    Qtd = Mfn
    ret = ret And (Mfn = Records.Count)
    
    RecordSave = ret
End Function

'-----------------------------------------------------------------------
'RecordUpdate - atualiza uma quantidade de Records a partir do Mfn inicial
'MfnINI    - mfn inicial
'qtd    - quantidade atualizada
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Private Function RecordUpdate(MfnIni As Long, Qtd As Long) As Boolean
    Dim Mfn As Long
    Dim Fim As Long
    Dim ret As Boolean
    Dim i As Long
    
    Fim = MfnIni + Records.Count - 1
    Mfn = MfnIni - 1
    ret = True
    While (Mfn < Fim) And ret
        Mfn = Mfn + 1
        i = i + 1
        ret = Isis.RecordUpdate(Mfn, Records(i).conteudo)
    Wend
    Qtd = i
    ret = ret And (Mfn = Fim)
    
    RecordUpdate = ret
End Function

'-----------------------------------------------------------------------
'RecordDel    - apagar uma quantidade de Records a partir do Mfn inicial
'MfnINI    - mfn inicial
'qtd    - quantidade atualizada
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Private Function Recorddel(MfnIni As Long, Qtd As Long) As Boolean
    Dim Mfn As Long
    Dim Fim As Long
    Dim ret As Boolean
    Dim i As Long
    
    Fim = MfnIni + Qtd - 1
    Mfn = MfnIni - 1
    ret = True
    While (Mfn < Fim) And ret
        Mfn = Mfn + 1
        ret = Isis.Recorddel(Mfn)
    Wend
    ret = ret And (Mfn = Fim)
    
    Recorddel = ret
End Function

'-----------------------------------------------------------------------
'DocDel  - apaga um documento
'pii        - identificação do documento
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Function DocDel(pii As String) As Boolean
    Dim ini As Long
    Dim Fim As Long
    Dim Qtd As Long
    Dim ret As Boolean
    
    If DocExist(pii, ini, Qtd) Then
        Fim = ini + Qtd - 1
        If Recorddel(ini, Qtd) Then ret = Isis.IfUpdate(ini, Fim)
    End If
    DocDel = ret
End Function

'-----------------------------------------------------------------------
'DocSave  - grava um documento
'Name       - nome do documento
'pii        - identificação do documento
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Function DocSave(Name As String, pii As String, DocRecords As ColRegistro) As Boolean
    Dim ini As Long
    Dim Fim As Long
    Dim q As Long
    Dim ret As Boolean
    Dim IniAmpliado As Long
    Dim FimAmpliado As Long
    Dim TamIntervalo As Long
    
    Msg.GiveRunInformation (Name + ": Recording data.")
        Set Records = New ColRegistro
        Set Records = DocRecords
        DocName = Name
        If DocExist(pii, ini, q) Then
            Fim = ini + q - 1
            IniAmpliado = ini
            FimAmpliado = Fim
            TamIntervalo = q
            If Isis.AmpliarIntervaloLivre(IniAmpliado, FimAmpliado) Then TamIntervalo = FimAmpliado - IniAmpliado + 1
            If TamIntervalo < Records.Count Then
                'Não há espaço suficiente
                'MsgBox "...AmpliarIntervalo"
                If Recorddel(ini, q) Then
                    If Isis.BDColetaLixo Then
                        If RecordSave(ini, q) Then
                            ret = Isis.IfUpdate(1, Isis.MfnQuantity)
                        End If
                    End If
                End If
            Else
                If RecordUpdate(IniAmpliado, q) Then
                    ret = True
                    Fim = IniAmpliado + q - 1
                    If Fim < FimAmpliado Then ret = Recorddel(Fim + 1, FimAmpliado - Fim)
                    If ret Then ret = Isis.IfUpdate(IniAmpliado, FimAmpliado)
                Else
                    Call Recorddel(IniAmpliado, q)
                End If
            End If
        Else
            'If Isis.BDOrganiza Then
                If RecordSave(ini, q) Then
                    ret = Isis.IfUpdate(ini, ini + q - 1)
                    'ret = Isis.ifupdate(ini1, Isis.MfnQuantity)
                Else
                    Call Recorddel(ini, q - 1)
                End If
            'End If
        End If
        Set Records = Nothing
    
    DocSave = ret
End Function

'-----------------------------------------------------------------------
'ChangeFieldContents    - substitui nos Records de um documento o traço que indica previous pelo nome do autor
'pii        - identificação do documento
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Function ChangeFieldContents(pii As String) As Boolean
    Dim ret As Boolean
    Dim i As Long
    Dim MfnIni As Long
    Dim Ref1Start As Long
    Dim Ref2Start As Long
    Dim q As Long
    Dim MfnReference As Long
    Dim ISSN As String
    Dim ISSNDB   As ClIsisDll
    Dim ISIDB    As ClIsisDll
    
    ret = True
    'SetReferencesMfn (pii)
    If DocExist(pii, MfnIni, q) Then
        If RecordInfo("citation").index > 0 Then
            Ref1Start = MfnIni + RecordInfo("citation").index - 1
            Ref2Start = MfnIni + RecordInfo("reference").index - 1
            
            Paths("ISSN_ISI").NotChecked = True
            Paths("ISSN").NotChecked = True
            If LoadIsisDB("ISSN_ISI", ISIDB) And LoadIsisDB("ISSN", ISSNDB) Then
                For i = Ref1Start To Ref2Start - 1
                    SetPrevious (i)
                    Call CheckISSN(i, ISSNDB, ISIDB)
                Next
                
                MfnReference = Ref1Start
                For i = Ref2Start To (Ref2Start - Ref1Start + Ref2Start - 1)
                    SetPrevious (i)
                    ISSN = Isis.FieldContentOccGet(MfnReference, ISISTAGS("ISSN").value, 1)
                    MfnReference = MfnReference + 1
                    If Len(ISSN) > 0 Then Call Isis.FieldContentAdd(i, ISISTAGS("ISSN").value, ISSN)
                Next
            End If
            Set ISIDB = Nothing
            Set ISSNDB = Nothing
        End If
    End If
    ChangeFieldContents = ret
End Function

Function SetPrevious(Mfn As Long) As Boolean
    Dim ret As Boolean
    Dim QtdTagPrevious As Long
    Dim QtdTag As Long
    Dim i As Long
    Dim j As Long
    Dim k As Long
    Dim n As Long
    Dim Tag() As String
    Dim Tags() As String
    Dim achou As Boolean
    Dim novo As String
    Dim TagNovo As Long
    
    With Isis
    If (Mfn > 0) And (Mfn <= .MfnQuantity) Then
        ret = True
        QtdTagPrevious = .FieldContentGet(Mfn, ISISTAGS("previous").value, Tags)
        For i = 1 To QtdTagPrevious
            k = GetElemStr(Tags(i), "|", Tag)
            TagNovo = CLng(Tag(1))
            n = 1
            achou = False
            While (n < k) And (Not achou)
                n = n + 1
                QtdTag = .FieldOccCount(Mfn - 1, CLng(Tag(n)))
                If QtdTag > 0 Then
                    achou = True
                    novo = .FieldContentAllOccGet(Mfn - 1, CLng(Tag(n)), i)
                    'ret = ret And .fieldcontentadd(Mfn, CLng(Tag(n)), .FieldContentAllOccGet(Mfn - 1, CLng(Tag(n)), i))
                End If
            Wend
            If achou Then
                QtdTag = .FieldOccCount(Mfn, TagNovo)
                ret = .FieldContentUpdate(Mfn, TagNovo, novo, i)
                For n = 2 To QtdTag
                    ret = ret And .FieldContentUpdate(Mfn, TagNovo, .FieldContentAllOccGet(Mfn, TagNovo, 1), 1)
                Next
            End If
        Next
        For i = 1 To QtdTagPrevious
            ret = ret And .FieldContentDel(Mfn, ISISTAGS("previous").value, i)
        Next
    End If
    End With
    SetPrevious = ret
End Function

Function CheckISSN(Mfn As Long, ISSNDB As ClIsisDll, ISIDB As ClIsisDll) As Boolean
    Dim ret As Boolean
    Dim SertitleCount As Long
    Dim Sertitle() As String
    Dim ISSNCount As Long
    Dim ISSN() As String
    Dim SertitleMfnCount As Long
    Dim SertitleMfn() As Long
    Dim ISSNMfnCount As Long
    Dim ISSNMfn() As Long
    Dim MfnNOISSN As Long
    Dim TagISSN As Long
    Dim TagISSNinISSNDB As Long
    Dim TagISSNinISIDB As Long
    Dim TagISSNinTitle As Long
    Dim TagSertitle As Long
    Dim TagSertitleinISIDB As Long
    Dim TagSertitleinISSNDB As Long
    Dim TagSertitleinTitle As Long
    Dim i As Long
    Dim DataBase As ClIsisDll
    Dim NoSertitleDB As ClIsisDll
    
    TagISSNinISSNDB = ISISTAGS("ISSNinISSN01").value
    TagISSNinISIDB = ISISTAGS("ISSNinISI").value
    TagISSNinTitle = ISISTAGS("ISSNTitle").value
    
    TagSertitleinISIDB = ISISTAGS("sertitleinISSN01").value
    TagSertitleinISSNDB = ISISTAGS("sertitleinISI").value
    TagSertitleinTitle = ISISTAGS("sertitle").value
    
    ret = True
    With Isis
    If (Mfn > 0) And (Mfn <= .MfnQuantity) Then
        SertitleCount = .FieldContentGet(Mfn, ISISTAGS("stitle").value, Sertitle)
        ISSNCount = .FieldContentGet(Mfn, ISISTAGS("ISSN").value, ISSN)
        
        If (SertitleCount > 0) And (ISSNCount = 0) Then
            Sertitle(1) = ReplaceAllHTML(Sertitle(1))
            If SertitleCount > 1 Then Msg.GiveRunInformation ("Checking ISSN: There are more than one sertitle in the reference whose mfn is " + CStr(Mfn) + ".")
            'procura sertitle nas bases de issn (prioridade:issn01,isi,title)
            
            Set DataBase = New ClIsisDll
            SertitleMfnCount = ISIDB.MfnFind(Sertitle(1), SertitleMfn)
            If SertitleMfnCount > 0 Then
                Set DataBase = ISIDB
                TagISSN = TagISSNinISIDB
            Else
                SertitleMfnCount = DBTitle.BDTitle.MfnFind(Sertitle(1), SertitleMfn)
                If SertitleMfnCount > 0 Then
                    Set DataBase = DBTitle.BDTitle
                    TagISSN = TagISSNinTitle
                Else
                    SertitleMfnCount = ISSNDB.MfnFind(Sertitle(1), SertitleMfn)
                    If SertitleMfnCount > 0 Then
                        Set DataBase = ISSNDB
                        TagISSN = TagISSNinISSNDB
                    End If
                End If
            End If
            
            If SertitleMfnCount > 0 Then
                'obtem o Value do issn
                ISSNMfnCount = DataBase.FieldContentGet(SertitleMfn(1), TagISSN, ISSN)
                If ISSNMfnCount > 0 Then
                    'acrescenta na base
                    Call .FieldContentAdd(Mfn, ISISTAGS("ISSN").value, ISSN(1))
                    'procura o nome oficial
                    If DataBase Is ISSNDB Then
                        'procura nas outras bases
                        
                        ISSNMfnCount = DBTitle.BDTitle.MfnFind(ISSN(1), ISSNMfn)
                        If ISSNMfnCount > 0 Then
                            Set DataBase = DBTitle
                            TagSertitle = TagSertitleinTitle
                        Else
                            ISSNMfnCount = ISIDB.MfnFind(ISSN(1), ISSNMfn)
                            If ISSNMfnCount > 0 Then
                                Set DataBase = ISIDB
                                TagSertitle = TagSertitleinISIDB
                            Else
                                ISSNMfnCount = ISSNDB.MfnFind(ISSN(1), ISSNMfn)
                                TagSertitle = TagSertitleinISSNDB
                                If ISSNMfnCount > 0 Then
                                    SertitleCount = DataBase.FieldContentGet(ISSNMfn(1), TagSertitle, Sertitle)
                                Else
                                    Call Msg.GiveRunInformation("Checking ISSN: ISSN must be found anywhere.", True)
                                End If
                            End If
                        End If
                    End If
                    If SertitleCount > 0 Then Call .FieldContentAdd(Mfn, ISISTAGS("standardtitle").value, Sertitle(1))
                Else
                    'if nao existe issn
                    Msg.GiveRunInformation ("Checking ISSN: ISSN of the serial " + Sertitle(1) + " not found in Data Base of ISSN.")
                End If
            Else
                Msg.GiveRunInformation ("Checking ISSN: Title of the serial " + Sertitle(1) + " not found in Data Base of ISSN.")
                Paths("NoSertitleISSN").NotChecked = True
                If LoadIsisDB("NoSertitleISSN", NoSertitleDB) Then
                    If NoSertitleDB.MfnFind(Sertitle(1), SertitleMfn) = 0 Then
                        MfnNOISSN = NoSertitleDB.RecordSave(TagContents(Sertitle(1), ISISTAGS("stitle").value))
                        If MfnNOISSN > 0 Then Call NoSertitleDB.IfUpdate(MfnNOISSN, MfnNOISSN)
                    End If
                End If
                Set NoSertitleDB = Nothing
            End If
            Set DataBase = Nothing
        End If
    End If
    End With
    CheckISSN = ret
End Function


'-----------------------------------------------------------------------
'CheckOrder - verifica a DocOrder do documento
'DocName    - Nome do documento
'DocOrder   - Order do documento
'pii        - identificação do documento
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Function CheckOrder(DocName As String, DocOrder As String, pii As String) As Boolean
    Dim ord As String
    Dim QtdMfnOrder As Long
    Dim QtdMfnPii As Long
    Dim MfnOrder() As Long
    Dim MfnPii() As Long
    Dim MfnDocOrder As Long
    Dim MfnOthOrder As Long
    Dim ret As Boolean
       
    'QtdMfnOrder = Isis.MfnFind(DocOrder, MfnOrder)

    QtdMfnPii = Isis.MfnFind(pii, MfnPii)
    If QtdMfnPii = 1 Then
        DocOrder = Isis.FieldContentOccGet(MfnPii(1), ISISTAGS("order").value, 1)
        QtdMfnOrder = Isis.MfnFind(DocOrder, MfnOrder)
        If QtdMfnOrder <> 1 Then
            With FormOrder
            'Form para a correção de order
            .ComboOrd2.AddItem DocOrder
            .ComboOrd1.AddItem DocOrder
            .TxtArq2.Text = Isis.FieldContentOccGet(MfnPii(1), ISISTAGS("docfile").value, 1)
            If MfnOrder(1) = MfnPii(1) Then
                MfnDocOrder = MfnOrder(1)
                MfnOthOrder = MfnOrder(2)
            Else
                MfnOthOrder = MfnOrder(1)
                MfnDocOrder = MfnOrder(2)
            End If
            .TxtArq1.Text = Isis.FieldContentOccGet(MfnOthOrder, ISISTAGS("docfile").value, 1)
            .ComboOrd2.ListIndex = 0
            
            For QtdMfnOrder = 1 To QtdTotalDocs
                ord = "0" + CStr(QtdMfnOrder)
                ord = Mid(ord, Len(ord) - 1)
                If Isis.MfnFind(ord, MfnOrder) = 0 Then
                    .ComboOrd1.AddItem ord
                    .ComboOrd2.AddItem ord
                End If
            Next
            .ComboOrd1.Text = DocOrder
            
            .Show vbModal
            'Fim Form para a correção de order
            If .Feito Then
                ret = True
                If DocOrder <> .Ord1 Then
                    Call Isis.FieldContentUpdate(MfnOthOrder, CLng(ISISTAGS("order").value), .Ord1)
                    Call Isis.FieldContentUpdate(MfnOthOrder + 1, CLng(ISISTAGS("order").value), .Ord1)
                    Call Isis.IfUpdate(MfnOthOrder, MfnOthOrder)
                End If
                If DocOrder <> .Ord2 Then
                    Call Isis.FieldContentUpdate(MfnDocOrder, CLng(ISISTAGS("order").value), .Ord2)
                    Call Isis.FieldContentUpdate(MfnDocOrder + 1, CLng(ISISTAGS("order").value), .Ord2)
                    Call Isis.IfUpdate(MfnDocOrder, MfnDocOrder)
                End If
            Else
                ret = False
            End If
            End With
        Else
            ret = True
        End If
    Else
        Call Msg.GiveRunInformation("CheckOrder: number found of pii " + CStr(QtdMfnPii), True)
    End If

    CheckOrder = ret
End Function

'-----------------------------------------------------------------------
'DocExist    - verifica a existência de um documento
'pii    - identificação do documento
'RegIni - primeiro registro do documento
'QtdRegistros   - Quantidade de Records
'Retorno    - verdadeiro ou falso
'-----------------------------------------------------------------------
Function DocExist(pii As String, RegIni As Long, QtdRegistros As Long) As Boolean
    Dim Mfn As Long
    Dim vMfn() As Long
    Dim i As Long
    Dim q As String
    Dim Q1 As Long
    Dim ret As Boolean
    Dim DataBase As New ClIsisDll

    If DataBase.Inicia(DBPath, DBName, "Document Database") Then
        If DataBase.IfCreate(DBName) Then
            i = DataBase.MfnFind(pii, vMfn)
            If i > 0 Then
                ' para obter o Mfn do registro outline
                Mfn = vMfn(i) - 1
                q = DataBase.FieldContentOccGet(Mfn, ISISTAGS("reccount").value, 1)
                If Len(q) > 0 Then Q1 = CLng(q)
            End If
            ret = (Mfn > 0) And (Q1 > 0)
            RegIni = Mfn
            QtdRegistros = Q1
        End If
    End If
    DocExist = ret
End Function

'-----------------------------------------------------------------------
'GarbageCollection - elimina os Records vazios
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Function GarbageCollection() As Boolean
    GarbageCollection = Isis.BDColetaLixo
End Function

Private Sub Class_Initialize()
    Set Isis = New ClIsisDll
End Sub

Private Sub Class_Terminate()
    Set Isis = Nothing
End Sub

Function CheckConfiguration(pii As String) As Boolean
    Dim ret As Boolean
    Dim IssueMfnCount As Long
    Dim xIssueMfn() As Long
    Dim IssueMfn As Long
    Dim ChDoc As String
    Dim xDocMfn() As Long
    Dim DocMfn As Long
    Dim order As Long
    Dim aux As String
    Dim q As Long
    Dim DocCount As Long
    
    Call Msg.GiveRunInformation(DocName + ": Checking Configuration of Document.")
    
    If ConfigRecordExist Then
        IssueMfn = 1
    
        If DocExist(pii, DocMfn, q) Then
            If DocMfn > 0 Then DocMfn = DocMfn + 1
        Else
            Call Msg.GiveRunInformation(DocName + ": Missing document " + pii)
        End If
    Else
        Call Msg.GiveRunInformation(DocName + ": Configuration record is missing.")
    End If
    
    If (IssueMfn > 0) And (DocMfn > 0) Then
        aux = Isis.FieldContentOccGet(IssueMfn, ISISTAGS("doccount").value, 1)
        If IsNumber(aux) Then DocCount = CLng(aux)
        
        aux = Isis.FieldContentOccGet(DocMfn, ISISTAGS("order").value, 1)
        If IsNumber(aux) Then order = CLng(aux)
        If (order > 0) And (order <= DocCount) Then
            ret = True
        Else
            Call Msg.GiveRunInformation(DocName + ": Invalid value for order in document " + CStr(order) + ". It must be in the range of 1-" + CStr(DocCount) + ".")
        End If
        Call LetValuesForComparing("Order", "in the range of [1-" + CStr(DocCount) + "]", aux)
        
        ValuesForCheckingCount = 0
        Erase Labels
        Erase ValueInIssueRecord
        Erase ValueInDocument
        
        ret = ret And CheckConfigurationSeccode(IssueMfn, DocMfn)
        ret = ret And CheckConfigurationField("Issue Short title", ISISTAGS("stitle").value, IssueMfn, DocMfn)
        ret = ret And CheckConfigurationField("ISSN", ISISTAGS("ISSN").value, IssueMfn, DocMfn)
        ret = ret And CheckConfigurationField("Status", ISISTAGS("Status").value, IssueMfn, DocMfn)
        ret = ret And CheckConfigurationField("Date", ISISTAGS("DateISO").value, IssueMfn, DocMfn)
    End If
    CheckConfiguration = ret
End Function

Function CheckConfigurationRecord(DocId As String) As Boolean
    Dim ret As Boolean
    Dim IssueMfnCount As Long
    Dim xIssueMfn() As Long
    Dim IssueMfn As Long
    Dim ChDoc As String
    Dim xDocMfn() As Long
    Dim DocMfn As Long
    Dim order As Long
    Dim aux As String
    Dim q As Long
    Dim DocCount As Long
    
    Call Msg.GiveRunInformation(DocId + ": Checking Configuration of Document.")
    
    If ConfigRecordExist Then
        IssueMfn = 1
    
        If DocExist(DocId, DocMfn, q) Then
            If DocMfn > 0 Then DocMfn = DocMfn + 1
        Else
            Call Msg.GiveRunInformation(DocId + ": Missing document " + DocId)
        End If
    Else
        Call Msg.GiveRunInformation(DocId + ": Configuration record is missing.")
    End If
    
    If (IssueMfn > 0) And (DocMfn > 0) Then
        aux = Isis.FieldContentOccGet(IssueMfn, ISISTAGS("doccount").value, 1)
        If IsNumber(aux) Then DocCount = CLng(aux)
        
        aux = Isis.FieldContentOccGet(DocMfn, ISISTAGS("order").value, 1)
        If IsNumber(aux) Then order = CLng(aux)
        If (order > 0) And (order <= DocCount) Then
            ret = True
        Else
            Call Msg.GiveRunInformation(DocId + ": Invalid value for order in document " + CStr(order) + ". It must be in  [1-" + CStr(DocCount) + "].")
        End If
        
        ret = ret And CheckSeccode(IssueMfn, DocMfn)
        ret = ret And CheckField("Issue Short title", ISISTAGS("stitle").value, IssueMfn, DocMfn)
        ret = ret And CheckField("ISSN", ISISTAGS("ISSN").value, IssueMfn, DocMfn)
        ret = ret And CheckField("Status", ISISTAGS("Status").value, IssueMfn, DocMfn)
        ret = ret And CheckField("Date", ISISTAGS("DateISO").value, IssueMfn, DocMfn)
    End If
    CheckConfigurationRecord = ret
End Function


