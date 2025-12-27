
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload

def authenticate_youtube():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"
    
    client_secrets_file = "credentials.json"

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes=["https://www.googleapis.com/auth/youtube.upload"]
    )

    credentials = flow.run_local_server(port=0)
    
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials
    )
    
    return youtube

def upload_video_to_youtube(youtube, video_file, title, description, tags):
    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
        },
        "status": {
            "privacyStatus": "public",
        },
    }

    media_file = MediaFileUpload(video_file, mimetype="video/mp4", resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media_file
    )

    response = request.execute()
    print(f"Uploaded video with ID: {response['id']}")

# Example Usage
if __name__ == "__main__":
    youtube = authenticate_youtube()
    video_file = "product_video.mp4"
    title = "High-End Laptop"
    description = f"Check out this amazing product! Buy it now: https://www.amazon.com/dp/B08P2M9JFF?tag=your_amazon_affiliate_tag"
    tags = ["electronics", "laptops", "tech"]
    upload_video_to_youtube(youtube, video_file, title, description, tags)
