Attribute VB_Name = "Converter"
Option Explicit


Public Const CONST_SUBFIELDINDICATOR = "^"
Public Const CONST_VALIDSUBFIELDS = "[a-z1-9]"

Public Const CONST_SPACE_END_for_HTML = " "
Public Const CONST_DELIM1 = "<"
Public Const CONST_DELIM2 = ">"

Public Const CONST_CHANGE_FIELDS_PREVIOUS = "CHANGE_FIELDS=1"
Public Const CONST_CHANGE_FIELDS_ISSN = "CHANGE_FIELDS=2"
'Public Const CONST_CHANGE_FIELDS_SYMBOL = "CHANGE_FIELDS=3"
'Public Const CONST_CHANGE_FIELDS_SPECIALCHR = "CHANGE_FIELDS=4"

Type TpPosition
    i As Long
    j As Long
    
End Type

'Variaveis de configuracao
Public MKPERRDISPLAYED As String
Public DEFAULTBROWSERPATH As String
Public help As String
Public CONVERT_97_TO_2000 As String
Private MULT_REF_IN_PARAGRAPH As String
Public ReferenceSeparators() As String

Public IdiomHelp   As ColIdiom
Public BV As ColBV
Public AppHandle    As Long
Public Msg As ClMsg

Public ConvertDirTree As ClTree
Public COMMONISISTAGS As ColTag

Private CfgRec As ClCfgRec
Private Estatistic As ClMsg
Private PathBody As String
Private PathMarkup As String
Private PathBase As String
Private ArqBase As String
Private PathLog As String
Private ArqLog As String

Public mainConfig As ColPair


Private currentidiom As String
Private currentbv As String

Public EXISTDELETEDRECORDS As Boolean
Public Entities As New ClsEntities

Public Property Get Currbv() As String
    Currbv = currentbv
End Property

Public Property Let Currbv(ByRef bvirtual As String)
  Dim ret As Boolean

  
  If StrComp(currentbv, LCase(bvirtual), vbTextCompare) <> 0 Then
    
    With BV(LCase(bvirtual))
    'Initiate the Configuration of the Current Virtual Library
    If .BVConfigGet(ConvertDirTree.DirNodes("Library Directory").fullpath) Then
        'Initiate the bv directory structure / Check the path of the files
        
        'FIXME_DIR
        'Set .FileTree = New ClTree
        'FormMenu.BVDirStruct.Nodes.Clear
        'Call .FileTree.MakeTree(.BVPath + PathSep + .BVdirstructure, FormMenu.BVDirStruct.Nodes, FormMenu.WorkDir.path)
        
        If .setFileTree(.ReadPaths(.BVPathsConfigurationFile)) Then
            'Load the files used to converter program
            If .LoadFilestoConverterProgram Then
                FormMenu.SetLabels
                ret = True
                currentbv = LCase(bvirtual)
            End If
        End If
    End If
    
    End With
  End If

End Property

'Public Function CheckCurrbv() As Boolean
'    Dim ret As Boolean
'
'
'    With BV(Currbv)
'    'Initiate the Configuration of the Current Virtual Library
'    If .BVConfigGet(ConvertDirTree.DirNodes("Library Directory").FullPath) Then
'        'Initiate the bv directory structure / Check the path of the files
'        Set .FileTree = new ClTree
'        FormMenu.BVDirStruct.Nodes.Clear
'        Call .FileTree.MakeTree(.BVPath + PathSep + .BVdirstructure, FormMenu.BVDirStruct.Nodes, FormMenu.WorkDir.Path)
'
'        'Load the files used to converter program
'        If .LoadFilestoConverterProgram Then
'            FormMenu.SetLabels
'            ret = True
'        End If
'    End If
'    End With
'    CheckCurrbv = ret
'End Function

Public Property Get CurrIdiomHelp() As String
    CurrIdiomHelp = currentidiom
End Property

Public Property Let CurrIdiomHelp(idiom As String)
    UpdateInterface (IdiomHelp(idiom).code)
    FormMenu.SetLabels
    currentidiom = idiom
End Property

