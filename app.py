from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle, os
import datetime
import time
import argparse
from pytz import timezone

SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",
    "https://www.googleapis.com/auth/youtube.readonly"
]

def get_authenticated_service():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build("youtube", "v3", credentials=creds)


def find_broadcast(youtube, keyword, test_mode=False):
    try:
        broadcast_statuses = ["upcoming", "live", "active"] if test_mode else ["upcoming"]
        
        for status in broadcast_statuses:
            print(f"🔍 Searching for broadcasts with status: {status}")
            request = youtube.liveBroadcasts().list(
                part="id,snippet,status",
                broadcastStatus=status,
                maxResults=10
            )
            response = request.execute()

            for item in response.get("items", []):
                title = item["snippet"]["title"]
                current_status = item["status"]["lifeCycleStatus"]
                print(f"📺 Found broadcast: '{title}' (Status: {current_status})")
                
                if keyword in title:
                    print(f"✅ Found matching broadcast: {title}")
                    return item["id"]
        
        print("❌ No matching broadcast found.")
        return None
    except Exception as e:
        print(f"❌ Error finding broadcast: {e}")
        if "liveStreamingNotEnabled" in str(e):
            print("💡 Please enable live streaming on your YouTube channel:")
            print("   1. Go to YouTube Studio")
            print("   2. Enable live streaming in your channel settings")
            print("   3. Verify your channel if required")
        return None


def start_broadcast(youtube, broadcast_id):
    try:
        request = youtube.liveBroadcasts().transition(
            broadcastStatus="live",
            id=broadcast_id,
            part="id,snippet,status"
        )
        response = request.execute()
        print("🎬 Broadcast started:", response["id"])
    except Exception as e:
        print(f"❌ Error starting broadcast: {e}")


def end_broadcast(youtube, broadcast_id):
    """End the live broadcast"""
    try:
        request = youtube.liveBroadcasts().transition(
            broadcastStatus="complete",
            id=broadcast_id,
            part="id,snippet,status"
        )
        response = request.execute()
        print("🛑 Broadcast ended:", response["id"])
        return True
    except Exception as e:
        print(f"❌ Error ending broadcast: {e}")
        return False


def change_broadcast_visibility(youtube, broadcast_id, privacy_status="public"):
    """Change broadcast visibility from private to public"""
    try:
        print(f"🔍 Getting broadcast details for ID: {broadcast_id}")
        
        get_response = youtube.liveBroadcasts().list(
            part="id,snippet,status",
            id=broadcast_id
        ).execute()
        
        print(f"📋 API Response: {get_response}")
        
        if not get_response.get("items"):
            print(f"❌ Broadcast {broadcast_id} not found")
            return False
            
        broadcast = get_response["items"][0]
        current_privacy = broadcast["status"].get("privacyStatus", "unknown")
        broadcast_title = broadcast["snippet"].get("title", "Unknown")
        
        print(f"📺 Broadcast: '{broadcast_title}'")
        print(f"📋 Current privacy status: {current_privacy}")
        
        if current_privacy == privacy_status:
            print(f"ℹ️  Privacy status is already {privacy_status}, no change needed")
            return True
        
        broadcast["status"]["privacyStatus"] = privacy_status
        
        print(f"🔄 Updating privacy status to {privacy_status}...")
        
        update_response = youtube.liveBroadcasts().update(
            part="id,snippet,status",
            body=broadcast
        ).execute()
        
        print(f"✅ Broadcast visibility changed from {current_privacy} to {privacy_status}: {broadcast_id}")
        return True
        
    except Exception as e:
        print(f"❌ Error changing broadcast visibility: {e}")
        print(f"   Error type: {type(e).__name__}")
        import traceback
        print(f"   Traceback: {traceback.format_exc()}")
        return False


def wait_until_scheduled_time(target_hour, target_minute, action_description):
    """Wait until the scheduled time and return when reached"""
    korea_tz = timezone('Asia/Seoul')
    
    while True:
        now_korea = datetime.datetime.now(korea_tz)
        current_hour = now_korea.hour
        current_minute = now_korea.minute
        
        print(f"🕐 Current time (KST): {now_korea.strftime('%H:%M:%S')} - Waiting for {action_description} at {target_hour}:{target_minute:02d}")
        
        if current_hour >= target_hour and current_minute >= target_minute:
            print(f"⏰ Scheduled time reached! ({target_hour}:{target_minute:02d}) - {action_description}")
            break
            
        time.sleep(10)
    
    return True


