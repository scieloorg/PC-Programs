VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClTxt"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

'Const StrMaxLen = 60000
Private Lines() As String
Private LinesLen() As Long
Private LinesCounter As Long


Function test_get_from_a_row_a_string_with_max_characters(ByVal startLine As Long, Max As Long) As String
    Dim i As Long
    Dim r As String
    
    i = startLine
    While i <= LinesCounter
        r = r & Lines(i)
        i = i + 1
    Wend
    test_get_from_a_row_a_string_with_max_characters = r
End Function

Function test_getSubstring(s_i As Long, s_j As Long, e_i As Long, e_j As Long) As String
    Dim test As String
    Dim i As Long
    
    If s_i > 0 And s_i <= LinesCounter Then
    If s_i = e_i Then
        test = Mid(GetLine(s_i), s_j, e_j - s_j + 1)
    Else
        test = Mid(GetLine(s_i), s_j)
        For i = s_i + 1 To e_i - 1
            test = test & GetLine(i)
        Next
        test = test & Mid(GetLine(e_i), 1, e_j)
    End If
    End If
    test_getSubstring = test
End Function

Sub replaceSubstring(substring As String, s_i As Long, s_j As Long, e_i As Long, e_j As Long)
    Dim i As Long
    
    If s_i = e_i Then
        SetLine(s_i) = Mid(GetLine(s_i), 1, s_j - 1) & substring & Mid(GetLine(s_i), e_j + 1)
    Else
        SetLine(s_i) = Mid(GetLine(s_i), 1, s_j - 1) & substring
         
        
        For i = s_i + 1 To e_i - 1
            SetLine(i) = ""
        Next
        SetLine(e_i) = Mid(GetLine(e_i), e_j + 1)
    End If
    
End Sub
'-----------------------------------------------------------------------
'test_InString   - verifica se existe alguma substring num determinado intervalo
'startFinding - linha inicial da busca
'term - substring
' rowStart - linha inicial da string
' colStart - coluna inicial da string
' rowEnd - linha final da string
' colEnd - coluna final da string
'-----------------------------------------------------------------------
Sub test_InString(ByVal SearchingBeginRow As Long, ByVal SearchingBeginCol As Long, term As String, _
                TermBeginRow As Long, TermBeginCol As Long, TermEndRow As Long, TermEndCol As Long, _
                prevRow As Long, prevCol As Long, nextRow As Long, nextCol As Long, comp As VbCompareMethod)
    Dim s As String
    Dim pTerm As Long
    Dim P As Long
    
    Dim pfoundPrevious As Long
        
    TermBeginRow = 0
    TermBeginCol = 0
    TermEndRow = 0
    TermEndCol = 0
    prevRow = 0
    prevCol = 0
    nextRow = 0
    nextCol = 0
    
    If SearchingBeginRow > 0 And SearchingBeginCol > 0 Then
    s = test_get_from_a_row_a_string_with_max_characters(SearchingBeginRow, Len(term))
    pTerm = InStr(SearchingBeginCol, s, term, comp)
        
    If pTerm > 0 Then
        P = pTerm - 1
        prevRow = SearchingBeginRow
        Call test_getStringEndPosition(P, prevRow, prevCol)
        
        TermBeginRow = SearchingBeginRow
        Call test_getStringEndPosition(pTerm, TermBeginRow, TermBeginCol)
        
        If TermBeginCol > 0 Then
                    
            P = pTerm + Len(term) - 1
            TermEndRow = SearchingBeginRow
            Call test_getStringEndPosition(P, TermEndRow, TermEndCol)
            
            P = pTerm + Len(term)
            nextRow = SearchingBeginRow
            Call test_getStringEndPosition(P, nextRow, nextCol)
            
        End If
    End If
    End If
End Sub

Sub test_getStringEndPosition(ByVal stringLength As Long, beginAndEndRow As Long, EndCol As Long)
    EndCol = 0
    If stringLength > 0 Then
        While beginAndEndRow <= LinesCounter And EndCol = 0
            If stringLength <= LinesLen(beginAndEndRow) Then
                ' está nesta linha
                EndCol = stringLength
            Else
                stringLength = stringLength - LinesLen(beginAndEndRow)
                beginAndEndRow = beginAndEndRow + 1
            End If
        Wend
    Else
        ' vai para uma linha anterior e pega a última coluna
        While EndCol = 0 And beginAndEndRow > 0
            beginAndEndRow = beginAndEndRow - 1
            EndCol = LinesLen(beginAndEndRow)
        Wend
    End If
End Sub
'-----------------------------------------------------------------------
'GetSubstrInRow    - obtém uma substring de uma linha a partir da posição inicial
'RowIdx  - índice da linha
'InitPos - posição inicial
'MaxLen - tamanho máximo da substring, retorna o tamanho real
'Retorno    - substring
'-----------------------------------------------------------------------
Function GetSubstrInRow(RowIdx As Long, InitPos As Long, maxlen As Long) As String
    Dim substr As String
    
    If (maxlen >= (LinesLen(RowIdx) - InitPos + 1)) Then
        substr = Mid(Lines(RowIdx), InitPos)
        maxlen = Len(substr)
    ElseIf (maxlen = 0) Then
        substr = ""
    Else
        substr = Mid(Lines(RowIdx), InitPos, maxlen)
    End If
    GetSubstrInRow = substr
End Function

'-----------------------------------------------------------------------
'AddLines  - adiciona linhas
'Line  - Linha
'-----------------------------------------------------------------------
Sub AddLines(Line As String)
 
    Qtd = Qtd + 1
    If Len(Line) > 0 Then
        Lines(LinesCounter) = Line
        LinesLen(LinesCounter) = Len(Line)
    Else
        Lines(LinesCounter) = ""
        LinesLen(LinesCounter) = 1
    End If
    'If LinesLen(LinesCounter) > StrMaxLen Then msgbox (CStr(LinesCounter) + Chr(32) + CStr(LinesLen(LinesCounter)))
End Sub

'-----------------------------------------------------------------------
'ForwardPosition  - avança a posição
'pi - posição da linha
'pj - posição da coluna
'avanco - avanço
'-----------------------------------------------------------------------
Sub ForwardPosition(pi As Long, pj As Long, ByVal avanco As Long)
    Dim i As Long
    Dim j As Long
    Dim t As Long
    
    If (pi > 0) And (pi <= Qtd) And (pj > 0) And (pj <= Len(Lines(pi))) And (avanco > 0) Then
        i = pi
        j = pj
        While (avanco > 0) And (i <= Qtd)
            t = Len(Lines(i)) - j + 1
            If avanco >= t Then
                avanco = avanco - t
                i = i + 1
                j = 1
            Else
                j = j + avanco
                avanco = 0
            End If
        Wend
        pi = i
        pj = j
    End If
End Sub

