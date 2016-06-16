VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClsIssueDAO"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Private isis As ClIsisdll
Public issue_TOC_DAO As New ClsTOC_DAO
Public dbLabel As String

Sub create(Path As String, FileName As String, key As String, Optional generateTOC As Boolean = True)
    Set isis = New ClIsisdll
    If isis.Inicia(Path, FileName, key) Then
        If isis.IfCreate(FileName) Then
            If generateTOC Then Call issue_TOC_DAO.create(isis)
        End If
    End If
End Sub


Function returnSectionsInUse(journal As String) As ClsTOC
    Dim mfnQtd As Long
    Dim mfnList() As Long
    Dim i As Long
    'Dim format As String
    
    Dim toc As New ClsTOC
    
    'format = "v31,'|',v32,'|',v131,'|',v132,'|',v36/"
    
    mfnQtd = isis.MfnFind(journal, mfnList)
    For i = 1 To mfnQtd
        Set toc = issue_TOC_DAO.getTOC(mfnList(i), toc)
    Next
    
    Set returnSectionsInUse = toc
End Function

Function whereSectionInUse(journal As String, Code As String, issues As ClsIssues, resultType As String) As Boolean
    Dim mfnQtd As Long
    Dim mfnList() As Long
    Dim i As Long
    Dim issue As ClsIssue
    
    Dim found As Boolean
    Dim format As String
    
    Set issues = New ClsIssues
    
    If resultType = "" Then resultType = "all"
    
    format = "(if v49^c='" + Code + "' then v31[1],'|',v32[1],'|',v131[1],'|',v132[1],'|',v36[1],'|',v41/,break  fi)"
    mfnQtd = isis.MfnFind(journal, mfnList)
    
    Select Case resultType
    Case "all"
        
        For i = 1 To mfnQtd
            Set issue = returnIssue(mfnList(i), format)
            If issue Is Nothing Then
            
            Else
                Call issues.add(issue)
                found = True
            End If
        Next
    Case "first"
        While i < mfnQtd And Not found
            i = i + 1
            Set issue = returnIssue(mfnList(i), Code)
            If issue Is Nothing Then
            
            Else
                Call issues.add(issue)
                found = True
            End If
        Wend
    End Select
    whereSectionInUse = found
End Function
Function returnIssue(Mfn As Long, Optional format As String) As ClsIssue
    Dim issue As ClsIssue
    Dim x As String
    Dim Y() As String
    Dim i As Long
    Dim lic As String
    Set issue = New ClsIssue
    If format <> "" Then
        x = isis.UsePft(Mfn, format)
        If Len(x) > 0 Then
            Y = Split(x, "|")
            
            issue.volume = Y(0)
            issue.vsuppl = Y(2)
            issue.number = Y(1)
            issue.suppl = Y(3)
            issue.issueorder = Y(4)
            issue.idPart = Y(5)
        Else
            Set issue = Nothing
        End If
    Else
        
        With issue.journal
            .shorttitle = isis.UsePft(Mfn, "v30")
            .Title = isis.UsePft(Mfn, "v130")
            .pubid = isis.UsePft(Mfn, "v930")
            .JournalStandard = isis.UsePft(Mfn, "v117")
            .vocabulary = isis.UsePft(Mfn, "v85")
            .publisherName = isis.UsePft(Mfn, "v480")
            .parallelTitles = isis.UsePft(Mfn, "(v230/)")
            .ISOTitle = isis.UsePft(Mfn, "v151")
            .MedlineTitle = isis.UsePft(Mfn, "v421")
            .ISSN = isis.UsePft(Mfn, "v35")
            
        End With
        issue.volume = isis.UsePft(Mfn, " v31")
        issue.number = isis.UsePft(Mfn, " v32")
        issue.suppl = isis.UsePft(Mfn, " v132")
        issue.vsuppl = isis.UsePft(Mfn, "v131")
        issue.issueorder = isis.UsePft(Mfn, " v36")
        issue.idPart = isis.UsePft(Mfn, " v41")
        issue.doccount = isis.UsePft(Mfn, " v122")
        issue.DateISO = isis.UsePft(Mfn, " v65")
        issue.issuepart = isis.UsePft(Mfn, " v34")
        issue.issueSponsor = isis.UsePft(Mfn, " v140")
        issue.issuePublisher = isis.UsePft(Mfn, " v62")
        issue.issueCover = isis.UsePft(Mfn, " v97")
        issue.markupDone = isis.UsePft(Mfn, " v200")
        
        
        Dim pissn As String
        Dim eissn As String
        
        Call issn_get(Mfn, pissn, eissn)
        issue.pissn = pissn
        issue.eissn = eissn
        
        
        issue.status = isis.UsePft(Mfn, " v42")
        
        Dim t As ClsTextByLang
        Dim obj As ClsBibStrip
        Dim subf(8) As String
         Dim content(8) As String
        subf(1) = "t"
        subf(2) = "v"
        subf(3) = "w"
        subf(4) = "n"
        subf(5) = "s"
        subf(6) = "c"
        subf(7) = "m"
        subf(8) = "a"
        
        Set issue.toc = New ClsTOC
        Set issue.toc = issue_TOC_DAO.getTOC(Mfn, issue.toc)
        issue.license_code = isis.UsePft(Mfn, "v541")
        
        
        For i = 1 To idiomsinfo.count
            Set t = New ClsTextByLang
            t.lang = idiomsinfo.item(i).Code
            t.text = isis.getFieldContentByLanguage(Mfn, 33, idiomsinfo.item(i).Code, "*")
            issue.issueTitle.add t
            
            Set obj = New ClsBibStrip
            Call isis.getSubFieldsContentByLanguage(Mfn, 43, idiomsinfo.item(i).Code, subf, content)
            With obj
                .stitle = content(1)
                .v = content(2)
                .vs = content(3)
                .n = content(4)
                .s = content(5)
                .loc = content(6)
                .month = content(7)
                .year = content(8)
                .lang = idiomsinfo.item(i).Code
            End With
            Call issue.bibstrips.add(obj)
        Next
    End If
    Set returnIssue = issue
