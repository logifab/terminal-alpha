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

  lines = []
  lines.append(f"# MATRIX INTELLIGENCE BRIEFING // {timestamp}")
  lines.append(
      "## Autonomous Anomaly Scan: 7-Day High-Velocity New Repository Spikes"
  )
  lines.append("\n---")

  if not repos:
    lines.append("_No anomalous velocity spikes detected in the current window._")
  else:
    for idx, repo in enumerate(repos, 1):
      lines.append(f"\n### {idx}. [{repo['name']}]({repo['url']})")
      lines.append(f"* **Created:** {repo['created']}")
      lines.append(f"* **Velocity Gain:** +{repo['stars']} stars this week")
      lines.append(f"* **Vector Analysis:** {repo['description']}")

    top_repo = repos[0]
    lines.append("\n---")
    lines.append("\n## 🔗 Ready-to-Publish LinkedIn Post Artifact\n")
    lines.append("The bleeding edge is moving faster than ever.\n")
    lines.append(
        f"Anomalous velocity spike detected on GitHub this week: {top_repo['name']}"
        f" just pulled +{top_repo['stars']} stars in days.\n"
    )
    lines.append(f"What it is: {top_repo['description']}\n")
    lines.append(
        "Why it matters: While everyone is looking at last year's tech stacks,"
        " early-stage infrastructure is shifting toward zero-dependency,"
        " highly portable execution layers.\n"
    )
    lines.append(f"Source: {top_repo['url']}\n")
    lines.append(
        "#AI #TechTrends #SoftwareEngineering #BuildInPublic\n---"
    )

  lines.append(
      "\n*Generated autonomously by Terminal Alpha. Zero human intervention.*"
  )

  content = "\n".join(lines)

  with open("index.md", "w") as f:
    f.write(content)

  print("Intelligence briefing and LinkedIn artifact compiled to index.md.")


if __name__ == "__main__":
  generate_briefing()