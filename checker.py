import os
import re
import requests
from playwright.sync_api import sync_playwright

DEFAULT_TARGET_PRICE = 450000

PRODUCTS = [
    # =========================
    # PS5 - avisa a $450.000 o menos
    # =========================
    {
        "name": "PS5 Paris - Slim Digital",
        "url": "https://www.paris.cl/consola-sony-ps5-playstation-5-slim-edicion-digital-MK208523YL.html",
        "target_price": 450000,
        "min_price": 300000,
        "max_price": 1000000,
        "alert_title": "🚨 PS5 EN OFERTA",
    },
    {
        "name": "PS5 Entel - Digital",
        "url": "https://miportal.entel.cl/personas/catalogo/prod2580055?omc=c_shopping&utm_id=",
        "target_price": 450000,
        "min_price": 300000,
        "max_price": 1000000,
        "alert_title": "🚨 PS5 EN OFERTA",
    },
    {
        "name": "PS5 Lider - Digital Astro Bot y GT7",
        "url": "https://www.lider.cl/ip/videojuegos/consola-ps5-digital-astro-bot-y-gt7/00071171902355?channable=42320f69640030303037313137313930323335355b&",
        "target_price": 450000,
        "min_price": 300000,
        "max_price": 1000000,
        "alert_title": "🚨 PS5 EN OFERTA",
    },
    {
        "name": "PS5 Ripley - Digital Astro Bot y GT7",
        "url": "https://simple.ripley.cl/paquete-de-consola-playstation-5-edicion-digital-con-astro-bot-y-gran-turismo-7-mpm10003300046",
        "target_price": 450000,
        "min_price": 300000,
        "max_price": 1000000,
        "alert_title": "🚨 PS5 EN OFERTA",
    },
    {
        "name": "PS5 PC Factory - Digital Slim Version US",
        "url": "https://www.pcfactory.cl/producto/54253-sony-consola-playstation-5-digital-slim-version-us",
        "target_price": 450000,
        "min_price": 300000,
        "max_price": 1000000,
        "alert_title": "🚨 PS5 EN OFERTA",
    },
    {
        "name": "PS5 Paris - Digital con soporte vertical",
        "url": "https://www.paris.cl/consola-sony-playstation-5-slim-edicion-digital-soporte-vertical-adicional-para-ps5-MKFJLGELDR.html",
        "target_price": 450000,
        "min_price": 300000,
        "max_price": 1000000,
        "alert_title": "🚨 PS5 EN OFERTA",
    },
    {
        "name": "PS5 Falabella - Slim Digital",
        "url": "https://www.falabella.com/falabella-cl/product/126614389/Consola-Sony-PS5-PlayStation-5-Slim-(Edicion-Digital)/126614390?kid=shopp198fc",
        "target_price": 450000,
        "min_price": 300000,
        "max_price": 1000000,
        "alert_title": "🚨 PS5 EN OFERTA",
    },
    {
        "name": "PS5 Entel - Producto 2620074",
        "url": "https://miportal.entel.cl/personas/catalogo/prod2620074?omc=c_shopping&utm_id=",
        "target_price": 450000,
        "min_price": 300000,
        "max_price": 1000000,
        "alert_title": "🚨 PS5 EN OFERTA",
    },
    {
        "name": "PS5 Paris - Digital con DualSense adicional",
        "url": "https://www.paris.cl/consola-sony-playstation-5-slim-edicion-digital-control-dualsense-adicional-MKNO07O202.html",
        "target_price": 450000,
        "min_price": 300000,
        "max_price": 1000000,
        "alert_title": "🚨 PS5 EN OFERTA",
    },
    {
        "name": "PS5 ABC - Standard Slim 1TB Astro Bot y GT7",
        "url": "https://www.abc.cl/consola-sony-playstation-ps5-standard-slim-1-tb-ssd-1-control-2-juegos-fisicos-astro-bot-y-gran-turismo-7/28956762.html",
        "target_price": 450000,
        "min_price": 300000,
        "max_price": 1000000,
        "alert_title": "🚨 PS5 EN OFERTA",
    },
    {
        "name": "PS5 Lider - Standard Astro Bot y GT7",
        "url": "https://www.lider.cl/ip/videojuegos/consola-ps5-standard-astro-bot-y-gt7/00071171902395?channable=42320f69640030303037313137313930323339355d&",
        "target_price": 450000,
        "min_price": 300000,
        "max_price": 1000000,
        "alert_title": "🚨 PS5 EN OFERTA",
    },
    {
        "name": "PS5 Falabella - Standard GT7 Sony",
        "url": "https://www.falabella.com/falabella-cl/product/80648267/Consola-PS5-HW-Standard-GT7-Sony/80648267?kid=shopp198fc",
        "target_price": 450000,
        "min_price": 300000,
        "max_price": 1000000,
        "alert_title": "🚨 PS5 EN OFERTA",
    },
    {
        "name": "PS5 Ripley - Standard Astro Bot y GT7",
        "url": "https://simple.ripley.cl/playstation-5-con-astrobot-y-gran-turismo-7-2000408087922p?color_80=Blanco",
        "target_price": 450000,
        "min_price": 300000,
        "max_price": 1000000,
        "alert_title": "🚨 PS5 EN OFERTA",
    },
    {
        "name": "PS5 Entel - Producto 2680050",
        "url": "https://miportal.entel.cl/personas/catalogo/prod2680050?omc=c_shopping&utm_id=",
        "target_price": 450000,
        "min_price": 300000,
        "max_price": 1000000,
        "alert_title": "🚨 PS5 EN OFERTA",
    },
    {
        "name": "PS5 Falabella - Digital con DualSense Midnight Black",
        "url": "https://www.falabella.com/falabella-cl/product/148993549/Consola-Sony-Playstation-5-Slim-Edicion-Digital-+-Control-Dualsense-Adicional-Midnight-Black/148993551?kid=shopp198fc",
        "target_price": 450000,
        "min_price": 300000,
        "max_price": 1000000,
        "alert_title": "🚨 PS5 EN OFERTA",
    },

    # =========================
    # Nintendo Switch 2 - avisa a $400.000 o menos
    # =========================
    {
        "name": "Nintendo Switch 2 Falabella - Consola",
        "url": "https://www.falabella.com/falabella-cl/product/17448346/HW-SWITCH-2-SYSTEM-LT2-SOLUS/17448346?kid=shopp1141fm",
        "target_price": 400000,
        "min_price": 250000,
        "max_price": 800000,
        "alert_title": "🚨 SWITCH 2 EN OFERTA",
    },
    {
        "name": "Nintendo Switch 2 Ripley - Consola",
        "url": "https://simple.ripley.cl/consola-nintendo-switch-2-2000406245874p?color_80=Negro",
        "target_price": 400000,
        "min_price": 250000,
        "max_price": 800000,
        "alert_title": "🚨 SWITCH 2 EN OFERTA",
    },
    {
        "name": "Nintendo Switch 2 Entel - Producto 2550046",
        "url": "https://miportal.entel.cl/personas/catalogo/prod2550046?omc=c_shopping&utm_id=",
        "target_price": 400000,
        "min_price": 250000,
        "max_price": 800000,
        "alert_title": "🚨 SWITCH 2 EN OFERTA",
    },
    {
        "name": "Nintendo Switch 2 Paris - Consola",
        "url": "https://www.paris.cl/consola-nintendo-switch-2-MKLL6XJZ1F.html",
        "target_price": 400000,
        "min_price": 250000,
        "max_price": 800000,
        "alert_title": "🚨 SWITCH 2 EN OFERTA",
    },
    {
        "name": "Nintendo Switch 2 Falabella - Bundle Mario Kart World",
        "url": "https://www.falabella.com/falabella-cl/product/17524937/Consola-Nintendo-Hw-Switch2-Bun-Mkwlt2/17524937?kid=shopp1141fm",
        "target_price": 400000,
        "min_price": 250000,
        "max_price": 800000,
        "alert_title": "🚨 SWITCH 2 EN OFERTA",
    },
    {
        "name": "Nintendo Switch 2 Entel - Producto 2550047",
        "url": "https://miportal.entel.cl/personas/catalogo/prod2550047?omc=c_shopping&utm_id=",
        "target_price": 400000,
        "min_price": 250000,
        "max_price": 800000,
        "alert_title": "🚨 SWITCH 2 EN OFERTA",
    },
    {
        "name": "Nintendo Switch 2 Ripley - Mario Kart World",
        "url": "https://simple.ripley.cl/consola-nintendo-switch-2-juego-mario-kart-world-2000406245867p?color_80=Negro",
        "target_price": 400000,
        "min_price": 250000,
        "max_price": 800000,
        "alert_title": "🚨 SWITCH 2 EN OFERTA",
    },
    {
        "name": "Nintendo Switch 2 Ripley - Mario Kart World Marketplace",
        "url": "https://simple.ripley.cl/nintendo-switch-2-mario-kart-world-mpm10002910645?color_80=Gris",
        "target_price": 400000,
        "min_price": 250000,
        "max_price": 800000,
        "alert_title": "🚨 SWITCH 2 EN OFERTA",
    },
]


