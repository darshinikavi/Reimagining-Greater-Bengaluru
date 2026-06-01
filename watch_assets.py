import os
import time
import re

TARGET_HTML = 'CK_map_46.html'
ASSETS_DIR = 'assets'

def get_latest_mtime():
    """Returns the latest modification time among all files in the assets directory."""
    latest = 0
    if not os.path.exists(ASSETS_DIR): 
        return latest
    for f in os.listdir(ASSETS_DIR):
        p = os.path.join(ASSETS_DIR, f)
        if os.path.isfile(p):
            m = os.path.getmtime(p)
            if m > latest:
                latest = m
    return latest

def update_html_cache_buster(timestamp):
    """Updates the ?v= parameter in the HTML file to force the browser to load new assets."""
    if not os.path.exists(TARGET_HTML):
        print(f"Error: {TARGET_HTML} not found in this directory.")
        return

    with open(TARGET_HTML, 'r', encoding='utf-8') as f:
        text = f.read()
    
    # Regex to find .kml?v=SOMETHING or .kmz?v=SOMETHING and replace the value with the new timestamp
    # This ensures the browser downloads the fresh file instead of using a cached version
    new_text = re.sub(r'(\.kml|\.kmz)\?v=[a-zA-Z0-9_]+', fr'\1?v={int(timestamp)}', text)
    
    if new_text != text:
        with open(TARGET_HTML, 'w', encoding='utf-8') as f:
            f.write(new_text)
        print(f"[{time.strftime('%H:%M:%S')}] Detected asset changes! Updated {TARGET_HTML} cache-busters to ?v={int(timestamp)}")

if __name__ == '__main__':
    print(f"Starting auto-sync...")
    print(f"Watching the '{ASSETS_DIR}' folder. Keep this script running in the background.")
    print(f"Whenever you replace/save a file in '{ASSETS_DIR}', {TARGET_HTML} will be automatically updated.")
    print("Press Ctrl+C to stop.\n")
    
    last_mtime = get_latest_mtime()
    # Perform an initial sync just in case
    update_html_cache_buster(last_mtime) 
    
    try:
        while True:
            time.sleep(1.5) # Poll every 1.5 seconds
            current_mtime = get_latest_mtime()
            if current_mtime > last_mtime:
                last_mtime = current_mtime
                update_html_cache_buster(last_mtime)
    except KeyboardInterrupt:
        print("\nStopped auto-sync.")
