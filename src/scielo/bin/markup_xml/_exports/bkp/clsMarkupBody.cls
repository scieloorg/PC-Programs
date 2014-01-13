VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "clsMarkupBody"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Private mvarMarkupRange As New clsMarkupRange

Private tableIds As String
Private graphicIds As String


Public IgnSections As Boolean

Property Get MarkupRange() As clsMarkupRange
    Set MarkupRange = mvarMarkupRange
End Property

Property Set MarkupRange(v As clsMarkupRange)
    Set mvarMarkupRange = v
End Property


Function markupBody(range As range, Optional s As Long, Optional e As Long, Optional trac As String) As range
   Dim elementsopen() As String
   Dim elementsClose() As String
   Dim tracing As String
   
    'MsgBox "Analisis"
    'MsgBox getParagraphStyles(range)
    On Error GoTo ERRLOG
    
    tracing = tracing & vbCrLf & " mark_unidentified_blocks_aux 12 a " & CStr(Time)
    s = range.start
    e = range.End
    tracing = tracing & vbCrLf & " mark_unidentified_blocks_aux 12 b " & CStr(Time)
    Call markupParagraphs(s, e)
    tracing = tracing & vbCrLf & " mark_unidentified_blocks_aux 12 c " & CStr(Time)
    
    Call range.SetRange(s, e)
    tracing = tracing & vbCrLf & " mark_unidentified_blocks_aux 12 d " & CStr(Time)
    
    Set range = markupHyperLinks(range)
    tracing = tracing & vbCrLf & " mark_unidentified_blocks_aux 12 e " & CStr(Time)
       
    Call range.SetRange(s, range.End)
    tracing = tracing & vbCrLf & " mark_unidentified_blocks_aux 12 f " & CStr(Time)
    e = range.End
    
    Set markupBody = range
    tracing = tracing & vbCrLf & " mark_unidentified_blocks_aux 12 g " & CStr(Time)
    
    trac = trac & tracing
    Exit Function
ERRLOG:
    MsgBox "markupBody " & err.description
End Function
Function markupHyperLinks(range As range) As range
    Dim i As Long
    Dim q As Long
    
    On Error GoTo ERRLOG
    For i = 1 To range.Hyperlinks.count
        content = Trim(LCase(range.Hyperlinks(i).range.text))
        x = x & vbCrLf & range.Hyperlinks(i).Type & " " & range.Hyperlinks(i).Address & " " & range.Hyperlinks(i).TextToDisplay & " " & range.Hyperlinks(i).SubAddress
        
        
        If range.Hyperlinks(i).Address = "" Then
        
            ' link no proprio documento
            Call markupAsInternalLink(range.Hyperlinks(i), q)
            
        Else
            ' link externo
            Call markupAsExternalLink(range.Hyperlinks(i), q)
        End If
        't = t + q
    Next
    'MsgBox x
    'range.End = range.End + q
    Set markupHyperLinks = range
    Exit Function
ERRLOG:
    MsgBox "markupHyperLinks " & err.description
    
End Function

Sub markupAsInternalLink(hpl As Hyperlink, ByRef qCharsInserted As Long)
    Dim content As String, reftype As String, TAG As String, attributes As String
    Dim rid As String
    

    On Error GoTo ERRLOG
    qCharsInserted = 0
    TAG = "xref"
    content = Trim(LCase(hpl.range.text))
    If Len(Trim(content)) > 0 Then
        If InStr(content, "fig") > 0 Or (InStr(content, "gr") > 0 And InStr(content, "ic") > 0) Then
            reftype = "fig"
            'hasGraphics = hasGraphics + 1
        ElseIf InStr(content, "tab") > 0 Then
            reftype = "table"
            'hasTables = hasTables + 1
        Else
            If content Like myReplace(space(Len(content)), " ", "#") Then
                reftype = "bibr"
            Else
                reftype = ""
            End If
        End If
        
        
        If InStr(content, " ") > 0 Then
            rid = Mid(content, InStr(content, " ") + 1)
        Else
            rid = hpl.SubAddress
            'hpl.range.text = hpl.SubAddress
        End If
        If Len(reftype) > 0 Then
            attributes = "ref-type=" & Chr(34) & reftype & Chr(34)
        End If
        If Len(Trim(rid)) > 0 Then
            If Len(attributes) > 0 Then attributes = attributes & " "
            If Len(reftype) > 0 Then
                rid = LCase(Mid(reftype, 1, 1)) & replace(space(Len(rid) - 2), " ", "0") & Trim(rid)
            End If
            attributes = attributes & "rid=" & Chr(34) & rid & Chr(34)
        End If
        If MarkupRange.CheckInsertTag(hpl.range, TAG) Then
            Call MarkupRange.InsertTag(True, hpl.range, TAG, MKP_COLOR_XREF, attributes)
            qCharsInserted = hpl.range.Characters.count - Len(content)
        End If
    End If
    Exit Sub
