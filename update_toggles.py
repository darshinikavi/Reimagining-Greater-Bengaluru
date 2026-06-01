import re

with open('CK_map_46.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Default closed panel
text = text.replace('<button id="panel-toggle" class="open" onclick="togglePanel()" title="Toggle Layers">',
                    '<button id="panel-toggle" class="" onclick="togglePanel()" title="Toggle Layers">')
text = text.replace('<div id="layer-panel">', '<div id="layer-panel" class="hidden">')
text = text.replace('let panelOpen   = true;', 'let panelOpen   = false;')

# 2. Add category toggle
old_hdr = '''      const hdr = document.createElement('div');
      hdr.className = 'cat-header';
      const lbl = document.createElement('span');
      lbl.className = 'cat-label'; lbl.textContent = group.label;
      const arrow = document.createElement('span');
      arrow.className = 'cat-arrow open'; arrow.textContent = '▾';
      hdr.append(lbl, arrow);'''

new_hdr = '''      const hdr = document.createElement('div');
      hdr.className = 'cat-header';
      
      const hdrLeft = document.createElement('div');
      hdrLeft.style.display = 'flex'; hdrLeft.style.alignItems = 'center'; hdrLeft.style.gap = '8px';
      
      const pill = document.createElement('label');
      pill.className = 'pill';
      pill.addEventListener('click', (e) => e.stopPropagation());
      const inp = document.createElement('input');
      inp.type = 'checkbox';
      inp.checked = true;
      inp.addEventListener('change', (e) => {
        const isChecked = e.target.checked;
        defs.forEach(def => {
          const childInp = document.getElementById('tog-' + def.id);
          if (childInp && childInp.checked !== isChecked) {
            childInp.checked = isChecked;
            toggleLayer(def.id);
          }
        });
      });
      const track = document.createElement('span');
      track.className = 'pill-track';
      pill.append(inp, track);
      
      const lbl = document.createElement('span');
      lbl.className = 'cat-label'; lbl.textContent = group.label;
      
      hdrLeft.append(pill, lbl);
      
      const arrow = document.createElement('span');
      arrow.className = 'cat-arrow open'; arrow.textContent = '▾';
      hdr.append(hdrLeft, arrow);'''

if old_hdr in text:
    text = text.replace(old_hdr, new_hdr)
else:
    print('Could not find old header code!')
    exit(1)

with open('CK_map_46.html', 'w', encoding='utf-8') as f:
    f.write(text)
print('Done!')
