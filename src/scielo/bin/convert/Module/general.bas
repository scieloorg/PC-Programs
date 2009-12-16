Attribute VB_Name = "General"
Option Explicit

Public Const PathSep = "\"

Private TempDispo As New ClFila     'Arquivos temporários disponíveis
Private TempCounter As Long         'Índice diferenciador dos arquivos temporários
Const TempName = "cvttmp"        'Nome do arquivos temporários

'----------------------------------------------------------------------
'DelFile    - apaga arquivo(s)
'Path       - caminho do arquivo
'File       - nome do arquivo
'Retorno    - sucesso ou fracasso
'----------------------------------------------------------------------
Function DelFile(Path As String, File As String) As Boolean
    Dim ret As Boolean
    
    If FileExist(Path, File) Then
        'If Path = "" Then
        '    Kill file
        'Else
            Kill Path + PathSep + File
        'End If
        ret = True
    End If
    DelFile = ret

End Function

'----------------------------------------------------------------------
'DelTmpFile - apaga arquivo(s) criados por GetNewTmpFileName
'Path       - caminho do arquivo
'File       - nome do arquivo
'Retorno    - sucesso ou fracasso
'----------------------------------------------------------------------
Function DelTmpFile(Path As String, File As String) As Boolean
    Dim ret As Boolean
    
    If TempDispo.Insere(File) Then
        If Path = "" Then
            Kill File
        Else
            Kill Path + PathSep + File
        End If
    End If
    ret = True
    DelTmpFile = ret
End Function

'----------------------------------------------------------------------
'GetNewTmpFileName - cria um arquivo temporário no caminho dado
'Path       - caminho do arquivo
'Retorno    - nome do arquivo temporário
'----------------------------------------------------------------------
Function GetNewTmpFileName(Path As String) As String
    Dim name As String
    Dim fn As Long
    
    If DirExist(Path, "Temporário") Or (Len(Path) = 0) Then
        If Not TempDispo.Remove(name) Then
            TempCounter = TempCounter + 1
            name = TempName + CStr(TempCounter)
        End If
        fn = FreeFile(1)
        Open Path + PathSep + name For Output As #fn
        Close fn
    End If
    GetNewTmpFileName = name
End Function

'----------------------------------------------------------------------
'DirExist  - check whether a path exists
'Path       - path to check
'Label      - path label
'Return - <True> to sucess; <False> to failure
'----------------------------------------------------------------------
Public Function DirExist(ByVal Path As String, Optional Label As String) As Boolean
    Dim x As String
    
    On Error GoTo ERRINHO
    If Len(Path) > 0 Then x = dir(Path, vbDirectory)
    DirExist = (Len(x) > 0)
    If Not DirExist Then GoTo ERRINHO
Exit Function

ERRINHO:
    If Len(Label) > 0 Then
        MsgBox Label + InterfaceLabels("MsgNotFoundpath").elem2 + Path
    End If
    DirExist = False
End Function

'----------------------------------------------------------------------
'FileExist  - Check whether the file exists
'Path   - path to create
'Label  - path label
'Return - <True> to sucess; <False> to failure
'----------------------------------------------------------------------
Function FileExist(Path As String, File As String, Optional Label As String) As Boolean
    Dim x As String
    Dim f As String
    
    f = File
    If Path <> "" Then f = Path + PathSep + File
    
    On Error GoTo ERRINHO
    If Len(f) > 0 Then
        x = dir(f)
        FileExist = (Len(x) > 0)
    Else
        FileExist = False
    End If
    If Not FileExist Then GoTo ERRINHO
Exit Function
ERRINHO:
    If Len(Label) > 0 Then
        MsgBox Label + InterfaceLabels("MsgNotFoundFile").elem2 + f
    End If
    FileExist = False
End Function

'----------------------------------------------------------------------
'FormatDigits   - completa com zeros à esquerda de um número para que
'               este fique com uma determinada quantidade de dígitos
'Number         - número
'DigitsNumber   - número de dígitos
'Retorno        - número formatado
'----------------------------------------------------------------------
Function FormatDigits(ByVal number As String, DigitsNumber As Long) As String
    
    If IsNumber(number) Then number = String(DigitsNumber - Len(number), "0")
    FormatDigits = number
End Function