'-----------------------------------------------------------------------
'GetLen - retorna o tamanho de uma string de dadas posições
'Row1 - posição da linha 1
'Col1 - posição da coluna 1
'Row2 - posição da linha 2
'Col2 - posição da coluna 2
'retorno    - o tamanho
'-----------------------------------------------------------------------
Function GetLen(Row1 As Long, Col1 As Long, Row2 As Long, Col2 As Long) As Long
    Dim i As Long
    Dim tamanho As Long
    
    If Row2 > Qtd Then
        Row2 = Qtd
        'msgbox ("GetLen")
    End If
    If (Row1 > 0) And (Row2 > 0) And (Col1 > 0) And (Col2 > 0) Then
        If Row1 = Row2 Then
            'GetLen = LinesLen(Row1) - Col1 + 1
            GetLen = Col2 - Col1 + 1
        ElseIf Row1 < Row2 Then
            tamanho = LinesLen(Row1) - Col1 + 1 + Col2
            For i = (Row1 + 1) To (Row2 - 1)
                tamanho = tamanho + LinesLen(i)
            Next
            GetLen = tamanho
        Else
            GetLen = -1
        End If
    Else
        GetLen = -1
    End If
End Function

'-----------------------------------------------------------------------
'RewardPosition  - retrocede a posição
'pi - posição da linha
'pj - posição da coluna
'retro  - retrocesso
'-----------------------------------------------------------------------
Sub RewardPosition(pi As Long, pj As Long, retro As Long)

    Dim i As Long
    Dim j As Long
    Dim t As Long
    
    If (pi > 0) And (pi <= Qtd) And (pj > 0) And (retro > 0) Then
        i = pi
        j = pj
        While (retro > 0) And (i > 0)
            t = j
            If retro >= t Then
                retro = retro - t
                i = i - 1
                If i > 0 Then
                    j = Len(Lines(i))
                Else
                    j = 0
                End If
            Else
                j = t - retro
                retro = 0
            End If
        Wend
        pi = i
        pj = j
    End If
End Sub

'-----------------------------------------------------------------------
'Delete   - Delete
'-----------------------------------------------------------------------
Sub Delete()
    LinesCounter = 0
    ReDim Lines(1)
    ReDim LinesLen(1)
    Lines(1) = ""
    LinesLen(1) = 0
End Sub

'-----------------------------------------------------------------------
'ExisteStr  - verifica se string existe
'Row1 - posição da linha inicial
'Col1 - posição da coluna inicial
'Row2 - posição da linha final
'Col2 - posição da coluna final
'Retorno    - verdadeiro ou falso
'-----------------------------------------------------------------------
Public Function ExisteStr(Row1 As Long, Col1 As Long, Row2 As Long, Col2 As Long) As Boolean
    Dim retorno As Boolean
        
    If (Row1 < Row2) Or ((Row1 = Row2) And (Col1 <= Col2)) Then
        If (Row1 > 0) And (Row1 < Qtd) Then
            retorno = True
        ElseIf (Row1 = Qtd) And (Col1 <= LinesLen(Qtd)) Then
            retorno = True
        ElseIf (Row2 > 0) And (Row2 < Qtd) Then
            retorno = True
        ElseIf (Row2 = Qtd) And (Col2 <= LinesLen(Qtd)) Then
            retorno = True
        End If
    End If
    ExisteStr = retorno
End Function

'-----------------------------------------------------------------------
'GetEnd - obtém a posição final
'EndRow - posição da linha final
'EndCol - posição da coluna final
'-----------------------------------------------------------------------
Sub GetEnd(EndRow As Long, EndCol As Long)
    Dim i As Long
    
    i = Qtd
    If Qtd > 0 Then
        While (LinesLen(i) = 0) And (i > 0)
            i = i - 1
        Wend
    
        EndRow = i
        EndCol = LinesLen(i)
    End If
End Sub

'-----------------------------------------------------------------------
'GetLine  - retorna o conteúdo de uma GetLine
'pi     - índice da GetLine
'retorno - o conteúdo
'-----------------------------------------------------------------------
Property Get GetLine(pi As Long) As String
    If (pi < 1) Or (pi > Qtd) Then
        GetLine = ""
    Else
        GetLine = Lines(pi)
    End If
End Property

'-----------------------------------------------------------------------
'Line  - dá Value a uma linha
'pi     - índice da SetLine
'retorno - o conteúdo
'-----------------------------------------------------------------------
Property Let SetLine(pi As Long, Value As String)
    If (pi > Qtd) Then Qtd = pi
    Lines(pi) = Value
    LinesLen(pi) = Len(Value)
End Property

'-----------------------------------------------------------------------
'GetLineLen   - retorna tamanho de uma linha a partir de alguma posição
'LineIndex - índice da linha
'PosInLine - índice da coluna (opcional, posição default=1)
'retorno    - o tamanho
'-----------------------------------------------------------------------
Function GetLineLen(LineIndex As Long, Optional PosInLine As Variant) As Long
    If (LineIndex < 1) Or (LineIndex > Qtd) Then
        GetLineLen = 0
    Else
        If IsMissing(PosInLine) Then
            GetLineLen = LinesLen(LineIndex)
        Else
            GetLineLen = LinesLen(LineIndex) - PosInLine + 1
        End If
    End If
End Function

'-----------------------------------------------------------------------
'Qtd    - quantidade de linhas
'-----------------------------------------------------------------------
Property Get Qtd() As Long
    Qtd = LinesCounter
End Property

'-----------------------------------------------------------------------
'Qtd    - set quantidade de linhas
'-----------------------------------------------------------------------
Property Let Qtd(Value As Long)
    LinesCounter = Value
    ReDim Preserve Lines(Value)
    ReDim Preserve LinesLen(Value)
End Property

'-----------------------------------------------------------------------
'InString   - verifica se existe alguma substring num determinado intervalo
'Row1 - posição da linha inicial
'Col1 - posição da coluna inicial
'Row2 - posição da linha final
'Col2 - posição da coluna final
'substr - substring
'PosRow - posição da substring na linha
'PosCol - posição da substring na coluna
'-----------------------------------------------------------------------
Sub InString(Row1 As Long, Col1 As Long, Row2 As Long, Col2 As Long, substr As String, PosRow As Long, PosCol As Long, compare As VbCompareMethod)
    Dim aux1() As String
    Dim aux2() As String
    Dim SubstrLen As Long
    Dim i As Long
    Dim j As Long
    Dim CurrLine As String
    Dim NextLine As String
    Dim NextLineRow As Long
    Dim t As String
        
        
    PosRow = Row1 - 1
    PosCol = 0
    
    If (Row2 > LinesCounter) Or ((Row2 = LinesCounter) And (Col2 > LinesLen(LinesCounter))) Then
    
    Else
        
        If Col1 = 0 Then
            j = 1
        Else
            j = Col1
        End If
        
        SubstrLen = Len(substr)
    
        ReDim Preserve aux1(SubstrLen)
        ReDim Preserve aux2(SubstrLen)
        For i = 1 To SubstrLen
            aux1(i) = Mid(substr, 1, i)
            aux2(i) = Mid(substr, i + 1)
        Next
        While (PosRow < Row2) And (PosCol = 0)
            PosRow = PosRow + 1
            'Debug.Print "instring-CurrLine(" + CStr(PosRow) + ")=" + Lines(PosRow)
            If PosRow < Row2 Then
                CurrLine = Mid(Lines(PosRow), j)
            Else
                CurrLine = Mid(Lines(PosRow), j, Col2 - j + 1)
            End If
            
            If Len(CurrLine) > 0 Then
                i = SubstrLen + 1
                While (PosCol = 0) And (i > 1)
                    i = i - 1
                    PosCol = InStr(1, CurrLine, aux1(i), compare)
                    If PosCol > 0 Then
                        If Len(aux1(i)) < SubstrLen Then
                            If (PosCol = (Len(CurrLine) - Len(aux1(i)) + 1)) Then
                                If PosRow = Row2 Then
                                    PosCol = 0
                                Else
                                    'em linhas diferentes, considerar que pode haver linha em branco
                                    NextLineRow = PosRow + 1
                                    NextLine = Trim(Lines(NextLineRow))
                                    While (Len(NextLine) = 0) And (NextLineRow < LinesCounter)
                                      NextLineRow = NextLineRow + 1
                                      NextLine = Trim(Lines(NextLineRow))
                                    Wend
                                    
                                    If InStr(1, Lines(NextLineRow), aux2(i), compare) <> 1 Then
                                      PosCol = 0
                                    End If
                                End If
                            Else
                                PosCol = 0
                            End If
                        End If
                    End If
                Wend
            End If
            j = 1
        Wend
    End If
    
    If (PosCol > 0) And (PosRow = Row1) Then PosCol = PosCol + Col1 - 1
