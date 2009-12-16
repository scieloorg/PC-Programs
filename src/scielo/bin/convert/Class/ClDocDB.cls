VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClDBDoc"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

Public Records As ColRegistro  'local copy
Private DBPath As String 'local copy
Private dbname As String 'local copy


'Public Isis As ClIsisDll 'local copy

Public Property Get fullpath() As String
    fullpath = DBPath + PathSep + dbname
End Property

'-----------------------------------------------------------------------
'Initiate - Initiate a base de dados de documentos
'Path   - caminho da base
'FileName   - FileName do arquivo da base
'Retorno        - sucesso ou fracasso
'-----------------------------------------------------------------------
Function Initiate(Path As String, filename As String, Label As String) As Boolean
    Dim ret As Boolean
    
    'Call articleDAO.setData(Path, fileName, Label)
    
    
 '   If isis.Initiate(dbPath, dbName, "Doc DB") Then
        'If Not FileExist(Path + PathSep + FileName + ".fst", "fst file of " + ConvertdirTree.DirNodes("Database Directory").label) Then Call FileCopy(PathParser + PathSep + parser.DTDName + ".fst", Path + PathSep + FileName + ".fst")
 '       If isis.IfCreate(dbName) Then
 '           If Isis.MfnQuantity > 0 Then Call Isis.IfUpdate(1, Isis.MfnQuantity)
 '           ret = True
            DBPath = Path
            dbname = filename
            'IfName = FileName
 '       End If
 '   End If
    ret = True
    Initiate = ret
End Function

'-----------------------------------------------------------------------
'RecordDel    - apagar uma quantidade de Records a partir do Mfn inicial
'MfnINI    - mfn inicial
'qtd    - quantidade atualizada
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Private Function RecordDel(MfnIni As Long, Qtd As Long) As Boolean
    Dim Mfn As Long
    Dim fim As Long
    Dim ret As Boolean
    Dim i As Long
    Dim isis As ClIsisDll
    
    Set isis = New ClIsisDll
    If isis.Initiate(DBPath, dbname, "Doc DB") Then
        If isis.IfCreate(dbname) Then
    
            fim = MfnIni + Qtd - 1
            Mfn = MfnIni - 1
            ret = True
            While (Mfn < fim) And ret
                Mfn = Mfn + 1
                If isis.RecordDel(Mfn) Then
                    ret = isis.IfUpdate(Mfn, Mfn)
                End If
            Wend
        End If
    End If
    ret = ret And (Mfn = fim)
    Set isis = Nothing
    RecordDel = ret
End Function

'-----------------------------------------------------------------------
'DocDel  - apaga um documento
'DOCId        - identificação do documento
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Function DOCDel(DocId As String) As Boolean
    Dim ini As Long
    Dim fim As Long
    Dim Qtd As Long
    Dim ret As Boolean
    Dim isis As ClIsisDll
        
    If DOCExist(DocId, ini, Qtd) Then
        fim = ini + Qtd - 1
        If RecordDel(ini, Qtd) Then
            Set isis = New ClIsisDll
            If isis.Initiate(DBPath, dbname, "Doc DB") Then
                If isis.IfCreate(dbname, "Doc DB") Then
                    ret = isis.IfUpdate(ini, fim)
                End If
            End If
            Set isis = Nothing
        End If
    End If
    
    DOCDel = ret
End Function


Private Function ISSNCheck(Mfn As Long, ISSNBASES As ColISSNDB, NOSERTITLE As ClISSNDB) As Boolean
    Dim ret As Boolean
    Dim Sertitle_tofind As String
    Dim ISSNCount As Long
    Dim issn As String
    Dim ISSNMfnCount As Long
    Dim ISSNMfn() As Long
    Dim ISSNDB As ClISSNDB
    Dim StandardSertitle As String
    Dim i As Long
    Dim found As Boolean
    Dim isis As ClIsisDll
    
    Set isis = New ClIsisDll
    With isis
    If .Initiate(DBPath, dbname, "Doc DB") Then
        If .IfCreate(dbname, "Doc DB") Then
            
            Sertitle_tofind = .FieldContentOccGet(Mfn, BV(Currbv).BVISISTAGS("stitle").Value, 1)
            issn = .FieldContentOccGet(Mfn, BV(Currbv).BVISISTAGS("ISSN").Value, 1)
            
            If (Len(Sertitle_tofind) > 0) And (Len(issn) = 0) Then
                Sertitle_tofind = RmAllHTML(Sertitle_tofind)
            
                Set ISSNDB = New ClISSNDB
                
                i = 0
                While (i < ISSNBASES.Count) And (Len(issn) = 0)
                    i = i + 1
                    Set ISSNDB = ISSNBASES(i)
                    found = ISSNDB.MatchISSN1(Sertitle_tofind, StandardSertitle, issn)
                Wend
                Set ISSNDB = Nothing
                
                If found Then
                    Call .FieldContentAdd(Mfn, BV(Currbv).BVISISTAGS("ISSN").Value, issn)
                    Call .FieldContentAdd(Mfn, BV(Currbv).BVISISTAGS("standardtitle").Value, StandardSertitle)
                Else
                    'if nao existe issn
                    
                    NOSERTITLE.AddTitleWithoutISSN (Sertitle_tofind)
                    
                End If
                
            End If
        End If
    End If
    
    End With
    Set isis = Nothing
    ISSNCheck = ret
