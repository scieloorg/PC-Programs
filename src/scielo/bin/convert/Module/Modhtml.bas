Attribute VB_Name = "ModHTML"
Option Explicit

Public Const TAG_FINAL = 2
Public Const TAG_INICIAL = 1
Public Const TAG_NENHUMA = 0

'Private ValidTagTable As ClTable

Private ValidHTMLTagTable As MyCollection
Public ASCIIList As ClSortList

Public CvtTables As Collection 'ColCvtTab
Public CvtTabLanguage As Collection 'ColCvtTab

'-----------------------------------------------------------------------
'LoadHTML2ASCIIList - lê tabela de correspondência tags HTML para tags ASCII
'Path       - caminho do arquivo
'File       - nome do arquivo
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Function LoadHTML2ASCIIList() As Boolean
    Dim ret As Boolean
    Dim Linha As String
    Dim QtdLinhas As Long
    Dim fn As Long
    
    With ConvertDirTree.DirNodes("Conversion List of HTML to ASCII")
    If FileExist(.Parent.fullpath, .text, .key) Then
        fn = FreeFile(1)
        Set ASCIIList = New ClSortList
        
        Open .fullpath For Input As fn
        While Not EOF(fn)
            Line Input #fn, Linha
            QtdLinhas = QtdLinhas + 1
            ASCIIList.Insert (Linha)
        Wend
        Close fn
        ret = (ASCIIList.counter = QtdLinhas)
    End If
    End With
    LoadHTML2ASCIIList = ret
End Function


'-----------------------------------------------------------------------
'LoadHTMLTagsTable - lê tabela de tags HTML relevantes
'Path       - caminho do arquivo
'File       - nome do arquivo
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Function LoadHTMLTagsTable() As Boolean
    Dim fn As Long
    Dim StartTag As String
    Dim EndTag   As String
    Dim alwayspresent As String
    Dim Item As ClValidTag
    Dim Count As Long
    
    With ConvertDirTree.DirNodes("Valid HTML Tags Table")
    
        Set ValidHTMLTagTable = New MyCollection
        
        ValidHTMLTagTable.isobj = True
        
        fn = FreeFile
        Open .Parent.fullpath + PathSep + .text For Input As fn
        While Not EOF(fn)
            Input #fn, StartTag, EndTag, alwayspresent
            Count = Count + 1
            Set Item = New ClValidTag
            Item.StartTag = StartTag
            Item.EndTag = EndTag
            Item.alwayspresent = alwayspresent
            
            Call ValidHTMLTagTable.Add(Item, StartTag)
        Wend
        Close fn
        
    End With
    Set Item = Nothing
    LoadHTMLTagsTable = (Count = ValidHTMLTagTable.Count)
End Function

'-----------------------------------------------------------------------
'RmAllHTML - remove todas as tags HTML existentes na string
's           - string
'Retorno     - string sem tags HTML
'-----------------------------------------------------------------------
Function RmAllHTML(s As String, Optional c As String = " ") As String
    Dim original As String
    Dim p1 As Long
    Dim p2 As Long
    Dim P3 As Long
    Dim nova As String

    original = s
    While Len(original) > 0
        p1 = InStr(original, "<")
        p2 = InStr(original, ">")
        If (p1 = 0) Or (p2 = 0) Then
            nova = Trim(nova) + c + Trim(original)
            original = ""
        ElseIf p1 < p2 Then
            P3 = InStr(p1 + 1, original, "<", vbBinaryCompare)
            While (P3 > 0) And (P3 < p2)
                p1 = P3
                P3 = InStr(p1 + 1, original, "<", vbBinaryCompare)
            Wend
            
            nova = Trim(nova) + c + Trim(Mid(original, 1, p1 - 1))
            original = Trim(Mid(original, p2 + 1))
        Else
            nova = nova + Mid(original, 1, p2)
            original = Mid(original, p2 + 1)
        End If
    Wend
    RmAllHTML = Trim(nova)
End Function