End Sub

'-----------------------------------------------------------------------
'New_InString   - verifica se existe alguma substring num determinado intervalo
'Row1 - posição da linha inicial
'Col1 - posição da coluna inicial
'Row2 - posição da linha final
'Col2 - posição da coluna final
'substr - substring
'PosRow - posição da substring na linha
'PosCol - posição da substring na coluna
'-----------------------------------------------------------------------
Sub New_InString(Row1 As Long, Col1 As Long, Row2 As Long, Col2 As Long, substr As String, row As Long, col As Long, comp As VbCompareMethod)
    Dim i As Long
    Dim Found2 As TpPosition
    Dim finish2 As TpPosition
    Dim start2 As TpPosition
    
    Dim start As TpPosition
    Dim finish As TpPosition
    Dim pfound As TpPosition
    
    Dim found As Boolean
    Dim lensubstr As Long
    Dim substring As String
    
    Dim checkstring As String
    
    start.i = Row1
    start.j = Col1
    finish.i = Row2
    finish.j = Col2
    lensubstr = 2
    row = 0
        
    While (Not found) And (ExisteStr(start.i, start.j, finish.i, finish.j))
        i = 1
        substring = Mid(substr, i, lensubstr)
        Call InString(start.i, start.j, finish.i, finish.j, substring, pfound.i, pfound.j, comp)
        
        Found2 = pfound
        If pfound.j > 0 Then
            
            While (Found2.j > 0) And ((i + Len(substring)) <= Len(substr))
                
                start2 = Found2
                Call ForwardPosition(start2.i, start2.j, Len(substring))
                
                i = i + Len(substring)
                substring = Mid(substr, i, lensubstr)
                                
                Debug.Print "substring " + substring
                Debug.Print "start2 String " + Mid(GetLine(start2.i), start2.j)
                Debug.Print "start2 " + CStr(start2.i) + ", " + CStr(start2.j)
                
                
                Call InString(start2.i, start2.j, finish.i, finish.j, substring, Found2.i, Found2.j, comp)
                
                checkstring = Trim(GetSubstrRange(start2.i, start2.j, Found2.i, Found2.j))
                If Len(checkstring) > 1 Then
                    Found2.j = 0
                End If
                Debug.Print "Found2 " + CStr(Found2.i) + ", " + CStr(Found2.j)
            Wend
            If Found2.j = 0 Then
                start = start2
            Else
                found = True
            End If
        Else
            start = finish
            Call ForwardPosition(start.i, start.j, 1)
        End If
    Wend
    If Found2.j > 0 Then
        row = pfound.i
        col = pfound.j
    Else
        col = 0
    End If
    Debug.Print '------'
End Sub

'-----------------------------------------------------------------------
'New_InString   - verifica se existe alguma substring num determinado intervalo
'Row1 - posição da linha inicial
'Col1 - posição da coluna inicial
'Row2 - posição da linha final
'Col2 - posição da coluna final
'substr - substring
'PosRow - posição da substring na linha
'PosCol - posição da substring na coluna
'-----------------------------------------------------------------------
Sub Old_New_InString(Row1 As Long, Col1 As Long, Row2 As Long, Col2 As Long, substr As String, row As Long, col As Long, comp As VbCompareMethod)
    Dim i As Long
    Dim pNext As TpPosition
    Dim start As TpPosition
    Dim finish As TpPosition
    Dim PartialFinish As TpPosition
    Dim first As TpPosition
    Dim curr As TpPosition
    Dim found As Boolean
    Dim lensubstr As Long
    Dim substring As String
    
    start.i = Row1
    start.j = Col1
    finish.i = Row2
    finish.j = Col2
    lensubstr = 2
    row = 0
        
    While (Not found) And (ExisteStr(start.i, start.j, finish.i, finish.j))
        i = 1
        substring = Mid(substr, i, lensubstr)
        
        Call InString(start.i, start.j, finish.i, finish.j, substring, first.i, first.j, comp)
    
        If first.j > 0 Then
            pNext = first
            curr = first
        
            While (curr.i = pNext.i) And (curr.j = pNext.j) And ((i + Len(substring)) <= Len(substr))
                Call ForwardPosition(curr.i, curr.j, Len(substring))
                
                i = i + Len(substring)
                substring = Mid(substr, i, lensubstr)
                
                PartialFinish = curr
                Call ForwardPosition(PartialFinish.i, PartialFinish.j, Len(substring))
                
                Debug.Print "substring " + substring
                Debug.Print "Curr String " + Mid(GetLine(curr.i), curr.j)
                Debug.Print "curr " + CStr(curr.i) + ", " + CStr(curr.j)
                
                
                Call InString(curr.i, curr.j, PartialFinish.i, PartialFinish.j, substring, pNext.i, pNext.j, comp)
                
                Debug.Print "pNext " + CStr(pNext.i) + ", " + CStr(pNext.j)
                                
            Wend
            
            
            If (curr.i = pNext.i) And (curr.j = pNext.j) And ((i + Len(substring)) > Len(substr)) Then
                found = True
            Else
                start = first
                Call ForwardPosition(start.i, start.j, 1)
            End If
        Else
            start = finish
            Call ForwardPosition(start.i, start.j, 1)
        End If
    Wend
    If found Then
        row = first.i
        col = first.j
    Else
        col = 0
    End If
    Debug.Print '------'
End Sub

