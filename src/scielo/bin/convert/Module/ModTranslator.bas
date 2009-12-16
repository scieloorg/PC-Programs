Attribute VB_Name = "ModTranslator"


Public AppHandle As Long
Public CurrDTD As String
Public DTDs As ColDTD


Const DTDInfoFile = "dtdinfo.txt"

Const OpenFont = "<FONT "
Const CloseFont = "</FONT>"

Const GizmoMarkupStart = "<REPLACESYMBOL>"
Const GizmoMarkupEnd = "</REPLACESYMBOL>"

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
    Dim PFTFile As String
    Dim PFTCount As Long
    Dim ReportPFTFile As String
    Dim SGM2ASC As String
    Dim SubSup2ASC As String
    Dim IMG2ASC As String
    Dim RECOVER_REPLACESYMBOL As String
    Dim ASC2SGM As String
    Dim DTD As ClDTD
    Dim Exist As Boolean
    Dim i As Long
    Dim P As Long
    
    fn = 1
    Open DTDInfoFile For Input As fn
    
    Set DTDs = New ColDTD
    While Not EOF(fn)
        'name,dtdfile,pftfile,pft relatorio,extensao relatorio,gizmo,validrecords,recidfield,FileNamePft,docipfile
        Input #fn, DTDName, DocTypeName, DTDFile, PFTFile, PFTCount, ReportPFTFile, SGM2ASC, SubSup2ASC, IMG2ASC, RECOVER_REPLACESYMBOL, ASC2SGM
        
        
        Set DTD = New ClDTD
        Set DTD = DTDs(DTDName, Exist)
        If Not Exist Then
            Set DTD = DTDs.Add(DTDName)
            DTD.name = DTDName
            DTD.DocTypeName = DocTypeName
            DTD.DTDFile = DTDFile
            DTD.PFTFile = PFTFile
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

Function FindImg(DBPath As String, DBFile As String, ImageAddress() As String, ImageShortAddress() As String, ImageReplace() As String) As Long
    Dim P1 As Long
    Dim p2 As Long
    Dim Result As String
    Dim Img As String
    Dim img2 As String
    Dim DBase As ClIsisDll
    Dim mfn As Long
    Dim P As Long
    Dim IMGFile As String
    Dim ImgCounter As Long
    Dim count As Long
            
    Dim mfns() As Long
    Dim q As Long
    Dim i As Long
    
            
    Set DBase = New ClIsisDll
    If DBase.Inicia(DBPath, DBFile, DBFile) Then
        IMGFile = DBFile + ImgSuf
        q = DBase.MfnFind(CHANGE_SYMBOL, mfns)
        For i = 1 To q
            mfn = mfns(i)
            Result = DBase.RecordGet(mfn)
            P1 = 0
            P1 = InStr(P1 + 1, Result, TagImg, vbTextCompare)
            While P1 > 0
                p2 = InStr(P1, Result, TAGC, vbBinaryCompare)
                Img = Mid(Result, P1, p2 - P1 + 1)
                P = InStr(Img, PathSepUnix)
                While P > 0
                    img2 = Mid(Img, P + 1)
                    P = InStr(P + 1, Img, PathSepUnix, vbBinaryCompare)
                Wend
                img2 = DBPath + PathSep + ImgSuf + PathSep + Mid(img2, 1, InStr(2, img2, Chr(34)) - 1)
                
                count = ImgCounter
                Call InsElem(ImageAddress, ImgCounter, Img)
                If count < ImgCounter Then
                    ReDim Preserve ImageShortAddress(ImgCounter)
                    ReDim Preserve ImageReplace(ImgCounter)
                    'ImageAddress(ImgCounter) = Img
                    ImageShortAddress(ImgCounter) = img2
                End If
                P1 = InStr(P1 + 1, Result, TagImg, vbTextCompare)
            Wend
        Next
        'Close fn1
        'Close fn2
    End If
    Set DBase = Nothing
    FindImg = ImgCounter
End Function

