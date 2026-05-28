import json
import os
from openai import OpenAI
from utils.memory import Memory

class ChannelManager:
    def __init__(self):
        self.memory = Memory()
        # Default to a mock if no API key is provided
        self.api_key = os.environ.get("OPENAI_API_KEY", "")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def _call_llm(self, prompt, system_prompt="You are a YouTube Channel Manager."):
        if not self.client:
            # Fallback mock behavior if no key is set
            print("[Manager] WARNING: No OPENAI_API_KEY found, using mock LLM response.")
            if "Generate a topic" in prompt:
                return json.dumps({
                    "topic": "How to automate YouTube with AI",
                    "seo_goals": ["AI automation", "YouTube API"],
                    "target_audience": "Tech enthusiasts",
                    "required_retention_hook": "Mention potential revenue growth in first 10 seconds"
                })
            else:
                return json.dumps({"status": "Approved", "feedback": ""})

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                response_format={ "type": "json_object" },
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"[Manager] LLM Error: {e}")
            return json.dumps({"error": str(e)})

    def generate_topic(self, current_trends):
        """
        Analyzes current trends, niche demands, and audience retention metrics.
        Generates a weekly content calendar and assigns specific topics.
        """
        past_videos = self.memory.get_all()
        
        print("[Manager] Analyzing trends and past performance...")
        
        prompt = f"""
        Generate a topic brief based on the current trends: {current_trends}.
        Past video performance: {json.dumps(past_videos)}
        
        Output a JSON object with the following keys:
        - "topic": The video topic title.
        - "seo_goals": A list of 3-5 target keywords.
        - "target_audience": A description of the target audience.
        - "required_retention_hook": A specific direction for the hook to keep retention high.
        """
        
        brief_json = self._call_llm(prompt)
        return brief_json

    def review_script(self, script_json):
        """
        Reviews the final script and metadata for brand consistency.
        Returns approval status.
        """
        print("[Manager] Reviewing script...")
        
        prompt = f"""
        Review the following YouTube script:
        {script_json}
        
        Does it have a strong 'hook' and a clear 'call_to_action'?
        If it meets quality standards, output JSON: {{"status": "Approved"}}
        If it fails, output JSON: {{"status": "Rejected", "feedback": "<Specific feedback on what to change>"}}
        """
        
        review_result_str = self._call_llm(prompt, system_prompt="You are a strict YouTube Content Reviewer. Respond in JSON.")
        
        try:
            review_result = json.loads(review_result_str)
            if review_result.get("status") == "Approved":
                return True, json.dumps({"status": "Approved", "script_data": json.loads(script_json)})
            else:
                return False, review_result_str
        except json.JSONDecodeError:
             return False, json.dumps({"error": "LLM returned invalid JSON for review."})

    def record_performance(self, video_id, views, retention_rate):
        """
        Records the performance of a published video.
        """
        record = {
            "video_id": video_id,
            "views": views,
            "retention_rate": retention_rate
        }
        self.memory.add_record(record)
        print(f"[Manager] Recorded performance for {video_id}")
