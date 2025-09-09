#!/bin/bash

# YouTube Live Autostart Background Runner
# This script runs the app.py in the background with optional arguments

echo "🚀 Starting YouTube Live Autostart in background..."

# Check if arguments are provided
if [ $# -eq 0 ]; then
    echo "📅 Using default schedule: visibility at 7:30 PM, stream at 7:44 PM KST"
    ARGS=""
else
    echo "📅 Using custom arguments: $@"
    ARGS="$@"
fi

# Activate virtual environment and run the script
source venv/bin/activate
nohup python app.py $ARGS > youtube_autostart.log 2>&1 &

# Get the process ID
PID=$!
echo "✅ Process started with PID: $PID"
echo "📝 Logs are being written to: youtube_autostart.log"
echo "🛑 To stop the process, run: kill $PID"
echo "📊 To view logs, run: tail -f youtube_autostart.log"

# Save PID to file for easy management
echo $PID > youtube_autostart.pid
echo "💾 Process ID saved to: youtube_autostart.pid"

echo ""
echo "💡 Usage examples:"
echo "  ./run_background.sh                                    # Default times"
echo "  ./run_background.sh --visibility-time 20:00 --stream-time 20:15"
echo "  ./run_background.sh --keyword \"테스트 방송\" --test-mode"
