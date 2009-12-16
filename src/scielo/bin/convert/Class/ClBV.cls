VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClBV"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Attribute VB_Ext_KEY = "SavedWithClassBuilder" ,"Yes"
Attribute VB_Ext_KEY = "Top_Level" ,"Yes"
Option Explicit

Public BVPath As String
Public BVKey As String
Public BVname As String
Public BVconfigurationfile As String
Public BVdirstructure As String
Public Icon As String
Public BVPathsConfigurationFile As String

'Public FileTree As ClTree
Public FileTree As ClTempFileTree


Public Directory As ColDirInfo
Public SearchOptions As ColSearchOptions

Public DTDCol  As ColDTD
Public CfgTagCol As ColCfgTag

Private DocOrderLen() As Long
Public HasFulltext As Boolean
Public DatabaseNameFormat As String
Public DatabaseNamePattern As String
Public BVISISTAGS As ColTag
Public Flag_PreviousAuthor As String
Public Flag_ISSN As String
Public Flag_ISODB As String
Public Flag_CfgRecInDB As String
Private mvarEletronicMediumPft As String

Private WebPath() As String
Private WebFile() As String
Public WebCount As Long

Public BuildDocId As String
Public DatabaseId As String



'--------------------------
'leis
'--------------------------
Public LawBodyTags As ColPair

Property Let EletronicMediumPft(Optional acron As String, v As String)
    mvarEletronicMediumPft = v
End Property


Property Get EletronicMediumPft(acron As String) As String
    Dim temp As String
    Dim novo As String
    Dim r As String
    
    r = mvarEletronicMediumPft
    novo = getScieloUrl(acron)
    If novo <> "" Then
        temp = Mid(mvarEletronicMediumPft, InStr(mvarEletronicMediumPft, "http://") + Len("http://"))
        temp = Mid(temp, 1, InStr(temp, "/") - 1)
        If temp <> novo Then
            r = Replace(mvarEletronicMediumPft, temp, novo)
        End If
    End If
    EletronicMediumPft = r
End Property
Property Get getDocOrderLen(Optional i As Long) As Variant
    If i >= 0 Then
        getDocOrderLen = DocOrderLen(i)
    Else
        getDocOrderLen = DocOrderLen
    End If
End Property
Property Get WebBasesPath(i As Long) As String
    WebBasesPath = WebPath(i)
End Property
Property Get WebBasesFile(i As Long) As String
    WebBasesFile = WebFile(i)
End Property

'------------------------------------------------------------------------
'BVConfigSet - Write the convert.ini file
'------------------------------------------------------------------------
Private Sub BVConfigSet()
    Dim fn As Long
    Dim i As Long
    Dim temp As String
    
    
    fn = FreeFile(1)
    temp = Join(DocOrderLen, "|")
    
    Open BVconfigurationfile For Output As fn
    Print #fn, "[Variables]"
    Write #fn, "MKPERRDISPLAYED", MKPERRDISPLAYED
    Write #fn, "DEFAULTBROWSERPATH", DEFAULTBROWSERPATH
    Write #fn, "CurrIdiomHelp", CurrIdiomHelp
    Write #fn, "DocOrderLen", temp
    
    If IdiomHelp.Count > 0 Then
        Print #fn,
        Print #fn, "[IdiomHelp]"
        For i = 1 To IdiomHelp.Count
            With IdiomHelp(i)
            Print #fn, .Label + SEP_CONVERTINI + .code
            End With
        Next
    End If
    
    If DTDCol.Count > 0 Then
        Print #fn,
        Print #fn, "[DTDs]"
        For i = 1 To DTDCol.Count
            With DTDCol(i)
            Print #fn, .name + SEP_CONVERTINI + _
            .Version + SEP_CONVERTINI + _
            .SGMLDecl + SEP_CONVERTINI + _
            .FileName + SEP_CONVERTINI + _
            .CTableFile + SEP_CONVERTINI + _
            .TranslFile + SEP_CONVERTINI + _
            .ProcFile + SEP_CONVERTINI + _
            .CitationFile + SEP_CONVERTINI + _
            .LiteratureType + SEP_CONVERTINI + _
            .RecCode + SEP_CONVERTINI + .RecLabel
            End With
        Next
    End If
    If CvtTables.Count > 0 Then
        Print #fn,
        Print #fn, "[GIZMOS]"
        For i = 1 To CvtTables.Count
            With CvtTables(i)
            Print #fn, .key
            End With
        Next
    End If
    
    If CvtTabLanguage.Count > 0 Then
        Print #fn,
        Print #fn, "[IDIOM CONVERSION TABLES]"
        For i = 1 To CvtTabLanguage.Count
            With CvtTabLanguage(i)
            Print #fn, .key
            End With
        Next
    End If
       
    If BVISISTAGS.Count > 0 Then
        Print #fn,
        Print #fn, "[Tags]"
        For i = 1 To BVISISTAGS.Count
            With BVISISTAGS(i)
            Print #fn, .key + EQUALSIGNAL + CStr(.Value) + SEP_CONVERTINI + .Subf + SEP_CONVERTINI + .Label
            End With
        Next
    End If
    Close fn
