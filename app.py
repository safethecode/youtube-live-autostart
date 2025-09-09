from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle, os
import datetime
import time
from pytz import timezone

SCOPES = [
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl"
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


def change_broadcast_visibility(youtube, broadcast_id, privacy_status="public"):
    """Change broadcast visibility from private to public"""
    try:
        request = youtube.liveBroadcasts().get(
            part="id,snippet,status",
            id=broadcast_id
        )
        response = request.execute()
        
        if not response.get("items"):
            print(f"❌ Broadcast {broadcast_id} not found")
            return False
            
        broadcast = response["items"][0]
        
        broadcast["status"]["privacyStatus"] = privacy_status
        
        update_request = youtube.liveBroadcasts().update(
            part="id,snippet,status",
            body=broadcast
        )
        update_response = update_request.execute()
        
        print(f"✅ Broadcast visibility changed to {privacy_status}: {broadcast_id}")
        return True
        
    except Exception as e:
        print(f"❌ Error changing broadcast visibility: {e}")
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
            
        time.sleep(30)
    
    return True


if __name__ == "__main__":
    youtube = get_authenticated_service()

    keyword = "인천순복음교회 성령충만기도회"
    
    test_mode = False

    print(f"🧪 Test mode: {'ON' if test_mode else 'OFF'}")
    broadcast_id = find_broadcast(youtube, keyword, test_mode=test_mode)
    
    if broadcast_id:
        print("📋 Found broadcast, starting automated workflow...")
        
        print("⏰ Step 1: Waiting until 7:30 PM KST to change visibility to public...")
        wait_until_scheduled_time(19, 30, "visibility change to public")
        
        print("🔓 Changing broadcast visibility from private to public...")
        change_broadcast_visibility(youtube, broadcast_id, "public")
        
        print("⏰ Step 2: Waiting until 7:44 PM KST to start streaming...")
        wait_until_scheduled_time(19, 44, "stream start")
        
        print("🎬 Starting broadcast...")
        start_broadcast(youtube, broadcast_id)
        
        print("✅ All tasks completed successfully!")
    else:
        print("❌ No broadcast found to process.")