ERRLOG:
    MsgBox "markupAsInternalLink " & err.description
End Sub
Sub markupAsExternalLink(hpl As Hyperlink, ByRef qCharsInserted As Long)
    Dim TAG As String, attributes As String
    On Error GoTo ERRLOG
    TAG = "uri"
    attributes = "href=" & Chr(34) & hpl.Address & Chr(34)
    qCharsInserted = 0
    content = Trim(LCase(hpl.range.text))
    If MarkupRange.CheckInsertTag(hpl.range, TAG) Then
        Call MarkupRange.InsertTag(True, hpl.range, TAG, MKP_COLOR_URL, attributes)
        qCharsInserted = hpl.range.Characters.count - Len(content)
    End If
    Exit Sub
ERRLOG:
    MsgBox "markupAsExternalLink " & err.description
    
End Sub

Function markupGraphics(range As range) As range
    Dim i As Long, content As String, reftype As String, TAG As String, attributes As String
    
    Dim rid As String
    Dim v As String
    Dim scrollPercent As Long
    Dim item As InlineShape
    Dim s As Long
    Dim e As Long
    
    On Error GoTo ERRLOG
    
    'scrollPercent = ActiveWindow.VerticalPercentScrolled
    
    'MsgBox range.InlineShapes.count
    
    TAG = "graphic"
    
    For Each item In range.InlineShapes
        'range.InlineShapes(item.index)
        'attributes = " xlink:href=" & Chr(34) & range.InlineShapes(i).Hyperlink & Chr(34)
        
'MsgBox " 1 " & Application.ScreenUpdating
        v = ""
        Select Case item.Type
        Case wdInlineShapeLinkedPicture
            v = item.LinkFormat.SourceFullName
        Case wdInlineShapePicture
            v = item.LinkFormat.SourceFullName
        End Select
        
        If item.LinkFormat Is Nothing Then
        Else
            If Len(v) > 0 Then
                attributes = "href=" & Chr(34) & v & Chr(34)
            End If
'MsgBox " 2 " & Application.ScreenUpdating
            s = item.range.start
            e = item.range.End
            
            Call InsertTag(s, e, TAG, MKP_COLOR_GRAPHIC, attributes)
            
            Call item.range.SetRange(s, e)
'MsgBox " 3 " & Application.ScreenUpdating
            
        End If
    Next item
   
    Set markupGraphics = range
    'ActiveWindow.VerticalPercentScrolled = scrollPercent
    Exit Function
ERRLOG:
    MsgBox "clsMarkupBody.markupGraphics " & err.description
    
End Function
Function markupGraphicAndTablesInElements(range As range, elementsopen() As String, elementsClose() As String, typeElem As String) As range
    
    Dim pos2 As Long
    Dim o_start As Long
    Dim o_end As Long
    Dim continua As Boolean
    Dim currentEnd As Long
    
    Dim pOpenTag As Long
    Dim pCloseTag As Long
    Dim i As Long
    Dim r As range
    
    On Error GoTo ERRLOG
    
    o_start = range.start
    o_end = range.End
    currentEnd = range.End
    
    For i = 0 To UBound(elementsopen) - 1
        Selection.start = range.start
        Selection.End = range.End
        
