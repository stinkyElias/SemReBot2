\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{mtprarprt}[2023/09/13 Report class for the Robotics and Automation group at MTP, NTNU]

\LoadClass[
headings=standardclasses,
a4paper,
11pt,
twoside=false,
headsepline=false,
]{scrbook}

\RequirePackage[english]{isodate}
\isodate

\RequirePackage{lineno}
%% PATCH AMS FOR LINENO
\newcommand*\patchAmsMathEnvironmentForLineno[1]{%
  \expandafter\let\csname old#1\expandafter\endcsname\csname #1\endcsname
  \expandafter\let\csname oldend#1\expandafter\endcsname\csname end#1\endcsname
  \renewenvironment{#1}%
     {\linenomath\csname old#1\endcsname}%
     {\csname oldend#1\endcsname\endlinenomath}}% 
\newcommand*\patchBothAmsMathEnvironmentsForLineno[1]{%
  \patchAmsMathEnvironmentForLineno{#1}%
  \patchAmsMathEnvironmentForLineno{#1*}}%
\AtBeginDocument{%
\patchBothAmsMathEnvironmentsForLineno{equation}%
\patchBothAmsMathEnvironmentsForLineno{align}%
\patchBothAmsMathEnvironmentsForLineno{flalign}%
\patchBothAmsMathEnvironmentsForLineno{alignat}%
\patchBothAmsMathEnvironmentsForLineno{gather}%
\patchBothAmsMathEnvironmentsForLineno{multline}%
}

\RequirePackage{setspace}

\DeclareOption{draft}{
  \linenumbers
  \doublespacing
}

\setkomafont{captionlabel}{\bfseries}
\setcapindent{0em}

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{scrbook}}
\ProcessOptions\relax

\RequirePackage[utf8]{inputenc} 
\RequirePackage{csquotes}
\RequirePackage[english]{babel}
\RequirePackage[T1]{fontenc} 
\RequirePackage{lmodern}

\RequirePackage{amsmath}
\RequirePackage{amsfonts}
\RequirePackage{graphicx}


\RequirePackage[draft=false,automark]{scrlayer-scrpage}
\setkomafont{pageheadfoot}{\normalfont}
\clearpairofpagestyles
\lohead{\headmark}
\rehead{\headmark}
\rohead{\pagemark}
\lehead{\pagemark}
\pagestyle{scrheadings}


\RequirePackage[
backend=biber,
style=numeric,
backref=false,
maxbibnames=99
]{biblatex}

\setkomafont{descriptionlabel}{\bfseries}

\RequirePackage[a4paper,top=25mm,bottom=30mm,left=25mm,right=25mm,marginparwidth=1.75cm]{geometry}
\RequirePackage{parskip}

\RequirePackage{hyperref}
\hypersetup{
  colorlinks=true, 
  citecolor=blue,
  linkcolor=blue,
  filecolor=blue,
  urlcolor=blue,
}
\raggedbottom