End Sub

'------------------------------------------------------------------------
'BVConfigGet - Read the .ini file of the virtual library and set values to global variables
'------------------------------------------------------------------------
Function BVConfigGet(LibraryPath As String) As Boolean
    Dim NewIdiomHelp As ClIdiom
    Dim NewDTD As ClDTD
    Dim NewCfgTag As ClCfgTag
    Dim NewBodyTag As ClPair
    Dim direct As ClDirInfo
    Dim ctab As ClCvtTab
    Dim NewSearchOpt As ClSearchOptions
    Dim SECTION As String
    Dim fn As Long
    Dim InputLine As String
    Dim P As Long
    Dim Value() As String
    Dim q As Long
    Dim ERROR As Boolean
    Dim key As String
    
    
    Set DTDCol = New ColDTD
    Set CfgTagCol = New ColCfgTag
    Set BVISISTAGS = New ColTag
    Set direct = New ClDirInfo
    Set Directory = New ColDirInfo
    Set SearchOptions = New ColSearchOptions
    Set LawBodyTags = New ColPair

    
    fn = FreeFile(1)
    BVPath = LibraryPath + PathSep + BVKey
    
    Open BVPath + PathSep + BVconfigurationfile For Input As fn
    While Not EOF(fn) And (Not ERROR)
        Line Input #fn, InputLine
        
        If (InStr(InputLine, OPEN_SECTION) = 1) And (InStr(InputLine, CLOSE_SECTION) = Len(InputLine)) Then
            SECTION = InputLine
        
        ElseIf Len(InputLine) = 0 Then
            SECTION = ""
            
        ElseIf Len(InputLine) > 0 Then
        
            q = GetElemStr(InputLine, SEP_CONVERTINI, Value)
            
            Select Case SECTION
            Case "[Variables]"
                If q = 2 Then
                    'Input #fn, key, MKPERRDISPLAYED
                    Select Case Value(1)
                    'Case "VOLSGL"
                    '    VOLSGL = Value(2)
                    'Case "NOSGL"
                    '    NOSGL = Value(2)
                    'Case "VOLSUPPLSGL"
                    '    VOLSUPPLSGL = Value(2)
                    'Case "NOSUPPLSGL"
                    '    NOSUPPLSGL = Value(2)
                    Case "DocOrderLen"
                        Dim test() As String
                        Dim i As Long
                        
                        test = Split(Value(2), "|")
                        For i = 0 To UBound(test, 1)
                            ReDim Preserve DocOrderLen(i)
                            DocOrderLen(i) = CLng(test(i))
                        Next
                    Case "BuildDocId"
                        BuildDocId = Value(2)
                    Case "DatabaseId"
                        DatabaseId = Value(2)
                    Case "HasFulltext"
                        HasFulltext = Value(2)
                    Case "DatabaseNameFormat"
                        DatabaseNameFormat = Value(2)
                    Case "DBNamePattern"
                        DatabaseNamePattern = Value(2)
                    Case "Flag_PreviousAuthor"
                        Flag_PreviousAuthor = Value(2)
                    Case "Flag_ISSN"
                        Flag_ISSN = Value(2)
                    Case "Flag_ISODB"
                        Flag_ISODB = Value(2)
                    Case "Flag_CfgRecInDB"
                        Flag_CfgRecInDB = Value(2)
                    Case "EletronicMediumPft"
                        EletronicMediumPft = Value(2)
                    
                    End Select
                Else
                    ERROR = True
                End If
            Case "[Tags]"
                P = InStr(InputLine, EQUALSIGNAL)
                If P > 0 Then
                    key = Mid(InputLine, 1, P - 1)
                    InputLine = Mid(InputLine, P + 1)
                    q = GetElemStr(InputLine, SEP_CONVERTINI, Value)
                    If q = 3 Then
                        Call BVISISTAGS.Add(Value(3), key, CLng(Value(1)), Value(2), key)
                    Else
                        ERROR = True
                    End If
                Else
                    ERROR = True
                End If
                
            Case "[BVSLaw Markup Tags]"
                If q = 3 Then
                    Set NewBodyTag = New ClPair
                    Set NewBodyTag = LawBodyTags.Add(Value(1))
                    NewBodyTag.elem1 = Value(1)
                    NewBodyTag.elem2 = Value(2)
                    NewBodyTag.elem3 = Value(3)
                Else
                    ERROR = True
                End If
                
            Case "[DTDs]"
                If q = 12 Then
                    Set NewDTD = New ClDTD
                    Set NewDTD = DTDCol.Add(Value(1) + Chr(32) + Value(2))
                    With NewDTD
                    .name = Value(1)
                    .Version = Value(2)
                    .SGMLDecl = Value(3)
                    .FileName = Value(4)
                    .CTableFile = Value(5)
                    .TranslFile = Value(6)
                    .ProcFile = Value(7)
                    .CitationFile = Value(8)
                    .LiteratureType = Value(9)
                    .RecCode = Value(10)
                    .RecLabel = Value(11)
                    .SetUnclosedTags (Value(12))
                    End With
                Else
                    ERROR = True
                End If
            Case "[DirInfo]"
                If q = 17 Then
                    Set direct = New ClDirInfo
                    Set direct = Directory.Add()
                    With direct
                    .Index = CLng(Value(1))
                    .LabDir = Value(2)
                    .ObjTypeDir = Value(3)
                    .pattern = Value(4)
                    .ContentListFile = Value(5)
                    .level = CLng(Value(6))
                    .Prefix = Value(7)
                    .suffix = Value(8)
                    .DatabaseKey = Value(9)
                    .codefield = Value(10)
                    .valfield = Value(11)
                    .cfgkey_pft = Value(12)
                    .cfgkey_val = Value(13)
                    .MsgInvalidData = Value(14)
                    .IsDatabaseDir = Value(15)
                    .IsDatabaseName = Value(16)
                    .optional_level = Value(17)
                    End With
                Else
                    ERROR = True
                End If
            Case "[SearchOptions]"
                If q = 6 Then
                    Set NewSearchOpt = New ClSearchOptions
                    Set NewSearchOpt = SearchOptions.Add()
                    With NewSearchOpt
                    .Id = CLng(Value(1))
                    .LabelKey = Value(2)
                    .ComponentType = Value(3)
                    If Len(Value(4)) > 0 Then .ValueListId = CLng(Value(4))
                    .Field = Value(5)
                    .CompareType = Value(6)
                    End With
                Else
                    ERROR = True
                End If
            Case "[CfgRec]"
                If q = 6 Then
                    Set NewCfgTag = New ClCfgTag
                    Set NewCfgTag = CfgTagCol.Add(Value(1))
                    With NewCfgTag
                    .LabelKey = Value(1)
                    .Tag = CLng(Value(2))
                    .DocFieldPft = Value(3)
                    .CfgFieldPft = Value(4)
                    .CompareType = Value(5)
                    .ContentType = Value(6)
                    End With
                Else
                    ERROR = True
                End If
            
            Case "[WebBase]"
                If q = 2 Then
                    WebCount = WebCount + 1
                    ReDim Preserve WebPath(WebCount)
                    ReDim Preserve WebFile(WebCount)
                    WebPath(WebCount) = Value(1)
                    WebFile(WebCount) = Value(2)
                Else
                    ERROR = True
                End If
                
            End Select
        End If
    Wend
    Close fn
    
    If ERROR Then
        MsgBox InterfaceLabels("MsgBVINIFileFailure").elem2 + InputLine
    End If
    BVConfigGet = Not ERROR
