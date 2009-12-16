VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "ClFullTxt"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

Const TamMaxParag = 7000

Private mvarNome As String 'local copy
Private mvarPath As String 'local copy
Private mvarTexto As ClTxt 'local copy
Private mvarFullpath As String 'local copy
Private mvarRegParags As ColRegistro 'local copy

Private TextWithoutSpaces As ClTxt
Private SpacePos() As String

Private LinesParag() As String

Private REFTAGEND   As String
Private REFTAGSTART   As String

Const STANDARDIZEDENDPARAG = "[STANDARDIZEDENDPARAG]"

Public Property Let Path(ByVal vData As String)
'used when assigning a value to the property, on the left side of an assignment.
'Syntax: X.Path = 5
    mvarPath = vData
End Property

Public Property Get Path() As String
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: 'Debug.Print X.Path
    Path = mvarPath
End Property

Public Property Let Nome(ByVal vData As String)
    mvarNome = vData
End Property

Public Property Get Nome() As String
    Nome = mvarNome
End Property

Public Property Set RegParags(ByVal vData As Object)
'used when assigning an Object to the property, on the left side of a Set statement.
'Syntax: Set x.RegParags = Form1
    Set mvarRegParags = vData
End Property

Public Property Get RegParags() As ColRegistro
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: 'Debug.Print X.RegParags
    Set RegParags = mvarRegParags
End Property

Public Property Get FullPath() As String
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: 'Debug.Print X.Fullpath
    FullPath = mvarPath + PathSep + mvarNome
End Property

Public Property Set Texto(ByVal vData As Object)
'used when assigning an Object to the property, on the left side of a Set statement.
'Syntax: Set x.Texto = Form1
    Set mvarTexto = vData
End Property

Public Property Get Texto() As ClTxt
'used when retrieving value of a property, on the right side of an assignment.
'Syntax: 'Debug.Print X.Texto
    Set Texto = mvarTexto
End Property

'-----------------------------------------------------------------------
'Read    -   le texto completo
'Path   - caminho
'File   - nome do arquivo do texto completo
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Public Function Read(Path As String, file As String) As Boolean
    Dim ret As Boolean
    Dim fn As Long
    Dim s As String
    Dim i As Long
    Dim BlockTags() As String
    Dim BlockTagsCount As Long
    
    BlockTagsCount = 14
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
    
    
    If FileExist(Path, file, "Fulltext") Then
        Set Texto = New ClTxt
        Set TextWithoutSpaces = New ClTxt
        
        mvarPath = Path
        mvarNome = file
        
        fn = FreeFile(1)
        Open Path + PathSep + file For Input As fn
        Do Until EOF(fn)
            Line Input #fn, s
            s = s + SPACE_END_FOR_HTML
            s = StandardizeEndParag(s, BlockTags, BlockTagsCount)
            s = ReplaceString(ReplaceString(s, "&amp;rsqb;", "]"), "&amp;lsqb;", "[")
            s = ReplaceString(ReplaceString(s, "&amp;#093;", "]"), "&amp;#091;", "[")
            Texto.AddLines (s)
            TextWithoutSpaces.AddLines (s)
        Loop
        Close fn
        
        Set TextWithoutSpaces = TextWithoutSpaces.ReplaceEntitybySpaces(ASCIITable, " ")
        Set TextWithoutSpaces = TextWithoutSpaces.ReplaceEntitybySpaces(ASCIITable, ";")
        Set TextWithoutSpaces = TextWithoutSpaces.ReplaceAllHTMLbySpaces
        'ReplaceAllHTMLbySpaces (TextWithoutSpaces)
        
        ReDim SpacePos(TextWithoutSpaces.Qtd)
        
        For i = 1 To TextWithoutSpaces.Qtd
            TextWithoutSpaces.SetLine(i) = KeepSomeChar(TextWithoutSpaces.GetLine(i))
            TextWithoutSpaces.SetLine(i) = RmSpace(TextWithoutSpaces.GetLine(i), SpacePos(i))
        Next
        
        ret = True
    End If

    Read = ret
End Function

'OldReplaceAllHTMLbySpaces - replace the HTML Tags by spaces for
'keeping the position of the words when they are compared.

