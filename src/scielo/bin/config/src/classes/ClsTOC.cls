VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClsTOC"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Public sections As ClsSections
Public names As ColTextByLang
Private dict As ClsDictionary
Sub loadDict()
    Dim i As Long
    Dim j As Long
    Dim termDict As ClsTerm
    Dim section As ClsSection
    Dim term As String
        
    Set dict = New ClsDictionary
    
    For i = 1 To sections.count
        
        Set section = sections.item(i)
        
        term = ""
        For j = 1 To section.sectionNames.count
            term = term + section.sectionNames.getItemByIndex(j).text
        Next
        
        Set termDict = dict.item(term)
        
        If termDict Is Nothing Then
            Set termDict = New ClsTerm
            termDict.term = term
            termDict.occurrences.add (section.sectionCode)
            Call dict.add(termDict, termDict.term)
        Else
            termDict.occurrences.add (section.sectionCode)
            
        End If
    Next
End Sub

Function existSectionName(sectionNames As String) As Collection
    Dim termDict As ClsTerm
    Dim r As Collection
    
    Set termDict = dict.item(sectionNames)
    If termDict Is Nothing Then
        Set r = Nothing
    Else
        Set r = termDict.occurrences
    End If
    Set existSectionName = r
End Function

Private Sub Class_Initialize()
    Set sections = New ClsSections
    Set names = New ColTextByLang
End Sub
