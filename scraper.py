import requests
from bs4 import BeautifulSoup

def scrape_website(url: str):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        title = soup.title.string if soup.title else "No title found"
        meta_description = ""
        description_tag = soup.find("meta", attrs={"name": "description"})
        if description_tag and "content" in description_tag.attrs:
            meta_description = description_tag["content"]

        return {
            "url": url,
            "title": title,
            "meta_description": meta_description
        }
    except Exception as e:
        return {"error": str(e)}
