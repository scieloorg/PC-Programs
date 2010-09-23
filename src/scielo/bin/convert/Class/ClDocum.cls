VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClDocum"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

Private privateContent As ClContent



Const CONST_CARRET = "&#094;"
Const TagFech = "]"
Const TagInicialAbre = "["
Const TagFinalAbre = "[/"

Const WIN_FORMAT = "0"
Const PARTIAL_HTML = "1"
Const FULL_HTML = "2"
Const DOS_FORMAT = "3"
Const WIN_AND_IDIOM_DEPENDENT_FORMAT = "4"
Const DOS_AND_IDIOM_DEPENDENT_FORMAT = "5"
Const DOS_FORMAT_FNAME = "6"
Const DOS_FORMAT_SURNAME = "7"
Const DOS_FORMAT_STITLE = "8"
Const WIN_FORMAT_TABLE = "9"


Const TamMaxParag = 7000
Const STANDARDIZEDENDPARAG = "[STANDARDIZEDENDPARAG]"
Const BVSLAWBREAKMARK = "^qp"

Const ConfigFile = "cfg.sci"
Private ConfigPath As String
Private TmpDocFile As String
    
Private DBRecords As ColRegistro
Private RepeatInAllRecords As ColRegistro
Private IdiomDependentFields As ClSortList
Private LinkedFields As ColLink
Private SortedRecords As ColRegistro

Private References() As String
Private ReferencesCounter As Long

Private LinkMarkup2Body As ColPair
Private LinkMark As ColPair

Private ParserResult As String

Private FullTextFile As String
Private FullTextPath As String


Private MARKUP_Text As ClTxt
Private BODY_Text As ClTxt

Private CompressedInfo As ClTxt
Private CompressionInfo() As String

Private REFTAGEND   As String
Private REFTAGSTART   As String
 
Private DTDCurrent As ClDTD

Private BlockTags() As String
Private BlockTagsCount As Long

Private FindWhat(6) As String

Private RecordInfo As ColRecordInfo

Public docOrder As String

Private LawStructure As ColRegistro

Private mvarArticle As ClsArticle
Private previousDocument As ClsArticle
Private PreviousIssue As ClsRelatedIssues

Public ArticleAction As New ClsArticleAction



'-----------------------------------------------------------------------
'ConvertBODYintoPARAGRAPH   - convert the body bodycontent into various paragraphs
'bodycontent   - body bodycontent
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Private Sub ConvertBODYintoPARAGRAPH(bodycontent As String, RecordType As String, Field As Long, Subf As String, format As String, counter As Long)

    Set BODY_Text = New ClTxt
    bodycontent = BODY_StandardizeEndParag(bodycontent, STANDARDIZEDENDPARAG)
        
    'change the presentation format of the bodycontent according to the conversion tables
    Select Case format
    Case WIN_FORMAT
        bodycontent = Convert2Win(bodycontent)
    
    Case PARTIAL_HTML
        bodycontent = RmPartialHTML(bodycontent, True)
    
    Case FULL_HTML
        'bodycontent = RmPartialHTML(bodycontent, True)
    
    Case Else
    End Select
    
    bodycontent = ReplaceString(Trim(bodycontent), "  ", " ", vbTextCompare)
    
    BODY_Text.AddLines (bodycontent)
    counter = BODY_GetParagraphs(RecordType, Field, Subf, "", counter)
    

End Sub

'--------------------------------------------------------------------
'Read   - read the full text
'Path   - path file
'File   - file name
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Private Function BODY_READ(Path As String, File As String) As Boolean
    Dim ret As Boolean
    Dim fn As Long
    Dim s As String
    Dim i As Long
    Dim endi As Long
    Dim endj As Long

    If FileExist(Path, File, "Fulltext") Then
        Set BODY_Text = New ClTxt
        Set CompressedInfo = New ClTxt
        
        FullTextPath = Path
        FullTextFile = File
        
        fn = FreeFile(1)
        Open Path + PathSep + File For Input As fn
        Do Until EOF(fn)
            Line Input #fn, s
            s = s + CONST_SPACE_END_for_HTML
            s = BODY_StandardizeEndParag(s, STANDARDIZEDENDPARAG)
            
            s = ReplaceString(ReplaceString(s, "&amp;#093;", "&#093;", vbBinaryCompare), "&amp;#091;", "&#091;", vbBinaryCompare)
            BODY_Text.AddLines (s)
            If ReferencesCounter > 0 Or LinkMarkup2Body.Count > 0 Then
                CompressedInfo.AddLines (s)
            End If
        Loop
        Close fn
        
        If ReferencesCounter > 0 Or LinkMarkup2Body.Count > 0 Then
            'Replace the entities sgml by spaces, in order to match the references of the markup
            'document and of the body document
            Set CompressedInfo = CompressedInfo.ReplaceEntitybySpaces(ASCIIList)
            
            'Replace the tags html by spaces, in order to match the references of the markup
            'document and of the body document
            Set CompressedInfo = CompressedInfo.ReplaceAllHTMLbySpaces
            
            'Compress the lines, eliminating the spaces between the words, in order to match
            'the references of the markup document and body document
            Call CompressedInfo.GetEnd(endi, endj)
            ReDim CompressionInfo(endi)
            For i = 1 To endi
                CompressedInfo.SetLine(i) = BODY_CompressLine(CompressedInfo.GetLine(i), CompressionInfo(i))
            Next
        End If
        ret = True
    End If
    
    BODY_READ = ret
End Function

'-----------------------------------------------------------------------
'BODY_GetParagraphs  - obtém parágrafos do BODY_Text completo
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Private Function BODY_GetParagraphs(RecordType As String, Field As Long, Subf As String, Complement As String, counter As Long) As Long
    Dim ret         As Boolean
    Dim Parag()     As String
    Dim TagParag    As String
    Dim P           As TpPosition
    Dim LimInf      As TpPosition
    Dim LimSup      As TpPosition
    Dim ParagIni    As TpPosition
    Dim ParagEnd    As TpPosition
    Dim QtdParag    As Long
    Dim j           As Long
    Dim prossegue   As Boolean
    Dim s           As String
    Dim PRefMark1   As Long
    Dim PRefMark2   As Long
    Dim Mark        As String
    'Dim counter     As Long
    
    
    'Obtem o body html sem tags de marcacao
    With BODY_Text
    LimInf.i = 1
    LimInf.j = 1
    Call .GetEnd(LimSup.i, LimSup.j)
    If .GetLen(LimInf.i, LimInf.j, LimSup.i, LimSup.j) > 0 Then
        Call .InString(LimInf.i, LimInf.j, LimSup.i, LimSup.j, "<body", P.i, P.j, vbTextCompare)
        If P.j > 0 Then
            Call .InString(P.i, P.j, LimSup.i, LimSup.j, ">", LimInf.i, LimInf.j, 1)
            Call .ForwardPosition(LimInf.i, LimInf.j, 1)
            Call .InString(LimInf.i, LimInf.j, LimSup.i, LimSup.j, "</body", P.i, P.j, vbTextCompare)
            LimSup = P
            Call .RewardPosition(LimSup.i, LimSup.j, 1)
        End If

        '--counter = 0
        prossegue = .ExisteStr(LimInf.i, LimInf.j, LimSup.i, LimSup.j)
        While prossegue
            TagParag = BODY_FindNewParagraph(LimInf, LimSup, P)
            ParagIni = LimInf
            LimInf = P
            If P.j > 0 Then
                Call .ForwardPosition(LimInf.i, LimInf.j, Len(TagParag))  'obtem o novo ParagIni
                'ParagEnd = LimInf 'obtem o ParagEnd parcial
                ParagEnd = P 'obtem o ParagEnd parcial
                Call .RewardPosition(ParagEnd.i, ParagEnd.j, 1)
            Else
                ParagEnd = LimSup
                prossegue = False
            End If
            QtdParag = BODY_GetParagraph(ParagIni, ParagEnd, Parag)
            
            For j = 1 To QtdParag - 1
                Call BODY_BuildParagraphRecord(Parag(j), Complement, RecordType, counter, Field, Subf)
            Next
            
            If QtdParag > 0 Then Call BODY_BuildParagraphRecord(Parag(QtdParag), Complement, RecordType, counter, Field, Subf)
        Wend
    End If
    End With
    
    Set BODY_Text = Nothing
    BODY_GetParagraphs = counter
End Function

'-----------------------------------------------------------------------
'BODY_BuildParagraphRecord - Build the paragraph record
'Parag  - content of the paragraph
'Counter - counter of the paragraph, it also counts the paragraph records
'-----------------------------------------------------------------------
Private Sub BODY_BuildParagraphRecord(Parag As String, OptionalComplement As String, RecordType As String, counter As Long, Field As Long, ByVal Subf As String)
    Dim pRefCount As Long
    Dim Marks()        As String
    Dim Paragraphs() As String
    Dim i As Long
    
    If (Len(Trim(Parag)) > 0) Then
        
        pRefCount = BODY_SplitParagraphWhichHasMoreThanOneReference(Parag, Marks, Paragraphs)
        For i = 1 To pRefCount
            Call BODY_BuildParagraphRecordXXX(Paragraphs(i), OptionalComplement, RecordType, counter, Field, Subf, Marks(i))
        Next
        
        Call BODY_BuildParagraphRecordXXX(Parag, OptionalComplement, RecordType, counter, Field, Subf)
    End If
End Sub
'-----------------------------------------------------------------------
'BODY_BuildParagraphRecord - Build the paragraph record
'Parag  - content of the paragraph
'Counter - counter of the paragraph, it also counts the paragraph records
'-----------------------------------------------------------------------
Private Sub BODY_BuildParagraphRecordXXX(Parag As String, OptionalComplement As String, RecordType As String, counter As Long, Field As Long, ByVal Subf As String, Optional Mark As String)
    Dim pMark1   As Long
    Dim pMark2   As Long
    Dim Paragraphs() As String
    
    Dim found As Boolean
    Dim Item As ClRegistro
    Dim i As Long
    
    
    If (Len(Trim(Parag)) > 0 Or Len(Mark) > 0) Then
        counter = counter + 1
        
        
        Set Item = New ClRegistro
        Set Item = DBRecords.Add(RecordType + CStr(counter), RecordType, counter)
        If Len(Mark) > 0 Then
            Call Item.fields.Add(, Trim(BV(Currbv).BVISISTAGS("ref").Value), Mark, RecordType, CStr(counter))
        End If

        'Record of link
        i = 0
        found = False
        While (i < LinkMark.Count) And (Not found)
            i = i + 1
            pMark1 = InStr(Parag, LinkMark(i).elem1)
            pMark2 = InStr(Parag, LinkMark(i).elem2)
            
            If (pMark1 > 0) And (pMark2 > pMark1) Then
                Mark = Mid(Parag, pMark1 + Len(LinkMark(i).elem1), pMark2 - pMark1 - Len(LinkMark(i).elem1))
                Parag = Mid(Parag, 1, pMark1 - 1) + Mid(Parag, pMark2 + Len(LinkMark(i).elem2))
                Call Item.fields.Add(, LinkMark(i).elem3, Mark, RecordType, CStr(counter))
                found = True
            End If
        Wend
        
        'Build the paragraph record
        Parag = ReplaceString(Parag, CONST_SUBFIELDINDICATOR, CONST_CARRET, vbBinaryCompare)
        If Len(Subf) > 0 Then Subf = "^" + Subf
        Call Item.fields.Add(, Field, Subf + Parag + OptionalComplement, RecordType, CStr(counter))
        
        Set Item = Nothing
    End If
End Sub
'-----------------------------------------------------------------------
'BODY_BuildParagraphRecord - Build the paragraph record
'Parag  - content of the paragraph
'Counter - counter of the paragraph, it also counts the paragraph records
'-----------------------------------------------------------------------
Private Function BODY_SplitParagraphWhichHasMoreThanOneReference(Parag As String, Marks() As String, Paragraphs() As String) As Long
    Dim pMark1   As Long
    Dim pMark2   As Long
    Dim i As Long
    
    If (Len(Trim(Parag)) > 0) Then
        
        pMark1 = InStr(Parag, REFTAGSTART)
        pMark2 = InStr(Parag, REFTAGEND)
        
        While (pMark1 > 0) And (pMark2 > pMark1)
            i = i + 1
            ReDim Preserve Paragraphs(i)
            ReDim Preserve Marks(i)
            
            Marks(i) = Mid(Parag, pMark1 + Len(REFTAGSTART), pMark2 - pMark1 - Len(REFTAGSTART))
            Paragraphs(i) = Mid(Parag, 1, pMark1 - 1)
            
            Parag = Mid(Parag, pMark2 + Len(REFTAGEND))
            
            pMark1 = InStr(Parag, REFTAGSTART)
            pMark2 = InStr(Parag, REFTAGEND)
        Wend

    End If
    BODY_SplitParagraphWhichHasMoreThanOneReference = i
End Function
'-----------------------------------------------------------------------
'BODY_FindNewParagraph  - encontra um novo parágrafo dentro de um intervalo
'ini    - limite inferior
'fim    - limite superior
'P  - posição do parágrafo encontrado
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Private Function BODY_FindNewParagraph(ini As TpPosition, fim As TpPosition, P As TpPosition) As String
    Dim retorno As String
    
    Call BODY_Text.InString(ini.i, ini.j, fim.i, fim.j, STANDARDIZEDENDPARAG, P.i, P.j, vbBinaryCompare)
    If P.j > 0 Then
        retorno = STANDARDIZEDENDPARAG
    End If
    BODY_FindNewParagraph = retorno
End Function

'-----------------------------------------------------------------------
'BODY_GetParagraph   - obtém parágrafo de um intervalo
'ini    - limite inferior
'fim    - limite superior
'Paragraph  - parágrafos
'Retorno    - quantidade de parágrafos
'-----------------------------------------------------------------------
Private Function BODY_GetParagraph(ini As TpPosition, fim As TpPosition, Paragraph() As String) As Long
    Dim Qtd As Long
    Dim i As Long
    Dim p1 As TpPosition
    Dim p2 As TpPosition
    Dim total_length As Long
    Dim line_total_length As Long
    Dim partial_length As Long
    Dim line_partial_length As Long
    
    Erase Paragraph
    total_length = BODY_Text.GetLen(ini.i, ini.j, fim.i, fim.j)
    
    If total_length <= TamMaxParag Then
        ReDim Paragraph(1)
        Paragraph(1) = BODY_Text.GetSubstrRange(ini.i, ini.j, fim.i, fim.j)
        Qtd = 1
    Else
'        If ini.i = Fim.i Then
'            p1 = ini
'            while total_length > 0
'                Qtd = Qtd + 1
'                ReDim Preserve Paragraph(Qtd)
'                If total_length > TamMaxParag Then
'                    partial_length = TamMaxParag
'                Else
'                    partial_length = total_length
'                End If
'                Paragraph(Qtd) = BODY_Text.GetSubstrInRow(p1.i, p1.j, partial_length)
'                Call BODY_Text.ForwardPosition(p1.i, p1.j, partial_length)
'                total_length = total_length - TamMaxParag
'            Wend
'        ElseIf ini.i < Fim.i Then
            p1 = ini
            For i = ini.i To fim.i
                If ini.i = fim.i Then
                    line_total_length = fim.j - ini.j + 1
                ElseIf i < fim.i Then
                    line_total_length = BODY_Text.GetLineLen(i) - p1.j + 1
                ElseIf i = fim.i Then
                    line_total_length = fim.j
                End If
                
                While line_total_length > 0
                    Qtd = Qtd + 1
                    ReDim Preserve Paragraph(Qtd)
                    If line_total_length > TamMaxParag Then
                        line_partial_length = TamMaxParag
                    Else
                        line_partial_length = line_total_length
                    End If
                    Paragraph(Qtd) = BODY_Text.GetSubstrInRow(p1.i, p1.j, line_partial_length)
                    Call BODY_Text.ForwardPosition(p1.i, p1.j, line_partial_length)
                    line_total_length = line_total_length - TamMaxParag
                Wend
            Next
        'End If
    End If
    BODY_GetParagraph = Qtd
End Function

