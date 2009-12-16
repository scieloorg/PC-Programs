Attribute VB_Name = "ModParser"


Declare Sub SGMLDocGetErrorMsg Lib "SGMLPars.dll" (ByVal ErrorCode As Long, ByVal ErrorMsg As String, ByVal MsgLen As Long)
Declare Function SGMLDocParse Lib "SGMLPars.dll" (ByVal DocFile As String, ByVal MaxErrors As Long, ByVal MaxMsgLen As Long, ByRef ErrorsLen As Long, ByVal Errors As String) As Long
Declare Function SGMLDocParserInfoFile Lib "SGMLPars.dll" (ByVal DocFile As String, ByVal CTableFile As String, ByVal OutputFile As String) As Long
Declare Function SGMLDocPrepareForParsing Lib "SGMLPars.dll" (ByVal DocFile As String, ByVal SGMLDeclFile As String, ByVal DTDName As String, ByVal DTDFile As String) As Long