'-----------------------------------------------------------------------
'RmAllHTML - remove todas as tags HTML existentes na string
's           - string
'Retorno     - string sem tags HTML
'-----------------------------------------------------------------------
Function RmAllHTML2(s As String) As String
    Dim original As String
    Dim p1 As Long
    Dim p2 As Long
    Dim P3 As Long
    Dim nova As String

    original = s
    While Len(original) > 0
        p1 = InStr(original, "<")
        p2 = InStr(original, ">")
        If (p1 = 0) Or (p2 = 0) Then
            nova = nova + original
            original = ""
        ElseIf p1 < p2 Then
            P3 = InStr(p1 + 1, original, "<", vbBinaryCompare)
            While (P3 > 0) And (P3 < p2)
                p1 = P3
                P3 = InStr(p1 + 1, original, "<", vbBinaryCompare)
            Wend
            
            nova = nova + Mid(original, 1, p1 - 1)
            original = Mid(original, p2 + 1)
        Else
            nova = nova + Mid(original, 1, p2)
            original = Mid(original, p2 + 1)
        End If
    Wend
    RmAllHTML2 = nova
End Function
'-----------------------------------------------------------------------
'RmPartialHTML - remove as tags HTML irrelevantes existentes na string
's              - string
'RmTodas        - se verdadeiro, remove as tags HTML cuja validade=0, além daquelas que não existem na tabela
'Retorno        - string sem tags HTML irrelevantes
'-----------------------------------------------------------------------
Function RmPartialHTML(s As String, KeepAll As Boolean) As String
    Dim original  As String
    Dim tmp     As String
    Dim nova    As String
    Dim p1      As Long
    Dim p2      As Long
    Dim P3      As Long
    Dim P4      As Long
    Dim Tag     As String
    Dim lista   As ClLista
    Dim apagar  As Boolean
    Dim EndTag As String
    Dim found As Boolean
    
    
    Set lista = New ClLista
    
    original = Trim(s)
    
    'while (InStr(original, "</") = 1)
    '    P1 = InStr(original, ">")
    '    original = Trim(Mid(original, P1 + 1))
    'Wend
    
    'P1 = Len(original) - 1
    'found = False
    'while (Len(original) > 0) And (Not found)
    '    If (Mid(original, Len(original)) = ">") Then
            'while (StrComp(Mid(original, P1, 1), "<") <> 0)
            '    P1 = P1 - 1
            'Wend
    '        P4 = InStr(1, original, "<")
    '        while (P4 > 0)
    '            P1 = P4
    '            P4 = InStr(P1 + 1, original, "<")
    '        Wend
    '        If (InStr(Mid(original, P1), "</") = 0) Then
    '            original = Trim(Mid(original, 1, P1 - 1))
    '        Else
    '            found = True
    '        End If
    '    Else
    '        found = True
    '    End If
    'Wend
    
    While Len(original) > 0
        p1 = InStr(original, "<")
        p2 = InStr(original, ">")
        
        If (p1 = 0) Or (p2 = 0) Then
            nova = nova + original
            original = ""
        ElseIf p1 < p2 Then
            apagar = False
            P3 = InStr(p1 + 1, original, "<", vbBinaryCompare)
            While (P3 > 0) And (P3 < p2)
                p1 = P3
                P3 = InStr(p1 + 1, original, "<", vbBinaryCompare)
            Wend
            Tag = Mid(original, p1, p2 - p1 + 1)
            If InStr(Tag, "</") > 0 Then
                If lista.RemoveElem(Tag) Then
                    'atual = TAG_FINAL
                Else
                    apagar = True
                End If
            Else
                If IsValid(Tag, KeepAll, EndTag) Then
                    If Len(EndTag) > 0 Then
                        lista.Insere (EndTag)
                        'atual = TAG_INICIAL
                    'Else
                        'atual = TAG_FINAL
                    End If
                Else
                    apagar = True
                End If
            End If
            
            'tmp = Trim(Mid(original, 1, P1 - 1))
            If apagar Then
                'atual = TAG_NENHUMA
                nova = nova + Mid(original, 1, p1 - 1)
            Else
                'tmp = tmp + tag
                'tag deve continuar para padronizar font face symbol
                nova = nova + Mid(original, 1, p1 - 1) + Tag
            End If
                       
            original = Mid(original, p2 + 1)
        ElseIf p1 > p2 Then
            nova = nova + Mid(original, 1, p2)
            original = Mid(original, p2 + 1)
        End If
    Wend
    
       
    While lista.RemoveLast(Tag)
        nova = nova + Tag
    Wend
    Set lista = Nothing
    
    RmPartialHTML = Trim(ReplaceString(nova, Chr(32) + Chr(32), Chr(32), vbTextCompare))
End Function

