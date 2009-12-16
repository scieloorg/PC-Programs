Attribute VB_Name = "Module1"
Public BrowserPath As String

Public AppHandle As Long
Public CurrDTD As String
Public DTDs As ColDTD


Const DTDInfoFile = "dtdinfo.txt"

Const ImgSuf = "img"
Const TagImg = "<img "

Private Const TAGC = ">"
Private Const ETAGO = "</"
Private Const STAGO = "<"

Public Const PathSep = "\"
Public Const PathSepUnix = "/"

Private Const MstExt = ".mst"
Private Const XrfExt = ".xrf"
Private Const SGMLExt = ".sgml"
Private Const ParserExt = ".txt"
Public Const ReportExt = ".rep"
Private Const ALLFiles = ".*"

Const SerialDirectory = "c:\scielo\serial"
Public Const BaseDIR = "base"
Public Const PubMedDIR = "pubmed"

Public Const TitleDB_Fullpath = "c:\scielo\serial\title"
Public Const TitleDB_File = "title"
Public Const TitleDB_InvFile = "tit_issn"
Public Const TitleDB_Field = "v100"
Public Const TitleDB_Label = "Title Database"
Public Const MEDLINE_TITLE = "if p(v421) then v100 fi"

Private Const GzmField1 = "v1"
Private Const GzmField2 = "v2"

Private Const Parser_EXE = "parser.exe"


Sub MainOld()
    ReadIni
    FrmBase2Doc.OpenForm
End Sub

Sub ReadIni()
    Dim fn As Long
    Dim DTDName As String
    Dim DocTypeName As String
    Dim DTDFile As String
    Dim PFTFILE As String
    Dim CIPFILE As String
    Dim PFTCount As Long
    Dim ReportPFTFile As String
    Dim SGM2ASC As String
    Dim SubSup2ASC As String
    Dim IMG2ASC As String
    Dim RECOVER_REPLACESYMBOL As String
    Dim ASC2SGM As String
    Dim DTD As ClDTD
    Dim exist As Boolean
    Dim i As Long
    Dim P As Long
    Dim WhiteLine As String
    Dim TAGSFILE As String
    Dim ProcFile As String
    
    fn = 1
    Open "brwrpath.txt" For Input As fn
    Line Input #fn, BrowserPath
    Close fn
    
    Open DTDInfoFile For Input As fn
    
    Set DTDs = New ColDTD
    While Not EOF(fn)
        'name,dtdfile,pftfile,pft relatorio,extensao relatorio,gizmo,validrecords,recidfield,FileNamePft,docipfile
        Line Input #fn, DTDName
        Line Input #fn, DocTypeName
        Line Input #fn, DTDFile
        Line Input #fn, ProcFile
        Line Input #fn, PFTFILE
        Line Input #fn, CIPFILE
        Line Input #fn, TAGSFILE
        Line Input #fn, ReportPFTFile
        Line Input #fn, SGM2ASC
        Line Input #fn, SubSup2ASC
        Line Input #fn, IMG2ASC
        Line Input #fn, RECOVER_REPLACESYMBOL
        Line Input #fn, ASC2SGM
        Line Input #fn, WhiteLine
        
        Set DTD = New ClDTD
        Set DTD = DTDs(DTDName, exist)
        If Not exist Then
            Set DTD = DTDs.Add(DTDName)
            DTD.name = DTDName
            DTD.DocTypeName = DocTypeName
            DTD.DTDFile = DTDFile
            DTD.PFTFILE = PFTFILE
            DTD.ProcFile = ProcFile
            DTD.CIPFILE = CIPFILE
            DTD.TAGSFILE = TAGSFILE
            DTD.PFTCount = PFTCount
            DTD.ReportPFTFile = ReportPFTFile
            DTD.SGM2ASC = SGM2ASC
            DTD.SubSup2ASC = SubSup2ASC
            DTD.IMG2ASC = IMG2ASC
            DTD.RECOVER_REPLACESYMBOL = RECOVER_REPLACESYMBOL
            DTD.ASC2SGM = ASC2SGM
        End If
    Wend
    Close fn
    
    CurrDTD = DTDName
    
    'por causa do pubmed
    'ReadDirTree ("treetest.txt")
    'MakeTree

End Sub