Function FindSUBSUP(DBPath As String, DBFile As String, SUBSUPTAGs() As String, SUBSUPReplace() As String, SUBSUPContext() As String) As Long
    Dim P1 As Long
    Dim p2 As Long
    Dim P3 As Long
    Dim P4 As Long
    Dim Result As String
    Dim SUBSUP As String
    Dim SUBSUP2 As String
    Dim DBase As ClIsisDll
    Dim mfn As Long
    Dim P As Long
    Dim SUBSUPCounter As Long
    
    Dim mfns() As Long
    Dim q As Long
    Dim i As Long
    
    Set DBase = New ClIsisDll
    If DBase.Inicia(DBPath, DBFile, DBFile) Then
        q = DBase.MfnFind(CHANGE_SYMBOL, mfns)
        For i = 1 To q
            mfn = mfns(i)
            
            Result = DBase.RecordGet(mfn)
            Result = ReplaceString(Result, "<sub> ", " <SUB>", vbTextCompare)
            Result = ReplaceString(Result, " </sub>", "</SUB> ", vbTextCompare)
            Result = ReplaceString(Result, "<sub>", "<SUB>", vbTextCompare)
            Result = ReplaceString(Result, "</sub>", "</SUB>", vbTextCompare)
            Result = ReplaceString(Result, "<sup> ", " <SUP>", vbTextCompare)
            Result = ReplaceString(Result, " </sup>", "</SUP> ", vbTextCompare)
            Result = ReplaceString(Result, "<sup>", "<SUP>", vbTextCompare)
            Result = ReplaceString(Result, "</sup>", "</SUP>", vbTextCompare)
            
            Call DBase.RecordUpdate(mfn, Result)
            
            Call InsSubSup(SUBSUPTAGs, SUBSUPReplace, SUBSUPContext, SUBSUPCounter, Result, "<SUB>", "</SUB>")
            Call InsSubSup(SUBSUPTAGs, SUBSUPReplace, SUBSUPContext, SUBSUPCounter, Result, "<SUP>", "</SUP>")
            
        Next
        'Close fn1
        'Close fn2
        
    End If
    Set DBase = Nothing
    FindSUBSUP = SUBSUPCounter
End Function

Private Sub InsSubSup(SUBSUPTAGs() As String, SUBSUPReplace() As String, SUBSUPContext() As String, SUBSUPCounter As Long, content As String, TAG1 As String, TAG2 As String)
    Dim P1 As Long
    Dim p2 As Long
    Dim pTAG1 As Long
    Dim pTAG2 As Long
    Dim SUBSUP As String
    Dim P As Long
    Dim pos As Long
    Dim q As Long
    Dim PrevChar As String
    Dim NextChar As String
    Dim s1 As String
    Dim s2 As String
    Dim s3 As String
    Dim br1 As String
    Dim br2 As String
    Dim br3 As String
    Dim Counter As Long
    Dim Context As String
    
            
        P1 = InStr(1, content, TAG1, vbBinaryCompare)
        While P1 > 0
            p2 = InStr(P1, content, TAG2, vbBinaryCompare)
            
            If P1 > 10 Then
                Context = Mid(content, P1 - 10, p2 + Len(TAG2) - P1 + 12)
            Else
                Context = Mid(content, 1, p2 + Len(TAG2) - P1 + 2)
            End If
            
            PrevChar = Mid(content, P1 - 1, 1)
            NextChar = Mid(content, p2 + Len(TAG2), 1)
            SUBSUP = Mid(content, P1 - 1, p2 + Len(TAG2) - P1 + 2)
            
            If PrevChar = ">" Then SUBSUP = Mid(SUBSUP, 2)
            If NextChar = "<" Then SUBSUP = Mid(SUBSUP, 1, Len(SUBSUP) - 1)
                        
            pTAG1 = InStr(SUBSUP, TAG1)
            pTAG2 = InStr(pTAG1, SUBSUP, TAG2, vbBinaryCompare)
                            
            Counter = SUBSUPCounter
            Call InsElem(SUBSUPTAGs, SUBSUPCounter, SUBSUP)
                
            If Counter < SUBSUPCounter Then
                ReDim Preserve SUBSUPReplace(SUBSUPCounter)
                ReDim Preserve SUBSUPContext(SUBSUPCounter)
                
                s1 = Mid(SUBSUP, pTAG1 + Len(TAG1), pTAG2 - pTAG1 - Len(TAG1))
                If Len(s1) > 0 Then s2 = Mid(s1, Len(s1))
                s3 = Mid(s1, 1, 2)
                s1 = Mid(s1, 1, 1)
                
                If (PrevChar Like "[A-Z]") And (s1 Like "[A-Z]") Then
                    br1 = " "
                ElseIf (PrevChar Like "[a-z]") And (s1 Like "[a-z]") Then
                    br1 = " "
                ElseIf (PrevChar Like "[0-9]") And (s1 Like "[0-9]") Then
                    br1 = "("
                ElseIf (PrevChar Like "[0-9]") And (s3 Like "[-+][0-9]") Then
                    br1 = "("
                Else
                    br1 = ""
                End If
                
                If (s2 Like "[A-Z]") And (NextChar Like "[A-Z]") Then
                    br2 = " "
                ElseIf (s2 Like "[a-z]") And (NextChar Like "[a-z]") Then
                    br2 = " "
                ElseIf (s2 Like "[0-9]") And (NextChar Like "[0-9]") Then
                    br2 = ")"
                'ElseIf (s2 Like "[0-9]") And (NextChar Like "[-+]") Then
                  '   br2 = ")"
                Else
                    br2 = ""
                End If
                
                If br1 = "(" Then br2 = ")"
                If br1 = ")" Then br2 = "("
                
                SUBSUPReplace(SUBSUPCounter) = Mid(SUBSUP, 1, pTAG1 - 1) + br1 + Mid(SUBSUP, pTAG1 + 5, pTAG2 - pTAG1 - 5) + br2 + Mid(SUBSUP, pTAG2 + 6)
                SUBSUPContext(SUBSUPCounter) = Context
            End If
            
            P1 = InStr(P1 + 1, content, TAG1, vbTextCompare)
        Wend
            
