VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "clsConverterXML_Java"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Private MVAR_JavaExe As String
Private MVAR_XMLTOOLSPATH As String

Private xsl As String
Private xml As String
Public logFile As clsLogFile

Function loadXSL(xslFileName As String) As Boolean
    On Error GoTo show_error
    xsl = xslFileName
    loadXSL = True
    Exit Function
show_error:
    MsgBox "clsConverterXML_Java.loadxsl " & err.description

End Function

Function loadxml(xmlcontent As String) As Boolean
    Call logFile.writelogFile(" clsConverterXML_Java.loadxml")
    loadxml = loadxmlCommon(xmlcontent, "")
End Function
Function loadxmlFile(xmlfilename As String) As Boolean
    Call logFile.writelogFile(" clsConverterXML_Java.loadxmlFile")
    loadxmlFile = loadxmlCommon("", xmlfilename)
End Function
Private Function loadxmlCommon(xmlcontent As String, xmlfile As String) As Boolean
    
    Dim doc As Document
    
    On Error GoTo show_error
    
    If Len(xmlcontent) > 0 Then
        
        xml = MarkupPrg & "temp\java.loadxmlCommon1." & replace(CStr(Time), ":", "-") & ".xml"
        
        Set doc = Documents.add(Visible:=False)
        doc.range.text = Trim(xmlcontent)
        Call logFile.writelogFile(" clsConverterXML_Java.loadxmlCommon cria xml: " & xml)
        
        If Len(xmlcontent) > 90 Then
            Call logFile.writelogFile(" clsConverterXML_Java.loadxmlCommon ultimos 100 caracteres do conteudo: " & Mid(xmlcontent, Len(xmlcontent) - 100))
        Else
            Call logFile.writelogFile(" clsConverterXML_Java.loadxmlCommon  conteudo: " & xmlcontent)
        
        End If
        Call doc.SaveAs(filename:=xml, addtorecentfiles:=False, fileFormat:=wdFormatText, encoding:=msoEncodingUTF8)
        doc.Close
        Set doc = Nothing
        
        Call logFile.writelogFile(" clsConverterXML_Java.loadxmlCommon cria o arquivo: " & xml)
    Else
        If xmlfile = "" Then
            xml = MarkupPrg & "temp\java.loadxmlCommon2." & replace(CStr(Time), ":", "-") & ".xml"
        Else
            xml = xmlfile
        End If
        Call logFile.writelogFile(" clsConverterXML_Java.loadxmlCommon usa o arquivo: " & xml)
    End If
    loadxmlCommon = True
    Exit Function
show_error:
    MsgBox "clsConverterXML_Java.loadxmlcommon " & vbCrLf & err.description & vbCrLf & tracing
End Function

Function validateXML(xsdFileName As String, errorFileName As String, errorMsg As String) As Boolean
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
        Call logFile.writelogFile(" clsConverterXML_Java.validatexml validateDTD")
        validate = "--validate"
    End If
    
    Call logFile.writelogFile(" clsConverterXML_Java.validatexml : " & xml)
    
    ctrlFileName = MarkupPrg & "temp\validate.ctrl"
    
    Call logFile.writelogFile(" clsConverterXML_Java.validatexml delete ctrlFileName: " & ctrlFileName)
    If f.existFile(ctrlFileName) Then f.DeleteFile (ctrlFileName)
    Call logFile.writelogFile(" clsConverterXML_Java.validatexml delete errorFileName: " & errorFileName)
    If f.existFile(errorFileName) Then f.DeleteFile (errorFileName)
    
    'call_validation = MVAR_XMLTOOLSPATH & "\call_validate.bat " & parameter(ctrlFileName) & parameter(MVAR_JavaExe) & parameter(MVAR_XMLTOOLSPATH) & parameter(xml) & parameter(errorFileName) & parameter(validate)
    'Call Shell(call_validation, vbHide)
    
    
    Dim p As String
    p = parameter(ctrlFileName) & parameter(MVAR_JavaExe) & parameter(MVAR_XMLTOOLSPATH) & parameter(xml) & parameter(errorFileName) & parameter(validate)
    errorMsg = ExecuteShellScript(MVAR_XMLTOOLSPATH, "call_validate.bat", p, ctrlFileName, errorFileName, "", glTimer, logFile)
    
    r = (InStr(LCase(errorMsg), "error") = 0)
    Call logFile.writelogFile(" clsConverterXML_Java.validatexml result " & CStr(r))
    If r Then errorMsg = ""

    Call logFile.writelogFile(" clsConverterXML_Java.validatexml delete ctrlFileName: " & ctrlFileName)
    If f.existFile(ctrlFileName) Then f.DeleteFile (ctrlFileName)
    Call logFile.writelogFile(" clsConverterXML_Java.validatexml delete errorFileName: " & errorFileName)
    If f.existFile(errorFileName) Then f.DeleteFile (errorFileName)
    
    Call logFile.writelogFile(" clsConverterXML_Java.validatexml fim ")
    
    validateXML = r
    Exit Function
show_error:
    MsgBox "clsConverterXML_Java.validatexml " & vbCrLf & err.description
End Function
Function transform(ByVal transfErrorFileName As String, Optional resultFileName As String) As String
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
    
    Call logFile.writelogFile("clsConverterXML_Java.transform inicio")
    Call logFile.writelogFile("clsConverterXML_Java.transform ResultFileName = " & resultFileName)
    Call logFile.writelogFile("clsConverterXML_Java.transform xml = " & xml)
    
    
    If Len(resultFileName) > 0 Then
        TransformationResultFileName = resultFileName
    Else
        TransformationResultFileName = xml & ".txt"
    End If
    ctrlFileName = MarkupPrg & "\temp\transf.ctrl"
    
    Call logFile.writelogFile("clsConverterXML_Java.transform delete TransformationResultFileName: " & TransformationResultFileName)
    If f.existFile(TransformationResultFileName) Then f.DeleteFile (TransformationResultFileName)
    
    Call logFile.writelogFile("clsConverterXML_Java.transform delete ctrlFileName: " & ctrlFileName)
    If f.existFile(ctrlFileName) Then f.DeleteFile (ctrlFileName)
    
    Call logFile.writelogFile("clsConverterXML_Java.transform use xml: " & TransformationResultFileName)
    
    Dim parameters As String
    parameters = parameter(MVAR_JavaExe) & parameter(MVAR_XMLTOOLSPATH) & parameter(xml) & parameter(xsl) & parameter(resultFileName) & parameter(transfErrorFileName) & parameter(ctrlFileName)
    TransformationResult = ExecuteShellScript(MVAR_XMLTOOLSPATH, "call_transform.bat", parameters, ctrlFileName, TransformationResultFileName, "", glTimer, logFile)
    
    Call logFile.writelogFile("clsConverterXML_Java.transform fim")
    
    If f.existFile(ctrlFileName) Then
        f.DeleteFile (ctrlFileName)
    End If
    transform = TransformationResult
    Exit Function
show_error:
    MsgBox "clsConverterXML_Java.transform " & err.description & " " & tracing
End Function

Property Let JavaExe(v As String)
    MVAR_JavaExe = v
End Property
Property Let XMLTOOLSPATH(v As String)
    MVAR_XMLTOOLSPATH = v
End Property


Private Function parameter(S As String) As String
    Dim r As String
    r = S
    If InStr(S, " ") > 0 Then
        r = Chr(34) & S & Chr(34)
    End If
    parameter = r & " "
End Function

