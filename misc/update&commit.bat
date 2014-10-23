@echo off
echo. [ SVN Updater ]
:: The SOURCEj below should be already set to fit your system.
echo. Updating %SOURCE%\ from SVN...
"%SVN%\TortoiseProc.exe" /command:update /path:"%SOURCE%\" /closeonend:2
echo.        done.
echo. [ SVN Committer ]
:: The two lines below should be changed to suit your system.
set SOURCE=C:\some_directory_path
set SVN=C:\some_directory_path
echo.
echo. Committing %SOURCE% to SVN...
"%SVN%\TortoiseProc.exe" /command:commit /path:"%SOURCE%" /closeonend:0
echo. done.
echo.
echo. Operation complete.
PAUSE