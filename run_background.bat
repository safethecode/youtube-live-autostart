@echo off
REM filepath: /Users/aaron-son/Documents/youtube-live-autostart/run_background.bat

REM YouTube Live Autostart Background Runner (Windows version)
REM This script runs app.py in the background with optional arguments

echo 🚀 Starting YouTube Live Autostart in background...

REM Check if arguments are provided
IF "%~1"=="" (
    echo 📅 Using default schedule: visibility at 7:30 PM, stream at 7:44 PM KST
    SET ARGS=
) ELSE (
    echo 📅 Using custom arguments: %*
    SET ARGS=%*
)

REM Activate virtual environment
CALL venv\Scripts\activate

REM Run app.py in background and redirect output to log file
start /b python app.py %ARGS% > youtube_autostart.log 2>&1

REM Get the last started python process PID
for /f "tokens=2" %%a in ('tasklist /FI "IMAGENAME eq python.exe" /NH') do set PID=%%a

echo ✅ Process started with PID: %PID%
echo 📝 Logs are being written to: youtube_autostart.log
echo 🛑 To stop the process, run: taskkill /PID %PID%
echo 📊 To view logs, run: type youtube_autostart.log

REM Save PID to file for easy management
echo %PID% > youtube_autostart.pid
echo 💾 Process ID saved to: youtube_autostart.pid

echo.
echo 💡 Usage examples:
echo   run_background.bat                                    ^<== Default times
echo   run_background.bat --visibility-time 20:00 --stream-time 20:15
echo   run_background.bat --keyword "테스트 방송" --test-mode