'MsgBox "markupGraphicAndTablesInElements " & vbCrLf & " range=" & range.text & vbCrLf & " selection=" & selection.text & vbCrLf & " procurar " & elementsopen(i)
        continua = True
        'final = selection.start
        While continua
            Selection.End = currentEnd
            
'If MsgBox("markupGraphicAndTablesInElements find " & elementsopen(i) & " em selection=" & selection.text, vbYesNo) = vbNo Then End
        
            If findText(elementsopen(i), True, pOpenTag, pos2) Then
                'MsgBox "found: elementsopen(i)=" & selection.text
                If pOpenTag > o_start And pOpenTag < currentEnd Then
                    
                    
                    Selection.start = pOpenTag - 1
                    Selection.End = currentEnd
                                        
                    'MsgBox "finding... " & elementsClose(i) & " em " & selection.text
                    If findText(elementsClose(i), True, pos2, pCloseTag) Then
                    'MsgBox "found: " & selection.text
                        
                        Selection.start = pOpenTag
                        Selection.End = pCloseTag + 1
                        currentEnd = pos2
                        
                    'MsgBox "finding [" & typeElem & " em " & selection.text
                        If InStr(Selection.text, "[" & typeElem) = 0 Then
                            Set r = Selection.range
                            
                            'MsgBox "posicao inicial " & CStr(r.start) & "," & CStr(r.End)
                            If typeElem = "table" Then
                                Set r = markupTables(r)
                            Else
                                Set r = markupGraphics(r)
                            End If
                            'MsgBox "posicao final range " & CStr(r.start) & "," & CStr(r.End) & vbCrLf & r.text
                            'MsgBox "posicao final selection " & CStr(selection.start) & "," & CStr(selection.End) & vbCrLf & selection.text
                            
                             
                            Selection.start = r.End
                            currentEnd = r.End
                            range.End = r.End
                        Else
                            Selection.start = currentEnd
                        End If
                    Else
                        Selection.start = currentEnd
                    End If
                Else
                    continua = False
                    Selection.start = Selection.End
                End If
            Else
                    continua = False
                    Selection.start = Selection.End
                
            End If
       Wend
    Next
    
    '?selection.End = selection.End + 1
    '?selection.start = selection.End
    
    'MsgBox "range inicial " & CStr(o_start) & "," & CStr(o_end) & vbCrLf & ActiveDocument.range(o_start, o_end).text
    'MsgBox "range final " & CStr(range.start) & "," & CStr(range.End) & vbCrLf & r.text
                            
    
    'MarkupRange.xdebug = False
    Set markupGraphicAndTablesInElements = range
     'ActiveWindow.VerticalPercentScrolled = scrollPercent
    Exit Function
ERRLOG:
    MsgBox "markupGraphicAndTablesInElements " & err.description
    
    
End Function

Public Function findText(ByVal t As String, f As Boolean, Optional sPos As Long, Optional fPos As Long) As Boolean
  Const errIDMet As String = "20"
  '-----------------------------
  On Error GoTo ERRLOG
  
  findText = False
  'MsgBox "findText " & t & ": " & selection.start & "," & selection.End
  sPos = 0
  fPos = 0
  
  
  With Selection.find
    .text = t: .Replacement.text = "":  .forward = f
    .Wrap = wdFindStop: .format = False: .MatchCase = False
    .MatchWholeWord = False: .MatchWildcards = False
    .MatchSoundsLike = False: .MatchAllWordForms = False
  End With
  Selection.find.Execute
  If Selection.find.found = True Then
    With Selection
      sPos = .start + 1: fPos = .End - 1
    End With
    findText = True
  End If
  
  'MsgBox "findText result " & t & ": " & selection.start & "," & selection.End
  
  Exit Function
ERRLOG:
MsgBox "findText " & t & " " & err.description & tracing
  Dim conf As New clsConfig
  With mErr
    conf.LoadPublicValues
    .LoadErr conf
    .BuildLog errIDObj & errIDMet, conf
  End With
  Set conf = Nothing