Sub ShowMsgInForm(ByVal mens As String)
    FormMarkup.LabRightMsg.Caption = mens
    FormMarkup.LabRightMsg.Refresh
End Sub

Private Sub Main()
    Dim CONVERTER_PROGRAM_INITIALIZATION As Boolean
    
    'Initiate the application in isis dll
    AppHandle = IsisAppNew()
    Call IsisAppDebug(AppHandle, DEBUG_LIGHT)
    
    ' Read ..\scielo_paths.ini
    readMainConfigFile
    
    'Initiate global variables
    Set Msg = New ClMsg

    'Read the ini file, which will set the global variables
    'Initiate the converter program directory structure / Check the path of the files
    Set ConvertDirTree = New ClTree
    FormMenu.DirStruct.Nodes.Clear
    Call ConvertDirTree.MakeTree("paths.txt", FormMenu.DirStruct.Nodes, FormMenu.WorkDir.Path)
        
    If ConfigGet Then
        'Open Menu
        FormMenu.OpenMenu
        
        'Load the files used to converter program
        If LoadFilestoConverterProgram Then
            CONVERTER_PROGRAM_INITIALIZATION = True
        End If
    End If
    
    If Not CONVERTER_PROGRAM_INITIALIZATION Then
        TerminateConverterProgram (True)
    End If
End Sub


Sub TerminateConverterProgram(unloadmenu As Boolean)
    
    Set Msg = Nothing
    Set ConvertDirTree = Nothing
    Set BV = Nothing
    Set IdiomHelp = Nothing
    Set CvtTables = Nothing
    Set CvtTabLanguage = Nothing
    Set COMMONISISTAGS = Nothing
    Set InterfaceLabels = Nothing
    Set CfgRec = Nothing
    Set ASCIIList = Nothing

    
    If unloadmenu Then Unload FormMenu
    
    
    
    End
End Sub

'------------------------------------------------------------------------
'ConfigGet - Read the convert.ini file and set values to global variables
'------------------------------------------------------------------------
Private Function ConfigGet() As Boolean
    Dim fn As Long
    Dim P As Long
    Dim q As Long
    Dim InputLine As String
    Dim SECTION As String
    Dim Value() As String
    Dim key As String
    Dim NewIdiomHelp As ClIdiom
    Dim ctab As ClCvtTab
    Dim bvitem As ClBV
    Dim ERROR As Boolean
    Dim idiom As String
    Dim bibvirtual As String
    
    Set IdiomHelp = New ColIdiom
    Set CvtTables = New Collection
    Set CvtTabLanguage = New Collection
    Set BV = New ColBV
    Set COMMONISISTAGS = New ColTag
    
    fn = FreeFile(1)
    
    Open CONVERTINIFILE For Input As fn
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
                    MKPERRDISPLAYED = Value(2)
                    Input #fn, key, DEFAULTBROWSERPATH
                    Input #fn, key, idiom
                    Input #fn, key, bibvirtual
                    Input #fn, key, help
                    Input #fn, key, CONVERT_97_TO_2000
                    Input #fn, key, MULT_REF_IN_PARAGRAPH
                    
                Else
                    ERROR = True
                End If
            Case "[GIZMOS]"
                If q = 1 Then
                    Set ctab = New ClCvtTab
                    ctab.key = Value(1)
                    Call CvtTables.Add(ctab, Value(1))
                Else
                    ERROR = True
                End If
            Case "[IDIOM CONVERSION TABLES]"
                If q = 1 Then
                    Set ctab = New ClCvtTab
                    ctab.key = Value(1)
                    Call CvtTabLanguage.Add(ctab, Value(1))
                Else
                    ERROR = True
                End If
            Case "[IdiomHelp]"
                If q = 2 Then
                    Set NewIdiomHelp = New ClIdiom
                    Set NewIdiomHelp = IdiomHelp.Add(Value(2), Value(1), Value(1), Value(1))
                Else
                    ERROR = True
                End If
            Case "[BV]"
                If q = 4 Or q = 5 Then
                    Set bvitem = New ClBV
                    Set bvitem = BV.Add(LCase(Value(1)))
                    bvitem.BVKey = LCase(Value(1))
                    bvitem.BVname = Value(1)
                    bvitem.BVconfigurationfile = Value(2)
                    bvitem.BVdirstructure = Value(3)
                    bvitem.Icon = Value(4)
                    If q = 5 Then bvitem.BVPathsConfigurationFile = Value(5)
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
                        Call COMMONISISTAGS.Add(Value(3), key, CLng(Value(1)), Value(2), key)
                    Else
                        ERROR = True
                    End If
                Else
                    ERROR = True
                End If
            End Select
        End If
    Wend
    Close fn
    
    LoadReferenceSeparator
    
    CurrIdiomHelp = idiom
    Currbv = bibvirtual
    
    If ERROR Then
        MsgBox InterfaceLabels("MsgINIFileFailure").elem2 + InputLine
    End If
    ConfigGet = Not ERROR
