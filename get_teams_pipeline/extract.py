import cloudscraper
from bs4 import BeautifulSoup


def get_league_teams(url: str, league_name: str) -> dict:
    """Function to extract team names and their links from a league page on FBref."""

    if not url or not league_name:
        raise ValueError("Both url and league_name must be provided")

    scraper = cloudscraper.create_scraper()

    response = scraper.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find(
        "caption", string=f"{league_name} Table").find_parent("table")
    if not table:
        raise ValueError(f"Could not find the teams table for {league_name}")

    teams = {}
    tbody = table.find("tbody")

    for row in tbody.find_all("tr"):
        team_cell = row.find("a")
        if team_cell:
            teams[team_cell.text.strip()] = "https://fbref.com" + \
                team_cell['href']

    return teams


if __name__ == "__main__":
    url = "https://fbref.com/en/comps/13/2025-2026-Ligue-1-Stats"
    league_name = "Ligue 1"
    teams = get_league_teams(url, league_name)
    for team, link in teams.items():
        print(f"{team}: {link}")
