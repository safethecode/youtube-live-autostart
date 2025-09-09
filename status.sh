#!/bin/bash

if [ -f "youtube_autostart.pid" ]; then
    PID=$(cat youtube_autostart.pid)
    echo "📊 Checking process status (PID: $PID)..."
    
    if ps -p $PID > /dev/null 2>&1; then
        echo "✅ Process is running"
        echo "📝 Recent logs:"
        echo "----------------------------------------"
        tail -10 youtube_autostart.log
        echo "----------------------------------------"
        echo "📊 To view live logs: tail -f youtube_autostart.log"
    else
        echo "❌ Process is not running (PID file exists but process not found)"
        rm youtube_autostart.pid
    fi
else
    echo "❌ No PID file found. Process is not running."
fi
