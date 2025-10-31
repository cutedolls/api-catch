import requests
import json

GITHUB_USERNAME = "smartlegionlab"
EXCLUDED_REPOS = ["smartlegionlab"]

def fetch_github_repos():
    print("📡 Fetching GitHub repositories...")
    
    url = f"https://api.github.com/users/{GITHUB_USERNAME}/repos?sort=updated&per_page=100"
    response = requests.get(url)
    response.raise_for_status()
    
    repos = response.json()
    
    # Фильтруем и сортируем
    filtered_repos = [
        repo for repo in repos 
        if not repo['archived'] and repo['name'] not in EXCLUDED_REPOS
    ]
    
    sorted_repos = sorted(filtered_repos, key=lambda x: x['pushed_at'], reverse=True)
    
    # Сохраняем в корень
    with open('github_repos.json', 'w', encoding='utf-8') as f:
        json.dump(sorted_repos, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Fetched {len(sorted_repos)} GitHub repositories")

if __name__ == "__main__":
    fetch_github_repos()