Function FindImg(dbpath As String, DBFile As String, ImageAddress() As String, ImageShortAddress() As String, ImageReplace() As String) As Long
    Dim P1 As Long
    Dim p2 As Long
    Dim result As String
    Dim Img As String
    Dim img2 As String
    Dim DBase As ClIsisDll
    Dim Mfn As Long
    Dim P As Long
    Dim IMGFile As String
    Dim ImgCounter As Long
    Dim Count As Long
            
    Set DBase = New ClIsisDll
    If DBase.Inicia(dbpath, DBFile, DBFile) Then
        
        IMGFile = DBFile + ImgSuf
        
        For Mfn = 1 To DBase.MfnQuantity
            result = DBase.RecordGet(Mfn)
            P1 = 0
            P1 = InStr(P1 + 1, result, TagImg, vbTextCompare)
            While P1 > 0
                p2 = InStr(P1, result, TAGC, vbBinaryCompare)
                Img = Mid(result, P1, p2 - P1 + 1)
                P = InStr(Img, PathSepUnix)
                While P > 0
                    img2 = Mid(Img, P + 1)
                    P = InStr(P + 1, Img, PathSepUnix, vbBinaryCompare)
                Wend
                img2 = dbpath + PathSep + ImgSuf + PathSep + Mid(img2, 1, InStr(2, img2, Chr(34)) - 1)
                
                Count = ImgCounter
                Call InsElem(ImageAddress, ImgCounter, Img)
                If Count < ImgCounter Then
                    ReDim Preserve ImageShortAddress(ImgCounter)
                    ReDim Preserve ImageReplace(ImgCounter)
                    'ImageAddress(ImgCounter) = Img
                    ImageShortAddress(ImgCounter) = img2
                End If
                P1 = InStr(P1 + 1, result, TagImg, vbTextCompare)
            Wend
        Next
        'Close fn1
        'Close fn2
    End If
    Set DBase = Nothing
    FindImg = ImgCounter
End Function

Private Sub InsElem(Elements() As String, Counter As Long, NewElem As String)
    Dim i As Long
    Dim found As Boolean
    
    i = 0
    While (i < Counter) And (Not found)
        i = i + 1
        If StrComp(Elements(i), NewElem, vbBinaryCompare) = 0 Then
            found = True
        End If
    Wend
    If Not found Then
        Counter = Counter + 1
        ReDim Preserve Elements(Counter)
        Elements(Counter) = NewElem
    End If
End Sub
Function GzmImages(ImgGzmPath As String, ImgGzmFile As String, ImageAddress() As String, ImageShortAddress() As String, ImageReplace() As String) As Long
    Dim Mfn As Long
    Dim DBase As ClIsisDll
    Dim P As Long
    Dim Img As String
    Dim img2 As String
    
    Set DBase = New ClIsisDll
    If DBase.Inicia(ImgGzmPath, ImgGzmFile, ImgGzmFile) Then
        ReDim Preserve ImageAddress(DBase.MfnQuantity)
        ReDim Preserve ImageShortAddress(DBase.MfnQuantity)
        ReDim Preserve ImageReplace(DBase.MfnQuantity)
        
        For Mfn = 1 To DBase.MfnQuantity
            ImageAddress(Mfn) = DBase.UsePft(Mfn, GzmField1)
            ImageReplace(Mfn) = DBase.UsePft(Mfn, GzmField2)
            
            Img = ImageAddress(Mfn)
            P = InStr(Img, PathSepUnix)
            While P > 0
                img2 = Mid(Img, P + 1)
                P = InStr(P + 1, Img, PathSepUnix, vbBinaryCompare)
            Wend
            ImageShortAddress(Mfn) = ImgGzmPath + PathSep + ImgSuf + PathSep + Mid(img2, 1, InStr(2, img2, Chr(34)) - 1)
        Next
    End If
    GzmImages = DBase.MfnQuantity
    Set DBase = Nothing
    
End Function

Function GzmSUBSUP(SUBSUPGzmPath As String, SUBSUPGzmFile As String, SUBSUPTAGs() As String, SUBSUPReplace() As String) As Long
    Dim Mfn As Long
    Dim DBase As ClIsisDll
    Dim P As Long
    Dim Img As String
    Dim img2 As String
    Dim Counter As Long
    Dim i As Long
    
    Set DBase = New ClIsisDll
    If DBase.Inicia(SUBSUPGzmPath, SUBSUPGzmFile, SUBSUPGzmFile) Then
        For Mfn = 1 To DBase.MfnQuantity
            i = Counter
            Call InsElem(SUBSUPTAGs, Counter, DBase.UsePft(Mfn, GzmField1))
            If i < Counter Then
                ReDim Preserve SUBSUPReplace(Counter)
                SUBSUPReplace(Counter) = DBase.UsePft(Mfn, GzmField2)
            End If
        Next
    End If
    Set DBase = Nothing
    GzmSUBSUP = Counter