'-----------------------------------------------------------------------
'GetParagraphs  - obtém parágrafos do texto completo
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Public Function GetParagraphs() As Long
    Dim ret         As Boolean
    Dim Parag()     As String
    Dim TagParag    As String
    Dim p           As TpPosition
    Dim LimInf      As TpPosition
    Dim LimSup      As TpPosition
    Dim ParagIni    As TpPosition
    Dim ParagFim    As TpPosition
    Dim QtdParag    As Long
    Dim j           As Long
    Dim prossegue   As Boolean
    Dim s           As String
    Dim PRefMark1   As Long
    Dim PRefMark2   As Long
    Dim Mark        As String
    Dim Counter     As Long
    
    REFTAGEND = "</" + CStr(ISISTAGS("ref").value) + ">"
    REFTAGSTART = "<" + CStr(ISISTAGS("ref").value) + ">"
    
    'Obtem os paragrafos, texto completo.
    Call Msg.GiveRunInformation("Getting full text...", , True)
    
    'Obtem o body html sem tags de marcacao
    With Texto
    LimInf.i = 1
    LimInf.j = 1
    Call .GetEnd(LimSup.i, LimSup.j)
    If .GetLen(LimInf.i, LimInf.j, LimSup.i, LimSup.j) > 0 Then
        Call .InString(LimInf.i, LimInf.j, LimSup.i, LimSup.j, "<body", p.i, p.j, vbTextCompare)
        If p.j > 0 Then
            Call .InString(p.i, p.j, LimSup.i, LimSup.j, ">", LimInf.i, LimInf.j, 1)
            Call .ForwardPosition(LimInf.i, LimInf.j, 1)
            Call .InString(LimInf.i, LimInf.j, LimSup.i, LimSup.j, "</body", p.i, p.j, vbTextCompare)
            LimSup = p
            Call .RewardPosition(LimSup.i, LimSup.j, 1)
        End If

        Counter = 0
        prossegue = .ExisteStr(LimInf.i, LimInf.j, LimSup.i, LimSup.j)
        While prossegue
            TagParag = FindNewParagraph(LimInf, LimSup, p)
            ParagIni = LimInf
            LimInf = p
            If p.j > 0 Then
                Call .ForwardPosition(LimInf.i, LimInf.j, Len(TagParag))  'obtem o novo ParagIni
                'ParagFim = LimInf 'obtem o ParagFim parcial
                ParagFim = p 'obtem o ParagFim parcial
                Call .RewardPosition(ParagFim.i, ParagFim.j, 1)
            Else
                ParagFim = LimSup
                prossegue = False
            End If
            QtdParag = GetParagraph(ParagIni, ParagFim, Parag)
            
            For j = 1 To QtdParag - 1
                Call FormatParag(Parag(j), Counter)
            Next
            If QtdParag > 0 Then Call FormatParag(Parag(QtdParag), Counter)
        Wend
        Set Texto = Nothing
    End If
    End With
    GetParagraphs = Counter
End Function
               
Sub FormatParag(Parag As String, Counter As Long)
    Dim PRefMark1   As Long
    Dim PRefMark2   As Long
    Dim Mark        As String
        
    If (Len(Trim(Parag)) > 0) Then
        Counter = Counter + 1
        PRefMark1 = InStr(Parag, REFTAGSTART)
        PRefMark2 = InStr(Parag, REFTAGEND)
        
        If (PRefMark1 > 0) And (PRefMark2 > PRefMark1) Then
            Mark = Mid(Parag, PRefMark1 + Len(REFTAGSTART), PRefMark2 - PRefMark1 - Len(REFTAGSTART))
            Parag = Mid(Parag, 1, PRefMark1 - 1) + Mid(Parag, PRefMark2 + Len(REFTAGEND))
            Call RegParags.Add(RecordInfo("paragraph").label + CStr(Counter) + "r", Trim(ISISTAGS("ref").value), Mark, RecordInfo("paragraph").label, CStr(Counter))
        End If

        Parag = ReplaceString(Parag, "^", "&#094;")
        Call RegParags.Add(RecordInfo("paragraph").label + CStr(Counter), ISISTAGS("fulltext").value, Parag + "    ^cY", RecordInfo("paragraph").label, CStr(Counter))
    End If
