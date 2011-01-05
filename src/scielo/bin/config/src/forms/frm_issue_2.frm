VERSION 5.00
Object = "{6B7E6392-850A-101B-AFC0-4210102A8DA7}#1.3#0"; "Comctl32.ocx"
Object = "{BDC217C8-ED16-11CD-956C-0000C04E4C0A}#1.1#0"; "Tabctl32.ocx"
Begin VB.Form Issue2 
   BorderStyle     =   1  'Fixed Single
   Caption         =   "Issue"
   ClientHeight    =   5700
   ClientLeft      =   1560
   ClientTop       =   2100
   ClientWidth     =   9060
   Icon            =   "frm_issue_2.frx":0000
   LinkTopic       =   "Form1"
   MaxButton       =   0   'False
   MinButton       =   0   'False
   Moveable        =   0   'False
   ScaleHeight     =   5700
   ScaleWidth      =   9060
   StartUpPosition =   2  'CenterScreen
   Begin VB.CommandButton CmdClose 
      Caption         =   "Close"
      Height          =   375
      Left            =   6960
      TabIndex        =   41
      Top             =   5280
      Width           =   855
   End
   Begin VB.CommandButton FormCmdSave 
      Caption         =   "Save"
      Height          =   375
      Left            =   5880
      TabIndex        =   40
      Top             =   5280
      Width           =   855
   End
   Begin VB.CommandButton FormCmdAju 
      Caption         =   "Help"
      Height          =   375
      Left            =   8040
      TabIndex        =   42
      Top             =   5280
      Width           =   855
   End
   Begin TabDlg.SSTab SSTab1 
      Height          =   5055
      Left            =   120
      TabIndex        =   43
      Top             =   120
      Width           =   8895
      _ExtentX        =   15690
      _ExtentY        =   8916
      _Version        =   393216
      Tabs            =   4
      TabsPerRow      =   4
      TabHeight       =   520
      TabCaption(0)   =   "General"
      TabPicture(0)   =   "frm_issue_2.frx":030A
      Tab(0).ControlEnabled=   -1  'True
      Tab(0).Control(0)=   "FramFasc2(0)"
      Tab(0).Control(0).Enabled=   0   'False
      Tab(0).ControlCount=   1
      TabCaption(1)   =   "Bibliographic Strip"
      TabPicture(1)   =   "frm_issue_2.frx":0326
      Tab(1).ControlEnabled=   0   'False
      Tab(1).Control(0)=   "FramLeg"
      Tab(1).Control(0).Enabled=   0   'False
      Tab(1).ControlCount=   1
      TabCaption(2)   =   "Table of Contents"
      TabPicture(2)   =   "frm_issue_2.frx":0342
      Tab(2).ControlEnabled=   0   'False
      Tab(2).Control(0)=   "Frame1"
      Tab(2).ControlCount=   1
      TabCaption(3)   =   "Settings"
      TabPicture(3)   =   "frm_issue_2.frx":035E
      Tab(3).ControlEnabled=   0   'False
      Tab(3).Control(0)=   "FrameCreativeCommons"
      Tab(3).Control(0).Enabled=   0   'False
      Tab(3).ControlCount=   1
      Begin VB.Frame FrameCreativeCommons 
         Caption         =   "Creative Commons"
         Height          =   4455
         Left            =   -74880
         TabIndex        =   100
         Top             =   480
         Width           =   8535
         Begin VB.ComboBox ComboIssueLicText 
            Height          =   315
            Left            =   1560
            Style           =   2  'Dropdown List
            TabIndex        =   108
            Top             =   360
            Width           =   3135
         End
         Begin VB.TextBox TextCreativeCommons 
            Height          =   975
            Index           =   2
            Left            =   1560
            Locked          =   -1  'True
            MultiLine       =   -1  'True
            TabIndex        =   103
            Top             =   3120
            Width           =   6855
         End
         Begin VB.TextBox TextCreativeCommons 
            Height          =   975
            Index           =   1
            Left            =   1560
            Locked          =   -1  'True
            MultiLine       =   -1  'True
            TabIndex        =   102
            Top             =   2040
            Width           =   6855
         End
         Begin VB.TextBox TextCreativeCommons 
            Height          =   975
            Index           =   0
            Left            =   1560
            Locked          =   -1  'True
            MultiLine       =   -1  'True
            TabIndex        =   101
            Top             =   960
            Width           =   6855
         End
         Begin VB.Label Label10 
            Caption         =   "Espanhol"
            Height          =   255
            Index           =   2
            Left            =   120
            TabIndex        =   106
            Top             =   3120
            Width           =   1335
         End
         Begin VB.Label Label10 
            Caption         =   "Português"
            Height          =   255
            Index           =   1
            Left            =   120
            TabIndex        =   105
            Top             =   2040
            Width           =   1335
         End
         Begin VB.Label Label10 
            Caption         =   "Inglês"
            Height          =   255
            Index           =   0
            Left            =   120
            TabIndex        =   104
            Top             =   960
            Width           =   1335
         End
      End
      Begin VB.Frame FramFasc2 
         Height          =   4575
         Index           =   0
         Left            =   120
         TabIndex        =   74
         Top             =   360
         Width           =   8535
         Begin VB.ComboBox Text_issueissn 
            Height          =   315
            Left            =   6360
            Style           =   2  'Dropdown List
            TabIndex        =   109
            Top             =   2280
            Width           =   2055
         End
         Begin VB.ListBox ListScheme 
            Height          =   960
            Left            =   6120
            Style           =   1  'Checkbox
            TabIndex        =   99
            Top             =   3360
            Width           =   2295
         End
         Begin VB.TextBox TxtIssTitle 
            Height          =   285
            Index           =   2
            Left            =   1440
            TabIndex        =   95
            Top             =   1560
            Width           =   4095
         End
         Begin VB.TextBox TxtIssTitle 
            Height          =   285
            Index           =   1
            Left            =   1440
            TabIndex        =   94
            Top             =   1200
            Width           =   4095
         End
         Begin VB.CheckBox MkpCheck 
            Caption         =   "Ready to the Local Site"
            Height          =   495
            Left            =   6120
            TabIndex        =   9
            Top             =   2640
            Width           =   2055
         End
         Begin VB.ComboBox ComboStandard 
            Height          =   315
            Left            =   240
            TabIndex        =   8
            Top             =   4080
            Width           =   5295
         End
         Begin VB.TextBox TxtIssSponsor 
            Height          =   285
            Left            =   240
            TabIndex        =   7
            Top             =   3360
            Width           =   5295
         End
         Begin VB.TextBox TxtIssTitle 
            Height          =   285
            Index           =   3
            Left            =   1440
            TabIndex        =   3
            Top             =   1920
            Width           =   4095
         End
         Begin VB.TextBox TxtIssPublisher 
            Height          =   285
            Left            =   240
            TabIndex        =   5
            Top             =   2640
            Width           =   5295
         End
         Begin VB.TextBox TxtIssuept 
            Height          =   285
            Left            =   6360
            TabIndex        =   4
            Top             =   1080
            Width           =   1935
         End
         Begin VB.TextBox TxtCover 
            Height          =   285
            Left            =   6360
            TabIndex        =   6
            Top             =   1680
            Width           =   1935
         End
         Begin VB.TextBox TxtDateIso 
            Height          =   285
            Left            =   6360
            TabIndex        =   2
            Text            =   "9999"
            Top             =   480
            Width           =   1935
         End
         Begin VB.TextBox TxtDoccount 
            Height          =   285
            Left            =   3840
            TabIndex        =   1
            Top             =   480
            Width           =   1695
         End
         Begin VB.ComboBox ComboStatus 
            Height          =   315
            Left            =   240
            Style           =   2  'Dropdown List
            TabIndex        =   0
            Top             =   480
            Width           =   3375
         End
         Begin VB.Label LabelIssueISSN 
            AutoSize        =   -1  'True
            Caption         =   "Issue ISSN"
            Height          =   195
            Left            =   6360
            TabIndex        =   107
            Top             =   2040
            Width           =   795
         End
         Begin VB.Label LabIdiom2 
            Alignment       =   1  'Right Justify
            AutoSize        =   -1  'True
            Caption         =   "Portuguese"
            Height          =   195
            Index           =   1
            Left            =   600
            TabIndex        =   98
            Top             =   1200
            Width           =   810
         End
         Begin VB.Label LabIdiom2 
            Alignment       =   1  'Right Justify
            AutoSize        =   -1  'True
            Caption         =   "Spanish"
            Height          =   195
            Index           =   2
            Left            =   840
            TabIndex        =   97
            Top             =   1560
            Width           =   570
         End
         Begin VB.Label LabIdiom2 
            Alignment       =   1  'Right Justify
            AutoSize        =   -1  'True
            Caption         =   "English"
            Height          =   195
            Index           =   3
            Left            =   840
            TabIndex        =   96
            Top             =   1920
            Width           =   510
         End
         Begin VB.Label LabScheme 
            AutoSize        =   -1  'True
            Caption         =   "Scheme"
            Height          =   195
            Left            =   6120
            TabIndex        =   88
            Top             =   3120
            Width           =   1665
         End
         Begin VB.Label LabStandard 
            AutoSize        =   -1  'True
            Caption         =   "Standard"
            Height          =   195
            Left            =   240
            TabIndex        =   87
            Top             =   3840
            Width           =   645
         End
         Begin VB.Label LabIssSponsor 
            AutoSize        =   -1  'True
            Caption         =   "Sponsor"
            Height          =   195
            Left            =   240
            TabIndex        =   82
            Top             =   3120
            Width           =   585
         End
         Begin VB.Label LabFascTitulo 
            AutoSize        =   -1  'True
            Caption         =   "Title"
            Height          =   195
            Left            =   240
            TabIndex        =   81
            Top             =   960
            Width           =   300
         End
         Begin VB.Label LabEditorEspecial 
            AutoSize        =   -1  'True
            Caption         =   "Editor"
            Height          =   195
            Left            =   240
            TabIndex        =   80
            Top             =   2400
            Width           =   405
         End
         Begin VB.Label LabParte 
            AutoSize        =   -1  'True
            Caption         =   "Part"
            Height          =   195
            Left            =   6360
            TabIndex        =   79
            Top             =   840
            Width           =   285
         End
         Begin VB.Label LabFigCapa 
            AutoSize        =   -1  'True
            Caption         =   "Cover picture"
            Height          =   195
            Left            =   6360
            TabIndex        =   78
            Top             =   1440
            Width           =   945
         End
         Begin VB.Label LabDataIso 
            AutoSize        =   -1  'True
            Caption         =   "Date ISO"
            Height          =   195
            Left            =   6360
            TabIndex        =   77
            Top             =   240
            Width           =   660
         End
         Begin VB.Label LabQtdDoc 
            AutoSize        =   -1  'True
            Caption         =   "Number of Documents"
            Height          =   195
            Left            =   3840
            TabIndex        =   76
            Top             =   240
            Width           =   1590
         End
         Begin VB.Label LabStatus 
            AutoSize        =   -1  'True
            Caption         =   "Status"
            Height          =   195
            Left            =   240
            TabIndex        =   75
            Top             =   240
            Width           =   450
         End
      End
      Begin VB.Frame FramLeg 
         Height          =   3495
         Left            =   -74880
         TabIndex        =   46
         Top             =   480
         Width           =   8535
         Begin VB.Frame Legend 
            Caption         =   "Idioma 1:"
            Height          =   975
            Index           =   1
            Left            =   120
            TabIndex        =   65
            Top             =   240
            Width           =   8295
            Begin VB.TextBox TxtAno 
               Height          =   285
               Index           =   1
               Left            =   7560
               Locked          =   -1  'True
               TabIndex        =   17
               Text            =   " "
               Top             =   600
               Width           =   615
            End
            Begin VB.TextBox TxtMes 
               Height          =   285
               Index           =   1
               Left            =   6600
               TabIndex        =   16
               Text            =   " "
               Top             =   600
               Width           =   975
            End
            Begin VB.TextBox TxtLoc 
               Height          =   285
               Index           =   1
               Left            =   5400
               TabIndex        =   15
               Text            =   " "
               Top             =   600
               Width           =   1215
            End
            Begin VB.TextBox TxtNro 
               Height          =   285
               Index           =   1
               Left            =   3960
               TabIndex        =   13
               Text            =   " "
               Top             =   600
               Width           =   735
            End
            Begin VB.TextBox TxtVol 
               Height          =   285
               Index           =   1
               Left            =   2520
               TabIndex        =   11
               Top             =   600
               Width           =   735
            End
            Begin VB.TextBox TxtTitAbr 
               Height          =   285
               Index           =   1
               Left            =   120
               TabIndex        =   10
               Text            =   " "
               Top             =   600
               Width           =   2415
            End
            Begin VB.TextBox TxtSupplNro 
               Height          =   285
               Index           =   1
               Left            =   4680
               TabIndex        =   14
               Text            =   " "
               Top             =   600
               Width           =   735
            End
            Begin VB.TextBox TxtSupplVol 
               Height          =   285
               Index           =   1
               Left            =   3240
               TabIndex        =   12
               Text            =   " "
               Top             =   600
               Width           =   735
            End
            Begin VB.Label Label1 
               AutoSize        =   -1  'True
               Caption         =   "Short Title"
               Height          =   195
               Index           =   1
               Left            =   120
               TabIndex        =   73
               Top             =   360
               Width           =   720
            End
            Begin VB.Label Label2 
               AutoSize        =   -1  'True
               Caption         =   "Vol"
               Height          =   195
               Index           =   1
               Left            =   2520
               TabIndex        =   72
               Top             =   360
               Width           =   225
            End
            Begin VB.Label Label3 
               AutoSize        =   -1  'True
               Caption         =   "Num"
               Height          =   195
               Index           =   1
               Left            =   3960
               TabIndex        =   71
               Top             =   360
               Width           =   330
            End
            Begin VB.Label Label4 
               AutoSize        =   -1  'True
               Caption         =   "Vol Sup"
               Height          =   195
               Index           =   1
               Left            =   3240
               TabIndex        =   70
               Top             =   360
               Width           =   555
            End
            Begin VB.Label Label5 
               AutoSize        =   -1  'True
               Caption         =   "NumSup"
               Height          =   195
               Index           =   1
               Left            =   4680
               TabIndex        =   69
               Top             =   360
               Width           =   615
            End
            Begin VB.Label Label6 
               AutoSize        =   -1  'True
               Caption         =   "City"
               Height          =   195
               Index           =   1
               Left            =   5520
               TabIndex        =   68
               Top             =   360
               Width           =   255
            End
            Begin VB.Label Label7 
               AutoSize        =   -1  'True
               Caption         =   "Month"
               Height          =   195
               Index           =   1
               Left            =   6600
               TabIndex        =   67
               Top             =   360
               Width           =   450
            End
            Begin VB.Label Label8 
               AutoSize        =   -1  'True
               Caption         =   "Year"
               Height          =   195
               Index           =   1
               Left            =   7560
               TabIndex        =   66
               Top             =   360
               Width           =   330
            End
         End
         Begin VB.Frame Legend 
            Caption         =   "Idioma 1:"
            Height          =   975
            Index           =   2
            Left            =   120
            TabIndex        =   56
            Top             =   1320
            Width           =   8295
            Begin VB.TextBox TxtAno 
               Height          =   285
               Index           =   2
               Left            =   7560
               Locked          =   -1  'True
               TabIndex        =   25
               Text            =   " "
               Top             =   600
               Width           =   615
            End
            Begin VB.TextBox TxtMes 
               Height          =   285
               Index           =   2
               Left            =   6600
               TabIndex        =   24
               Text            =   " "
               Top             =   600
               Width           =   975
            End
            Begin VB.TextBox TxtLoc 
               Height          =   285
               Index           =   2
               Left            =   5400
               TabIndex        =   23
               Text            =   " "
               Top             =   600
               Width           =   1215
            End
            Begin VB.TextBox TxtNro 
               Height          =   285
               Index           =   2
               Left            =   3960
               TabIndex        =   21
               Text            =   " "
               Top             =   600
               Width           =   735
            End
            Begin VB.TextBox TxtVol 
               Height          =   285
               Index           =   2
               Left            =   2520
               TabIndex        =   19
               Top             =   600
               Width           =   735
            End
            Begin VB.TextBox TxtTitAbr 
               Height          =   285
               Index           =   2
               Left            =   120
               TabIndex        =   18
               Text            =   " "
               Top             =   600
               Width           =   2415
            End
            Begin VB.TextBox TxtSupplNro 
               Height          =   285
               Index           =   2
               Left            =   4680
               TabIndex        =   22
               Text            =   " "
               Top             =   600
               Width           =   735
            End
            Begin VB.TextBox TxtSupplVol 
               Height          =   285
               Index           =   2
               Left            =   3240
               TabIndex        =   20
               Text            =   " "
               Top             =   600
               Width           =   735
            End
            Begin VB.Label Label1 
               AutoSize        =   -1  'True
               Caption         =   "Short Title"
               Height          =   195
               Index           =   2
               Left            =   120
               TabIndex        =   64
               Top             =   360
               Width           =   720
            End
            Begin VB.Label Label2 
               AutoSize        =   -1  'True
               Caption         =   "Vol"
               Height          =   195
               Index           =   2
               Left            =   2520
               TabIndex        =   63
               Top             =   360
               Width           =   225
            End
            Begin VB.Label Label3 
               AutoSize        =   -1  'True
               Caption         =   "Num"
               Height          =   195
               Index           =   2
               Left            =   3960
               TabIndex        =   62
               Top             =   360
               Width           =   330
            End
            Begin VB.Label Label4 
               AutoSize        =   -1  'True
               Caption         =   "Vol Sup"
               Height          =   195
               Index           =   2
               Left            =   3240
               TabIndex        =   61
               Top             =   360
               Width           =   555
            End
            Begin VB.Label Label5 
               AutoSize        =   -1  'True
               Caption         =   "NumSup"
               Height          =   195
               Index           =   2
               Left            =   4680
               TabIndex        =   60
               Top             =   360
               Width           =   615
            End
            Begin VB.Label Label6 
               AutoSize        =   -1  'True
               Caption         =   "City"
               Height          =   195
               Index           =   2
               Left            =   5520
               TabIndex        =   59
               Top             =   360
               Width           =   255
            End
            Begin VB.Label Label7 
               AutoSize        =   -1  'True
               Caption         =   "Month"
               Height          =   195
               Index           =   2
               Left            =   6600
               TabIndex        =   58
               Top             =   360
               Width           =   450
            End
            Begin VB.Label Label8 
               AutoSize        =   -1  'True
               Caption         =   "Year"
               Height          =   195
               Index           =   2
               Left            =   7560
               TabIndex        =   57
               Top             =   360
               Width           =   330
            End
         End
         Begin VB.Frame Legend 
            Caption         =   "Idioma 1:"
            Height          =   975
            Index           =   3
            Left            =   120
            TabIndex        =   47
            Top             =   2400
            Width           =   8295
            Begin VB.TextBox TxtAno 
               Height          =   285
               Index           =   3
               Left            =   7560
               Locked          =   -1  'True
               TabIndex        =   33
               Text            =   " "
               Top             =   600
               Width           =   615
            End
            Begin VB.TextBox TxtMes 
               Height          =   285
               Index           =   3
               Left            =   6600
               TabIndex        =   32
               Text            =   " "
               Top             =   600
               Width           =   975
            End
            Begin VB.TextBox TxtLoc 
               Height          =   285
               Index           =   3
               Left            =   5400
               TabIndex        =   31
               Text            =   " "
               Top             =   600
               Width           =   1215
            End
            Begin VB.TextBox TxtNro 
               Height          =   285
               Index           =   3
               Left            =   3960
               TabIndex        =   29
               Text            =   " "
               Top             =   600
               Width           =   735
            End
            Begin VB.TextBox TxtVol 
               Height          =   285
               Index           =   3
               Left            =   2520
               TabIndex        =   27
               Text            =   " "
               Top             =   600
               Width           =   735
            End
            Begin VB.TextBox TxtTitAbr 
               Height          =   285
               Index           =   3
               Left            =   120
               TabIndex        =   26
               Text            =   " "
               Top             =   600
               Width           =   2415
            End
            Begin VB.TextBox TxtSupplNro 
               Height          =   285
               Index           =   3
               Left            =   4680
               TabIndex        =   30
               Text            =   " "
               Top             =   600
               Width           =   735
            End
            Begin VB.TextBox TxtSupplVol 
               Height          =   285
               Index           =   3
               Left            =   3240
               TabIndex        =   28
               Text            =   " "
               Top             =   600
               Width           =   735
            End
            Begin VB.Label Label1 
               AutoSize        =   -1  'True
               Caption         =   "Short Title"
               Height          =   195
               Index           =   3
               Left            =   120
               TabIndex        =   55
               Top             =   360
               Width           =   720
            End
            Begin VB.Label Label2 
               AutoSize        =   -1  'True
               Caption         =   "Vol"
               Height          =   195
               Index           =   3
               Left            =   2520
               TabIndex        =   54
               Top             =   360
               Width           =   225
            End
            Begin VB.Label Label3 
               AutoSize        =   -1  'True
               Caption         =   "Num"
               Height          =   195
               Index           =   3
               Left            =   3960
               TabIndex        =   53
               Top             =   360
               Width           =   330
            End
            Begin VB.Label Label4 
               AutoSize        =   -1  'True
               Caption         =   "Vol Sup"
               Height          =   195
               Index           =   3
               Left            =   3240
               TabIndex        =   52
               Top             =   360
               Width           =   555
            End
            Begin VB.Label Label5 
               AutoSize        =   -1  'True
               Caption         =   "NumSup"
               Height          =   195
               Index           =   3
               Left            =   4680
               TabIndex        =   51
               Top             =   360
               Width           =   615
            End
            Begin VB.Label Label6 
               AutoSize        =   -1  'True
               Caption         =   "City"
               Height          =   195
               Index           =   3
               Left            =   5520
               TabIndex        =   50
               Top             =   360
               Width           =   255
            End
            Begin VB.Label Label7 
               AutoSize        =   -1  'True
               Caption         =   "Month"
               Height          =   195
               Index           =   3
               Left            =   6600
               TabIndex        =   49
               Top             =   360
               Width           =   450
            End
            Begin VB.Label Label8 
               AutoSize        =   -1  'True
               Caption         =   "Year"
               Height          =   195
               Index           =   3
               Left            =   7560
               TabIndex        =   48
               Top             =   360
               Width           =   330
            End
         End
      End
      Begin VB.Frame Frame1 
         Height          =   4575
         Left            =   -74880
         TabIndex        =   44
         Top             =   360
         Width           =   8655
         Begin VB.ListBox DispoSecCode 
            Height          =   645
            Left            =   6600
            MultiSelect     =   2  'Extended
            Sorted          =   -1  'True
            TabIndex        =   93
            Top             =   960
            Visible         =   0   'False
            Width           =   1935
         End
         Begin VB.ListBox ListSortedSections 
            Height          =   255
            Left            =   7200
            Sorted          =   -1  'True
            TabIndex        =   91
            Top             =   1200
            Visible         =   0   'False
            Width           =   1095
         End
         Begin ComctlLib.ListView lvSortedSections 
            Height          =   255
            Left            =   6600
            TabIndex        =   90
            Top             =   1200
            Visible         =   0   'False
            Width           =   495
            _ExtentX        =   873
            _ExtentY        =   450
            View            =   3
            LabelWrap       =   -1  'True
            HideSelection   =   -1  'True
            _Version        =   327682
            ForeColor       =   -2147483640
            BackColor       =   -2147483643
            BorderStyle     =   1
            Appearance      =   1
            NumItems        =   4
            BeginProperty ColumnHeader(1) {0713E8C7-850A-101B-AFC0-4210102A8DA7} 
               Key             =   ""
               Object.Tag             =   ""
               Text            =   "Seccode"
               Object.Width           =   2540
            EndProperty
            BeginProperty ColumnHeader(2) {0713E8C7-850A-101B-AFC0-4210102A8DA7} 
               SubItemIndex    =   1
               Key             =   ""
               Object.Tag             =   ""
               Text            =   "idiom1"
               Object.Width           =   2540
            EndProperty
            BeginProperty ColumnHeader(3) {0713E8C7-850A-101B-AFC0-4210102A8DA7} 
               SubItemIndex    =   2
               Key             =   ""
               Object.Tag             =   ""
               Text            =   "idiom2"
               Object.Width           =   2540
            EndProperty
            BeginProperty ColumnHeader(4) {0713E8C7-850A-101B-AFC0-4210102A8DA7} 
               SubItemIndex    =   3
               Key             =   ""
               Object.Tag             =   ""
               Text            =   "idiom3"
               Object.Width           =   2540
            EndProperty
         End
         Begin ComctlLib.ListView DispoSections 
            Height          =   255
            Left            =   6600
            TabIndex        =   89
            Top             =   960
            Visible         =   0   'False
            Width           =   1575
            _ExtentX        =   2778
            _ExtentY        =   450
            View            =   3
            Sorted          =   -1  'True
            LabelWrap       =   -1  'True
            HideSelection   =   -1  'True
            _Version        =   327682
            ForeColor       =   -2147483640
            BackColor       =   -2147483643
            BorderStyle     =   1
            Appearance      =   1
            NumItems        =   4
            BeginProperty ColumnHeader(1) {0713E8C7-850A-101B-AFC0-4210102A8DA7} 
               Key             =   ""
               Object.Tag             =   ""
               Text            =   "code"
               Object.Width           =   2540
            EndProperty
            BeginProperty ColumnHeader(2) {0713E8C7-850A-101B-AFC0-4210102A8DA7} 
               SubItemIndex    =   1
               Key             =   ""
               Object.Tag             =   ""
               Text            =   "idiom1"
               Object.Width           =   2540
            EndProperty
            BeginProperty ColumnHeader(3) {0713E8C7-850A-101B-AFC0-4210102A8DA7} 
               SubItemIndex    =   2
               Key             =   ""
               Object.Tag             =   ""
               Text            =   "idiom2"
               Object.Width           =   2540
            EndProperty
            BeginProperty ColumnHeader(4) {0713E8C7-850A-101B-AFC0-4210102A8DA7} 
               SubItemIndex    =   3
               Key             =   ""
               Object.Tag             =   ""
               Text            =   "idiom3"
               Object.Width           =   2540
            EndProperty
         End
         Begin VB.Frame Frame2 
            Caption         =   "Sections of "
            Height          =   2655
            Left            =   120
            TabIndex        =   83
            Top             =   1800
            Width           =   8415
            Begin ComctlLib.ListView LVSections 
               Height          =   1695
               Left            =   120
               TabIndex        =   39
               Top             =   840
               Width           =   8175
               _ExtentX        =   14420
               _ExtentY        =   2990
               View            =   3
               LabelWrap       =   -1  'True
               HideSelection   =   -1  'True
               _Version        =   327682
               ForeColor       =   -2147483640
               BackColor       =   -2147483643
               BorderStyle     =   1
               Appearance      =   1
               NumItems        =   4
               BeginProperty ColumnHeader(1) {0713E8C7-850A-101B-AFC0-4210102A8DA7} 
                  Key             =   ""
                  Object.Tag             =   ""
                  Text            =   "Seccode"
                  Object.Width           =   2540
               EndProperty
               BeginProperty ColumnHeader(2) {0713E8C7-850A-101B-AFC0-4210102A8DA7} 
                  SubItemIndex    =   1
                  Key             =   ""
                  Object.Tag             =   ""
                  Text            =   "idiom1"
                  Object.Width           =   2540
               EndProperty
               BeginProperty ColumnHeader(3) {0713E8C7-850A-101B-AFC0-4210102A8DA7} 
                  SubItemIndex    =   2
                  Key             =   ""
                  Object.Tag             =   ""
                  Text            =   "idiom2"
                  Object.Width           =   2540
               EndProperty
               BeginProperty ColumnHeader(4) {0713E8C7-850A-101B-AFC0-4210102A8DA7} 
                  SubItemIndex    =   3
                  Key             =   ""
                  Object.Tag             =   ""
                  Text            =   "idiom3"
                  Object.Width           =   2540
               EndProperty
            End
            Begin VB.TextBox TxtHeader 
               BackColor       =   &H00FFFFFF&
               Height          =   285
               Index           =   3
               Left            =   5640
               TabIndex        =   38
               Top             =   480
               Width           =   2655
            End
            Begin VB.TextBox TxtHeader 
               BackColor       =   &H00FFFFFF&
               DataField       =   "TxtHeader"
               Height          =   285
               Index           =   2
               Left            =   2880
               TabIndex        =   37
               Top             =   480
               Width           =   2655
            End
            Begin VB.TextBox TxtHeader 
               BackColor       =   &H00FFFFFF&
               Height          =   285
               Index           =   1
               Left            =   120
               TabIndex        =   36
               Top             =   480
               Width           =   2655
            End
            Begin VB.Label LabIdiom 
               AutoSize        =   -1  'True
               Caption         =   "English"
               Height          =   195
               Index           =   3
               Left            =   5640
               TabIndex        =   86
               Top             =   240
               Width           =   510
            End
            Begin VB.Label LabIdiom 
               AutoSize        =   -1  'True
               Caption         =   "Spanish"
               Height          =   195
               Index           =   1
               Left            =   120
               TabIndex        =   85
               Top             =   240
               Width           =   570
            End
            Begin VB.Label LabIdiom 
               AutoSize        =   -1  'True
               Caption         =   "Portuguese"
               Height          =   195
               Index           =   2
               Left            =   2880
               TabIndex        =   84
               Top             =   240
               Width           =   810
            End
         End
         Begin VB.ListBox DispoSecTitle 
            Height          =   1185
            Left            =   120
            Sorted          =   -1  'True
            Style           =   1  'Checkbox
            TabIndex        =   34
            Top             =   480
            Width           =   6375
         End
         Begin VB.CommandButton CmdNewSections 
            Caption         =   "Create section"
            Height          =   375
            Left            =   6840
            TabIndex        =   35
            Top             =   480
            Width           =   1575
         End
         Begin VB.Label Label9 
            AutoSize        =   -1  'True
            Caption         =   "Select the sections that are present in "
            Height          =   195
            Left            =   120
            TabIndex        =   45
            Top             =   240
            Width           =   2715
         End
      End
   End
   Begin VB.Label LabIndicationMandatoryField 
      Caption         =   "Label1"
      ForeColor       =   &H000000FF&
      Height          =   255
      Left            =   240
      TabIndex        =   92
      Top             =   5280
      Width           =   3735
   End