'-----------------------------------------------------------------------
'BODY_FindReferences - find the references in full text
'Return - <True> - if all references were found, <False> - otherwise
'-----------------------------------------------------------------------
Private Function BODY_FindReferences() As Boolean
    Dim ret As Boolean
    Dim i As Long
    Dim LimInf As TpPosition
    Dim LimSup As TpPosition
    Dim r As String
    Dim found As Boolean
    Dim ReferenceStrLen As Long
    Dim j As Long
    Dim Reference As String
    Dim LimInf2 As TpPosition
    Dim LimSup2 As TpPosition
      
    Dim initialPos As TpPosition
    Dim finalPos As TpPosition
    Dim prevPosition As TpPosition
    Dim nextPosition As TpPosition
    Dim k As Long
    Dim text(5) As String
    
    REFTAGEND = "</" + CStr(BV(Currbv).BVISISTAGS("ref").Value) + ">"
    REFTAGSTART = "<" + CStr(BV(Currbv).BVISISTAGS("ref").Value) + ">"
    
    
    LimInf.i = 1
    LimInf.j = 1
    Call CompressedInfo.GetEnd(LimSup.i, LimSup.j)
    
    text(0) = "References"
    text(1) = "Referências"
    text(2) = "Bibliografia"
    text(3) = "Citas Bibliográficas"
    
    While k < UBound(text) And initialPos.i = 0
        
        Call CompressedInfo.test_InString(LimInf.i, LimInf.j, text(k), initialPos.i, initialPos.j, finalPos.i, finalPos.j, prevPosition.i, prevPosition.j, nextPosition.i, nextPosition.j, vbTextCompare)
        k = k + 1
        
    Wend
    
    ret = True
    For i = 1 To ReferencesCounter
        'prepare references to compare them
        Call Msg.GiveRunInformation(InterfaceLabels("MsgSettingReferenceLinks").elem2 & " " & CStr(i) & "/" & CStr(ReferencesCounter), , True, False)
        If i = 46 Then
        Debug.Print
        End If
        
        If InStr(References(i), "<br>") > 0 Then
            References(i) = Replace(References(i), "<br>", STANDARDIZEDENDPARAG)
        End If
        References(i) = BODY_RmSymbolHTML(References(i))
        References(i) = BODY_RmEntitiesHTML(References(i))
        ReferenceStrLen = Len(References(i))
        
        Reference = ""
        For j = 1 To ReferenceStrLen
            If Mid(References(i), j, 1) Like "[A-Za-z0-9]" Then
                Reference = Reference + Mid(References(i), j, 1)
            End If
        Next
        References(i) = ""
        
        'find the reference in body
        'found = test_BODY_FindReferenceInText(i, Reference, LimInf, LimSup)
        found = test_BODY_FindReferenceInText(i, Reference, LimInf, LimSup)
'        If found Then
'            LimInf.i = LimInf2.i
'            LimInf.j = LimInf2.j
'            LimSup.i = LimSup2.i
'            LimSup.j = LimSup2.j
'            Call test_BODY_FindReferenceInText(i, Reference, LimInf2, LimSup2)
'        End If
        If Not found Then
            r = r + COMMA + CStr(i)
        End If
        
        'free memory
        ret = ret And found
    Next
    
    ReferencesCounter = 0
    Erase References
    
    If Not ret Then
        r = Mid(r, 2)
        Call Msg.GiveRunInformation(InterfaceLabels("MsgMissingReferences").elem2 + r)
    End If
    BODY_FindReferences = ret
End Function

'-----------------------------------------------------------------------
'BODY_FindReferenceInText - Find a reference in body file
'IdReference - index of the reference to find
'Reference - reference to find
'LimInf - initial position at the body to find the reference
'LimSup - final position of the reference found
'Return - <True> to success and <False> to failure
'-----------------------------------------------------------------------
Private Function test_BODY_FindReferenceInText(IdReference As Long, Reference As String, LimInf As TpPosition, LimSup As TpPosition) As Boolean
    Dim RefInitialPos As TpPosition
    Dim RefFinalPos As TpPosition
    Dim p1 As Long
    Dim CompleteReference As String
    Dim OK As Boolean
    Dim ReferenceMark As String
    Dim li As TpPosition
    Dim ls As TpPosition
    Dim prevPosition As TpPosition
    Dim nextPosition As TpPosition
    
    Dim LimInfNovo As TpPosition, LimSupNovo As TpPosition
    Dim RefInitialPosNovo As TpPosition
    Dim RefFinalPosNovo As TpPosition
    Dim prevPositionNovo As TpPosition
    Dim nextPositionNovo As TpPosition
    
    li = LimInf
    ls = LimSup
    
    
    
    Call CompressedInfo.test_InString(LimInf.i, LimInf.j, Reference, RefInitialPos.i, RefInitialPos.j, RefFinalPos.i, RefFinalPos.j, prevPosition.i, prevPosition.j, nextPosition.i, nextPosition.j, vbBinaryCompare)
    
    If RefInitialPos.j = 0 Then
        LimInf = li
        LimSup = ls
        Call CompressedInfo.test_InString(LimInf.i, LimInf.j, Reference, RefInitialPos.i, RefInitialPos.j, RefFinalPos.i, RefFinalPos.j, prevPosition.i, prevPosition.j, nextPosition.i, nextPosition.j, vbTextCompare)
    End If
    'If RefInitialPos.j > 0 Then
    '    LimInfNovo.i = nextPosition.i
    '    LimInfNovo.j = nextPosition.j
    '
    '    Call CompressedInfo.test_InString(LimInfNovo.i, LimInfNovo.j, Reference, RefInitialPosNovo.i, RefInitialPosNovo.j, RefFinalPosNovo.i, RefFinalPosNovo.j, prevPositionNovo.i, prevPositionNovo.j, nextPositionNovo.i, nextPositionNovo.j, vbBinaryCompare)
    '
    '    If RefInitialPosNovo.j = 0 Then
    '        LimInfNovo = RefInitialPos
    '        LimSupNovo = ls
    '        Call CompressedInfo.test_InString(LimInfNovo.i, LimInfNovo.j, Reference, RefInitialPosNovo.i, RefInitialPosNovo.j, RefFinalPosNovo.i, RefFinalPosNovo.j, prevPositionNovo.i, prevPositionNovo.j, nextPositionNovo.i, nextPositionNovo.j, vbTextCompare)
    '    End If
    '    If RefInitialPosNovo.j > 0 Then
            'LimInf = LimInfNovo
    '        RefInitialPos = RefInitialPosNovo
    '        RefFinalPos = RefFinalPosNovo
            'prevPosition = prevPositionNovo
            'nextPosition = nextPositionNovo
    '    End If
    'End If
    If RefInitialPos.j > 0 Then
    
        With CompressedInfo
        'Update the next start position (LimInf)
        LimInf = nextPosition
    
        'Calculate the position of the end of the reference in the complete text to insert the reference mark
        CompleteReference = BODY_UnCompressLine(Mid(.GetLine(RefFinalPos.i), 1, RefFinalPos.j), CompressionInfo(RefFinalPos.i))
        RefFinalPos.j = Len(CompleteReference)
                
        End With
        
        With BODY_Text
        'Check the exact position to insert the reference mark
        If test_BODY_FindEndReference(RefFinalPos.i, RefFinalPos.j) Then
            
        
            'Build the reference mark to insert into the complete text
            ReferenceMark = Trim(RmNewLineInStr(DB_TagContents(CStr(IdReference), BV(Currbv).BVISISTAGS("ref").Value)))
        
            'Insert the reference mark
            .SetLine(RefFinalPos.i) = Mid(.GetLine(RefFinalPos.i), 1, RefFinalPos.j) + ReferenceMark + STANDARDIZEDENDPARAG + Mid(.GetLine(RefFinalPos.i), RefFinalPos.j + 1)
            'Update the compression information
             CompressionInfo(RefFinalPos.i) = Mid(CompressionInfo(RefFinalPos.i), 1, RefFinalPos.j) + String(Len(ReferenceMark + STANDARDIZEDENDPARAG), "0") + Mid(CompressionInfo(RefFinalPos.i), RefFinalPos.j + 1)
            
            'Debug.Print "Reconheceu " + .GetLine(RefFinalPos.i)
            'CompressedInfo.SetLine(RefFinalPos.i) = BODY_CompressLine(.GetLine(RefFinalPos.i), CompressionInfo(RefFinalPos.i))
            'Debug.Print "BODY_CompressLine " + .GetLine(RefFinalPos.i)
            OK = True
        Else
            Debug.Print "Não Reconheceu " + .GetLine(RefFinalPos.i)
        End If
        End With
        
    Else
        Debug.Print Reference
        
    End If
    
    test_BODY_FindReferenceInText = OK
End Function
'-----------------------------------------------------------------------
'BODY_FindReferenceInText - Find a reference in body file
'IdReference - index of the reference to find
'Reference - reference to find
'LimInf - initial position at the body to find the reference
'LimSup - final position of the reference found
'Return - <True> to success and <False> to failure
'-----------------------------------------------------------------------
Private Function anterior_test_BODY_FindReferenceInText(IdReference As Long, Reference As String, LimInf As TpPosition, LimSup As TpPosition) As Boolean
    Dim RefInitialPos As TpPosition
    Dim RefFinalPos As TpPosition
    Dim p1 As Long
    Dim CompleteReference As String
    Dim OK As Boolean
    Dim ReferenceMark As String
    Dim li As TpPosition
    Dim ls As TpPosition
    Dim prevPosition As TpPosition
    Dim nextPosition As TpPosition
    
    li = LimInf
    ls = LimSup
    
    
    
    Call CompressedInfo.test_InString(LimInf.i, LimInf.j, Reference, RefInitialPos.i, RefInitialPos.j, RefFinalPos.i, RefFinalPos.j, prevPosition.i, prevPosition.j, nextPosition.i, nextPosition.j, vbBinaryCompare)
    
    If RefInitialPos.j = 0 Then
        LimInf = li
        LimSup = ls
        Call CompressedInfo.test_InString(LimInf.i, LimInf.j, Reference, RefInitialPos.i, RefInitialPos.j, RefFinalPos.i, RefFinalPos.j, prevPosition.i, prevPosition.j, nextPosition.i, nextPosition.j, vbTextCompare)
    End If
    If RefInitialPos.j > 0 Then
        With CompressedInfo
        'Update the next start position (LimInf)
        LimInf = nextPosition
    
        'Calculate the position of the end of the reference in the complete text to insert the reference mark
        CompleteReference = BODY_UnCompressLine(Mid(.GetLine(RefFinalPos.i), 1, RefFinalPos.j), CompressionInfo(RefFinalPos.i))
        RefFinalPos.j = Len(CompleteReference)
                
        End With
        
        With BODY_Text
        'Check the exact position to insert the reference mark
        If test_BODY_FindEndReference(RefFinalPos.i, RefFinalPos.j) Then
            
        
            'Build the reference mark to insert into the complete text
            ReferenceMark = Trim(RmNewLineInStr(DB_TagContents(CStr(IdReference), BV(Currbv).BVISISTAGS("ref").Value)))
        
            'Insert the reference mark
            .SetLine(RefFinalPos.i) = Mid(.GetLine(RefFinalPos.i), 1, RefFinalPos.j) + ReferenceMark + STANDARDIZEDENDPARAG + Mid(.GetLine(RefFinalPos.i), RefFinalPos.j + 1)
            'Update the compression information
             CompressionInfo(RefFinalPos.i) = Mid(CompressionInfo(RefFinalPos.i), 1, RefFinalPos.j) + String(Len(ReferenceMark + STANDARDIZEDENDPARAG), "0") + Mid(CompressionInfo(RefFinalPos.i), RefFinalPos.j + 1)
            
            'Debug.Print "Reconheceu " + .GetLine(RefFinalPos.i)
            'CompressedInfo.SetLine(RefFinalPos.i) = BODY_CompressLine(.GetLine(RefFinalPos.i), CompressionInfo(RefFinalPos.i))
            'Debug.Print "BODY_CompressLine " + .GetLine(RefFinalPos.i)
            OK = True
        Else
            Debug.Print "Não Reconheceu " + .GetLine(RefFinalPos.i)
        End If
        End With
        
    Else
        Debug.Print Reference
        
    End If
    
    anterior_test_BODY_FindReferenceInText = OK
End Function
'-----------------------------------------------------------------------
'BODY_FindEndReference - Find the end of the reference
'InitRow    - initial position in row
'InitCol    - initial position in column
'Return <True> if found, <False> otherwise
'-----------------------------------------------------------------------
Private Function test_BODY_FindEndReference(InitRow As Long, InitCol As Long) As Boolean
    Dim pInitP As TpPosition
    Dim pEndP As TpPosition
    Dim nextParag As TpPosition, prevPosition As TpPosition
    
    Dim teste As TpPosition
    Dim Index As Long
    
    Dim i As Long
    Dim temp As String
    
    
    If UBound(ReferenceSeparators) > 0 Then
        'temp = temp & vbCrLf & vbCrLf & "Em " & BODY_Text.test_getSubstring(InitRow, InitCol, InitRow + 3, 1)
        For i = 0 To UBound(ReferenceSeparators)
            'temp = temp & vbCrLf & vbCrLf & "Procurar " & ReferenceSeparators(i)
            
            Call BODY_Text.test_InString(InitRow, InitCol, ReferenceSeparators(i), pInitP.i, pInitP.j, pEndP.i, pEndP.j, prevPosition.i, prevPosition.j, nextParag.i, nextParag.j, vbBinaryCompare)
            'temp = temp & vbCrLf & "[" & BODY_Text.test_getSubstring(pInitP.i, pInitP.j, pEndP.i, pEndP.j) & "]"
                
            If ReferenceSeparators(i) = STANDARDIZEDENDPARAG Then
                'temp = temp & vbCrLf & "    igual    "
                pInitP = prevPosition
            End If
        
            If (pInitP.i > 0 And pInitP.j > 0) Then
                ' seleciona aquele que está mais proximo do final da referencia.
                If (teste.i = 0 And teste.j = 0) Or (pInitP.i = teste.i And pInitP.j < teste.j) Or (pInitP.i < teste.i) Then
                    teste = pInitP
                    Index = i
                End If
            End If
        Next
        
      
        'temp = temp & vbCrLf & vbCrLf & "Eleito " & ReferenceSeparators(Index)
        'temp = temp & vbCrLf & "Reference:" & BODY_Text.test_getSubstring(InitRow, InitCol, teste.i, teste.j)
        'Dim fnLog As Long
        
    'fnLog = FreeFile(1)
    'Open "references.txt" For Append As fnLog
    'Print #fnLog, temp
    'Close #fnLog
    Else
        Call BODY_Text.test_InString(InitRow, InitCol, STANDARDIZEDENDPARAG, pInitP.i, pInitP.j, pEndP.i, pEndP.j, prevPosition.i, prevPosition.j, nextParag.i, nextParag.j, vbBinaryCompare)
        teste = prevPosition
    End If
    InitRow = teste.i
    InitCol = teste.j
    test_BODY_FindEndReference = True
End Function
'-----------------------------------------------------------------------
'BODY_CompressLine - Compress the lines, eliminating the spaces between the words,
'in order to match the references of the markup document and of the body document
'Str    - string to compress
'CompressionInfo   - it contains "0" and "1", according to the position of the characters of <Str>
'   "0" - at the position where the character is different from [A-Za-z0-9]
'   "1" - at the position where the character is equal to [A-Za-z0-9]
'-----------------------------------------------------------------------
Private Function BODY_CompressLine(str As String, CompressionInfo As String) As String
    Dim rStr As String
    Dim character As String
    Dim i As Long
    Dim StringLen As Long
        
    rStr = ""
    CompressionInfo = ""
    StringLen = Len(str)
        
    For i = 1 To StringLen
        character = Mid(str, i, 1)
        If character Like "[A-Za-z0-9]" Then
            rStr = rStr + character
        Else
            CompressionInfo = CompressionInfo + String(i - 1 - Len(CompressionInfo), "1") + "0"
        End If
    Next
    
    BODY_CompressLine = rStr
End Function

'-----------------------------------------------------------------------
'BODY_UnCompressLine - Replace the spaces in the string
'Str    - string to insert the spaces
'CompressionInfo   - it contains the "0" and "1" that identify the positions of the spaces and
'the other character
'Return - string with spaces
'-----------------------------------------------------------------------
Private Function BODY_UnCompressLine(ByVal str As String, CompressionInfo As String) As String
    Dim i As Long
    Dim rStr As String
    Dim quit As Boolean
    Dim P As Long
    
    rStr = str
    P = InStr(1, CompressionInfo, "0", vbBinaryCompare)
    While (P > 0) And (P <= Len(rStr))
        rStr = Mid(rStr, 1, CLng(P) - 1) + Chr(32) + Mid(rStr, CLng(P))
        P = InStr(P + 1, CompressionInfo, "0", vbBinaryCompare)
    Wend
    
    BODY_UnCompressLine = rStr
End Function

