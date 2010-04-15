VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "cls_XMLToolsJava"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Private MVAR_JavaExe As String
Private MVAR_XMLTOOLSPATH As String

Private xsl As String
Private xml As String

Function loadXSL(xslFileName As String) As Boolean

    xsl = xslFileName
    loadXSL = True
End Function

Function loadxml(xmlContent As String, xsdFileName As String, msgInfoXMLError As String) As Boolean

    Dim fn As Long
    Dim Result As String
    
    xml = MarkupPrg & "\temp\xmltools.xml"
    
    fn = FreeFile
    Open xml For Output As fn
    Print #fn, xmlContent
    Close fn
    
    If Len(xsdFileName) > 0 Then
        Result = xml & ".err"
        Call Shell(MVAR_XMLTOOLSPATH & "\call_validate.bat " & MVAR_JavaExe & " " & MVAR_XMLTOOLSPATH & " " & xml & " " & xsdFileName & " " & Result, vbHide)
        
        fn = FreeFile
        Open Result For Input As fn
        Input #fn, msgInfoXMLError
        Close fn
        
        loadxml = (InStr(msgInfoXMLError, "finished") = 1)
        
    Else
        loadxml = True
    End If
    
    
End Function

Function transform() As String
    Dim Result As String
    Dim r As String
    
    Result = xml & ".res"
    
    Call Shell(MVAR_XMLTOOLSPATH & "\call_transform.bat " & MVAR_JavaExe & " " & MVAR_XMLTOOLSPATH & " " & xml & " " & xsl & " " & Result, vbHide)
    
    Dim fn As Long
    fn = FreeFile
    Open Result For Input As fn
    Input #fn, r
    Close fn
    transform = r
End Function

Property Let JavaExe(v As String)
    MVAR_JavaExe = v
End Property
Property Let XMLTOOLSPATH(v As String)
    MVAR_XMLTOOLSPATH = v
End Property

