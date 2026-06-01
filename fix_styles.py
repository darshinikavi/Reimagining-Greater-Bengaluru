import re

with open('CK_map_46.html', 'r', encoding='utf-8') as f:
    text = f.read()

def replacer(match):
    color = match.group(1)
    return f"style:{{ color:'{color}', weight:1.2, opacity:0.9, dashArray:'4 3', fillColor:'{color}', fillOpacity:0.22 }}"

# Replace styles for Ecological (which are polygons)
ecological_regex = r"style:\{\s*color:'#3A0020'.*?fillColor:'(.*?)'.*?\}"
text = re.sub(ecological_regex, replacer, text)

# For point styles:
point_regex = r"pointStyle:\{\s*radius:\d+,.*?fillColor:'(.*?)'.*?\}"
def point_replacer(match):
    color = match.group(1)
    return f"pointStyle:{{ radius:5, fillColor:'{color}', color:'{color}', weight:0, opacity:1, fillOpacity:1 }}"
text = re.sub(point_regex, point_replacer, text)

with open('CK_map_46.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated styles for ecological and points.')
