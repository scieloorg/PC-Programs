Attribute VB_Name = "ModGlobal"
Option Explicit

Public Const SECTION_SEP = "%"
Public Const LIMIT_MFN = 200
'Uso de isisdll
Public AppHandle    As Long
Public Const delim1 = "<"
Public Const delim2 = ">"
Public Const pathsep = "\"

Public issueidparts As New ColCode
    
Public ConfigLabels As ClLabels
Public Fields As ColFields
Public Months As ColIdiomMeses
Public idiomsinfo As ColIdiom

'Variaveis de configuracao
Public SciELOPath As String
Public VolSiglum As String
Public NoSiglum As String
Public SupplVolSiglum  As String
Public SupplNoSiglum  As String
Public BrowserPath  As String
Public CurrIdiomHelp As String
Public IssueCloseDenied As Integer
Public TitleCloseDenied As Integer
Public PathsConfigurationFile As String

Public Paths As ColFileInfo


'Public IdiomHelp   As ColIdiom
Public Msg As New ClMsg
Public SepLinha As String


Public NodeFatherKey() As String
Public NodeChild() As String
Public NodeInfo() As String
Public FileNotRequired() As Boolean
Public Counter As Long

Public codeLIcense As ColCode
Public CodeStudyArea As ColCode
Public CodeAlphabet As ColCode
Public CodeLiteratureType As ColCode
Public CodeTreatLevel As ColCode
Public CodePubLevel As ColCode
Public CodeFrequency As ColCode
Public codeStatus As ColCode
Public codeHistory As ColCode
Public CodeTxtLanguage As ColCode
Public CodeAbstLanguage As ColCode
Public CodeCountry As ColCode
Public CodeState As ColCode
Public CodeUsersubscription As ColCode
Public CodePublishingModel As ColCode

Public CodeFTP As ColCode
Public CodeCCode As ColCode
Public CodeIdxRange As ColCode
Public CodeStandard As ColCode
Public CodeScheme As ColCode
Public CodeIssStatus As ColCode
Public CodeIdiom As ColCode
Public CodeTOC As ColCode
Public CodeScieloNet As ColCode
Public wok_subjects As ColCode

Public journal As ClsJournal

Public ErrorMessages As ClsErrorMessages

Public isisfn As Long



Property Get NotRequiredFile(i As Long) As Boolean
    NotRequiredFile = FileNotRequired(i)
End Property

Function TagContent(ByVal conteudo As String, ByVal tag As Long) As String
    Dim ComTag As String
    
    If tag = 0 Then
        MsgBox "TagContent: tag=0. Conteudo=" + conteudo
    ElseIf conteudo = "" Then
        'MsgBox "TagContent: Conteudo=" + conteudo
    Else
        conteudo = RmNewLineInStr(conteudo)
        ComTag = delim1 + CStr(tag) + delim2 + conteudo + delim1 + "/" + CStr(tag) + delim2 + SepLinha
    End If
    TagContent = ComTag
End Function

Function TagSubf(ByVal conteudo As String, ByVal subf As String) As String
    If conteudo <> "" Then TagSubf = "^" + subf + conteudo
End Function