'-----------------------------------------------------------------------
'GetPartialCopy   - obtém cópia parcial da classe
'Row1 - posição da linha inicial
'Col1 - posição da coluna inicial
'Row2 - posição da linha final
'Col2 - posição da coluna final
'retorno    - instância da cltxt
'-----------------------------------------------------------------------
Function GetPartialCopy(Row1 As Long, Col1 As Long, Row2 As Long, Col2 As Long) As ClTxt
    Dim aux As ClTxt
    Dim i As Long
    
    Set aux = New ClTxt
    If (Row1 > 0) And (Col1 > 0) And (Row2 > 0) And (Col2 > 0) Then
        If Row2 > Qtd Then Row2 = Qtd
        If (Row2 = Qtd) And (Col2 > LinesLen(Qtd)) Then Col2 = LinesLen(Qtd)
        If Row1 < Row2 Then
            aux.AddLines (Mid(Lines(Row1), Col1))
            i = Row1 + 1
            While (i < Row2)
                aux.AddLines (Lines(i))
                i = i + 1
            Wend
            aux.AddLines (Mid(Lines(i), 1, Col2))
        ElseIf Row1 = Row2 Then
            If Col1 <= Col2 Then
                aux.AddLines (Mid(Lines(Row1), Col1, Col2 - Col1 + 1))
            Else
                aux.Delete
            End If
        Else
            aux.Delete
        End If
    End If
    Set GetPartialCopy = aux
End Function

'-----------------------------------------------------------------------
'GetCopy    - obtém cópia da classe
'Row1 - posição da linha inicial
'Col1 - posição da coluna inicial
'Row2 - posição da linha final
'Col2 - posição da coluna final
'retorno    - instância da cltxt
'-----------------------------------------------------------------------
Function GetCopy() As ClTxt
    Dim aux As New ClTxt
    Dim i As Long
    For i = 1 To LinesCounter
        aux.AddLines (Lines(i))
    Next
    Set GetCopy = aux
End Function

'-----------------------------------------------------------------------
'GetSubstrRange - obtém substring de um intervalo
'Row1 - posição da linha inicial
'Col1 - posição da coluna inicial
'Row2 - posição da linha final
'Col2 - posição da coluna final
'sep    - separador
'retorno    - instância da cltxt
'-----------------------------------------------------------------------
Function GetSubstrRange(ByVal Row1 As Long, ByVal Col1 As Long, ByVal Row2 As Long, ByVal Col2 As Long) As String
    Dim aux As String
    Dim aux1 As String
    Dim aux2 As New ClTxt
    Dim i As Long
    Dim separador As String
    Dim last As String
    Dim first As String
    
    Set aux2 = GetPartialCopy(Row1, Col1, Row2, Col2)
    
    For i = 1 To aux2.Qtd
        aux = aux + aux2.GetLine(i)
    Next
    
    GetSubstrRange = aux
End Function

'-----------------------------------------------------------------------
'ReplaceEntitybySpaces - replace entities html by spaces
'ASCIIList - list of the entities to convert
'Return - the new ClTxt
'-----------------------------------------------------------------------
Function ReplaceEntitybySpaces(ASCIIList As ClSortList) As ClTxt
    Dim result As ClTxt
    Dim Change As String
    Dim first As TpPosition
    Dim last As TpPosition
    Dim p1 As TpPosition
    Dim p2 As TpPosition
    Dim P3 As TpPosition
    Dim P4 As TpPosition
    Dim code As String
    Dim i As Long
    Dim BeginPos As TpPosition
    Dim EndPos As TpPosition
    Dim EntityEnd(3) As String
    Dim entity As String
    
    EntityEnd(1) = ";"
    EntityEnd(2) = Chr(32)
    EntityEnd(3) = "&"
    
    Set result = New ClTxt
    
    first.i = 1
    first.j = 1
    
    Call GetEnd(last.i, last.j)
    While ExisteStr(first.i, first.j, last.i, last.j)
        
        code = ""
        Call InString(first.i, first.j, last.i, last.j, "&", p1.i, p1.j, vbTextCompare)
        If p1.j > 0 Then
            i = 0
            P3.i = 0
            P3.j = 0
            p2 = P3
            P4 = last
            While (P4.j > 0) And (i < 3)
                i = i + 1
                p2 = P3
                Call InString(p1.i, p1.j, P4.i, P4.j, EntityEnd(i), P3.i, P3.j, vbTextCompare)
                P4 = P3
            Wend
            
            If p2.j > 0 Then
                entity = GetSubstrRange(p1.i, p1.j, p2.i, p2.j)
                If Len(entity) > 0 Then code = Mid(entity, 2, Len(entity) - 2)
                If InStr(entity, ";") = 0 Then entity = Mid(entity, 1, Len(entity) - 1)
                If Len(code) > 0 Then
                    If ASCIIList.exist(code) Then
                        BeginPos = first
                        EndPos = p1
                        Change = Space(Len(entity))
                        first = p2
                    ElseIf code Like "[#]" + String(Len(code) - 1, "#") Then
                        BeginPos = first
                        EndPos = p1
                        Change = Space(Len(entity))
                        first = p2
                    Else
                        BeginPos = first
                        EndPos = p2
                        Call ForwardPosition(EndPos.i, EndPos.j, 1)
                        Change = ""
                        first = p2
                    End If
                Else
                    BeginPos = first
                    EndPos = p2
                    Call ForwardPosition(EndPos.i, EndPos.j, 1)
                    Change = ""
                    first = p2
                End If
            ElseIf p2.j = 0 Then
                BeginPos = first
                EndPos = last
                first = last
                Change = ""
            End If
        ElseIf p1.j = 0 Then
            BeginPos = first
            EndPos = last
            first = last
            Change = ""
        End If
    
        If (EndPos.i = 1) And (EndPos.j = 1) Then
            EndPos.j = 0
        Else
            Call RewardPosition(EndPos.i, EndPos.j, 1)
        End If
            
        If BeginPos.i = EndPos.i Then
            result.SetLine(BeginPos.i) = result.GetLine(BeginPos.i) + GetSubstrInRow(BeginPos.i, BeginPos.j, EndPos.j + 1 - BeginPos.j) + Change
        ElseIf BeginPos.i < EndPos.i Then
            result.SetLine(BeginPos.i) = result.GetLine(BeginPos.i) + GetSubstrInRow(BeginPos.i, BeginPos.j, GetLineLen(BeginPos.i))
            For i = BeginPos.i + 1 To EndPos.i - 1
                result.SetLine(i) = GetLine(i)
            Next
            result.SetLine(EndPos.i) = GetSubstrInRow(EndPos.i, 1, EndPos.j) + Change
        Else
            result.SetLine(BeginPos.i) = result.GetLine(BeginPos.i) + Change
        End If
        Call ForwardPosition(first.i, first.j, 1)
    Wend
    
    Set ReplaceEntitybySpaces = result

End Function

