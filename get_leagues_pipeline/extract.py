import cloudscraper
from bs4 import BeautifulSoup


def extract_top_five_leagues(url: str) -> list[dict]:
    scraper = cloudscraper.create_scraper(
        browser={
            "browser": "chrome",
            "platform": "windows",
            "desktop": True
        }
    )

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://fbref.com/",
    }
    response = scraper.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

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
                    "fbref_url": "https://fbref.com" + table_link["href"],
                    "league_country": league_country.get_text(strip=True),
                    "league_season": table_link.get_text(strip=True)[:9].strip()
                })

    return results


if __name__ == "__main__":
    leagues = extract_top_five_leagues("https://fbref.com/en/")
    for l in leagues:
        print(l)