def parse_time_string(time_str):
    """Parse time string in format 'HH:MM' and return hour, minute"""
    try:
        hour, minute = map(int, time_str.split(':'))
        if not (0 <= hour <= 23 and 0 <= minute <= 59):
            raise ValueError("Invalid time range")
        return hour, minute
    except ValueError as e:
        raise argparse.ArgumentTypeError(f"Invalid time format '{time_str}'. Use HH:MM format (e.g., 19:30)")

def main():
    parser = argparse.ArgumentParser(
        description="YouTube Live Autostart - Automatically manage broadcast visibility and streaming",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Use default times (7:30 PM visibility, 7:44 PM stream start, 9:30 PM end)
  python app.py

  # Custom times for testing
  python app.py --visibility-time 19:30 --stream-time 19:44 --end-time 21:30

  # Test with different keyword and custom end time
  python app.py --keyword "테스트 방송" --visibility-time 20:00 --stream-time 20:15 --end-time 22:00

  # Enable test mode (searches all broadcast statuses)
  python app.py --test-mode
        """
    )
    
    parser.add_argument(
        '--visibility-time', 
        type=parse_time_string,
        default=(19, 30),
        help='Time to change visibility from private to public (default: 19:30)'
    )
    
    parser.add_argument(
        '--stream-time',
        type=parse_time_string, 
        default=(19, 44),
        help='Time to start streaming (default: 19:44)'
    )
    
    parser.add_argument(
        '--keyword',
        type=str,
        default="인천순복음교회 성령충만기도회",
        help='Keyword to search for in broadcast titles (default: "인천순복음교회 성령충만기도회")'
    )
    
    parser.add_argument(
        '--end-time',
        type=parse_time_string,
        default=(21, 30),
        help='Time to end stream and change visibility to private (default: 21:30)'
    )
    
    parser.add_argument(
        '--test-mode',
        action='store_true',
        help='Enable test mode (searches all broadcast statuses including live/active)'
    )
    
    args = parser.parse_args()
    
    visibility_hour, visibility_minute = args.visibility_time
    stream_hour, stream_minute = args.stream_time
    end_hour, end_minute = args.end_time
    
    print("🚀 YouTube Live Autostart")
    print("=" * 50)
    print(f"🔍 Keyword: {args.keyword}")
    print(f"🔓 Visibility change: {visibility_hour:02d}:{visibility_minute:02d} KST")
    print(f"🎬 Stream start: {stream_hour:02d}:{stream_minute:02d} KST")
    print(f"🛑 Stream end: {end_hour:02d}:{end_minute:02d} KST")
    print(f"🧪 Test mode: {'ON' if args.test_mode else 'OFF'}")
    print("=" * 50)
    
    youtube = get_authenticated_service()
    broadcast_id = find_broadcast(youtube, args.keyword, test_mode=args.test_mode)
    
    if broadcast_id:
        print("📋 Found broadcast, starting automated workflow...")
        
        # Step 1: Wait until visibility time to change from private to public
        print(f"⏰ Step 1: Waiting until {visibility_hour:02d}:{visibility_minute:02d} KST to change visibility to public...")
        wait_until_scheduled_time(visibility_hour, visibility_minute, "visibility change to public")
        
        print("🔓 Changing broadcast visibility from private to public...")
        change_broadcast_visibility(youtube, broadcast_id, "public")
        
        # Step 2: Wait until stream time to start streaming
        print(f"⏰ Step 2: Waiting until {stream_hour:02d}:{stream_minute:02d} KST to start streaming...")
        wait_until_scheduled_time(stream_hour, stream_minute, "stream start")
        
        print("🎬 Starting broadcast...")
        start_broadcast(youtube, broadcast_id)
        
        # Step 3: Wait until end time to end stream and change visibility to private
        print(f"⏰ Step 3: Waiting until {end_hour:02d}:{end_minute:02d} KST to end stream and change visibility to private...")
        wait_until_scheduled_time(end_hour, end_minute, "stream end and visibility change to private")
        
        print("🛑 Ending broadcast...")
        end_broadcast(youtube, broadcast_id)
        
        print("🔒 Changing broadcast visibility from public to private...")
        change_broadcast_visibility(youtube, broadcast_id, "private")
        
        print("✅ All tasks completed successfully!")
    else:
        print("❌ No broadcast found to process.")

if __name__ == "__main__":
    main()
