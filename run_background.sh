#!/bin/bash

echo "🚀 Starting YouTube Live Autostart in background..."
echo "📅 Scheduled to change visibility at 7:44 PM KST"

source venv/bin/activate
nohup python app.py > youtube_autostart.log 2>&1 &

PID=$!
echo "✅ Process started with PID: $PID"
echo "📝 Logs are being written to: youtube_autostart.log"
echo "🛑 To stop the process, run: kill $PID"
echo "📊 To view logs, run: tail -f youtube_autostart.log"

echo $PID > youtube_autostart.pid
echo "💾 Process ID saved to: youtube_autostart.pid"