End Sub

'-----------------------------------------------------------------------
'FindNewParagraph  - encontra um novo parágrafo dentro de um intervalo
'ini    - limite inferior
'fim    - limite superior
'P  - posição do parágrafo encontrado
'Retorno    - sucesso ou fracasso
'-----------------------------------------------------------------------
Private Function FindNewParagraph(ini As TpPosition, Fim As TpPosition, p As TpPosition) As String
    Dim retorno As String
    
    Call Texto.InString(ini.i, ini.j, Fim.i, Fim.j, STANDARDIZEDENDPARAG, p.i, p.j, vbBinaryCompare)
    If p.j > 0 Then
        retorno = STANDARDIZEDENDPARAG
    End If
    FindNewParagraph = retorno
End Function

'-----------------------------------------------------------------------
'GetParagraph   - obtém parágrafo de um intervalo
'ini    - limite inferior
'fim    - limite superior
'Paragraph  - parágrafos
'Retorno    - quantidade de parágrafos
'-----------------------------------------------------------------------
Private Function GetParagraph(ini As TpPosition, Fim As TpPosition, Paragraph() As String) As Long
    Dim Qtd     As Long
    Dim aux As String
    Dim i As Long
    
    Erase Paragraph
    If Texto.GetLen(ini.i, ini.j, Fim.i, Fim.j) <= TamMaxParag Then
        ReDim Paragraph(1)
        'Paragraph(1) = Texto.GetSubstrRange(ini.i, ini.j, Fim.i, Fim.j, " ")
        Paragraph(1) = Texto.GetSubstrRange(ini.i, ini.j, Fim.i, Fim.j)
        Qtd = 1
    Else
        'paragrafo - aux = Mid(Texto.GetLine(ini.i), ini.j) + " "
        aux = Mid(Texto.GetLine(ini.i), ini.j)
        i = ini.i
        While (i < Fim.i - 1)
            i = i + 1
            If (Len(aux) + Len(Texto.GetLine(i))) < TamMaxParag Then
                'paragrafo - aux = aux + Texto.GetLine(i) + " "
                aux = aux + Texto.GetLine(i)
            Else
                Qtd = Qtd + 1
                ReDim Preserve Paragraph(Qtd)
                Paragraph(Qtd) = aux
                'paragrafo - aux = Texto.GetLine(i) + " "
                aux = Texto.GetLine(i)
            End If
        Wend
        aux = aux + Mid(Texto.GetLine(Fim.i), 1, Fim.j)
        Qtd = Qtd + 1
        ReDim Preserve Paragraph(Qtd)
        Paragraph(Qtd) = aux
    End If
    GetParagraph = Qtd
End Function

Function FindReferences(References() As String, ReferencesCounter As Long) As Boolean
    Dim ret As Boolean
    Dim i As Long
    Dim LimInf As TpPosition
    Dim LimSup As TpPosition
    Dim R As String
    Dim found As Boolean
    Dim ReferenceStrLen As Long
    Dim j As Long
    Dim OldReference As String
    
    LimInf.i = 1
    LimInf.j = 1
    Call TextWithoutSpaces.GetEnd(LimSup.i, LimSup.j)
    
    ret = True
    For i = 1 To ReferencesCounter
        'prepare references to compare them
        References(i) = RmAllHTML(References(i))
        ReferenceStrLen = Len(References(i))
        OldReference = References(i)
        References(i) = ""
        
        For j = 1 To ReferenceStrLen
            If Mid(OldReference, j, 1) Like "[A-Za-z0-9]" Then
                References(i) = References(i) + Mid(OldReference, j, 1)
            End If
        Next
        Debug.Print OldReference
        Debug.Print References(i)
               
        found = FindReferenceInText(i, References(i), LimInf, LimSup)
        If Not found Then R = R + "," + CStr(i)
        ret = ret And found
    Next
    
    If Not ret Then
        R = Mid(R, 2)
        Call Msg.GiveRunInformation("Missing References=" + R)
        ret = True 'retirar futuramente, roberta
    End If
    FindReferences = ret
