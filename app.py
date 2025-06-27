from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, HttpUrl
import requests
from bs4 import BeautifulSoup
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(title="Advanced Website Scraper", version="1.0.0")

class ScrapeRequest(BaseModel):
    url: HttpUrl

class ScrapeResult(BaseModel):
    title: str
    description: str
    links: list[str]

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": str(exc)}
    )

@app.post("/scrape", response_model=ScrapeResult)
def scrape_website(request: ScrapeRequest):
    try:
        response = requests.get(request.url, timeout=10)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to retrieve the webpage.")
        
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.title.string.strip() if soup.title and soup.title.string else "No title found"
        
        # Description meta tag
        description = ""
        desc_tag = soup.find("meta", attrs={"name": "description"})
        if desc_tag and desc_tag.get("content"):
            description = desc_tag["content"].strip()
        else:
            description = "No description found"

        # All links (cleaned)
        links = []
        for a_tag in soup.find_all("a", href=True):
            href = a_tag.get("href")
            if href and href.startswith(("http://", "https://")):
                links.append(href)

        return {
            "title": title,
            "description": description,
            "links": list(set(links))[:50]  # Return max 50 unique links
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scraping failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
