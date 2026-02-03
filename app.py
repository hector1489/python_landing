from flask import Flask, render_template, request, send_file
import json
import os
from datetime import datetime
from jinja2 import Template

app = Flask(__name__)

CONFIG_FILE = "config.json"
TEMPLATE_FILE = "template.html"
BUILDS_DIR = "builds"

if not os.path.exists(BUILDS_DIR):
    os.makedirs(BUILDS_DIR)

def load_config():
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_builds():
    """Returns a list of generated files with their info."""
    files = []
    for filename in os.listdir(BUILDS_DIR):
        if filename.endswith(".html"):
            path = os.path.join(BUILDS_DIR, filename)
            stats = os.stat(path)
            files.append({
                "name": filename,
                "date": datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M'),
                "size": f"{round(stats.st_size / 1024, 2)} KB"
            })
    return sorted(files, key=lambda x: x['date'], reverse=True)

@app.route('/')
def index():
    config_data = load_config()
    builds = get_builds()
    return render_template('admin.html', config=config_data, builds=builds)

@app.route('/generate', methods=['POST'])
def generate():
    store_name = request.form.get('store_name')
    description = request.form.get('description')
    
    names = request.form.getlist('p_name[]')
    prices = request.form.getlist('p_price[]')
    images = request.form.getlist('p_image[]')
    links = request.form.getlist('p_link[]')
    descs = request.form.getlist('p_desc[]')
    
    products = [{"name": n, "price": p, "image": i, "short_desc": d, "link": l} 
                for n, p, i, d, l in zip(names, prices, images, descs, links)]
    
    new_config = {"store_name": store_name, "description": description, "products": products}

    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template = Template(f.read())
    output_html = template.render(new_config)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    clean_name = "".join(x for x in store_name if x.isalnum())
    filename = f"{clean_name}_{timestamp}.html"
    filepath = os.path.join(BUILDS_DIR, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(output_html)

    return send_file(filepath, as_attachment=True, download_name="index.html")

@app.route('/download/<filename>')
def download_build(filename):
    return send_file(os.path.join(BUILDS_DIR, filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)