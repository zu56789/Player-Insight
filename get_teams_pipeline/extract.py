import cloudscraper
from bs4 import BeautifulSoup


def get_league_teams(url: str) -> dict:
    """Function to extract team names and their links from a league page on FBref."""

    if not url:
        raise ValueError("URL must be provided")

    scraper = cloudscraper.create_scraper()

    response = scraper.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Find the caption that contains the league name followed by " Table"
    caption = soup.find(
        "caption", string=lambda text: text and text.endswith("Table"))

    if not caption:
        raise ValueError("Could not find the teams table caption")

    league_name = caption.get_text(strip=True).replace(" Table", "").title()

    table = caption.find_parent("table")
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
    url = "https://fbref.com/en/comps/13/Ligue-1-Stats"
    teams = get_league_teams(url)
    for team, link in teams.items():
        print(f"{team}: {link}")