End Function
Function getIssueMfnByIseqNo(journalKey As String, iseqno As String) As Long
    Dim MfnIseqNo As Long
    Dim issue As ClsIssue
    Dim i As Long
    Dim mfns() As Long
    Dim q As Long
    Dim xNroSeq As String
    Dim xsertitle As String
    Dim IseqNoPFT As String
    
    MfnIseqNo = 0
    q = isis.MfnFind(journalKey + iseqno, mfns)
    i = 0
    While (i < q) And (MfnIseqNo = 0)
        i = i + 1
        xNroSeq = isis.UsePft(mfns(i), "v36")
        xsertitle = isis.UsePft(mfns(i), "v35")
        If (iseqno = xNroSeq) And (journalKey = xsertitle) Then
            MfnIseqNo = mfns(i)
        End If
    Wend
    If MfnIseqNo = 0 Then
        IseqNoPFT = "if "
        IseqNoPFT = IseqNoPFT + "v35='" + journalKey + "' and "
        IseqNoPFT = IseqNoPFT + "v36='" + iseqno + "' then mfn fi"
        
        MfnIseqNo = getIssueMfnByFormat(IseqNoPFT)
    End If
    getIssueMfnByIseqNo = MfnIseqNo
End Function
Function getIssueMfnByIssueId(journalKey As String, vol As String, SVol As String, No As String, SNo As String, IssueIdPart As String, iseqno As String) As Long
    Dim MfnIssueId As Long
    Dim issue As ClsIssue
    Dim i As Long
    Dim mfns() As Long
    Dim q As Long
    Dim IssueIdPFT As String
    Dim year As String
    
    MfnIssueId = 0
    If No = "ahead" Or No = "review" Then
        year = Mid(iseqno, 1, 4)
    End If
    q = isis.MfnFind(journalKey + year + issueId(vol, SVol, No, SNo, IssueIdPart), mfns)
    While (i < q) And (MfnIssueId = 0)
        i = i + 1
        Set issue = returnIssue(mfns(i))
        If (journalKey = issue.journal.ISSN) And (IssueIdPart = issue.idPart) And (vol = issue.volume) And (SVol = issue.vsuppl) And (No = issue.number) And (SNo = issue.suppl) Then
            If Len(year) > 0 Then
                If year = Mid(issue.DateISO, 1, 4) Then
                    MfnIssueId = mfns(i)
                End If
            Else
                MfnIssueId = mfns(i)
            End If
            
        End If
    Wend
    If MfnIssueId = 0 Then
        IssueIdPFT = "if "
        IssueIdPFT = IssueIdPFT + "v35='" + journalKey + "' and "
        IssueIdPFT = IssueIdPFT + "v31='" + vol + "' and "
        IssueIdPFT = IssueIdPFT + "v131='" + SVol + "' and "
        IssueIdPFT = IssueIdPFT + "v32='" + No + "' and "
        IssueIdPFT = IssueIdPFT + "v41='" + IssueIdPart + "' and "
        If Len(year) > 0 Then
            IssueIdPFT = IssueIdPFT + "v36*0.4='" + year + "' and "
        End If
        IssueIdPFT = IssueIdPFT + "v132='" + SNo + "' then mfn fi"
        MfnIssueId = getIssueMfnByFormat(IssueIdPFT)
    End If
    getIssueMfnByIssueId = MfnIssueId
