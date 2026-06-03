import os
import re
import glob
import subprocess

def run_cmd(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode

def update_html_asset_extensions(html_path="index.html", assets_dir="assets"):
    """
    Scans the HTML file for references to assets (like src="assets/Scene 1.mp4").
    If the file in the assets folder has a different extension (like .webm),
    it updates the HTML automatically to match.
    """
    print(f"--- 1. Checking {html_path} for updated asset formats ---")
    
    if not os.path.exists(html_path):
        print(f"Error: {html_path} not found.")
        return
        
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex to find src="assets/filename.ext" or data-src="assets/filename.ext"
    pattern = r'(src|data-src)="([^"]*?assets/)([^"/]+)\.([a-zA-Z0-9]+)"'
    changes_made = 0
    
    def replacer(match):
        nonlocal changes_made
        attr = match.group(1)
        path_prefix = match.group(2)
        base_name = match.group(3)
        old_ext = match.group(4)
        
        search_pattern = os.path.join(assets_dir, f"{base_name}.*")
        matches = glob.glob(search_pattern)
        
        if matches:
            actual_filename = os.path.basename(matches[0])
            actual_base, actual_ext = os.path.splitext(actual_filename)
            actual_ext = actual_ext.lstrip('.')
            
            if old_ext.lower() != actual_ext.lower():
                print(f"  -> Detected format change: {base_name}.{old_ext} is now {base_name}.{actual_ext}")
                changes_made += 1
                return f'{attr}="{path_prefix}{base_name}.{actual_ext}"'
                
        return match.group(0)

    updated_content = re.sub(pattern, replacer, content)
    
    if changes_made > 0:
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(updated_content)
        print(f"Successfully updated {changes_made} asset references in {html_path}.")
    else:
        print("All asset links in the HTML already match the actual files in the folder.")

def main():
    # 1. Update HTML assets
    update_html_asset_extensions("index.html")
    
    print("\n--- 2. Pushing to GitHub ---")
    
    # 2. Ignore massive .mp4 files so push doesn't fail
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
    except UnicodeDecodeError:
        pass

    # 3. Stage changes
    run_cmd("git add .")
    
    # 4. Commit
    commit_msg = "Auto-sync: Detect asset updates and push to Git"
    run_cmd(f'git commit -m "{commit_msg}"')
    
    # 5. Push
    code = run_cmd("git push origin main")
    
    if code == 0:
        print("\n[SUCCESS] Successfully pushed to GitHub!")
    else:
        print("\n[ERROR] Failed to push to GitHub. See errors above.")

if __name__ == "__main__":
    main()
