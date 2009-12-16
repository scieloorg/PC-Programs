VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClBody"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Private myhtml As New ClHTML
Private bodyNodes As New ClHTMLNodes

Function loadBody(Path As String, file As String) As Boolean
    Dim ret As Boolean
    Dim fn As Long
    Dim s As String
    Dim node As ClHTMLNode
    
    If FileExist(Path, file, "Fulltext") Then
                
        fn = FreeFile(1)
        Open Path + PathSep + file For Input As fn
        Do Until EOF(fn)
            Line Input #fn, s
            Set node = myhtml.loadHTML(s)
            Call bodyNodes.Add(node)
        Loop
        Close fn
        ret = True
    End If
    
    loadBody = ret
End Function

Function BODY_FindReferences(References() As String) As Boolean
    Dim ret As Boolean
    Dim i As Long
    Dim LimInf As TpPosition
    Dim LimSup As TpPosition
    Dim r As String
    Dim found As Boolean
    Dim node As New ClHTMLNode
    Dim reftagend As String, reftagstart As String
    Dim ReferencesCounter As Long
    
    reftagend = "</" + CStr(BV(Currbv).BVISISTAGS("ref").Value) + ">"
    reftagstart = "<" + CStr(BV(Currbv).BVISISTAGS("ref").Value) + ">"
    
    ret = True
    For i = 1 To ReferencesCounter
        'prepare references to compare them
        Call Msg.GiveRunInformation(CStr(i))
        Call Msg.GiveRunInformation(References(i))
        
        node = myhtml.loadHTML(References(i))
        
        found = FindReferenceInText(i, node.CleanedText, LimInf, LimSup)
        If Not found Then
            r = r + COMMA + CStr(i)
        End If
        
        'free memory
        ret = ret And found
    Next
    
    ReferencesCounter = 0
    Erase References
    
    If Not ret Then
        r = Mid(r, 2)
        Call Msg.GiveRunInformation(InterfaceLabels("MsgMissingReferences").elem2 + r)
    End If
End Function
'-----------------------------------------------------------------------
'BODY_FindReferenceInText - Find a reference in body file
'IdReference - index of the reference to find
'Reference - reference to find
'LimInf - initial position at the body to find the reference
'LimSup - final position of the reference found
'Return - <True> to success and <False> to failure
'-----------------------------------------------------------------------
Private Function FindReferenceInText(IdReference As Long, Reference As String, LimInf As TpPosition, LimSup As TpPosition) As Boolean
    Dim RefInitialPos As TpPosition
    Dim RefFinalPos As TpPosition
    Dim p1 As Long
    Dim CompleteReference As String
    Dim OK As Boolean
    Dim ReferenceMark As String
    Dim li As TpPosition
    Dim ls As TpPosition
    
    li = LimInf
    ls = LimSup
    
    Call CompressedInfo.New_InString(LimInf.i, LimInf.j, LimSup.i, LimSup.j, Reference, RefInitialPos.i, RefInitialPos.j, vbBinaryCompare)
    If RefInitialPos.j = 0 Then
        LimInf = li
        LimSup = ls
        Call CompressedInfo.New_InString(LimInf.i, LimInf.j, LimSup.i, LimSup.j, Reference, RefInitialPos.i, RefInitialPos.j, vbTextCompare)
    End If
    
    If RefInitialPos.j > 0 Then
        With CompressedInfo
        'Update the next start position (LimInf)
        RefFinalPos = RefInitialPos
        Call .ForwardPosition(RefFinalPos.i, RefFinalPos.j, Len(Reference))
        LimInf = RefFinalPos
    
        'Build the reference mark to insert into the complete text
        ReferenceMark = Trim(RmNewLineInStr(DB_TagContents(CStr(IdReference), BV(Currbv).BVISISTAGS("ref").Value)))
        
        'Calculate the position of the end of the reference in the complete text to insert the reference mark
        Call .RewardPosition(RefFinalPos.i, RefFinalPos.j, 1)
        CompleteReference = BODY_UnCompressLine(Mid(.GetLine(RefFinalPos.i), 1, RefFinalPos.j), CompressionInfo(RefFinalPos.i))
        RefFinalPos.j = Len(CompleteReference)
                
        End With
        
        With BODY_Text
        'Check the exact position to insert the reference mark
        If BODY_FindEndReference(RefFinalPos.i, RefFinalPos.j) Then
            'Insert the reference mark
            .SetLine(RefFinalPos.i) = Mid(.GetLine(RefFinalPos.i), 1, RefFinalPos.j) + ReferenceMark + STANDARDIZEDENDPARAG + Mid(.GetLine(RefFinalPos.i), RefFinalPos.j + 1)
            'Update the compression information
             CompressionInfo(RefFinalPos.i) = Mid(CompressionInfo(RefFinalPos.i), 1, RefFinalPos.j) + String(Len(ReferenceMark + STANDARDIZEDENDPARAG), "0") + Mid(CompressionInfo(RefFinalPos.i), RefFinalPos.j + 1)
            
            'Debug.Print "Reconheceu " + .GetLine(RefFinalPos.i)
            'CompressedInfo.SetLine(RefFinalPos.i) = BODY_CompressLine(.GetLine(RefFinalPos.i), CompressionInfo(RefFinalPos.i))
            'Debug.Print "BODY_CompressLine " + .GetLine(RefFinalPos.i)
            OK = True
        Else
            Debug.Print "Não Reconheceu " + .GetLine(RefFinalPos.i)
        End If
        End With
        
    Else
        Debug.Print Reference
        
    End If
    
    FindReferenceInText = OK
End Function