End
Attribute VB_Name = "Issue2"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Explicit

Private NormalHeight As Long
Private NormalWidth As Long

Private OldHeight As Long
Private OldWidth As Long

Private currDate As String

Private mfnSection As Long
Private mfnIssue As Long
Private CurrMonth As String

Private myIssue As ClsIssue
Private journalSections As ClsTOC



Private Const MaxLenSectitle = 500

Public Sub LoadIssue(mfn As Long)
    
    mfnIssue = mfn
    If mfn > 0 Then
        Set myIssue = Issue0.issueDAO.returnIssue(mfn)
    Else
        Set myIssue = New ClsIssue
        myIssue.volume = Issue1.TxtVolid.text
        myIssue.number = Issue1.TxtIssueno.text
        myIssue.suppl = Issue1.TxtSupplNo.text
        myIssue.vsuppl = Issue1.TxtSupplVol.text
        myIssue.issueorder = Issue1.TxtIseqno.text
        myIssue.idPart = Issue1.ComboIssueIdPart.text
        
        With myIssue.journal
        .JournalStandard = Issue1.Title_Standard
        .vocabulary = Issue1.Title_Scheme
        End With
    End If
    
    With myIssue.journal
        .shorttitle = Issue1.TxtStitle.Caption
        .Title = Issue1.TxtSertitle.Caption
        .pubid = Issue1.SiglaPeriodico
        .ISSN = Issue1.TxtISSN.Caption
        .ISOTitle = Issue1.TxtISOStitle.Caption
        .MedlineTitle = Issue1.TxtMedlineStitle.Caption
        .parallelTitles = Issue1.TxtParallel.text
        .publisherName = Issue1.TxtPubl.text
    End With
    
    loadFormLayout
    loadFormData
    
    'LoadGeneral (mfn)
    'LoadLegend (mfn)
    
    'LoadDispoSections
    
    Show vbModal
    