'-----------------------------------------------------------------------
'ReplaceEntitybySpaces2 - replace entities html by spaces
'ASCIIList - list of the entities to convert
'Return - the new ClTxt
'-----------------------------------------------------------------------
Function ReplaceEntitybySpaces2(ASCIIList As ClSortList) As ClTxt
    Dim result As ClTxt
    Dim Change As String
    Dim first As TpPosition
    Dim last As TpPosition
    Dim p1 As TpPosition
    Dim p2 As TpPosition
    Dim P3 As TpPosition
    Dim P4 As TpPosition
    Dim code As String
    Dim i As Long
    Dim BeginPos As TpPosition
    Dim EndPos As TpPosition
    Dim EntityEnd(3) As String
    Dim entity As String
    
    EntityEnd(1) = ";"
    EntityEnd(2) = Chr(32)
    EntityEnd(3) = "&"
    
    Set result = New ClTxt
    
    first.i = 1
    first.j = 1
    
    Call GetEnd(last.i, last.j)
    While ExisteStr(first.i, first.j, last.i, last.j)
        
        code = ""
        Call InString(first.i, first.j, last.i, last.j, "&", p1.i, p1.j, vbTextCompare)
        If p1.j > 0 Then
            i = 0
            P3.i = 0
            P3.j = 0
            p2 = P3
            P4 = last
            While (P4.j > 0) And (i < 3)
                i = i + 1
                p2 = P3
                Call InString(p1.i, p1.j, P4.i, P4.j, EntityEnd(i), P3.i, P3.j, vbTextCompare)
                P4 = P3
            Wend
            
            If p2.j > 0 Then
                entity = GetSubstrRange(p1.i, p1.j, p2.i, p2.j)
                If Len(entity) > 0 Then code = Mid(entity, 2, Len(entity) - 2)
                If InStr(entity, ";") = 0 Then entity = Mid(entity, 1, Len(entity) - 1)
                If Len(code) > 0 Then
                    If ASCIIList.exist(code) Then
                        BeginPos = first
                        EndPos = p1
                        Change = Space(Len(entity))
                        first = p2
                    ElseIf code Like "[#]" + String(Len(code) - 1, "#") Then
                        BeginPos = first
                        EndPos = p1
                        Change = Space(Len(entity))
                        first = p2
                    Else
                        BeginPos = first
                        EndPos = p2
                        Call ForwardPosition(EndPos.i, EndPos.j, 1)
                        Change = ""
                        first = p2
                    End If
                Else
                    BeginPos = first
                    EndPos = p2
                    Call ForwardPosition(EndPos.i, EndPos.j, 1)
                    Change = ""
                    first = p2
                End If
            ElseIf p2.j = 0 Then
                BeginPos = first
                EndPos = last
                first = last
                Change = ""
            End If
        ElseIf p1.j = 0 Then
            BeginPos = first
            EndPos = last
            first = last
            Change = ""
        End If
    
        If (EndPos.i = 1) And (EndPos.j = 1) Then
            EndPos.j = 0
        Else
            Call RewardPosition(EndPos.i, EndPos.j, 1)
        End If
            
        If BeginPos.i = EndPos.i Then
            result.SetLine(BeginPos.i) = result.GetLine(BeginPos.i) + GetSubstrInRow(BeginPos.i, BeginPos.j, EndPos.j + 1 - BeginPos.j) + Change
        ElseIf BeginPos.i < EndPos.i Then
            result.SetLine(BeginPos.i) = result.GetLine(BeginPos.i) + GetSubstrInRow(BeginPos.i, BeginPos.j, GetLineLen(BeginPos.i))
            For i = BeginPos.i + 1 To EndPos.i - 1
                result.SetLine(i) = GetLine(i)
            Next
            result.SetLine(EndPos.i) = GetSubstrInRow(EndPos.i, 1, EndPos.j) + Change
        Else
            result.SetLine(BeginPos.i) = result.GetLine(BeginPos.i) + Change
        End If
        Call ForwardPosition(first.i, first.j, 1)
    Wend
    
    Set ReplaceEntitybySpaces2 = result

End Function

'-----------------------------------------------------------------------
'ReplaceAllHTMLbySpaces - replace all html tags by spaces
'Return - the new ClTxt
'-----------------------------------------------------------------------
Function ReplaceAllHTMLbySpaces() As ClTxt
    Dim result As ClTxt
    Dim first As TpPosition
    Dim last As TpPosition
    Dim P As TpPosition
    Dim p1 As TpPosition
    Dim p2 As TpPosition
    Dim P3 As TpPosition
    Dim HTMLTag As String
    Dim i As Long
    Dim BeginPos As TpPosition
    Dim EndPos As TpPosition
    
    Set result = New ClTxt
    
    first.i = 1
    first.j = 1
   
    Call GetEnd(last.i, last.j)
    While ExisteStr(first.i, first.j, last.i, last.j)
        Call InString(first.i, first.j, last.i, last.j, "<", p1.i, p1.j, vbBinaryCompare)
        If p1.j > 0 Then
            Call InString(p1.i, p1.j, last.i, last.j, ">", p2.i, p2.j, vbBinaryCompare)
            If p2.j > 0 Then
                
                HTMLTag = GetSubstrRange(p1.i, p1.j, p2.i, p2.j)
                If Len(HTMLTag) > 2 Then
                    Debug.Print HTMLTag
                    P = p1
                    Call ForwardPosition(P.i, P.j, 1)
                    Call InString(P.i, P.j, p2.i, p2.j, "<", P3.i, P3.j, vbBinaryCompare)
            
                    While (P3.j > 0) And (((P3.i = p2.i) And (P3.j < p2.j)) Or (p2.i > P3.i))
                        P = P3
                        p1 = P3
                        Call ForwardPosition(P.i, P.j, 1)
                        Call InString(P.i, P.j, p2.i, p2.j, "<", P3.i, P3.j, vbBinaryCompare)
                    Wend
                    
                    If InStr(1, HTMLTag, "face=" + Chr(34) + "symbol" + Chr(34), vbTextCompare) > 0 Then
                        P3 = p2
                        Call ForwardPosition(P3.i, P3.j, 1)
                        Call InString(P3.i, P3.j, last.i, last.j, ">", p2.i, p2.j, vbBinaryCompare)
                    End If
            
                    BeginPos = first
                    EndPos = p1
                    first = p2
                Else
                    'foi encontrado <>
                    BeginPos = first
                    EndPos = p2
                    first = p2
                    'Call RewardPosition(First.i, First.j, 1)
                End If
            Else
                'encontrou <, mas nao >
                BeginPos = first
                EndPos = last
                first = last
            End If
        Else 'foi encontrado > antes de <
            BeginPos = first
            EndPos = last
            first = last
        End If
    
    
        If (EndPos.i = 1) And (EndPos.j = 1) Then
            EndPos.j = 0
        Else
            Call RewardPosition(EndPos.i, EndPos.j, 1)
        End If
            
        If (BeginPos.i = EndPos.i) Then
            result.SetLine(BeginPos.i) = result.GetLine(BeginPos.i) + GetSubstrInRow(BeginPos.i, BeginPos.j, EndPos.j + 1 - BeginPos.j)
        ElseIf (BeginPos.i < EndPos.i) Then
            result.SetLine(BeginPos.i) = result.GetLine(BeginPos.i) + GetSubstrInRow(BeginPos.i, BeginPos.j, GetLineLen(BeginPos.i))
            For i = BeginPos.i + 1 To EndPos.i - 1
                result.SetLine(i) = result.GetLine(i) + GetLine(i)
            Next
            result.SetLine(EndPos.i) = result.GetLine(EndPos.i) + GetSubstrInRow(EndPos.i, 1, EndPos.j)
        End If
                        
        If Len(HTMLTag) > 0 Then
            If p1.i = p2.i Then
                result.SetLine(p1.i) = result.GetLine(p1.i) + Space(p2.j + 1 - p1.j)
            ElseIf (p1.i < p2.i) Then
                result.SetLine(p1.i) = result.GetLine(p1.i) + Space(GetLineLen(p1.i) - p1.j)
                For i = p1.i + 1 To p2.i - 1
                    result.SetLine(i) = Space(GetLineLen(i))
                Next
                result.SetLine(p2.i) = Space(p2.j)
            End If
        End If
        Call ForwardPosition(first.i, first.j, 1)
    Wend
       
    Set ReplaceAllHTMLbySpaces = result
