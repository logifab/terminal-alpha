import datetime
import requests


def fetch_velocity_spikes():
  seven_days_ago = (
      datetime.datetime.utcnow() - datetime.timedelta(days=7)
  ).strftime("%Y-%m-%d")
  url = f"https://api.github.com/search/repositories?q=created:>{seven_days_ago}+sort:stars-desc&per_page=5"
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
            "created": item.get("created_at")[:10],
            "description": item.get(
                "description", "No description provided."
            ),
            "url": item.get("html_url"),
        })
      return repos
  except Exception as e:
    print(f"API fetch error: {e}")

  return []


def generate_briefing():
  repos = fetch_velocity_spikes()
  timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

  content = f"""# MATRIX INTELLIGENCE BRIEFING // {timestamp}
## Autonomous Anomaly Scan: 7-Day High-Velocity New Repository Spikes

---

"""

  if not repos:
    content += (
        "_No anomalous velocity spikes detected in the current window._\n"
    )
  else:
    for idx, repo in enumerate(repos, 1):
      content += f"""### {idx}. [{repo['name']}]({repo['url']})
* **Created:** {repo['created']}
* **Velocity Gain:** +{repo['stars']} stars this week
* **Vector Analysis:** {repo['description']}

"""

    # Generate a ready-to-post LinkedIn artifact using the #1 top velocity repo
    top_repo = repos[0]
    content += f"""---

## 🔗 Ready-to-Publish LinkedIn Post Artifact

```text
The bleeding edge is moving faster than ever. 

Anomalous velocity spike detected on GitHub this week: {top_repo['name']} just pulled +{top_repo['stars']} stars in days.

What it is: {top_repo['description']}

Why it matters: While everyone is looking at last year's tech stacks, early-stage infrastructure is shifting toward zero-dependency, highly portable execution layers. 

Source: {top_repo['url']}

#AI #TechTrends #SoftwareEngineering #BuildInPublic