End Sub

Private Sub loadFormLayout()
    Dim i As Long
    
    
    With Fields
    Caption = App.Title + " - " + myIssue.journal.pubid + " " + myIssue.issueId + " ISSN ID: " + Issue1.issn_id
    
    'Caption = TxtTitAbr(idiomidx).text + " " + TxtVol(idiomidx).text + " " + TxtSupplVol(idiomidx).text + " " + TxtNro(idiomidx).text + " " + TxtSupplNro(idiomidx).text
    
    For i = 1 To IdiomsInfo.count
        Label10(i - 1).Caption = IdiomsInfo(i).label
        Label1(i).Caption = .getLabel("ser1_ShortTitle")
        Label2(i).Caption = .getLabel("Volume")
        Label3(i).Caption = .getLabel("Issueno")
        Label4(i).Caption = .getLabel("VolSuppl")
        Label5(i).Caption = .getLabel("IssueSuppl")
        Label6(i).Caption = .getLabel("Issue_Place")
        Label7(i).Caption = .getLabel("Issue_month")
        Label8(i).Caption = .getLabel("Issue_year")
        Legend(i).Caption = IdiomsInfo(i).label
        LVSections.ColumnHeaders(i + 1).text = IdiomsInfo(i).label
        LVSections.ColumnHeaders(i + 1).Width = LVSections.Width / 5
    Next
    LabStatus.Caption = .getLabel("Issue_status")
    LabFascTitulo.Caption = .getLabel("Issue_IssTitle")
    LabEditorEspecial.Caption = .getLabel("Issue_IssPublisher")
    LabFigCapa.Caption = .getLabel("Issue_Cover")
    LabDataIso.Caption = .getLabel("Issue_DateISO")
    LabIssSponsor.Caption = .getLabel("Issue_Sponsor")
    LabParte.Caption = .getLabel("Issue_Part")
    LabQtdDoc.Caption = .getLabel("Issue_NumberofDocuments")
    LabScheme.Caption = .getLabel("Issue_Scheme")
    LabStandard.Caption = .getLabel("Title_standard")
    MkpCheck.Caption = .getLabel("Issue_MkpDone")
    End With
    
    With ConfigLabels
    LabIndicationMandatoryField.Caption = .getLabel("MandatoryFieldIndication")
    SSTab1.TabCaption(0) = .getLabel("Issue_General")
    SSTab1.TabCaption(1) = .getLabel("Issue_BibliographicStrip")
    SSTab1.TabCaption(2) = .getLabel("Issue_Tableofcontents")
    SSTab1.TabCaption(3) = .getLabel("Issue_TabConfigurations")
    
    Label9.Caption = .getLabel("Issue_SelectSections")
    Frame2.Caption = .getLabel("Issue_Sectionsof")
    CmdNewSections.Caption = .getLabel("Issue_CreateSection")
    CmdClose.Caption = .getLabel("ButtonClose")
    FormCmdAju.Caption = .getLabel("mnHelp")
    FormCmdSave.Caption = .getLabel("ButtonSave")
    End With
    
    IdiomLoad
    
    Call FillCombo(ComboStatus, CodeIssStatus)
    Call FillCombo(ComboStandard, CodeStandard)
    Call FillList(ListScheme, CodeScheme)
    
    Text_issueissn.Clear
    Text_issueissn.AddItem ("")
    If Len(Issue1.issn_current) > 0 Then
        Text_issueissn.AddItem (Issue1.issn_current)
    End If
    If Len(Issue1.issn_id) > 0 And (Issue1.issn_current <> Issue1.issn_id) Then
        Text_issueissn.AddItem (Issue1.issn_id)
    End If
    
    
    Label9.Caption = Label9.Caption + " " + Caption
    Frame2.Caption = Frame2.Caption + " " + Caption
    
    LVSections.ColumnHeaders(1).Width = LVSections.Width / 5
    
    
    
    OldHeight = Height
    OldWidth = Width
    NormalHeight = Height
    NormalWidth = Width
    
    