End Function

Private Sub CreateGzm(GzmPath As String, GzmFile As String, Address() As String, Replace() As String, Counter As Long)
    Dim Mfn As Long
    Dim DBase As ClIsisDll
    
    Set DBase = New ClIsisDll
    If DBase.Inicia(GzmPath, GzmFile, Chr(32), True) Then
        For Mfn = 1 To Counter
            Call DBase.RecordSave("<1>" + Address(Mfn) + "</1><2>" + Replace(Mfn) + "</2>")
        Next
    End If
    Set DBase = Nothing
End Sub

Sub CompareGzm(GzmAddress() As String, GzmReplace() As String, GzmCounter As Long, Address() As String, Replace() As String, Counter As Long)
    
    Dim i As Long
    Dim j As Long
    Dim found As Boolean
    
    For i = 1 To Counter
        j = 0
        found = False
        While (j < GzmCounter) And (Not found)
            j = j + 1
            If StrComp(Address(i), GzmAddress(j), vbBinaryCompare) = 0 Then
                Replace(i) = GzmReplace(j)
                
                found = True
            End If
        Wend
    Next
    
End Sub

Sub ConvertDBtoDoc(SourceDBPath As String, SourceDBFile As String, DestinyDBPath As String, DestinyDBFile As String)
    Dim SUBSUPCount As Long
    Dim SUBSUP_tag() As String
    Dim SUBSUPReplace() As String
    Dim SUBSUPContext() As String
    Dim GzmSUBSUPCount As Long
    Dim GzmSUBSUPAddr() As String
    Dim GzmSUBSUPReplace() As String
    Dim GzmSUBSUPFile As String
    Dim GzmSUBSUPPath As String
    Dim P As Long
    
    Dim DBImgCount As Long
    Dim DBImgAddr() As String
    Dim DBImgShortAddr() As String
    Dim DBImgReplace() As String
    Dim GzmImgCount As Long
    Dim GzmImgAddr() As String
    Dim GzmImgShortAddr() As String
    Dim GzmImgReplace() As String
    Dim GzmImgFile As String
    
    Dim fn As Long
    
    With DTDs(CurrDTD)
    
    .ReadTagsFile
    
    If FileExist(DestinyDBPath, .IMG2ASC + MstExt) Then Kill DestinyDBPath + PathSep + .IMG2ASC + ALLFiles
    
    Call GetValidRecords(SourceDBPath, SourceDBFile, DestinyDBPath, DestinyDBFile)
    Call UCaseLastName(DestinyDBPath, DestinyDBFile)
    Call CleanEmail(DestinyDBPath, DestinyDBFile)
    SUBSUPCount = FindSUBSUP(DestinyDBPath, DestinyDBFile, SUBSUP_tag, SUBSUPReplace, SUBSUPContext)
    If SUBSUPCount > 0 Then
        GzmSUBSUPCount = GzmSUBSUP(DestinyDBPath, .SubSup2ASC, GzmSUBSUPAddr, GzmSUBSUPReplace)
        If GzmSUBSUPCount > 0 Then
            Call CompareGzm(GzmSUBSUPAddr, GzmSUBSUPReplace, GzmSUBSUPCount, SUBSUP_tag, SUBSUPReplace, SUBSUPCount)
        End If
        Call FrmSubp.setTAGSUBSUPs(SUBSUP_tag, SUBSUPReplace, SUBSUPContext, SUBSUPCount)
        Call CreateGzm(DestinyDBPath, .SubSup2ASC, SUBSUP_tag, SUBSUPReplace, SUBSUPCount)
    End If
    
    DBImgCount = FindImg(DestinyDBPath, DestinyDBFile, DBImgAddr, DBImgShortAddr, DBImgReplace)
    If DBImgCount > 0 Then
        
        GzmImgFile = DestinyDBFile + ImgSuf
        If FileExist(DestinyDBPath, GzmImgFile + MstExt) Then
            GzmImgCount = GzmImages(DestinyDBPath, GzmImgFile, GzmImgAddr, GzmImgShortAddr, GzmImgReplace)
        End If
        If GzmImgCount > 0 Then
            Call CompareGzm(GzmImgAddr, GzmImgReplace, GzmImgCount, DBImgAddr, DBImgReplace, DBImgCount)
        End If
        Call FrmImage.setImages(DBImgAddr, DBImgShortAddr, DBImgReplace, DBImgCount)
        Call CreateGzm(DestinyDBPath, GzmImgFile, DBImgAddr, DBImgReplace, DBImgCount)
        Call CreateGzm(DestinyDBPath, .IMG2ASC, DBImgAddr, DBImgReplace, DBImgCount)
        
    End If
    Call ReplaceSpecialCharacters(DestinyDBPath, DestinyDBFile)
    
    
    Call CreateDoc(DestinyDBPath, DestinyDBFile, DestinyDBPath, DestinyDBFile)
    Call CreateHTML(DestinyDBPath, DestinyDBFile)
    
    Call FileCopy(DestinyDBPath + PathSep + DestinyDBFile + ".sgml", SerialDirectory + PathSep + PubMedDIR + PathSep + DestinyDBFile + ".sgml")
    End With
    
    fn = 1
    Open App.Path + PathSep + "settings.cfg" For Output As fn
    Print #fn, DTDs(CurrDTD).DTDFile
    Print #fn, DTDs(CurrDTD).DTDFile
    Print #fn, DTDs(CurrDTD).DocTypeName
    Print #fn, "0"
    Print #fn, "0"
    Close fn
    
    Shell App.Path + PathSep + Parser_EXE + Chr(32) + DestinyDBPath + PathSep + DestinyDBFile + ParserExt, vbMaximizedFocus
    