End Function


Function markupTables(range As range) As range
    Dim i As Long, content As String, reftype As String, TAG As String, attributes As String
    
    Dim rid As String
    Dim RowIdx As Long
    Dim CelIdx As Long
    Dim scrollPercent As Long
    On Error GoTo ERRLOG
    
    'ActiveWindow.VerticalPercentScrolled
    
    TAG = "table"
    'MarkupRange.xdebug = True
    
    For i = 1 To range.tables.count
        For RowIdx = 1 To range.tables(i).Rows.count
            For CelIdx = 1 To range.tables(i).Rows(RowIdx).Cells.count
            
                Call MarkupRange.InsertTag(False, range.tables(i).Rows(RowIdx).Cells(CelIdx).range, "td", MKP_COLOR_TABLE_TD, "")
            Next
            Call MarkupRange.InsertTag(False, range.tables(i).Rows(RowIdx).range, "tr", MKP_COLOR_TABLE_TR, "")
        Next
        Call MarkupRange.InsertTag(False, range.tables(i).range, TAG, MKP_COLOR_TABLE, attributes)
        'Call MarkupRange.InsertTag(range.tables(i).range, "p", 14, attributes)
        'range.End = range.tables(i).range.End
    Next
    
    'MarkupRange.xdebug = False
    Set markupTables = range
     'ActiveWindow.VerticalPercentScrolled = scrollPercent
    Exit Function
ERRLOG:
    MsgBox "markupTables " & err.description
    
    
End Function
Function getParagraphStyles(selectedRange As range) As String
    Dim i As Long
    Dim styles As String
    Dim x As String
    
    On Error GoTo ERRLOG
    For i = 1 To selectedRange.Paragraphs.count
        x = selectedRange.Paragraphs(i).format.STYLE & selectedRange.Paragraphs(i).range.Font.name & selectedRange.Paragraphs(i).range.Font.Size & selectedRange.Paragraphs(i).range.Font.bold
        If InStr(" " & styles, x) = 0 Then
            styles = styles & vbCrLf & x
        End If
    
    Next
    getParagraphStyles = styles
    Exit Function
ERRLOG:
    MsgBox "getParagraphStyles " & err.description
    
    
End Function

Sub markupParagraphs(range_start As Long, RANGE_END As Long)
    Dim selectedRange As range
    Dim i As Long
    Dim isSection As Boolean
    Dim former_start As Long
    Dim former_end As Long
    Dim selectedRange_start As Long
    Dim selectedRange_end As Long
    Dim s As Long
    Dim e As Long
    
    Dim total As Long
    
    Dim secid As String
    Dim sectag As String
    Dim openSection As Boolean
    Dim openSubSection As Boolean
    Dim insertedText As String
    Dim attributes As String
    Dim BeforeTextLen As Long
    Dim AfterTextLen As Long
        
    Dim prange As range
        
    Dim scrollPercent As Long
    Dim tracing As String
    
    On Error GoTo ERRLOG
    
    'ActiveWindow.VerticalPercentScrolled
    former_start = range_start
    former_end = RANGE_END
    
    Set selectedRange = ActiveDocument.range(range_start, RANGE_END)
    tracing = tracing & vbCrLf & " ActiveDocument.range(" & CStr(range_start) & ", " & CStr(RANGE_END) & ") " & vbCrLf & selectedRange.text
    total = selectedRange.Paragraphs.count
    
    tracing = tracing & vbCrLf & " Procurar ] "
    
    ' dentro primeiro paragrafo procura por ], para tras
    Selection.start = range_start
    Selection.End = RANGE_END
    
    tracing = tracing & vbCrLf & " Procurar ] 1 " & CStr(former_start) & "," & CStr(former_end) & "; " & CStr(range_start) & "," & CStr(RANGE_END) & "; " & CStr(selectedRange.start) & "," & CStr(selectedRange.End) & "; " & CStr(Selection.start) & "," & CStr(Selection.End)
    
    With Selection.find
        .text = "]": .Replacement.text = "":  .forward = False
        .Wrap = wdFindStop: .format = False: .MatchCase = False
        .MatchWholeWord = False: .MatchWildcards = False
        .MatchSoundsLike = False: .MatchAllWordForms = False
    End With
    Selection.find.Execute
    If Selection.find.found = True Then
    tracing = tracing & vbCrLf & " Procurar ] 1.1 " & CStr(Selection.start) & "," & CStr(Selection.End) & " " & Selection.text
    
        If Selection.start >= range_start Then
            range_start = Selection.start + 1
            'MsgBox "ranger after finding ] : " & CStr(range_start) & "," & CStr(range_end)
            Set selectedRange = ActiveDocument.range(range_start, RANGE_END)
            total = selectedRange.Paragraphs.count
            tracing = tracing & vbCrLf & "  found.range(" & CStr(range_start) & ", " & CStr(RANGE_END) & ") "