End Sub

Private Sub IdiomLoad()
    Dim i As Long
    
    For i = 1 To IdiomsInfo.count
        LabIdiom(i).Caption = IdiomsInfo(i).label  '990316
        Legend(i).Caption = IdiomsInfo(i).label
        LabIdiom2(i).Caption = IdiomsInfo(i).label
    Next
End Sub

Private Sub loadFormData()
    LoadDispoSections
    LoadIssueData
End Sub
Private Sub LoadIssueData()
    Dim i As Long
    Dim j As Long
    Dim bs As ClsBibStrip
    Dim lang As String
    
    Call FillCombo(ComboIssueLicText, CodeLicText, True)
    
    
    TxtDoccount.text = myIssue.doccount
    currDate = myIssue.DateISO
    TxtDateIso.text = currDate
    
    If InStr("|" + Issue1.issn_current + "|" + Issue1.issn_id + "|", "|" + myIssue.issueISSN + "|") > 0 Then
        Text_issueissn.text = myIssue.issueISSN
    Else
        myIssue.issueISSN = ""
    End If
    
    
    TxtIssuept.text = myIssue.issuepart
    
    TxtIssSponsor.text = myIssue.issueSponsor
    
    For i = 1 To IdiomsInfo.count
        lang = IdiomsInfo(i).Code
        TxtIssTitle(i).text = myIssue.issueTitle.getItemByLang(lang).text
        TextCreativeCommons(i - 1).text = myIssue.licenses.getItemByLang(lang).text
        Set bs = myIssue.bibstrips.getItemByLang(lang)
        
            With bs
                TxtTitAbr(i).text = .stitle
                TxtNro(i).text = .n
                TxtSupplVol(i).text = .vs
                TxtSupplNro(i).text = .s
                TxtLoc(i).text = .loc
                TxtMes(i) = .month
                TxtAno(i) = .year
                
                If .stitle = "" Then TxtTitAbr(i).text = Issue1.TxtStitle.Caption
                TxtVol(i).text = .v
                TxtVol(i).text = addBSPrefix(TxtVol(i).text, Issue1.TxtVolid.text, .lang, "v.", "vol.")
                TxtNro(i).text = addBSPrefix(TxtNro(i).text, Issue1.TxtIssueno.text, .lang, "n.", "no.")
                TxtSupplVol(i).text = addBSPrefix(TxtSupplVol(i).text, Issue1.TxtSupplVol.text, .lang, "suppl.", "supl.")
                TxtSupplNro(i).text = addBSPrefix(TxtSupplNro(i).text, Issue1.TxtSupplNo.text, .lang, "suppl.", "supl.")
                If TxtLoc(i).text = "" Then TxtLoc(i).text = Issue1.Cidade
                If TxtAno(i).text = "" Then TxtAno(i) = Mid(Issue1.TxtIseqno.text, 1, 4)
                
            End With
        
            If myIssue.toc.names.getItemByLang(lang).text <> "" Then
                TxtHeader(i).text = myIssue.toc.names.getItemByLang(lang).text
            End If
        
    Next
    For j = 1 To myIssue.toc.sections.count
        Call DispoSecTitleChecked(myIssue.toc.sections.item(j).sectionCode, True)
    Next
        
        

    If Len(myIssue.lic) > 0 Then ComboIssueLicText.text = myIssue.lic
    TxtIssPublisher.text = myIssue.issuePublisher
    TxtCover.text = myIssue.issueCover
    
    MkpCheck.value = Str2Int(myIssue.markupDone)
    
    If myIssue.status <> "" Then ComboStatus.text = CodeIssStatus.item(myIssue.status).value
    
    
    If myIssue.journal.JournalStandard = "" Then myIssue.journal.JournalStandard = Issue1.Title_Standard
    
    ComboStandard.text = CodeStandard(myIssue.journal.JournalStandard).value
    If Len(ComboStandard.text) = 0 Then ComboStandard.text = Issue1.Title_Standard
    
    If myIssue.journal.vocabulary = "" Then myIssue.journal.vocabulary = Issue1.Title_Scheme
    i = 0
    Dim found As Boolean
    If myIssue.journal.vocabulary <> "" Then
        While i < ListScheme.ListCount And Not found
            If ListScheme.list(i) = CodeScheme(myIssue.journal.vocabulary).value Then
                ListScheme.selected(i) = True
                found = True
            End If
            i = i + 1
        Wend
    End If