End Function

'--------------------------------------------------------------------------------
'LoadFilestoConverterProgram - Load the files used to the converter program
'Return - Sucess or failure
'--------------------------------------------------------------------------------
Function LoadFilestoConverterProgram() As Boolean
    Dim fn As Long
    Dim fn2 As Long
    Dim fullname As String
    Dim abbrname As String
    Dim ret As Boolean
    Dim i As Long
    Dim Mfn As Long
    Dim dir As ClPair
    Dim names As String
    
        
    If FileTree.CheckFilePath Then
    
        For i = 1 To Directory.Count
            With Directory(i)
            If Len(.ContentListFile) > 0 Then
                If Len(.DatabaseKey) > 0 Then
                    Set .Database = New ClIsisDll
                    If .Database.Initiate(FileTree.DirNodes(.DatabaseKey).fullpath, FileTree.DirNodes(.DatabaseKey).text, FileTree.DirNodes(.DatabaseKey).key) Then
                        fn = FreeFile
                        Open BVPath + PathSep + IdiomHelp(CurrIdiomHelp).code + "_" + .ContentListFile For Output As fn
                    
                        Set Directory(i).CfgKeys = New ColPair
                    
                        Print #fn, "," + Chr(34) + Chr(34)
                        For Mfn = 1 To .Database.MfnQuantity
                            fullname = .Database.UsePft(Mfn, .valfield)
                            abbrname = .Database.UsePft(Mfn, .codefield)
                            If (Len(Trim(fullname)) > 0) And (Len(Trim(abbrname)) > 0) Then
                                Print #fn, abbrname + "," + Chr(34) + fullname + Chr(34)
                                If Len(.cfgkey_pft) > 0 Then
                                    Set dir = Directory(i).CfgKeys.Item(fullname)
                                    If dir Is Nothing Then
                                        Set dir = Directory(i).CfgKeys.Add(fullname)
                                        dir.elem1 = fullname
                                    Else
                                        Set dir = Directory(i).CfgKeys.Add(fullname + " " + abbrname)
                                        dir.elem1 = fullname + " {" + abbrname + "}"
                                    End If
                                    
                                    dir.elem2 = .Database.UsePft(Mfn, .cfgkey_pft)
                                End If
                            End If
                        Next
                        Close fn
                    End If
                    Set .Database = Nothing
                End If
            
                
                fn = FreeFile
                Open BVPath + PathSep + IdiomHelp(CurrIdiomHelp).code + "_" + Directory(i).ContentListFile For Input As fn
                
                Set Directory(i).ContentListAbbr = New ColPair
                Set Directory(i).ContentListFull = New ColPair
                
                While Not EOF(fn)
                    Input #fn, abbrname, fullname
                    
                    
                    Set dir = Directory(i).ContentListFull.Item(fullname)
                    If dir Is Nothing Then
                        Set dir = Directory(i).ContentListFull.Add(fullname)
                        dir.elem1 = fullname
                    Else
                        Set dir = Directory(i).ContentListFull.Add(fullname + " " + abbrname)
                        dir.elem1 = fullname + " {" + abbrname + "}"
                        
                    End If
                    dir.elem2 = abbrname
                    names = dir.elem1
                    
                    Set dir = Directory(i).ContentListAbbr.Add(abbrname)
                    dir.elem1 = abbrname
                    
                    dir.elem2 = names
                    
                Wend
                Close fn
            End If
            End With
            ret = True
        Next
    End If
    
    LoadFilestoConverterProgram = ret
