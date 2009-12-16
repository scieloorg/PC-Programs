Attribute VB_Name = "MdInterf"
Option Explicit

Public InterfaceLabels As ColPair

Sub UpdateInterface(idiom As String)

    Dim fn As Long
    Dim key As String
    Dim Value As String
    Dim Label As ClPair
    
    Set InterfaceLabels = New ColPair
    Set Label = New ClPair
    
    fn = FreeFile
    Open idiom + "_label.txt" For Input As fn
    While Not EOF(fn)
        Input #fn, key, Value
        Set Label = InterfaceLabels.Add(key)
        Label.elem1 = key
        Label.elem2 = Value
    Wend
    
Close fn
End Sub