End Function

'-----------------------------------------------------------------------
'DocExist    - verifica a existência de um documento
'DOCId    - identificação do documento
'RegIni - primeiro registro do documento
'QtdRegistros   - Quantidade de Records
'Retorno    - verdadeiro ou falso
'-----------------------------------------------------------------------
Private Function DOCExist(DocId As String, RegIni As Long, QtdRegistros As Long) As Boolean
    Dim Mfn As Long
    Dim vMfn() As Long
    Dim i As Long
    Dim q As String
    Dim q1 As Long
    Dim ret As Boolean
    Dim isis As ClIsisDll
    
    Set isis = New ClIsisDll
    If isis.Initiate(DBPath, dbname, "Doc DB") Then
        If isis.IfCreate(dbname, "Doc DB") Then
        
            i = isis.MfnFind(DocId, vMfn)
            If i > 0 Then
                
                Mfn = vMfn(1) - 1
                q = isis.FieldContentOccGet(Mfn, COMMONISISTAGS("totaldocrec").Value, 1)
                If Len(q) > 0 Then q1 = CLng(q)
            End If
        End If
    End If
    
    Set isis = Nothing
    
    ret = (Mfn > 0) And (q1 > 0)
    RegIni = Mfn
    QtdRegistros = q1
   
    DOCExist = ret
End Function

Private Sub Class_Initialize()
    Set Records = New ColRegistro
End Sub

Private Sub Class_Terminate()
    Set Records = Nothing
End Sub

Function CfgRecImport(ConfigRecord As String) As Boolean
    Dim isis As ClIsisDll
    Dim ret As Boolean
    
    If Len(ConfigRecord) > 0 Then
        Set isis = New ClIsisDll
        If isis.Initiate(DBPath, dbname, "Doc DB") Then
            If isis.IfCreate(dbname, "Doc DB") Then
                If isis.RecordUpdate(1, ConfigRecord) Then
                    ret = isis.IfUpdate(1, 1)
                End If
            End If
        End If
        Set isis = Nothing
    End If
    CfgRecImport = ret
End Function

Function DBDel() As Boolean
    Dim ret As Boolean
    Dim isis As ClIsisDll
    
    Set isis = New ClIsisDll
    If isis.Initiate(DBPath, dbname, "Doc DB", True) Then
        If isis.IfCreate(dbname, "Doc DB", True) Then
            ret = True
        End If
    End If
    Set isis = Nothing
    DBDel = ret
End Function

Private Function Convert2ISO() As Boolean
    Dim ret As Boolean
    Dim isis As ClIsisDll
    
    Msg.GiveRunInformation ("iso start.")
    Set isis = New ClIsisDll
    If isis.Initiate(DBPath, dbname, "Doc DB") Then
        If isis.IfCreate(dbname, "Doc DB") Then
            ret = isis.BDConvert2ISO
        End If
    End If
    Set isis = Nothing
    Msg.GiveRunInformation ("iso end.")
    Convert2ISO = ret
End Function

Private Function DBRemoveDeletedRecords() As Boolean
    Dim ret As Boolean
    Dim isis As ClIsisDll
    
    Set isis = New ClIsisDll
    If isis.Initiate(DBPath, dbname, "Doc DB") Then
        If isis.IfCreate(dbname, "Doc DB") Then
            ret = isis.BDClean
        End If
    End If
    Set isis = Nothing
    DBRemoveDeletedRecords = ret