tracing = tracing & vbCrLf & " Procurar ] 2 " & CStr(former_start) & "," & CStr(former_end) & "; " & CStr(range_start) & "," & CStr(RANGE_END) & "; " & CStr(selectedRange.start) & "," & CStr(selectedRange.End) & "; " & CStr(Selection.start) & "," & CStr(Selection.End)
                
        End If
    End If
    
    tracing = tracing & vbCrLf & " Procurar ] 3 " & CStr(former_start) & "," & CStr(former_end) & "; " & CStr(range_start) & "," & CStr(RANGE_END) & "; " & CStr(selectedRange.start) & "," & CStr(selectedRange.End) & "; " & CStr(Selection.start) & "," & CStr(Selection.End)
    
    
    
    
    tracing = tracing & vbCrLf & " Paragrafos "
    
    For i = 1 To total
        With selectedRange.Paragraphs(i)
            Set prange = .range
            insertedText = ""
            If i = 1 Then
                prange.start = range_start
            End If
            If i = total Then
                tracing = tracing & vbCrLf & " Procurar [ "
                tracing = tracing & vbCrLf & "  found.range(" & CStr(prange.start) & ", " & CStr(prange.End) & ") "
                tracing = tracing & vbCrLf & " Procurar [ 1"
                Selection.start = prange.start
                tracing = tracing & vbCrLf & " Procurar [ 2"
                Selection.End = prange.End
                tracing = tracing & vbCrLf & " Procurar [ 3"
                With Selection.find
                    .text = "[": .Replacement.text = "": .forward = True
                    .Wrap = wdFindStop: .format = False: .MatchCase = False
                    .MatchWholeWord = False: .MatchWildcards = False
                    .MatchSoundsLike = False: .MatchAllWordForms = False
                End With
                Selection.find.Execute
                tracing = tracing & vbCrLf & " Procurar [ 4"
                If Selection.find.found = True Then
                tracing = tracing & vbCrLf & " Procurar [ 5 " & CStr(former_start) & "," & CStr(former_end) & "; " & CStr(range_start) & "," & CStr(RANGE_END) & "; " & CStr(prange.start) & "," & CStr(prange.End) & "; " & CStr(Selection.start) & "," & CStr(Selection.End)
                
                    If (Selection.start >= prange.start) And (Selection.start <= prange.End) Then
                tracing = tracing & vbCrLf & " Procurar [ 6"
                        
                        prange.End = Selection.start - 1
                tracing = tracing & vbCrLf & " Procurar [ 7 " & CStr(former_start) & "," & CStr(former_end) & "; " & CStr(range_start) & "," & CStr(RANGE_END) & "; " & CStr(prange.start) & "," & CStr(prange.End) & "; " & CStr(Selection.start) & "," & CStr(Selection.End)
                        Set selectedRange = ActiveDocument.range(range_start, RANGE_END)
                tracing = tracing & vbCrLf & " Procurar [ 8"
                        
                    End If
                End If
                tracing = tracing & vbCrLf & "ranger after finding [ : " & CStr(prange.start) & "," & CStr(prange.End)
            End If
            tracing = tracing & vbCrLf & " Section "
    
            isSection = isSectionTitle(selectedRange.Paragraphs(i))
            If isSection Then
                secid = getSectionId(prange.text)
                If openSubSection Then
                    ' Insere o fim de uma subsection
                    insertedText = insertedText & MarkupRange.BuildFinishTag("subsec")
                    openSubSection = False
                End If
                If openSection And secid <> "" Then
                    ' Insere o fim de uma section
                    insertedText = insertedText & MarkupRange.BuildFinishTag("sec")
                    openSection = False
                End If
                ' Obtem os atributos da nova secao
                If openSection Then
                    attributes = ""
                    openSubSection = True
                    sectag = "subsec"
                Else
                    openSection = True
                    sectag = "sec"
                    If secid <> "" Then
                        attributes = "sec-type=" & Chr(34) & secid & Chr(34)
                    End If
                End If
                ' Insere o início da tag sec, com ou sem atributos
                insertedText = insertedText & MarkupRange.BuildStartTag(sectag, attributes)
                ' Insere o início da tag title
                insertedText = insertedText & MarkupRange.BuildStartTag("sectitle", "")
                BeforeTextLen = Len(insertedText)
                prange.InsertBefore (insertedText)
                ' Insere o fim da tag title
                insertedText = MarkupRange.BuildFinishTag("sectitle")
                AfterTextLen = Len(insertedText)
                Selection.start = prange.start
                Selection.End = prange.End - 1
                Selection.InsertAfter (insertedText)
                
                'ANTES
                Selection.start = prange.start - 1
                Selection.End = prange.start + BeforeTextLen
                Call MarkupRange.FormatText(Selection.range, MKP_COLOR_SECTITLE)
                
                ' DEPOIS
                Selection.start = prange.End - AfterTextLen - 1
                Selection.End = prange.End
                Call MarkupRange.FormatText(Selection.range, MKP_COLOR_SECTITLE)
            Else
            
            'MsgBox "Paragrafo antes de marcar : " & CStr(pRange.start) & "," & CStr(pRange.End)
