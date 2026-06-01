import os
import re
import subprocess
import glob

def run_cmd(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode

def update_html_asset_extensions(html_path, assets_dir="assets"):
    """
    Scans the HTML file for references to assets (like data-src="assets/Scene 1.mp4").
    It checks the assets folder to see if the file exists. If a different extension 
    (like .webm) exists for the same base name, it updates the HTML file automatically.
    """
    print(f"Checking {html_path} for updated asset formats...")
    
    if not os.path.exists(html_path):
        print(f"Error: {html_path} not found.")
        return
        
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex to find src="assets/filename.ext" or data-src="assets/filename.ext"
    # Group 1: src or data-src
    # Group 2: assets/
    # Group 3: filename (without extension)
    # Group 4: extension
    pattern = r'(src|data-src)="([^"]*?assets/)([^"/]+)\.([a-zA-Z0-9]+)"'
    
    updated_content = content
    changes_made = 0
    
    def replacer(match):
        nonlocal changes_made
        attr = match.group(1)
        path_prefix = match.group(2)
        base_name = match.group(3)
        old_ext = match.group(4)
        
        # Look for any file in assets matching the base name
        search_pattern = os.path.join(assets_dir, f"{base_name}.*")
        matches = glob.glob(search_pattern)
        
        if matches:
            # Grab the first match's extension
            actual_filename = os.path.basename(matches[0])
            actual_base, actual_ext = os.path.splitext(actual_filename)
            actual_ext = actual_ext.lstrip('.') # remove the dot
            
            if old_ext.lower() != actual_ext.lower():
                print(f"  -> Detected format change: {base_name}.{old_ext} is now {base_name}.{actual_ext}")
                changes_made += 1
                return f'{attr}="{path_prefix}{base_name}.{actual_ext}"'
                
        return match.group(0) # No change

    updated_content = re.sub(pattern, replacer, content)
    
    if changes_made > 0:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"Successfully updated {changes_made} asset references in {html_path}.")
    else:
        print("No format updates were necessary.")


def main():
    print("--- Starting Git Sync ---")
    
    # 1. Automatically fix any updated asset extensions in HTML
    update_html_asset_extensions("index 24.html")
    
    # 2. Make sure we ignore large .mp4 files so GitHub doesn't reject the push
    # Note: .webm files are generally smaller so we don't ignore them by default, 
    # but be careful if they exceed 100MB!
    gitignore_path = ".gitignore"
    ignore_entries = ["*.mp4", "*.MP4", "assets/*.mp4", "assets/*.MP4"]
    
    existing_lines = []
    if os.path.exists(gitignore_path):
        try:
            with open(gitignore_path, "r", encoding="utf-8") as f:
                existing_lines = [line.strip() for line in f.readlines()]
        except UnicodeDecodeError:
            with open(gitignore_path, "r", encoding="utf-16") as f:
                existing_lines = [line.strip() for line in f.readlines()]
            
    try:
        with open(gitignore_path, "a", encoding="utf-8") as f:
            for entry in ignore_entries:
                if entry not in existing_lines:
                    f.write(f"\n{entry}\n")
                    print(f"Added {entry} to .gitignore to prevent large file errors.")
    except UnicodeDecodeError:
        pass

    # 3. Stage all files (respecting the updated .gitignore)
    run_cmd("git add .")
    
    # 4. Commit changes
    commit_msg = "Auto-sync: update asset formats and deploy"
    run_cmd(f'git commit -m "{commit_msg}"')
    
    # 5. Push to GitHub
    print("Pushing to GitHub...")
    code = run_cmd("git push origin main")
    
    if code == 0:
        # Changed emoji to a standard ascii symbol to prevent Windows cp1252 encode errors
        print("\n[SUCCESS] Successfully synced to GitHub!")
    else:
        print("\n[ERROR] Failed to push to GitHub. See errors above.")

if __name__ == "__main__":
    main()
