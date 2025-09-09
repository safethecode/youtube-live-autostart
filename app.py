from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle, os

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


if __name__ == "__main__":
    youtube = get_authenticated_service()

    keyword = "인천순복음교회 성령충만기도회"
    
    test_mode = False

    print(f"🧪 Test mode: {'ON' if test_mode else 'OFF'}")
    broadcast_id = find_broadcast(youtube, keyword, test_mode=test_mode)
    if broadcast_id:
        start_broadcast(youtube, broadcast_id)
