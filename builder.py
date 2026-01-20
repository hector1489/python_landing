import json
from jinja2 import Template

# 1. Datos de ejemplo (Esto podría venir de un archivo config.json)
data = {
    "store_name": "Mi Tienda de Software",
    "description": "Herramientas premium desarrolladas en Python para automatización.",
    "products": [
        {
            "name": "Bot de Trading Pro",
            "price": "49.99",
            "image": "https://via.placeholder.com/300x200",
            "short_desc": "Automatiza tus operaciones con precisión de milisegundos.",
            "link": "https://payhip.com/tu-producto-1"
        },
        {
            "name": "Dashboard IoT",
            "price": "29.00",
            "image": "https://via.placeholder.com/300x200",
            "short_desc": "Controla tus dispositivos industriales desde la web.",
            "link": "https://payhip.com/tu-producto-2"
        }
    ]
}

def build_site():
    # Cargar el template HTML
    with open("template.html", "r", encoding="utf-8") as f:
        template_str = f.read()

    # Renderizar con Jinja2
    template = Template(template_str)
    output_html = template.render(data)

    # Guardar el resultado final
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(output_html)
    
    print("¡Éxito! Tu tienda ha sido generada en 'index.html'")

if __name__ == "__main__":
    build_site()