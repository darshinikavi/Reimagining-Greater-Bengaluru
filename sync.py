import os
import subprocess

def run_cmd(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    return result.returncode

def main():
    print("--- Starting Git Sync ---")
    
    # 1. Make sure we ignore large .mp4 files so GitHub doesn't reject the push
    gitignore_path = ".gitignore"
    ignore_entries = ["*.mp4", "*.MP4", "assets/*.mp4", "assets/*.MP4"]
    
    existing_lines = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as f:
            existing_lines = [line.strip() for line in f.readlines()]
            
    with open(gitignore_path, "a") as f:
        for entry in ignore_entries:
            if entry not in existing_lines:
                f.write(f"\n{entry}\n")
                print(f"Added {entry} to .gitignore to prevent large file errors.")

    # 2. Stage all files (respecting the updated .gitignore)
    run_cmd("git add .")
    
    # 3. Commit changes
    commit_msg = "Optimize for mobile devices, update footer and estate image"
    run_cmd(f'git commit -m "{commit_msg}"')
    
    # 4. Push to GitHub
    print("Pushing to GitHub...")
    code = run_cmd("git push origin main")
    
    if code == 0:
        print("\n✅ Successfully synced to GitHub!")
    else:
        print("\n❌ Failed to push to GitHub. See errors above.")

if __name__ == "__main__":
    main()