End Sub

Private Function addBSPrefix(formerText As String, text As String, lang As String, prefixEn As String, prefixOther As String) As String
    If formerText = "" Then
        If text <> "" Then
            If lang = "en" Then
                formerText = prefixEn + text
            Else
                formerText = prefixOther + text
            End If
        End If
    End If
    
    addBSPrefix = formerText
End Function


Private Sub LoadDispoSections()
    Dim i As Long
    Dim j As Long
    Dim lang As String
    Dim seccode As String
    Dim sectitle As String
    Dim sectionDAO As ClsSectionDAO
    
    
    With Paths("Section Database")
    Set sectionDAO = New ClsSectionDAO
    Call sectionDAO.create(.Path, .FileName, .key)
    End With
    
    DispoSecTitle.Clear
    
    DispoSecCode.Clear
    DispoSecCode.visible = False
    
    Set journalSections = sectionDAO.getTOC(Issue1.TxtSertitle.Caption, Issue1.TxtISSN.Caption, Issue1.SiglaPeriodico, mfnSection)
        
    For i = 1 To IdiomsInfo.count
        lang = IdiomsInfo(i).Code
        TxtHeader(i).text = journalSections.names.getItemByLang(lang).text
    Next
    
    For j = 1 To journalSections.sections.count
        seccode = journalSections.sections.item(j).sectionCode
        sectitle = ""
        i = 0
        While sectitle = "" And i < IdiomsInfo.count
            lang = IdiomsInfo(i + 1).Code
            sectitle = journalSections.sections.item(seccode).sectionNames.getItemByLang(lang).text
            i = i + 1
        Wend
        
        DispoSecTitle.AddItem (sectitle)
        DispoSecCode.AddItem (applyStandard(sectitle) + "|" + seccode)
        
    Next
