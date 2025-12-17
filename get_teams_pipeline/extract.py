import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from firecrawl import Firecrawl

load_dotenv()  # Load environment variables from .env file


def get_league_teams(url: str) -> list[dict]:
    """Function to extract team names and their links from a league page on FBref."""

    firecrawl = Firecrawl(api_key=os.getenv("FIRECRAWL_API_KEY"))

    if not url:
        raise ValueError("URL must be provided")

    # Scrape the page using Firecrawl
    scrape_result = firecrawl.scrape(url, formats=["html"])
    html_content = scrape_result.html

    soup = BeautifulSoup(html_content, "html.parser")

    # Find the caption that contains the league name followed by " Table"
    caption = soup.find(
        "caption", string=lambda text: text and text.endswith("Table"))

    if not caption:
        raise ValueError("Could not find the teams table caption")

    league_name = caption.get_text(strip=True).replace(" Table", "").title()

    table = caption.find_parent("table")
    if not table:
        raise ValueError(f"Could not find the teams table for {league_name}")

    teams = []
    tbody = table.find("tbody")

    for row in tbody.find_all("tr"):
        team_cell = row.find("a")
        # Ensure it's a team link and not a redirected link
        if team_cell and "/squads/" in team_cell['href']:
            teams.append({
                "team_name": team_cell.text.strip(),
                "fbref_url": team_cell['href'],
                "league_name": league_name
            })
        else:
            raise ValueError("Team link not found in the expected format")

    return teams


if __name__ == "__main__":
    url = "https://fbref.com/en/comps/13/Ligue-1-Stats"
    teams = get_league_teams(url)
    for team in teams:
        print(team)
