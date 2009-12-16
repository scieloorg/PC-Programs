VERSION 5.00
Object = "{BDC217C8-ED16-11CD-956C-0000C04E4C0A}#1.1#0"; "TABCTL32.OCX"
Begin VB.Form FormConfig 
   Caption         =   "Configuration"
   ClientHeight    =   4980
   ClientLeft      =   1350
   ClientTop       =   945
   ClientWidth     =   7830
   Icon            =   "config.frx":0000
   LinkTopic       =   "Form5"
   PaletteMode     =   1  'UseZOrder
   ScaleHeight     =   4980
   ScaleWidth      =   7830
   StartUpPosition =   2  'CenterScreen
   Begin VB.CommandButton CmdAjuda 
      Caption         =   "Help"
      Height          =   375
      Left            =   6960
      TabIndex        =   12
      Top             =   2160
      Width           =   735
   End
   Begin VB.CommandButton CmdCan 
      Caption         =   "Cancel"
      Height          =   375
      Left            =   6960
      TabIndex        =   11
      Top             =   1560
      Width           =   735
   End
   Begin VB.CommandButton CmdOK 
      Caption         =   "OK"
      Height          =   375
      Left            =   6960
      TabIndex        =   10
      Top             =   960
      Width           =   735
   End
   Begin TabDlg.SSTab SSTabConfig 
      Height          =   4815
      Left            =   120
      TabIndex        =   0
      Top             =   120
      Width           =   6615
      _ExtentX        =   11668
      _ExtentY        =   8493
      _Version        =   327680
      Tabs            =   4
      Tab             =   2
      TabsPerRow      =   4
      TabHeight       =   529
      BeginProperty Font {0BE35203-8F91-11CE-9DE3-00AA004BB851} 
         Name            =   "MS Sans Serif"
         Size            =   8.25
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      TabCaption(0)   =   "Directory Tree"
      TabPicture(0)   =   "config.frx":030A
      Tab(0).ControlCount=   0
      Tab(0).ControlEnabled=   0   'False
      TabCaption(1)   =   "Tags"
      TabPicture(1)   =   "config.frx":0326
      Tab(1).ControlCount=   0
      Tab(1).ControlEnabled=   0   'False
      TabCaption(2)   =   "Others"
      TabPicture(2)   =   "config.frx":0342
      Tab(2).ControlCount=   4
      Tab(2).ControlEnabled=   -1  'True
      Tab(2).Control(0)=   "FramTpLiterat"
      Tab(2).Control(0).Enabled=   0   'False
      Tab(2).Control(1)=   "FramOrdReg"
      Tab(2).Control(1).Enabled=   0   'False
      Tab(2).Control(2)=   "FramSgl"
      Tab(2).Control(2).Enabled=   0   'False
      Tab(2).Control(3)=   "Frame1"
      Tab(2).Control(3).Enabled=   0   'False
      TabCaption(3)   =   "Parser"
      TabPicture(3)   =   "config.frx":035E
      Tab(3).ControlCount=   0
      Tab(3).ControlEnabled=   0   'False
      Begin VB.Frame Frame1 
         Caption         =   "Web Browser Program"
         Height          =   1455
         Left            =   120
         TabIndex        =   21
         Top             =   480
         Width           =   6255
         Begin VB.ComboBox ComboIdiomHelp 
            Height          =   315
            Left            =   120
            Sorted          =   -1  'True
            Style           =   2  'Dropdown List
            TabIndex        =   3
            Tag             =   "ComboIdiomHelp"
            Top             =   960
            Width           =   3255
         End
         Begin VB.CommandButton CmdFind 
            Caption         =   "Find"
            Height          =   375
            Left            =   5520
            TabIndex        =   2
            Top             =   240
            Width           =   615
         End
         Begin VB.TextBox TxtBrowserPath 
            Height          =   285
            Left            =   120
            Locked          =   -1  'True
            TabIndex        =   1
            Tag             =   "Text"
            Top             =   240
            Width           =   5175
         End
         Begin VB.Label Label1 
            Caption         =   "Idiom of Help Files"
            Height          =   255
            Left            =   120
            TabIndex        =   22
            Top             =   720
            Width           =   1335
         End
      End
      Begin VB.Frame FramSgl 
         Caption         =   "Sigla"
         Height          =   1815
         Left            =   120
         TabIndex        =   16
         Top             =   2880
         Width           =   2295
         Begin VB.TextBox TxtSupplVol 
            Height          =   285
            Left            =   1320
            TabIndex        =   7
            Tag             =   "Text"
            Top             =   720
            Width           =   855
         End
         Begin VB.TextBox TxtSupplNo 
            Height          =   285
            Left            =   1320
            TabIndex        =   9
            Tag             =   "Text"
            Top             =   1440
            Width           =   855
         End
         Begin VB.TextBox TxtSglNro 
            Height          =   285
            Left            =   1320
            TabIndex        =   8
            Tag             =   "Text"
            Top             =   1080
            Width           =   855
         End
         Begin VB.TextBox TxtSglVol 
            Height          =   285
            Left            =   1320
            TabIndex        =   6
            Tag             =   "Text"
            Top             =   360
            Width           =   855
         End
         Begin VB.Label LabSupplNo 
            Caption         =   "Supplement"
            Height          =   255
            Left            =   240
            TabIndex        =   20
            Top             =   1440
            Width           =   975
         End
         Begin VB.Label LabSupplVol 
            Caption         =   "Supplement"
            Height          =   255
            Left            =   240
            TabIndex        =   19
            Top             =   720
            Width           =   1095
         End
         Begin VB.Label LabSglVol 
            Caption         =   "Volume"
            Height          =   255
            Left            =   240
            TabIndex        =   18
            Top             =   360
            Width           =   855
         End
         Begin VB.Label LabSglNro 
            Caption         =   "Number"
            Height          =   255
            Left            =   240
            TabIndex        =   17
            Top             =   1080
            Width           =   855
         End
      End
      Begin VB.Frame FramOrdReg 
         Caption         =   "Record Order in Data Base"
         Height          =   855
         Left            =   2640
         TabIndex        =   14
         Top             =   2160
         Width           =   3735
         Begin VB.TextBox TxtOrdReg 
            Height          =   285
            Left            =   120
            TabIndex        =   5
            Tag             =   "Text"
            Top             =   480
            Width           =   3495
         End
         Begin VB.Label LabOrdReg 
            Caption         =   "outline,header,font,paragraph,citation,reference"
            Height          =   255
            Left            =   120
            TabIndex        =   15
            Top             =   240
            Width           =   3495
         End
      End
      Begin VB.Frame FramTpLiterat 
         Caption         =   "Literature Type"
         Height          =   615
         Left            =   120
         TabIndex        =   13
         Top             =   2160
         Width           =   2295
         Begin VB.ComboBox ComboTpLiterat 
            Height          =   315
            Left            =   120
            Style           =   2  'Dropdown List
            TabIndex        =   4
            Tag             =   "Combo"
            Top             =   240
            Width           =   2055
         End
      End
   End
End
Attribute VB_Name = "FormConfig"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit
