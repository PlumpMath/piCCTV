@ECHO OFF
SETLOCAL

if -%2-==-- GOTO SYNTAX

scp 'pi@%~1:~/cctv_capture/%~2' .

GOTO END

:SYNTAX
ECHO example : %0 192.168.0.15 "2015\ 05\ 18-22*"

:END
ENDLOCAL