End Function
Function getIssueMfnByFormat(format As String) As Long
    Dim Mfn As Long
    Dim mfnfound As Long
    Dim r As String
    Dim limit As Long
    Mfn = isis.MfnQuantity
    limit = isis.MfnQuantity - LIMIT_MFN
    
    While (Mfn > limit) And (mfnfound = 0)
        Mfn = Mfn - 1
        r = isis.UsePft(Mfn, format)
        
        If Len(r) > 0 Then
            mfnfound = Mfn
        End If
    Wend
    getIssueMfnByFormat = mfnfound
End Function

Function getIssueMfn(journalKey As String, vol As String, SVol As String, No As String, SNo As String, iseqno As String, IssueIdPart As String, MfnIseqNo As Long, MfnIssueId As Long) As Boolean
    MfnIssueId = getIssueMfnByIssueId(journalKey, vol, SVol, No, SNo, IssueIdPart, iseqno)
    MfnIseqNo = getIssueMfnByIseqNo(journalKey, iseqno)
    
    getIssueMfn = (MfnIseqNo = MfnIssueId)
End Function
Function deleteRecord(Mfn As Long) As Boolean
    If isis.RecordDel(Mfn) Then
        Call isis.IfUpdate(Mfn, Mfn)
        deleteRecord = True
    End If
End Function
Function UpdateIssueId(Mfn As Long, vol As String, vs As String, n As String, s As String, iseq As String, idPart As String) As Long
    Dim xMfn As Long
    Dim resp As Boolean
    
    With isis
    
        If .FieldContentUpdate(Mfn, 36, iseq) Then
        If .FieldContentUpdate(Mfn, 31, vol) Then
        If .FieldContentUpdate(Mfn, 32, n) Then
        If .FieldContentUpdate(Mfn, 131, vs) Then
        If .FieldContentUpdate(Mfn, 132, s) Then
        If .FieldContentUpdate(Mfn, 41, idPart) Then
            resp = .IfUpdate(Mfn, Mfn)
            xMfn = Mfn
        End If
        End If
        End If
        End If
        End If
        End If
    End With
    UpdateIssueId = xMfn
End Function



Function getIssuesMfnByISSN(volid As String, iseqno As String, ISSN As String, mfns() As Long) As Long
    Dim term As String
    
    Dim q As Long
    
    term = ISSN
    
    
    'q = isis.search(term, mfns)
    q = isis.MfnFind(term, mfns)
    
    
    getIssuesMfnByISSN = q
End Function

Function tag(issue As ClsIssue) As String
    Dim s As String
    Dim i As Long
    
    s = s + TagContent("1", 991)
    s = s + TagContent("0", 700)
    s = s + TagContent("i", 706)
    s = s + TagContent("1", 701)
    s = s + TagContent(getDateIso(Date), 91)
    
    With issue
        With .journal
        s = s + TagContent(.Title, 130)
        s = s + TagContent(.MedlineTitle, 421)
        s = s + TagContent(.ISOTitle, 151)
        s = s + TagTxtContent(.parallelTitles, 230)
        s = s + TagContent(.ISSN, 35)
        s = s + TagTxtContent(.publisherName, 480)
        s = s + TagContent(.shorttitle, 30)
        s = s + TagContent(.pubid, 930)
        s = s + TagContent(.JournalStandard, 117)
        s = s + TagContent(.vocabulary, 85)
        End With
        
        Dim v435 As String
        Dim v35 As String
        Dim v935 As String
        
        Call issn_build_field(.pissn, .eissn, v435, v35, v935)
        
        s = s + TagTxtContent(v435, 435)
        s = s + TagContent(v935, 935)
        
        s = s + TagContent(.volume, 31)
        s = s + TagContent(.vsuppl, 131)
        s = s + TagContent(.number, 32)
        s = s + TagContent(.suppl, 132)
        s = s + TagContent(.issueorder, 36)
        
        s = s + TagContent(.idPart, 41)
        
        s = s + TagContent(.status, 42)
        s = s + TagContent(.markupDone, 200)
        
        s = s + TagContent(.DateISO, 65)
        s = s + TagContent(.doccount, 122)
        's = s + TagContent(TxtIssTitle.Text, 33)
        s = s + TagContent(.issuepart, 34)
        
        s = s + TagContent(.issueSponsor, 140)
        s = s + TagContent(.issuePublisher, 62)
        s = s + TagContent(.issueCover, 97)
        
        s = s + issue_TOC_DAO.tagTOC(.toc)
        
        Dim bs As ClsBibStrip
        Set .bibstrips.nullObject = New ClsBibStrip
        Dim t As String
        For i = 1 To idiomsinfo.count
            Set bs = .bibstrips.getItemByLang(idiomsinfo(i).Code)
            With bs
            s = s + TagContent(TagSubf(.lang, "l") + TagSubf(.stitle, "t") + TagSubf(.v, "v") + TagSubf(.vs, "w") + TagSubf(.n, "n") + TagSubf(.s, "s") + TagSubf(.loc, "c") + TagSubf(.month, "m") + TagSubf(.year, "a"), 43)
            End With
        Next
        
        s = s + TagContent(.license_code, 541)
        For i = 1 To idiomsinfo.count
            If Len(.issueTitle.getItemByIndex(i).text) > 0 Then
              s = s + TagContent(.issueTitle.getItemByIndex(i).text + "^l" + idiomsinfo(i).Code, 33)
            End If
        Next
        
    End With
    tag = s