End Sub


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
    Dim mfn As Long
    Dim DBase As ClIsisDll
    Dim P As Long
    Dim Img As String
    Dim img2 As String
    
    Set DBase = New ClIsisDll
    If DBase.Inicia(ImgGzmPath, ImgGzmFile, ImgGzmFile) Then
        ReDim Preserve ImageAddress(DBase.MfnQuantity)
        ReDim Preserve ImageShortAddress(DBase.MfnQuantity)
        ReDim Preserve ImageReplace(DBase.MfnQuantity)
        
        For mfn = 1 To DBase.MfnQuantity
            ImageAddress(mfn) = DBase.UsePft(mfn, GzmField1)
            ImageReplace(mfn) = DBase.UsePft(mfn, GzmField2)
            
            Img = ImageAddress(mfn)
            P = InStr(Img, PathSepUnix)
            While P > 0
                img2 = Mid(Img, P + 1)
                P = InStr(P + 1, Img, PathSepUnix, vbBinaryCompare)
            Wend
            ImageShortAddress(mfn) = ImgGzmPath + PathSep + ImgSuf + PathSep + Mid(img2, 1, InStr(2, img2, Chr(34)) - 1)
        Next
    End If
    GzmImages = DBase.MfnQuantity
    Set DBase = Nothing
    
End Function

Function GzmSUBSUP(SUBSUPGzmPath As String, SUBSUPGzmFile As String, SUBSUPTAGs() As String, SUBSUPReplace() As String) As Long
    Dim mfn As Long
    Dim DBase As ClIsisDll
    Dim P As Long
    Dim Img As String
    Dim img2 As String
    Dim Counter As Long
    Dim i As Long
    
    Set DBase = New ClIsisDll
    If DBase.Inicia(SUBSUPGzmPath, SUBSUPGzmFile, SUBSUPGzmFile) Then
        For mfn = 1 To DBase.MfnQuantity
            i = Counter
            Call InsElem(SUBSUPTAGs, Counter, DBase.UsePft(mfn, GzmField1))
            If i < Counter Then
                ReDim Preserve SUBSUPReplace(Counter)
                SUBSUPReplace(Counter) = DBase.UsePft(mfn, GzmField2)
            End If
        Next
    End If
    Set DBase = Nothing
    GzmSUBSUP = Counter
End Function

Private Sub CreateGzm(GzmPath As String, GzmFile As String, Address() As String, Replace() As String, Counter As Long)
    Dim mfn As Long
    Dim DBase As ClIsisDll
    
    Set DBase = New ClIsisDll
    If DBase.Inicia(GzmPath, GzmFile, Chr(32), True) Then
        For mfn = 1 To Counter
            Call DBase.RecordSave("<1>" + Address(mfn) + "</1><2>" + Replace(mfn) + "</2>")
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