'-----------------------------------------------------------------------
'BODY_RmSymbolHTML - Remove the <FONT FACE SYMBOL>
's  - string to be convert
'Return - string converted
'-----------------------------------------------------------------------
Private Function BODY_RmSymbolHTML(s As String) As String
    Dim original As String
    Dim p1 As Long
    Dim p2 As Long
    Dim P3 As Long
    Dim nova As String
    Dim test As String
    
    original = s
    While Len(original) > 0
        p1 = InStr(original, "<")
        p2 = InStr(original, ">")
        If (p1 = 0) Or (p2 = 0) Then
            nova = Trim(nova) + Chr(32) + Trim(original)
            original = ""
        ElseIf p1 < p2 Then
            P3 = InStr(p1 + 1, original, "<", vbBinaryCompare)
            While (P3 > 0) And (P3 < p2)
                p1 = P3
                P3 = InStr(p1 + 1, original, "<", vbBinaryCompare)
            Wend
            
            test = Mid(original, p1, p2 - p1 + 1)
            
            If InStr(1, test, "face=" + Chr(34) + "symbol" + Chr(34), vbTextCompare) > 0 Then
                p2 = InStr(p2 + 1, original, ">", vbTextCompare)
            ElseIf InStr(1, test, "font-family:symbol", vbTextCompare) > 0 Or InStr(1, test, "font-family: symbol", vbTextCompare) > 0 Then
                p2 = InStr(p2 + 1, original, ">", vbTextCompare)
            End If
            nova = Trim(nova) + Chr(32) + Trim(Mid(original, 1, p1 - 1))
            original = Trim(Mid(original, p2 + 1))
        Else
            nova = nova + Mid(original, 1, p2)
            original = Mid(original, p2 + 1)
        End If
    Wend
    BODY_RmSymbolHTML = Trim(nova)
End Function

'-----------------------------------------------------------------------
'BODY_StandardizeEndParag - Insert the tag [STANDARDIZEDENDPARAG_MARK] to sign the end
'of the paragraph
's  - string to be convert
'Return - string converted
'-----------------------------------------------------------------------
Private Function BODY_StandardizeEndParag(s As String, STANDARDIZEDENDPARAG_MARK As String) As String
    Dim s2 As String
    Dim P As Long
    Dim pi As Long
    Dim i As Long
    
    s2 = s
    If Len(s2) > 0 Then
        For i = 1 To BlockTagsCount
            pi = 1
            P = InStr(pi, s2, BlockTags(i), vbTextCompare)
            While (P > 0)
                If P > 1 Then
                    s2 = Mid(s2, 1, P - 1) + STANDARDIZEDENDPARAG_MARK + Mid(s2, P)
                Else
                    s2 = STANDARDIZEDENDPARAG_MARK + s2
                End If
                pi = P + Len(STANDARDIZEDENDPARAG_MARK) + Len(BlockTags(i))
                P = InStr(pi, s2, BlockTags(i), vbTextCompare)
            Wend
        Next
    End If
    BODY_StandardizeEndParag = s2
End Function


Private Sub Class_Initialize()
    
    Set privateContent = New ClContent
    
    ReferencesCounter = 0
    Erase References

    Set BODY_Text = New ClTxt
    Set MARKUP_Text = New ClTxt
    Set CompressedInfo = New ClTxt
    Set IdiomDependentFields = New ClSortList
    Set LinkMarkup2Body = New ColPair
    
    BlockTagsCount = 16
    ReDim BlockTags(BlockTagsCount)
    
    BlockTags(1) = "<p "
    BlockTags(2) = "<p>"
    BlockTags(3) = "<li>"
    BlockTags(4) = "<dt>"
    BlockTags(5) = "<pre "
    BlockTags(6) = "<pre>"
    BlockTags(7) = "<div "
    BlockTags(8) = "<div>"
    BlockTags(9) = "<center>"
    BlockTags(10) = "<blockquote>"
    BlockTags(11) = "<form>"
    BlockTags(12) = "<form "
    BlockTags(13) = "</ol>"
    BlockTags(14) = "</ul>"
    BlockTags(15) = "</body>"
    BlockTags(16) = "<br>"

    FindWhat(1) = "<500>"
    FindWhat(2) = "<30>"
    FindWhat(3) = "<FONT FACE=" + Chr(34) + "Symbol" + Chr(34) + ">"
    FindWhat(4) = "<sub>"
    FindWhat(5) = "<sup>"
    FindWhat(6) = "<img"

    
    'bv(CURRBV).BODYsubc(0) = "^b"
    'bv(CURRBV).BODYsubc(1) = "^h"
    'bv(CURRBV).BODYsubc(2) = "^k"
    'bv(CURRBV).BODYsubc(3) = "^p"
    'bv(CURRBV).BODYsubc(4) = "^t"
    'bv(CURRBV).BODYsubc(5) = "^c"
    'bv(CURRBV).BODYsubc(6) = "^s"
    'bv(CURRBV).BODYsubc(7) = "^a"
    'bv(CURRBV).BODYsubc(8) = "^i"
    'bv(CURRBV).BODYsubc(9) = "^g"
    'bv(CURRBV).BODYsubc(10) = "^l"
    
    

End Sub

Private Sub Class_Terminate()
    Set MARKUP_Text = Nothing
    Set BODY_Text = Nothing
    Set CompressedInfo = Nothing
    Set DBRecords = Nothing
    Set IdiomDependentFields = Nothing
    Set DTDCurrent = Nothing
    Set RecordInfo = Nothing
    Set LinkMarkup2Body = Nothing
    
    Erase BlockTags
    Erase FindWhat
End Sub

'-----------------------------------------------------------------------
'MARKUP_GetTmpDoc    - faz uma cópia temporária do documento
'DocPath  - caminho do arquivo do documento
'DocName  - arquivo do documento
'-----------------------------------------------------------------------
Private Function MARKUP_GetTmpDoc(DocPath As String, DocName As String, FileExtension As String) As String
    Dim DocTmpFile As String
    Dim DocTmpFullPath As String
    Dim P As Long
    
    'Cria uma cópia do documento
    P = InStr(DocName, ".")
    DocTmpFile = Mid(DocName, 1, P) + FileExtension
    DocTmpFullPath = DocPath + PathSep + DocTmpFile
    FileCopy DocPath + PathSep + DocName, DocTmpFullPath
    
    MARKUP_GetTmpDoc = DocTmpFile
End Function

'-----------------------------------------------------------------------
'MARKUP_ReadFile   - le o arquivo do documento
'DocPath    - caminho do arquivo do documento
'DocFile       - arquivo do documento
'-----------------------------------------------------------------------
Private Function MARKUP_ReadFile(DocPath As String, DocFile As String) As Boolean
    Dim fn As Long
    Dim aux As String
    Dim ret As Boolean
    Dim openBody As Boolean
    Dim closeBody As Boolean
    Dim isHTML As Boolean
    
        
    isHTML = (InStr(LCase(DocFile), ".htm") > 0)
    Set MARKUP_Text = New ClTxt
    fn = FreeFile
    Open DocPath + PathSep + DocFile For Input As fn
    Do Until EOF(fn)
        Line Input #fn, aux
        If isHTML And Not openBody Then
            openBody = (InStr(LCase(aux), "<body") > 0)
        End If
        
        If (isHTML And openBody And Not closeBody) Or (Not isHTML) Then
            'It is necessary because the sgml parser need to recognize the attribute
            'between the character <quote>, and <&quot;> is not compiled as the quote character
            aux = ReplaceString(ReplaceString(aux, "&quot;", Chr(34), vbBinaryCompare), "&quot", Chr(34), vbBinaryCompare) + CONST_SPACE_END_for_HTML
            
            'If InStr(aux, "&") > 0 Then
                'aux = ReplaceString(ReplaceString(aux, "&amp;rsqb;", "&#093;"), "&amp;lsqb;", "&#091;")
                'aux = ReplaceString(ReplaceString(aux, "&amp;#093;", "&#093;"), "&amp;#091;", "&#091;")
                'aux = ReplaceString(ReplaceString(aux, "&amp;rsqb ", "&#093;"), "&amp;lsqb ", "&#091;")
                'aux = ReplaceString(ReplaceString(aux, "&amp;#093 ", "&#093;"), "&amp;#091 ", "&#091;")
            'End If
            '-- aux = CvtTables("Conversion sgml to windows 1").Convert(aux)
            MARKUP_Text.AddLines (Entities.entNum2myEnt(aux))
            If isHTML And Not closeBody Then
                closeBody = (InStr(LCase(aux), "</body>") > 0)
            End If
        End If
    Loop
    Close #fn
    MARKUP_CleanTags
        
    If MARKUP_Text.CheckErrorinMarkupTag = 0 Then ret = True
        
    '-- It is made to standardize the characters in order to match the markup file references and
    'body file references
    '-- 000321 Set MARKUP_Text = MARKUP_Text.ConvertSpecialChar(ASCIITable)
    MARKUP_ReadFile = ret
End Function

'-------------------------------------------------------------------------------------
'MARKUP_GetMarkupDoc - Find the begin and the end of the document and identify
'the DTD name and DTD version
'BeginRow  - position on the row of the begin of the document
'BeginCol  - position on the column of the begin of the document
'EndRow  - position on the row of the end of the document
'EndCol  - position on the column of the end of the document
'DTDId  - the DTD name and DTD version
'Return - <True> to sucess, <False> to failure
'-------------------------------------------------------------------------------------
Private Function MARKUP_GetMarkupDoc(BeginRow As Long, BeginCol As Long, EndRow As Long, EndCol As Long, StartTag As String, EndTag As String, DTDId As String) As Boolean
    Dim init As TpPosition
    Dim Fin As TpPosition
    Dim P As TpPosition
    Dim p1 As TpPosition
    Dim p2 As TpPosition
    Dim P3 As TpPosition
    Dim p0 As Long
    Dim DocumentOK As Boolean
    
    Call Msg.GiveRunInformation(InterfaceLabels("MsgRecognizeDocType").elem2, , True)
    
    StartTag = ""
    DTDId = ""
    BeginRow = 0
    BeginCol = 0
    EndRow = 0
    EndCol = 0
    
    init.i = 1
    init.j = 1
    
    With MARKUP_Text
    Call .GetEnd(Fin.i, Fin.j)
    If .ExisteStr(init.i, init.j, Fin.i, Fin.j) Then
        Call .InString(init.i, init.j, Fin.i, Fin.j, "<body", P.i, P.j, vbTextCompare)
        If P.j > 0 Then
            Call .InString(P.i, P.j, Fin.i, Fin.j, ">", init.i, init.j, vbTextCompare)
            Call .ForwardPosition(init.i, init.j, 1)
            'Call .InString(Init.i, Init.j, Fin.i, Fin.j, "</body>", P.i, P.j, vbTextCompare)
            'If P.j > 0 Then
            '    Fin = P
            '    Call .RewardPosition(Fin.i, Fin.j, 1)
            'End If
        End If
    End If
    
    If .ExisteStr(init.i, init.j, Fin.i, Fin.j) Then
        Call .InString(init.i, init.j, Fin.i, Fin.j, TagFech, p2.i, p2.j, vbTextCompare)
        If p2.j > 0 Then
            Call .InString(init.i, init.j, p2.i, p2.j, TagInicialAbre, p1.i, p1.j, vbTextCompare)
            If p1.j > 0 Then
                P = p1
                Call .ForwardPosition(P.i, P.j, 1)
                Call .InString(P.i, P.j, p2.i, p2.j, TagInicialAbre, P3.i, P3.j, vbTextCompare)
                While (P3.j > 0) And ((P3.i < p2.i) Or ((P3.i = p2.i) And (P3.j < p2.j)))
                    p1 = P3
                    P = P3
                    Call .ForwardPosition(P.i, P.j, 1)
                    Call .InString(P.i, P.j, p2.i, p2.j, TagInicialAbre, P3.i, P3.j, vbTextCompare)
                Wend
                StartTag = .GetSubstrRange(p1.i, p1.j, p2.i, p2.j)
                
                If Len(StartTag) > 0 Then
                    DTDId = MARKUP_IdentifyDTD(StartTag, EndTag)
                    Call .InString(BeginRow, BeginCol, Fin.i, Fin.j, EndTag, EndRow, EndCol, vbBinaryCompare)
                    If EndCol > 0 Then
                        DocumentOK = True
                        Call .ForwardPosition(EndRow, EndCol, Len(EndTag) - 1)
                        BeginRow = p1.i
                        BeginCol = p1.j
                    Else
                        Msg.GiveRunInformation (InterfaceLabels("MsgFinalTagNotFound").elem2 + EndTag)
                    End If
                End If
            End If
        End If
    End If
    End With
    
    
    MARKUP_GetMarkupDoc = DocumentOK
End Function
'-----------------------------------------------------------------------
'MARKUP_CleanTags - replace all html tags by spaces
'Return - the new ClTxt
'-----------------------------------------------------------------------
Sub MARKUP_CleanTags()
    Dim mkpStart As TpPosition
    Dim mkpEnd As TpPosition
    
    Dim test As String
    
    Dim prevPosition As TpPosition
    Dim nextPosition As TpPosition
    
    Dim LimInf As TpPosition
    
    Dim qSPAN As Long
    Dim i As Long, j As Long
    Dim spanTags() As String
    
    Call Msg.GiveRunInformation(InterfaceLabels("MsgCleaningSpan").elem2, False, True, True)
    
    qSPAN = existSPANTags(MARKUP_Text.test_get_from_a_row_a_string_with_max_characters(1, 1), spanTags)
    Call Msg.GiveRunInformation(InterfaceLabels("MsgCleaningSpan").elem2, False, True, True)
    
    LimInf.i = 1
    LimInf.j = 1
    Call MARKUP_Text.GetEnd(i, j)
    
    For i = 1 To qSPAN
        Call MARKUP_Text.test_InString(LimInf.i, LimInf.j, spanTags(i), mkpStart.i, mkpStart.j, mkpEnd.i, mkpEnd.j, prevPosition.i, prevPosition.j, nextPosition.i, nextPosition.j, vbBinaryCompare)
        LimInf = mkpStart
        test = MARKUP_Text.test_getSubstring(mkpStart.i, mkpStart.j, mkpEnd.i, mkpEnd.j)
        test = RmAllHTML2(test)
        Call MARKUP_Text.replaceSubstring(test, mkpStart.i, mkpStart.j, mkpEnd.i, mkpEnd.j)
    Next
    
    
End Sub
'-------------------------------------------------------------------------------------
'MARKUP_IdentifyDTD - Identify the DTD name and DTD version
'StartTag   - Input/Output - the start tag of document including the attributes
'EndTag - Output - the end tag of document
'Return - identification of the DTD name and DTD version
'-------------------------------------------------------------------------------------
Private Function MARKUP_IdentifyDTD(StartTag As String, EndTag As String) As String
    Dim Pos As Long
    Dim Version As String
    Dim found As Boolean
    Dim DTDId As String
    
    StartTag = RmAllHTML(ReplaceString(StartTag, Chr(160), Chr(32), vbBinaryCompare))
    
    If Len(StartTag) > 0 Then
        Pos = InStr(StartTag, Chr(32))
        If Pos > 0 Then
            DTDId = Mid(StartTag, 2, Pos - 2)
        Else
            DTDId = Mid(StartTag, 2, Len(StartTag) - 2)
        End If
        EndTag = TagFinalAbre + DTDId + TagFech
                    
        Pos = InStr(StartTag, "version=")
        If Pos > 0 Then
            Version = Mid(StartTag, Pos + 8)
            Pos = InStr(Version, Chr(32))
            If Pos > 0 Then
                Version = Mid(Version, 1, Pos - 1)
            Else
                Version = Mid(Version, 1, Len(Version) - 1)
            End If
            Pos = InStr(Version, Chr(34))
            If Pos > 0 Then
                Version = Mid(Version, 2, Len(Version) - 2)
            End If
        End If
    End If
    
    DTDId = DTDId + Chr(32) + Version
    
    MARKUP_IdentifyDTD = DTDId
End Function