'-----------------------------------------------------------------------
'IsValid    - Verifica a importância da tag HTML
'Tag        - string
'BastaExistir   - se para que a tag seja válida basta estar na tabela ou
'               ter importância 1.
'Idx        - posição da tag na tabela
'Retorno    - verdadeiro ou falso
'-----------------------------------------------------------------------
Private Function IsValid(Tag As String, KeepAll As Boolean, EndTag As String) As Boolean
    Dim Item As ClValidTag
    Dim exist As Boolean
    Dim ret As Boolean
    Dim i As Long
    
    
    With ValidHTMLTagTable
    Set Item = New ClValidTag
    Set Item = .Item(Tag, exist)
    i = 0
    While (i < .Count) And (Not exist)
        i = i + 1
        If LCase(Tag) Like LCase(.Item(i).StartTag) Then
            exist = True
            Set Item = .Item(i)
        End If
    Wend
    
    If exist Then
        EndTag = Item.EndTag
        If (InStr(1, Item.StartTag, "FACE=" + Chr(34) + "Symbol" + Chr(34), vbTextCompare) > 0) Then
            Tag = "<FONT FACE=" + Chr(34) + "Symbol" + Chr(34) + ">"
        End If
        If KeepAll Then
            ret = True
        Else
            'If item.alwayspresent = "1" Then
            ret = (Item.alwayspresent = "1")
        End If
    End If
    
    End With
    Set Item = Nothing
    IsValid = ret
End Function

'-----------------------------------------------------------------------
'CloseOpenedTags - Eliminate the close tags which do not have open tags and vice versa.
'                   It is usually used to the contents returned by parser, because the
'                   markup program inserts collored tags (and also the html tags to achieve
'                   the collored effect), bringing also garbagge to the content, it means
'                   close tags which do not have open tags and vice versa.
'original   - string that contains close tags which do not have open tags and vice versa.
'Return - string without close tags which do not have open tags and vice versa.
'-----------------------------------------------------------------------
Function CloseOpenedTags(original As String) As String
    Dim curr    As String
    Dim nova    As String
    Dim P      As Long
    Dim p1      As Long
    Dim p2      As Long
    Dim Tag     As String
    Dim lista As ClLista
    Dim i As Long
    Dim found As Boolean
    Dim free As Long
    Dim tTag As String
    
    
    
    curr = Trim(original)
    While (InStr(curr, "</") = 1)
        P = InStr(curr, ">")
        curr = Mid(curr, P + 1)
    Wend
    
    P = Len(curr) - 1
    found = False
    
    
    While (Len(curr) > 0) And (Not found)
        If (Mid(curr, Len(curr)) = ">") Then
            P = 1
            p1 = InStr(curr, "<")
            While (p1 > 0)
                P = p1
                p1 = InStr(P + 1, curr, "<", vbBinaryCompare)
            Wend
            Tag = Mid(curr, P)
            If (InStr(Tag, "</") = 0) Then
                p2 = InStr(Tag, Chr(32))
                If p2 > 0 Then
                    tTag = Mid(Tag, 1, p2 - 1)
                Else
                    tTag = Tag
                    p2 = Len(Tag)
                End If
                Select Case LCase(tTag)
                Case "<br>", "<img", "<h", "<h>"
                    found = True
                Case Else
                    curr = Mid(curr, 1, P - 1)
                End Select
            Else
                found = True
            End If
        Else
            found = True
        End If
    Wend
    
    Set lista = New ClLista
    While Len(curr) > 0
        P = InStr(curr, "<")
        p1 = InStr(curr, ">")
        If (P = 0) Or (p1 = 0) Then
            nova = nova + curr
            curr = ""
        ElseIf P < p1 Then
            nova = nova + Mid(curr, 1, P - 1)
            Tag = Mid(curr, P, p1 - P + 1)
            curr = Mid(curr, p1 + 1)
            If InStr(Tag, "</") = 1 Then
                If Not lista.RemoveElem(Tag) Then
                    Tag = ""
                End If
            Else
                P = InStr(Tag, Chr(32))
                If P > 0 Then
                    tTag = Mid(Tag, 1, P - 1)
                Else
                    tTag = Tag
                    P = Len(Tag)
                End If
                
                Select Case LCase(tTag)
                Case "<br>", "<img", "<h", "<h>"
                Case Else
                    lista.Insere ("</" + Mid(Tag, 2, P - 2) + ">")
                End Select
            End If
            nova = nova + Tag
        Else
            nova = nova + Mid(curr, 1, P - 1)
            curr = Mid(curr, P)
        End If
    Wend
    While lista.RemoveLast(Tag)
        nova = nova + Tag
    Wend
    CloseOpenedTags = Trim(nova)
    
