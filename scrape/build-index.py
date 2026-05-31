"""Replace the products section in index.html with the full 36-product catalog."""
import json, os

# Read current index.html
with open('E:/www/quartz-sink-website/index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Read generated product HTML
with open('E:/www/quartz-sink-website/scrape/products-html.txt', 'r', encoding='utf-8') as f:
    prod_html = f.read()

# Find the old product grid section
# Old pattern: starts with <div class="product-grid reveal-stagger">
# Ends with: </section> followed by Factory Introduction
old_start = '<div class="product-grid reveal-stagger">'
old_end = '    </div>\n    </div>\n  </section>\n\n  <!-- ========================================\n       Factory Introduction'

start_idx = html.find(old_start)
end_idx = html.find(old_end)

if start_idx == -1:
    print("ERROR: Could not find old_start")
    # Try alternative patterns
    for i, line in enumerate(html.split('\n')):
        if 'product-grid' in line and 'reveal-stagger' in line:
            print(f"  Found at line {i+1}: {line.strip()}")
    exit(1)

if end_idx == -1:
    print("ERROR: Could not find old_end")
    exit(1)

print(f"Found old section from index {start_idx} to {end_idx} (length {end_idx - start_idx})")

# Build new section
new_section = f'''{prod_html}
    </div>
  </section>

  <!-- ========================================
       Factory Introduction'''

# Replace
new_html = html[:start_idx] + new_section + html[end_idx + len(old_end):]

# Also add tab switching JavaScript
tab_js = '''
    // --- Product Category Tabs ---
    document.querySelectorAll('.prod-tab').forEach(tab => {
      tab.addEventListener('click', () => {
        document.querySelectorAll('.prod-tab').forEach(t => t.classList.remove('active'));
        document.querySelectorAll('.product-grid').forEach(g => g.classList.remove('active'));
        tab.classList.add('active');
        const grid = document.getElementById('cat-' + tab.dataset.cat);
        if (grid) grid.classList.add('active');
      });
    });'''

# Insert tab JS before the mobile menu code
js_marker = "    menuBtn.addEventListener('click'"
js_idx = new_html.find(js_marker)
if js_idx != -1:
    new_html = new_html[:js_idx] + tab_js + '\n' + new_html[js_idx:]

# Write
with open('E:/www/quartz-sink-website/index.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"Done. File size: {len(new_html)} bytes")
print(f"Product grids: {new_html.count('product-grid active')} active, {new_html.count('<div class=\"product-grid\"')} total")
print(f"Product cards: {new_html.count('<article class=\"product-card\">')}")