End Function

'-----------------------------------------------------------------------
'CheckErrorinMarkupTag - replace all html tags by spaces
'Return - the new ClTxt
'-----------------------------------------------------------------------
Function CheckErrorinMarkupTag() As Long
    Dim result As Long
    Dim first As TpPosition
    Dim last As TpPosition
    Dim P As TpPosition
    Dim p1 As TpPosition
    Dim p2 As TpPosition
    Dim P3 As TpPosition
    Dim MarkupTag As String
    Dim maux As String
    Dim i As Long
    Dim BeginPos As TpPosition
    Dim EndPos As TpPosition
    
    
    first.i = 1
    first.j = 1
   
    Call GetEnd(last.i, last.j)
    While ExisteStr(first.i, first.j, last.i, last.j)
        Call InString(first.i, first.j, last.i, last.j, "[", p1.i, p1.j, vbBinaryCompare)
        If p1.j > 0 Then
            Call InString(p1.i, p1.j, last.i, last.j, "]", p2.i, p2.j, vbBinaryCompare)
            If p2.j > 0 Then
                
                MarkupTag = GetSubstrRange(p1.i, p1.j, p2.i, p2.j)
                If Len(MarkupTag) > 2 Then
                    
                    P = p1
                    Call ForwardPosition(P.i, P.j, 1)
                    Call InString(P.i, P.j, p2.i, p2.j, "[", P3.i, P3.j, vbBinaryCompare)
            
                    While (P3.j > 0) And (((P3.i = p2.i) And (P3.j < p2.j)) Or (p2.i > P3.i))
                        P = P3
                        Debug.Print P3.i, P3.j
                        p1 = P3
                        Call ForwardPosition(P.i, P.j, 1)
                        Call InString(P.i, P.j, p2.i, p2.j, "[", P3.i, P3.j, vbBinaryCompare)
                    Wend
                    Debug.Print p1.i, p1.j
                    
                    MarkupTag = GetSubstrRange(p1.i, p1.j, p2.i, p2.j)
                    maux = RmAllHTML(MarkupTag)
                    If StrComp(maux, MarkupTag, vbBinaryCompare) <> 0 Then
                        Msg.GiveRunInformation (InterfaceLabels("MsgDirtyTag").elem2 & MarkupTag)
                        result = result + 1
                    End If
                    
                    '-- If InStr(1, MarkupTag, "face=" + Chr(34) + "symbol" + Chr(34), vbTextCompare) > 0 Then
                    '--     P3 = p2
                        '-- Call ForwardPosition(P3.i, P3.j, 1)
                        '-- Call InString(P3.i, P3.j, last.i, last.j, ">", p2.i, p2.j, vbBinaryCompare)
                    '-- End If
            
                    BeginPos = first
                    EndPos = p1
                    first = p2
                Else
                    'foi encontrado <>
                    BeginPos = first
                    EndPos = p2
                    first = p2
                    'Call RewardPosition(First.i, First.j, 1)
                End If
            Else
                'encontrou [, mas nao >
                BeginPos = first
                EndPos = last
                first = last
            End If
        Else 'foi encontrado > antes de [
            BeginPos = first
            EndPos = last
            first = last
        End If
    
    
        If (EndPos.i = 1) And (EndPos.j = 1) Then
            EndPos.j = 0
        Else
            Call RewardPosition(EndPos.i, EndPos.j, 1)
        End If
            
        '-- If (BeginPos.i = EndPos.i) Then
            '-- Result.SetLine(BeginPos.i) = Result.GetLine(BeginPos.i) + GetSubstrInRow(BeginPos.i, BeginPos.j, EndPos.j + 1 - BeginPos.j)
        '-- ElseIf (BeginPos.i < EndPos.i) Then
            '-- Result.SetLine(BeginPos.i) = Result.GetLine(BeginPos.i) + GetSubstrInRow(BeginPos.i, BeginPos.j, GetLineLen(BeginPos.i))
            '-- for i = BeginPos.i + 1 To EndPos.i - 1
                '-- Result.SetLine(i) = Result.GetLine(i) + GetLine(i)
            '-- Next
            '-- Result.SetLine(EndPos.i) = Result.GetLine(EndPos.i) + GetSubstrInRow(EndPos.i, 1, EndPos.j)
        '-- End If
                        
        '-- If Len(MarkupTag) > 0 Then
            '-- If P1.i = p2.i Then
                '-- Result.SetLine(P1.i) = Result.GetLine(P1.i) + MarkupTag 'Space(p2.j + 1 - P1.j)
            '-- ElseIf (P1.i < p2.i) Then
                '-- Result.SetLine(P1.i) = Result.GetLine(P1.i) + MarkupTag ' Space(GetLineLen(P1.i) - P1.j)
                '-- for i = P1.i + 1 To p2.i - 1
                    '-- Result.SetLine(i) = Space(GetLineLen(i))
                '-- Next
                '-- Result.SetLine(p2.i) = Space(p2.j)
            '-- End If
        '-- End If
        Call ForwardPosition(first.i, first.j, 1)
    Wend
       
    'Set CheckErrorinMarkupTag = Result
    CheckErrorinMarkupTag = result
End Function


