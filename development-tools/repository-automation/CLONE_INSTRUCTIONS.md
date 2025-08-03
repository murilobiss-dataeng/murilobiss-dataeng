# GitHub Repository Consolidation Instructions

This script will clone all public repositories from the specified GitHub accounts and create independent copies in the GitDataEng directory.

## What This Script Does

1. **Fetches all public repositories** from:
   - `murilobiss` (linked to murilobiss@gmail.com)
   - `mbxagencycwb` (linked to mbxagencycwb@gmail.com)

2. **Creates independent copies** by:
   - Cloning each repository
   - Removing the `.git` directory to break all connections
   - Organizing them in separate folders

3. **Organizes the structure** as:
   ```
   GitDataEng/
   ├── murilobiss/
   │   ├── repo1/
   │   ├── repo2/
   │   └── ...
   ├── mbxagencycwb/
   │   ├── repo1/
   │   ├── repo2/
   │   └── ...
   └── README_CONSOLIDATED.md
   ```

## Prerequisites

- Python 3.6 or higher
- Git installed
- Internet connection

## How to Run

### Option 1: Using the shell script (Recommended)
```bash
./run_clone.sh
```

### Option 2: Manual execution
```bash
# Install dependencies
pip3 install -r requirements.txt

# Run the script
python3 clone_repositories.py
```

## What Happens After Cloning

1. **Independent Copies**: Each repository is completely independent
2. **No Git History**: Original git history is removed
3. **Ready to Use**: You can start working on any repository immediately
4. **Documentation**: A README_CONSOLIDATED.md file is created with details

## Working with Cloned Repositories

To start working with any cloned repository:

1. **Navigate to the repository folder**:
   ```bash
   cd GitDataEng/murilobiss/repository-name
   ```

2. **Initialize a new git repository** (optional):
   ```bash
   git init
   ```

3. **Add your remote origin** (if you want to push to your account):
   ```bash
   git remote add origin https://github.com/murilobiss.dataeng/repository-name.git
   ```

4. **Start making changes and commit them**:
   ```bash
   git add .
   git commit -m "Initial commit"
   git push -u origin main
   ```

## Important Notes

- ✅ **Completely Independent**: Changes won't affect original repositories
- ✅ **No Dependencies**: Each copy is self-contained
- ✅ **Safe to Delete**: You can delete any repository without affecting others
- ✅ **Ready for Development**: All code is immediately available for work
- ✅ **Organized in GitDataEng**: All repositories are consolidated in the GitDataEng folder

## Troubleshooting

### Rate Limiting
If you encounter GitHub API rate limiting, the script will show an error. This is normal for public API usage. The script will continue with repositories it can access.

### Network Issues
If cloning fails for some repositories, the script will continue with the others. You can re-run the script to get missing repositories.

### Permission Issues
Make sure you have write permissions in the current directory to create the GitDataEng folder.

## Customization

To modify the script for different accounts:

1. Edit `clone_repositories.py`
2. Change the `accounts` list in the `main()` function:
   ```python
   accounts = [
       ("new-username", "new-folder-name"),
       ("another-username", "another-folder-name")
   ]
   ```

To change the target directory, modify the `GitHubRepoCloner("GitDataEng")` line in the `main()` function.

## Support

If you encounter any issues, check:
1. Python and Git are properly installed
2. You have internet connection
3. The GitHub usernames are correct
4. You have sufficient disk space
5. You have write permissions to create the GitDataEng directory 