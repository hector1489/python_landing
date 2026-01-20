import json
from jinja2 import Template

def build_site():
    try:
        with open("config.json", "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: 'config.json' file not found")
        return

    try:
        with open("template.html", "r", encoding="utf-8") as f:
            template_str = f.read()
    except FileNotFoundError:
        print("Error: 'template.html' file not found")
        return

    template = Template(template_str)
    output_html = template.render(data)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(output_html)
    
    print("Success! Your store has been generated in 'index.html' using config.json")

if __name__ == "__main__":
    build_site()