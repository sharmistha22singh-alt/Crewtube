# Multi-Agent YouTube Channel Automation

This project implements an automated, multi-agent system designed to autonomously operate a YouTube channel. The pipeline divides tasks across specialized AI agents working hierarchically, covering trend analysis, research, content creation, and publishing.

## System Architecture

The workflow consists of four specialized agents coordinated in a pipeline:

1. **The Channel Manager (Lead Strategist)** (`agents/manager.py`)
   - Analyzes trends and past video performance.
   - Generates content briefs with SEO goals.
   - Performs Quality Control (QC) by reviewing scripts before deployment.
   - Saves performance metrics to memory (`utils/memory.py`).

2. **The Researcher (Data & SEO Specialist)** (`agents/researcher.py`)
   - Receives topics from the Manager.
   - Scrapes the web for facts, stats, and SEO keywords.
   - Outputs a compiled research document.

3. **The Creator (Scriptwriter & Visual Director)** (`agents/creator.py`)
   - Transforms research into an engaging YouTube script.
   - Incorporates a strong hook, informative body, and clear Call to Action (CTA).
   - Generates visual/audio prompts for external generation tools.
   - Listens to the Manager's feedback if a script fails QC and revises accordingly.

4. **The Publisher (Distribution Expert)** (`agents/publisher.py`)
   - Receives approved scripts from the Manager.
   - Generates metadata (Titles, Descriptions, Tags).
   - Simulates uploading the video using the YouTube Data API v3 (`utils/youtube_api.py`).

## Communication

To prevent infinite loops and ensure seamless data transfer, **all agents communicate via structured JSON**. 
- The Manager generates a JSON brief.
- The Researcher generates a JSON research document.
- The Creator outputs a JSON script package.
- The Manager reviews the script and outputs a JSON approval/feedback response.
- The Publisher outputs a JSON API response.

## Setup and Deployment

1. **Clone the repository:**
   Ensure you have the project directory on your local machine or server.

2. **Install dependencies:**
   It is recommended to use a virtual environment.
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Configuration:**
   Create a `.env` file in the root directory and add your OpenAI API key.
   ```
   OPENAI_API_KEY=your_actual_openai_api_key_here
   ```
   *Note: If no API key is provided, the agents will safely fall back to using hardcoded mock responses for demonstration purposes.*

## Running and Testing the Simulation

To execute a single run of the pipeline, run the main orchestration script:

```bash
python main.py
```

This will execute the entire pipeline from Initiation to Deployment, logging the interactions and JSON payloads exchanged between the agents in the terminal. You can review the logs to see the actual topics generated, facts scraped, scripts written, and the simulated upload response.

### Running as a Scheduled Job (Cron)
If you wish to deploy this as an autonomous cron job on a Linux server to run, for instance, every Monday at 9:00 AM, you can add an entry like this to your crontab (`crontab -e`):

```bash
0 9 * * 1 cd /path/to/project && /path/to/venv/bin/python main.py >> /var/log/youtube_agents.log 2>&1
```