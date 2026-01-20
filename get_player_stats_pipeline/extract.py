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