End Function

'-----------------------------------------------------------------------
'StandardFontFaceSymbol - eliminate the other attributes of the tag <FONT>, but remain
'    FACE="Symbol". This function do this is in order to standardize the tags <FONT FACE="Symbol">
'original   - input string, to be converted
'Return the string with the standardize the tags <FONT FACE="Symbol">
'-----------------------------------------------------------------------
Function StandardFontFaceSymbol(original As String) As String
    Dim pOpenFont1 As Long
    Dim pOpenFont2 As Long
    Dim pCloseFont1 As Long
    Dim symbol As String
    Dim Line As String
    Dim TagFONT As String
    Dim STANDARD As String
    Dim i As Long
    Dim GizmoMarkupStart As String
    Dim GizmoMarkupEnd As String
    
    Const OpenFont = "<FONT "
    Const CloseFont = "</FONT>"
    Const TAGC = ">"
    
    Line = original
    
    If InStr(1, Line, "symbol", vbTextCompare) > 0 Then
    
        GizmoMarkupStart = "<FONT FACE=" + Chr(34) + "Symbol" + Chr(34) + ">"
        GizmoMarkupEnd = "</FONT>"
    
        
        pOpenFont1 = InStr(1, Line, OpenFont, vbTextCompare)
        
        While pOpenFont1 > 0
            pOpenFont2 = InStr(pOpenFont1, Line, TAGC)
            If pOpenFont2 > 0 Then
                TagFONT = Mid(Line, pOpenFont1, pOpenFont2 - pOpenFont1 + 1)
                pCloseFont1 = InStr(pOpenFont2, Line, CloseFont, vbTextCompare)
                
                If pCloseFont1 > 0 Then
                    symbol = Trim(Mid(Line, pOpenFont2 + 1, pCloseFont1 - pOpenFont2 - 1))
            
                    If InStr(1, TagFONT, "symbol", vbTextCompare) > 0 Then
                        If Len(symbol) > 1 Then
                        Debug.Print symbol
                    '    i = 1
                    '    while i < Len(symbol)
                    '        standard = standard + Mid(symbol, i, 1) + GizmoMarkupEnd + GizmoMarkupStart
                    '        i = i + 1
                    '    Wend
                    '    symbol = standard
                        End If
                        Line = Mid(Line, 1, pOpenFont1 - 1) + GizmoMarkupStart + symbol + GizmoMarkupEnd + Mid(Line, pCloseFont1 + Len(CloseFont))
                'Else
                '    Line = Mid(Line, 1, pOpenFont1 - 1) + symbol + Mid(Line, pCloseFont1 + Len(CloseFont))
                    
                    End If
                Else
                    pCloseFont1 = Len(Line)
                End If
            End If
            pOpenFont1 = InStr(pCloseFont1 + Len(CloseFont), Line, OpenFont, vbTextCompare)
        Wend
    End If
    StandardFontFaceSymbol = Line
End Function

'-----------------------------------------------------------------------
'ConvertFONTFACESYMBOL2REPLACESYMBOL - Replace <FONT FACE="Symbol"> with <REPLACESYMBOL> and
'                                      and </FONT> with </REPLACESYMBOL>
'original   - input string, to be converted
'Return the string with <REPLACESYMBOL> and </REPLACESYMBOL>
'-----------------------------------------------------------------------
Private Function ConvertFONTFACESYMBOL2REPLACESYMBOL(original As String) As String
    Dim pOpenFont1 As Long
    Dim pOpenFont2 As Long
    Dim pCloseFont1 As Long
    Dim symbol As String
    Dim Line As String
    Dim TagFONT As String
    
    Const OpenFont = "<FONT FACE"
    Const CloseFont = "</FONT>"

    Const GizmoMarkupStart = "<REPLACESYMBOL>"
    Const GizmoMarkupEnd = "</REPLACESYMBOL>"

        
    Line = original
    
    If InStr(1, Line, "symbol", vbTextCompare) > 0 Then
    
        pOpenFont1 = InStr(1, Line, OpenFont, vbTextCompare)
        
        While pOpenFont1 > 0
            pOpenFont2 = InStr(pOpenFont1, Line, CONST_DELIM2)
            If pOpenFont2 > 0 Then
                TagFONT = Mid(Line, pOpenFont1, pOpenFont2 - pOpenFont1)
                pCloseFont1 = InStr(pOpenFont2, Line, CloseFont, vbTextCompare)
                symbol = Trim(Mid(Line, pOpenFont2 + 1, pCloseFont1 - pOpenFont2 - 1))
            
                If InStr(1, TagFONT, "symbol", vbTextCompare) > 0 Then
                    Line = Mid(Line, 1, pOpenFont1 - 1) + GizmoMarkupStart + symbol + GizmoMarkupEnd + Mid(Line, pCloseFont1 + Len(CloseFont))
                Else
                    Line = Mid(Line, 1, pOpenFont1 - 1) + symbol + Mid(Line, pCloseFont1 + Len(CloseFont))
                End If
            End If
            pOpenFont1 = InStr(1, Line, OpenFont, vbTextCompare)
        Wend
    End If
    
    ConvertFONTFACESYMBOL2REPLACESYMBOL = Line
