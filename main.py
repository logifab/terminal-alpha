import os
import requests
import json
from datetime import datetime

# Free API endpoints for raw signal extraction (e.g., GitHub trending or security advisories)
GITHUB_TRENDING_URL = "https://api.github.com/search/repositories?q=created:>2026-07-01&sort=stars&order=desc"

def fetch_raw_signals():
    headers = {"Accept": "application/vnd.github.v3+json"}
    response = requests.get(GITHUB_TRENDING_URL, headers=headers)
    if response.status_code == 200:
        items = response.status_code and response.json().get("items", [])[:5]
        return items
    return []

def compile_intelligence_briefing(data):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    briefing = f"# MATRIX INTELLIGENCE BRIEFING // {timestamp}\n\n"
    briefing += "## Autonomous Anomaly Scan: High-Velocity Repositories & Vector Shifts\n\n"
    
    for idx, repo in enumerate(data, 1):
        name = repo.get("full_name", "Unknown")
        desc = repo.get("description", "No description provided.")
        stars = repo.get("stargazers_count", 0)
        url = repo.get("html_url", "#")
        
        briefing += f"### {idx}. [{name}]({url})\n"
        briefing += f"- **Signal Velocity:** {stars} absolute stars gained.\n"
        briefing += f"- **Vector Analysis:** {desc}\n\n"
        
    briefing += "---\n*Generated autonomously by Terminal Alpha. Zero human intervention.*"
    return briefing

if __name__ == "__main__":
    raw_data = fetch_raw_signals()
    final_output = compile_intelligence_briefing(raw_data)
    
    #  Output to a static file deployed automatically via Vercel/GitHub Pages
    with open("index.md", "w") as f:
        f.write(final_output)
    print("Intelligence briefing compiled and locked.")