Sub Insert_igntag(UnclosedTags As ColPair)
    Dim Index As Long
    
    Dim pContinue As TpPosition
    Dim last As TpPosition
    Dim P As TpPosition
    Dim pUnclosedTag As TpPosition
    Dim pOpenIGNtag As TpPosition
    Dim pCloseIGNtag As TpPosition
    Dim igncontent As String
    Dim i As Long
    Dim pStop As TpPosition
    
    Const igntag1 = "[ign]"
    Const igntag2 = "[/ign]"
    
    For Index = 1 To UnclosedTags.Count
        pContinue.i = 1
        pContinue.j = 1
        
        Call GetEnd(last.i, last.j)
        While ExisteStr(pContinue.i, pContinue.j, last.i, last.j)
            igncontent = ""
            Call InString(pContinue.i, pContinue.j, last.i, last.j, "[" & UnclosedTags(Index).elem1, pUnclosedTag.i, pUnclosedTag.j, vbBinaryCompare)
            If pUnclosedTag.j > 0 Then
                Call InString(pUnclosedTag.i, pUnclosedTag.j, last.i, last.j, "]", pOpenIGNtag.i, pOpenIGNtag.j, vbBinaryCompare)
                If pOpenIGNtag.j > 0 Then
                    pStop = pOpenIGNtag
                    
                    Call ForwardPosition(pOpenIGNtag.i, pOpenIGNtag.j, 1)
                    Call InString(pOpenIGNtag.i, pOpenIGNtag.j, last.i, last.j, "[", pCloseIGNtag.i, pCloseIGNtag.j, vbBinaryCompare)
                    If pCloseIGNtag.j > 0 Then
                        pContinue = pCloseIGNtag
                        Call RewardPosition(pCloseIGNtag.i, pCloseIGNtag.j, 1)
                    Else
                        pCloseIGNtag = last
                        pContinue = last
                        Call ForwardPosition(pContinue.i, pContinue.j, 1)
                    End If
                    
                    igncontent = GetSubstrRange(pOpenIGNtag.i, pOpenIGNtag.j, pCloseIGNtag.i, pCloseIGNtag.j)
                    If Len(igncontent) > 0 Then Call ForwardPosition(pContinue.i, pContinue.j, Len(igntag1) + Len(igntag2))
                Else
                    'encontrou [, mas nao encontrou ]
                    pContinue = last
                    Call ForwardPosition(pContinue.i, pContinue.j, 1)
                End If
            Else
                'esta tag nao foi encontrada
                pContinue = last
                Call ForwardPosition(pContinue.i, pContinue.j, 1)
            End If
        
            If Len(igncontent) > 0 Then
                If pStop.i = pOpenIGNtag.i Then
                    If pOpenIGNtag.i = pCloseIGNtag.i Then
                        If pCloseIGNtag.i = pContinue.i Then
                            SetLine(pOpenIGNtag.i) = GetSubstrRange(pStop.i, 1, pStop.i, pStop.j) + GetSubstrInRow(pContinue.i, pContinue.j, GetLineLen(pContinue.i))
                        ElseIf pCloseIGNtag.i < pContinue.i Then
                            SetLine(pOpenIGNtag.i) = GetSubstrRange(pStop.i, 1, pStop.i, pStop.j)
                        End If
                    ElseIf pOpenIGNtag.i < pCloseIGNtag.i Then
                        SetLine(pOpenIGNtag.i) = GetSubstrRange(pStop.i, 1, pStop.i, pStop.j)
                        For i = pOpenIGNtag.i + 1 To pCloseIGNtag.i - 1
                            SetLine(i) = ""
                        Next
                        If pCloseIGNtag.i = pContinue.i Then
                            SetLine(pCloseIGNtag.i) = GetSubstrInRow(pContinue.i, pContinue.j, GetLineLen(pContinue.i))
                        ElseIf pCloseIGNtag.i < pContinue.i Then
                            SetLine(pCloseIGNtag.i) = ""
                        End If
                    End If
                ElseIf pStop.i < pOpenIGNtag.i Then
                    If pOpenIGNtag.i = pCloseIGNtag.i Then
                        If pCloseIGNtag.i = pContinue.i Then
                            SetLine(pOpenIGNtag.i) = GetSubstrInRow(pContinue.i, pContinue.j, GetLineLen(pContinue.i))
                        ElseIf pCloseIGNtag.i < pContinue.i Then
                            SetLine(pOpenIGNtag.i) = ""
                        End If
                    ElseIf pOpenIGNtag.i < pCloseIGNtag.i Then
                        SetLine(pOpenIGNtag.i) = ""
                        For i = pOpenIGNtag.i + 1 To pCloseIGNtag.i - 1
                            SetLine(i) = ""
                        Next
                        If pCloseIGNtag.i = pContinue.i Then
                            SetLine(pCloseIGNtag.i) = GetSubstrInRow(pContinue.i, pContinue.j, GetLineLen(pContinue.i))
                        ElseIf pCloseIGNtag.i < pContinue.i Then
                            SetLine(pCloseIGNtag.i) = ""
                        End If
                    End If
                End If
            End If
        Wend
    Next
End Sub
Sub Old_Insert_igntag(UnclosedTags As ColPair)
    Dim Index As Long
    
    Dim pContinue As TpPosition
    Dim last As TpPosition
    Dim P As TpPosition
    Dim pUnclosedTag As TpPosition
    Dim pOpenIGNtag As TpPosition
    Dim pCloseIGNtag As TpPosition
    Dim igncontent As String
    Dim i As Long
    Dim pStop As TpPosition
    
    Const igntag1 = "[ign]"
    Const igntag2 = "[/ign]"
    
    For Index = 1 To UnclosedTags.Count
        pContinue.i = 1
        pContinue.j = 1
        
        Call GetEnd(last.i, last.j)
        While ExisteStr(pContinue.i, pContinue.j, last.i, last.j)
            igncontent = ""
            Call InString(pContinue.i, pContinue.j, last.i, last.j, "[" & UnclosedTags(Index).elem1, pUnclosedTag.i, pUnclosedTag.j, vbBinaryCompare)
            If pUnclosedTag.j > 0 Then
                Call InString(pUnclosedTag.i, pUnclosedTag.j, last.i, last.j, "]", pOpenIGNtag.i, pOpenIGNtag.j, vbBinaryCompare)
                If pOpenIGNtag.j > 0 Then
                    pStop = pOpenIGNtag
                    
                    Call ForwardPosition(pOpenIGNtag.i, pOpenIGNtag.j, 1)
                    Call InString(pOpenIGNtag.i, pOpenIGNtag.j, last.i, last.j, "[", pCloseIGNtag.i, pCloseIGNtag.j, vbBinaryCompare)
                    If pCloseIGNtag.j > 0 Then
                        pContinue = pCloseIGNtag
                        Call RewardPosition(pCloseIGNtag.i, pCloseIGNtag.j, 1)
                    Else
                        pCloseIGNtag = last
                        pContinue = last
                        Call ForwardPosition(pContinue.i, pContinue.j, 1)
                    End If
                    
                    igncontent = GetSubstrRange(pOpenIGNtag.i, pOpenIGNtag.j, pCloseIGNtag.i, pCloseIGNtag.j)
                    If Len(igncontent) > 0 Then Call ForwardPosition(pContinue.i, pContinue.j, Len(igntag1) + Len(igntag2))
                Else
                    'encontrou [, mas nao encontrou ]
                    pContinue = last
                    Call ForwardPosition(pContinue.i, pContinue.j, 1)
                End If
            Else
                'esta tag nao foi encontrada
                pContinue = last
                Call ForwardPosition(pContinue.i, pContinue.j, 1)
            End If
        
            If Len(igncontent) > 0 Then
                If pStop.i = pOpenIGNtag.i Then
                    If pOpenIGNtag.i = pCloseIGNtag.i Then
                        If pCloseIGNtag.i = pContinue.i Then
                            SetLine(pOpenIGNtag.i) = GetSubstrRange(pStop.i, 1, pStop.i, pStop.j) + igntag1 + igncontent + igntag2 + GetSubstrInRow(pContinue.i, pContinue.j, GetLineLen(pContinue.i))
                        ElseIf pCloseIGNtag.i < pContinue.i Then
                            SetLine(pOpenIGNtag.i) = GetSubstrRange(pStop.i, 1, pStop.i, pStop.j) + igntag1 + igncontent + igntag2
                        End If
                    ElseIf pOpenIGNtag.i < pCloseIGNtag.i Then
                        SetLine(pOpenIGNtag.i) = GetSubstrRange(pStop.i, 1, pStop.i, pStop.j) + igntag1 + GetSubstrInRow(pOpenIGNtag.i, pOpenIGNtag.j, GetLineLen(pOpenIGNtag.i))
                        If pCloseIGNtag.i = pContinue.i Then
                            SetLine(pCloseIGNtag.i) = GetSubstrRange(pCloseIGNtag.i, 1, pCloseIGNtag.i, pCloseIGNtag.j) + igntag2 + GetSubstrInRow(pContinue.i, pContinue.j, GetLineLen(pContinue.i))
                        ElseIf pCloseIGNtag.i < pContinue.i Then
                            SetLine(pCloseIGNtag.i) = GetLine(pCloseIGNtag.i) + igntag2
                        End If
                    End If
                ElseIf pStop.i < pOpenIGNtag.i Then
                    If pOpenIGNtag.i = pCloseIGNtag.i Then
                        If pCloseIGNtag.i = pContinue.i Then
                            SetLine(pOpenIGNtag.i) = igntag1 + igncontent + igntag2 + GetSubstrInRow(pContinue.i, pContinue.j, GetLineLen(pContinue.i))
                        ElseIf pCloseIGNtag.i < pContinue.i Then
                            SetLine(pOpenIGNtag.i) = igntag1 + igncontent + igntag2
                        End If
                    ElseIf pOpenIGNtag.i < pCloseIGNtag.i Then
                        SetLine(pOpenIGNtag.i) = igntag1 + GetSubstrInRow(pOpenIGNtag.i, pOpenIGNtag.j, GetLineLen(pOpenIGNtag.i))
                        If pCloseIGNtag.i = pContinue.i Then
                            SetLine(pCloseIGNtag.i) = GetSubstrRange(pCloseIGNtag.i, 1, pCloseIGNtag.i, pCloseIGNtag.j) + igntag2 + GetSubstrInRow(pContinue.i, pContinue.j, GetLineLen(pContinue.i))
                        ElseIf pCloseIGNtag.i < pContinue.i Then
                            SetLine(pCloseIGNtag.i) = GetLine(pCloseIGNtag.i) + igntag2
                        End If
                    End If
                End If
            End If
        Wend
    Next
