VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "OldClsXMLTools"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Public logfile As clsLogFile
Private MVAR_JavaExe As String
Private MVAR_XMLTOOLSPATH As String


Property Let JavaExe(v As String)
    MVAR_JavaExe = v
End Property
Property Let XMLTOOLSPATH(v As String)
    MVAR_XMLTOOLSPATH = v
End Property

Function createXMLFile(xmlcontent As String, xmlfile As String) As Boolean
   
    Dim doc As Document
    
    On Error GoTo show_error
    
    If Len(xmlfile) = 0 Then
        MsgBox "clsXMLTools.createXML xmlFile missing"
    Else
        If Len(xmlcontent) = 0 Then
            MsgBox "clsXMLTools.createXML xmlcontent missing"
        Else
            Set doc = Documents.add(Visible:=False)
            doc.range.text = Trim(xmlcontent)
            Call logfile.writelogFile(" clsXMLTools.createxml cria: " & xmlfile)
            If Len(xmlcontent) > 500 Then
                Call logfile.writelogFile(" clsXMLTools.createxml conteudo: " & Mid(xmlcontent, Len(xmlcontent) - 100))
            Else
                Call logfile.writelogFile(" clsXMLTools.createxml conteudo: " & xmlcontent)
            End If
            Call doc.SaveAs(filename:=xmlfile, addtorecentfiles:=False, fileformat:=wdFormatEncodedText, encoding:=msoEncodingUTF8)
            doc.Close
            Set doc = Nothing
            createXMLFile = True
        End If
    End If
    Exit Function
show_error:
    MsgBox "clsXMLTools.createXMLFile " & vbCrLf & err.description
End Function
Public Function validateXMLFile(xmlfilename As String, xsdFileName As String, errorFileName As String, errorMsg As String) As Boolean
    Dim test As String
    Dim timer As Long
    Dim validate As String
    Dim call_validation As String
    Dim doc As Document
    Dim f As New clsFile
    Dim tracing As String
    Dim r As Boolean
    
    Dim ctrlFileName As String
    
    On Error GoTo show_error
    
    If Len(xsdFileName) > 0 Then
        Call logfile.writelogFile(" clsXMLTools.validateXMLFile validateDTD")
        validate = "--validate"
    End If
    
    Call logfile.writelogFile(" clsXMLTools.validateXMLFile : " & xmlfilename)
    
    ctrlFileName = MarkupPrg & "temp\validate.ctrl"
    
    Dim parameters As String
    parameters = parameter(ctrlFileName) & parameter(MVAR_JavaExe) & parameter(MVAR_XMLTOOLSPATH) & parameter(xmlfilename) & parameter(errorFileName) & validate
    errorMsg = ExecuteShellScript("", MVAR_XMLTOOLSPATH & "\call_validate.bat", parameters, ctrlFileName, errorFileName, "", glTimer, logfile)

    r = (InStr(LCase(errorMsg), "error") = 0)
    If r Then errorMsg = ""
    Call logfile.writelogFile(" clsXMLTools.validateXMLFile delete ctrlFileName: " & ctrlFileName)
    If f.existFile(ctrlFileName) Then f.DeleteFile (ctrlFileName)
    
    Call logfile.writelogFile(" clsXMLTools.validateXMLFile delete errorFileName: " & errorFileName)
    If f.existFile(errorFileName) Then f.DeleteFile (errorFileName)
    
    
    Call logfile.writelogFile(" clsXMLTools.validateXMLFile fim ")
    
    
    validateXMLFile = r
    Exit Function
show_error:
    MsgBox "clsXMLTools.validateXMLFile " & vbCrLf & err.description
End Function

Private Function parameter(s As String) As String
    Dim r As String
    r = s
    If InStr(s, " ") > 0 Then
        r = Chr(34) & s & Chr(34)
    End If
    parameter = r & " "
