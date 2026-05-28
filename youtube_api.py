import json

class YouTubeAPI:
    def __init__(self, api_key=None):
        self.api_key = api_key

    def upload_video(self, metadata):
        """
        Mocks the YouTube Data API v3 video upload endpoint.
        Returns a mock response.
        """
        print(f"[YouTubeAPI] Uploading with metadata:")
        print(json.dumps(metadata, indent=2))
        
        return {
            "status": "success",
            "video_id": "mock_video_id_123",
            "message": "Video successfully scheduled/uploaded via YouTube Data API v3."
        }