End Sub

Private Function applyStandard(t As String) As String
    applyStandard = t + Space(500 - Len(t))
End Function


Private Sub DispoSecTitleChecked(sectionCode As String, Flag As Boolean)
    Dim i As Long
    Dim index As Long
    Dim found As Boolean
    
    found = False
    i = 0
    While (i < DispoSecCode.ListCount) And (Not found)
        If InStr(DispoSecCode.list(i), sectionCode) > 0 Then
            found = True
            DispoSecTitle.selected(i) = Flag
            DispoSecCode.selected(i) = Flag
        End If
        i = i + 1
    Wend
End Sub


Private Sub CmdClose_Click()
    Unload Me
End Sub

Private Sub CmdNewSections_Click()
    Call New_Section2.OpenSection(Issue1.TxtSertitle.Caption, False)
    
    LoadDispoSections
End Sub

Private Sub ComboIssueLicText_Click()
Dim i As Long
    
    'Set currentLicText = New ColIdiom
    For i = 1 To IdiomsInfo.count
        TextCreativeCommons(i - 1).text = CodeLicTextMultilingue.getItemByLang(IdiomsInfo(i).Code).item(ComboIssueLicText.text).value
    Next
    
End Sub



Private Sub DispoSecTitle_Click()
    Dim i As Long
    Dim Code As String
    Dim lvSection As ListItem
    'Dim LvDispo As ListItem
    Dim SelectedIdx As Long
    
    
    SelectedIdx = DispoSecTitle.ListIndex
    DispoSecCode.selected(SelectedIdx) = DispoSecTitle.selected(SelectedIdx)
    Code = Mid(DispoSecCode.list(SelectedIdx), InStr(DispoSecCode.list(SelectedIdx), "|") + 1)
        
    If DispoSecTitle.selected(SelectedIdx) Then
        'add
        'Set LvDispo = DispoSections.FindItem(Code, lvwText)
        Set lvSection = LVSections.FindItem(Code, lvwText)
        
        If lvSection Is Nothing Then
            Set lvSection = LVSections.ListItems.add(, Code, Code)
        End If
        For i = 1 To IdiomsInfo.count
            lvSection.SubItems(i) = journalSections.sections.item(Code).sectionNames.getItemByLang(IdiomsInfo(i).Code).text
        Next
    Else
        'delete
        Set lvSection = LVSections.FindItem(Code, lvwText)
        If Not (lvSection Is Nothing) Then
            LVSections.ListItems.Remove (lvSection.index)
        End If
    End If
    