End Function
Public Function transformXMLFile(xmlfilename As String, ByVal xslFileName As String, ByVal validateXML As Boolean, ByVal errorFileName As String, Optional TransformationResultFileName As String) As String
    On Error GoTo show_error
    Dim res As String
    Dim errMsg As String
    Dim doTransformation As Boolean

    Call logfile.writelogFile("clsXMLTools.transformXMLFile inicio:" & xslFileName & " => " & TransformationResultFileName)
    
    Call logfile.writelogFile("clsXMLTools.transformXMLFile loadXSL xsl:" & xslFileName)
    If loadXSL(xslFileName) Then
        If validateXML Then
            Call logfile.writelogFile("clsXMLTools.transformXMLFile validateXML ")
            If validateXMLFile(xmlfilename, "", errorFileName, errMsg) Then
                doTransformation = True
            End If
        Else
            doTransformation = True
        End If
        If doTransformation Then
            Call logfile.writelogFile("clsXMLTools.transformXMLFile transform ")
            res = transform(xmlfilename, xslFileName, errorFileName, TransformationResultFileName)
        Else
            Call logfile.writelogFile("clsXMLTools.transformXMLFile nao validou xml de entrada!!!!!! ")
        End If
    End If
    Call logfile.writelogFile("clsXMLTools.transformXMLFile fim")
    transformXMLFile = res
    Exit Function
show_error:
    MsgBox "clsXMLTools.transformXMLFile " & err.description & vbCrLf & tracing
End Function

Public Sub insertProcessingInstruction(xml As String, ByVal encoding As String)
'MsgBox "loadXML"
On Error GoTo error
    Call logfile.writelogFile(" clsXMLTools.insertProcessingInstruction 1 ")

    If InStr(xml, "<?xml") = 0 Then
        xml = "<?xml version=" & Chr(34) & "1.0" & Chr(34) & " encoding=" & Chr(34) & encoding & Chr(34) & "?>" & xml
    End If
    Call logfile.writelogFile(" clsXMLTools.insertProcessingInstruction 2 ")
    If InStr(xml, "<?xml") > 1 Then
        xml = Mid(xml, InStr(xml, "<?xml"))
    End If
    Call logfile.writelogFile(" clsXMLTools.insertProcessingInstruction 3 ")
    Exit Sub
error:
    MsgBox "clsXMLTools.insertProcessingInstruction " & err.description
End Sub

