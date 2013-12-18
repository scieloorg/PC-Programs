VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "clsConverterXML_MS"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False

'Private xslt As New MSXML2.XSLTemplate30
'Private xslDoc As New MSXML2.FreeThreadedDOMDocument30
'Private xmlDoc As New MSXML2.DOMDocument30

Private xslt As New MSXML2.XSLTemplate30
Private xslDoc As New MSXML2.FreeThreadedDOMDocument30
Private xmlDoc As New MSXML2.DOMDocument30
Public logFile As clsLogFile
Public local_msgInfoXMLError As String


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

Function loadxml(xmlcontent As String) As Boolean
    loadxml = loadxmlCommon(xmlcontent, "")
End Function
Function loadxmlFile(xmlfilename As String) As Boolean
    loadxmlFile = loadxmlCommon("", xmlfilename)
End Function

Private Function loadxmlCommon(xmlcontent As String, xmlfilename As String) As Boolean
    Dim xsdCache As New MSXML2.XMLSchemaCache
    Dim xml As String
    Dim r As Boolean
    Dim msgInfoXMLError As String
    Dim errFileName As String
    
    On Error GoTo show_error
    Call logFile.writelogFile(" clsConverterXML_MS.loadxml 1 ")
    
    xmlDoc.async = False
    Call logFile.writelogFile(" clsConverterXML_MS.loadxml 2 ")
    
        
    If Len(xmlcontent) > 0 Then
        r = xmlDoc.loadxml(xmlcontent)
    Else
        If Len(xmlfilename) > 0 Then
            r = xmlDoc.load(xmlfilename)
        End If
    End If
    
    Call logFile.writelogFile(" clsConverterXML_MS.loadxml 4 ")
    
    
    Call parse(errFileName, msgInfoXMLError)
    
    
    Call logFile.writelogFile(" clsConverterXML_MS.loadxml 11 ")
    loadxmlCommon = (Len(msgInfoXMLError) = 0)
    Exit Function
show_error:
    MsgBox "clsConverterXML_MS.loadxml  " & err.description & tracing
    
End Function
Private Function parse(ByVal errFileName As String, ByRef errorMsg As String) As Boolean
    If (xmlDoc.parseError.ErrorCode <> 0) Then
        Dim myerr
        Dim x As String
        Dim c As String
        Dim Msg As New clsMessageWithParameters
    
        Call logFile.writelogFile(" clsConverterXML_MS.parse")
        Set myerr = xmlDoc.parseError
        
        Call logFile.writelogFile(" clsConverterXML_MS.parse 2")
        Msg.addParam (myerr.reason)
        
        Call logFile.writelogFile(" clsConverterXML_MS.parse 3")
        Msg.addParam (CStr(myerr.ErrorCode))
        
        Call logFile.writelogFile(" clsConverterXML_MS.parse 4")
        xml = xmlDoc.xml
        
        Call logFile.writelogFile(" clsConverterXML_MS.parse 5")
        If Len(xml) > 0 Then
            Call logFile.writelogFile(" clsConverterXML_MS.parse 6")
            x = Mid(xml, xmlDoc.parseError.filepos, 200)
            
            Call logFile.writelogFile(" clsConverterXML_MS.parse 7")
            c = Mid(x, 1, 1)
            
            Call logFile.writelogFile(" clsConverterXML_MS.parse 8")
            Msg.addParam (CStr(Asc(c)))
            
            Call logFile.writelogFile(" clsConverterXML_MS.parse 9")
            Msg.addParam (x)
        End If
        Call logFile.writelogFile(" clsConverterXML_MS.parse 10 ")
        errorMsg = Msg.getMessage(local_msgInfoXMLError)
        If Len(errFileName) > 0 Then
            Dim fn As Long
            fn = FreeFile
            Open errFileName For Output As fn
            Print #fn, errorMsg
            Close fn
        End If
    End If
    Call logFile.writelogFile(" clsConverterXML_MS.parse 11 ")
End Function
Function validateXML(xsdFileName As String, errorFileName As String, errorMsg As String) As Boolean
    Dim xsdCache As New MSXML2.XMLSchemaCache
    Dim xml As String
    Dim r As Boolean
    
    
    On Error GoTo show_error
    Call logFile.writelogFile(" clsConverterXML_MS.validatexml 1 ")
        
    If Len(xsdFileName) > 0 Then
        Call xsdCache.add("", xsdFileName)
        xmlDoc.schemas = xsdCache
    End If
    Call logFile.writelogFile(" clsConverterXML_MS.validatexml 3 ")
        
    r = xmlDoc.loadxml(xmlDoc.xml)
        
    
    Call logFile.writelogFile(" clsConverterXML_MS.validatexml 4 ")
    
    Call parse(errorFileName, errorMsg)
    
    Call logFile.writelogFile(" clsConverterXML_MS.validatexml 10 ")
    If Len(xsdFileName) > 0 Then
        Set xmlDoc.schemas = Nothing
    End If
    
    Call logFile.writelogFile(" clsConverterXML_MS.validatexml 11 ")
    trac = trac & tracing
    validateXML = r
    Exit Function
show_error:
    MsgBox "clsConverterXML_MS.validatexml  " & err.description & tracing
    
End Function
Function transform(ByVal transfErrorFileName As String, Optional resFileName As String) As String
    Dim xslPRoc As IXSLProcessor
    
    Dim doc As Document
    Dim xml As String
    Dim trac As String
    
    On Error GoTo show_error
    
    Set xslPRoc = xslt.createProcessor()
    xslPRoc.input = xmlDoc
    xslPRoc.transform
    xml = xslPRoc.output
    If Len(resFileName) > 0 Then
        Set doc = Documents.add(Visible:=False)
        doc.range.text = replace(xml, "UTF-16", "UTF-8")
        Call doc.SaveAs(filename:=resFileName, addtorecentfiles:=False, fileFormat:=wdFormatText, encoding:=msoEncodingUTF8)
        doc.Close
        Set doc = Nothing
    End If
    transform = xml
    Exit Function
show_error:
    MsgBox "clsConverterXML_MS.transform " & err.description & trac
End Function