End Function

'-----------------------------------------------------------------------
'Old_ConvertFONTFACESYMBOL2REPLACESYMBOL - Replace <FONT FACE="Symbol"> with <REPLACESYMBOL> and
'                                      and </FONT> with </REPLACESYMBOL>
'original   - input string, to be converted
'Return the string with <REPLACESYMBOL> and </REPLACESYMBOL>
'-----------------------------------------------------------------------
Private Function Old_ConvertFONTFACESYMBOL2REPLACESYMBOL(original As String) As String
    Dim pOpenFont1 As Long
    Dim pOpenFont2 As Long
    Dim pCloseFont1 As Long
    Dim symbol As String
    Dim Line As String
    Dim TagFONT As String
    
    Const OpenFont = "<FONT FACE"
    Const CloseFont = "</FONT>"

    Const GizmoMarkupStart = "<REPLACESYMBOL>"
    Const GizmoMarkupEnd = "</REPLACESYMBOL>"

        
    Line = original
    pOpenFont1 = InStr(1, Line, OpenFont, vbTextCompare)
        
    While pOpenFont1 > 0
        pOpenFont2 = InStr(pOpenFont1, Line, CONST_DELIM2)
        If pOpenFont2 > 0 Then
            TagFONT = Mid(Line, pOpenFont1, pOpenFont2 - pOpenFont1)
            pCloseFont1 = InStr(pOpenFont2, Line, CloseFont, vbTextCompare)
            symbol = Trim(Mid(Line, pOpenFont2 + 1, pCloseFont1 - pOpenFont2 - 1))
            
            If InStr(1, TagFONT, "symbol", vbTextCompare) > 0 Then
                Line = Mid(Line, 1, pOpenFont1 - 1) + GizmoMarkupStart + symbol + GizmoMarkupEnd + Mid(Line, pCloseFont1 + Len(CloseFont))
            Else
                Line = Mid(Line, 1, pOpenFont1 - 1) + symbol + Mid(Line, pCloseFont1 + Len(CloseFont))
            End If
        End If
        pOpenFont1 = InStr(1, Line, OpenFont, vbTextCompare)
    Wend
    Old_ConvertFONTFACESYMBOL2REPLACESYMBOL = Line
End Function


Function Convert2Win(s As String) As String
    Dim result As String
    
    result = s
    

    'Conversion sgml to <ReplaceSymbol>
    result = CvtTables("Conversion sgml to replsymb").Convert(result)
    
    result = ReplaceString(result, "&nbsp;", " ", vbBinaryCompare)
    
    If InStr(result, "<") > 0 Then
    
        '--Convert Font Face Symbol to <ReplaceSymbol>
        '--Result = ConvertFONTFACESYMBOL2REPLACESYMBOL(Result)
        'Convert Font Face Symbol to win
        result = CvtTables("Conversion symb to win").Convert(result)

        'Conversion of format of presentation to window

        result = CvtTables("Conversion presentation tags").Convert(result)
        
        'Conversion sup to windows
        result = CvtTables("Conversion sup to windows").Convert(result)
        result = TranslateSUBSUP(result, "<SUB>", "</SUB>")
        result = TranslateSUBSUP(result, "<SUP>", "</SUP>")

        'Remove the sgml tags which are not important
        'IMG,LINKS,EMAIL
        '--result = RmPartialHTML(result, True)
        result = RmPartialHTML(result, False)
        
    End If
    
    
    If InStr(result, "&lt;") > 0 And InStr(result, "&gt;") > 0 Then
        result = ReplaceString(result, "&lt;", "<", vbBinaryCompare)
    Else
        result = ReplaceString(result, "&lt;", "<", vbBinaryCompare)
        result = ReplaceString(result, "&gt;", ">", vbBinaryCompare)
    End If
    Convert2Win = result