tracing = tracing & vbCrLf & " Paragrafo "
    
                If xdebug Then If MsgBox("isP " & prange.text, vbYesNo) = vbNo Then End
                
                s = prange.start
                e = prange.End
                Call InsertTag(s, e, "p", MKP_COLOR_LI_OR_P, "")
                Call prange.SetRange(s, e)
            End If

    End With
    Next
    insertedText = ""
    If openSubSection Then
    tracing = tracing & vbCrLf & " fecha subsec "

        insertedText = insertedText & MarkupRange.BuildFinishTag("subsec")
    End If
    If openSection Then
    tracing = tracing & vbCrLf & " fecha sec "
    insertedText = insertedText & MarkupRange.BuildFinishTag("sec")
    End If
    If Len(insertedText) > 0 Then
        Call prange.SetRange(prange.End, prange.End)
        prange.InsertAfter (insertedText)
        MarkupRange.FormatText prange, MKP_COLOR_CLOSE_SEC
        
    End If
    
    'Call selectedRange.SetRange(start, pRange.End)
    RANGE_END = prange.End
    'MsgBox tracing
    'ActiveWindow.VerticalPercentScrolled = scrollPercent
    Exit Sub
    
    
ERRLOG:
MsgBox "markupParagraphs " & err.description & tracing

End Sub


Private Function isSectionTitle(paragraphRange As Paragraph) As Boolean
    Dim r As Boolean
    Dim fontSize As Long
    
    On Error GoTo ERRLOG
    If IgnSections Then

    Else
    
        ask = "É seção ou subseção?"
        
        If paragraphRange.range.Font.bold Or (paragraphRange.range.Font.bold And paragraphRange.range.Font.name = "Verdana, Arial") Then
            If paragraphRange.range.tables.count = 0 Then
                If MsgBox(paragraphRange.range.text & vbCrLf & ask, vbYesNo) = vbYes Then
                    r = True
                    If fontSize = 0 Then
                        fontSize = paragraphRange.range.Font.Size
                    End If
                End If
            End If
        End If
    End If
    isSectionTitle = r
    Exit Function
