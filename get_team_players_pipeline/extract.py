import os
import time
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from firecrawl import Firecrawl
from firecrawl.v2.utils.error_handler import RateLimitError

load_dotenv()


def safe_scrape(firecrawl: Firecrawl, url: str):
    while True:
        try:
            return firecrawl.scrape(url, formats=["html"])
        except RateLimitError as e:
            print("Rate limited, sleeping 40 seconds...")
            time.sleep(40)


def get_team_players(team_name: str, url: str) -> list[dict]:
    """
    Extract players from an FBref league page.
    Returns player name + link to player page.
    """

    if not url:
        raise ValueError("URL must be provided")

    firecrawl = Firecrawl(api_key=os.getenv("FIRECRAWL_API_KEY"))

    scrape_result = safe_scrape(firecrawl, url)
    html_content = scrape_result.html

    soup = BeautifulSoup(html_content, "html.parser")

    players = []

    table = soup.find("table", id="stats_standard_9")
    if not table:
        return players

    tbody = table.find("tbody")
    if not tbody:
        return players

    for row in tbody.find_all("tr"):
        player_cell = row.find("th", {"data-stat": "player"})
        if not player_cell:
            continue

        player_link = player_cell.find("a")
        if not player_link:
            continue

        players.append({
            "player_name": player_link.get_text(strip=True),
            "team_name": team_name,
            "fbref_url": player_link["href"]
        })

    return players


def get_player_details(player_name: str, team_name: str, url: str) -> dict:
    """Extract player information from an FBref player page."""

    if not url:
        raise ValueError("URL must be provided")

    firecrawl = Firecrawl(api_key=os.getenv("FIRECRAWL_API_KEY"))

    scrape_result = safe_scrape(firecrawl, url)
    html_content = scrape_result.html

    soup = BeautifulSoup(html_content, "html.parser")

    info_div = soup.find("div", id="info")
    if not info_div:
        raise ValueError("Player info section not found")

    player_data = {
        "player_name": player_name,
        "player_position": "Unknown",
        "player_nationality": "Unknown",
        "player_dob": "Unknown",
        "player_height": "Unknown",
        "player_strong_foot": "Unknown",
        "team_name": team_name,
        "fbref_url": url

    }

    for p in info_div.find_all("p"):
        strong_tags = p.find_all("strong")
        for strong in strong_tags:
            label = strong.get_text(strip=True)

            if label == "Position:":
                player_data["player_position"] = strong.next_sibling.strip().replace(
                    "\xa0▪", "").strip()

            if label == "Footed:":
                player_data["player_strong_foot"] = strong.next_sibling.strip()

            if "National" in label:
                country_link = p.find("a").get_text(strip=True)
                player_data["player_nationality"] = country_link

    height_span = info_div.find("span", string=lambda x: x and "cm" in x)
    if height_span:
        player_data["player_height"] = height_span.get_text(
            strip=True).replace("cm", "").strip()

    birth_span = info_div.find("span", id="necro-birth")
    if birth_span:
        player_data["player_dob"] = birth_span.get("data-birth")

    return player_data


if __name__ == "__main__":
    players = get_team_players(
        "Chelsea", "https://fbref.com/en/squads/cff3d9bb/Chelsea-Stats"
    )

    if players:
        for player in players[-10:-9]:

            details = get_player_details(
                player["player_name"], player["team_name"], player["fbref_url"]
            )
            print(details)
