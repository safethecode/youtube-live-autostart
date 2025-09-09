@echo off
REM filepath: /Users/aaron-son/Documents/youtube-live-autostart/status.bat

REM Check if PID file exists
IF EXIST youtube_autostart.pid (
    SET /p PID=<youtube_autostart.pid
    echo 📊 Checking process status (PID: %PID%)...

    REM Check if process is running
    tasklist /FI "PID eq %PID%" | find "%PID%" >nul
    IF %ERRORLEVEL%==0 (
        echo ✅ Process is running
        echo 📝 Recent logs:
        echo ----------------------------------------
        REM Show last 10 lines of log (PowerShell)
        powershell -Command "Get-Content -Path 'youtube_autostart.log' -Tail 10"
        echo ----------------------------------------
        echo 📊 To view live logs: powershell -Command \"Get-Content -Path 'youtube_autostart.log' -Wait\"
    ) ELSE (
        echo ❌ Process is not running (PID file exists but process not found)
        del youtube_autostart.pid
    )
) ELSE (
    echo ❌ No PID file found. Process is not running.
)