def format_clp(price: int) -> str:
    return f"${price:,}".replace(",", ".")


def parse_price(text: str, min_price: int, max_price: int):
    """
    Busca precios chilenos tipo $549.990.
    Filtra cuotas, garantías, despacho, puntos, CMR, seguros, etc.
    """
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    prices = []

    bad_words = [
        "cuotas",
        "cuota",
        "garantía",
        "garantia",
        "despacho",
        "retiro",
        "envío",
        "envio",
        "cmr",
        "tarjeta",
        "puntos",
        "punto",
        "giftcard",
        "gift card",
        "seguro",
        "protección",
        "proteccion",
        "servicio técnico",
        "servicio tecnico",
        "garantía extendida",
        "garantia extendida",
    ]

    for i, line in enumerate(lines):
        matches = re.findall(r"\$?\s?(\d{1,3}(?:\.\d{3})+)", line)

        for match in matches:
            price = int(match.replace(".", ""))

            if min_price <= price <= max_price:
                context = " ".join(lines[max(0, i - 3): i + 4]).lower()

                if any(word in context for word in bad_words):
                    continue

                prices.append(price)

    if not prices:
        return None

    unique_prices = sorted(set(prices))

    return unique_prices[0]

def get_page_text_with_playwright(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        )

        page = browser.new_page(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        )

        # No usamos networkidle porque Falabella/Ripley/Paris a veces nunca terminan de cargar.
        page.goto(url, wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(8000)

        text = page.inner_text("body", timeout=30000)
        browser.close()
        return text

def send_telegram(message: str):
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    api_url = f"https://api.telegram.org/bot{token}/sendMessage"

    response = requests.post(
        api_url,
        json={
            "chat_id": chat_id,
            "text": message,
            "disable_web_page_preview": False,
        },
        timeout=30,
    )

    response.raise_for_status()


def main():
    results = []

    for product in PRODUCTS:
        name = product["name"]
        url = product["url"]

        target_price = product.get("target_price", DEFAULT_TARGET_PRICE)
        min_price = product.get("min_price", 300000)
        max_price = product.get("max_price", 1000000)
        alert_title = product.get("alert_title", "🚨 OFERTA DETECTADA")

        try:
            text = get_page_text_with_playwright(url)
            price = parse_price(text, min_price, max_price)

            if price is None:
                results.append(f"⚠️ No pude leer precio: {name}\n{url}")
                continue

            print(f"{name}: precio detectado {format_clp(price)}")

            if price <= target_price:
                message = (
                    f"{alert_title}\n\n"
                    f"{name}\n"
                    f"Precio detectado: {format_clp(price)}\n"
                    f"Objetivo: {format_clp(target_price)} o menos\n\n"
                    f"{url}"
                )

                send_telegram(message)
                results.append(f"✅ Aviso enviado: {name} {format_clp(price)}")
            else:
                results.append(f"Sin oferta: {name} {format_clp(price)}")

        except Exception as e:
            results.append(f"❌ Error revisando {name}: {e}")

    print("\n".join(results))


if __name__ == "__main__":
    main()