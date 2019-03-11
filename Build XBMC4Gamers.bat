:: Copyright of John Conn (Rocky5 Forums & JCRocky5 Twitter) 2016
:: Please don't re-release this as your own, if you make a better tool then I don't mind :-)

@Echo off & SetLocal EnableDelayedExpansion & Mode con:cols=100 lines=10 & Color 0B
title XBMC4Gamers Builder

if exist "XBMC" Set "foldername=XBMC"
if exist "Build" Set "foldername=Build"
if not exist "%foldername%" (
	Echo Error, place a fresh copy of XBMC next to this batch file and try again.
	timeout /t 5
	Exit
)
Attrib /s -r -h -s "Thumbs.db" >NUL
Del /Q /S "Thumbs.db" 2>NUL

cls
:menu
CLS & echo:
echo  Select Time formating, this is used for versioning.
echo:
set "entry="
echo  1. DD/MM/YYYY
echo  2. MM/DD/YYYY
echo:
echo  or press "Enter" to exit
echo:
set /p entry=Enter Choice:
if "%entry%"=="1" Set "fromDate=20/12/2018" & Goto Start
if "%entry%"=="2" Set "fromDate=12/20/2018" & Goto Start
if "%entry%"=="" exit
echo Error: Incorrect entry.
timeout /t %Delay%
goto menu

:Start
Set "toDate=%date%"
Set "version=1.2"
(
echo fromDate^=CDate^("%fromDate%"^)
echo toDate^=CDate^("%toDate%"^)
echo WScript.Echo DateDiff^("d",fromDate,toDate,vbMonday^)
)>tmp.vbs
for /f %%a in ('cscript /nologo tmp.vbs') do (
if %%a GEQ 100 Set "daytotal=%%a"
if %%a LSS 100 Set "daytotal=0%%a"
if %%a LSS 10 Set "daytotal=00%%a"
)
del tmp.vbs
cls
Echo: & Echo: & Echo: & Echo   Please wait...

(
rd /q /s "%foldername%\plugins"
rd /q /s "%foldername%\sounds"
rd /q /s "%foldername%\userdata"
rd /q /s "%foldername%\visualisations"
rd /q /s "%foldername%\web"
rd /q /s "%foldername%\system\keymaps"
rd /q /s "%foldername%\system\cdrip"
rd /q /s "%foldername%\system\scrapers"
rd /q /s "%foldername%\system\players\mplayer\codecs"
rd /q /s "%foldername%\scripts"
rd /q /s "%foldername%\skin"
rd /q /s "%foldername%\screensavers"
del /q "%foldername%\system\filezilla server.xml"
del /q "%foldername%\copying.txt"
del /q "%foldername%\keymapping.txt"
del /q "%foldername%\media\icon.png"
del /q "%foldername%\media\Splash_2007.png"
del /q "%foldername%\media\Splash_2008.png"
del /q "%foldername%\media\weather.rar"
move "%foldername%\media" "%foldername%\system\"
move "%foldername%\language" "%foldername%\system\"
move "%foldername%\media" "%foldername%\system\"
move "%foldername%\screenshots" "%foldername%\system\"
move "%foldername%\UserData" "%foldername%\system\"

XCopy /s /e /i /h /r /y "Mod Files" "%foldername%"
copy /y "Changes.txt" "%foldername%"
if exist "Other\build for release" (
	Call Other\Tools\repl.bat "XBMC4Gamers 0.0.000" "XBMC4Gamers %version%.%daytotal%" L < "%foldername%\skins\Profile Skin\language\English\strings.po" >"%foldername%\skins\Profile Skin\language\English\strings.tmp"
	Del "%foldername%\skins\Profile Skin\language\English\strings.po"
	rename "%foldername%\skins\Profile Skin\language\English\strings.tmp" "strings.po"
	Call Other\Tools\repl.bat "	" "" L < "%foldername%\changes.txt" >"%foldername%\changes.tmp"
	copy /b "Other\Tools\Changes\Changes_Header.xml"+"%foldername%\changes.tmp"+"Other\Tools\Changes\Changes_Footer.xml" "%foldername%\skins\Profile Skin\720p\Custom_Changes.xml"
	del /q "%foldername%\changes.tmp"
)
copy "%foldername%\skins\Profile Skin\language\English\strings.po" "%foldername%\skins\Manage Profiles Skin\language\English\strings.po"
copy "%foldername%\skins\Profile Skin\language\English\strings.po" "%foldername%\skins\DVD2Xbox Skin\language\English\strings.po"
del /Q "%foldername%\Changes.txt"
copy /y "New XBMC xbe\default.xbe" "%foldername%\default.xbe"
del /Q /S "%foldername%\*.bat"
del /Q /S "%foldername%\empty"
ren "%foldername%" "XBMC4Gamers"
)
cls
Echo:
Echo: & Echo: & Echo: & Echo   Done...
timeout /t 3 >NUL