End Function

Function KeepSomeChar(s As String) As String
    Dim s2 As String
    Dim s3 As String
    Dim x As String
    Dim j As Long
    Dim ReferenceStrLen As Long
    
    s2 = s
    s3 = ""
    ReferenceStrLen = Len(s)
        
    For j = 1 To ReferenceStrLen
        x = Mid(s2, j, 1)
        If x Like "[A-Za-z0-9]" Then
            s3 = s3 + x
        Else
            s3 = s3 + " "
        End If
    Next
    Debug.Print s
    Debug.Print s3
    KeepSomeChar = s3
End Function


Private Function FindReferenceInText(IdReference As Long, Reference As String, LimInf As TpPosition, LimSup As TpPosition) As Long
    Dim Pos As TpPosition
    Dim Pos2 As TpPosition
    Dim P1 As Long
    Dim P2 As Long
    Dim Pieces As String
    Dim OK As Boolean
    Dim ReferenceMark As String
    
    
    
    Call TextWithoutSpaces.New_InString(LimInf.i, LimInf.j, LimSup.i, LimSup.j, Reference, Pos.i, Pos.j, vbBinaryCompare)
    If Pos.j > 0 Then
        With TextWithoutSpaces
        Pos2 = Pos
        Call .ForwardPosition(Pos2.i, Pos2.j, Len(Reference))
        LimInf = Pos2
    
        ReferenceMark = Trim(RmNewLineInStr(TagContents(CStr(IdReference), ISISTAGS("ref").value)))
        
        Pieces = InsSpace(Mid(.GetLine(Pos.i), 1, Pos.j), SpacePos(Pos.i))
        P1 = Len(Pieces)
        
        Call .RewardPosition(Pos2.i, Pos2.j, 1)
        Pieces = InsSpace(Mid(.GetLine(Pos2.i), 1, Pos2.j), SpacePos(Pos2.i))
        P2 = Len(Pieces)
        End With
        
        With Texto
        Pos2.j = P2
        If FindEndReference(Pos2.i, Pos2.j) Then
            .SetLine(Pos2.i) = Mid(.GetLine(Pos2.i), 1, Pos2.j) + ReferenceMark + STANDARDIZEDENDPARAG + Mid(.GetLine(Pos2.i), Pos2.j + 1)
            Debug.Print "Reconheceu " + .GetLine(Pos2.i)
            TextWithoutSpaces.SetLine(Pos2.i) = RmSpace(.GetLine(Pos2.i), SpacePos(Pos2.i))
            Debug.Print "RmSpace " + .GetLine(Pos2.i)
            OK = True
        Else
            Debug.Print "Não Reconheceu " + .GetLine(Pos2.i)
        End If
        End With
        
    Else
        Debug.Print Reference
        
    End If
    
    FindReferenceInText = OK
End Function