End Function

'------------------------------------------------------------------------
'ConfigSet - Write the convert.ini file
'------------------------------------------------------------------------
Public Sub ConfigSet()
    Dim fn As Long
    Dim i As Long
    
    fn = FreeFile(1)
    
    
    Open CONVERTINIFILE For Output As fn
    Print #fn, "[Variables]"
    Write #fn, "MKPERRDISPLAYED", MKPERRDISPLAYED
    Write #fn, "DEFAULTBROWSERPATH", DEFAULTBROWSERPATH
    Write #fn, "CurrIdiomHelp", CurrIdiomHelp
    Write #fn, "CurrBV", Currbv
    Write #fn, "Help", help
    Write #fn, "CONVERT_97_TO_2000", CONVERT_97_TO_2000
    Write #fn, "MULT_REF_IN_PARAGRAPH", MULT_REF_IN_PARAGRAPH
    
    If IdiomHelp.Count > 0 Then
        Print #fn,
        Print #fn, "[IdiomHelp]"
        For i = 1 To IdiomHelp.Count
            With IdiomHelp(i)
            Print #fn, .Label + SEP_CONVERTINI + .code
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
       
    If BV.Count > 0 Then
        Print #fn,
        Print #fn, "[BV]"
        For i = 1 To BV.Count
            With BV(i)
            Print #fn, .BVname + SEP_CONVERTINI + .BVconfigurationfile + SEP_CONVERTINI + .BVdirstructure + SEP_CONVERTINI + .Icon + SEP_CONVERTINI + .BVPathsConfigurationFile
            End With
        Next
    End If
       
    If COMMONISISTAGS.Count > 0 Then
        Print #fn,
        Print #fn, "[Tags]"
        For i = 1 To COMMONISISTAGS.Count
            With COMMONISISTAGS(i)
            Print #fn, .key + EQUALSIGNAL + CStr(.Value) + SEP_CONVERTINI + .Subf + SEP_CONVERTINI + .Label
            End With
        Next
    End If
    
    Close fn
End Sub


'--------------------------------------------------------------------------------
'BodyFileName - Return the Body file name based to the markup file name
'MarkupFileName   - INPUT - markup file name
'Return - the body file name if it exists or otherwise return an empty string
'--------------------------------------------------------------------------------
Public Function BodyFileName(MarkupFileName As String) As String
    Dim file2 As String
    
    If FileExist(PathBody, MarkupFileName) Then
        file2 = MarkupFileName
    Else
        If (InStr(1, MarkupFileName, ".html", vbTextCompare) > 0) Then
            file2 = Mid(MarkupFileName, 1, Len(MarkupFileName) - 1)
        ElseIf InStr(1, MarkupFileName, ".htm", vbTextCompare) > 0 Then
            file2 = MarkupFileName + "l"
        End If
    End If
    If Len(file2) > 0 Then
        If Not FileExist(PathBody, file2, "Body Document") Then file2 = ""
    End If
    BodyFileName = file2
End Function

