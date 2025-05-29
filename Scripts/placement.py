import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PIL import Image
import pytesseract

os.makedirs("images/bar_charts", exist_ok=True)
os.makedirs("images/company_logos", exist_ok=True)

url = "https://www.daiict.ac.in/placements"
headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

full_text = []

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    main_container = soup.find("div", class_="region-content")
    if main_container:
        for tag in main_container.find_all(["h1", "h2", "h3", "p", "li", "table"]):
            if tag.name == "table":
                rows = tag.find_all("tr")
                for row in rows:
                    cells = row.find_all(["td", "th"])
                    row_text = "\t".join(cell.get_text(strip=True) for cell in cells)
                    full_text.append(row_text)
            else:
                full_text.append(tag.get_text(strip=True))

    img_tags = soup.find_all("img")

    for img in img_tags:
        img_url = img.get("src")
        if not img_url:
            continue

        full_img_url = urljoin(url, img_url)
        filename = os.path.basename(img_url.split("?")[0])

        if "recruiters" in img_url.lower() or "companies" in img_url.lower():
            folder = "images/company_logos"
        elif "bar" in img_url.lower() or "stats" in img_url.lower() or "placement" in img_url.lower():
            folder = "images/bar_charts"
        else:
            continue

        save_path = os.path.join(folder, filename)

        try:
            img_data = requests.get(full_img_url).content
            with open(save_path, "wb") as f:
                f.write(img_data)
            print(f"✅ Downloaded: {save_path}")

            img = Image.open(save_path)
            text = pytesseract.image_to_string(img)
            if text.strip():
                full_text.append(f"\n[OCR from image: {filename}]\n{text.strip()}")
        except Exception as e:
            print(f"❌ Failed to process image {full_img_url}: {e}")

else:
    print(f"❌ Failed to fetch page. Status: {response.status_code}")

with open("daiict_placement_full_text.txt", "w", encoding="utf-8") as f:
    for line in full_text:
        f.write(line + "\n")

print("All content (text + OCR) saved to 'daiict_placement_full_text.txt'")
