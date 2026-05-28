import json
import requests
from bs4 import BeautifulSoup
import os
from openai import OpenAI
import urllib.parse

class Researcher:
    def __init__(self):
        self.api_key = os.environ.get("OPENAI_API_KEY", "")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None

    def _scrape_duckduckgo(self, query):
        """
        Perform a simple web scrape of DuckDuckGo HTML results.
        Note: This is a basic implementation for demonstration.
        """
        try:
            url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            results = []
            
            for a in soup.find_all('a', class_='result__snippet', limit=3):
                results.append(a.text.strip())
                
            return " ".join(results)
        except Exception as e:
            print(f"[Researcher] Scraping error: {e}")
            return f"Failed to gather real-time data due to: {e}"

    def conduct_research(self, brief_json):
        """
        Receives topics from the Channel Manager.
        Scrapes the web for accurate facts, engaging statistics, and relevant news.
        Identifies high-volume, low-competition SEO keywords using LLM.
        Compiles a comprehensive research document.
        """
        print("[Researcher] Conducting research based on brief...")
        try:
            brief = json.loads(brief_json)
        except json.JSONDecodeError:
            return json.dumps({"error": "Invalid JSON brief provided to Researcher."})

        topic = brief.get("topic", "Unknown Topic")
        seo_goals = brief.get("seo_goals", [])
        
        print(f"[Researcher] Scraping web for info on: {topic}")
        scraped_data = self._scrape_duckduckgo(topic)

        if not self.client:
             print("[Researcher] WARNING: No OPENAI_API_KEY found, using mock LLM response.")
             facts = ["AI increases output.", "Agents reduce errors."]
             keywords = seo_goals + ["AI tutorial 2024", "Make money"]
             return json.dumps({
                 "topic": topic,
                 "facts_and_stats": facts,
                 "seo_keywords": keywords,
                 "news_context": scraped_data[:100] + "..."
             })
             
        prompt = f"""
        You are an expert YouTube Content Researcher.
        I have a topic: {topic}
        Initial SEO Goals: {seo_goals}
        Here is some raw data scraped from the web: {scraped_data}
        
        Extract engaging facts/statistics and generate high-volume, low-competition SEO keywords.
        
        Output a JSON object with:
        - "topic": {topic}
        - "facts_and_stats": A list of 3-5 interesting facts or statistics.
        - "seo_keywords": A list of 10-15 highly optimized SEO keywords/tags.
        - "news_context": A short summary of the current landscape based on the scraped data.
        """

        try:
             response = self.client.chat.completions.create(
                 model="gpt-3.5-turbo",
                 response_format={ "type": "json_object" },
                 messages=[
                     {"role": "system", "content": "You are a YouTube Researcher. Respond in JSON."},
                     {"role": "user", "content": prompt}
                 ]
             )
             return response.choices[0].message.content
        except Exception as e:
             print(f"[Researcher] LLM Error: {e}")
             return json.dumps({"error": str(e)})