End Function
'-----------------------------------------------------------------------
'DOCSave - Save the document in the database
'DOCId   - Identification of the document
'Return <True> - success and <False> - failure
'-----------------------------------------------------------------------
Function DOCSave(DocId As String) As Boolean
    Dim init As Long
    Dim RangeSize As Long
    Dim ret As Boolean
    Dim i As Long
    Dim Mfn As Long
    Dim DatabaseName As String
    Dim percent As Double
    Dim recidx As Long
    Dim pages As String
    Dim p As Long
    Dim p2 As Long
    Dim isis As ClIsisDll
    Dim NewRangeInit As Long
    Dim NewRangeEnd As Long
    Dim NewRangeSize As Long
        
    
    Msg.GiveRunInformation (InterfaceLabels("MsgRecordingdata").elem2)
    
    If DOCExist(DocId, init, RangeSize) Then
                
        NewRangeInit = init
        NewRangeEnd = init + RangeSize - 1
        NewRangeSize = RangeSize
        
        If RecordDel(init, RangeSize) Then
            Set isis = New ClIsisDll
            If isis.Initiate(DBPath, dbname, "Doc DB") Then
                If isis.IfCreate(dbname, "Doc DB") Then
                    If isis.AmpliarIntervaloLivre(NewRangeInit, NewRangeEnd) Then NewRangeSize = NewRangeEnd - NewRangeInit + 1
                    If NewRangeSize < Records.Count Then
                        EXISTDELETEDRECORDS = True
                        'nao possui registros suficientes para gravar o documento
                        If NewRangeEnd + 1 <= isis.MfnQuantity Then
                            NewRangeInit = isis.MfnQuantity + 1
                        End If
                    ElseIf NewRangeSize > Records.Count Then
                        EXISTDELETEDRECORDS = True
                    End If
                End If
            End If
        End If
    Else
        Set isis = New ClIsisDll
        If isis.Initiate(DBPath, dbname, "Doc DB") Then
            If isis.IfCreate(dbname, "Doc DB") Then
                NewRangeInit = isis.MfnQuantity + 1
            End If
        End If
    End If
                
    percent = 100 / Records.Count
    DatabaseName = isis.TagContents(dbname, COMMONISISTAGS("database").Value)
            
    recidx = 0
    Mfn = NewRangeInit
    ret = True
        
    While (recidx < Records.Count) And ret
    
        recidx = recidx + 1
    Debug.Print DatabaseName + Records(recidx).conteudo
        If Mfn > isis.MfnQuantity Then
            Mfn = isis.RecordSave(DatabaseName + Records(recidx).conteudo)
            ret = (Mfn > 0)
        Else
            ret = isis.RecordUpdate(Mfn, DatabaseName + Records(recidx).conteudo)
        End If
        Mfn = Mfn + 1
        ShowMsgInForm (CStr(CInt(recidx * percent)) + "% loaded.")
    Wend
    Call isis.FieldContentAdd(NewRangeInit, COMMONISISTAGS("totaldocrec").Value, CStr(Records.Count))
    If (recidx = Records.Count) Then ret = isis.IfUpdate(NewRangeInit, Mfn)
            
    Set isis = Nothing
    Set Records = Nothing
    
    'If ret Then Call ChangeReferencesFieldContent(DOCId)
    DOCSave = ret
End Function


