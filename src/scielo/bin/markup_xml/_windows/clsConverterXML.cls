VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "clsConverterXML"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Private XML_Tools As Object
Private tracing As String
Private logFile As clsLogFile

Public Sub setXMLTools(v As String, parlogfile As clsLogFile)
    
    Select Case v
    Case "ms"
        Set XML_Tools = New clsConverterXML_MS
        XML_Tools.local_msgInfoXMLError = "... fixme "
    Case "java"
        Set XML_Tools = New clsConverterXML_Java
        XML_Tools.JavaExe = "java"
        XML_Tools.XMLTOOLSPATH = replace(MarkupPrg, "\markup\", "\XMLTools")
    End Select
    Set logFile = parlogfile
    Set XML_Tools.logFile = parlogfile
    
End Sub


Public Function validateXML(xmlcontent As String, DTDorSchemaFileName As String, errFileName As String, errMsg As String) As Boolean
    On Error GoTo show_error
    
    Call logFile.writelogFile("clsConverterXML.validateXML")
    
    If XML_Tools.loadxml(xmlcontent) Then
        Call logFile.writelogFile("clsConverterXML.validateXML xml loaded")
        validateXML = XML_Tools.validateXML(DTDorSchemaFileName, errFileName, errMsg)
        Call logFile.writelogFile("clsConverterXML.validateXML fim")
    End If
    Exit Function
show_error:
    MsgBox "clsconverterXML.validateXML " & err.description
End Function

Public Function validateXMLFile(xmlfilename As String, DTDorSchemaFileName As String, errFileName As String, errMsg As String) As Boolean
    On Error GoTo show_error
    Call logFile.writelogFile("clsConverterXML.validateXMLFile")
    
    If XML_Tools.loadxmlFile(xmlfilename) Then
        validateXMLFile = XML_Tools.validateXML(DTDorSchemaFileName, errFileName, errMsg)
    End If
    Exit Function
show_error:
    MsgBox "clsconverterXML.validateXMLFile " & err.description
End Function

Public Function transformXML(xmlcontent As String, ByVal xslFileName As String, ByVal validateXML As Boolean, ByVal errorFileName As String, Optional TransformationResultFileName As String) As String
    On Error GoTo show_error
    Dim res As String
    Dim errMsg As String

    Call logFile.writelogFile("clsconverterXML.transformXML inicio:" & xslFileName & " => " & TransformationResultFileName)
    
    Call logFile.writelogFile("clsconverterXML.transformXML loadXSL xsl:" & xslFileName)
    If loadXSL(xslFileName) Then
        Call logFile.writelogFile("clsconverterXML.transformXML loadXML")
        Call logFile.writelogFile(xmlcontent)
        If XML_Tools.loadxml(xmlcontent) Then
            Call logFile.writelogFile("clsconverterXML.transformXML XML_TOOLS.validateXML ")
            If validateXML Then
                If XML_Tools.validateXML("", errorFileName, errMsg) Then
                    Call logFile.writelogFile("clsconverterXML.transformXML XML_TOOLS.transform ")
                    res = XML_Tools.transform(errorFileName, TransformationResultFileName)
                End If
            Else
                Call logFile.writelogFile("clsconverterXML.transformXML XML_TOOLS.transform ")
                res = XML_Tools.transform(errorFileName, TransformationResultFileName)
            End If
        End If
    End If
    Call logFile.writelogFile("clsconverterXML.transformXML fim")
    transformXML = res
    Exit Function
show_error:
    MsgBox "clsconverterXML.transformXML " & err.description & vbCrLf & tracing
End Function

Public Sub insertProcessingInstruction(xml As String, ByVal encoding As String)
'MsgBox "loadXML"
On Error GoTo error
    Call logFile.writelogFile(" clsConverterXML.insertProcessingInstruction 1 ")

    If InStr(xml, "<?xml") = 0 Then
        xml = "<?xml version=" & Chr(34) & "1.0" & Chr(34) & " encoding=" & Chr(34) & encoding & Chr(34) & "?>" & xml
    End If
    Call logFile.writelogFile(" clsConverterXML.insertProcessingInstruction 2 ")
    If InStr(xml, "<?xml") > 1 Then
        xml = Mid(xml, InStr(xml, "<?xml"))
    End If
    Call logFile.writelogFile(" clsConverterXML.insertProcessingInstruction 3 ")
    Exit Sub
error:
    MsgBox "clsConverterXML.insertProcessingInstruction " & err.description
End Sub

Private Function loadXSL(xslFileName As String) As Boolean
    If dir(xslFileName) = Mid(xslFileName, InStrRev(xslFileName, "\") + 1) Then
        loadXSL = XML_Tools.loadXSL(xslFileName)
    Else
        MsgBox "clsConverterXML.loadXSL - Failure: No XSL " & xslFileName
    End If
End Function

