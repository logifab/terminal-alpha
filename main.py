import datetime
import requests


def fetch_trending_repos():
  # Query GitHub Search API for high-velocity repositories created or updated recently
  url = "https://api.github.com/search/repositories?q=topic:ai+sort:stars-desc&per_page=5"
  headers = {
      "Accept": "application/vnd.github.v3+json",
      "User-Agent": "TerminalAlpha-Engine",
  }

  try:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
      items = response.json().get("items", [])
      repos = []
      for item in items:
        repos.append({
            "name": item.get("full_name"),
            "stars": item.get("stargazers_count"),
            "description": item.get(
                "description", "No description provided."
            ),
            "url": item.get("html_url"),
        })
      return repos
  except Exception as e:
    print(f"API fetch error: {e}")

  # Fallback core intelligence payload if rate-limited
  return [{
      "name": "terminal-alpha/core",
      "stars": "N/A",
      "description": "Autonomous pipeline baseline.",
      "url": "#",
  }]


def generate_briefing():
  repos = fetch_trending_repos()
  timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

  content = f"""# MATRIX INTELLIGENCE BRIEFING // {timestamp}
## Autonomous Anomaly Scan: High-Velocity AI & Agent Tooling

---

"""

  for idx, repo in enumerate(repos, 1):
    content += f"""### {idx}. [{repo['name']}]({repo['url']})
* **Signal Velocity:** {repo['stars']} total stars
* **Vector Analysis:** {repo['description']}

"""

  content += (
      "\n*Generated autonomously by Terminal Alpha. Zero human intervention.*"
  )

  with open("index.md", "w") as f:
    f.write(content)

  print("Refined intelligence briefing compiled to index.md.")


if __name__ == "__main__":
  generate_briefing()