Private Sub Main()
    Dim CodeDB As ClFileInfo
    Dim codedao As New ClsCodesDAO
    Dim fn_wok As Long
    
    fn_wok = FreeFile(4)
    isisfn = FreeFile
    
    Open App.Path + "\isis.log" For Output As isisfn
    
    AppHandle = IsisAppNew()
    Call IsisAppDebug(AppHandle, DEBUG_LIGHT)
    
    SepLinha = Chr(13) + Chr(10)
    If ConfigGet Then
        Set wok_subjects = New ColCode
        Dim c As ClCode
        Dim s As String
        
        Open App.Path + "\subjects_categories_wok.csv" For Input As #fn_wok
        While Not EOF(fn_wok)
            Line Input #fn_wok, s
            Set c = New ClCode
            c.Code = Trim(s)
            c.value = Trim(s)
            c.index = wok_subjects.count + 1
            Call wok_subjects.add(c, c.index)
        Wend
        Close #fn_wok
        
        
        ChangeInterfaceIdiom = CurrIdiomHelp
        Set CodeDB = Paths("NewCode Database")
        Call codedao.create(CodeDB.Path, CodeDB.FileName, CodeDB.key)
        Call codedao.getTable("", "ccode", CodeCCode)
    
        
        Set CodeDB = Paths("Code Database")
        Call codedao.create(CodeDB.Path, CodeDB.FileName, CodeDB.key)
        Call codedao.getTable("", "standard", CodeStandard)
        Call codedao.getTable("", "scielonet", CodeScieloNet)
        
        Set ErrorMessages = New ClsErrorMessages
        ErrorMessages.load ("langs\" + CurrIdiomHelp + "_err.txt")
        
        Set Months = New ColIdiomMeses
        Months.ReadMonthTable
    
        
        
        FormMenuPrin.OpenMenu
        
        Set journalDAO = New ClsJournalDAO
        
        
        
        'FormConfig.Show vbModal
    End If
    
    
End Sub

Function ConfigGet() As Boolean
    Dim fn As Long
    Dim key As String
    
    
    fn = FreeFile
    Open App.Path + "\scipath.ini" For Input As fn
    Input #fn, SciELOPath
    Close fn
    
    fn = FreeFile(1)
    Open App.Path + "\value.ini" For Input As fn
    'Input #fn, Key, SciELOPath
    Input #fn, key, VolSiglum
    Input #fn, key, NoSiglum
    Input #fn, key, SupplVolSiglum
    Input #fn, key, SupplNoSiglum
    Input #fn, key, BrowserPath
    Input #fn, key, CurrIdiomHelp
    Input #fn, key, IssueCloseDenied
    Input #fn, key, TitleCloseDenied
    Input #fn, key, PathsConfigurationFile
    Close fn


    ConfigGet = True
End Function


Sub ConfigSet()
    Dim fn As Long
    
    fn = FreeFile(1)
    Open "value.ini" For Output As fn
'    Write #fn, "SciELOPath", SciELOPath
    Write #fn, "SglVol", VolSiglum
    Write #fn, "SglNo", NoSiglum
    Write #fn, "SglVolSuppl", SupplVolSiglum
    Write #fn, "SglNoSuppl", SupplNoSiglum
    Write #fn, "BrowserPath", BrowserPath
    Write #fn, "CurrIdiomHelp", CurrIdiomHelp
    Write #fn, "IssueCloseDenied", IssueCloseDenied
    Write #fn, "TitleCloseDenied", TitleCloseDenied
    Write #fn, "PathsConfigurationFile", PathsConfigurationFile
    Close fn
End Sub

Function CheckDateISO(Issue_DateISO As String) As Boolean
    Dim Ret As Boolean
    Dim Data As Date
    Dim dia1 As String
    Dim mes1 As String
    Dim ano1 As String
    Dim dia2 As String
    Dim mes2 As String
    Dim ano2 As String
    
    If Len(Issue_DateISO) <> 8 Then
        
    Else
        dia1 = Mid(Issue_DateISO, 7, 2)
        mes1 = Mid(Issue_DateISO, 5, 2)
        ano1 = Mid(Issue_DateISO, 1, 4)
        
        If (CLng(dia1) > 31) And (CLng(dia1) < 0) Then
            'MsgBox ("Invalid day")
        ElseIf (CLng(mes1) > 12) And (CLng(mes1) < 0) Then
            'MsgBox ("Invalid month.")
        Else
            Ret = True
        End If
    End If
    If Not Ret Then MsgBox ConfigLabels.getLabel("MsgInvalidDATEISO"), vbCritical
    CheckDateISO = Ret
End Function




Function issueId(vol As String, supplvol As String, Num As String, SupplNum As String, part As String) As String
    Dim Ret As String
    
    If Len(vol) > 0 Then Ret = Ret + VolSiglum + vol
    If Len(supplvol) > 0 Then Ret = Ret + SupplVolSiglum + supplvol
    If Len(Num) > 0 Then Ret = Ret + NoSiglum + Num
    If Len(SupplNum) > 0 Then Ret = Ret + SupplNoSiglum + SupplNum
    If Len(part) > 0 Then Ret = Ret + part
    
    issueId = Ret
End Function
Function IssueKey(vol As String, supplvol As String, Num As String, SupplNum As String) As String
    Dim Ret As String
    
    Ret = Ret + VolSiglum + vol
    Ret = Ret + SupplVolSiglum + supplvol
    Ret = Ret + NoSiglum + Num
    Ret = Ret + SupplNoSiglum + SupplNum
    
    IssueKey = Ret
End Function

Function MsgIssueId(vol As String, supplvol As String, Num As String, SupplNum As String, iseqno As String) As String
    Dim Ret As String
    
    If Len(vol) > 0 Then Ret = Ret + "Volume = " + vol + SepLinha
    If Len(supplvol) > 0 Then Ret = Ret + "Volume Suppl = " + supplvol + SepLinha
    If Len(Num) > 0 Then Ret = Ret + "Number = " + Num + SepLinha
    If Len(SupplNum) > 0 Then Ret = Ret + "Number Suppl = " + SupplNum + SepLinha
    If Len(iseqno) > 0 Then Ret = Ret + "Seq. Number = " + iseqno + SepLinha
    MsgIssueId = Ret
End Function




Sub LoadCodes(CodeDB As ClFileInfo, idiom As String, key As String, Code As ColCode, Optional codeEqualValue As Boolean = False)
    Dim isisCode As ClIsisdll
    Dim Mfn As Long
    Dim mfns() As Long
    Dim q As Long
    Dim i As Long
    Dim aux As String
    Dim a_codes() As String
    Dim a_values() As String
    Dim a() As String
    Dim itemCode As ClCode
    Dim exist As Boolean
    Dim format As String
    Dim tracing As String
    Dim find As String
    
    With CodeDB
    Set Code = New ColCode
    Set isisCode = New ClIsisdll
    If Not isisCode.Inicia(.Path, .FileName, .key) Then
            MsgBox "Problem with " + .FileName
    Else
        If Not isisCode.IfCreate(.FileName) Then
            MsgBox "Problem with inverted of " + .FileName
        Else
            i = 0
            Mfn = 0
            
            find = key
            If Len(idiom) > 0 Then
                find = idiom & "_" & find
            End If
            
            find = Replace(find, " ", "_")
            'q = isisCode.MfnFind(Replace(find, " ", "_"), mfns)
            q = isisCode.MfnFind(find, mfns)
            
            format = "if s(v1^*)='" + key + "' and (s(v1^l)='" + idiom + "' or a(v1^l))  then (v2^v|;|),'|',(v2^c|;;|) fi"
            
            If q > 0 Then
                While (i < q) And (Mfn = 0)
                    i = i + 1
                    aux = isisCode.UsePft(mfns(i), format)
                    If Len(aux) > 0 Then Mfn = mfns(i)
                Wend
            Else
                q = isisCode.MfnQuantity
                While (i < q) And (Mfn = 0)
                    i = i + 1
                    aux = isisCode.UsePft(i, format)
                    If Len(aux) > 0 Then Mfn = i
                Wend
            End If
            tracing = vbCrLf & "format: " & format & vbCrLf & "result:" & aux & vbCrLf & "mfn: " & CStr(Mfn)
            
            If Mfn > 0 Then
                a = Split(aux, "|")
                a_values = Split(a(0), ";")
                a_codes = Split(a(1), ";;")
                
                For i = 0 To UBound(a_values) - 1
                    Set itemCode = Code.item(CVar(a_codes(i)), exist)
                    tracing = tracing + vbCrLf + "(" + a_codes(i) + "," + a_values(i) + ")" + CStr(exist)
                    If Not exist Then
                        Set itemCode = New ClCode
                        
                        itemCode.Code = a_codes(i)
                        If codeEqualValue Then
                            itemCode.value = a_codes(i)
                        Else
                            itemCode.value = a_values(i)
                        End If
                        Call Code.add(itemCode, CVar(a_codes(i)))
                    End If
                Next
                
            End If
        End If
    End If
    If Code.count = 0 Then MsgBox CodeDB.Path + "\" + CodeDB.FileName + vbCrLf + find + " " + tracing
    
    End With
End Sub

Sub LoadCodesMultilingue(CodeDB As ClFileInfo, key As String, tableList As ColObjByLang)
    Dim isisCode As ClIsisdll
    Dim Mfn As Long
    Dim mfns() As Long
    Dim q As Long
    Dim i As Long
    Dim k As Long
    Dim aux As String
    Dim a_codes() As String
    Dim a_values() As String
    Dim a() As String
    Dim table As ColCode
    Dim itemCode As ClCode
    Dim exist As Boolean
    Dim format As String
    Dim tracing As String
    Dim find As String
    Dim lang As String
    
    With CodeDB
    Set tableList = New ColObjByLang
    Set isisCode = New ClIsisdll
    If isisCode.Inicia(.Path, .FileName, .key) Then
        If isisCode.IfCreate(.FileName) Then
            
            Mfn = 0
            Set tableList = New ColObjByLang
            
            find = key
            find = Replace(find, " ", "_")
            
            q = isisCode.MfnFind(find, mfns)
            format = "if s(v1^*)='" + key + "' then (v2^v|~|),'|',(v2^c|~~|) fi,,'|',v1^l"
            For k = 1 To q
                aux = isisCode.UsePft(mfns(k), format)
                If Len(aux) > 0 Then
                    Mfn = mfns(k)
                    tracing = vbCrLf & "format: " & format & vbCrLf & "result:" & aux & vbCrLf & "mfn: " & CStr(Mfn)
                    
                    If Mfn > 0 Then
                        a = Split(aux, "|")
                        a_values = Split(a(0), "~")
                        a_codes = Split(a(1), "~~")
                        lang = a(2)
                        Set table = New ColCode
                        table.lang = lang
                        
                        For i = 0 To UBound(a_values) - 1
                            Set itemCode = New ClCode
                            itemCode.value = a_values(i)
                            itemCode.Code = a_codes(i)
                            Call table.add(itemCode, CVar(a_codes(i)))
                        Next
                        
                        Call tableList.add(table)
                    End If
                End If
            Next
        End If
    End If
    If tableList.count = 0 Then MsgBox "count=0 q=" + CStr(q) + " " + find + " " + tracing
    
    End With
End Sub
Property Let ChangeInterfaceIdiom(idiom As String)
    Dim i As Long
    Dim x As ClIdiom
    Dim CodeDB As ClFileInfo
    Dim codedao As New ClsCodesDAO
    
    CurrIdiomHelp = idiom
    Set Paths = New ColFileInfo
    Set Paths = ReadPathsConfigurationFile(PathsConfigurationFile)
    Set ConfigLabels = New ClLabels
    ConfigLabels.SetLabels (idiom)
    Set Fields = New ColFields
    Fields.SetLabels (idiom)
    
    loadIssueIdPart idiom
    Set CodeDB = New ClFileInfo

    Set CodeDB = Paths("Code Database")
    Call codedao.create(CodeDB.Path, CodeDB.FileName, CodeDB.key)
    
    Call codedao.getTable(idiom, "license", codeLIcense)
    
    Call codedao.getTable(idiom, "idiom interface", CodeIdiom)
    
    Call codedao.getTable(idiom, "alphabet of title", CodeAlphabet)
    Call codedao.getTable(idiom, "literature type", CodeLiteratureType)
    Call codedao.getTable(idiom, "treatment level", CodeTreatLevel)
    Call codedao.getTable(idiom, "publication level", CodePubLevel)
    Call codedao.getTable(idiom, "frequency", CodeFrequency)
    Call codedao.getTable(idiom, "status", codeStatus)
    'FIXME
    Call codedao.getTable(idiom, "historystatus", codeHistory)
    Call codedao.getTable(idiom, "country", CodeCountry)
    Call codedao.getTable(idiom, "state", CodeState)
    
    Call codedao.getTable(idiom, "publishingmodel", CodePublishingModel)
    Call codedao.getTable(idiom, "usersubscription", CodeUsersubscription)
    Call codedao.getTable(idiom, "ftp", CodeFTP)
        
    Call codedao.getTable(idiom, "language", CodeAbstLanguage)
    Call codedao.getTable(idiom, "language", CodeTxtLanguage)
    Call codedao.getTable(idiom, "issue status", CodeIssStatus)
    Call codedao.getTable(idiom, "scheme", CodeScheme)
    Call codedao.getTable("", "table of contents", CodeTOC)
    
    
    Set CodeDB = Paths("Code Database")
    Call codedao.create(CodeDB.Path, CodeDB.FileName, CodeDB.key)
    
    Call codedao.getTable(idiom, "study area", CodeStudyArea)
    
           
    Set idiomsinfo = New ColIdiom
    Set x = New ClIdiom
    For i = 1 To CodeIdiom.count
        'Set x = IdiomsInfo(CodeIdiom(i).Code)
        'If x Is Nothing Then
        
            Set x = idiomsinfo.add(CodeIdiom.item(i).Code, CodeIdiom(i).value, CodeTOC.item(CodeIdiom(i).Code).value, CodeIdiom(i).Code)
        'Else
        '    IdiomsInfo.item(CodeIdiom(i).Code).label = CodeIdiom(i).value
        '    IdiomsInfo.item(CodeIdiom(i).Code).More = CodeTOC(CodeIdiom(i).Code).value
        'End If
    Next
'MsgBox "changeInterfaceIdiom 29"
    
End Property


Function ReadPathsConfigurationFile(File As String) As ColFileInfo
    Dim fn As Long
    Dim lineread As String
    Dim item As ClFileInfo
    Dim key As String
    Dim Path As String
    Dim CollectionPaths As ColFileInfo
    Dim req As Long
    
    fn = FreeFile
    Open File For Input As fn
        
    Set CollectionPaths = New ColFileInfo
    
    While Not EOF(fn)
        Line Input #fn, lineread
        If InStr(lineread, "=") > 0 Then
            key = Mid(lineread, 1, InStr(lineread, "=") - 1)
            Path = Mid(lineread, InStr(lineread, "=") + 1)
            req = InStr(Path, ",required")
            If req > 0 Then
                Path = Mid(Path, 1, req - 1)
                
            End If
            Set item = CollectionPaths.add(key)
            item.key = key
            If InStr(Path, "\") > 0 Then
                item.Path = Mid(Path, 1, InStrRev(Path, "\") - 1)
                item.FileName = Mid(Path, InStrRev(Path, "\") + 1)
            Else
                item.Path = ""
                item.FileName = Path
            End If
            item.required = (req > 0)
        End If
    Wend
    Close fn
    Set ReadPathsConfigurationFile = CollectionPaths
End Function
Sub loadIssueIdPart(CurrCodeIdiom As String)
    Dim fn As Long
    Dim key As String
    Dim value As String
    Dim obj As ClCode
    
    Set issueidparts = New ColCode
    fn = FreeFile
    Open App.Path + "\tables\" + CurrCodeIdiom + "\part.ini" For Input As fn
    While Not EOF(fn)
        Input #fn, key, value
        
        Set obj = New ClCode
        obj.index = issueidparts.count + 1
        obj.value = value
        obj.Code = key
        issueidparts.add obj, key
         
    Wend
    Close fn
End Sub

Sub openHelp(Path As String, Optional File As String)
    Dim f As String
    If Len(File) > 0 Then f = "\" & CurrIdiomHelp & File
    Call Shell("cmd.exe /k start " & Path & f, vbHide)
    
End Sub
