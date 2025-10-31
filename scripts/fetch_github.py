import requests
import json
from datetime import datetime

def fetch_github_repos():
    print("🚀 Starting GitHub repositories fetch...")
    print("📡 Connecting to GitHub API...")
    
    GITHUB_USERNAME = "smartlegionlab"
    EXCLUDED_REPOS = ["smartlegionlab"]
    
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos?sort=updated&per_page=100"
    response = requests.get(url)
    response.raise_for_status()
    
    repos = response.json()
    
    filtered_repos = [
        repo for repo in repos 
        if not repo['archived'] and repo['name'] not in EXCLUDED_REPOS
    ]
    
    sorted_repos = sorted(filtered_repos, key=lambda x: x['pushed_at'], reverse=True)
    
    with open('github_repos.json', 'w', encoding='utf-8') as f:
        json.dump(sorted_repos, f, indent=2, ensure_ascii=False)
    
    print(f"✅ SUCCESS: Fetched {len(sorted_repos)} active repositories")
    print(f"⭐ Total stars: {sum(repo['stargazers_count'] for repo in sorted_repos)}")
    print(f"🍴 Total forks: {sum(repo['forks_count'] for repo in sorted_repos)}")
    print(f"💾 Saved to: github_repos.json")
    print("")

if __name__ == "__main__":
    fetch_github_repos()
