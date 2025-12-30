import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from firecrawl import Firecrawl

load_dotenv()


def get_team_players(url: str) -> list[dict]:
    """
    Extract players from an FBref league page.
    Returns player name + link to player page.
    """

    if not url:
        raise ValueError("URL must be provided")

    firecrawl = Firecrawl(api_key=os.getenv("FIRECRAWL_API_KEY"))

    # Scrape page
    scrape_result = firecrawl.scrape(url, formats=["html"])
    html_content = scrape_result.html

    soup = BeautifulSoup(html_content, "html.parser")

    players = []

    # Find the main stats table body
    table = soup.find("table", id="stats_standard_9")
    if not table:
        return players

    tbody = table.find("tbody")
    if not tbody:
        return players

    # Loop through each player row
    for row in tbody.find_all("tr"):
        player_cell = row.find("th", {"data-stat": "player"})
        if not player_cell:
            continue

        player_link = player_cell.find("a")
        if not player_link:
            continue

        players.append({
            "player_name": player_link.get_text(strip=True),
            "fbref_url": "https://fbref.com" + player_link["href"]
        })

    return players


if __name__ == "__main__":
    players = get_team_players(
        "https://fbref.com/en/squads/cff3d9bb/Chelsea-Stats"
    )

    for p in players:
        print(p)