End Function


Function ConvertIdiom(s As String, Optional language As String) As String
    Dim result As String
    
    result = s
    
    'conversao que depende de idioma
    If Len(language) > 0 Then
        Select Case language
        Case "en"
            result = CvtTabLanguage("Conversion to English").Convert(result)
        Case "es"
            result = CvtTabLanguage("Conversion to Spanish").Convert(result)
        Case "pt"
            result = CvtTabLanguage("Conversion to Portuguese").Convert(result)
        End Select
    End If
    ConvertIdiom = result
End Function

Function ConvertPercentCharacter(s As String, Optional language As String) As String
    Dim result As String
    
    
    result = s
    
    'conversao que depende de idioma
    'If Len(language) > 0 Then
        Select Case language
        Case "en"
            result = ReplaceString(result, "%", " percent", vbBinaryCompare)
        Case "es"
            result = ReplaceString(result, "%", " por ciento", vbBinaryCompare)
        Case "pt"
            result = ReplaceString(result, "%", " por cento", vbBinaryCompare)
        Case Else
            result = ReplaceString(result, "%", " percent", vbBinaryCompare)
        End Select
    'End If
    ConvertPercentCharacter = result
End Function


Private Function TranslateSUBSUP(content As String, TAG1 As String, TAG2 As String) As String
    Dim pTAG1 As Long
    Dim pTAG2 As Long
    Dim PrevChar As String
    Dim NextChar As String
    Dim sFirstChar As String
    Dim sLastChar As String
    Dim br1 As String
    Dim br2 As String
    Dim s As String
    Dim result As String
            
    result = content
    pTAG1 = InStr(1, result, TAG1, vbBinaryCompare)
    While pTAG1 > 0
        pTAG2 = InStr(pTAG1, result, TAG2, vbBinaryCompare)
        If pTAG1 > 1 Then
            PrevChar = Mid(result, pTAG1 - 1, 1)
        Else
            PrevChar = ""
        End If
        If (pTAG2 + Len(TAG2)) < Len(result) Then
            NextChar = Mid(result, pTAG2 + Len(TAG2), 1)
        Else
            NextChar = ""
        End If
        
        s = Mid(result, pTAG1 + Len(TAG1), pTAG2 - (pTAG1 + Len(TAG1)))
        If Len(s) > 0 Then
            sFirstChar = Mid(s, 1, 1)
            sLastChar = Mid(s, Len(s), 1)
            
            If (PrevChar Like "[A-Z]") And (sFirstChar Like "[A-Z]") Then
                br1 = " "
            ElseIf (PrevChar Like "[a-z]") And (sFirstChar Like "[a-z]") Then
                br1 = " "
            ElseIf (PrevChar Like "[0-9]") And (sFirstChar Like "[0-9]") Then
                br1 = "("
            ElseIf (PrevChar Like "[0-9]") And (Mid(s, Len(s), 2) Like "[-+][0-9]") Then
                br1 = "("
            Else
                br1 = ""
            End If
                
            If (sLastChar Like "[A-Z]") And (NextChar Like "[A-Z]") Then
                br2 = " "
            ElseIf (sLastChar Like "[a-z]") And (NextChar Like "[a-z]") Then
                br2 = " "
            ElseIf (sLastChar Like "[0-9]") And (NextChar Like "[0-9]") Then
                br2 = ")"
            'ElseIf (sLastChar Like "[0-9]") And (NextChar Like "[-+]") Then
                '   br2 = ")"
            Else
                br2 = ""
            End If
                
            If br1 = "(" Then br2 = ")"
            If br2 = ")" Then br1 = "("
        End If
        
        result = Mid(result, 1, pTAG1 - 1) + br1 + s + br2 + Mid(result, pTAG2 + Len(TAG2))
        
        pTAG1 = InStr(1, result, TAG1, vbTextCompare)
    Wend
    TranslateSUBSUP = result
End Function


