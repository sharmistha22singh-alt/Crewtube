import json
import os
from openai import OpenAI
from utils.youtube_api import YouTubeAPI

class Publisher:
    def __init__(self):
        self.yt_api = YouTubeAPI()
        self.api_key = os.environ.get("OPENAI_API_KEY", "")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def prepare_and_publish(self, approved_script_json):
        """
        Receives the approved content package.
        Uses LLM to write highly clickable, clickbait-free video titles and SEO descriptions.
        Formats tags and metadata for YouTube API, then uploads.
        """
        print("[Publisher] Preparing metadata and publishing...")
        try:
            script_data = json.loads(approved_script_json)
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON script provided to Publisher."})

        script = script_data.get("script_data", {})
        
        if not self.client:
             print("[Publisher] WARNING: No OPENAI_API_KEY found, using mock LLM response.")
             metadata = {
                 "snippet": {
                     "title": "Mock Title",
                     "description": "Mock Description",
                     "tags": script.get("seo_keywords", [])[:15],
                     "categoryId": "28"
                 },
                 "status": {
                     "privacyStatus": "public",
                     "selfDeclaredMadeForKids": False
                 }
             }
             return json.dumps(self.yt_api.upload_video(metadata))

        prompt = f"""
        You are an expert YouTube Metadata Optimizer.
        Based on the following approved script content, generate an optimized Title, Description, and Tags.
        
        Script Content:
        {json.dumps(script)}
        
        Output a JSON object with:
        - "title": A highly clickable, clickbait-free title (max 60 chars).
        - "description": An SEO-optimized description including timestamps and hashtags.
        - "tags": A list of up to 15 relevant SEO tags.
        """

        try:
             response = self.client.chat.completions.create(
                 model="gpt-3.5-turbo",
                 response_format={ "type": "json_object" },
                 messages=[
                     {"role": "system", "content": "You are a YouTube SEO Publisher. Respond in JSON."},
                     {"role": "user", "content": prompt}
                 ]
             )
             llm_metadata = json.loads(response.choices[0].message.content)
             
             metadata = {
                 "snippet": {
                     "title": llm_metadata.get("title", "Generated Title"),
                     "description": llm_metadata.get("description", "Generated Description"),
                     "tags": llm_metadata.get("tags", [])[:15],
                     "categoryId": "28"  # Science & Technology
                 },
                 "status": {
                     "privacyStatus": "public",
                     "selfDeclaredMadeForKids": False
                 }
             }
             
             return json.dumps(self.yt_api.upload_video(metadata))
             
        except Exception as e:
             print(f"[Publisher] LLM Error: {e}")
             return json.dumps({"error": str(e)})
