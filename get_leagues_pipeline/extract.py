import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from firecrawl import Firecrawl

load_dotenv()  # Load environment variables from .env file
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")


def extract_top_five_leagues(url: str) -> list[dict]:
    """Extract the top five football leagues from the given URL."""

    firecrawl = Firecrawl(api_key=FIRECRAWL_API_KEY)

    # Scrape the page using Firecrawl
    scrape_result = firecrawl.scrape(url, formats=["html"])
    html_content = scrape_result.html

    soup = BeautifulSoup(html_content, "html.parser")

    leagues_primary = soup.find(id="leagues_primary")
    if not leagues_primary:
        return []

    results = []
    top_five_leagues = ["Premier League", "La Liga",
                        "Bundesliga", "Serie A", "Ligue 1"]

    for div in leagues_primary.find_all("div", id=lambda x: x and x.startswith("mini-")):
        league_country = div.find("a", href=lambda x: x and "/country/" in x)
        if not league_country:
            continue

        table_link = div.find("a", href=lambda x: x and "/comps/" in x)

        caption = None
        if table_link:
            caption_tag = div.find_next("caption")
            if caption_tag:
                caption = caption_tag.get_text(strip=True)

        if table_link and caption:
            # check if caption is a substring of any of the top five leagues
            if any(top_league in caption for top_league in top_five_leagues):

                results.append({
                    "league_name": caption,
                    "fbref_url": table_link["href"],
                    "league_country": league_country.get_text(strip=True),
                    "league_season": table_link.get_text(strip=True)[:9].strip()
                })

    return results


if __name__ == "__main__":
    leagues = extract_top_five_leagues("https://fbref.com/en/")
    for l in leagues:
        print(l)
