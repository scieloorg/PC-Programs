Attribute VB_Name = "ModCodes"
Option Explicit

Public MARKUPPATH As String
Public ATTB_FILE As String
Public ATTB_LABEL As String



Public DBCODESPATH As String
Public DBNEWCODEFILE As String
Public DBCODEFILE As String
Public DBCODESLABEL As String
Public AppHandle As Long

Public IdiomsInfo As ColIdiom
Public ConfigLabels As ClLabels
Public CURRENT_LANG As String
Public FORMER_LANG As String

Public paths As ColFileInfo

Sub setLang(langCode As String, langText As String)
    Set ConfigLabels = New ClLabels
    ConfigLabels.SetLabels (langCode)
    CURRENT_LANG = langText
    FormMenuPrin.SetLabels
End Sub
Sub Main()
    Dim fn As Long
    Dim code As String
    Dim value As String
    Dim idiominfo As ClIdiom
    Dim i As Long
    Dim PATHS_CONFIGURATION_FILE As String
    
    Dim lang As String
    Dim langT As String
    
    AppHandle = IsisAppNew
    
    
    
    fn = 1
    Open App.path + "\codes.ini" For Input As fn
    Input #fn, code, PATHS_CONFIGURATION_FILE
    'Input #fn, DBCODESPATH, DBNEWCODEFILE, DBCODESLABEL
    'Input #fn, DBCODESPATH, DBCODEFILE, DBCODESLABEL
    'Input #fn, MARKUPPATH, ATTB_FILE, ATTB_LABEL
    
    lang = ""
    Set IdiomsInfo = New ColIdiom
    Set idiominfo = New ClIdiom
    For i = 1 To 3
        Input #fn, code, value
        Set idiominfo = IdiomsInfo.Add(code, value, " ", value)
    Next
    Close fn
    
    fn = FreeFile
    Open App.path + "\lang.ini" For Input As fn
    Input #fn, lang
     FORMER_LANG = lang
    Close fn
    
    For i = 1 To 3
        If (lang = IdiomsInfo.Item(i).code) Or (lang = "") Then
            langT = IdiomsInfo.Item(i).label
            lang = IdiomsInfo.Item(i).code
        End If
    Next
    Call setLang(lang, langT)
    Set paths = ReadPathsConfigurationFile(PATHS_CONFIGURATION_FILE)
    
    DBCODESPATH = paths("Code Database").path
    DBNEWCODEFILE = paths("NewCode Database").filename
    DBCODEFILE = paths("Code Database").filename
    DBCODESLABEL = paths("Code Database").key
    MARKUPPATH = paths("Markup Attributes Table").path
    ATTB_FILE = paths("Markup Attributes Table").filename
    ATTB_LABEL = paths("Markup Attributes Table").key
    
    
    FormMenuPrin.OpenMenu
    
End Sub

Function ReadPathsConfigurationFile(File As String) As ColFileInfo
    Dim fn As Long
    Dim lineread As String
    Dim Item As ClFileInfo
    Dim key As String
    Dim path As String
    Dim CollectionPaths As ColFileInfo
    Dim req As Long
    
    fn = FreeFile
    Open File For Input As fn
        
    Set CollectionPaths = New ColFileInfo
    
    While Not EOF(fn)
        Line Input #fn, lineread
        If InStr(lineread, "=") > 0 Then
            key = Mid(lineread, 1, InStr(lineread, "=") - 1)
            path = Mid(lineread, InStr(lineread, "=") + 1)
            req = InStr(path, ",required")
            If req > 0 Then
                path = Mid(path, 1, req - 1)
                
            End If
            Set Item = CollectionPaths.Add(key)
            Item.key = key
            If InStr(path, "\") > 0 Then
                Item.path = Mid(path, 1, InStrRev(path, "\") - 1)
                Item.filename = Mid(path, InStrRev(path, "\") + 1)
            Else
                Item.path = ""
                Item.filename = path
            End If
            Item.required = (req > 0)
        End If
    Wend
    Close fn
    Set ReadPathsConfigurationFile = CollectionPaths
End Function

Sub GenerateCodeFile()
    Dim i As Long
    Dim j As Long
    Dim fn As Long
    Dim fn2 As Long
    Dim dbtype As String
    Dim attr As String
    Dim idiom As String
    Dim dbname As String
    
    Dim dao As New clsCodeDAO
    
    fn = 1
    fn2 = 2
    
    For i = 1 To IdiomsInfo.Count
        Open MARKUPPATH + PathSep + IdiomsInfo(i).code + ATTB_FILE For Output As fn
        Open "values.lst" For Input As fn2
        While Not EOF(fn2)
            Input #fn2, dbtype, attr, idiom
            If dbtype = "new" Then
                dbname = DBNEWCODEFILE
            ElseIf dbtype = "curr" Then
                dbname = DBCODEFILE
            End If
            Call dao.setDB(DBCODESPATH, dbname, dbtype)
            
            If idiom = "yes" Then
                Print #fn, dao.getCodesAndValues(attr, IdiomsInfo(i).code)
            Else
                Print #fn, dao.getCodesAndValues(attr)
            End If
        Wend
        Close fn2
        Close fn
    Next
End Sub

Sub saveConfig()
    Dim fn As Long
    If FORMER_LANG <> IdiomsInfo(CURRENT_LANG).code Then
        fn = FreeFile
        Open App.path + "\lang.ini" For Output As fn
        Print #fn, IdiomsInfo(CURRENT_LANG).code
        Close fn
    End If
End Sub