'-----------------------------------------------------------------------
'MARKUP_WriteTmpMarkupDoc - Write the Markup Document
'Path - path of the file
'DocFile - name of the document
'Init  - initial position of the markup document in html file
'finish  - finish position of the markup document in html file
'Return - <True> - sucess, <False> - failure
'-----------------------------------------------------------------------
Private Function MARKUP_WriteTmpMarkupDoc(Path As String, DocFile As String, init As TpPosition, finish As TpPosition) As Boolean
    Dim ret As Boolean
    Dim fn As Long
    Dim i As Long
    
    With MARKUP_Text
    If .ExisteStr(init.i, init.j, finish.i, finish.j) Then
        fn = FreeFile
        
        Open Path + PathSep + DocFile For Output As fn
        If init.i = finish.i Then
            Print #fn, .GetSubstrInRow(init.i, init.j, finish.j + 1 - init.j)
        Else
            Print #fn, Mid(.GetLine(init.i), init.j)
            
            For i = init.i + 1 To finish.i - 1
                Print #fn, .GetLine(i)
            Next
    
            Print #fn, Mid(.GetLine(finish.i), 1, finish.j)
            Print #fn, Chr(32)
        End If
        Close fn
        ret = True
    End If
    End With
    Set MARKUP_Text = Nothing
    
    MARKUP_WriteTmpMarkupDoc = ret
End Function

Function ConvertDocW97to2000(inputFile As String, OutputFile As String)
    Dim Path As String
    Dim File As String
    Dim fn As Long
    Dim convertBatch As String
    
    fn = 200
    
    convertBatch = App.Path + "\mkp97to2000\markup97to2000XP.bat " + inputFile + " " + OutputFile
    
    Open inputFile + ".tmp" For Output As fn
    Print #fn, convertBatch
    Close fn
    
    
    Shell (convertBatch)
    
    Call SeparateFileandPath(inputFile, Path, File)
    While (FileExist(Path, File + ".tmp"))
        'MsgBox "existe: " + path + "\" + file + ".tmp"
    Wend
End Function