'-----------------------------------------------------------------------
'Convert_LILACS_fname - convert some fields to be according to LILACS
'-----------------------------------------------------------------------
Function Convert_LILACS_fname(content As String) As String
    Dim P As Long
    content = Trim(ReplaceString(content, "  ", " ", vbTextCompare))
    If Len(content) > 0 Then
         
        P = InStr(content, ".")
        If P > 0 Then
            content = Trim(ReplaceString(content, ".", ". ", vbBinaryCompare))
            If Mid(content, Len(content), 1) = "." Then
                 content = Mid(content, 1, Len(content) - 1)
            End If
            content = ReplaceString(content, "  ", " ", vbTextCompare)
        End If
        
        'content = UpperCaseFirstLetterAfterCharacter(content, " ")
        'content = UpperCaseFirstLetterAfterCharacter(content, "-")
     End If
     
     Convert_LILACS_fname = content
End Function

'-----------------------------------------------------------------------
'Convert_LILACS_surname - convert some fields to be according to LILACS
'-----------------------------------------------------------------------
Function Convert_LILACS_surname(content As String) As String
    
    content = Trim(ReplaceString(content, "  ", " ", vbTextCompare))
    If Len(content) > 0 Then
        'content = UpperCaseFirstLetterAfterCharacter(content, " ")
        'content = UpperCaseFirstLetterAfterCharacter(content, "-")
        
        content = ReplaceString(content, "Jr.", "Júnior", vbBinaryCompare)
        content = ReplaceString(content, "Jr", "Júnior", vbBinaryCompare)
    End If
    Convert_LILACS_surname = content
End Function


Function UpperCaseFirstLetterAfterCharacter(s As String, character As String) As String
    Dim aux As String
    Dim r As String
    Dim P As Long
    
    s = Trim(s)
    
    P = InStr(s, character)
    
    If P > 0 Then
        aux = LCase(s)
        r = ""
        While (P > 0) And (Len(aux) > 0)
            r = r + Mid(aux, 1, P) + UCase(Mid(aux, P + 1, 1))
            aux = Mid(aux, P + 2)
            P = InStr(aux, character)
        Wend
    Else
        r = s
    End If
    r = UCase(Mid(r, 1, 1)) + Mid(r, 2)
    
    If InStr(1, r, character, vbTextCompare) > 0 Then
        r = ReplaceString(r, character + "E" + character, character + "e" + character, vbBinaryCompare)
        r = ReplaceString(r, character + "De" + character, character + "de" + character, vbBinaryCompare)
        r = ReplaceString(r, character + "Da" + character, character + "da" + character, vbBinaryCompare)
        r = ReplaceString(r, character + "Do" + character, character + "do" + character, vbBinaryCompare)
        r = ReplaceString(r, character + "Dos" + character, character + "dos" + character, vbBinaryCompare)
    End If
    
    UpperCaseFirstLetterAfterCharacter = r
End Function


Function convertTable(s As String) As String
  Dim table As String
  
  If InStr(1, s, "<table", vbTextCompare) > 0 Then
    table = s
  Else
    table = ""
  End If
  convertTable = table
  
End Function
Function existSPANTags(t As String, res() As String) As Long
    Dim r As Boolean
    
    Dim a() As String, B() As String
    Dim i As Long, j As Long
    
    a = Split(t, "[")
    For i = 1 To UBound(a)
        If Len(a(i)) > 0 Then
            B = Split(a(i), "]")
            If InStr(B(0), "<") > 0 And InStr(B(0), ">") > 0 Then
                j = j + 1
                ReDim Preserve res(j)
                res(j) = B(0)
            End If
        End If
    Next
    
    existSPANTags = j
End Function
Function xexistSPANTags(t As String, res() As String) As Long
    Dim r As Boolean
    
    Dim a() As String, B() As String
    Dim i As Long, j As Long
    
    a = Split(t, "[")
    For i = 0 To UBound(a) - 1
        B = Split(a(i), "]")
        If InStr(B(0), "<") > 0 And InStr(B(0), ">") > 0 Then
            j = j + 1
            ReDim Preserve res(j)
            res(j) = B(0)
        End If
    Next
    
    xexistSPANTags = j
End Function

Function convertChar2Ent(content) As String
    Dim i As Long
    Dim c As String
    Dim n As Long
    Dim s As String
    
    For i = 1 To Len(content)
        c = Mid(content, i, 1)
        n = AscW(c)
        If n > 256 Then
            s = s + "&#" + CStr(n) + ";"
        Else
            s = s + c
        End If
    Next
    convertChar2Ent = s
End Function