'-----------------------------------------------------------------------
'AfterSaving    - substitui nos Records de um documento o traço que indica previous pelo nome do autor
'DOCId        - identificação do documento
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Private Sub SetPrevious()
    Dim i As Long
    Dim q As Long
    Dim Mfns() As Long
    Dim Mfn As Long
    Dim isis As ClIsisDll
    Dim flags As String
    Dim j As Long
    Dim k As Long
    Dim NewTag As Long
    Dim Tag() As String
    Dim PreviousTagCount As Long
    Dim ret As Boolean
    Dim n As Long
    Dim Tags() As String
    Dim achou As Boolean
    Dim novo As String
    Dim QtdTag As Long
    Dim proc As String
    
                
            
    Set isis = New ClIsisDll
    If isis.Initiate(DBPath, dbname, "Doc DB") Then
        If isis.IfCreate(dbname, "Doc DB") Then
            q = isis.MfnFind(CONST_CHANGE_FIELDS_PREVIOUS, Mfns)
            If q > 0 Then
                Call Msg.GiveRunInformation(InterfaceLabels("MsgSettingPrevious").elem2, , True)

                For i = 1 To q
                    Mfn = Mfns(i)
                    'previous author
                
                    With isis
                    ret = True
                    PreviousTagCount = .FieldContentGet(Mfn, BV(Currbv).BVISISTAGS("previous").Value, Tags)
                    For j = 1 To PreviousTagCount
                        k = GetElemStr(Tags(j), "|", Tag)
                        NewTag = CLng(Tag(1))
                        n = 1
                        achou = False
                        While (n < k) And (Not achou)
                            n = n + 1
                            QtdTag = .FieldOccCount(Mfn - 1, CLng(Tag(n)))
                            If QtdTag > 0 Then
                                achou = True
                                novo = .FieldContentAllOccGet(Mfn - 1, CLng(Tag(n)), j)
                                'ret = ret And .fieldcontentadd(Mfn, CLng(Tag(n)), .FieldContentAllOccGet(Mfn - 1, CLng(Tag(n)), i))
                            End If
                        Wend
                        If achou Then
                            QtdTag = .FieldOccCount(Mfn, NewTag)
                            ret = .FieldContentUpdate(Mfn, NewTag, novo, j)
                            For n = 2 To QtdTag
                                ret = ret And .FieldContentUpdate(Mfn, NewTag, .FieldContentAllOccGet(Mfn, NewTag, 1), 1)
                            Next
                            proc = isis.UsePft(Mfn, "(if v710<>'1' then |a710{|v710|{| fi)")
                            Call isis.UseProc(Mfn, "d710" + proc)
                        End If
                    Next
                    For j = 1 To PreviousTagCount
                        ret = ret And .FieldContentDel(Mfn, BV(Currbv).BVISISTAGS("previous").Value, j)
                    Next
                    End With
                    Call isis.IfUpdate(Mfn, Mfn)
                Next
            End If
        End If
    End If
    Set isis = Nothing
End Sub


Private Sub ISSNSet()
    Dim isis As ClIsisDll
    Dim i As Long
    Dim q As Long
    Dim Mfns() As Long
    Dim Mfn As Long
    Dim issn As String
    Dim proc As String
    Dim refcount As Long
    Dim ISSNBASES As ColISSNDB
    Dim NOSERTITLE As ClISSNDB
    Dim found As Boolean

    'Dim isis As ClIsisDll
    Dim j As Long
    Dim ret As Boolean
    Dim Sertitle_tofind As String
    Dim ISSNCount As Long
    'Dim issn As String
    Dim ISSNMfnCount As Long
    Dim ISSNMfn() As Long
    Dim ISSNDB As ClISSNDB
    Dim StandardSertitle As String
    

    Set isis = New ClIsisDll
    
    With isis
    If .Initiate(DBPath, dbname, "Doc DB") Then
        If .IfCreate(dbname, "Doc DB") Then
            q = .MfnFind(CONST_CHANGE_FIELDS_ISSN, Mfns)
            If q > 0 Then
                Call Msg.GiveRunInformation(InterfaceLabels("MsgSettingISSN").elem2, , True)
            
                Set ISSNBASES = New ColISSNDB
                Set NOSERTITLE = New ClISSNDB
                If ReadISSNFILE(ISSNBASES, NOSERTITLE) Then
                    
                End If
            End If
            
            FormMarkup.ProgressBar1.Visible = True
            For i = 1 To q
                Mfn = Mfns(i)
                
                FormMarkup.ProgressBar1.Value = ((i / q) * FormMarkup.ProgressBar1.Max)
                Sertitle_tofind = .FieldContentOccGet(Mfn, BV(Currbv).BVISISTAGS("stitle").Value, 1)
                issn = .FieldContentOccGet(Mfn, BV(Currbv).BVISISTAGS("ISSN").Value, 1)
                
                If (Len(Sertitle_tofind) > 0) And (Len(issn) = 0) Then
                    Sertitle_tofind = RmAllHTML(Sertitle_tofind)
                    j = 0
                    While (j < ISSNBASES.Count) And (Len(issn) = 0)
                        j = j + 1
                        Set ISSNDB = New ClISSNDB
                        Set ISSNDB = ISSNBASES(j)
                        found = ISSNDB.MatchISSN1(Sertitle_tofind, StandardSertitle, issn)
                        Set ISSNDB = Nothing
                    Wend
                        
                    If found Then
                        Call .FieldContentAdd(Mfn, BV(Currbv).BVISISTAGS("ISSN").Value, issn)
                        Call .FieldContentAdd(Mfn, BV(Currbv).BVISISTAGS("standardtitle").Value, StandardSertitle)
                        proc = .UsePft(Mfn, "(if v710<>'2' then |a710{|v710|{| fi)")
                        Call .UseProc(Mfn, "d710")
                        If Len(proc) > 0 Then
                            Call .UseProc(Mfn, proc)
                        End If
                    Else
                        NOSERTITLE.AddTitleWithoutISSN (Sertitle_tofind)
                    End If
                    Call .IfUpdate(Mfn, Mfn)
                End If
            Next
            FormMarkup.ProgressBar1.Visible = False
            If q > 0 Then
                Call Msg.GiveRunInformation(InterfaceLabels("MsgEndofSettingISSN").elem2, , True)
                Set ISSNBASES = Nothing
                Set NOSERTITLE = Nothing
            End If
                
        End If
    End If
    End With
    Set isis = Nothing