End Function

Private Sub Class_Initialize()
    Set DTDCol = New ColDTD
    Set BVISISTAGS = New ColTag
    Set FileTree = New ClTempFileTree
    Set Directory = New ColDirInfo
    Set SearchOptions = New ColSearchOptions
    Set CfgTagCol = New ColCfgTag
    Set LawBodyTags = New ColPair
End Sub

Private Sub Class_Terminate()
    Set DTDCol = Nothing
    Set BVISISTAGS = Nothing
    Set FileTree = Nothing
    Set Directory = Nothing
    Set SearchOptions = Nothing
    Set CfgTagCol = Nothing
    Set LawBodyTags = Nothing
End Sub

Public Sub LawBodyTagsGetInfo(ByVal scope As String, key As String, root As String, element As String, status As String)
    Dim IndexedElem As String
    Dim scope_tmp As String
    Dim first As String
    Dim Index As String
    Dim elem As String
    Dim P As Long
    Dim p1 As Long
    Dim p2 As Long
    Dim i As Long
    Dim found As Boolean

    'obtem a chave a partir do escopo
    'a chave é formada por uma sequencia de
    'caracter e numero <Index> correspondentes ao elemento <elem>,
    'sendo que o caracter correspondente provem de LawBodyTags
    'exemplo:
    
    scope_tmp = scope + " "
    status = ""
    key = ""
    P = 1
    p2 = InStr(scope_tmp, " ")
    While (p2 > 0) And (Len(scope_tmp) > 0)
        IndexedElem = Mid(scope_tmp, P, p2 - P)
        scope_tmp = Mid(scope_tmp, p2 + 1)
        
        p1 = InStr(IndexedElem, ":")
        If p1 > 0 Then
            elem = Mid(IndexedElem, 1, p1 - 1)
            Index = Mid(IndexedElem, p1 + 1)
        End If
        
        i = 0
        found = False
        While (i < LawBodyTags.Count) And (Not found)
            i = i + 1
            found = (StrComp(elem, LawBodyTags(i).elem1, vbTextCompare) = 0)
        Wend
        If found Then
            
            If (Len(key) = 0) And (status = "none") Then
                key = first
            End If
            
            key = key + LawBodyTags(i).elem2 + Index
            If Len(element) = 0 Then
                element = elem
                status = LawBodyTags(i).elem3
            End If
            
            'Elemento raiz (body ou attach)
            root = elem
        End If
        
        first = Index
        p2 = InStr(scope_tmp, " ")
    Wend
    
    Debug.Print element, status
