import urllib.request, re, os, json

BASE = 'http://www.nature-sink.com'
SCRAPE_DIR = 'E:/www/quartz-sink-website/scrape'
os.makedirs(SCRAPE_DIR, exist_ok=True)

results = {}
for code in ['05', '06', '07', '08', '09']:
    url = f'{BASE}/products.aspx?code={code}'
    try:
        resp = urllib.request.urlopen(url, timeout=15)
        raw = resp.read()
        try:
            html = raw.decode('gbk')
        except:
            html = raw.decode('gb2312', errors='replace')

        with open(f'{SCRAPE_DIR}/cat-{code}.html', 'w', encoding='utf-8') as f:
            f.write(html)

        all_links = re.findall(r'p_details\.aspx\?code=' + code + r'&id=(\d+)', html)
        ids = sorted(set(all_links), key=lambda x: int(x))

        product_blocks = re.findall(
            r'<a[^>]*href=["\']p_details\.aspx\?code=' + code + r'&id=(\d+)["\'][^>]*>(.*?)</a>',
            html, re.DOTALL
        )

        products = []
        for pid, inner_html in product_blocks:
            name = re.sub(r'<[^>]+>', '', inner_html).strip()
            name = re.sub(r'\s+', ' ', name)
            if name and len(name) > 1:
                products.append({'id': pid, 'name': name})

        results[code] = {
            'product_count': len(ids),
            'ids': ids,
            'products': products,
            'link_count': len(product_blocks)
        }

    except Exception as e:
        results[code] = {'error': str(e)}

with open(f'{SCRAPE_DIR}/category-summary.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print('Done. Check category-summary.json')