End Sub



Sub FinishDocConversion()  '(TransSymbolPath As String, TransSymbolFile As String)
    Dim pts As ClPTSDB
    Dim iso As ClISODB
    Dim drv As String
    Dim Path As String
    
    
    If BV(Currbv).Flag_PreviousAuthor = "1" Then SetPrevious
    If BV(Currbv).Flag_ISSN = "1" Then ISSNSet
    
    If BV(Currbv).Flag_ISODB = "1" Then
        Convert2ISO
    Else
        If EXISTDELETEDRECORDS Then DBRemoveDeletedRecords
    End If
        
    Set iso = New ClISODB
    Call iso.ISOUpdate(GetDatabaseId, Mid(DBPath, 1, 2), Mid(DBPath, 4), dbname)
    Set iso = Nothing
    
    
    Set pts = New ClPTSDB
    Call pts.PTSUpdate(GetConversionInfo)
    Set pts = Nothing
    
    Call Msg.GiveRunInformation("", , True)
        
End Sub




'----------------------------------------------------------------------
'ImportCfgRecordContent  - Get issue record from the issue database and store it on <CfgRecord>
'CfgRecId    - the identification of the issue whose record will be gotten
'Return - <True> to sucess; <False> to failure
'----------------------------------------------------------------------
Function ImportCfgRecordContent(pft As String) As String
    Dim content As String
    Dim q As Long
    Dim CfgRecMfn() As Long
    Dim isis  As ClIsisDll
    
    Set isis = New ClIsisDll
    If isis.Initiate(DBPath, dbname, "Doc DB") Then
        content = isis.UsePft(1, pft)
    End If
    
    Set isis = Nothing
    ImportCfgRecordContent = content
End Function


Function GetConversionInfo() As String
    Dim isis As ClIsisDll
    Dim Mfn As Long
    Dim eventdata As String
    Dim drv As String
    Dim Path As String
    Dim name As String
    Dim PathBase As String
    Dim p As Long
    
    Set isis = New ClIsisDll
    
    With isis
    If .Initiate(DBPath, dbname, "Doc DB") Then
        If .IfCreate(dbname, "Doc DB") Then
            If Len(BV(Currbv).Directory.ReturnCfgRecKey) > 0 Then
                Mfn = 1
            Else
                Mfn = 2
            End If
            eventdata = .UsePft(Mfn, "@" + BV(Currbv).FileTree.DirNodes("pts pft file").fullpath + "\" + BV(Currbv).FileTree.DirNodes("pts pft file").text)
            eventdata = eventdata + .TagContents(GetDateISO(Date), 301)
            eventdata = eventdata + .TagContents(GetTimeISO(Time), 302)
            
            PathBase = DBPath + PathSep + dbname
            p = InStr(PathBase, ":")
            If p > 0 Then
                drv = Mid(PathBase, 1, p)
                name = Mid(PathBase, p + 1)
                p = InStr(name, "\")
                While p > 0
                    Path = Path + Mid(name, 1, p)
                    name = Mid(name, p + 1)
                    p = InStr(name, "\")
                Wend
            End If
            eventdata = eventdata + .TagContents(drv, 500)
            eventdata = eventdata + .TagContents(Mid(Path, 1, Len(Path) - 1), 501)
            eventdata = eventdata + .TagContents(name, 502)
            
        End If
    End If
    End With
    Set isis = Nothing
    GetConversionInfo = eventdata
End Function


Function GetDatabaseId() As String
    Dim isis As ClIsisDll
    Dim Mfn As Long
    Dim Id As String
    
    Set isis = New ClIsisDll
    
    With isis
    If .Initiate(DBPath, dbname, "") Then
        If .IfCreate(dbname, "") Then
            If BV(Currbv).Flag_CfgRecInDB = "1" Then
                Mfn = 1
            Else
                Mfn = 2
            End If
            Id = .UsePft(Mfn, BV(Currbv).DatabaseId)
        End If
    End If
    End With
    Set isis = Nothing
    GetDatabaseId = Id
End Function