ERRLOG:
    MsgBox "isSectionTitle " & err.description
    
    
End Function
Private Sub show(range As range, ByVal start As Long, ByVal endx As Long, label As String)
    Dim s As Long, e As Long
    
    s = range.start
    e = range.End
    
    range.start = start
    range.End = endx
    
    'MsgBox label & vbCrLf & range.text
    
    range.start = s
    range.End = e
End Sub
Private Function getSectionId(section As String) As String
    Dim r As String
    Dim test(22) As String
    
    test(1) = "introdu|intro"
    test(2) = "result|results"
    test(3) = "subjects|subjects"
    test(4) = "conclus|conclusions"
    test(5) = "discus|discussion"
    test(6) = "materia|materials"
    test(7) = "method|methods"
    test(8) = "métodos|methods"
    test(9) = "metodo|methods"
    test(10) = "proced|methods"
    test(11) = "pacient|subjects"
    test(12) = "partici|subjects"
    test(13) = "comment|conclusions"
    test(14) = "coment|conclusions"
    test(15) = "interpret|discussion"
    test(16) = "case|cases"
    test(17) = "caso|cases"
    test(18) = "suppl|supplementary-material"
    test(19) = "supl|supplementary-material"
    test(20) = "patient|subjects"
    test(21) = "synopsis|intro"
    test(22) = "sinop|intro"
    
    On Error GoTo ERRLOG
    section = myReplace(Trim(section), Chr(160), "")
    
    i = 1
    counter = 22
    r = ""
    While (r <> "") And (i <= counter)
        pair = Split(test(i), "|")
        MsgBox pair(0) & " " & pair(1)
        If InStr(1, " " & section, pair(0), vbTextCompare) > 0 Then
            r = pair(1)
        End If
        i = i + 1
    Wend
    'MsgBox "[" & section & "]" & r
    getSectionId = r
    Exit Function
ERRLOG:
    MsgBox "getSectionId " & err.description
    
End Function



Private Function formattag(ByVal TAG As String, Document As range) As String
   Document.text = TAG
  Call MarkupRange.FormatText(Document, 3)
formattag = Document.text

End Function

Sub analyzeText(selectedRange As range)
    
End Sub

Function markupTableOrGraphic(r As range, Optional element As String) As range
   Dim elementsopen() As String
   Dim elementsClose() As String
   Dim s As Long
   
   On Error GoTo WARN
   s = r.start
   If Len(element) > 0 Then
        ReDim elementsopen(1)
        ReDim elementsClose(1)
        elementsopen(0) = "[" & element & " "
        elementsClose(0) = "[/" & element & "]"
   Else
        ReDim elementsopen(3)
        ReDim elementsClose(3)
        elementsopen(0) = "[figgrp "
        elementsopen(1) = "[tabwrap "
        elementsopen(2) = "[equation "
        elementsClose(0) = "[/figgrp]"
        elementsClose(1) = "[/tabwrap]"
        elementsClose(2) = "[/equation]"
    End If
    Set r = markupGraphicAndTablesInElements(r, elementsopen, elementsClose, "graphic")
'MsgBox "TRACING 4 " & Application.ScreenUpdating

    'ReDim elementsopen(1)
    'ReDim elementsClose(1)
    'elementsopen(0) = "[tabwrap "
    'elementsClose(0) = "[/tabwrap]"
    'Set r = markupGraphicAndTablesInElements(r, elementsopen, elementsClose, "table")
    
    'r.End = s
    Set markupTableOrGraphic = r
    Exit Function
WARN:

MsgBox "markupTableOrGraphic " & err.description
    

End Function

