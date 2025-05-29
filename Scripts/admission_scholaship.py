import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import fitz  
from PIL import Image
import pytesseract

URLS = [
    "https://www.daiict.ac.in/undergraduate-admissions-all-india-category",
    "https://www.daiict.ac.in/undergraduate-admissions-gujarat-category",
    "https://www.daiict.ac.in/undergraduate-admissions-nri-and-foreign-national-category",
    "https://www.daiict.ac.in/btech-faq",
    "https://www.daiict.ac.in/mtech-ict-all-india-category",
    "https://www.daiict.ac.in/mtech-ict-gujarat-category",
    "https://www.daiict.ac.in/admission-msc-it",
    "https://www.daiict.ac.in/admissions-msc-agriculture-analytics",
    "https://www.daiict.ac.in/admission-msc-data-science",
    "https://www.daiict.ac.in/admissions-mdes",
    "https://www.daiict.ac.in/admission-phd",
    "https://www.daiict.ac.in/phd-rolling-admissions",
    "https://www.daiict.ac.in/visvesvaraya-phd-scheme",
    "https://www.daiict.ac.in/btech-institute-fellowships",
    "https://www.daiict.ac.in/btech-merit-and-mcm-scholarships",
    "https://www.daiict.ac.in/b-tech-dafs-merit-scholarships-da-iict",
    "https://www.daiict.ac.in/msc-it-scholarships",
    "https://www.daiict.ac.in/mdes-scholarship",
    "https://www.daiict.ac.in/da-iict-scholarships-msc-data-science-students",
    "https://www.daiict.ac.in/da-iict-scholarships-msc-agriculture-analytics-students",
    "https://www.daiict.ac.in/ugpg-cybage-khushboo-scholarships",
    "https://www.daiict.ac.in/jai-jhulelal-scholarships-btech-students",
    "https://www.daiict.ac.in/satnaam-waheguruji-scholarships-btech-students",
    "https://www.daiict.ac.in/financial-assistance-govt-gujarat",
    "https://www.daiict.ac.in/scholarships-offered-students"
]

OUTPUT_DIR = "scraped_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_filename(url):
    parsed = urlparse(url)
    name = parsed.path.replace("/", "_").strip("_")
    return f"{parsed.netloc}_{name or 'index'}"

def clean_text(raw_text):
    text = re.sub(r'\s+', ' ', raw_text)            
    text = re.sub(r'\n{2,}', '\n', text)             
    text = re.sub(r'[^\x00-\x7F]+', '', text)        
    return text.strip()

def extract_text_from_pdf_bytes(data):
    text = ""
    try:
        with fitz.open("pdf", data) as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        text += f"[ERROR extracting PDF: {e}]"
    return clean_text(text)

def extract_text_from_image_bytes(data):
    try:
        from io import BytesIO
        img = Image.open(BytesIO(data))
        return clean_text(pytesseract.image_to_string(img))
    except Exception as e:
        return f"[ERROR extracting image: {e}]"

def scrape_url(url):
    print(f"🔍 Scraping: {url}")
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.content, 'html.parser')

        raw_text = soup.get_text(separator='\n', strip=True)
        page_text = clean_text(raw_text)

        folder_name = clean_filename(url)
        folder_path = os.path.join(OUTPUT_DIR, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        with open(os.path.join(folder_path, "page.txt"), "w", encoding="utf-8") as f:
            f.write(page_text)

        doc_counter = 1
        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            if any(href.lower().endswith(ext) for ext in ['.pdf', '.jpg', '.jpeg', '.png']):
                file_url = urljoin(url, href)
                file_data = requests.get(file_url, timeout=10).content

                if href.lower().endswith(".pdf"):
                    extracted = extract_text_from_pdf_bytes(file_data)
                else:
                    extracted = extract_text_from_image_bytes(file_data)

                doc_filename = f"doc_{doc_counter}.txt"
                with open(os.path.join(folder_path, doc_filename), "w", encoding="utf-8") as f:
                    f.write(extracted)
                doc_counter += 1

    except Exception as e:
        print(f"❌ Failed to process {url}: {e}")

if __name__ == "__main__":
    for url in URLS:
        scrape_url(url)

    print("\n✅ All URLs processed. Clean text files are in the 'scraped_data' folder.")