End Sub
Sub Insert_igntag2(UnclosedTags As ColPair)
    Dim Index As Long
    
    Dim pContinue As TpPosition
    Dim last As TpPosition
    Dim P As TpPosition
    Dim pUnclosedTag As TpPosition
    Dim pOpenIGNtag As TpPosition
    Dim pCloseIGNtag As TpPosition
    Dim igncontent As String
    Dim i As Long
    Dim pStop As TpPosition
    
    Const igntag1 = "[ign]"
    Const igntag2 = "[/ign]"
    
    For Index = 1 To UnclosedTags.Count
        pContinue.i = 1
        pContinue.j = 1
        
        Call GetEnd(last.i, last.j)
        While ExisteStr(pContinue.i, pContinue.j, last.i, last.j)
            igncontent = ""
            Call InString(pContinue.i, pContinue.j, last.i, last.j, "[" & UnclosedTags(Index).elem1, pUnclosedTag.i, pUnclosedTag.j, vbBinaryCompare)
            If pUnclosedTag.j > 0 Then
                Call InString(pUnclosedTag.i, pUnclosedTag.j, last.i, last.j, "]", pOpenIGNtag.i, pOpenIGNtag.j, vbBinaryCompare)
                If pOpenIGNtag.j > 0 Then
                    pStop = pOpenIGNtag
                    
                    Call ForwardPosition(pOpenIGNtag.i, pOpenIGNtag.j, 1)
                    Call InString(pOpenIGNtag.i, pOpenIGNtag.j, last.i, last.j, "[", pCloseIGNtag.i, pCloseIGNtag.j, vbBinaryCompare)
                    If pCloseIGNtag.j > 0 Then
                        pContinue = pCloseIGNtag
                        Call RewardPosition(pCloseIGNtag.i, pCloseIGNtag.j, 1)
                    Else
                        pCloseIGNtag = last
                        pContinue = last
                        Call ForwardPosition(pContinue.i, pContinue.j, 1)
                    End If
                    
                    igncontent = GetSubstrRange(pOpenIGNtag.i, pOpenIGNtag.j, pCloseIGNtag.i, pCloseIGNtag.j)
                    If Len(igncontent) > 0 Then Call ForwardPosition(pContinue.i, pContinue.j, Len(igntag1) + Len(igntag2))
                Else
                    'encontrou [, mas nao encontrou ]
                    pContinue = last
                    Call ForwardPosition(pContinue.i, pContinue.j, 1)
                End If
            Else
                'esta tag nao foi encontrada
                pContinue = last
                Call ForwardPosition(pContinue.i, pContinue.j, 1)
            End If
        
            If Len(igncontent) > 0 Then
                If pStop.i = pOpenIGNtag.i Then
                    If pOpenIGNtag.i = pCloseIGNtag.i Then
                        If pCloseIGNtag.i = pContinue.i Then
                            SetLine(pOpenIGNtag.i) = GetSubstrRange(pStop.i, 1, pStop.i, pStop.j) + GetSubstrInRow(pContinue.i, pContinue.j, GetLineLen(pContinue.i))
                        ElseIf pCloseIGNtag.i < pContinue.i Then
                            SetLine(pOpenIGNtag.i) = GetSubstrRange(pStop.i, 1, pStop.i, pStop.j)
                        End If
                    ElseIf pOpenIGNtag.i < pCloseIGNtag.i Then
                        SetLine(pOpenIGNtag.i) = GetSubstrRange(pStop.i, 1, pStop.i, pStop.j)
                        For i = pOpenIGNtag.i + 1 To pCloseIGNtag.i - 1
                            SetLine(i) = ""
                        Next
                        If pCloseIGNtag.i = pContinue.i Then
                            SetLine(pCloseIGNtag.i) = GetSubstrInRow(pContinue.i, pContinue.j, GetLineLen(pContinue.i))
                        ElseIf pCloseIGNtag.i < pContinue.i Then
                            SetLine(pCloseIGNtag.i) = ""
                        End If
                    End If
                ElseIf pStop.i < pOpenIGNtag.i Then
                    If pOpenIGNtag.i = pCloseIGNtag.i Then
                        If pCloseIGNtag.i = pContinue.i Then
                            SetLine(pOpenIGNtag.i) = GetSubstrInRow(pContinue.i, pContinue.j, GetLineLen(pContinue.i))
                        ElseIf pCloseIGNtag.i < pContinue.i Then
                            SetLine(pOpenIGNtag.i) = ""
                        End If
                    ElseIf pOpenIGNtag.i < pCloseIGNtag.i Then
                        SetLine(pOpenIGNtag.i) = ""
                        For i = pOpenIGNtag.i + 1 To pCloseIGNtag.i - 1
                            SetLine(i) = ""
                        Next
                        If pCloseIGNtag.i = pContinue.i Then
                            SetLine(pCloseIGNtag.i) = GetSubstrInRow(pContinue.i, pContinue.j, GetLineLen(pContinue.i))
                        ElseIf pCloseIGNtag.i < pContinue.i Then
                            SetLine(pCloseIGNtag.i) = ""
                        End If
                    End If
                End If
            End If
        Wend
    Next
End Sub

Private Sub Class_Terminate()
    Erase Lines
    Erase LinesLen
End Sub