Private Function loadXSL(xslFileName As String) As Boolean
    On Error GoTo show_error
    If dir(xslFileName) = Mid(xslFileName, InStrRev(xslFileName, "\") + 1) Then
        loadXSL = True
    Else
        MsgBox "clsXMLTools.loadXSL - Failure: No XSL " & xslFileName
    End If
    
    Exit Function
show_error:
    MsgBox "clsXMLTools.loadxsl " & err.description

End Function

Private Function transform(par_xmlFileName As String, par_xslFileName As String, ByVal transfErrorFileName As String, Optional resultFileName As String) As String
    Dim TransformationResultFileName As String
    Dim r As String
    Dim timer As Long
    Dim tracing As String
    
    Dim call_shell As String
    Dim TransformationResult As String
    Dim f As New clsFile
    Dim fn As Long
    Dim ctrlFileName As String
    
    On Error GoTo show_error
    
    Call logfile.writelogFile("clsXMLTools.transform inicio")
    Call logfile.writelogFile("clsXMLTools.transform ResultFileName = " & resultFileName)
    Call logfile.writelogFile("clsXMLTools.transform par_xmlFileName = " & par_xmlFileName)
    
    
    If Len(resultFileName) > 0 Then
        TransformationResultFileName = resultFileName
    Else
        TransformationResultFileName = par_xmlFileName & ".txt"
    End If
    ctrlFileName = MarkupPrg & "\temp\transf.ctrl"
    
    
    Call logfile.writelogFile("clsXMLTools.transform use par_xmlFileName: " & par_xmlFileName)
    
    
    Dim parameters As String
    parameters = parameter(MVAR_JavaExe) & parameter(MVAR_XMLTOOLSPATH) & parameter(par_xmlFileName) & parameter(par_xslFileName) & parameter(TransformationResultFileName) & parameter(transfErrorFileName) & parameter(ctrlFileName)
    'TransformationResult = ExecuteShellScript("", MVAR_XMLTOOLSPATH & "\call_transform.bat", parameters, ctrlFileName, TransformationResultFileName, "", glTimer, logfile)
    TransformationResult = ExecuteShellScript("", "python", MVAR_XMLTOOLSPATH & "\call_transform.py " & parameters, ctrlFileName, TransformationResultFileName, "", glTimer, logfile)
    
    Call logfile.writelogFile("clsXMLTools.transform fim")
    
    If f.existFile(ctrlFileName) Then
        f.DeleteFile (ctrlFileName)
    End If
    transform = TransformationResult
    Exit Function
show_error:
    MsgBox "clsXMLTools.transform " & err.description & " " & tracing
End Function

Function GenerateXMLandHTML(ByRef xmlfile As String, ByVal xsl_pmc As String, ByVal xsl_html As String, ByVal OUTPUT_XML_filename As String, ByVal OUTPUT_HTML_filename As String, ByRef errorFileName As String, issue_path As String, filename As String) As Boolean
    Dim f As New clsFile
    Dim r As Boolean
    Dim timer As Long
    Dim call_script As String
    Dim doit As Boolean
    Dim result As String
    Dim ctrlFileName As String
    Dim resultFileName As String
    
    On Error GoTo show_error
    
    
    
    
    Call logfile.writelogFile(" clsXMLTools.GenXMLHTML : " & xmlfile)
    
    'call_script = MVAR_XMLTOOLSPATH & "\gen_xml_html.bat " & parameter(MVAR_XMLTOOLSPATH) & parameter(xmlfile) & parameter(xsl_pmc) & parameter(xsl_html) & parameter(errorFileName) & parameter(OUTPUT_XML_filename) & parameter(OUTPUT_HTML_filename) & parameter(issue_path) & parameter(filename)
    'Call Shell(call_script, vbHide)
    'Call logFile.writelogFile(" clsXMLTools.GenXMLHTML executou " & call_script)
    Dim parameters As String
    parameters = parameter(MVAR_XMLTOOLSPATH) & parameter(xmlfile) & parameter(xsl_pmc) & parameter(xsl_html) & parameter(errorFileName) & parameter(OUTPUT_XML_filename) & parameter(OUTPUT_HTML_filename) & parameter(issue_path) & parameter(filename)
    
    result = ExecuteShellScript("", MVAR_XMLTOOLSPATH & "\gen_xml_html.bat", parameters, "", OUTPUT_HTML_filename, errorFileName, glTimer * 2, logfile)
    
    
    Call logfile.writelogFile(" clsXMLTools.GenXMLHTML fim ")
    GenerateXMLandHTML = r
    Exit Function
show_error:
    MsgBox "clsXMLTools.GenXMLHTML " & vbCrLf & err.description
    GenerateXMLandHTML = r
End Function


Function GenerateXMLandCheckStyle(ByRef xmlfile As String, ByVal xsl_pmc As String, ByVal xsl_html As String, ByVal OUTPUT_XML_filename As String, ByVal OUTPUT_HTML_filename As String, ByRef errorFileName As String, issue_path As String, filename As String) As Boolean
    Dim f As New clsFile
    Dim r As Boolean
    Dim timer As Long
    Dim call_script As String
    Dim doit As Boolean
    Dim result As String
    Dim ctrlFileName As String
    Dim resultFileName As String
    
    On Error GoTo show_error
    
    
    
    
    Call logfile.writelogFile(" clsXMLTools.GenerateXMLandCheckStyle : " & xmlfile)
    
    'call_script = MVAR_XMLTOOLSPATH & "\gen_xml_html.bat " & parameter(MVAR_XMLTOOLSPATH) & parameter(xmlfile) & parameter(xsl_pmc) & parameter(xsl_html) & parameter(errorFileName) & parameter(OUTPUT_XML_filename) & parameter(OUTPUT_HTML_filename) & parameter(issue_path) & parameter(filename)
    'Call Shell(call_script, vbHide)
    'Call logFile.writelogFile(" clsXMLTools.GenerateXMLandCheckStyle executou " & call_script)
    Dim parameters As String
    parameters = parameter(MVAR_XMLTOOLSPATH) & parameter(xmlfile) & parameter(xsl_pmc) & parameter(xsl_html) & parameter(errorFileName) & parameter(OUTPUT_XML_filename) & parameter(OUTPUT_HTML_filename) & parameter(issue_path) & parameter(filename)
    
    result = ExecuteShellScript("", MVAR_XMLTOOLSPATH & "\gen_xml_and_check.bat", parameters, "", OUTPUT_HTML_filename, errorFileName, glTimer * 2, logfile)
    
    
    Call logfile.writelogFile(" clsXMLTools.GenerateXMLandCheckStyle fim ")
    GenerateXMLandCheckStyle = r
    Exit Function
show_error:
    MsgBox "clsXMLTools.GenerateXMLandCheckStyle " & vbCrLf & err.description
    GenerateXMLandCheckStyle = r
End Function
