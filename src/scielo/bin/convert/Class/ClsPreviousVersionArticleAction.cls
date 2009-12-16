VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
  Persistable = 0  'NotPersistable
  DataBindingBehavior = 0  'vbNone
  DataSourceBehavior  = 0  'vbNone
  MTSTransactionMode  = 0  'NotAnMTSObject
END
Attribute VB_Name = "ClsPreviousVersionArticleAction"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = False
Attribute VB_Exposed = False
Option Explicit

Private mvarArticleAction As ClsArticleAction

Private Function findPreviousVersionArticleData(previousIssue As ClsRelatedIssues, article As ClsArticle) As ClsArticle
    
    mvarArticleAction.initDAO (previousIssue)
    
    Set findPreviousVersionArticleData = mvarArticleAction.ArticleDAO.findDocument(article)
End Function


Function archive(previousIssue As ClsRelatedIssues, article As ClsArticle) As ClsArticle
    Set findPreviousVersionArticleData = artDAO.findDocument(article)
End Function

Public Property Get ArticleAction() As ClsArticleAction
    Set ArticleAction = mvarArticleAction
End Property

Public Property Set ArticleAction(ByVal vNewValue As ClsArticleAction)
    Set mvarArticleAction = vNewValue
End Property