End Sub

Private Sub Form_Load()
    SSTab1.Tab = 0
End Sub

Private Sub Form_Unload(Cancel As Integer)
    Dim res As VbMsgBoxResult
    
    Dim QExit As Boolean
    
    
    
    QExit = CheckYears And (Not WarnMandatoryFields)
    
    If Not QExit Then
        If IssueCloseDenied Then
            MsgBox ConfigLabels.getLabel("MsgUnabledtoClose")
        Else
            res = MsgBox(ConfigLabels.getLabel("MsgExit"), vbYesNo + vbDefaultButton2)
            If res = vbYes Then
                QExit = True
            ElseIf res = vbNo Then
                QExit = False
            End If
        End If
    End If
    
    
    If QExit Then
        If Issue_ChangedContents Then
            res = MsgBox(ConfigLabels.getLabel("MsgSaveChanges"), vbYesNoCancel)
            If res = vbYes Then
                Issue_Save
            ElseIf res = vbNo Then
            
            Else
                QExit = False
            End If
        End If
    End If
    
    If QExit Then
        Unload Me
    Else
        Cancel = 1
    End If
End Sub

Private Sub FormCmdAju_Click()
    Call openHelp(Paths("Help of Issue2").Path, Paths("Help of Issue2").FileName)
End Sub

Private Sub Form_Resize()
    Resize
End Sub

Private Sub Resize()
    Dim x As Double
    Dim Y As Double
    
    If WindowState <> vbMinimized Then
        If Height < NormalHeight Then
            'OldHeight = Height
            Height = NormalHeight
        ElseIf Width < NormalWidth Then
            'OldWidth = Width
            Width = NormalWidth
        Else
            x = Width / OldWidth
            Y = Height / OldHeight
            Call Posicionar(x, Y)
            OldHeight = Height
            OldWidth = Width
        End If
    End If
End Sub

Private Sub Redimensionar(obj As Object, Left As Double, Top As Double, Width As Double, Height As Double)
    obj.Left = Left * obj.Left
    obj.Top = Top * obj.Top
    If Height <> 1 Then obj.Height = CLng(Height * obj.Height)
    If Width <> 1 Then obj.Width = Width * obj.Width
End Sub

Private Sub PosicionarLegenda(x As Double, Y As Double)
    Dim i As Integer
    
    If (x <> 1) And (Y <> 1) Then
    Call Redimensionar(FramLeg, x, Y, x, Y)
    Call Redimensionar(FormCmdAju, x, Y, x, 1)
    Call Redimensionar(FormCmdSave, x, Y, x, 1)
    
    For i = 1 To 3
        Call Redimensionar(Legend(i), x, Y, x, Y)
        Call Redimensionar(TxtTitAbr(i), x, Y, x, 1)
        Call Redimensionar(TxtVol(i), x, Y, x, 1)
        Call Redimensionar(TxtNro(i), x, Y, x, 1)
        Call Redimensionar(TxtSupplVol(i), x, Y, x, 1)
        Call Redimensionar(TxtSupplNro(i), x, Y, x, 1)
        Call Redimensionar(TxtLoc(i), x, Y, x, 1)
        Call Redimensionar(TxtMes(i), x, Y, x, 1)
        Call Redimensionar(TxtAno(i), x, Y, x, 1)
        Call Redimensionar(Label1(i), x, Y, x, 1)
        Call Redimensionar(Label2(i), x, Y, x, 1)
        Call Redimensionar(Label3(i), x, Y, x, 1)
        Call Redimensionar(Label4(i), x, Y, x, 1)
        Call Redimensionar(Label5(i), x, Y, x, 1)
        Call Redimensionar(Label6(i), x, Y, x, 1)
        Call Redimensionar(Label7(i), x, Y, x, 1)
        Call Redimensionar(Label8(i), x, Y, x, 1)
    Next
    End If
End Sub

Private Sub Posicionar(x As Double, Y As Double)
    
    If (x <> 1) And (Y <> 1) Then
    Call Redimensionar(SSTab1, x, Y, x, Y)
    
    If SSTab1.Tab = 0 Then
        Call PosicionarLegenda(x, Y)
        'If SSTab1.TabVisible(1) Then
            SSTab1.Tab = 1
            'Call PosicionarSumario(X, Y)
            SSTab1.Tab = 0
        'End If
    Else
        'Call PosicionarSumario(X, Y)
        SSTab1.Tab = 0
        Call PosicionarLegenda(x, Y)
        SSTab1.Tab = 1
    End If
    End If
End Sub

Private Sub formcmdsave_Click()
    If Len(currDate) > 0 Then
        If StrComp(TxtDateIso.text, currDate, vbTextCompare) <> 0 Then
            MsgBox ConfigLabels.getLabel("Issue_InvalidDateBibStrip")
        End If
    End If
    Issue_Save
End Sub

Private Sub LVSections_BeforeLabelEdit(Cancel As Integer)
    Cancel = 1
End Sub

Private Sub LVSections_ColumnClick(ByVal ColumnHeader As ComctlLib.ColumnHeader)
    'LVSections.SortKey = ColumnHeader.index - 1
    'LVSections.Sorted = True
    'LVSections.SortOrder = lvwAscending
End Sub

Private Sub TxtDateIso_Change()

    Dim idiomidx As Long
    Dim month As String
    Dim change As Boolean
    
    
    If Len(TxtDateIso.text) >= 4 Then
        If Len(TxtDateIso.text) >= 6 Then
            month = Mid(TxtDateIso.text, 5, 2)
        Else
            month = "00"
        End If
        
        If Len(currDate) >= 6 Then
            CurrMonth = Mid(currDate, 5, 2)
        Else
            CurrMonth = ""
        End If
        
        
        
        Set myIssue.bibstrips.nullObject = New ClsBibStrip
        'Set myIssue.bibstrips.nullObject = bibstrip
        For idiomidx = 1 To IdiomsInfo.count
            If month = CurrMonth Then
                If mfnIssue > 0 Then
                    TxtMes(idiomidx).text = myIssue.bibstrips.getItemByLang(IdiomsInfo(idiomidx).Code).month
                Else
                    TxtMes(idiomidx).text = Months.GetMonth(IdiomsInfo(idiomidx).Code, TxtDateIso.text, Issue1.Title_Freq)
                End If
            Else
                TxtMes(idiomidx).text = Months.GetMonth(IdiomsInfo(idiomidx).Code, TxtDateIso.text, Issue1.Title_Freq)
            End If
        Next
               
        If Mid(TxtDateIso.text, 1, 4) <> Issue1.year Then
            If Len(TxtDateIso.text) = 8 Then MsgBox ConfigLabels.getLabel("MsgInvalidYear"), vbCritical
            TxtDateIso.text = Issue1.year ' + Mid(TxtDateIso.Text, 5)
        Else
            For idiomidx = 1 To IdiomsInfo.count
                TxtAno(idiomidx).text = Mid(TxtDateIso.text, 1, 4)
            Next
        End If
    End If