End Sub

Sub ReplaceSpecialCharacters(Path As String, Database As String)
    Dim Mfn As Long
    Dim NewContents As String
    Dim DBase As ClIsisDll
    
    Set DBase = New ClIsisDll
    If DBase.Inicia(Path, Database, Database) Then
    
        
        Call DBase.Gizmo(Path + PathSep + DTDs(CurrDTD).SubSup2ASC)
        Call DBase.Gizmo(Path + PathSep + DTDs(CurrDTD).SubSup2ASC)
        If FileExist(Path, DTDs(CurrDTD).IMG2ASC + ".mst") Then Call DBase.Gizmo(Path + PathSep + DTDs(CurrDTD).IMG2ASC)
                      
        'ProcMsg.GiveRunInformation ("Converting SGML 2 ASCII.")
        Call DBase.Gizmo(DTDs(CurrDTD).SGM2ASC)
            
        'ProcMsg.GiveRunInformation ("Replace Font Face Symbol.")
        For Mfn = 1 To DBase.MfnQuantity
            NewContents = DBase.RecordGet(Mfn)
            NewContents = ReplaceFontFaceSymbol(NewContents)
            If DBase.RecordUpdate(Mfn, NewContents) Then
            End If
        Next
        
        'ProcMsg.GiveRunInformation ("Converting ASCII2SGML")
        Call DBase.Gizmo(DTDs(CurrDTD).ASC2SGM)
        
        'ProcMsg.GiveRunInformation ("Converting Grk2SGML")
        Call DBase.Gizmo(DTDs(CurrDTD).RECOVER_REPLACESYMBOL)
        
    End If
    Set DBase = Nothing
End Sub

Sub UCaseLastName(Path As String, Database As String)
    Dim Mfn As Long
    Dim DBase As ClIsisDll
    Dim Occ As Long
    Dim occcount As Long
    Dim author() As String
    Dim P As Long
    Dim p2 As Long
    Dim surname As String
    
    Set DBase = New ClIsisDll
    If DBase.Inicia(Path, Database, Database) Then
        For Mfn = 1 To DBase.MfnQuantity
                occcount = DBase.FieldOccCount(Mfn, 10)
                ReDim author(occcount)
                For Occ = 1 To occcount
                    author(Occ) = DBase.FieldContentAllOccGet(Mfn, 10, Occ)
                    P = InStr(author(Occ), "^s")
                    If P > 0 Then
                        P = P + 2
                        p2 = InStr(P, author(Occ), "^", vbTextCompare)
                        If p2 > 0 Then
                            surname = UCase(Mid(author(Occ), P, p2 - P))
                            author(Occ) = Mid(author(Occ), 1, P - 1) + surname + Mid(author(Occ), p2)
                        Else
                            surname = UCase(Mid(author(Occ), P))
                            author(Occ) = Mid(author(Occ), 1, P - 1) + surname
                        End If
                    End If
                Next
                For Occ = 1 To occcount
                    Call DBase.FieldContentUpdate(Mfn, 10, author(Occ), 1)
                Next
        Next
    End If
    Set DBase = Nothing
End Sub

