#!/usr/bin/env python3
"""
Script to clone all public repositories from specified GitHub accounts
and organize them as independent folders in the GitDataEng directory on Desktop.
"""

import os
import requests
import subprocess
import json
from pathlib import Path
from typing import List, Dict

class GitHubRepoCloner:
    def __init__(self, target_base_path: str = "~/Desktop/GitDataEng"):
        self.target_base_path = Path(target_base_path).expanduser()
        self.github_api_base = "https://api.github.com"
        
    def get_public_repos(self, username: str) -> List[Dict]:
        """Get all public repositories for a given GitHub username."""
        repos = []
        page = 1
        
        while True:
            url = f"{self.github_api_base}/users/{username}/repos"
            params = {
                'page': page,
                'per_page': 100,
                'type': 'public'
            }
            
            try:
                response = requests.get(url, params=params)
                response.raise_for_status()
                
                page_repos = response.json()
                if not page_repos:
                    break
                    
                repos.extend(page_repos)
                page += 1
                
            except requests.exceptions.RequestException as e:
                print(f"Error fetching repos for {username}: {e}")
                break
                
        return repos
    
    def clone_repository(self, repo_url: str, target_path: Path) -> bool:
        """Clone a repository to the specified target path."""
        try:
            # Create target directory if it doesn't exist
            target_path.mkdir(parents=True, exist_ok=True)
            
            # Clone the repository
            cmd = ["git", "clone", repo_url, str(target_path)]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Successfully cloned to {target_path}")
                
                # Remove .git directory to make it independent
                git_dir = target_path / ".git"
                if git_dir.exists():
                    import shutil
                    shutil.rmtree(git_dir)
                    print(f"   Removed .git directory to make repository independent")
                
                return True
            else:
                print(f"❌ Failed to clone {repo_url}: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Error cloning {repo_url}: {e}")
            return False
    
    def process_account(self, username: str):
        """Process all public repositories for a given account."""
        print(f"\n🔍 Fetching public repositories for {username}...")
        repos = self.get_public_repos(username)
        
        if not repos:
            print(f"No public repositories found for {username}")
            return
            
        print(f"Found {len(repos)} public repositories")
        
        successful_clones = 0
        
        for repo in repos:
            repo_name = repo['name']
            repo_url = repo['clone_url']
            repo_description = repo.get('description', 'No description')
            
            print(f"\n📦 Processing: {repo_name}")
            print(f"   Description: {repo_description}")
            
            # Create repository folder directly in GitDataEng
            repo_path = self.target_base_path / repo_name
            
            if repo_path.exists():
                print(f"   ⚠️  Repository already exists at {repo_path}")
                continue
            
            # Clone the repository
            if self.clone_repository(repo_url, repo_path):
                successful_clones += 1
        
        print(f"\n✅ Successfully cloned {successful_clones}/{len(repos)} repositories for {username}")
    
    def create_readme(self):
        """Create a README file explaining the repository structure."""
        readme_content = """# Consolidated GitHub Repositories

This directory contains independent copies of public repositories from multiple GitHub accounts.

## Structure

All repositories are stored directly in this folder without separation by account.

## Important Notes

- These are independent copies, not forks or linked repositories
- Original .git directories have been removed to ensure independence
- Changes to these copies will not affect the original repositories
- Each repository is completely self-contained

## Usage

To work with any repository:
1. Navigate to the desired repository folder
2. Initialize a new git repository if needed: `git init`
3. Add your remote origin: `git remote add origin <your-new-repo-url>`
4. Make your changes and commit them

## Original Sources

- murilobiss@gmail.com: https://github.com/murilobiss
- mbxagency@gmail.com: https://github.com/mbxagency

Generated on: {datetime}
""".format(datetime=__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        readme_path = self.target_base_path / "README_CONSOLIDATED.md"
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        print(f"\n📝 Created README_CONSOLIDATED.md with repository information")

def main():
    """Main function to clone repositories from specified accounts."""
    print("🚀 Starting GitHub Repository Consolidation")
    print("=" * 50)
    print(f"Target directory: ~/Desktop/GitDataEng/")
    
    # Initialize the cloner with GitDataEng on Desktop
    cloner = GitHubRepoCloner("~/Desktop/GitDataEng")
    
    # Create the base directory first
    cloner.target_base_path.mkdir(parents=True, exist_ok=True)
    
    # Define the accounts to process
    accounts = ["murilobiss", "mbxagency"]
    
    total_repos = 0
    total_successful = 0
    
    for username in accounts:
        print(f"\n{'='*20} Processing {username} {'='*20}")
        cloner.process_account(username)
    
    # Create consolidated README
    cloner.create_readme()
    
    print(f"\n🎉 Repository consolidation completed!")
    print(f"All repositories are now independent copies in ~/Desktop/GitDataEng/ directory.")

if __name__ == "__main__":
    main() 