'----------------------------------------------------------------------
'RmNewLineInStr - remove <new line> de uma string
's              - string
'Retorno        - string sem <new line>
'----------------------------------------------------------------------
Function RmNewLineInStr(ByVal s As String) As String
    Dim P As Long
    
    P = InStr(s, vbCrLf)
    While P > 0
        s = Mid(s, 1, P - 1) + Chr(32) + Mid(s, P + 2)
        P = InStr(s, vbCrLf)
    Wend
    
    P = InStr(s, vbCr)
    While P > 0
        s = Mid(s, 1, P - 1) + Chr(32) + Mid(s, P + 1)
        P = InStr(s, vbCr)
    Wend
    
    P = InStr(s, vbLf)
    While P > 0
        s = Mid(s, 1, P - 1) + Chr(32) + Mid(s, P + 1)
        P = InStr(s, vbLf)
    Wend

    P = InStr(s, vbTab)
    While P > 0
        s = Mid(s, 1, P - 1) + Chr(32) + Mid(s, P + 1)
        P = InStr(s, vbTab)
    Wend

    RmNewLineInStr = s
End Function

'----------------------------------------------------------------------
'ReplaceString   - substitui uma string <s> por <Replace> em uma string
'r          - string
'ToBeReplaced    - substring to be replaced
'Replace    - substring to replace <Replace> with the <ToBeReplaced>
'TpComp - type of comparation
'Return the replaced string
'----------------------------------------------------------------------
Function ReplaceString(s As String, ToBeReplaced As String, Replace As String, TpComp As VbCompareMethod) As String
    Dim P As Long
    Dim r As String
    Dim forward As Long
    Dim f As Long
    
    r = s
    f = InStr(1, Replace, ToBeReplaced, TpComp)
    While (f > 0)
        forward = f
        f = InStr(f + 1, Replace, ToBeReplaced, vbBinaryCompare)
    Wend
    
    'If InStr(1, Replace, ToBeReplaced, TpComp) > 0 Then forward = 1
    
    If Len(ToBeReplaced) > 0 Then
        P = InStr(1, r, ToBeReplaced, TpComp)
        While P > 0
            r = Mid(r, 1, P - 1) + Replace + Mid(r, P + Len(ToBeReplaced))
            P = InStr(P + forward, r, ToBeReplaced, TpComp)
        Wend
    End If
    ReplaceString = r
End Function

'----------------------------------------------------------------------
'GetElemStr - obtém elementos de uma string sendo que eles estão
'           separados por algum separador e agrupados por aspas duplas
's          - string
'sep        - separador de um caracter apenas
'Elem       - os elementos obtidos
'Retorno    - a quantidade de elementos obtidos
'----------------------------------------------------------------------
Function GetElemStr(s As String, sep As String, elem() As String) As Long
    Dim pos_aspas As Long
    Dim q_aspas As Long
    Dim linhaaux As String
    Dim pos_virg As Long
    Dim virgs() As Long
    Dim qvirg As Long
    Dim fecha As Boolean
    Dim i As Long
    
    fecha = True
    Erase elem
    pos_aspas = InStr(s, Chr(34))
    While pos_aspas > 0
        q_aspas = q_aspas + 1
        If (q_aspas Mod 2) = 0 Then
            If pos_aspas = Len(s) Then
                fecha = True
                pos_virg = pos_aspas
            ElseIf StrComp(Mid(s, pos_aspas + 1, 1), COMMA, vbTextCompare) = 0 Then
                fecha = True
                pos_virg = pos_aspas
            End If
        Else
            If (pos_aspas = 1) Then
                fecha = False
                linhaaux = Mid(s, 1, pos_aspas)
                pos_virg = InStr(pos_virg + 1, linhaaux, sep, vbBinaryCompare)
                While (pos_virg > 0)
                    qvirg = qvirg + 1
                    ReDim Preserve virgs(qvirg)
                    virgs(qvirg) = pos_virg
                    pos_virg = InStr(pos_virg + 1, linhaaux, sep, vbBinaryCompare)
                Wend
            ElseIf (StrComp(Mid(s, pos_aspas - 1, 1), COMMA, vbTextCompare) = 0) Then
                fecha = False
                linhaaux = Mid(s, 1, pos_aspas)
                pos_virg = InStr(pos_virg + 1, linhaaux, sep, vbBinaryCompare)
                While (pos_virg > 0)
                    qvirg = qvirg + 1
                    ReDim Preserve virgs(qvirg)
                    virgs(qvirg) = pos_virg
                    pos_virg = InStr(pos_virg + 1, linhaaux, sep, vbBinaryCompare)
                Wend
            End If
        End If
        pos_aspas = InStr(pos_aspas + 1, s, Chr(34), vbBinaryCompare)
    Wend
    If fecha Then
        pos_virg = InStr(pos_virg + 1, s, sep, vbBinaryCompare)
        While (pos_virg > 0)
            qvirg = qvirg + 1
            ReDim Preserve virgs(qvirg)
            virgs(qvirg) = pos_virg
            pos_virg = InStr(pos_virg + 1, s, sep, vbBinaryCompare)
        Wend
    Else
        qvirg = -1
    End If
    pos_virg = 0
    For i = 1 To qvirg
        ReDim Preserve elem(i)
        elem(i) = Mid(s, pos_virg + 1, virgs(i) - pos_virg - 1)
        If InStr(elem(i), Chr(34)) = 1 Then
            elem(i) = Mid(elem(i), 2, Len(elem(i)) - 2)
        End If
        pos_virg = virgs(i)
    Next
    If qvirg >= 0 Then
        i = qvirg + 1
        ReDim Preserve elem(i)
        elem(i) = Mid(s, pos_virg + 1)
        If InStr(elem(i), Chr(34)) = 1 Then
            elem(i) = Mid(elem(i), 2, Len(elem(i)) - 2)
        End If
    End If
    GetElemStr = qvirg + 1
