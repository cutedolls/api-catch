import requests
import json

PYPI_PACKAGES = [
    'smartpasslib', 'clipassman', 'clipassgen', 'smart-tsp-solver', 
    'smart-tsp-benchmark', 'smart-2fa-secure', 'babylonian-image-library',
    'smart-babylon-library', 'commandman', 'smartpathlibrary', 
    'smartexecutorlib', 'climan', 'github-ssh-key', 'commandpack',
    'smartprinter', 'smartcliapp', 'commandex', 'smartrandom',
    'smarttextdecorator', 'smartauthen', 'smart-redis-storage',
    'smart-text-randomizer', 'smart-ip-info'
]

def fetch_pypi_package(package_name):
    try:
        response = requests.get(f"https://pypi.org/pypi/{package_name}/json", timeout=10)
        
        if response.status_code == 404:
            return {
                'name': package_name,
                'version': '0.0.0',
                'summary': 'Package not found',
                'is_valid': False,
                'not_found': True,
                'project_url': f'https://pypi.org/project/{package_name}/'
            }
        
        response.raise_for_status()
        data = response.json()
        info = data['info']
        
        return {
            'name': info['name'],
            'version': info.get('version', '0.0.0'),
            'summary': info.get('summary', 'No summary'),
            'description': info.get('description', ''),
            'license': info.get('license', 'Not specified'),
            'home_page': info.get('home_page', ''),
            'project_url': info.get('project_url', f'https://pypi.org/project/{info["name"]}/'),
            'is_valid': True
        }
        
    except Exception as e:
        return {
            'name': package_name,
            'version': '0.0.0',
            'summary': f'Error: {str(e)}',
            'is_valid': False,
            'error': True,
            'project_url': f'https://pypi.org/project/{package_name}/'
        }

def fetch_all_packages():
    print("📦 Fetching PyPI packages...")
    
    packages = []
    for package_name in PYPI_PACKAGES:
        package_data = fetch_pypi_package(package_name)
        packages.append(package_data)
    
    # Сортируем: валидные первые
    sorted_packages = sorted(packages, key=lambda x: (not x.get('is_valid', False), x['name']))
    
    with open('pypi_packages.json', 'w', encoding='utf-8') as f:
        json.dump(sorted_packages, f, indent=2, ensure_ascii=False)
    
    valid_count = sum(1 for pkg in packages if pkg.get('is_valid'))
    print(f"✅ Fetched {valid_count} valid PyPI packages out of {len(packages)}")

if __name__ == "__main__":
    fetch_all_packages()