Public Function InsertTag(selStart As Long, selEnd As Long, TAG As String, colorI As WdColor, attributes As String, Optional attl As clsAttrList, Optional linkl As clsLkList, Optional inter As clsInterface, Optional button As clsButton) As Boolean
  Dim sTag As String, fTag As String
  Dim s As Long, e As Long
  Dim findStart As Long, findEnd As Long
  Dim blankAfterCloseBracket As Boolean
  Dim i  As Long
  Dim p  As Long
  Dim tracing As String
  Dim newDocStart As Long
  Dim x As String
  Dim marcar As range
  
  Const errIDMet As String = "01"
  
  '-----------------------------
  On Error GoTo ERRLOG
  
    
    Set marcar = ActiveDocument.range(selStart, selEnd)
    If selEnd - selStart > 1 Then
        tracing = "(" & CStr(selStart) & "," & CStr(selEnd) & ") "
        If selStart - 500 > 0 Then
            tracing = tracing & ActiveDocument.range(selStart - 500, selStart - 1).text
        Else
            tracing = tracing & ActiveDocument.range(ActiveDocument.range.start, selStart - 1).text
        End If
        tracing = tracing & " >>>> " & ActiveDocument.range(selStart, selEnd).text & " <<<< "
        If ActiveDocument.range.End > selEnd + 500 Then
            tracing = tracing & ActiveDocument.range(selEnd + 1, selEnd + 500).text
        Else
            tracing = tracing & ActiveDocument.range(selEnd + 1, ActiveDocument.range.End).text
        End If
        
        test = marcar.text
        test = replace(test, Chr(32), "", , , vbTextCompare)
        test = replace(test, Chr(13), "", , , vbTextCompare)
        test = replace(test, Chr(10), "", , , vbTextCompare)
        blankAfterCloseBracket = (Len(test) = 0)
        
        If blankAfterCloseBracket Then
            
        Else
            If Len(attributes) > 0 Then
                attributes = " " & attributes
            End If
            sTag = "[" & TAG & attributes & "]"
            fTag = "[/" & TAG & "]"
            tracing = tracing & vbCrLf & " passo 1"
            
            If TAG = "p" Then
                If selEnd - 1 > selStart Then
                    selEnd = selEnd - 1
                End If
                Set marcar = ActiveDocument.range(selStart, selEnd)
                tracing = tracing & vbCrLf & " passo 1.1"
            End If
            If TAG = "graphic" Then
                sTag = " " & sTag
                fTag = fTag & " "
            End If
            tracing = tracing & vbCrLf & " passo 2"
            
              marcar.InsertBefore sTag
            tracing = tracing & vbCrLf & " passo 3"
              
              marcar.InsertAfter fTag
              
              s = marcar.start
              e = marcar.End
            tracing = tracing & vbCrLf & " passo 4"
            
              Call marcar.SetRange(s, s + Len(sTag))
        tracing = tracing & vbCrLf & " passo 5"
                      
              FormatText marcar, colorI
    tracing = tracing & vbCrLf & " passo 6"
                      
              Call marcar.SetRange(e - Len(fTag), e)
              tracing = tracing & vbCrLf & " passo 7"
            
              FormatText marcar, colorI
              tracing = tracing & vbCrLf & " passo 8"
            
              Call marcar.SetRange(s, e)
    tracing = tracing & vbCrLf & " passo 9"
                      
        End If
    End If
    
    selStart = marcar.start
    selEnd = marcar.End
    
  Exit Function
ERRLOG:

MsgBox "MarkupBody.InsertTag " & TAG & " " & err.description & " " & tracing

End Function

Public Sub FormatText(txt As range, color As WdColor)
  
  '-----------------------------
  On Error GoTo ERRLOG

  With txt.Font
  
    .AllCaps = False
    .Animation = wdAnimationNone
    .bold = False
    .color = color
    .DoubleStrikeThrough = False
    .Emboss = False
    .Engrave = False
    .Hidden = False
    .Italic = False
    .name = "Verdana"
    .Outline = False
    .Shadow = False
    .Size = 9
    .SmallCaps = False
    .StrikeThrough = False
    .Subscript = False
    .Superscript = False
    .Underline = wdUnderlineNone
  End With
  Exit Sub
ERRLOG:
 MsgBox "MarkupBody.Formattext " & err.description
  
End Sub
