import os
import re
import glob

def update_html_asset_extensions(html_path="index.html", assets_dir="assets"):
    """
    Scans the HTML file for references to assets (like src="assets/Scene 1.mp4").
    If the file in the assets folder has a different extension (like .webm),
    it updates the HTML automatically to match.
    """
    print(f"Checking {html_path} for updated asset formats...")
    
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
        print("All asset links in the HTML match the actual files in the folder. No updates necessary.")

if __name__ == "__main__":
    # Note: Using index.html since we renamed index 24.html
    update_html_asset_extensions("index.html")