End Function


Function SetElemStr(ByVal s As String, sep As String, elem As String) As String
    If Len(s) > 0 Then
        s = s + sep + PutAspas(elem, sep)
    Else
        s = PutAspas(elem, sep)
    End If
    SetElemStr = s
End Function

Function SetElemArray(ByVal s As String, sep As String, elem() As String, Count As Long) As String
    Dim i As Long
    
    For i = 2 To Count
        s = s + sep + PutAspas(elem(i), sep)
    Next
    If Count > 0 Then s = PutAspas(elem(1), sep) + s
    SetElemArray = s
End Function

'----------------------------------------------------------------------
'PutAspas   - delimita com aspas duplas uma string que contenha vírgula
's          - string
'Retorno    - a nova string
'----------------------------------------------------------------------
Function PutAspas(s As String, sep As String) As String
    If InStr(s, sep) > 0 Then s = Chr(34) + s + Chr(34)
    PutAspas = s
End Function

'----------------------------------------------------------------------
'GetDateISO - transforma uma data para data ISO
'Data       - y data
'Retorno    - y nova data
'----------------------------------------------------------------------
Function GetDateISO(data As Date) As String

    Dim Y As String
    Dim m As String
    Dim d As String
    
    Y = year(data)
    m = Month(data)
    d = Day(data)
    If Len(m) = 1 Then m = "0" + m
    If Len(d) = 1 Then d = "0" + d
    
    GetDateISO = Y + m + d
End Function

'----------------------------------------------------------------------
'GetTimeISO - transforma uma xhour para xhour ISO
'xhour       - h1 xhour
'Retorno    - h1 nova xhour
'----------------------------------------------------------------------
Function GetTimeISO(xhour As Date) As String

    Dim h1 As String
    Dim h2 As String
    Dim h3 As String
    
    h1 = Hour(xhour)
    h2 = Minute(xhour)
    h3 = Second(xhour)
    If Len(h1) = 1 Then h1 = "0" + h1
    If Len(h2) = 1 Then h2 = "0" + h2
    If Len(h3) = 1 Then h3 = "0" + h3
    
    GetTimeISO = h1 + h2 + h3
End Function

'----------------------------------------------------------------------
'IsNumber   - verifica se uma string corresponde a um número
'Number     - string
'Retorno    - verdadeiro ou falso
'----------------------------------------------------------------------
Function IsNumber(number As String) As Boolean
    Dim pattern As String
    
    If Len(number) > 0 Then
        pattern = String(Len(number), "#")
        If number Like pattern Then IsNumber = True
    End If
End Function


