VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "clsConverterXML"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Private mErr As New clsErrList
Const errIDObj As String = "700"
Private mvarXSLToConvertXML As String
Private mvarXSDFile As String

Public doDebug As Boolean
Private debugResult As String

Private xslt As New MSXML2.XSLTemplate30
Private xslDoc As New MSXML2.FreeThreadedDOMDocument30
Private xmlDoc As New MSXML2.DOMDocument30

Public xmlError As String
Private xslProc As IXSLProcessor
    
Public Property Get xslToConvertXML() As String
    xslToConvertXML = mvarXSLToConvertXML
End Property

Public Property Let xslToConvertXML(ByVal vNewValue As String)
    mvarXSLToConvertXML = vNewValue
End Property

Public Property Get xsdFile() As String
    xsdFile = mvarXSDFile
End Property

Public Property Let xsdFile(ByVal vNewValue As String)
    mvarXSDFile = vNewValue
End Property

Function convert(XML_text As String, msgInfoXMLError As String) As String
    Dim res As String
    Dim r As Boolean
    
    On Error GoTo errlog
    
    debugResult = "convert XML " & xslToConvertXML
    If Dir(xslToConvertXML) = Mid(xslToConvertXML, InStrRev(xslToConvertXML, "\") + 1) Then
        res = convertXML(XML_text, msgInfoXMLError)
        If Len(res) > 0 Then
            r = True
        End If
    Else
        MsgBox "clsConverterXML.convert - Failure: No XSL " & xslToConvertXML
    End If
    If r Then
        convert = res
    Else
        If doDebug Then MsgBox "debugging: " & debugResult
    End If
    Exit Function
    
errlog:
    MsgBox "clsConverterXML.convert " & ERR.description
    MsgBox "debugging: " & debugResult
End Function

Private Function convertXML(textInXML As String, msgInfoXMLError As String) As String
    'Dim debugResult As String
    
    On Error GoTo errlog
    
debugResult = debugResult & vbCrLf & "convertXML 0 " & CStr(Time) & vbCrLf
    
    If callLoadXML(textInXML, "UTF-8", msgInfoXMLError, debugResult, True) Then
debugResult = debugResult & vbCrLf & "convertXML 00 " & CStr(Time) & vbCrLf
        If loadXSL() Then
debugResult = debugResult & vbCrLf & "convertXML 1 " & CStr(Time) & vbCrLf
    
            Set xslt.StyleSheet = xslDoc
debugResult = debugResult & vbCrLf & "convertXML 2 " & CStr(Time) & vbCrLf
            Set xslProc = xslt.createProcessor()
debugResult = debugResult & vbCrLf & "convertXML 3 " & CStr(Time) & vbCrLf
            xslProc.input = xmlDoc
debugResult = debugResult & vbCrLf & "convertXML 4 " & CStr(Time) & vbCrLf
        
            xslProc.transform
debugResult = debugResult & vbCrLf & "convertXML 5 " & CStr(Time) & vbCrLf
            convertXML = xslProc.output
        End If
    End If
'MsgBox debugResult
    Exit Function
    
errlog:
    MsgBox "clsConverterXML.convertXML " & ERR.description

End Function


Public Sub insertProcessingInstruction(xml As String, encoding As String)
'MsgBox "loadXML"

    If InStr(xml, "<?xml") = 0 Then
        xml = "<?xml version=" & Chr(34) & "1.0" & Chr(34) & " encoding=" & Chr(34) & encoding & Chr(34) & "?>" & xml
    End If
    If InStr(xml, "<?xml") > 1 Then
        xml = Mid(xml, InStr(xml, "<?xml"))
    End If
    
End Sub


Public Function callLoadXML(xml As String, encoding As String, msgInfoXMLError As String, ByRef tracing As String, Optional showMessage As Boolean) As Boolean

    
    
    On Error GoTo errlog
tracing = tracing & " callLoadXML 1   " & CStr(Time) & vbCrLf
    Call insertProcessingInstruction(xml, encoding)
    xmlDoc.async = False
tracing = tracing & " callLoadXML 2   " & CStr(Time) & vbCrLf
    
    If Len(xsdFile) > 0 Then
        Dim xsdCache As New MSXML2.XMLSchemaCache
        Call xsdCache.add("", xsdFile)
        xmlDoc.schemas = xsdCache
    End If
tracing = tracing & " callLoadXML 3   " & CStr(Time) & vbCrLf
    
    xmlDoc.loadxml xml
tracing = tracing & " callLoadXML 4   " & CStr(Time) & vbCrLf
    
    'MsgBox "error code " & xmlDoc.parseError.ErrorCode
    
    If (xmlDoc.parseError.ErrorCode <> 0) Then
        Dim myerr
        Dim x As String
        Dim c As String
        Dim msg As New clsMessageWithParameters
        
        Set myerr = xmlDoc.parseError
        
        x = Mid(xml, xmlDoc.parseError.filepos, 200)
        c = Mid(x, 1, 1)
tracing = tracing & " callLoadXML 5   " & CStr(Time) & vbCrLf
        
        msg.addParam (myerr.reason)
        msg.addParam (CStr(myerr.ErrorCode))
        msg.addParam (CStr(Asc(c)))
        msg.addParam (x)
tracing = tracing & " callLoadXML 6   " & CStr(Time) & vbCrLf
    
        xmlError = msg.getMessage(msgInfoXMLError)
tracing = tracing & " callLoadXML 7   " & CStr(Time) & vbCrLf
        
        If showMessage Then
tracing = tracing & " callLoadXML 8   " & CStr(Time) & vbCrLf
        
            Call MsgBox(xmlError, vbInformation)
        End If
    End If
tracing = tracing & " callLoadXML 9   " & CStr(Time) & vbCrLf
    If Len(xsdFile) > 0 Then
        Set xmlDoc.schemas = Nothing
    End If
    
tracing = tracing & " callLoadXML 10   " & CStr(Time) & vbCrLf
    
'MsgBox "loadXML"
    callLoadXML = (xmlDoc.parseError.ErrorCode = 0)
    Exit Function
errlog:
    MsgBox "clsConverterXML.callLoadXML " & ERR.description & vbCrLf & tracing
    
End Function
Private Function loadXSL() As Boolean
'MsgBox "loadXSL"
    xslDoc.async = False
    xslDoc.load xslToConvertXML
    
    If (xslDoc.parseError.ErrorCode <> 0) Then
       Dim myerr
       Set myerr = xslDoc.parseError
       MsgBox "Stylesheet error: " + myerr.reason
    End If
'MsgBox "loadXSL"
    
    loadXSL = (xslDoc.parseError.ErrorCode = 0)
End Function



