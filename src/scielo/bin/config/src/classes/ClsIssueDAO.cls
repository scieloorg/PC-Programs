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
Public generalTOC_DAO As New ClsTOC_DAO
Public dbLabel As String

Sub create(Path As String, FileName As String, key As String, Optional generateTOC As Boolean = True)
    Set isis = New ClIsisdll
    If isis.Inicia(Path, FileName, key) Then
        Call FileCopy(Paths("Issue FST").Path + "\misc\" + Paths("Issue FST").FileName, Path + "\" + FileName + ".fst")
        If isis.IfCreate(FileName) Then
            If generateTOC Then Call generalTOC_DAO.create(isis)
        End If
    End If
End Sub

'Function reinvert(newfst As String, log As String) As Boolean
'
    'Dim Ret As Boolean
 '
    'Dim isisDAO As New ClsIsisDAO
    'If isisDAO.create(isis.MSTPATH, isis.MSTFILE, "") Then
    '    Ret = isisDAO.reinvertIfNecessary(newfst, log)
    'End If
    'reinvert = Ret
'End Function
Function returnSectionsInUse(journal As String) As ClsTOC
    Dim mfnQtd As Long
    Dim mfnList() As Long
    Dim i As Long
    'Dim format As String
    
    Dim toc As New ClsTOC
    
    'format = "v31,'|',v32,'|',v131,'|',v132,'|',v36/"
    
    mfnQtd = isis.MfnFind(journal, mfnList)
    For i = 1 To mfnQtd
        Set toc = generalTOC_DAO.getTOC(mfnList(i), toc)
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
        issue.issueISSN = isis.UsePft(Mfn, " v935")
        issue.lic = isis.UsePft(Mfn, "v541")
        
        
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
        
        For i = 1 To IdiomsInfo.count
            Set t = New ClsTextByLang
            t.lang = IdiomsInfo.item(i).Code
            t.text = isis.getFieldContentByLanguage(Mfn, 33, IdiomsInfo.item(i).Code, "*")
            
            
            issue.issueTitle.add t
            
            Set t = New ClsTextByLang
            t.lang = IdiomsInfo.item(i).Code
            t.text = isis.getFieldContentByLanguage(Mfn, 540, IdiomsInfo.item(i).Code, "t")
            
            lic = t.text
            issue.licenses.add t
            
            Set obj = New ClsBibStrip
            
            Call isis.getSubFieldsContentByLanguage(Mfn, 43, IdiomsInfo.item(i).Code, subf, content)
            With obj
                .stitle = content(1)
                .v = content(2)
                .vs = content(3)
                .n = content(4)
                .s = content(5)
                .loc = content(6)
                .month = content(7)
                .year = content(8)
                .lang = IdiomsInfo.item(i).Code
            End With
            
            Call issue.bibstrips.add(obj)
            
        Next
            
            Set issue.toc = generalTOC_DAO.getTOC(Mfn, issue.toc)
            
        If Len(issue.lic) = 0 Then
            If InStr(lic, "<p> </p>") > 0 Then
                issue.lic = "nd"
            Else
                If Len(lic) = 0 Then
                    issue.lic = "BY-NC"
                Else
                    issue.lic = "BY"
                End If
            End If
        End If
    End If
    Set returnIssue = issue
End Function
Function getIssueMfnByIseqNo(journalKey As String, IseqNo As String) As Long
    Dim MfnIseqNo As Long
    Dim issue As ClsIssue
    Dim i As Long
    Dim mfns() As Long
    Dim q As Long
    Dim xNroSeq As String
    Dim xsertitle As String
    Dim IseqNoPFT As String
    
    MfnIseqNo = 0
    q = isis.MfnFind(journalKey + "|" + IseqNo, mfns)
    i = 0
    While (i < q) And (MfnIseqNo = 0)
        i = i + 1
        xNroSeq = isis.UsePft(mfns(i), "v36")
        xsertitle = isis.UsePft(mfns(i), "v35")
        If (IseqNo = xNroSeq) And (journalKey = xsertitle) Then
            MfnIseqNo = mfns(i)
        End If
    Wend
    If MfnIseqNo = 0 Then
        IseqNoPFT = "if "
        IseqNoPFT = IseqNoPFT + "v35='" + journalKey + "' and "
        IseqNoPFT = IseqNoPFT + "v36='" + IseqNo + "' then mfn fi"
        
        MfnIseqNo = getIssueMfnByFormat(IseqNoPFT)
    End If
    getIssueMfnByIseqNo = MfnIseqNo
End Function
Function getIssueMfnByIssueId(journalKey As String, vol As String, SVol As String, No As String, SNo As String, IssueIdPart As String, IseqNo As String) As Long
    Dim MfnIssueId As Long
    Dim issue As ClsIssue
    Dim i As Long
    Dim mfns() As Long
    Dim q As Long
    Dim IssueIdPFT As String
    Dim year As String
    
    MfnIssueId = 0
    If No = "ahead" Or No = "review" Then
        year = Mid(IseqNo, 1, 4)
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
    
    While (Mfn < isis.MfnQuantity) And (mfnfound = 0)
        Mfn = Mfn + 1
        r = isis.UsePft(Mfn, format)
        
        If Len(r) > 0 Then
            mfnfound = Mfn
        End If
    Wend
    getIssueMfnByFormat = mfnfound
End Function

Function getIssueMfn(journalKey As String, vol As String, SVol As String, No As String, SNo As String, IseqNo As String, IssueIdPart As String, MfnIseqNo As Long, MfnIssueId As Long) As Boolean
    MfnIssueId = getIssueMfnByIssueId(journalKey, vol, SVol, No, SNo, IssueIdPart, IseqNo)
    MfnIseqNo = getIssueMfnByIseqNo(journalKey, IseqNo)
    
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

Function getIssuesMfn(volid As String, issueno As String, sertitle As String, mfns() As Long) As Long
    Dim term As String
    
    Dim q As Long
    
    If Len(volid) > 0 Then
        term = "V=" + volid + "," + sertitle
    ElseIf Len(issueno) > 0 Then
        term = "N=" + issueno + "," + sertitle
    Else
        term = "SERTIT=" + sertitle
    End If
    q = isis.MfnFind(term, mfns)
    getIssuesMfn = q
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
        
        s = s + TagContent(.issueISSN, 935)
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
        
        s = s + generalTOC_DAO.tagTOC(.toc)
        
        Dim bs As ClsBibStrip
        Set .bibstrips.nullObject = New ClsBibStrip
        Dim t As String
        For i = 1 To IdiomsInfo.count
            Set bs = .bibstrips.getItemByLang(IdiomsInfo(i).Code)
            With bs
            s = s + TagContent(TagSubf(.lang, "l") + TagSubf(.stitle, "t") + TagSubf(.v, "v") + TagSubf(.vs, "w") + TagSubf(.n, "n") + TagSubf(.s, "s") + TagSubf(.loc, "c") + TagSubf(.month, "m") + TagSubf(.year, "a"), 43)
            End With
        Next
        
        For i = 1 To IdiomsInfo.count
            If Len(Trim(.licenses.getItemByLang(IdiomsInfo(i).Code).text)) > 0 Then
                s = s + TagContent(TagSubf(.licenses.getItemByLang(IdiomsInfo(i).Code).text, "t") + TagSubf(IdiomsInfo(i).Code, "l"), 540)
            End If
        Next
        s = s + TagContent(.lic, 541)
        For i = 1 To IdiomsInfo.count
            If Len(.issueTitle.getItemByIndex(i).text) > 0 Then
              s = s + TagContent(.issueTitle.getItemByIndex(i).text + "^l" + IdiomsInfo(i).Code, 33)
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
        For j = 1 To isis.MfnQuantity
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
