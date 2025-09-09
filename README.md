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
# Start in background
./run_background.sh

# Check status
./status.sh

# Stop process
./stop_background.sh
```

### Direct Execution

```bash
# Activate virtual environment
source venv/bin/activate

# Run directly
python app.py
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

- **Keyword**: `"인천순복음교회 성령충만기도회"` (configurable in `app.py`)
- **Visibility Change**: 7:30 PM KST (configurable in main workflow)
- **Stream Start**: 7:44 PM KST (configurable in main workflow)
- **Test Mode**: Set to `False` for production use

## Requirements

- Python 3.7+
- Google YouTube API credentials
- Required Python packages (see `requirements.txt`)
