@echo off
REM filepath: /Users/aaron-son/Documents/youtube-live-autostart/stop_background.bat

IF EXIST youtube_autostart.pid (
    SET /p PID=<youtube_autostart.pid
    echo 🛑 Stopping YouTube Live Autostart process (PID: %PID%)...

    REM Attempt to stop the process
    taskkill /PID %PID% >nul 2>&1
    IF %ERRORLEVEL%==0 (
        echo ✅ Process stopped successfully
        del youtube_autostart.pid
    ) ELSE (
        echo ❌ Process not found or already stopped
        del youtube_autostart.pid
    )
) ELSE (
    echo ❌ No PID file found. Process may not be running.
)