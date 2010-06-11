VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "clsXMLTools2"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Private mvar_XML_TOOLS As clsXMLToolsMS
Property Set XML_TOOLS(x As clsXMLToolsMS)
    Set mvarXML_TOOLS = x
End Property
Property Get XML_TOOLS() As clsXMLToolsMS
    Set XML_TOOLS = mvarXML_TOOLS
End Property

Public Sub setXMLTools(v As String)
'    Select Case v
'    Case "ms"
        Set XML_TOOLS = New clsXMLToolsMS
'    Case "java"
'        Set XML_TOOLS = New clsXMLToolsJava
'    End Select
End Sub


Public Function validateXML(xmlContent As String, encoding As String, xsdFileName As String, showMessage As Boolean, xmlError As String) As Boolean
        If loadxml(xmlContent, encoding, xsdFileName, xmlError) Then
            validateXML = True
        Else
            If showMessage Then
                Call MsgBox(xmlError, vbInformation)
            End If
        End If
End Function
Public Function transformXML(xmlContent As String, encoding As String, xsdFileName As String, xslFileName As String, showMessage As Boolean, ByVal xmlError As String) As String
    If loadXSL(xslFileName) Then
        If loadxml(xmlContent, encoding, xsdFileName, xmlError) Then
            transformXML = XML_TOOLS.transform()
        Else
            If showMessage Then
                Call MsgBox(xmlError, vbInformation)
            End If
        End If
    End If

End Function
Public Sub insertProcessingInstruction(xml As String, ByVal encoding As String)
'MsgBox "loadXML"
On Error GoTo error

    If InStr(xml, "<?xml") = 0 Then
        xml = "<?xml version=" & Chr(34) & "1.0" & Chr(34) & " encoding=" & Chr(34) & encoding & Chr(34) & "?>" & xml
    End If
    If InStr(xml, "<?xml") > 1 Then
        xml = Mid(xml, InStr(xml, "<?xml"))
    End If
    Exit Sub
error:
    MsgBox "clsXMLTools.insertProcessingInstruction " & ERR.description
End Sub

Private Function loadXSL(xslFileName As String) As Boolean

    If Dir(xslFileName) = Mid(xslFileName, InStrRev(xslFileName, "\") + 1) Then
        loadXSL = XML_TOOLS.loadXSL(xslFileName)
    Else
        MsgBox "clsXMLTools.loadXSL - Failure: No XSL " & xslFileName
    End If
    
    
End Function

Private Function loadxml(xmlContent As String, encoding As String, xsdFileName As String, xmlError As String) As Boolean
    If Len(encoding) > 0 Then
        Call insertProcessingInstruction(xmlContent, encoding)
    End If
    If XML_TOOLS.loadxml(xmlContent, xsdFileName, xmlError) Then
        loadxml = True
    Else
    End If
End Function



