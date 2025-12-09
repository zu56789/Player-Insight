import cloudscraper
from bs4 import BeautifulSoup


def extract_leagues(url: str) -> list[dict]:
    scraper = cloudscraper.create_scraper()
    response = scraper.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.prettify()


if __name__ == "__main__":
    url = "https://fbref.com/"
    html_content = extract_leagues(url)
    print(html_content)