Sub CleanEmail(Path As String, Database As String)
    Dim Mfn As Long
    Dim DBase As ClIsisDll
    Dim Occ As Long
    Dim occcount As Long
    Dim aff() As String
    Dim P As Long
    Dim p2 As Long
    Dim email As String
    
    Dim q2 As Long
    Dim Mfns() As Long
    Dim PROCres As String
        
    Dim PROCs() As String
    Dim qPROCs As Long
    Dim ProcPath As String
    Dim ProcFile As String
    Dim j As Long
    
    
    Set DBase = New ClIsisDll
    If DBase.Inicia(Path, Database, Database) Then
        
        fn = 1
        Open DTDs(CurrDTD).ProcFile For Input As fn
        While Not EOF(fn)
            qPROCs = qPROCs + 1
            ReDim Preserve PROCs(qPROCs)
            Line Input #fn, PROCs(qPROCs)
        Wend
        Close fn
        Call SeparateFileandPath(DTDs(CurrDTD).ProcFile, ProcPath, ProcFile)
        
        
        For Mfn = 1 To DBase.MfnQuantity
            occcount = DBase.FieldOccCount(Mfn, 70)
            ReDim aff(occcount)
            For Occ = 1 To occcount
                aff(Occ) = DBase.FieldContentAllOccGet(Mfn, 70, Occ)
                P = InStr(aff(Occ), "^e")
                If P > 0 Then
                    P = P + 2
                    p2 = InStr(P, aff(Occ), "^", vbTextCompare)
                    If p2 > 0 Then
                        email = cleanedemail(Mid(aff(Occ), P, p2 - P))
                        aff(Occ) = Mid(aff(Occ), 1, P - 1) + email + Mid(aff(Occ), p2)
                    Else
                        email = cleanedemail(Mid(aff(Occ), P))
                        aff(Occ) = Mid(aff(Occ), 1, P - 1) + email
                    End If
                End If
            Next
        
        
            For Occ = 1 To occcount
                Call DBase.FieldContentUpdate(Mfn, 70, aff(Occ), 1)
            Next
                
        'proc FILE
            For j = 1 To qPROCs
                PROCres = DBase.UsePft(Mfn, "@" + ProcPath + PathSep + PROCs(j))
                If Len(PROCres) > 0 Then
                    If DBase.UseProc(Mfn, PROCres) Then
                                        
                    End If
                End If
            Next
        Next
    End If
    Set DBase = Nothing
End Sub

Private Function cleanedemail(email As String) As String
    Dim r As String
    Dim P As Long
    Dim rOK As Boolean
    Dim pa As Long
    
    
    r = email
    pa = InStr(1, r, "<a ", vbBinaryCompare)
    
    While pa > 0
        r = Mid(r, pa + 1)
        P = InStr(1, r, ">", vbBinaryCompare)
        If P > 0 Then
            r = Mid(r, P + 1)
            P = InStr(1, r, "</a>", vbBinaryCompare)
            If P > 0 Then
                r = Mid(r, 1, P - 1)
            End If
        End If
        pa = InStr(1, r, "<a ", vbBinaryCompare)
    Wend
    Debug.Print email
        Debug.Print r
    cleanedemail = r
End Function