'-----------------------------------------------------------------------
'MARKUP_IsValidDTD  - verifica se a DTD que descreve o documento pode ser usada pelo
'programa de conversao, isto e', se e' uma DTD valida
'DocPath  - caminho do arquivo do documento
'DocFile  - arquivo do documento
'-----------------------------------------------------------------------
Function MARKUP_IsValidDTD(DocPath As String, DocFile As String) As Boolean
    Dim init As TpPosition
    Dim finish As TpPosition
    Dim fn As Long
    Dim Valid As Boolean
    Dim StartTag As String
    Dim EndTag As String
    Dim DTDId As String
    
    'Call Msg.GiveRunInformation("Preparing the document...", , True)
    
    'word 97 to XP
    
    FileCopy DocPath + PathSep + DocFile, DocPath + PathSep + DocFile + ".bkp"
    If CONVERT_97_TO_2000 = "1" Then
        Call ConvertDocW97to2000(DocPath + "\" + DocFile, DocPath + "\" + DocFile)
    End If
    
    'Get a name to the temporary markup file, which extension is .sci
    TmpDocFile = MARKUP_GetTmpDoc(DocPath, DocFile, "sci")
    
    'Read the original markup file
    If MARKUP_ReadFile(DocPath, DocFile) Then
    
        'Get the start and the end of the document
        If MARKUP_GetMarkupDoc(init.i, init.j, finish.i, finish.j, StartTag, EndTag, DTDId) Then
        
            'Check the existence of the DTD
            Set DTDCurrent = New ClDTD
            Set DTDCurrent = BV(Currbv).DTDCol.Item(DTDId, Valid)
            If Valid Then
                'Create the Temporary Markup Document
                'Call MARKUP_Text.Insert_igntag(DTDCurrent.UnclosedTags)
                
                Call MARKUP_WriteTmpMarkupDoc(DocPath, TmpDocFile, init, finish)
            
                'Create a Temporary File <ConfigFile> to check the configuration of document
                ConfigPath = App.Path
                
                fn = FreeFile
                Open ConfigPath + PathSep + ConfigFile For Output As fn
                Print #fn, StartTag
                Print #fn, EndTag
                Close fn
                
                If Not DTDCurrent.isLoaded Then
                    Call DTDCurrent.ReadProcParam(BV(Currbv).BVPath)
                End If
            Else
                Call Msg.GiveRunInformation(InterfaceLabels("MsgInvalidDocumentType").elem2 + DTDId)
            End If
            
        End If
    End If
    If CONVERT_97_TO_2000 = "1" Then
        FileCopy DocPath + PathSep + DocFile + ".old", DocPath + PathSep + DocFile
    End If
    MARKUP_IsValidDTD = Valid
End Function

'-----------------------------------------------------------------------
'MARKUP_ParserResult2Fields    - get the marked contents and put them in Fields
'DOCId    - identification of the document
'Return - <True> - success, <False> - failure
'-----------------------------------------------------------------------
' FIXED_20070115 ahead of print - identify existence of new-pid
'-----------------------------------------------------------------------
Private Function MARKUP_ParserResult2Fields(DocId As String, MarkupFileName As String, Optional htmlfragpath As String) As Boolean
    Dim fn As Long
    Dim Line As String
    
    'Dim hasDocIdinMarkup As Boolean
    Dim nextproc As Boolean
    Dim ret As Boolean
    
    Dim paramidx As Long
    Dim proccount As Long
    Dim ReferenceIdx As Long
    
    Dim LinkedContent As String
    Dim type4 As String
    Dim type4count As Long
    Dim type4p1 As Long
    Dim type4p2 As Long
    
    Dim scope_recidx As String
    Dim ContentFatherScope As String
    Dim CROSSREFERENCE As String
    
    Dim proc As ClProc
    Dim field_model As String
    Dim sgmltag As String
    Dim sgmltag_check As String
    Dim content As String
    Dim rcontent As String
    Dim proctype As String
    Dim record As String
    Dim recindex As String
    Dim Field As String
    Dim Subf As String
    Dim subf_preffix As String
    Dim format As String
    Dim scope As String
    Dim GroupIdx As String
    Dim Link As String
    Dim fieldkey As String
    Dim LinkKey As String
    Dim exist As Boolean
    Dim existLink As Boolean
    
    Dim reg As ClRegistro
    Dim reg2 As ClRegistro
    Dim f As ClField
    Dim j As Long
    Dim i As Long
    Dim P As Long
    Dim paragcounter As Long
    Dim idiom As String
    Dim occsep As String
    
    Dim plink As ClPair
    
    Dim htmlfragidx As Long
    
    Dim dataFilled As Boolean
    Dim temp As Variant
    Dim hasFormerRef As Long
    
    Set mvarArticle = New ClsArticle
    Set mvarArticle.VersionHistory = New ClsArticleVersionHistory
    
    Dim oldPID As String
    
    Set LawStructure = New ColRegistro
    Set IdiomDependentFields = New ClSortList
    Set RepeatInAllRecords = New ColRegistro
    Set LinkedFields = New ColLink
    Set DBRecords = New ColRegistro
    Set LinkMarkup2Body = New ColPair
    Set LinkMark = New ColPair
    
    article.FileName = MarkupFileName
        
    'hasDocIdinMarkup = False
    
    fn = FreeFile
    Open ParserResult For Input As fn
    While Not EOF(fn)
        
        'Get the each marked content and make some processes to classify them according to
        'its field_model, subfield, record, and so on, that means, according to the tables
        'of conversion (See the technical documentation)
        
        FormMarkup.ProgressBar1.Visible = True
        FormMarkup.ProgressBar1.Value = 0
        
        'Get the data from parser result to make the process of conversion
        Line Input #fn, field_model
        Line Input #fn, scope
        Line Input #fn, content
        Line Input #fn, Line
        
        P = InStr(scope, ":")
        sgmltag = Mid(scope, 1, P - 1)
        
        If Not dataFilled Then
            If sgmltag = "rvpdate" Then
                article.VersionHistory.RVPDate = content
            ElseIf sgmltag = "ahpdate" Then
                article.VersionHistory.AHPDate = content
            ElseIf sgmltag = "title" Or sgmltag = "surname" Then
                dataFilled = True
            ElseIf sgmltag = "issueno" And article.IssueNo = "" Then
                article.IssueNo = content
            ElseIf sgmltag = "dateiso" And article.dateiso = "" Then
                article.dateiso = content
            ElseIf sgmltag = "old-pid" Then
                oldPID = content
            ElseIf sgmltag = "issn" And article.issn = "" Then
                article.issn = content
            End If
        End If
        ' FIXED_20070115 ahead of print
        sgmltag_check = Mid(Trim(scope), P + 1)
        P = InStr(sgmltag_check, " ")
        If P > 0 Then
            sgmltag_check = Mid(sgmltag_check, P + 1)
        End If
        
        P = InStr(sgmltag_check, ":")
        If P > 0 Then
            sgmltag_check = Mid(sgmltag_check, 1, P - 1)
        Else
            sgmltag_check = ""
        End If
       
        
        Set proc = New ClProc
        Set proc = DTDCurrent.ReturnProcedure(field_model, sgmltag, sgmltag_check, scope, ContentFatherScope, GroupIdx, CROSSREFERENCE, exist)
        If exist Then
            'Search for the parameters to use in each process
            For paramidx = 1 To proc.params.Count
                proctype = DTDCurrent.GetProcParam(proc.params(paramidx), field_model, content, scope, ContentFatherScope, CROSSREFERENCE, record, recindex, Field, Subf, subf_preffix, format, fieldkey, LinkKey, rcontent)
                    
                'Execute all the demanded process, it is defined by the conversion tables
                Select Case proctype
                    
                    Case "5", "6", "7", "8", "9"
                        Select Case proctype
                        Case "9"
                            'Structure for Laws
                            Call MARKUP_BuildLawStructure(rcontent, scope, fieldkey, record, CLng(Field), Subf, format)
                        Case "5"
                            'Structure for Laws
                            Call MARKUP_BuildLawStructure(rcontent, scope, "", record, CLng(Field), Subf, format)
                        Case "8"
                            Call MARKUP_Content2Fields(rcontent, GroupIdx, fieldkey, LinkKey, record, recindex, CLng(Field), Subf, subf_preffix, format)
                        Case "6", "7"
                            Call ConvertBODYintoPARAGRAPH(rcontent, record, CLng(Field), Subf, format, paragcounter)
                        End Select
                    
                    Case "1", "2", "2a", "2b", "3"
                        Select Case proctype
                        Case "1"
                            'do nothing else but inserting the content in the <Records> object
                            Call MARKUP_ExecuteProcedure(rcontent, GroupIdx, fieldkey, LinkKey, record, recindex, CLng(Field), Subf, subf_preffix, format)
                            
                        Case "2", "2b"
                            'store the references to match later
                            ReferenceIdx = CLng(recindex)
                            If (ReferencesCounter < ReferenceIdx) Then
                                ReferencesCounter = ReferenceIdx
                                ReDim Preserve References(ReferencesCounter)
                                
                            End If
                            If proctype = "2b" Then
                                hasFormerRef = ReferenceIdx
                                References(ReferencesCounter) = content
                            Else
                                If hasFormerRef <> ReferenceIdx Then
                                    References(ReferencesCounter) = References(ReferencesCounter) + content
                                End If
                            End If
                            
                        Case "2a"
                            'store the links present in the fulltext
                            Set plink = LinkMarkup2Body(fieldkey, existLink)
                            If Not existLink Then
                                Set plink = LinkMarkup2Body.Add(fieldkey)
                                plink.elem2 = "<" + CStr(Field) + ">"
                                plink.elem3 = "</" + CStr(Field) + ">"
                                plink.elem1 = plink.elem1 + rcontent
                                Set plink = LinkMark(CStr(Field), existLink)
                                If Not existLink Then
                                    Set plink = LinkMark.Add(CStr(Field))
                                    plink.elem1 = "<" + CStr(Field) + ">"
                                    plink.elem2 = "</" + CStr(Field) + ">"
                                    plink.elem3 = Field
                                End If
                            Else
                                plink.elem1 = plink.elem1 + rcontent
                            End If
                        Case "3"
                            'Identify the document identification
                            'Former we decided the pii=nd, but in database pii becomes the document file name
                            'This must be change some day, that means, people will insert the definitive pii
                            'hasDocIdinMarkup = True
                            If (StrComp(content, "nd", vbTextCompare) <> 0) Then
                                DocId = content
                            End If
                        
                        End Select
                        
                        
                    Case "4", "10"
                        Select Case proctype
                        Case "10"
                            htmlfragidx = htmlfragidx + 1
                            Call MARKUP_ConvertHTMLFragment2File(htmlfragpath, htmlfragidx, rcontent, scope, fieldkey, record, CLng(Field), Subf, format)
                        
                        Case "4"
                            'it is used when the content is NAMES type in DTD
                            'but in database it have to be inserted like a repetitive field_model
                            '??? - pages
        '                    If InStr(content, "%") > 0 Then
        '                        occsep = "%"
        '                    Else
        '                        occsep = Chr(32)
        '                        content = ReplaceString(content, Chr(160), occsep, vbBinaryCompare)
        '                    End If
                            If format = "%" Then
                                occsep = format
                            Else
                                occsep = Chr(32)
                                content = Replace(content, Chr(160), occsep, , , vbTextCompare)
                            End If
                            
                            
                            content = content + occsep
                            type4p1 = 1
                            type4p2 = InStr(type4p1, content, occsep)
                            type4count = 0
                            While type4p2 > 0
                                type4count = type4count + 1
                                type4 = Mid(content, type4p1, type4p2 - type4p1)
                                If Len(type4) > 0 Then Call MARKUP_ExecuteProcedure(type4, GroupIdx, fieldkey + CStr(type4count), LinkKey, record, recindex, CLng(Field), Subf, subf_preffix, format)
                                    
                                type4p1 = type4p2 + 1
                                type4p2 = InStr(type4p1, content, occsep)
                            Wend
                        End Select
                    
                    Case "0"
                        'no procedure available
                End Select
            Next
        End If
        Set proc = Nothing
        FormMarkup.ProgressBar1.Value = FormMarkup.ProgressBar1.Max
    Wend
    Close fn
    
    Kill ParserResult
    
    If oldPID <> "" Then
        Select Case article.IssueNo
        Case "review"
    
        Case "ahead"
            If article.VersionHistory.RVPDate <> "" Then
                article.VersionHistory.RVP_PID = oldPID
            End If
        Case Else
            If article.VersionHistory.AHPDate <> "" Then
                article.VersionHistory.AHP_PID = oldPID
            Else
                If article.VersionHistory.RVPDate <> "" Then
                    article.VersionHistory.RVP_PID = oldPID
                End If
            End If
        End Select
    Else
        previousDocVersion_exportData
    End If
    'FIXME_ identificar previous issue, instanciar old pid, instanciar historico
    
    Set reg = New ClRegistro
    Set f = New ClField
    For i = 1 To RecordInfo.Count
        Set reg = RepeatInAllRecords.Item(RecordInfo(i).Label, exist)
        If Not exist Then
            Set reg = RepeatInAllRecords.Add(RecordInfo(i).Label, RecordInfo(i).Label)
        End If
        Set f = reg.fields.Add("DocId", COMMONISISTAGS("pii").Value, DocId, RecordInfo(i).Label)
    Next
    Set f = Nothing
    Set reg = Nothing

    FormMarkup.ProgressBar1.Value = 0
    FormMarkup.ProgressBar1.Visible = False
    
    
    'Link the content which have to be linked
    Set reg = New ClRegistro
    Set f = New ClField
    For i = 1 To LinkedFields.Count
        j = 0
        exist = False
        While (Not exist) And (j < DBRecords.Count)
            j = j + 1
            Set f = DBRecords(j).fields.Item(LinkedFields.Item(i).Id, exist)
            If exist Then
                LinkedContent = f.conteudo
                For ReferenceIdx = 1 To LinkedFields.Item(i).RIdCount
                    Set f = DBRecords(j).fields.Item(LinkedFields.Item(i).RId(ReferenceIdx), exist)
                    If exist Then
                        f.conteudo = LinkedContent + f.conteudo
                    Else
                        Msg.GiveRunInformation (InterfaceLabels("MsgLinkedFieldNotExist").elem2 + LinkedFields.Item(i).RId(ReferenceIdx))
                    End If
                Next
                DBRecords(j).fields.Remove (LinkedFields.Item(i).Id)
            End If
        Wend
        If exist Then
        
        Else
            Msg.GiveRunInformation (InterfaceLabels("MsgLinkedFieldNotExist").elem2 + LinkedFields.Item(i).Id)
        End If
    Next
    Set LinkedFields = Nothing
    Set f = Nothing
    Set reg = Nothing
    
    'convert the contents whose special characteres depends on idiom to be converted
    Set f = New ClField
    For i = 1 To IdiomDependentFields.counter
        j = 0
        exist = False
        While (Not exist) And (j < DBRecords.Count)
            j = j + 1
            Set f = DBRecords(j).fields.Item(IdiomDependentFields.GetElem(i), exist)
            If exist Then
                P = InStr(f.conteudo, "^l")
                If P > 0 Then
                    idiom = Mid(f.conteudo, P + 2)
                    P = InStr(idiom, "^")
                    If P > 0 Then
                        idiom = Mid(idiom, 1, P - 1)
                    End If
                    f.conteudo = ConvertIdiom(f.conteudo, idiom)
                    If f.Tipo = "l" Then
                        f.conteudo = ConvertPercentCharacter(f.conteudo, idiom)
                    End If
                End If
            End If
        Wend
    Next
    Set f = Nothing
    Set IdiomDependentFields = Nothing
    
    
    'LawStructure
    LawStructureLevel
    
    
    MARKUP_ParserResult2Fields = (True)
End Function
'--------------------------------------------------------------------------------
'MARKUP_ExecuteProcedure - Execute the procedure on the marked content, that means,
'   the procedure will change the content, determine which field/subfield,
'   and alone/together other content it will be stored, and so on.
'
'   Each content can be stored or not in one or more RepeatInAllRecords.
'   Each field has a key <Key1> in <Fields> collection.
'   More than one content can be stored in the same field, like the name and surname author.
'
'content    - marked content
'GrpIdx - index of the group, if exist
'FieldKey   - used to identify the field where the content will be stored
'LinkKey   - used to identify two or more RepeatInAllRecords which will be linked together
'Return - <True> - no error found, <False> - error found
'--------------------------------------------------------------------------------
Private Sub MARKUP_ExecuteProcedure(content As String, GrpIdx As String, fieldkey As String, LinkKey As String, rectype As String, recidx As String, Field As Long, SubField As String, subf_preffix As String, format As String)
    Dim P As Long
    Dim exist As Boolean
    Dim formatedcontent As String
    Dim recitem As New ClRegistro
    Dim LinkedContent As New ClLink
    Dim Item As New ClField
    Dim idiomfield As ClField
    
    If Len(LinkKey) = 0 Then
        'this content will not be linked to another one
        If IsNumber(recidx) Then
            'Content will be stored in a specific record
            Set recitem = DBRecords.Item(rectype + recidx, exist)
            If Not exist Then
                Set recitem = DBRecords.Add(rectype + recidx)
            End If
            Set Item = recitem.fields.Item(fieldkey, exist)
            If Not exist Then
                Set Item = recitem.fields.Add(fieldkey)
                Item.Campo = Field
                Item.Tipo = rectype
                Item.Id = recidx
            End If
        Else
            'Content will be stored in more than one record
            Set recitem = RepeatInAllRecords.Item(rectype, exist)
            If Not exist Then
                Set recitem = RepeatInAllRecords.Add(rectype, rectype)
            End If
            Set Item = recitem.fields.Item(fieldkey, exist)
            If Not exist Then
                Set Item = recitem.fields.Add(fieldkey)
                Item.Campo = Field
                Item.Tipo = rectype
                Item.Id = recidx
            End If
        End If
        
        
        'change the presentation format of the content according to the conversion tables
        Select Case format
        Case WIN_FORMAT
            content = CloseOpenedTags(content)
            formatedcontent = Convert2Win(content)
        
        Case PARTIAL_HTML
            content = convertChar2Ent(content)
            content = CloseOpenedTags(content)
            formatedcontent = RmPartialHTML(content, True)
        
        Case FULL_HTML
            'formatedcontent = RmPartialHTML(content, False)
            content = convertChar2Ent(content)
            content = CloseOpenedTags(content)
            formatedcontent = content
        
        Case DOS_FORMAT
            content = CloseOpenedTags(content)
            formatedcontent = Convert2Win(content)
            'formatedcontent = CvtTables("Conversion windows to dos").Convert(formatedcontent)
            formatedcontent = ConvertPercentCharacter(formatedcontent)
            
        Case WIN_AND_IDIOM_DEPENDENT_FORMAT
            content = CloseOpenedTags(content)
            formatedcontent = Convert2Win(content)
            
            'store the key of the field whose content depends on idiom to be converted
            If Not IdiomDependentFields.exist(fieldkey) Then IdiomDependentFields.Insert (fieldkey)
            
        Case DOS_AND_IDIOM_DEPENDENT_FORMAT
            content = CloseOpenedTags(content)
            formatedcontent = Convert2Win(content)
            'formatedcontent = CvtTables("Conversion windows to dos").Convert(formatedcontent)
            
            'store the key of the field whose content depends on idiom to be converted
            If Not IdiomDependentFields.exist(fieldkey) Then IdiomDependentFields.Insert (fieldkey)
            
        Case DOS_FORMAT_FNAME
            content = CloseOpenedTags(content)
            formatedcontent = Convert2Win(content)
            'formatedcontent = CvtTables("Conversion windows to dos").Convert(formatedcontent)
            formatedcontent = ConvertPercentCharacter(formatedcontent)
            formatedcontent = Convert_LILACS_fname(formatedcontent)
        Case DOS_FORMAT_SURNAME
            content = CloseOpenedTags(content)
            formatedcontent = Convert2Win(content)
            'formatedcontent = CvtTables("Conversion windows to dos").Convert(formatedcontent)
            formatedcontent = ConvertPercentCharacter(formatedcontent)
            formatedcontent = Convert_LILACS_surname(formatedcontent)

        Case DOS_FORMAT_STITLE
            content = CloseOpenedTags(content)
            formatedcontent = Convert2Win(content)
           ' formatedcontent = CvtTables("Conversion windows to dos").Convert(formatedcontent)
            formatedcontent = ConvertPercentCharacter(formatedcontent)
        
        Case Else
            formatedcontent = content ' ReplaceString(content, Chr(32) + Chr(32), Chr(32), vbTextCompare)
        End Select
        
        
        
        formatedcontent = ReplaceString(Trim(formatedcontent), "  ", " ", vbTextCompare)
        
        If Len(SubField) = 0 Then
            'content will not be stored in subfield, content inserted directly in field
            Item.conteudo = formatedcontent + Item.conteudo + GrpIdx
        Else
            If SubField Like CONST_VALIDSUBFIELDS Then
                'content will be stored in subfield
                Item.conteudo = Item.conteudo + CONST_SUBFIELDINDICATOR + SubField + formatedcontent + GrpIdx
            Else
                If Len(subf_preffix) > 0 Then
                    Select Case subf_preffix
                    Case "*"
                        P = InStr(Item.conteudo, CONST_SUBFIELDINDICATOR)
                    Case Else
                        P = InStr(Item.conteudo, CONST_SUBFIELDINDICATOR + subf_preffix)
                        If P > 0 Then
                            P = InStr(P + 1, Item.conteudo, CONST_SUBFIELDINDICATOR)
                            If P = 0 Then
                                P = Len(Item.conteudo) + 1
                            End If
                        Else
                            SubField = CONST_SUBFIELDINDICATOR + subf_preffix + SubField
                        End If
                    End Select
                End If
                
                If P > 0 Then
                    Item.conteudo = Mid(Item.conteudo, 1, P - 1) + SubField + formatedcontent + Mid(Item.conteudo, P) + GrpIdx
                Else
                    Item.conteudo = Item.conteudo + SubField + formatedcontent + GrpIdx
                End If
            End If
        End If
    Else
        'Content will be linked to another content
        Set LinkedContent = LinkedFields.Item(fieldkey, exist)
        If exist Then
            LinkedContent.RIdCount = LinkedContent.RIdCount + 1
            LinkedContent.RId(LinkedContent.RIdCount) = LinkKey
        Else
            Set LinkedContent = LinkedFields.Add(fieldkey)
            LinkedContent.Id = LinkKey
        End If
    End If
    
    Set recitem = Nothing
    Set LinkedContent = Nothing
    Set Item = Nothing
    Set idiomfield = Nothing
End Sub

'--------------------------------------------------------------------------------
'MARKUP_Content2Fields - Execute the procedure on the marked content, that means,
'   the procedure will change the content, determine which field/subfield,
'   and alone/together other content it will be stored, and so on.
'
'   Each content can be stored or not in one or more RepeatInAllRecords.
'   Each field has a key <Key1> in <Fields> collection.
'   More than one content can be stored in the same field, like the name and surname author.
'
'content    - marked content
'GrpIdx - index of the group, if exist
'FieldKey   - used to identify the field where the content will be stored
'LinkKey   - used to identify two or more RepeatInAllRecords which will be linked together
'Return - <True> - no error found, <False> - error found
'--------------------------------------------------------------------------------
Private Sub MARKUP_Content2Fields(content As String, GrpIdx As String, fieldkey As String, LinkKey As String, rectype As String, recidx As String, Field As Long, SubField As String, subf_preffix As String, format As String)
    Dim Count As Long
    Dim Paragraphs() As String
    Dim i As Long
    Dim exist As Boolean
    Dim recitem As New ClRegistro
    Dim f As New ClField
    
    If IsNumber(recidx) Then
        'Content will be stored in a specific record
        Set recitem = DBRecords.Item(rectype + recidx, exist)
        If Not exist Then
            Set recitem = DBRecords.Add(rectype + recidx)
        End If
    End If
        
    Count = MARKUP_LAWPARTIALBODY(content, Paragraphs, format, fieldkey)
    For i = 1 To Count
    
        
        If SubField Like CONST_VALIDSUBFIELDS Then
            Paragraphs(i) = CONST_SUBFIELDINDICATOR + SubField + Paragraphs(i)
        End If
        Set f = recitem.fields.Add(, Field, Paragraphs(i), rectype, CLng(recidx), SubField)
        
    Next
                
    Set recitem = Nothing
    Set f = Nothing
    Erase Paragraphs
End Sub

'--------------------------------------------------------------------------------
'MARKUP_ParseDoc - Parse the document
'PathMarkup -   File path
'DocMarkup  -   File name
'MsgPath    -   Message file path
'MsgFile    -   Message file name
'ErrorCount -   Number of the error found
'Return - <True> - no error found, <False> - error found
'--------------------------------------------------------------------------------
Function MARKUP_ParseDoc(PathMarkup As String, DocMarkup As String, MsgPath As String, MsgFile As String, ErrorCount As Long) As Boolean
    Dim parser As ClParser
    Dim NoErrorFound As Boolean
    
    'Parse the document
    Set parser = New ClParser
    Call Msg.GiveRunInformation(InterfaceLabels("MsgAnalyseDoc").elem2, , True)
    If parser.Parse(PathMarkup, TmpDocFile, DTDCurrent, ParserResult) Then
        NoErrorFound = True
    End If
    
    'Write the error, if exist, in the lof file
    ErrorCount = parser.PrintParserErrors(MsgPath, MsgFile)
    Set parser = Nothing
    
    MARKUP_ParseDoc = NoErrorFound
End Function

'--------------------------------------------------------------------------------
'MARKUP_DocConfigRecord - Return the configuration record of the document
'--------------------------------------------------------------------------------
Function MARKUP_DocConfigRecord(MarkupFileName As String) As String
    Dim DocConfigRecord   As String
    Dim parser As ClParser
    Dim NoErrorFound As Boolean
    Dim exist As Boolean
    Dim i As Long
    
    Set parser = New ClParser
    Call parser.Parse(ConfigPath, ConfigFile, DTDCurrent, ParserResult)
    
    'Set the record information, like the record code and label, come from convert.ini file
    Call DB_InitiateRecordInfo(DTDCurrent.RecCode, DTDCurrent.RecLabel)
    
    If MARKUP_ParserResult2Fields(ConfigFile, MarkupFileName) Then
        If DB_SortRecords(ConfigPath, ConfigFile) Then
        
            
            DocConfigRecord = SortedRecords(2).conteudo
            
            If Len(DocConfigRecord) > 0 Then
                If UBound(BV(Currbv).getDocOrderLen(-1)) > 0 Then
                    With SortedRecords(2).fields
                    While (i < .Count) And (Not exist)
                        i = i + 1
                        If .Item(i).Campo = CLng(BV(Currbv).BVISISTAGS("order").Value) Then
                            exist = True
                        End If
                    Wend
                    If exist Then docOrder = .Item(i).conteudo
                    End With
                End If
                'Kill ConfigPath + PathSep + ConfigFile
            End If
        End If
        Set DBRecords = Nothing
    End If
    Set parser = Nothing
    
    MARKUP_DocConfigRecord = DocConfigRecord
End Function

'--------------------------------------------------------------------------------
'DB_InitiateRecordInfo - Initiate the information about the records of the database
'RecCode    - code of the record
'RecLabel   - label of the record
'--------------------------------------------------------------------------------
Private Sub DB_InitiateRecordInfo(RecCode As String, RecLabel As String)
    Dim q As Long
    Dim i As Long
    Dim code() As String
    Dim Label() As String
    
    Set RecordInfo = New ColRecordInfo
    q = GetElemStr(RecCode, "|", code)
    q = GetElemStr(RecLabel, "|", Label)
    
    For i = 1 To q
        Call RecordInfo.Add(code(i), i, Label(i))
    Next
    
    If q <> RecordInfo.Count Then MsgBox (InterfaceLabels("MsgWrongNumberofRecType").elem2)
    
    Erase code
    Erase Label
End Sub

Private Function DB_TagContents(ByVal conteudo As String, ByVal Tag As Long) As String
    DB_TagContents = privateContent.TagContent(conteudo, Tag)
End Function

'--------------------------------------------------------------------------------
'DB_BuildDocDatabase - Build Document Database
'PathMarkup -   Markup File path
'DocMarkup  -   Markup File name
'PathBody -   Body File path
'DocBody  -   Body File name
'Return - Sorted Records of the database
'--------------------------------------------------------------------------------
' FIXED_20070115 ahead of print
' if new-pid exist then do not load the fulltext [neither the references records]
'------------------------------------------------------------------------------------------
Function DB_BuildDocDatabase(DocId As String, _
                             PathMarkup As String, DocMarkup As String, _
                             PathBody As String, DocBody As String, _
                             PathTable As String, _
                             ISO_STITLE As String, PUBMONTH As String, _
                             url As String, _
                             LinkError As Boolean) As ColRegistro
    
        
    'Get the content of the markup
    LinkError = False
    
    Call Msg.GiveRunInformation(InterfaceLabels("MsgGettingFieldContents").elem2, False, True)
    Call DB_InitiateRecordInfo(DTDCurrent.RecCode, DTDCurrent.RecLabel)

    If MARKUP_ParserResult2Fields(DocId, DocMarkup, PathTable) Then
        
        If BV(Currbv).HasFulltext Then
            'Get the fulltext
            Call Msg.GiveRunInformation(InterfaceLabels("MsgPrepareFulltext").elem2, , True)
        
            
            If BODY_READ(PathBody, DocBody) Then
                LinkError = False
                If ReferencesCounter > 0 Then
                    'Match the references of the markup and the references of the body
                    Call Msg.GiveRunInformation(InterfaceLabels("MsgSettingReferenceLinks").elem2, False, True)
                    LinkError = LinkError Or (Not BODY_FindReferences)
                End If
                
                '---------------------
                ' link markup x body
                '---------------------
                If LinkMarkup2Body.Count > 0 Then
                    'Match the elements from markup and the elements from body
                    LinkError = LinkError Or (Not BODY_FindLinkMarkup2Body)
                End If
            
                Erase CompressionInfo
                Set CompressedInfo = Nothing

                'Get the paragraphs
                Call Msg.GiveRunInformation(InterfaceLabels("MsgGettingfulltext").elem2, , True)
                Call BODY_GetParagraphs(RecordInfo("paragraph").Label, BV(Currbv).BVISISTAGS("fulltext").Value, "", "    ^cY", 0)
            End If
        End If
    
        ' check previous version of the article, getting pid of ahead and/or review
        If Len(article.VersionHistory.RVPDate) > 0 Or Len(article.VersionHistory.AHPDate) > 0 Then
            Set previousDocument = ArticleAction.FindPreviousArticle(article, PreviousIssue)
            If Not (previousDocument Is Nothing) Then
                Call ArticleAction.importPreviousPIDs(article, previousDocument)
                If Not previousDocument.IsArchived Then
                    Call ArticleAction.init(PreviousIssue)
                    Call ArticleAction.archive(previousDocument)
                End If
            End If
        End If
        
        
        
        'Group the records
        Call Msg.GiveRunInformation(InterfaceLabels("MsgSortingRecords").elem2, , True)
        Call DB_SortRecords(PathMarkup, DocMarkup, DocId)
       
        'Lilacs Record
        Call Convert2LILACS(ISO_STITLE, PUBMONTH, url)
        
    End If
    Set DB_BuildDocDatabase = SortedRecords
End Function

'-----------------------------------------------------------------------
'DB_SortRecords - prepara/ordena para gravar um documento na base de dados
'DocPath  - caminho do documento
'DocName  - nome do arquivo do documento
'DocId  - identification of the document
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
' FIXED_20070115 ahead of print
' if new-pid exist then do not load the fulltext neither the references records
'------------------------------------------------------------------------------------------
Function DB_SortRecords(DocPath As String, DocName As String, Optional DocId As String) As Boolean
    Dim rec As ClRegistro
    Dim Item As ClRegistro
    Dim i As Long
    Dim j As Long
    Dim Index As Long
    Dim exist As Boolean
    Dim recordInfoCount As Long
                
    'Outline record contains the data about the document archive, its data do not come from
    'the markup document, like update date (See technical documentation for more details)
    Set rec = DBRecords(RecordInfo("outline").Label + "1", exist)
    If Not exist Then
        Set rec = DBRecords.Add(RecordInfo("outline").Label + "1")
    End If
    Call rec.fields.Add(, COMMONISISTAGS("update").Value, GetDateISO(Date))
    Call rec.fields.Add(, COMMONISISTAGS("update_time").Value, GetTimeISO(Time))

    Set rec = DBRecords(RecordInfo("header").Label + "1", exist)
    If Not exist Then
        Set rec = DBRecords.Add(RecordInfo("header").Label + "1")
    End If
    Call rec.fields.Add(, 881, article.VersionHistory.AHP_PID)
    Call rec.fields.Add(, 891, article.VersionHistory.RVP_PID)
    

    'Get the contents previously inserted in <RepeatInAllRecords> and put them in
    'each item of the correspondent <DBRecords>
    For i = 1 To RepeatInAllRecords.Count
        With RepeatInAllRecords(i)
        Index = 1
        Set rec = DBRecords(.Tipo + CStr(Index), exist)
        While exist
            For j = 1 To .fields.Count
                Call rec.fields.Add(, .fields(j).Campo, .fields(j).conteudo)
            Next
            Index = Index + 1
            Set rec = DBRecords(.Tipo + CStr(Index), exist)
        Wend
        End With
    Next
    Set RepeatInAllRecords = Nothing
    
    'Ordena os Records
    Set SortedRecords = New ColRegistro
    
    For i = 1 To RecordInfo.Count
        Index = 1
        Set rec = DBRecords.Item(RecordInfo(i).Label + CStr(Index), exist)
        While exist
            Set Item = SortedRecords.Add(RecordInfo(i).Label + CStr(Index))
            Set Item.fields = rec.fields
            Item.Id = rec.Id
            Item.Tipo = rec.Tipo
            
            Call Item.InfoFields.Add(, COMMONISISTAGS("docfile").Value, DocPath + PathSep + DocName)
            Call Item.InfoFields.Add(, COMMONISISTAGS("literattp").Value, DTDCurrent.LiteratureType)
            Call Item.InfoFields.Add(, COMMONISISTAGS("rectp").Value, RecordInfo(i).Label)
            Call Item.InfoFields.Add(, COMMONISISTAGS("docrecidx").Value, CStr(SortedRecords.Count))
            Call Item.InfoFields.Add(, COMMONISISTAGS("rectpidx").Value, CStr(Index))
            Call Item.InfoFields.Add(, COMMONISISTAGS("firsttag").Value, DTDCurrent.name)
            
            Index = Index + 1
            Set rec = DBRecords.Item(RecordInfo(i).Label + CStr(Index), exist)
        Wend
        
        'insert the record type counter as content in each record
        RecordInfo(i).Count = Index - 1
        For Index = 1 To RecordInfo(i).Count
            Set Item = SortedRecords.Item(RecordInfo(i).Label + CStr(Index))
            Call Item.InfoFields.Add(, COMMONISISTAGS("total of a record type").Value, RecordInfo(i).Count)
        Next
    Next
    
    
    Set DBRecords = Nothing
    Set rec = Nothing
    Set Item = Nothing
    
    DB_SortRecords = (SortedRecords.Count > 0)
End Function

'-----------------------------------------------------------------------
'Convert2LILACS - convert some fields to be according to LILACS
'ISO_STITLE  - journal short title in ISO format
'PUBMONTH  - issue publication month
'-----------------------------------------------------------------------
Private Sub Convert2LILACS(Optional ISO_STITLE As String, Optional PUBMONTH As String, Optional url As String)
    Dim Item As ClRegistro
    Dim i As Long
    Dim j As Long
    Dim P As Long
    Dim p1 As Long
    Dim p2 As Long
    Dim illustrative_type As String
    Dim aux As String
    Dim exist As Boolean
    Dim language As String
    Dim orgnames As ColRegistro

    
    Set Item = SortedRecords.Item("l1", exist)
    If exist Then
        Select Case Currbv
        Case "scielo"
            Call Item.InfoFields.Add(, 64, PUBMONTH)
            
            Set orgnames = New ColRegistro
            
            For i = 1 To Item.fields.Count
                With Item.fields(i)
                Select Case .Campo
                Case 30
                    ISO_STITLE = Trim(ISO_STITLE)
                    If Len(ISO_STITLE) > 0 Then
                        If Mid(ISO_STITLE, Len(ISO_STITLE), 1) = "." Then
                            ISO_STITLE = Mid(ISO_STITLE, 1, Len(ISO_STITLE) - 1)
                        End If
                    End If
                    .conteudo = ISO_STITLE
                    '.conteudo = CvtTables("Conversion windows to dos").Convert(ISO_STITLE)
                Case 38
                    If StrComp(.conteudo, "nd", vbTextCompare) = 0 Then
                        .conteudo = ""
                    Else
                        .conteudo = LCase(.conteudo)
                        .conteudo = ReplaceString(.conteudo, "fig", "ilus", vbTextCompare)
                    End If
                Case 121
                    If Len(url) > 0 Then
                        Call Item.fields.Add("8", 8, "Internet^i" + url + Right("00000" + .conteudo, 5))
                    End If
                Case 70
                   Call InsertAff(orgnames, .conteudo, "id123cspze", 3, 6, True)
                End Select
                End With
            Next
            
            For i = 1 To Item.fields.Count
                With Item.fields(i)
                Select Case .Campo
                Case 70
                   .conteudo = InsertAff(orgnames, .conteudo, "id123cspze", 3, 6, False)
                End Select
                End With
            Next
            'Call Item.fields.Add("38", 38, ReplaceString(LCase(ReplaceString(Trim(illustrative_type), " ", "%", vbTextCompare)), "fig", "ilus", vbTextCompare))
            Set orgnames = Nothing
            
        Case "bvslaw"
            For i = 1 To Item.InfoFields.Count
                With Item.InfoFields(i)
                Select Case .Campo
                Case 705
                    Call Item.InfoFields.Add(, 5, .conteudo)
                    Call Item.InfoFields.Add(, 6, "as")
                End Select
                End With
            Next
        End Select
    End If
    Set Item = Nothing
End Sub


'-----------------------------------------------------------------------
'MARKUP_ConvertHTMLFragment2File    - procedimento de acrescentar ao registro
'CampoIntermediario - campo na base gerada pelo parser
'tpreg      - Records em que o conteúdo será gravado
'grupo      - grupo do campo
'Campo      - campo em que o conteúdo será gravado
'Subcampo   - subcampo em que o conteúdo será gravado
'content   - conteúdo a ser gravado
'scope_tmp   - scope_tmp do conteúdo
'-----------------------------------------------------------------------
Private Sub MARKUP_ConvertHTMLFragment2File(htmlfragpath As String, htmlfragidx As Long, _
                                        content As String, _
                                        scope As String, _
                                        fieldkey As String, _
                                        rectype As String, _
                                        Field As Long, _
                                        SubField As String, _
                                        format As String)
    Dim P As Long
    Dim idxhtmlfrag As Long
    
    Dim subfield2 As String
    Dim existe As Boolean
    Dim existef As Boolean
    Dim LawStructElem As ClRegistro
    
    Dim fn As Long
    Dim key As String
    Dim root As String
    Dim element As String
    Dim found As Boolean
    Dim i As Long
    Dim j As Long
    Dim k As Long
    Dim f As ClField
    Dim status As String
    Dim fkey As String
    Dim body_parag() As String
    Dim body_count As Long
    
    
    idxhtmlfrag = MARKUP_ConvertHTMLFragment2File_GetFrag(content, format, fieldkey, htmlfragpath, htmlfragidx, body_parag, body_count)
    If body_count > 0 Then
    
        Call BV(Currbv).LawBodyTagsGetInfo(scope, key, root, element, status)
                    
        Set LawStructElem = New ClRegistro
        Set LawStructElem = LawStructure.GetLawRecord(key, element, root, fieldkey, rectype, status)
            
        Set f = New ClField
        If Len(fieldkey) > 0 Then
            'conteúdo na mesma ocorrência do campo
            fkey = fieldkey
        Else
            'ocorrências diferentes
            fkey = CStr(Field)
        End If
        
        For i = 1 To body_count
            If idxhtmlfrag <> i Then
                subfield2 = "^p"
            Else
               subfield2 = "^" + SubField
            End If
            With LawStructElem
            Set f = .fields.Item(fkey, existef)
            If existef Then
                If Len(fieldkey) > 0 Then
                    If InStr(f.conteudo, subfield2) > 0 Then
                        Call .fields.Add(, Field, subfield2 + body_parag(i))
                    Else
                        If Len(subfield2) > 0 Then
                            f.conteudo = f.conteudo + subfield2 + body_parag(i)
                        Else
                            f.conteudo = subfield2 + body_parag(i) + f.conteudo
                        End If
                    End If
                Else
                    Call .fields.Add(, Field, subfield2 + body_parag(i))
                End If
            Else
                Call .fields.Add(fkey, Field, subfield2 + body_parag(i))
            End If
            Set f = Nothing
            End With
        Next
        Set LawStructElem = Nothing
    End If
End Sub

'-----------------------------------------------------------------------
'MARKUP_BuildLawStructure    - procedimento de acrescentar ao registro
'CampoIntermediario - campo na base gerada pelo parser
'tpreg      - Records em que o conteúdo será gravado
'grupo      - grupo do campo
'Campo      - campo em que o conteúdo será gravado
'Subcampo   - subcampo em que o conteúdo será gravado
'content   - conteúdo a ser gravado
'scope_tmp   - scope_tmp do conteúdo
'-----------------------------------------------------------------------
Private Sub MARKUP_BuildLawStructure(content As String, _
                                        scope As String, _
                                        fieldkey As String, _
                                        rectype As String, _
                                        Field As Long, _
                                        SubField As String, _
                                        format As String)
    Dim subfield2 As String
    Dim existe As Boolean
    Dim existef As Boolean
    Dim LawStructElem As ClRegistro
    
    Dim fn As Long
    Dim key As String
    Dim root As String
    Dim element As String
    Dim found As Boolean
    Dim i As Long
    Dim j As Long
    Dim k As Long
    Dim body_parag() As String
    Dim body_count As Long
    Dim f As ClField
    Dim status As String
    Dim fkey As String
    Dim P As Long
    Dim level As Long
    
    Call BV(Currbv).LawBodyTagsGetInfo(scope, key, root, element, status)
            
    ' verifica existencia do registro
    Set LawStructElem = New ClRegistro
    Set LawStructElem = LawStructure.GetLawRecord(key, element, root, fieldkey, rectype, status)
    
    
    'Verifica se <content> ficara distribuido em mais de um campo.
    
    body_count = MARKUP_LAWPARTIALBODY(content, body_parag, format, fieldkey)
    For i = 1 To body_count
        
        If Len(body_parag(i)) > 0 Then
            
            'no/name/content/titlediv
            With LawStructElem
            If Len(body_parag(i)) > 0 Then
                If Len(SubField) > 0 Then
                    subfield2 = "^" + SubField
                Else
                    subfield2 = ""
                End If
                
                Set f = New ClField
                If Len(fieldkey) > 0 Then
                    'conteúdo na mesma ocorrência do campo
                    fkey = fieldkey
                Else
                    'ocorrências diferentes
                    fkey = CStr(Field)
                End If
                
                Set f = .fields.Item(fkey, existef)
                If existef Then
                    If Len(fieldkey) > 0 Then
                        If InStr(f.conteudo, subfield2) > 0 Then
                            Call .fields.Add(, Field, subfield2 + body_parag(i))
                        Else
                            If Len(subfield2) > 0 Then
                                f.conteudo = f.conteudo + subfield2 + body_parag(i)
                            Else
                                f.conteudo = subfield2 + body_parag(i) + f.conteudo
                            End If
                        End If
                    Else
                        Call .fields.Add(, Field, subfield2 + body_parag(i))
                    End If
                Else
                    Call .fields.Add(fkey, Field, subfield2 + body_parag(i))
                End If
                
            End If
            End With
        End If
    Next
    
    Erase body_parag
    Set LawStructElem = Nothing
End Sub


'-----------------------------------------------------------------------
'MARKUP_LAWPARTIALBODY   - convert the body bodycontent into various paragraphs
'bodycontent   - body bodycontent
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Private Function MARKUP_LAWPARTIALBODY(bodycontent As String, Paragraphs() As String, format As String, fieldkey As String) As Long
    
    
    Set BODY_Text = New ClTxt
    If Len(bodycontent) > 0 Then
        bodycontent = BODY_StandardizeEndParag(bodycontent, BVSLAWBREAKMARK + STANDARDIZEDENDPARAG)
        'change the presentation format of the bodycontent according to the conversion tables
        Select Case format
        Case WIN_FORMAT, PARTIAL_HTML, WIN_AND_IDIOM_DEPENDENT_FORMAT
            Select Case format
            Case WIN_FORMAT
                bodycontent = CloseOpenedTags(bodycontent)
                bodycontent = Convert2Win(bodycontent)
            
            Case PARTIAL_HTML
                bodycontent = CloseOpenedTags(bodycontent)
                bodycontent = RmPartialHTML(bodycontent, True)
        
            Case WIN_AND_IDIOM_DEPENDENT_FORMAT
                bodycontent = CloseOpenedTags(bodycontent)
                bodycontent = Convert2Win(bodycontent)
                
                'store the key of the field whose bodycontent depends on idiom to be converted
                If Not IdiomDependentFields.exist(fieldkey) Then IdiomDependentFields.Insert (fieldkey)
            End Select
        Case FULL_HTML, DOS_FORMAT, DOS_AND_IDIOM_DEPENDENT_FORMAT
            Select Case format
            Case FULL_HTML
                'bodycontent = RmPartialHTML(bodycontent, False)
                bodycontent = CloseOpenedTags(bodycontent)
                'bodycontent = bodycontent
        
            Case DOS_FORMAT
                bodycontent = CloseOpenedTags(bodycontent)
                bodycontent = Convert2Win(bodycontent)
                'bodycontent = CvtTables("Conversion windows to dos").Convert(bodycontent)
                bodycontent = ConvertPercentCharacter(bodycontent)
                
            Case DOS_AND_IDIOM_DEPENDENT_FORMAT
                bodycontent = CloseOpenedTags(bodycontent)
                bodycontent = Convert2Win(bodycontent)
                'bodycontent = CvtTables("Conversion windows to dos").Convert(bodycontent)
                
                'store the key of the field whose bodycontent depends on idiom to be converted
                If Not IdiomDependentFields.exist(fieldkey) Then IdiomDependentFields.Insert (fieldkey)
            End Select
        
        Case DOS_FORMAT_FNAME, DOS_FORMAT_SURNAME, DOS_FORMAT_STITLE, WIN_FORMAT_TABLE
            Select Case format
            Case DOS_FORMAT_FNAME
                bodycontent = CloseOpenedTags(bodycontent)
                bodycontent = Convert2Win(bodycontent)
                'bodycontent = CvtTables("Conversion windows to dos").Convert(bodycontent)
                bodycontent = ConvertPercentCharacter(bodycontent)
                bodycontent = Convert_LILACS_fname(bodycontent)
            
            Case DOS_FORMAT_SURNAME
                bodycontent = CloseOpenedTags(bodycontent)
                bodycontent = Convert2Win(bodycontent)
                'bodycontent = CvtTables("Conversion windows to dos").Convert(bodycontent)
                bodycontent = ConvertPercentCharacter(bodycontent)
                bodycontent = Convert_LILACS_surname(bodycontent)
    
            Case DOS_FORMAT_STITLE
                bodycontent = CloseOpenedTags(bodycontent)
                bodycontent = Convert2Win(bodycontent)
                'bodycontent = CvtTables("Conversion windows to dos").Convert(bodycontent)
                bodycontent = ConvertPercentCharacter(bodycontent)
            
            Case WIN_FORMAT_TABLE
                bodycontent = CloseOpenedTags(bodycontent)
                If InStr(1, bodycontent, BVSLAWBREAKMARK + STANDARDIZEDENDPARAG, vbBinaryCompare) > 0 Then
                    bodycontent = Replace(bodycontent, BVSLAWBREAKMARK + STANDARDIZEDENDPARAG, "")
                    bodycontent = bodycontent + BVSLAWBREAKMARK
                End If
                bodycontent = convertTable(bodycontent)
            End Select
        Case Else
            'bodycontent = bodycontent ' ReplaceString(bodycontent, Chr(32) + Chr(32), Chr(32), vbTextCompare)
        End Select
            
        If Len(Trim(Replace(bodycontent, BVSLAWBREAKMARK + STANDARDIZEDENDPARAG, ""))) > 0 Then
            bodycontent = ReplaceString(Trim(bodycontent), "  ", " ", vbTextCompare)
            BODY_Text.AddLines (bodycontent)
            MARKUP_LAWPARTIALBODY = MARKUP_GetParagraphs(bodycontent, Paragraphs)
        End If
    End If
    Set BODY_Text = Nothing

End Function


'-----------------------------------------------------------------------
'MARKUP_GetParagraphs  - obtém parágrafos do BODY_Text completo
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Private Function MARKUP_GetParagraphs(bodycontent As String, Paragraphs() As String) As Long
    Dim ret         As Boolean
    Dim TagParag    As String
    Dim P           As TpPosition
    Dim LimInf      As TpPosition
    Dim LimSup      As TpPosition
    Dim ParagIni    As TpPosition
    Dim ParagEnd    As TpPosition
    Dim j           As Long
    Dim prossegue   As Boolean
    Dim s           As String
    Dim PRefMark1   As Long
    Dim PRefMark2   As Long
    Dim Mark        As String
    
    Dim ParagraphCount As Long
    Dim PartialParag()     As String
    Dim PartialParagCount    As Long
    
    'Obtem o body html sem tags de marcacao
    With BODY_Text
    LimInf.i = 1
    LimInf.j = 1
    Call .GetEnd(LimSup.i, LimSup.j)
    If .GetLen(LimInf.i, LimInf.j, LimSup.i, LimSup.j) > 0 Then
        Call .InString(LimInf.i, LimInf.j, LimSup.i, LimSup.j, "<body", P.i, P.j, vbTextCompare)
        If P.j > 0 Then
            Call .InString(P.i, P.j, LimSup.i, LimSup.j, ">", LimInf.i, LimInf.j, 1)
            Call .ForwardPosition(LimInf.i, LimInf.j, 1)
            Call .InString(LimInf.i, LimInf.j, LimSup.i, LimSup.j, "</body", P.i, P.j, vbTextCompare)
            LimSup = P
            Call .RewardPosition(LimSup.i, LimSup.j, 1)
        End If

        '--counter = 0
        prossegue = .ExisteStr(LimInf.i, LimInf.j, LimSup.i, LimSup.j)
        While prossegue
            TagParag = BODY_FindNewParagraph(LimInf, LimSup, P)
            ParagIni = LimInf
            LimInf = P
            If P.j > 0 Then
                Call .ForwardPosition(LimInf.i, LimInf.j, Len(TagParag))  'obtem o novo ParagIni
                'ParagEnd = LimInf 'obtem o ParagEnd parcial
                ParagEnd = P 'obtem o ParagEnd parcial
                Call .RewardPosition(ParagEnd.i, ParagEnd.j, 1)
            Else
                ParagEnd = LimSup
                prossegue = False
            End If
            PartialParagCount = BODY_GetParagraph(ParagIni, ParagEnd, PartialParag)
            
            For j = 1 To PartialParagCount
                If Len(PartialParag(j)) > 0 Then
                    ParagraphCount = ParagraphCount + 1
                    ReDim Preserve Paragraphs(ParagraphCount)
                    Paragraphs(ParagraphCount) = PartialParag(j)
                End If
            Next
            
        Wend
    End If
    End With
    
    Erase PartialParag
    Set BODY_Text = Nothing
    MARKUP_GetParagraphs = ParagraphCount
End Function

'-----------------------------------------------------------------------
'BODY_RmEntitiesHTML - remove todas entidades HTML existentes na string
's           - string
'Retorno     - string sem entidades HTML
'-----------------------------------------------------------------------
Function BODY_RmEntitiesHTML(s As String) As String
    Dim original As String
    Dim p1 As Long
    Dim p2 As Long
    Dim P3 As Long
    Dim nova As String
    Dim entity As String

    original = s
    While Len(original) > 0
        p1 = InStr(original, "&")
        p2 = InStr(original, ";")
        If (p1 = 0) Or (p2 = 0) Then
            nova = Trim(nova) + Chr(32) + Trim(original)
            original = ""
        ElseIf p1 < p2 Then
            P3 = InStr(p1 + 1, original, "&", vbBinaryCompare)
            While (P3 > 0) And (P3 < p2)
                p1 = P3
                P3 = InStr(p1 + 1, original, "&", vbBinaryCompare)
            Wend
            
            entity = Mid(original, p1, p2 - p1 + 1)
            If InStr(1, entity, " ", vbTextCompare) > 0 Then
                nova = Trim(nova) + Chr(32) + Trim(Mid(original, 1, p2))
            Else
                nova = Trim(nova) + Chr(32) + Trim(Mid(original, 1, p1 - 1))
            End If
            original = Trim(Mid(original, p2 + 1))
        Else
            nova = nova + Mid(original, 1, p2)
            original = Mid(original, p2 + 1)
        End If
    Wend
    BODY_RmEntitiesHTML = Trim(nova)
End Function

Sub LawStructureLevel()
    Dim LawHier As ColPair
    Dim i As Long
    Dim level As Long
    Dim reg As ClRegistro
    Dim reg2 As ClRegistro
    Dim f As ClField
    Dim exist As Boolean
    Dim status As String
    Dim index_content As String
    Dim j As Long
    Dim inicio() As Long
    Dim fim() As Long
    Dim reccontent() As String
    Dim NewRecCount As Long
    Dim RecordCount As Long
    Dim k As Long
    Dim key As String
    Dim Copy As ClRegistro
    Dim header() As String
    Dim nheader As Long
    
    Set LawHier = New ColPair
    Set f = New ClField
    Set reg2 = New ClRegistro
    
    'inicializa o registro que contem o indice
    If LawStructure.Count > 0 Then
        Set reg2 = DBRecords.Item(RecordInfo("index").Label + "1", exist)
        If Not exist Then
            Set reg2 = DBRecords.Add(RecordInfo("index").Label + "1")
        End If
    End If
    
    For i = 1 To LawStructure.Count
    
        With LawStructure(i)
            
        Set f = .fields("999", exist)
        If exist Then
            status = f.conteudo
            Call .fields.Remove("999")
        End If
        Set f = .fields("200", exist)
        If exist Then
            key = f.conteudo
        End If
        
        Call SetLevel(i, status, LawHier)
            
'        If status <> "none" Then
        If status = "part" Then
            
            index_content = ""
            Set f = .fields("202", exist)
            If exist Then
               index_content = index_content + "^t" + .fields("202").conteudo
            Else
                nheader = .OccNumber(208, header)
                For j = 2 To nheader
                    header(1) = header(1) + header(j)
                Next
                If nheader > 0 Then
                    header(1) = Replace(header(1), BVSLAWBREAKMARK, " ")
                    index_content = index_content + "^t" + header(1)
                    exist = True
                End If
            End If
            
            If exist Then
                Set f = .fields("201", exist)
                If exist Then index_content = index_content + "^i" + .fields("201").conteudo
                
                Set f = .fields("200", exist)
                If exist Then index_content = index_content + "^k" + f.conteudo
                     
                Set f = .fields("205", exist)
                If exist Then index_content = "^n" + .fields("205").conteudo + index_content
                     
                Call reg2.fields.Add(, 200, index_content)
            End If
        End If
        
        'Insert LawStructure(i) into DBRecords
        NewRecCount = SeparateRecords(i, reccontent, inicio, fim)
        If NewRecCount = 0 Then
            Set f = .fields("208", exist)
            If exist Then
                RecordCount = RecordCount + 1
                Set reg = New ClRegistro
                Set reg = DBRecords.Item(.Tipo + CStr(RecordCount), exist)
                If Not exist Then
                    Set reg = DBRecords.Add(.Tipo + CStr(RecordCount), .Tipo, CStr(RecordCount), LawStructure(i))
                End If
            End If
        Else
            For j = 1 To NewRecCount
                RecordCount = RecordCount + 1
                Set reg = New ClRegistro
                Set reg = DBRecords.Item(.Tipo + CStr(RecordCount), exist)
                If Not exist Then
                    If j = 1 Then Set reg = DBRecords.Add(.Tipo + CStr(RecordCount), .Tipo, CStr(RecordCount), LawStructure(i))
                    
                    If NewRecCount > 1 Then
                                        
                        If j = 1 Then
                            reg.DelFields (203)
                            Set Copy = New ClRegistro
                            Set Copy = .Copy
                            For k = 1 To NewRecCount - 1
                                Call reg.fields.Add(, 217, key + "_" + CStr(k))
                            Next
                        ElseIf j > 1 Then
                            Set reg = Copy.Copy
                            Set reg = DBRecords.Add(.Tipo + CStr(RecordCount), .Tipo, CStr(RecordCount), reg)
                            Call reg.fields.Add(, 216, key)
                            Call reg.fields.Remove("200")
                            Call reg.fields.Add("200", 200, key + "_" + CStr(j - 1))
                        End If
                        
                        For k = inicio(j) To fim(j)
                            Call reg.fields.Add(, 203, reccontent(k))
                        Next
                    End If
                End If
                Set reg = Nothing
            Next
        End If
        End With
    Next
    Set reg = Nothing
    Set reg2 = Nothing
    Set f = Nothing
    Set LawStructure = Nothing
    Set LawHier = Nothing
    Set Copy = Nothing
    
    Erase inicio
    Erase fim
    Erase header
    Erase reccontent
End Sub


Private Function InsertAff(orgnames As ColRegistro, ByVal aff As String, aff_subf As String, orgname_idx As Long, location_idx As Long, Insert As Boolean) As String
    Dim Item As ClRegistro
    Dim exist As Boolean
    Dim orgname As String
    Dim location As String
    
    Dim aff_content() As String
    Dim i As Long
    Dim new_aff As String
    Dim old_aff As String
    Dim P As Long
    
    'aff = "^o" + aff
    'aff_subf = "id123cspze"
    old_aff = aff
    If Mid(aff, 1, 1) <> "^" Then
        aff = "^" + Mid(aff_subf, orgname_idx, 1) + aff
        P = 3
    Else
        P = 1
    End If
    
    ReDim aff_content(Len(aff_subf))
    For i = 1 To Len(aff_subf)
        aff_content(i) = GetSubfContent(aff, Mid(aff_subf, i, 1))
    Next
    
    orgname = aff_content(orgname_idx)
    location = ""
    For i = location_idx To Len(aff_subf)
        location = location + aff_content(i)
    Next
    
    If Insert Then
        Set Item = New ClRegistro
        If Len(location) > 0 Then
            Set Item = orgnames(orgname, exist)
            If exist Then
                For i = 1 To Len(aff_subf)
                    If Len(Item.fields(i).conteudo) = 0 Then
                        Item.fields(i).conteudo = aff_content(i)
                    End If
                Next
            Else
                Set Item = orgnames.Add(orgname)
                For i = 1 To Len(aff_subf)
                    Call Item.fields.Add(CStr(i), i, aff_content(i))
                Next
            End If
        End If
    Else
        If Len(location) = 0 Then
            Set Item = orgnames(orgname, exist)
            If exist Then
                For i = 1 To location_idx - 1
                    If Len(aff_content(i)) > 0 Then
                        new_aff = new_aff + "^" + Mid(aff_subf, i, 1) + aff_content(i)
                    End If
                Next
                For i = location_idx To Len(aff_subf)
                    If Len(aff_content(i)) = 0 Then
                        aff_content(i) = Item.fields(i).conteudo
                    End If
                    If Len(aff_content(i)) > 0 Then
                        new_aff = new_aff + "^" + Mid(aff_subf, i, 1) + aff_content(i)
                    End If
                Next
                new_aff = Mid(new_aff, P)
            Else
                new_aff = old_aff
            End If
        Else
            new_aff = old_aff
        End If
    End If
    
    Erase aff_content
    InsertAff = new_aff
    
End Function

Private Function GetSubfContent(fieldcontent As String, Subf As String) As String
    Dim P As Long
    Dim p2 As Long
    Dim subfcontent As String
    
    P = InStr(fieldcontent, CONST_SUBFIELDINDICATOR + Subf)
    If P > 0 Then
        p2 = InStr(P + 1, fieldcontent, CONST_SUBFIELDINDICATOR, vbBinaryCompare)
        If p2 = 0 Then p2 = Len(fieldcontent) + 1
        subfcontent = Mid(fieldcontent, P + 2, p2 - P - 2)
    End If
    GetSubfContent = subfcontent
End Function


'-----------------------------------------------------------------------
'BODY_FindLinkMarkup2Body - find the references in full text
'Return - <True> - if all references were found, <False> - otherwise
'-----------------------------------------------------------------------
Private Function BODY_FindLinkMarkup2Body() As Boolean
    Dim ret As Boolean
    Dim i As Long
    Dim LimInf As TpPosition
    Dim LimSup As TpPosition
    Dim r As String
    Dim found As Boolean
    Dim LinkMarkup2BodyStrlen As Long
    Dim j As Long
    Dim linkText As String
    
    
    LimInf.i = 1
    LimInf.j = 1
    Call CompressedInfo.GetEnd(LimSup.i, LimSup.j)
    
    ret = True
    For i = 1 To LinkMarkup2Body.Count
        'prepare link to compare them
        
        LinkMarkup2Body(i).elem1 = BODY_RmSymbolHTML(LinkMarkup2Body(i).elem1)
        LinkMarkup2Body(i).elem1 = BODY_RmEntitiesHTML(LinkMarkup2Body(i).elem1)
        LinkMarkup2BodyStrlen = Len(LinkMarkup2Body(i).elem1)
        Debug.Print LinkMarkup2Body(i).elem1
        
        linkText = ""
        For j = 1 To LinkMarkup2BodyStrlen
            If Mid(LinkMarkup2Body(i).elem1, j, 1) Like "[A-Za-z0-9]" Then
                linkText = linkText + Mid(LinkMarkup2Body(i).elem1, j, 1)
            End If
        Next
        'Set LinkMarkup2Body(i) = nothing
        
        'find the link in body
        found = BODY_FindLinkMarkup2BodyInText(LinkMarkup2Body(i).elem2 + LinkMarkup2Body(i).elem1 + LinkMarkup2Body(i).elem3, linkText, LimInf, LimSup)
        If Not found Then
            r = r + COMMA + LinkMarkup2Body(i).elem1
        End If
        
        'free memory
        ret = ret And found
    Next
    
    Set LinkMarkup2Body = Nothing
    
    
    If Not ret Then
        r = Mid(r, 2)
        Call Msg.GiveRunInformation(InterfaceLabels("MsgMissingLink").elem2 + r)
    End If
    BODY_FindLinkMarkup2Body = ret
End Function

'-----------------------------------------------------------------------
'BODY_FindLinkMarkup2BodyInText - Find a linkText in body file
'LinkTextMark - mark to identify the link text record
'linkText - linkText to find
'LimInf - initial position at the body to find the linkText
'LimSup - final position of the linkText found
'Return - <True> to success and <False> to failure
'-----------------------------------------------------------------------
Private Function BODY_FindLinkMarkup2BodyInText(LinkTextMark As String, linkText As String, LimInf As TpPosition, LimSup As TpPosition) As Boolean
    Dim LinkTextInitialPos As TpPosition
    Dim LinkTextFinalPos As TpPosition
    Dim p1 As Long
    Dim uncompressedtext As String
    Dim OK As Boolean
    Dim li As TpPosition
    Dim ls As TpPosition
    
    li = LimInf
    ls = LimSup
    
    Call CompressedInfo.New_InString(LimInf.i, LimInf.j, LimSup.i, LimSup.j, linkText, LinkTextInitialPos.i, LinkTextInitialPos.j, vbBinaryCompare)
    If LinkTextInitialPos.j = 0 Then
        LimInf = li
        LimSup = ls
        Call CompressedInfo.New_InString(LimInf.i, LimInf.j, LimSup.i, LimSup.j, linkText, LinkTextInitialPos.i, LinkTextInitialPos.j, vbTextCompare)
    End If
    
    If LinkTextInitialPos.j > 0 Then
        With CompressedInfo
        'Update the next start position (LimInf)
        LinkTextFinalPos = LinkTextInitialPos
        Call .ForwardPosition(LinkTextFinalPos.i, LinkTextFinalPos.j, Len(linkText))
        LimInf = LinkTextFinalPos
    
        'Calculate the position of the beggining of the linkText in the complete text to insert the paragraph mark
        uncompressedtext = BODY_UnCompressLine(Mid(.GetLine(LinkTextInitialPos.i), 1, LinkTextInitialPos.j), CompressionInfo(LinkTextInitialPos.i))
        LinkTextInitialPos.j = Len(uncompressedtext)
        
        'Calculate the position of the end of the linkText in the complete text to insert the linkText mark
        Call .RewardPosition(LinkTextFinalPos.i, LinkTextFinalPos.j, 1)
        uncompressedtext = BODY_UnCompressLine(Mid(.GetLine(LinkTextFinalPos.i), 1, LinkTextFinalPos.j), CompressionInfo(LinkTextFinalPos.i))
        LinkTextFinalPos.j = Len(uncompressedtext)
                
        End With
        
        With BODY_Text
        'Check the exact position to insert the linkText mark
        'If BODY_FindEndLinkText(LinkTextFinalPos.i, LinkTextFinalPos.j) Then
        
        If (LinkTextInitialPos.i = LinkTextFinalPos.i) Then
            'Insert the record separator
            .SetLine(LinkTextInitialPos.i) = Mid(.GetLine(LinkTextInitialPos.i), 1, LinkTextInitialPos.j - 1) + _
                                            STANDARDIZEDENDPARAG + _
                                            Mid(.GetLine(LinkTextInitialPos.i), LinkTextInitialPos.j, LinkTextFinalPos.j - LinkTextInitialPos.j + 1) + _
                                            LinkTextMark + _
                                            STANDARDIZEDENDPARAG + _
                                            Mid(.GetLine(LinkTextFinalPos.i), LinkTextFinalPos.j + 1)
                                            
            'Update the compression information
             CompressionInfo(LinkTextInitialPos.i) = Mid(CompressionInfo(LinkTextInitialPos.i), 1, LinkTextInitialPos.j - 1) + _
                                                        String(Len(STANDARDIZEDENDPARAG), "0") + _
                                                        Mid(CompressionInfo(LinkTextInitialPos.i), LinkTextInitialPos.j, LinkTextFinalPos.j - LinkTextInitialPos.j + 1) + _
                                                        String(Len(LinkTextMark + STANDARDIZEDENDPARAG), "0") + _
                                                        Mid(CompressionInfo(LinkTextInitialPos.i), LinkTextFinalPos.j + 1)
            OK = True
        Else
            'Insert the record separator
            .SetLine(LinkTextInitialPos.i) = Mid(.GetLine(LinkTextInitialPos.i), 1, LinkTextInitialPos.j - 1) + STANDARDIZEDENDPARAG + Mid(.GetLine(LinkTextFinalPos.i), LinkTextInitialPos.j + 1)
            'Update the compression information
             CompressionInfo(LinkTextInitialPos.i) = Mid(CompressionInfo(LinkTextInitialPos.i), 1, LinkTextInitialPos.j - 1) + String(Len(STANDARDIZEDENDPARAG), "0") + Mid(CompressionInfo(LinkTextInitialPos.i), LinkTextInitialPos.j)
            
            'Insert the linkText mark
            .SetLine(LinkTextFinalPos.i) = Mid(.GetLine(LinkTextFinalPos.i), 1, LinkTextFinalPos.j) + LinkTextMark + STANDARDIZEDENDPARAG + Mid(.GetLine(LinkTextFinalPos.i), LinkTextFinalPos.j + 1)
            'Update the compression information
             CompressionInfo(LinkTextFinalPos.i) = Mid(CompressionInfo(LinkTextFinalPos.i), 1, LinkTextFinalPos.j) + String(Len(LinkTextMark + STANDARDIZEDENDPARAG), "0") + Mid(CompressionInfo(LinkTextFinalPos.i), LinkTextFinalPos.j + 1)
            
            OK = True
        'Else
        '    Debug.Print "Não Reconheceu " + .GetLine(LinkTextFinalPos.i)
        End If
        End With
        
    Else
        Debug.Print linkText
        
    End If
    
    BODY_FindLinkMarkup2BodyInText = OK
End Function

Private Sub SetLevel(i As Long, status As String, LawHier As ColPair)
    Dim LawElem As ClPair
    Dim f As ClField
    Dim exist As Boolean
    Dim elem_name As String
    Dim level As Long
    Dim found As Boolean
    Dim father As String
    Dim parents() As String
    Dim j As Long
    Dim k As Long
    
    ' encontra hierarquia: nivel, pais, filhos
    Set LawElem = New ClPair
    
    With LawStructure(i)
    Select Case status
    Case "none"
        'body ou attach
        level = 1
    Case Else
        Set f = .fields("202", exist)
        If exist Then elem_name = f.conteudo
        
        If Len(elem_name) = 0 Then
            'part sem header
            While LawHier.Count > 0
                LawHier.Remove (LawHier.Count)
            Wend
            elem_name = status
        End If
        
        If Len(elem_name) > 0 Then
            'Outros
            'Find the level of the current elem_name
            level = 0
            found = False
            While (level < LawHier.Count) And (Not found)
                level = level + 1
                If StrComp(LawHier(level).elem1, elem_name, vbTextCompare) <> 0 Then
                    'set parents of the current elem_name
                    father = LawHier(level).elem2 + "^n" + CStr(level)
                    Call .fields.Add(, 206, father)
                Else
                    found = True
                End If
            Wend
            
            If found Then
                While LawHier.Count >= level
                    LawHier.Remove (LawHier.Count)
                Wend
            End If
                        
            Set LawElem = LawHier.Add(elem_name)
            LawElem.elem1 = elem_name
            LawElem.elem2 = .fields("200").conteudo
            level = LawHier.Count
            
            'set current elem_name as son of higher levels
            For j = 1 To level - 1
                Call LawStructure.Item(LawHier(j).elem2).fields.Add(, 207, LawElem.elem2 + "^n" + CStr(level))
'                '----------------
'                ' insere campo 207 (filhos) nos registros de mesmo nivel
'                For k = 1 To LawStructure.Item(LawHier(j).elem2).OccNumber(217, parents)
'                    Call LawStructure.Item(parents(k)).fields.Add(, 207, LawElem.elem2 + "^n" + CStr(level))
'                Next
'                '----------------
            Next
        
'            '----------------
'            ' insere campo 206 (pai) nos registros de mesmo nivel
'            For k = 1 To .OccNumber(217, parents)
'                Call LawStructure(parents(k)).fields.Add(, 206, father)
'                Call LawStructure(parents(k)).fields.Add("202", 202, elem_name)
'            Next
'            '----------------
        End If
    End Select
    
    'level
    Call .fields.Add("205", 205, CStr(level))
    End With
    
    Erase parents
    Set LawElem = Nothing
End Sub

Private Function SeparateRecords(i As Long, reccontent() As String, inicio() As Long, fim() As Long) As Long
    Dim ndiv As Long
    Dim nrecord As Long
    Dim maxlen As Long
    Dim minlen As Long
    Dim currlen As Long
    Dim j As Long
    
    With LawStructure(i)
        maxlen = 8000
        nrecord = .OccNumber(203, reccontent)
        If Len(.conteudo) < maxlen Then
            If nrecord > 0 Then
            ndiv = 1
            ReDim Preserve inicio(ndiv)
            ReDim Preserve fim(ndiv)
            inicio(ndiv) = 1
            fim(ndiv) = nrecord
            End If
        Else
            minlen = Len(.conteudo)
            For j = 1 To nrecord
                minlen = minlen - Len(reccontent(j))
            Next
            
            If maxlen > minlen Then
                maxlen = maxlen - minlen
            Else
                maxlen = 200
            End If
        
            j = 0
            While (j < nrecord)
                j = j + 1
                            
                If currlen = 0 Then
                    ndiv = ndiv + 1
                    ReDim Preserve inicio(ndiv)
                    ReDim Preserve fim(ndiv)
                    inicio(ndiv) = j
                    fim(ndiv) = j
                End If
                If currlen + Len(reccontent(j)) < maxlen Then
                    currlen = currlen + Len(reccontent(j))
                    fim(ndiv) = j
                Else
                    If currlen = 0 Then
                        fim(ndiv) = j
                    Else
                        j = j - 1
                        currlen = 0
                    End If
                End If
            Wend
        End If
    End With
    SeparateRecords = ndiv
End Function


Private Function MARKUP_ConvertHTMLFragment2File_GetFrag(content As String, format As String, fieldkey As String, htmlfragpath As String, htmlfragidx As Long, result() As String, Count As Long) As Long
    Dim htmlfragfile As String
    Dim preffix As String
    Dim HTMLFRAGCount As Long
    Dim HTMLFRAGStart As String
    Dim HTMLFRAGEnd As String
    Dim before() As String
    Dim bcount As Long
    Dim after() As String
    Dim acount As Long
    Dim ishtmlfrag As Boolean
    Dim idxhtmlfrag As Long
    Dim aux() As String
    Dim P As Long
    Dim i As Long
    Dim fn As Long
    
    HTMLFRAGCount = GetElemStr(format, ";", aux)
    If HTMLFRAGCount > 0 Then
        HTMLFRAGStart = aux(1)
        HTMLFRAGEnd = aux(2)
    End If
    
    If Len(HTMLFRAGStart) > 0 Then
        P = InStr(1, content, HTMLFRAGStart, vbTextCompare)
        If P > 0 Then
            preffix = Mid(HTMLFRAGStart, 2, 1)
            bcount = MARKUP_LAWPARTIALBODY(Mid(content, 1, P - 1), before, "0", fieldkey)
            content = Mid(content, P)
            ishtmlfrag = True
        End If
    Else
        ishtmlfrag = True
    End If
    If ishtmlfrag Then
        ishtmlfrag = False
        If Len(HTMLFRAGEnd) > 0 Then
            P = InStrRev(content, HTMLFRAGEnd, -1, vbTextCompare)
            If P > 0 Then
                acount = MARKUP_LAWPARTIALBODY(Mid(content, P + Len(HTMLFRAGEnd) + 1), after, "0", fieldkey)
                content = Mid(content, 1, P + Len(HTMLFRAGEnd))
                ishtmlfrag = True
            End If
        Else
            ishtmlfrag = True
        End If
    End If
    
    If ishtmlfrag Then
        If Not DirExist(htmlfragpath) Then
            MakeDir (htmlfragpath)
        End If
        htmlfragfile = LCase(preffix + CStr(htmlfragidx) + ".htmf")
        
        fn = 2
        Open htmlfragpath + "\" + htmlfragfile For Output As fn
        Print #fn, content
        Close fn
    
        Count = bcount + acount + 1
        ReDim result(Count)
        For i = 1 To bcount
            result(i) = before(i)
        Next
        
        idxhtmlfrag = i
        result(i) = htmlfragfile
        For i = i + 1 To Count
            result(i) = after(i - bcount - 1)
        Next
        Erase before
        Erase after
        
    Else
        Count = MARKUP_LAWPARTIALBODY(content, result, "0", fieldkey)
    End If
    MARKUP_ConvertHTMLFragment2File_GetFrag = idxhtmlfrag
End Function


Public Property Get article() As ClsArticle
    Set article = mvarArticle
End Property

Public Property Set article(ByVal vNewValue As ClsArticle)
    Set mvarArticle = article
End Property
Function MARKUP_checkPreviousPIDs() As Boolean
    Dim myMsg As String
    
    Select Case article.IssueNo
    Case "ahead"
        If (Len(article.VersionHistory.RVPDate) > 0) Then
            If (Len(article.VersionHistory.RVP_PID) = 0) Then
                myMsg = Replace(InterfaceLabels("MsgMissingPreviousPID").elem2, "%PARAM_1%", "review")
                Call Msg.GiveRunInformation(myMsg, False, False, True)
            End If
        End If
    Case "review"
    Case Else
        If (Len(article.VersionHistory.AHPDate) > 0) Then
            If (Len(article.VersionHistory.AHP_PID) = 0) Then
                myMsg = Replace(InterfaceLabels("MsgMissingPreviousPID").elem2, "%PARAM_1%", "ahead")
                Call Msg.GiveRunInformation(myMsg, False, False, True)
            End If
        End If
        If (Len(article.VersionHistory.RVPDate) > 0) Then
            If (Len(article.VersionHistory.RVP_PID) = 0) Then
                myMsg = Replace(InterfaceLabels("MsgMissingPreviousPID").elem2, "%PARAM_1%", "review")
                Call Msg.GiveRunInformation(myMsg, False, False, True)
            End If
        End If
    End Select
    MARKUP_checkPreviousPIDs = (Len(myMsg) = 0)
End Function
Sub previousDocVersion_exportData()
    Dim find As Boolean
    Dim ahead As Boolean
    Dim review As Boolean
    
    If previousDocVersion_mustHave(ahead, review) Then
        If ahead Then
            find = (article.VersionHistory.AHP_PID = "")
        End If
        If review And Not find Then
            find = (article.VersionHistory.RVP_PID = "")
        End If
        If find Then
            Set previousDocument = ArticleAction.FindPreviousArticle(article, PreviousIssue)
            If Not (previousDocument Is Nothing) Then
                Call ArticleAction.importPreviousPIDs(article, previousDocument)
            End If
        End If
    End If
End Sub
Function previousDocVersion_hasInDatabase() As Boolean
    Dim r As Boolean
        
    If previousDocVersion_mustHave Then
        Set previousDocument = ArticleAction.FindPreviousArticle(article, PreviousIssue)
        r = Not (previousDocument Is Nothing)
    End If
    previousDocVersion_hasInDatabase = r
End Function
Function previousDocVersion_mustHave(Optional ahead As Boolean, Optional review As Boolean) As Boolean
    Select Case article.IssueNo
    Case "ahead"
        review = (Len(article.VersionHistory.RVPDate) > 0)
    Case "review"
    Case Else
        ahead = (Len(article.VersionHistory.AHPDate) > 0)
        review = (Len(article.VersionHistory.RVPDate) > 0)
    End Select
    previousDocVersion_mustHave = ahead Or review
End Function
Sub previousDocVersion_archive()
    ' archive previous
    If Not (previousDocument Is Nothing) And Not (PreviousIssue Is Nothing) Then
        Set previousDocument = ArticleAction.FindPreviousArticle(article, PreviousIssue)
    End If
    If Not (previousDocument Is Nothing) And Not (PreviousIssue Is Nothing) Then
        If Not previousDocument.IsArchived Then
            Call ArticleAction.init(PreviousIssue)
            Call ArticleAction.archive(previousDocument)
        End If
    End If
End Sub
Function MARKUP_CheckArticleDates(Optional epubdate As String) As Boolean
    Dim r As Boolean
    Dim myMsg As String
    'Dim EPubDate As String
    
    'EPubDate = Date$ ' mm-dd-yyyy
    'EPubDate = Mid(EPubDate, 7, 4) & Mid(EPubDate, 1, 2) & Mid(EPubDate, 4, 2)
    Select Case article.IssueNo
    Case "ahead"
        r = True
        If article.VersionHistory.AHPDate = "" Then
            myMsg = Replace(InterfaceLabels("MsgAHPDateOrRVPdate").elem2, "%PARAM_1%", "ahpdate")
            Call Msg.GiveRunInformation(myMsg, False, False, True)
            r = False
        End If
        r = r And checkDates(article.VersionHistory.RVPDate, article.VersionHistory.AHPDate, "rvpdate", "ahpdate")
        r = r And checkDates(article.VersionHistory.AHPDate, epubdate, "ahpdate", "")
    Case "review"
        r = True
        If article.VersionHistory.RVPDate = "" Then
            myMsg = Replace(InterfaceLabels("MsgAHPDateOrRVPdate").elem2, "%PARAM_1%", "rvpdate")
            Call Msg.GiveRunInformation(myMsg, False, False, True)
            r = False
        End If
        r = r And checkDates(article.VersionHistory.RVPDate, epubdate, "rvpdate", "")
    Case Else
        r = True
        If article.VersionHistory.AHPDate <> "" Then
            r = r And checkDates(article.VersionHistory.RVPDate, article.VersionHistory.AHPDate, "rvpdate", "ahpdate")
        End If
        r = r And checkDates(article.VersionHistory.AHPDate, article.dateiso, "ahpdate", "dateiso")
    End Select
    
    MARKUP_CheckArticleDates = r
End Function