'----------------------------------------------------------------------
'MakeDir  - create a path
'Path   - path to create
'Label  - path label
'Return - <True> to sucess; <False> to failure
'----------------------------------------------------------------------
Public Function MakeDir(ByVal Path As String, Optional Label As String) As Boolean
    Dim ExistingPath As String
    Dim tocheck As String
    Dim tomake As String
    Dim P As Long
    Dim p2 As Long
    Dim exist As Boolean
    
    tomake = Path
    exist = True
    p2 = 1
    
    If Mid(tomake, Len(tomake)) <> PathSep Then
        tomake = tomake + PathSep
    End If
    
    'Check existing path
    While exist
        P = InStr(p2, tomake, PathSep, vbBinaryCompare)
        If P > 0 Then
            tocheck = Mid(tomake, 1, P - 1)
            exist = DirExist(tocheck)
            If exist Then ExistingPath = tocheck
        End If
        p2 = P + 1
    Wend
    
    'Make each directory
    P = Len(tocheck) + 1
    While P > 0
        MkDir Mid(tomake, 1, P - 1)
        P = InStr(p2, tomake, PathSep, vbBinaryCompare)
        p2 = P + 1
        exist = True
    Wend
    MakeDir = exist
End Function

Function NoExtensionFileName(filename As String) As String
    Dim s As String
    Dim s2 As String
    Dim P As Long
    
    s2 = filename
    P = InStr(s2, ".")
    While P > 0
        s = Mid(s2, 1, P)
        s2 = Mid(s2, P + 1)
        P = InStr(s2, ".")
    Wend
    s = Mid(s, 1, Len(s) - 1)
    NoExtensionFileName = s
End Function
Sub SeparateFileandPath(FullFilePath As String, Path As String, File As String)
    Dim fullpath As String
    Dim P As Long
    
    P = InStrRev(FullFilePath, "\")
    
    Path = Mid(FullFilePath, 1, P - 1)
    File = Mid(FullFilePath, P + 1)
    
End Sub

 Function moveFile(src As String, dest As String) As Boolean
    If FileExist("", src) Then
        Call FileCopy(src, dest)
        If FileExist("", dest) Then
            Kill src
        End If
    End If
    moveFile = FileExist("", dest)
End Function

Function rmEntities(s As String) As String
    Dim P As Long
    Dim p2 As Long
    Dim teste As String
    Dim checked As String
    Dim nova As String
    
    P = InStr(s, "&")
    While P > 0
        nova = Mid(s, 1, P - 1)
        s = Mid(s, P + 1)
        
        p2 = InStr(s, ";")
        If p2 > 0 Then
            teste = Mid(s, 1, p2)
            If InStr(teste, " ") > 0 Then
                nova = nova + "&"
            Else
                s = Mid(s, p2 + 1)
            End If
        Else
            nova = nova + "&"
        End If
        P = InStr(s, "&")
    Wend
End Function

Function cleanText(s As String) As String
    Dim j As Long
    Dim c As String
    Dim r As String
    
    Call Msg.GiveRunInformation("original " + s)
    s = rmEntities(s)
    Call Msg.GiveRunInformation("rmEntities " + s)
    For j = 1 To Len(s)
        c = Mid(s, j, 1)
        If c Like "[A-Za-z0-9]" Then
            r = r + c
        End If
    Next
    Call Msg.GiveRunInformation("cleanText " + r)
    
    cleanText = r
End Function

Function checkDates(prevDate As String, nextDate As String, prevDateLabel As String, nextDateLabel As String) As Boolean
    Dim r As Boolean
    Dim myMsg As String
    Dim diff As Long
    
    r = True
    If prevDate <> "" Then
        If CLng(prevDate) > CLng(nextDate) Then
                myMsg = Replace(InterfaceLabels("MsgAHPDateOrRVPdate_BadRange").elem2, "%PARAM_1%", prevDateLabel)
                myMsg = Replace(myMsg, "%PARAM_2%", prevDate)
                myMsg = Replace(myMsg, "%PARAM_3%", nextDate)
                myMsg = Replace(myMsg, "%PARAM_4%", nextDateLabel)
                Call Msg.GiveRunInformation(myMsg, False, False, True)
                r = False
        End If
    End If
    checkDates = r
End Function