Function FindEndReference(InitRow As Long, InitCol As Long) As Boolean
    Dim pEndRef As TpPosition
    Dim s As String
    Dim i As Long
    Dim j As Long
    Dim NextParag As TpPosition
    Dim char As String
    Dim found As Boolean
        
    i = InitRow
    j = InitCol
    
    Call Texto.ForwardPosition(i, j, 1)
    Call Texto.InString(i, j, Texto.Qtd, Len(Texto.GetLine(Texto.Qtd)), STANDARDIZEDENDPARAG, NextParag.i, NextParag.j, vbBinaryCompare)
    
    If NextParag.j > 0 Then
        pEndRef = NextParag
        Call Texto.RewardPosition(pEndRef.i, pEndRef.j, 1)
    Else
        pEndRef.i = Texto.Qtd
        pEndRef.j = Len(Texto.GetLine(Texto.Qtd))
    End If
    
    char = ""
    While Texto.ExisteStr(i, j, pEndRef.i, pEndRef.j) And (Len(char) = 0)
        s = TextWithoutSpaces.GetLine(i)
        s = InsSpace(s, SpacePos(i))
        
        Debug.Print "Linha em que procuro [A-z0-9]"
        Debug.Print s
        If pEndRef.i = i Then
            s = Mid(s, 1, pEndRef.j)
            Debug.Print s
        End If
        s = Mid(s, j)
        Debug.Print s
        
        char = Trim(s)
        Debug.Print "CHAR = " + char
        If Len(char) = 0 Then
            i = i + 1
            j = 1
        Else
            pEndRef.j = InStr(s, char)
            pEndRef.i = i
            Call Texto.ForwardPosition(pEndRef.i, pEndRef.j, j - 1)
        End If
    Wend
    'If Len(char) > 0 Then
        Debug.Print "Row Pos [A-z0-9] -> " + Texto.GetLine(pEndRef.i)
        Debug.Print "Col Pos [A-z0-9] -> " + Mid(Texto.GetLine(pEndRef.i), pEndRef.j)
        
        s = Texto.GetLine(pEndRef.i)
        
        Call Texto.ForwardPosition(InitRow, InitCol, 1)
    
        While (Not found) And Texto.ExisteStr(InitRow, InitCol, pEndRef.i, pEndRef.j)
            char = Mid(s, pEndRef.j, 1)
            Debug.Print "Case char = " + Mid(s, pEndRef.j)
            Select Case char
            Case ">"
                found = True
            Case ","
                found = True
            Case ";"
                found = True
            Case "."
                found = True
            Case Else
                Call Texto.RewardPosition(pEndRef.i, pEndRef.j, 1)
                s = Texto.GetLine(pEndRef.i)
            End Select
        Wend
    'End If
    
    Debug.Print "Linha da Ref "
    Debug.Print Texto.GetLine(pEndRef.i)
    
    Debug.Print "Linha da Ref Limitada"
    Debug.Print Mid(Texto.GetLine(pEndRef.i), 1, pEndRef.j) + " [FIM]"
    
    If found Then
        InitRow = pEndRef.i
        InitCol = pEndRef.j
    Else
        found = True
    End If
    
    FindEndReference = found
End Function

Private Function RmSpace(s As String, SpacePos As String) As String
    Dim nova As String
    Dim p As Long
    Dim Start As Long
    
    nova = s
    Start = 1
    p = InStr(Start, nova, " ", vbTextCompare)
    While (p > 0)
        SpacePos = SetElemStr(SpacePos, ",", CStr(p))
        Start = p + 1
        p = InStr(Start, nova, " ", vbTextCompare)
    Wend
    nova = ReplaceString(nova, " ")
    RmSpace = nova
End Function

'NoSpaceCounter - quantidade de caracteres diferentes de espaço que devem estar contido na string retornada
Private Function InsSpace(ByVal s1 As String, SpacePos As String) As String
    Dim Pos() As String
    Dim q As Long
    Dim i As Long
    Dim s As String
    Dim quit As Boolean
    
    s = s1
    If Len(SpacePos) > 0 Then
        q = GetElemStr(SpacePos, ",", Pos)
        For i = 1 To q
            s = Mid(s, 1, CLng(Pos(i)) - 1) + " " + Mid(s, CLng(Pos(i)))
        Next
    
        quit = False
        While (Len(s) > 0) And (Not quit)
            If Mid(s, Len(s), 1) = " " Then
                s = Mid(s, 1, Len(s) - 1)
            Else
                quit = True
            End If
        Wend
    End If
    InsSpace = s
End Function

Function StandardizeEndParag(s As String, BlockTags() As String, q As Long) As String
    Dim s2 As String
    Dim p As Long
    Dim pi As Long
    Dim i As Long
    
    s2 = s
    If Len(s2) > 0 Then
    For i = 1 To q
        
        pi = 1
        p = InStr(pi, s2, BlockTags(i), vbTextCompare)
        While (p > 0)
            If p > 1 Then
                s2 = Mid(s2, 1, p - 1) + STANDARDIZEDENDPARAG + Mid(s2, p)
            Else
                s2 = STANDARDIZEDENDPARAG + s2
            End If
            pi = p + Len(STANDARDIZEDENDPARAG) + Len(BlockTags(i))
            p = InStr(pi, s2, BlockTags(i), vbTextCompare)
        Wend
    Next
    End If
    StandardizeEndParag = s2
End Function
