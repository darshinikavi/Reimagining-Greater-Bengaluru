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
    print("--- Pushing to GitHub ---")
    
    # 1. Ignore massive .mp4 files so push doesn't fail
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

    # 2. Stage changes
    run_cmd("git add .")
    
    # 3. Commit
    commit_msg = "Deploy latest website updates"
    run_cmd(f'git commit -m "{commit_msg}"')
    
    # 4. Push
    code = run_cmd("git push origin main")
    
    if code == 0:
        print("\n[SUCCESS] Successfully pushed to GitHub!")
    else:
        print("\n[ERROR] Failed to push to GitHub. See errors above.")

if __name__ == "__main__":
    main()