Sub CreateDoc(Path As String, Database As String, DocPath As String, DocFile As String)
    Dim Mfn As Long
    Dim fn As Long
    Dim fn1 As Long
    Dim fn2 As Long
    Dim result As String
    Dim report As String
    Dim DBase As ClIsisDll
    Dim CIPFILE As String
    Dim CIPPath As String
    Dim P As Long
    Dim i As Long
    Dim Result2 As String
    
    Dim pfts() As String
    Dim qpfts As Long
    Dim PFTPath As String
    Dim PFTFILE As String
    
    Set DBase = New ClIsisDll
    If DBase.Inicia(Path, Database, Database) Then

        'CIP FILE
        Call SeparateFileandPath(DTDs(CurrDTD).CIPFILE, CIPPath, CIPFILE)
        P = InStr(CIPFILE, ".")
        If P > 0 Then CIPFILE = Mid(CIPFILE, 1, P) + "cip"
        If FileExist(CIPPath, CIPFILE) Then
            DBase.AppParSet (CIPPath + PathSep + CIPFILE)
        End If
        
        
        'PFT FILE
        fn = 1
        Open DTDs(CurrDTD).PFTFILE For Input As fn
        While Not EOF(fn)
            qpfts = qpfts + 1
            ReDim Preserve pfts(qpfts)
            Line Input #fn, pfts(qpfts)
        Wend
        Close fn
        Call SeparateFileandPath(DTDs(CurrDTD).PFTFILE, PFTPath, PFTFILE)
        
        fn1 = 2
        fn2 = 3
        
        Open DocPath + PathSep + DocFile + SGMLExt For Output As fn
        Open DocPath + PathSep + DocFile + ParserExt For Output As fn1
        Open DocPath + PathSep + DocFile + ReportExt For Output As fn2
        
        Print #fn1, "<!DOCTYPE " + DTDs(CurrDTD).DocTypeName + " SYSTEM " + Chr(34) + DTDs(CurrDTD).DTDFile + Chr(34) + TAGC
        Print #fn, STAGO + DTDs(CurrDTD).DocTypeName + TAGC
        Print #fn1, STAGO + DTDs(CurrDTD).DocTypeName + TAGC
        Print #fn2, DBase.UsePft(1, "@" + DTDs(CurrDTD).ReportPFTFile)
        
        For Mfn = 2 To DBase.MfnQuantity
            report = ""
            result = ""
            For i = 1 To qpfts
                result = result + DBase.UsePft(Mfn, "@" + PFTPath + "\" + pfts(i))
            Next
            If Len(result) > 0 Then
                Print #fn, result
                Print #fn1, result
                report = "Success|"
            Else
                Debug.Print
            End If
            If Len(report) = 0 Then
                report = "Failure|"
            End If
            report = report + DBase.UsePft(Mfn, "@" + DTDs(CurrDTD).ReportPFTFile)
            Print #fn2, report
        Next
        Print #fn, ETAGO + DTDs(CurrDTD).DocTypeName + TAGC
        Print #fn1, ETAGO + DTDs(CurrDTD).DocTypeName + TAGC
        Close fn, fn1, fn2
    
    End If
    Set DBase = Nothing
    Kill Path + PathSep + Database + MstExt
    Kill Path + PathSep + Database + XrfExt
    
End Sub

Sub Old2CreateDoc(Path As String, Database As String, DocPath As String, DocFile As String)
    Dim Mfn As Long
    Dim fn As Long
    Dim fn1 As Long
    Dim fn2 As Long
    Dim result As String
    Dim report As String
    Dim DBase As ClIsisDll
    Dim CIPFILE As String
    Dim CIPPath As String
    Dim P As Long
    Dim i As Long
    Dim PFTPath As String
    Dim Result2 As String
    
    Set DBase = New ClIsisDll
    If DBase.Inicia(Path, Database, Database) Then
                        
        Call SeparateFileandPath(DTDs(CurrDTD).PFTFILE, CIPPath, CIPFILE)
        
        P = InStr(CIPFILE, ".")
        If P > 0 Then CIPFILE = Mid(CIPFILE, 1, P) + "cip"
        If FileExist(CIPPath, CIPFILE) Then
            DBase.AppParSet (CIPPath + PathSep + CIPFILE)
        End If
        
        fn = 1
        fn1 = 2
        fn2 = 3
        
        Open DocPath + PathSep + DocFile + SGMLExt For Output As fn
        Open DocPath + PathSep + DocFile + ParserExt For Output As fn1
        Open DocPath + PathSep + DocFile + ReportExt For Output As fn2
        
        Print #fn1, "<!DOCTYPE " + DTDs(CurrDTD).DocTypeName + " SYSTEM " + Chr(34) + DTDs(CurrDTD).DTDFile + Chr(34) + TAGC
        Print #fn, STAGO + DTDs(CurrDTD).DocTypeName + TAGC
        Print #fn1, STAGO + DTDs(CurrDTD).DocTypeName + TAGC
            
        
        Print #fn2, DBase.UsePft(1, "@" + DTDs(CurrDTD).ReportPFTFile)
        
        For Mfn = 2 To DBase.MfnQuantity
            result = DBase.UsePft(Mfn, "@" + DTDs(CurrDTD).PFTFILE + ".pft")
            'For i = 1 To DTDs(CurrDTD).PFTCount
                'Result = Result + DBase.UsePft(mfn, "@" + DTDs(CurrDTD).PFTFile + CStr(i) + ".pft")
            'Next
            report = ""
            If Len(result) > 0 Then
                Print #fn, result
                Print #fn1, result
                report = "Success|"
            End If
            If Len(report) = 0 Then
                report = "Failure|"
            End If
            report = report + DBase.UsePft(Mfn, "@" + DTDs(CurrDTD).ReportPFTFile)
            Print #fn2, report
        Next
        Print #fn, ETAGO + DTDs(CurrDTD).DocTypeName + TAGC
        Print #fn1, ETAGO + DTDs(CurrDTD).DocTypeName + TAGC
        Close fn, fn1, fn2
    
    End If
    Set DBase = Nothing
    Kill Path + PathSep + Database + MstExt
    Kill Path + PathSep + Database + XrfExt
    
End Sub

Sub OldCreateDoc(Path As String, Database As String, DocPath As String, DocFile As String)
    Dim Mfn As Long
    Dim fn As Long
    Dim fn1 As Long
    Dim fn2 As Long
    Dim fn3 As Long
    Dim result As String
    Dim report As String
    Dim DBase As ClIsisDll
    Dim CIPFILE As String
    Dim CIPPath As String
    Dim P As Long
    Dim i As Long
    Dim pft(3) As String
    Dim PFTPath As String
    Dim Result2 As String
    
    Set DBase = New ClIsisDll
    If DBase.Inicia(Path, Database, Database) Then
                        
        Call SeparateFileandPath(DTDs(CurrDTD).PFTFILE, CIPPath, CIPFILE)
        
        P = InStr(CIPFILE, ".")
        If P > 0 Then CIPFILE = Mid(CIPFILE, 1, P) + "cip"
        If FileExist(CIPPath, CIPFILE) Then
            DBase.AppParSet (CIPPath + PathSep + CIPFILE)
        End If
        
        fn = 1
        fn1 = 2
        fn2 = 3
        fn3 = 4
        
        Open DocPath + PathSep + DocFile + SGMLExt For Output As fn
        Open DocPath + PathSep + DocFile + ParserExt For Output As fn1
        Open DocPath + PathSep + DocFile + ReportExt For Output As fn2
        Open DocPath + PathSep + DocFile + ".htm" For Output As fn3
        
        Print #fn1, "<!DOCTYPE " + DTDs(CurrDTD).DocTypeName + " SYSTEM " + Chr(34) + DTDs(CurrDTD).DTDFile + Chr(34) + TAGC
        Print #fn3, "<html><body>"
        Print #fn, STAGO + DTDs(CurrDTD).DocTypeName + TAGC
        Print #fn1, STAGO + DTDs(CurrDTD).DocTypeName + TAGC
            
        
        Print #fn2, DBase.UsePft(1, "@" + DTDs(CurrDTD).ReportPFTFile)
        Print #fn3, DBase.UsePft(1, "@" + DTDs(CurrDTD).CIPFILE + ".pft")
        
        For Mfn = 2 To DBase.MfnQuantity
            result = DBase.UsePft(Mfn, "@" + DTDs(CurrDTD).PFTFILE + ".pft")
            'For i = 1 To DTDs(CurrDTD).PFTCount
                'Result = Result + DBase.UsePft(mfn, "@" + DTDs(CurrDTD).PFTFile + CStr(i) + ".pft")
            'Next
            report = ""
            If Len(result) > 0 Then
                Print #fn, result
                Print #fn1, result
                Result2 = DBase.UsePft(Mfn, "@" + DTDs(CurrDTD).CIPFILE + ".pft")
                If Len(Result2) > 0 Then
                    Print #fn3, Result2
                    report = "Success|"
                End If
            End If
            If Len(report) = 0 Then
                report = "Failure|"
            End If
            report = report + DBase.UsePft(Mfn, "@" + DTDs(CurrDTD).ReportPFTFile)
            Print #fn2, report
        Next
        Print #fn, ETAGO + DTDs(CurrDTD).DocTypeName + TAGC
        Print #fn1, ETAGO + DTDs(CurrDTD).DocTypeName + TAGC
        Print #fn3, "</body></html>"
        
        Close fn, fn1, fn2, fn3
    
    End If
    Set DBase = Nothing
    Kill Path + PathSep + Database + MstExt
    Kill Path + PathSep + Database + XrfExt
    
End Sub

Sub CreateHTML(DocPath As String, DocFile As String)
    Dim fn As Long
    Dim fn3 As Long
    Dim SGMLContent As String
    
    
    fn = 1
    fn3 = 2
    Open DocPath + PathSep + DocFile + ".htm" For Output As fn3
    Print #fn3, "<html><body>"
    
    Open DocPath + PathSep + DocFile + ".sgml" For Input As fn
    While Not EOF(fn)
        Line Input #fn, SGMLContent
        
        Print #fn3, ConvertSGML2HTML(SGMLContent)
    Wend
    Print #fn3, "</body></html>"
    Close fn, fn3
    
End Sub

Private Function ConvertSGML2HTML(content As String) As String
    Dim P As Long
    Dim p2 As Long
    Dim aux As String
    Dim r As String
    
    aux = content
    P = InStr(aux, "<")
    While P > 0
        p2 = InStr(aux, ">")
        r = r + Mid(aux, 1, P - 1) + DTDs(CurrDTD).COLOREDTAG(Mid(aux, P, p2 - P + 1))
        aux = Mid(aux, p2 + 1)
        P = InStr(aux, "<")
    Wend
    
    ConvertSGML2HTML = r + "<br>"
End Function
Function GetValidRecords(SourcePath As String, SourceDB As String, DestPath As String, DestDB As String) As Long
    Dim i As Long
    Dim DB As ClIsisDll
    Dim NewDB As ClIsisDll
    Dim q As Long
    Dim order As String
    Dim Mfns() As Long

    Set DB = New ClIsisDll
    If DB.Inicia(SourcePath, SourceDB, "Source Database") Then
        If DB.IfCreate(SourceDB) Then
            Set NewDB = New ClIsisDll
            If NewDB.Inicia(DestPath, DestDB, "NewDB DestDB", True) Then
                FileCount = NewDB.RecordSave(DB.RecordGet(1))
                q = DB.UsePft(1, "v122")
                
                For i = 1 To q
                    If i < 10 Then
                        order = "0" + CStr(i)
                    Else
                        order = CStr(i)
                    End If
                    q2 = DB.MfnFind(order, Mfns)
                    If q2 = 1 Then
                        FileCount = NewDB.RecordSave(DB.RecordGet(Mfns(q2) + 1))
                        
                    End If
                Next
            End If
            Set NewDB = Nothing
        End If
    End If
    Set DB = Nothing
    
    GetValidRecords = FileCount
End Function

Function GetValidRecords2(SourcePath As String, SourceDB As String, DestPath As String, DestDB As String) As Long
    Dim Mfn As Long
    Dim i As Long
    Dim DB As ClIsisDll
    Dim NewDB As ClIsisDll
    Dim tpreg As String
    Dim FileCount As Long
        
    Set DB = New ClIsisDll
    If DB.Inicia(SourcePath, SourceDB, "Source Database") Then
    
        If FileExist(SourcePath, SourceDB + ".fst") Then Call FileCopy(SourcePath + PathSep + SourceDB + ".fst", DestPath + PathSep + DestDB + ".fst")
            
        Set NewDB = New ClIsisDll
        If NewDB.Inicia(DestPath, DestDB, "NewDB DestDB", True) Then
                'If NewDB.IfCreate(DestDB) Then
                'End If
                
            tpreg = DB.UsePft(1, "v706")
            If tpreg = "i" Then
                i = NewDB.RecordSave(DB.RecordGet(1))
                'Call NewDB.IfUpdate(i, i)
                FileCount = FileCount + 1
            End If
                
            For Mfn = 2 To DB.MfnQuantity
                tpreg = DB.UsePft(Mfn, "v706")
                If tpreg = "h" Then
                    i = NewDB.RecordSave(DB.RecordGet(Mfn))
                    'Call NewDB.IfUpdate(i, i)
                    FileCount = FileCount + 1
                End If
            Next
        End If
        Set NewDB = Nothing
    End If
    Set DB = Nothing
    
    GetValidRecords2 = FileCount
End Function

Function IssueFullPath(Siglum As String, vol As String, supplvol As String, nro As String, supplnro As String) As String
    Dim Path As String
    Dim Id As String
    
    Id = IssueId(vol, supplvol, nro, supplnro)
    If Len(Id) > 0 Then
        Path = SerialDirectory + PathSep + Siglum + PathSep + Id
        If Not DirExist(Path, "Issue Path") Then
            Path = ""
        End If
    End If
    
    IssueFullPath = Path
End Function

Function IssueId(vol As String, supplvol As String, nro As String, supplnro As String) As String
    Dim Id As String
    
    If Len(vol) > 0 Then Id = "v" + vol
    If Len(supplvol) > 0 Then Id = Id + "s" + supplvol
    If Len(nro) > 0 Then Id = Id + "n" + nro
    If Len(supplnro) > 0 Then Id = Id + "s" + supplnro

    IssueId = Id
End Function

Sub CopyFilestoPubmedDirectory(Path As String, Database As String)
    Call FileCopy(Path + PathSep + Database + ".sgml", SerialDirectory + PathSep + PubMedDIR + PathSep + Database + ".sgml")
End Sub

