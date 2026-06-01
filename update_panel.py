import re
import codecs

with open('assets/goodearth-hejjala-map.html', 'r', encoding='utf-8') as f:
    hejjala = f.read()

# Extract CSS
css_match = re.search(r'/\* ── HAMBURGER BUTTON ── \*/(.*?)/* ── BASEMAP SWITCHER ── \*/', hejjala, re.DOTALL)
if not css_match:
    print("CSS not found")
    exit(1)

css_block = '/* ── HAMBURGER BUTTON ── */\n' + css_match.group(1).strip() + '\n\n    /* Base map trigger */'

with open('CK_map_46.html', 'r', encoding='utf-8') as f:
    ck = f.read()

# Replace CSS
ck = re.sub(r'#panel-trigger \{.*?(?=/\* Base map trigger \*/)', css_block + '\n    ', ck, flags=re.DOTALL)

# Replace HTML
html_new = '''<!-- HAMBURGER BUTTON -->
    <button id="panel-toggle" class="open" onclick="togglePanel()" title="Toggle Layers">
      <div class="ham-icon">
        <div class="ham-bar"></div>
        <div class="ham-bar"></div>
        <div class="ham-bar"></div>
      </div>
    </button>

    <!-- LAYER PANEL -->
    <div id="layer-panel">
      <div class="panel-head">
        <span class="panel-title">Site Layers</span>
        <div class="panel-btns">
          <button class="btn-all" onclick="toggleAll(false)">Hide All</button>
          <button class="btn-all" onclick="toggleAll(true)">Show All</button>
        </div>
      </div>
      <div class="panel-scroll" id="layer-list"></div>
    </div>'''

ck = re.sub(r'<!-- Layer toggle -->.*?<div id="layer-list"></div>\n    </div>', html_new, ck, flags=re.DOTALL)

# Replace JS buildLayerList
js_new = '''function buildLayerList() {
    const listEl = document.getElementById('layer-list');
    listEl.innerHTML = '';
    
    GROUPS.forEach(group => {
      const defs = group.layers.map(id => getLayerDef(id)).filter(Boolean);
      if (!defs.length) return;
      
      const hdr = document.createElement('div');
      hdr.className = 'cat-header';
      const lbl = document.createElement('span');
      lbl.className = 'cat-label'; lbl.textContent = group.label;
      const arrow = document.createElement('span');
      arrow.className = 'cat-arrow open'; arrow.textContent = '▾';
      hdr.append(lbl, arrow);
      
      const rowsEl = document.createElement('div');
      rowsEl.className = 'cat-rows';
      
      defs.forEach(def => {
        const row = document.createElement('div');
        row.className = 'layer-row';
        row.id = 'row-' + def.id;
        
        const sw = document.createElement('div');
        sw.className = 'swatch'; sw.style.background = def.colour;
        
        const lb = document.createElement('span');
        lb.className = 'layer-lbl'; lb.textContent = def.label;
        
        const pill = document.createElement('label');
        pill.className = 'pill';
        const inp = document.createElement('input');
        inp.type = 'checkbox';
        inp.checked = true;
        inp.id = 'tog-' + def.id;
        inp.addEventListener('change', () => toggleLayer(def.id));
        const track = document.createElement('span');
        track.className = 'pill-track';
        pill.append(inp, track);
        
        row.append(sw, lb, pill);
        rowsEl.appendChild(row);
      });
      
      let open = true;
      hdr.addEventListener('click', () => {
        open = !open;
        arrow.classList.toggle('open', open);
        rowsEl.style.maxHeight = open ? rowsEl.scrollHeight + 'px' : '0px';
      });
      
      listEl.appendChild(hdr);
      listEl.appendChild(rowsEl);
      
      requestAnimationFrame(() => { rowsEl.style.maxHeight = rowsEl.scrollHeight + 'px'; });
    });
  }

  function toggleLayer(id) {
    const def = getLayerDef(id);
    if (!def || !def.group) return;
    const inp = document.getElementById('tog-' + id);
    if (!inp.checked) map.removeLayer(def.group);
    else def.group.addTo(map);
  }

  function toggleAll(show) {
    allVisible = show;
    LAYER_DEFS.forEach(def => {
      if (!def.group) return;
      if (allVisible) def.group.addTo(map);
      else map.removeLayer(def.group);
      
      const inp = document.getElementById('tog-' + def.id);
      if (inp) inp.checked = allVisible;
    });
  }

  function togglePanel() {
    panelOpen = !panelOpen;
    document.getElementById('layer-panel').classList.toggle('hidden', !panelOpen);
    document.getElementById('panel-toggle').classList.toggle('open', panelOpen);
  }'''

ck = re.sub(r'function buildLayerList\(\) \{.*?function togglePanel\(\) \{.*?\}', js_new, ck, flags=re.DOTALL)

with open('CK_map_46.html', 'w', encoding='utf-8') as f:
    f.write(ck)

print("Success")
