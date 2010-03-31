VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "clsXMLToolsMS"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False

Private xslt As New MSXML2.XSLTemplate30
Private xslDoc As New MSXML2.FreeThreadedDOMDocument30
Private xmlDoc As New MSXML2.DOMDocument30



Function loadXSL(xslFileName As String) As Boolean
    xslDoc.async = False
    xslDoc.load xslFileName
    If (xslDoc.parseError.ErrorCode <> 0) Then
       Dim myerr
       Set myerr = xslDoc.parseError
       MsgBox "Stylesheet error: " + myerr.reason
       loadXSL = False
    Else
        Set xslt.StyleSheet = xslDoc
        loadXSL = True
    End If
End Function

Function loadxml(xmlContent As String, xsdFileName As String, msgInfoXMLError As String) As Boolean
    Dim xsdCache As New MSXML2.XMLSchemaCache
    
    xmlDoc.async = False
    
    
    If Len(xsdFileName) > 0 Then
        Call xsdCache.add("", xsdFileName)
        xmlDoc.schemas = xsdCache
    End If
        
    xmlDoc.loadxml xmlContent
    
    If (xmlDoc.parseError.ErrorCode <> 0) Then
        Dim myerr
        Dim x As String
        Dim c As String
        Dim msg As New clsMessageWithParameters
        
        Set myerr = xmlDoc.parseError
                          
        x = Mid(xml, xmlDoc.parseError.filepos, 200)
        c = Mid(x, 1, 1)
        
        msg.addParam (myerr.reason)
        msg.addParam (CStr(myerr.ErrorCode))
        msg.addParam (CStr(Asc(c)))
        msg.addParam (x)
    
        msgInfoXMLError = msg.getMessage(msgInfoXMLError)
        
    Else
        loadxml = True
    End If
    
tracing = tracing & " callLoadXML 9   " & CStr(Time) & vbCrLf
    If Len(xsdFileName) > 0 Then
        Set xmlDoc.schemas = Nothing
    End If
    
       
       
    
End Function

Function transform() As String
Dim xslProc As IXSLProcessor
Set xslProc = xslt.createProcessor()
    xslProc.input = xmlDoc
    xslProc.transform
    transform = xslProc.output
End Function
