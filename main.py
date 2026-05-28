import json
from utils import load_environment
from agents.manager import ChannelManager
from agents.researcher import Researcher
from agents.creator import Creator
from agents.publisher import Publisher

def run_pipeline():
    load_environment()
    print("=== Initiating Multi-Agent YouTube Automation Pipeline ===")
    
    # Initialize agents
    manager = ChannelManager()
    researcher = Researcher()
    creator = Creator()
    publisher = Publisher()
    
    # 1. Initiation & Briefing
    print("\n--- Phase 1: Initiation & Briefing ---")
    current_trends = ["Agentic Workflows 2024", "OpenAI API"]
    brief_json = manager.generate_topic(current_trends)
    print("Manager generated brief:\n", json.dumps(json.loads(brief_json), indent=2))
    
    # 2. Data Gathering
    print("\n--- Phase 2: Data Gathering ---")
    research_json = researcher.conduct_research(brief_json)
    print("Researcher generated research doc:\n", json.dumps(json.loads(research_json), indent=2))
    
    # 3. Creation & 4. Quality Control Loop
    print("\n--- Phase 3 & 4: Creation and Quality Control ---")
    max_revisions = 3
    revision_count = 0
    approved = False
    approved_script_json = None
    feedback_json = None
    
    while not approved and revision_count < max_revisions:
        print(f"Drafting script (Attempt {revision_count + 1})...")
        script_json = creator.create_script_and_assets(research_json, previous_feedback_json=feedback_json)
        
        is_approved, review_result_json = manager.review_script(script_json)
        
        if is_approved:
            print("Manager approved the script!")
            approved = True
            approved_script_json = review_result_json
        else:
            print("Manager rejected the script. Providing feedback...")
            feedback_json = review_result_json
            print("Feedback:", json.dumps(json.loads(feedback_json), indent=2))
            revision_count += 1
            
    if not approved:
        print("Failed to get an approved script after maximum revisions. Aborting pipeline.")
        return
        
    # 5. Deployment
    print("\n--- Phase 5: Deployment ---")
    publish_result_json = publisher.prepare_and_publish(approved_script_json)
    publish_result = json.loads(publish_result_json)
    
    if publish_result.get("status") == "success":
        print("\nSuccess! Video Uploaded. Simulating gathering performance data...")
        # Simulate video performance and record to memory
        video_id = publish_result.get("video_id")
        manager.record_performance(video_id, views=15000, retention_rate=0.65)
        print("Pipeline Complete.")
    else:
        print("\nDeployment failed:", publish_result)

if __name__ == "__main__":
    run_pipeline()
