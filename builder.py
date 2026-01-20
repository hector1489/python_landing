import json
from jinja2 import Template

def build_site():
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: No se encontró 'config.json'")
        return

    try:
        with open("template.html", "r", encoding="utf-8") as f:
            template_str = f.read()
    except FileNotFoundError:
        print("Error: No se encontró 'template.html'")
        return

    template = Template(template_str)
    output_html = template.render(data)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(output_html)
    
    print("¡Éxito! Tu tienda ha sido generada en 'index.html' usando config.json")

if __name__ == "__main__":
    build_site()