End Function


Function save(mfnIssue As Long, issue As ClsIssue) As Boolean
    Dim s As String
    s = tag(issue)
    If mfnIssue > 0 Then
        If isis.RecordUpdate(mfnIssue, s) Then
            Call isis.IfUpdate(mfnIssue, mfnIssue)
        End If
    Else
        mfnIssue = isis.RecordSave(s)
        If mfnIssue > 0 Then Call isis.IfUpdate(mfnIssue, mfnIssue)
    End If
    save = True
End Function

Function UpdateIssueTable(FileName As String, PFTFileName As String) As Boolean
    Dim j As Long
    Dim fn As Long
    Dim result As String
    Dim mfns() As Long
    Dim q As Long
    
    
    q = isis.MfnFind("MKPDONE=0", mfns, 999999999)

    If q > 0 Then
        fn = FreeFile
        Open FileName For Output As fn
        For j = 1 To q
            result = isis.UsePft(mfns(j), "@" + PFTFileName)
            If Len(result) > 0 Then Print #fn, result
        Next
        Close fn
    Else
        For j = isis.MfnQuantity - LIMIT_MFN To isis.MfnQuantity
            result = isis.UsePft(j, "if v200<>'1' then mfn fi")
            If Len(result) > 0 Then
                result = isis.UsePft(j, "@" + PFTFileName)
                If Len(result) > 0 Then Print #fn, result
            End If
        Next
        'MsgBox "Problem creating " & FileName, vbExclamation
    End If
    
End Function
Function getIssuesMfnByJournalID(journalId As String) As Variant
    Dim mfns() As Long
    Dim q As Long
    
    
    
    q = isis.MfnFind(journalId, mfns)
    getIssuesMfnByJournalID = mfns
End Function
Sub issn_get(Mfn As Long, ByRef pissn As String, ByRef eissn As String)
    Dim v435 As String
    Dim v35 As String
    Dim v935 As String
    Dim v400 As String
    Dim issns() As String
    Dim issn_type() As String
    Dim i As Long
    
    pissn = ""
    eissn = ""
    v435 = isis.UsePft(Mfn, "(v435+|%|)")
    If Len(v435) > 0 Then
        issns = Split(v435, "%")
        For i = 0 To UBound(issns)
            If Len(issns(i)) > 0 Then
                issn_type = Split(issns(i), "^t")
                If issn_type(1) = "ONLIN" Then
                    eissn = issn_type(0)
                Else
                    pissn = issn_type(0)
                End If
            End If
        Next
    End If
End Sub
Sub issn_build_field(ByRef pissn As String, ByRef eissn As String, ByRef v435 As String, ByRef v35 As String, ByRef v935 As String)
    v435 = ""
    If Len(pissn) > 0 Then
        v435 = pissn + "^tPRINT"
        v35 = "PRINT"
        v935 = pissn
    End If
    If Len(eissn) > 0 Then
        v435 = v435 + vbCrLf + eissn + "^tONLIN"
        v35 = "ONLIN"
        v935 = eissn
    End If
End Sub
