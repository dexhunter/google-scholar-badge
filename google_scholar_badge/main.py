from fastapi import FastAPI
import httpx
from bs4 import BeautifulSoup
import uvicorn  # For running the server

app = FastAPI()


async def get_citation_number(url: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the citation number (adapt if the structure changes)
        citation_element = soup.find('td', {'class': 'gsc_rsb_std'})
        if citation_element:
            return citation_element.text.strip()  # Strip any extra whitespace
        return None


@app.get("/citations")
async def get_citations(user: str):
    url = f"https://scholar.google.com/citations?user={user}"
    citation_count = await get_citation_number(url)

    if citation_count:
        return {
            "schemaVersion": 1,
            "label": "Citations",
            "message": citation_count,
            "style": "social",
            "namedLogo": "Google Scholar"
        }
    else:
        return {
            "schemaVersion": 1,
            "label": "Citations",
            "message": 0,
            "style": "social",
            "namedLogo": "Google Scholar"
        }


# Ensure this block works properly
if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
