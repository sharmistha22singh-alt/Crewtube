import json
import os
from openai import OpenAI

class Creator:
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY", "")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def create_script_and_assets(self, research_json, previous_feedback_json=None):
        """
        Transforms the research document into a highly engaging YouTube video script using LLM.
        Structures the script with a strong hook, informative body, and clear CTA.
        Generates prompt instructions for external visual/audio generation tools.
        """
        print("[Creator] Drafting script and visual assets...")
        try:
            research = json.loads(research_json)
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON research doc."})

        topic = research.get("topic", "")
        
        if not self.client:
             print("[Creator] WARNING: No OPENAI_API_KEY found, using mock LLM response.")
             return json.dumps({
                 "hook": f"Mock Hook for {topic}!",
                 "body": "Mock body content.",
                 "call_to_action": "Mock CTA!",
                 "visual_prompts": ["Prompt 1"],
                 "seo_keywords": research.get("seo_keywords", [])
             })

        feedback_instruction = ""
        if previous_feedback_json:
             feedback = json.loads(previous_feedback_json)
             feedback_instruction = f"IMPORTANT: Your previous draft was rejected. Manager Feedback: {feedback.get('feedback', '')}. You MUST address this."

        prompt = f"""
        You are a top-tier YouTube Scriptwriter and Visual Director.
        Topic: {topic}
        Research Material: {json.dumps(research)}
        {feedback_instruction}
        
        Draft a highly engaging, retention-optimized YouTube video script.
        
        Output a JSON object exactly with these keys:
        - "hook": The first 10-15 seconds script designed to retain viewers.
        - "body": The main content of the video.
        - "call_to_action": The specific sign-off and call to action.
        - "visual_prompts": A list of 3-5 text-to-image/video prompts for B-roll generation.
        - "seo_keywords": The keywords passed from the research phase.
        """

        try:
             response = self.client.chat.completions.create(
                 model="gpt-3.5-turbo",
                 response_format={ "type": "json_object" },
                 messages=[
                     {"role": "system", "content": "You are a YouTube Script Creator. Respond in JSON."},
                     {"role": "user", "content": prompt}
                 ]
             )
             return response.choices[0].message.content
        except Exception as e:
             print(f"[Creator] LLM Error: {e}")
             return json.dumps({"error": str(e)})
