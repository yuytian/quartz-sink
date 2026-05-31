import json, os

# Load data
with open('E:/www/quartz-sink-website/scrape/category-summary.json', 'r', encoding='utf-8') as f:
    categories = json.load(f)

with open('E:/www/quartz-sink-website/scrape/product-images.json', 'r', encoding='utf-8') as f:
    prod_images = json.load(f)

# Category labels and descriptions
cat_info = {
    '05': {'label': '浴室柜盆', 'desc': '石英石一体盆/台下盆/台上盆系列，多款造型满足各类浴室柜搭配需求'},
    '06': {'label': '厨房水槽', 'desc': '高硬度石英石材质，耐刮擦抗冲击，单槽/双槽多款设计'},
    '07': {'label': '洗衣槽', 'desc': '大容量深槽设计，坚固耐用，适合阳台洗衣房等场景'},
}

html_lines = []
html_lines.append('      <div class="prod-tabs reveal">')
first = True
for code in ['05', '06', '07']:
    active = ' active' if first else ''
    info = cat_info[code]
    html_lines.append(f'        <button class="prod-tab{active}" data-cat="{code}">{info["label"]}</button>')
    first = False
html_lines.append('      </div>')

for code in ['05', '06', '07']:
    info = cat_info[code]
    cat_data = categories[code]
    active = ' active' if code == '05' else ''
    html_lines.append(f'')
    html_lines.append(f'      <!-- Category {code}: {info["label"]} ({len(cat_data["products"])} products) -->')
    html_lines.append(f'      <div class="product-grid{active}" id="cat-{code}">')

    for prod in cat_data['products']:
        pid = prod['id']
        model = prod['name']
        key = f'{code}_{pid}'

        # Get the first image for this product
        img_src = ''
        if key in prod_images and prod_images[key]:
            img_url = prod_images[key][0]
            img_filename = img_url.split('/')[-1]
            img_src = f'images/products/{img_filename}'

        if img_src:
            html_lines.append(f'        <article class="product-card">')
            html_lines.append(f'          <div class="product-card-image">')
            html_lines.append(f'            <img src="{img_src}" alt="{model}" loading="lazy" width="400" height="300">')
            html_lines.append(f'          </div>')
            html_lines.append(f'          <div class="product-card-body">')
            html_lines.append(f'            <p class="product-card-model">{model}</p>')
            html_lines.append(f'          </div>')
            html_lines.append(f'        </article>')

    html_lines.append(f'      </div>')

output = '\n'.join(html_lines)
with open('E:/www/quartz-sink-website/scrape/products-html.txt', 'w', encoding='utf-8') as f:
    f.write(output)

print(f'Generated HTML with {sum(len(categories[c]["products"]) for c in ["05","06","07"])} products')
print('Saved to scrape/products-html.txt')
