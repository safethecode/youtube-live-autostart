# YouTube Live Autostart

Automatically starts scheduled YouTube live broadcasts and changes visibility from private to public at specified times.

## Features

- 🔍 **Auto Discovery**: Finds YouTube broadcasts by keyword
- 🎬 **Auto Start**: Automatically starts live broadcasts
- ⏰ **Scheduled Visibility**: Changes broadcast visibility from private to public at 7:30 PM KST
- 🎬 **Scheduled Start**: Automatically starts streaming at 7:44 PM KST
- 🕐 **Timezone Aware**: Uses Korea Standard Time (KST) for accurate scheduling
- 🔄 **Background Execution**: Runs in background without requiring cron jobs

## Setup

1. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure OAuth**

   - Copy `client_secret.example.json` to `client_secret.json`
   - Fill in your Google OAuth credentials
   - Run the app once to authenticate and generate `token.pickle`

3. **Configure Broadcast**
   - Update the `keyword` variable in `app.py` to match your broadcast title
   - Adjust the scheduled times (7:30 PM for visibility, 7:44 PM for stream start) if needed

## Usage

### Background Execution (Recommended)

```bash
# Start in background with default times
./run_background.sh

# Start with custom times
./run_background.sh --visibility-time 20:00 --stream-time 20:15

# Start with different keyword and test mode
./run_background.sh --keyword "테스트 방송" --test-mode

# Check status
./status.sh

# Stop process
./stop_background.sh
```

### Direct Execution

```bash
# Activate virtual environment
source venv/bin/activate

# Run with default times (7:30 PM visibility, 7:44 PM stream start)
python app.py

# Run with custom times
python app.py --visibility-time 20:00 --stream-time 20:15

# Run with different keyword
python app.py --keyword "테스트 방송" --visibility-time 19:30 --stream-time 19:45

# Run in test mode (searches all broadcast statuses)
python app.py --test-mode

# Show help
python app.py --help
```

## Process Management

- **Logs**: Check `youtube_autostart.log` for detailed output
- **PID**: Process ID is saved in `youtube_autostart.pid`
- **Status**: Use `./status.sh` to check if process is running
- **Stop**: Use `./stop_background.sh` to stop the process

## Workflow

1. 🔍 Searches for upcoming broadcasts matching the keyword
2. ⏰ Waits until 7:30 PM KST
3. 🔓 Changes visibility from private to public
4. ⏰ Waits until 7:44 PM KST
5. 🎬 Starts the broadcast (transitions to live)
6. ✅ Completes successfully

## Configuration

### Command Line Arguments

- `--visibility-time HH:MM`: Time to change visibility from private to public (default: 19:30)
- `--stream-time HH:MM`: Time to start streaming (default: 19:44)
- `--keyword "TEXT"`: Keyword to search for in broadcast titles (default: "인천순복음교회 성령충만기도회")
- `--test-mode`: Enable test mode (searches all broadcast statuses including live/active)
- `--help`: Show help message with usage examples

### Default Settings

- **Keyword**: `"인천순복음교회 성령충만기도회"`
- **Visibility Change**: 7:30 PM KST
- **Stream Start**: 7:44 PM KST
- **Test Mode**: Disabled by default

## Requirements

- Python 3.7+
- Google YouTube API credentials
- Required Python packages (see `requirements.txt`)
