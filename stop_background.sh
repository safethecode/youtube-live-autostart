#!/bin/bash

if [ -f "youtube_autostart.pid" ]; then
    PID=$(cat youtube_autostart.pid)
    echo "🛑 Stopping YouTube Live Autostart process (PID: $PID)..."
    
    if kill $PID 2>/dev/null; then
        echo "✅ Process stopped successfully"
        rm youtube_autostart.pid
    else
        echo "❌ Process not found or already stopped"
        rm youtube_autostart.pid
    fi
else
    echo "❌ No PID file found. Process may not be running."
fi