'    Debug.Print "function"
'    Debug.Print "scope=", scope
'    Debug.Print "key=", key
'    Debug.Print "root=", root
'    Debug.Print "element=", element
'    Debug.Print "name=", name
'    Debug.Print "no=", no
End Sub


Function ReadPaths(File As String) As ColPair
    Dim fn As Long
    Dim lineread As String
    Dim Item As ClPair
    Dim key As String
    Dim Path As String
    Dim CollectionPaths As ColPair
    Dim req As Long
    
    fn = FreeFile
    Open File For Input As fn
        
    Set CollectionPaths = New ColPair
    
    While Not EOF(fn)
        Line Input #fn, lineread
        req = 0
        If InStr(lineread, "=") > 0 Then
            key = Mid(lineread, 1, InStr(lineread, "=") - 1)
            Path = Mid(lineread, InStr(lineread, "=") + 1)
            req = InStr(Path, ",required")
            If req > 0 Then
                Path = Mid(Path, 1, req - 1)
                
            End If
            Set Item = CollectionPaths.Add(key)
            Item.elem1 = key
            If InStr(Path, "\") > 0 Then
                Item.elem2 = Mid(Path, 1, InStrRev(Path, "\") - 1)
                Item.elem3 = Mid(Path, InStrRev(Path, "\") + 1)
            Else
                Item.elem2 = ""
                Item.elem3 = Path
            End If
            Item.elem4 = (req > 0)
        End If
    Wend
    Close fn
    Set ReadPaths = CollectionPaths
End Function

Function setFileTree(ByRef CollectionPaths As ColPair) As Boolean
    Dim Item As ClTempDirNodes
    
    Dim i As Long
    Dim filerequired As Boolean
    Dim test As Boolean
    
    Set FileTree.DirNodes = New Collection
        
    For i = 1 To CollectionPaths.Count
        Set Item = New ClTempDirNodes
        
        Item.key = CollectionPaths(i).elem1
        Item.fullpath = CollectionPaths(i).elem2
        Item.text = CollectionPaths(i).elem3
        
        If CollectionPaths(i).elem4 = True Then
        
        'Item.key
            test = False
            
            If Item.text = "" Then
                test = True
            Else
                If FileExist(Item.fullpath, Item.text) Then
                   test = True
                Else
                    If FileExist(Item.fullpath, Item.text + ".mst") Then
                       test = True
                    Else
                        If FileExist(Item.fullpath, Item.text + ".ifp") Then
                           test = True
                        Else
                            If FileExist(Item.fullpath, Item.text + ".fst") Then
                               test = True
                            Else
                            
                            End If
                        End If
                    End If
                End If
            End If
            If Not test Then Call FileExist(Item.fullpath, Item.text, Item.key)
            filerequired = Not test
        End If
        Call FileTree.DirNodes.Add(Item, Item.key)
    Next
    setFileTree = (Not filerequired)
End Function
Function getScieloUrl(acron As String) As String
    Dim fn As Long
    Dim content As String
    Dim P As Long
    Dim url As String
    
    fn = FreeFile
    If Not (FileTree.DirNodes("SciELO URL") Is Nothing) Then
        Open FileTree.DirNodes("SciELO URL").fullpath + "\" + FileTree.DirNodes("SciELO URL").text For Input As fn
        content = Input(LOF(fn), fn)
        Close fn
        P = InStr(content, acron + "|")
        If P > 0 Then
            url = Mid(content, P + Len(acron + "|"))
            url = Mid(url, 1, InStr(url, "|") - 1)
        End If
        
    End If
    getScieloUrl = url
End Function