Sub ConvertDBtoDoc(DBPath As String, DBFile As String)
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
    
    
    With DTDs(CurrDTD)
    If FileExist(DBPath, .IMG2ASC + MstExt) Then Kill DBPath + PathSep + .IMG2ASC + ALLFiles
        
    SUBSUPCount = FindSUBSUP(DBPath, DBFile, SUBSUP_tag, SUBSUPReplace, SUBSUPContext)
    If SUBSUPCount > 0 Then
        GzmSUBSUPCount = GzmSUBSUP(DBPath, .SubSup2ASC, GzmSUBSUPAddr, GzmSUBSUPReplace)
        If GzmSUBSUPCount > 0 Then
            Call CompareGzm(GzmSUBSUPAddr, GzmSUBSUPReplace, GzmSUBSUPCount, SUBSUP_tag, SUBSUPReplace, SUBSUPCount)
        End If
        Call FrmSubp.setTAGSUBSUPs(SUBSUP_tag, SUBSUPReplace, SUBSUPContext, SUBSUPCount)
        Call CreateGzm(DBPath, .SubSup2ASC, SUBSUP_tag, SUBSUPReplace, SUBSUPCount)
    End If
    
    DBImgCount = FindImg(DBPath, DBFile, DBImgAddr, DBImgShortAddr, DBImgReplace)
    If DBImgCount > 0 Then
        
        GzmImgFile = DBFile + ImgSuf
        If FileExist(DBPath, GzmImgFile + MstExt) Then
            GzmImgCount = GzmImages(DBPath, GzmImgFile, GzmImgAddr, GzmImgShortAddr, GzmImgReplace)
        End If
        If GzmImgCount > 0 Then
            Call CompareGzm(GzmImgAddr, GzmImgReplace, GzmImgCount, DBImgAddr, DBImgReplace, DBImgCount)
        End If
        Call FrmImage.setImages(DBImgAddr, DBImgShortAddr, DBImgReplace, DBImgCount)
        Call CreateGzm(DBPath, GzmImgFile, DBImgAddr, DBImgReplace, DBImgCount)
        Call CreateGzm(DBPath, .IMG2ASC, DBImgAddr, DBImgReplace, DBImgCount)
        
    End If
    
    Call ReplaceSpecialCharacters(DBPath, DBFile)
    
    
    End With
    
End Sub

Sub ReplaceSpecialCharacters(Path As String, database As String)
    Dim mfn As Long
    Dim NewContents As String
    Dim DBase As ClIsisDll
    
    Set DBase = New ClIsisDll
    If DBase.Inicia(Path, database, database) Then
        Call DBase.Gizmo(Path + PathSep + DTDs(CurrDTD).SubSup2ASC)
        Call DBase.Gizmo(Path + PathSep + DTDs(CurrDTD).SubSup2ASC)
        If FileExist(Path, DTDs(CurrDTD).IMG2ASC + ".mst") Then Call DBase.Gizmo(Path + PathSep + DTDs(CurrDTD).IMG2ASC)
                      
        'ProcMsg.GiveRunInformation ("Converting SGML 2 ASCII.")
        Call DBase.Gizmo(DTDs(CurrDTD).SGM2ASC)
            
        'ProcMsg.GiveRunInformation ("Replace Font Face Symbol.")
        For mfn = 1 To DBase.MfnQuantity
            NewContents = DBase.RecordGet(mfn)
            NewContents = ReplaceFontFaceSymbol(NewContents)
            If DBase.RecordUpdate(mfn, NewContents) Then
            End If
        Next
        
        'ProcMsg.GiveRunInformation ("Converting ASCII2SGML")
        'Call DBase.Gizmo(DTDs(CurrDTD).ASC2SGM)
        
        'ProcMsg.GiveRunInformation ("Converting Grk2SGML")
        'Call DBase.Gizmo(DTDs(CurrDTD).RECOVER_REPLACESYMBOL)
        
    End If
    Set DBase = Nothing
End Sub

Private Function ReplaceFontFaceSymbol(OldLine As String) As String
    Dim pOpenFont1 As Long
    Dim pOpenFont2 As Long
    Dim pCloseFont1 As Long
    Dim SYMBOL As String
    Dim Line As String
    Dim TagFONT As String
    
        
    Line = OldLine
    pOpenFont1 = InStr(1, Line, OpenFont, vbTextCompare)
        
    While pOpenFont1 > 0
        pOpenFont2 = InStr(pOpenFont1, Line, TAGC)
        If pOpenFont2 > 0 Then
            TagFONT = Mid(Line, pOpenFont1, pOpenFont2 - pOpenFont1)
            pCloseFont1 = InStr(pOpenFont2, Line, CloseFont, vbTextCompare)
            SYMBOL = Trim(Mid(Line, pOpenFont2 + 1, pCloseFont1 - pOpenFont2 - 1))
            
            If InStr(1, TagFONT, "symbol", vbTextCompare) > 0 Then
                Line = Mid(Line, 1, pOpenFont1 - 1) + GizmoMarkupStart + SYMBOL + GizmoMarkupEnd + Mid(Line, pCloseFont1 + Len(CloseFont))
            Else
                Line = Mid(Line, 1, pOpenFont1 - 1) + SYMBOL + Mid(Line, pCloseFont1 + Len(CloseFont))
            End If
        End If
        pOpenFont1 = InStr(1, Line, OpenFont, vbTextCompare)
    Wend
    ReplaceFontFaceSymbol = Line
End Function