'--------------------------------------------------------------------------------
'MakeConversion - Make the conversion process for a document
'DocMarkup  - markup file name
'DocBody    - body file name
'Return     - <True> to success, <False> to failure
'--------------------------------------------------------------------------------
Function MakeConversion(ByVal DocMarkup As String, ByVal DocBody As String, ByVal DocDB As String, Optional epubdate As String) As Boolean
    Dim BD As ClDBDoc
    Dim InitialTime As Date
    Dim NoErrorFound As Boolean
    Dim ConfigOK    As Boolean
    Dim OrderOK     As Boolean
    Dim DocConfigRecord As String
    Dim PartialT    As String
    Dim ErrorCount  As Long
    Dim docReader   As ClDocReader
    Dim ConversionOK As Boolean
    Dim DocId As String
    Dim ret As Boolean
    Dim RefLinkError As Boolean
    Dim epubDateError As Boolean
    Dim docOrder As String
    
    'Dim others As Boolean
    
    Dim ArticleAction As New ClsArticleAction
    Dim journalDirstructure As New ClJournalDirStructure
    
    Call journalDirstructure.setDirStructure(PathMarkup)
    Call ArticleAction.init(journalDirstructure.relatedissues)
            
    

    'initial time
    InitialTime = Time
    
    If Len(DocDB) = 0 Then DocDB = ArqBase
    
    'Copy the article.fst, used to invert the document database
    If Not FileExist(PathBase + PathSep + DocDB + ".fst", "fst file of library") Then Call FileCopy(ConvertDirTree.DirNodes("Library Directory").fullpath + "\" + Currbv + "\" + Currbv + ".fst", PathBase + PathSep + DocDB + ".fst")

    'Initiate the document database
    Set BD = New ClDBDoc
    If BD.Initiate(PathBase, DocDB, BV(Currbv).FileTree.DirNodes("Database Directory").key) Then
        
        If (BV(Currbv).DatabaseNameFormat = "FILENAME") Then
            BD.DBDel
            'Import the configuration record to the Document Database
            If Len(BV(Currbv).Directory.ReturnCfgRecKey) > 0 Then
                If BD.CfgRecImport(CfgRec.CfgRecord) Then
                    ret = True
                End If
            Else
                ret = True
            End If
        Else
            ret = True
        End If
    Else
        ret = True
    End If
    
    If ret Then
        Call Msg.InitLogDatabase(PathLog, ArqLog)
        Call Msg.GiveRunInformation("", , True)
        Call Msg.GiveRunInformation(DocMarkup, , True)
        Call Msg.GiveRunInformation(InterfaceLabels("MsgProcessBegin").elem2, , True)
        
        
        'Initiate the document
        Set docReader = New ClDocReader
        Call docReader.ArticleAction.init(journalDirstructure.relatedissues)
            
        
        'Check whether the DTD in document is accepted by the conversion program
        If docReader.MARKUP_IsValidDTD(PathMarkup, DocMarkup) Then
            
            'Verify if the document attributes are according to the configuration record
            ConfigOK = CfgRec.CfgRecCheck(docReader.MARKUP_DocConfigRecord(DocMarkup, docOrder))
                        
            OrderOK = ArticleAction.OrderCheck(DocMarkup, docOrder)
            
            'others = docReader.MARKUP_CheckArticleDates(epubdate) And docReader.MARKUP_checkPreviousPIDs
            
            'Parse the document and get the data
            NoErrorFound = docReader.MARKUP_ParseDoc(PathMarkup, DocMarkup, Msg.MsgDir, Msg.MsgFile, ErrorCount)
            If NoErrorFound And ConfigOK And OrderOK And docReader.MARKUP_checkPreviousPIDs Then
                
            
                ' DocId
                epubDateError = Not docReader.MARKUP_CheckArticleDates(epubdate)
                DocId = CfgRec.ReturnDocId(BV(Currbv).BuildDocId)
                If Len(DocId) = 0 Then
                    DocId = DocMarkup
                End If
                                                   
                'Build the database structure
                Set BD.Records = docReader.DB_BuildDocDatabase(DocId, PathMarkup, DocMarkup, PathBody, DocBody, PathBase + "\" + DocDB, BD.ImportCfgRecordContent("v151"), BD.ImportCfgRecordContent("(if v43^l='" + CfgRec.ImportDocRecordContent("if v706='h' then v40 fi") + "' then |^m|v43^m,|^a|v43^a fi)"), BD.ImportCfgRecordContent(BV(Currbv).EletronicMediumPft(LCase(BD.ImportCfgRecordContent("v930")))), RefLinkError)
                If Not (BD.Records Is Nothing) Then
                
                    'Save document in database
                    If BD.DOCSave(DocId) Then
                        ConversionOK = True
                    Else
                        If BD.DOCDel(DocId) Then
                            ConversionOK = False
                        End If
                    End If
                End If
            End If
            
        End If
        Set docReader = Nothing
        
        'Processing Time of the Document
        PartialT = CStr(DateDiff("s", InitialTime, Time))
        
        If ConversionOK Then
            Call Msg.GiveRunInformation(InterfaceLabels("MsgLoadedDatabase").elem2)
            If (BV(Currbv).DatabaseNameFormat = "FILENAME") Then
                BD.FinishDocConversion
            End If
        Else
            Call Msg.GiveRunInformation(InterfaceLabels("MsgNotLoadedDatabase").elem2)
        End If
        
        Call Msg.GiveRunInformation(InterfaceLabels("MsgProcessEnd").elem2, , True)
        Call Msg.GiveRunInformation(InterfaceLabels("MsgTokenTime").elem2 + PartialT)
        
        'Write the processing time in the statistic file
        Call Estatistic.GiveRunInformation(DocDB + vbTab + DocMarkup + vbTab + PartialT)
            
        Call Msg.WriteLogDatabase(DocMarkup, PathBase + PathSep + DocDB, ConversionOK, (ErrorCount > 0) Or RefLinkError Or epubDateError)
        
        
    End If
    Set BD = Nothing
    
    MakeConversion = ConversionOK
End Function

'--------------------------------------------------------------------------------
'FinishDBConversion - Make some processes in database document after loading all the
'selected files
'--------------------------------------------------------------------------------
Sub FinishDBConversion()
    Dim BD As ClDBDoc
    
    Set BD = New ClDBDoc
    If BD.Initiate(PathBase, ArqBase, BV(Currbv).FileTree.DirNodes("Database Directory").key) Then
        'BD.ChangeReferencesFieldContent
        'Call BD.TranslateGreekChar(ConvertdirTree.DirNodes("Symbol Conversion Table").Parent.FullPath, ConvertdirTree.DirNodes("Symbol Conversion Table").Text)
        'BD.ManualReplacement
        Call Msg.GiveRunInformation("", , True)
        Call BD.FinishDocConversion   '(ConvertdirTree.DirNodes("Symbol Conversion Table").Parent.FullPath, ConvertdirTree.DirNodes("Symbol Conversion Table").Text)
    End If
    Set BD = Nothing
    
End Sub


Function ReadISSNFILE(ISSNBASES As ColISSNDB, NOSERTITLE As ClISSNDB) As Boolean
    Dim fn As Long
    Dim SECTION As String
    Dim Linha As String
    Dim Value() As String
    Dim q As Long
    Dim fim As Boolean
    Dim aux As String
    Dim paux As String
    Dim issnbase As ClISSNDB
    
    fn = FreeFile(1)
    Open BV(Currbv).BVPath + "\issndb.ini" For Input As fn
    
    Set ISSNBASES = New ColISSNDB
    Set NOSERTITLE = New ClISSNDB
    
    While Not EOF(fn) And (Not fim)
        Line Input #fn, Linha
        
        q = GetElemStr(Linha, SEP_ISSNDBINI, Value)
        
        Select Case q
        Case 1
            SECTION = Linha
        Case 5
            Set issnbase = New ClISSNDB
            Set issnbase = ISSNBASES.Add(Value(1))
            aux = Value(3) + "|"
            paux = InStr(aux, "|")
            While paux > 0
                issnbase.sertitle_tag(issnbase.SertitleCount + 1) = CLng(Mid(aux, 1, paux - 1))
                aux = Mid(aux, paux + 1)
                paux = InStr(aux, "|")
            Wend
            issnbase.ISSN_tag = CLng(Value(2))
            issnbase.StandardSertitle_tag = CLng(Value(4))
            issnbase.FST_File_key = Value(5)
        Case 2
            Set NOSERTITLE = New ClISSNDB
            NOSERTITLE.key = Value(1)
            NOSERTITLE.sertitle_tag(NOSERTITLE.SertitleCount + 1) = Value(2)
        Case Else
            fim = True
        End Select
    Wend
    
    Close fn
    If fim Then
        MsgBox InterfaceLabels("MsgISSNFILEFailure").elem2 + Linha
    End If
    
    ReadISSNFILE = Not fim
End Function

'--------------------------------------------------------------------------------
'LoadFilestoConverterProgram - Load the files used to the converter program
'Return - Sucess or failure
'--------------------------------------------------------------------------------
Private Function LoadFilestoConverterProgram() As Boolean
    Dim ret As Boolean
    Dim i As Long
        
    'Check the existence of the files
    If ConvertDirTree.CheckFilePath Then
            'Load the HTML tags table
            ret = True
            ret = ret And LoadHTMLTagsTable
            
            'Load the HTML to ASCII Conversion List
            ret = ret And LoadHTML2ASCIIList
            
            'Load the character conversion tables
            For i = 1 To CvtTables.Count
                With ConvertDirTree.DirNodes(CvtTables(i).key)
                ret = ret And CvtTables(i).ReadTable(.Parent.fullpath, .text, "|")
                End With
            Next
            
            'Load the character conversion tables depending on the language
            For i = 1 To CvtTabLanguage.Count
                With ConvertDirTree.DirNodes(CvtTabLanguage(i).key)
                ret = ret And CvtTabLanguage(i).ReadTable(.Parent.fullpath, .text, "|")
                End With
            Next
            
    End If
    
    FormMenu.MousePointer = vbArrow
    
    LoadFilestoConverterProgram = ret
End Function

'--------------------------------------------------------------------------------
'SetSelectedDir - Check all the files used to the conversion process of a
'selected document group
'--------------------------------------------------------------------------------
Public Function SetSelectedDir(SelectedPath As String, FileCounter As Long) As Boolean
    Dim ret As Boolean
    Dim BD As ClDBDoc
    
    'Set Markup path
    PathMarkup = SelectedPath + BV(Currbv).FileTree.DirNodes("Markup Directory").text
    
    'Set Database Directory and File
    ArqBase = BV(Currbv).Directory.ReturnDatabaseName
    If Len(BV(Currbv).FileTree.DirNodes("Database Directory").text) = 0 Then
        PathBase = SelectedPath + BV(Currbv).Directory.ReturnDatabaseDir
    Else
        PathBase = SelectedPath + BV(Currbv).FileTree.DirNodes("Database Directory").text
    End If
    
    
    'Set Log Directory and File
    If StrComp(BV(Currbv).FileTree.DirNodes("Log Directory").text, BV(Currbv).FileTree.DirNodes("Database Directory").text, vbTextCompare) = 0 Then
        PathLog = PathBase
        ArqLog = ArqBase + "log"
        Msg.MsgDir = PathLog
        Msg.MsgFile = ArqBase + ".log"
        
        If Not FileExist(PathLog, ArqLog + ".mst") Then
            PathLog = PathBase
            ArqLog = "log"
            Msg.MsgDir = PathLog
            Msg.MsgFile = "db.log"
        End If
        
    Else
        PathLog = SelectedPath + BV(Currbv).FileTree.DirNodes("Log Directory").text
        ArqLog = BV(Currbv).FileTree.DirNodes("Log File").text
        Msg.MsgDir = PathLog
        Msg.MsgFile = ArqLog + ".log"
    End If
    Call Msg.InitLogDatabase(PathLog, ArqLog)
   
    'Check Body directory
    If BV(Currbv).HasFulltext Then
        PathBody = SelectedPath + BV(Currbv).FileTree.DirNodes("Body Directory").text
        If DirExist(PathBody, BV(Currbv).FileTree.DirNodes("Body Directory").key) Then
            ret = True
        End If
    Else
        ret = True
    End If
    
    If ret Then
        ret = False
        'Check Markup directory
        If DirExist(PathMarkup, BV(Currbv).FileTree.DirNodes("Markup Directory").key) Then
            'Create Base and Log directories if they do not exist
            If Not DirExist(PathBase) Then MakeDir PathBase
            If Not DirExist(PathLog) Then MakeDir PathLog
            
            'Check Database directory
            If DirExist(PathBase, BV(Currbv).FileTree.DirNodes("Database Directory").key) Then
            
                'Create the statistic file to this issue
                Set Estatistic = New ClMsg
                Estatistic.MsgDir = PathBase
                Estatistic.MsgFile = BV(Currbv).FileTree.DirNodes("Statistic File").text
    
                'Get the Configuration Record from the Configuration Database
                Set CfgRec = New ClCfgRec
    
                'Copy the log.fst, used to invert the log database
                If CfgRec.CfgRecordSet(BV(Currbv).Directory.ReturnCfgRecKey) Then
                    ret = True
                End If
                If Not FileExist(PathLog + PathSep + ArqLog + ".fst", "fst file of " + BV(Currbv).FileTree.DirNodes("Log Directory").key) And FileExist(ConvertDirTree.DirNodes("FST log").Parent.fullpath, ConvertDirTree.DirNodes("FST log").text, ConvertDirTree.DirNodes("FST log").key) Then Call FileCopy(ConvertDirTree.DirNodes("Conversion Table Directory").fullpath + PathSep + ConvertDirTree.DirNodes("FST log").text, PathLog + PathSep + ArqLog + ".fst")

                'Todos os documentos em uma base
                If Len(BV(Currbv).DatabaseNameFormat) = 0 Then
                    
                    'Copy the article.fst, used to invert the document database
                    If Not FileExist(PathBase + PathSep + ArqBase + ".fst", "fst file of library") Then Call FileCopy(ConvertDirTree.DirNodes("Library Directory").fullpath + "\" + Currbv + "\" + Currbv + ".fst", PathBase + PathSep + ArqBase + ".fst")
                        
                    'Initiate the document database
                    Set BD = New ClDBDoc
                    If BD.Initiate(PathBase, ArqBase, BV(Currbv).FileTree.DirNodes("Database Directory").key) Then
                        'Import the configuration record to the Document Database
                        If Len(BV(Currbv).Directory.ReturnCfgRecKey) > 0 Then
                            If BD.CfgRecImport(CfgRec.CfgRecord) Then
                                ret = True
                                FileCounter = CfgRec.DocCounter
                            End If
                        Else
                            ret = True
                        End If
                    End If
                    Set BD = Nothing
                Else
                    ret = True
                End If
            End If
        End If
    End If
    SetSelectedDir = ret
End Function


Private Sub LoadReferenceSeparator()
    If Len(MULT_REF_IN_PARAGRAPH) > 0 Then
        ReferenceSeparators = Split(MULT_REF_IN_PARAGRAPH, "|")
    End If
End Sub

Sub readMainConfigFile()
    Dim v As String
    Dim lineread As String
    Dim fn As Long
    Dim key As String
    Dim P As ClPair
    
    Set mainConfig = New ColPair
    fn = FreeFile
    Open "..\scielo_paths.ini" For Input As fn
    While Not EOF(fn)
        Line Input #fn, lineread
        If InStr(lineread, "=") > 0 Then
            key = Mid(lineread, 1, InStr(lineread, "=") - 1)
            v = Mid(lineread, InStr(lineread, "=") + 1)
            
            Set P = mainConfig.Add(key)
            P.elem1 = key
            P.elem2 = v
            If InStr(v, ",") > 0 Then
                P.elem2 = Mid(v, 1, InStr(v, ",") - 1)
                P.elem3 = Mid(v, InStr(v, ",") + 1)
            End If
        End If
    Wend
    Close fn
End Sub

Sub openHelp(helpPath As String, helpFile As String)
        If FileExist(helpPath, IdiomHelp(CurrIdiomHelp).code + helpFile) Then
        
            Shell "cmd.exe /k  start" + Chr(32) + helpPath + "\" + IdiomHelp(CurrIdiomHelp).code + helpFile
        
        End If
End Sub

