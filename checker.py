import os
import re
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

TARGET_PRICE = 599990

PRODUCTS = [
    {
        "name": "PS5 Falabella - Standard GT7 Sony 1TB",
        "url": "https://www.falabella.com/falabella-cl/product/80648267/Consola-PS5-HW-Standard-GT7-Sony/80648267",
    },
    # Agrega más links aquí después:
    # {
    #     "name": "PS5 Paris",
    #     "url": "PEGAR_LINK_PARIS",
    # },
    # {
    #     "name": "PS5 Lider",
    #     "url": "PEGAR_LINK_LIDER",
    # },
]


def parse_price(text: str):
    """
    Busca precios chilenos tipo $719.990 o 719.990.
    Retorna int: 719990.
    """
    matches = re.findall(r"\$?\s?(\d{1,3}(?:\.\d{3})+)", text)
    prices = []

    for match in matches:
        price = int(match.replace(".", ""))
        if 300000 <= price <= 1000000:
            prices.append(price)

    if not prices:
        return None

    return min(prices)


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

        page.goto(url, wait_until="networkidle", timeout=60000)
        page.wait_for_timeout(5000)

        text = page.inner_text("body")
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

        try:
            text = get_page_text_with_playwright(url)
            price = parse_price(text)

            if price is None:
                results.append(f"⚠️ No pude leer precio: {name}\n{url}")
                continue

            print(f"{name}: ${price:,}".replace(",", "."))

            if price <= TARGET_PRICE:
                message = (
                    f"🚨 PS5 EN OFERTA\n\n"
                    f"{name}\n"
                    f"Precio detectado: ${price:,}\n"
                    f"Objetivo: ${TARGET_PRICE:,} o menos\n\n"
                    f"{url}"
                ).replace(",", ".")

                send_telegram(message)
                results.append(f"✅ Aviso enviado: {name} ${price}")
            else:
                results.append(f"Sin oferta: {name} ${price}")

        except Exception as e:
            results.append(f"❌ Error revisando {name}: {e}")

    print("\n".join(results))


if __name__ == "__main__":
    main()