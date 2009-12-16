Attribute VB_Name = "Geral"
Option Explicit

Public Const PathSep = "\"


Function DelFile(Path As String, File As String) As Boolean
    Dim Ret As Boolean
    
    If FileExist(Path, File) Then
        If Path = "" Then
            Kill File
        Else
            Kill Path + PathSep + File
        End If
        Ret = True
    End If
    DelFile = Ret
End Function

Public Function DirExist(ByVal Path As String, Optional label As String) As Boolean
    Dim x As String
    
    On Error GoTo ERRINHO
    If Len(Path) > 0 Then
        x = Dir(Path, vbDirectory)
    Else
        x = Path
    End If
    DirExist = (StrComp(x, "") <> 0)
    If Not DirExist Then GoTo ERRINHO
Exit Function

ERRINHO:
    If label <> "" Then
        MsgBox label + " - Invalid path: " + Path
    End If
    DirExist = False
End Function
Function FileExist(Path As String, File As String, Optional label As String) As Boolean
    Dim x As String
    
    On Error GoTo ERRINHO
    If File = "" Then
        FileExist = False
    Else
        x = Dir(Path + PathSep + File)
        FileExist = (StrComp(x, "") <> 0)
    End If
    If Not FileExist Then GoTo ERRINHO
Exit Function
ERRINHO:
    If label <> "" Then
        MsgBox label + " - Invalid file: " + Path + PathSep + File
    End If
    FileExist = False
End Function

Function ExisteString(ByVal s As String) As Boolean
    Dim Ret As Boolean
    Dim aux As String
    Dim p As Long
    
    If s = "" Then
        Ret = False
    ElseIf s Like "*[a-zA-Z0-9]*" Then
        Ret = True
    Else
        aux = Trim(s)
        If aux <> "" Then
            p = InStr(aux, Chr(13))
            While p > 0
                aux = Mid(aux, 1, p - 1) + Mid(aux, p + 1)
                p = InStr(aux, Chr(13))
            Wend
        End If
        aux = Trim(aux)
        If aux <> "" Then
            p = InStr(aux, Chr(10))
            While p > 0
                aux = Mid(aux, 1, p - 1) + Mid(aux, p + 1)
                p = InStr(aux, Chr(10))
            Wend
        End If
        aux = Trim(aux)
        Ret = (aux <> "")
    End If
    ExisteString = Ret
End Function
Function FormataDigitos(Nro As String, QtdDigitos As Long) As String
    Dim aux As String
    Dim i As Long
    
    aux = Nro
    For i = 1 To (QtdDigitos - Len(Nro))
        aux = "0" + aux
    Next
    FormataDigitos = aux
End Function

Function RmNewLineInStr(ByVal conteudo As String) As String
    Dim p As Long
    Debug.Print conteudo
    p = InStr(conteudo, Chr(13))
    While p > 0
        conteudo = Mid(conteudo, 1, p - 1) + " " + Mid(conteudo, p + 1)
        p = InStr(conteudo, Chr(13))
    Wend
    
    p = InStr(conteudo, Chr(10))
    While p > 0
        conteudo = Mid(conteudo, 1, p - 1) + " " + Mid(conteudo, p + 1)
        p = InStr(conteudo, Chr(10))
    Wend

    p = InStr(conteudo, Chr(13) + Chr(10))
    While p > 0
        conteudo = Mid(conteudo, 1, p - 1) + " " + Mid(conteudo, p + 2)
        p = InStr(conteudo, Chr(13) + Chr(10))
    Wend
    RmNewLineInStr = conteudo
End Function



Function ReplaceString(s As String, ToBeRemoved As String, Replace As String) As String
    Dim p As Long
    
    p = InStr(s, ToBeRemoved)
    While p > 0
        s = Mid(s, 1, p - 1) + Replace + Mid(s, p + Len(ToBeRemoved))
        p = InStr(s, ToBeRemoved)
    Wend
    
    ReplaceString = s
End Function


Function GetElemStr(s As String, sep As String, Elem() As String) As Long
    'Dada uma S de uma tabela
    'Retorna a quantidade de colunas da tabela
    Dim aspas As Long
    Dim qaspas As Long
    Dim linhaaux As String
    Dim virg As Long
    Dim virgs() As Long
    Dim qvirg As Long
    Dim fecha As Boolean
    Dim i As Long
    
    'Debug.Print i, S
    fecha = True
    qvirg = 0
    qaspas = 0
    aspas = InStr(s, Chr(34))
    While aspas > 0
        qaspas = qaspas + 1
        If (qaspas Mod 2) = 0 Then
            fecha = True
            virg = aspas
        Else
            fecha = False
            linhaaux = Mid(s, 1, aspas)
            virg = InStr(virg + 1, linhaaux, sep, vbBinaryCompare)
            While (virg > 0)
                qvirg = qvirg + 1
                ReDim Preserve virgs(qvirg)
                virgs(qvirg) = virg
                virg = InStr(virg + 1, linhaaux, sep, vbBinaryCompare)
            Wend
        End If
        aspas = InStr(aspas + 1, s, Chr(34), vbBinaryCompare)
    Wend
    If fecha Then
        virg = InStr(virg + 1, s, sep, vbBinaryCompare)
        While (virg > 0)
            qvirg = qvirg + 1
            ReDim Preserve virgs(qvirg)
            virgs(qvirg) = virg
            virg = InStr(virg + 1, s, sep, vbBinaryCompare)
        Wend
    Else
        qvirg = -1
    End If
    virg = 0
    For i = 1 To qvirg
        ReDim Preserve Elem(i)
        Elem(i) = Mid(s, virg + 1, virgs(i) - virg - 1)
        If InStr(Elem(i), Chr(34)) > 0 Then
            Elem(i) = Mid(Elem(i), 2, Len(Elem(i)) - 2)
        End If
        virg = virgs(i)
    Next
    If qvirg >= 0 Then
        i = qvirg + 1
        ReDim Preserve Elem(i)
        Elem(i) = Mid(s, virg + 1)
        If InStr(Elem(i), Chr(34)) > 0 Then
            Elem(i) = Mid(Elem(i), 2, Len(Elem(i)) - 2)
        End If
    End If
    GetElemStr = qvirg + 1
End Function

Function PutAspas(s As String, sep As String) As String
    If InStr(s, sep) > 0 Then s = Chr(34) + s + Chr(34)
    PutAspas = s
End Function

Function GetDateISO(Data As Date) As String

    Dim AppHandle As String
    Dim m As String
    Dim d As String
    
    AppHandle = Year(Data)
    m = Month(Data)
    d = Day(Data)
    If Len(m) = 1 Then m = "0" + m
    If Len(d) = 1 Then d = "0" + d
    
    GetDateISO = AppHandle + m + d
End Function

Function IsNumber(number As String) As Boolean
    Dim i As Long
    Dim Pattern As String
    
    If Len(number) > 0 Then
        For i = 1 To Len(number)
            Pattern = Pattern + "#"
        Next
    
        If number Like Pattern Then IsNumber = True
    End If
End Function