End Sub

Private Function Issue_ChangedContents() As Boolean
    Dim dbissue As ClsIssue
    UpdateData
    
    Set dbissue = Issue0.issueDAO.returnIssue(mfnIssue)
    Issue_ChangedContents = (Issue0.issueDAO.tag(myIssue) <> Issue0.issueDAO.tag(dbissue))
End Function


Private Function WarnMandatoryFields() As Boolean
    Dim warning As String
    Dim i As Long
    
    With Fields
    
    If Not CheckDateISO(TxtDateIso.text) Then warning = warning + ConfigLabels.getLabel("MsgInvalidDATEISO") + vbCrLf
        
    warning = warning + .isA_mandatoryField(Text_issueissn.text, "Issue_ISSN")
    
    warning = warning + .isA_mandatoryField(ComboStatus.text, "Issue_status")
    warning = warning + .isA_mandatoryField(ComboStandard.text, "Issue_Standard")
    
    If ListScheme.SelCount = 0 Then
        warning = warning + .isA_mandatoryField("", "Issue_Scheme")
    End If
    
   
    warning = warning + .isA_mandatoryField(TxtDateIso.text, "Issue_DateISO")
    warning = warning + .isA_mandatoryField(TxtDoccount.text, "Issue_NumberofDocuments")
    
    
    If Not IsNumber(TxtDoccount.text) Then MsgBox ConfigLabels.getLabel("Issue_InvalidNumDoc")
    
    For i = 1 To IdiomsInfo.count
        warning = warning + .isA_mandatoryField(TxtTitAbr(i).text, "ser1_ShortTitle")
        warning = warning + .isA_mandatoryField(TxtVol(i).text + TxtSupplVol(i).text + TxtNro(i).text + TxtSupplNro(i).text, "Issueno")
        warning = warning + .isA_mandatoryField(TxtLoc(i).text, "Issue_Place")
        warning = warning + .isA_mandatoryField(TxtAno(i).text, "Issue_year")
    Next
    For i = 1 To IdiomsInfo.count
        warning = warning + .isA_mandatoryField(TxtHeader(i).text, "Issue_Header")
    Next
    
    
    End With
    
    If Len(warning) > 0 Then
        MsgBox ConfigLabels.getLabel("MsgMandatoryContent") + vbCrLf + warning
    End If
    WarnMandatoryFields = (Len(warning) > 0)
End Function

Private Function CheckYears() As Boolean
    Dim i As Long
    Dim yearOK As Boolean
    Dim year As String
    
    
    If Len(TxtDateIso.text) >= 4 Then
        year = Mid(TxtDateIso.text, 1, 4)
        yearOK = True
    End If
    
    For i = 1 To IdiomsInfo.count
        yearOK = yearOK And (TxtAno(i).text = year)
    Next
    
    yearOK = yearOK And (Mid(Issue1.TxtIseqno.text, 1, 4) = year)
    
    
    
    
    If Not yearOK Then
        Call MsgBox(ConfigLabels.getLabel("MsgInvalidYear"), vbCritical)
    End If
    CheckYears = yearOK
End Function


Private Sub TxtDateIso_LostFocus()
        
        If CheckDateISO(TxtDateIso.text) Then
            If Len(currDate) > 0 Then
                If StrComp(TxtDateIso.text, currDate) <> 0 Then
                    currDate = TxtDateIso.text
                End If
            Else
                currDate = TxtDateIso.text
            End If
        End If
End Sub

Private Function Issue_Save() As Boolean
    UpdateData
    Issue_Save = Issue0.issueDAO.save(mfnIssue, myIssue)
End Function

Private Sub UpdateData()
    With myIssue
    
        Dim i As Long
        Dim t As ClsTextByLang
        Dim obj As ClsBibStrip
        Dim subf(8) As String
        Dim content(8) As String
        
        
        Set .licenses = New ColTextByLang
        Set .issueTitle = New ColTextByLang
        Set .bibstrips = New ColObjByLang
        Set .bibstrips.nullObject = New ClsBibStrip
        
        
        For i = 1 To IdiomsInfo.count
            Set t = New ClsTextByLang
            t.lang = IdiomsInfo.item(i).Code
            t.text = Issue2.TxtIssTitle(i).text
            
            .issueTitle.add t
            
            Set t = New ClsTextByLang
            t.lang = IdiomsInfo.item(i).Code
            t.text = Issue2.TextCreativeCommons(i - 1).text
            
            
            .licenses.add t
            
            Set obj = New ClsBibStrip
            With obj
                .stitle = Issue2.TxtTitAbr(i).text
                .v = Issue2.TxtVol(i).text
                .vs = Issue2.TxtSupplVol(i).text
                .n = Issue2.TxtNro(i).text
                .s = Issue2.TxtSupplNro(i).text
                .loc = Issue2.TxtLoc(i).text
                .month = Issue2.TxtMes(i).text
                .year = Issue2.TxtAno(i).text
                .lang = IdiomsInfo.item(i).Code
            End With
            Call .bibstrips.add(obj)
            
            
        Next
        .lic = Issue2.ComboIssueLicText.text
        Set .toc = New ClsTOC
        Set .toc = getNewTOC
    .issueISSN = Issue2.Text_issueissn.text
    .DateISO = Issue2.TxtDateIso.text
        .doccount = Issue2.TxtDoccount.text
        .issueCover = Issue2.TxtCover.text
        .issuepart = Issue2.TxtIssuept.text
        .issuePublisher = Issue2.TxtIssPublisher.text
        .issueSponsor = Issue2.TxtIssSponsor.text
        .markupDone = Int2Str(Issue2.MkpCheck.value)
        .journal.JournalStandard = CodeStandard(Issue2.ComboStandard.text).Code
        If Issue2.ComboStatus.text <> "" Then .status = CodeIssStatus(Issue2.ComboStatus.text).Code
    End With
End Sub

Private Function getNewTOC() As ClsTOC
    Dim toc As New ClsTOC
    Dim section As ClsSection
    Dim titleAndLang As ClsTextByLang
    Dim i As Long
    Dim k As Long
    
    LVSections.SortKey = 0
    LVSections.Sorted = True
    LVSections.SortOrder = lvwAscending
    
    Set toc.names = New ColTextByLang
    For i = 1 To IdiomsInfo.count
        Set titleAndLang = New ClsTextByLang
        titleAndLang.lang = IdiomsInfo(i).Code
        titleAndLang.text = TxtHeader(i).text
                
        Call toc.names.add(titleAndLang)
            
    Next
    
    
    For k = 1 To LVSections.ListItems.count
        Set section = New ClsSection
        section.sectionCode = LVSections.ListItems(k).text
        
        For i = 1 To IdiomsInfo.count
            Set titleAndLang = New ClsTextByLang
            titleAndLang.lang = IdiomsInfo(i).Code
            titleAndLang.text = LVSections.ListItems(k).SubItems(i)
    
            section.sectionNames.add titleAndLang
        Next
        toc.sections.add section, section.sectionCode
    Next
    Set getNewTOC = toc
End Function


