import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://en.wikipedia.org/wiki/"
OUTPUT_CSV = "movies_dataset.csv"
IMAGE_DIR = "images"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/125.0 Safari/537.36"
    )
}

os.makedirs(IMAGE_DIR, exist_ok=True)


def get_budget_and_poster(movie_url, year, title):
    budget_raw = None
    img_path = None
    try:
        resp = requests.get(movie_url, headers=HEADERS, timeout=10)
        if resp.status_code != 200:
            return budget_raw, img_path
        soup = BeautifulSoup(resp.text, "html.parser")
        infobox = soup.find("table", {"class": "infobox"})
        if not infobox:
            return budget_raw, img_path

        for row in infobox.find_all("tr"):
            header = row.find("th")
            if header and "budget" in header.get_text(strip=True).lower():
                cell = row.find("td")
                if cell:
                    budget_raw = cell.get_text(" ", strip=True)

        img_tag = infobox.find("img")
        if img_tag:
            img_url = urljoin("https:", img_tag.get("src"))
            try:
                img_data = requests.get(img_url, headers=HEADERS, timeout=10).content
                img_filename = f"{year}_{title.replace(' ', '_')}.jpg"
                img_path = os.path.join(IMAGE_DIR, img_filename)
                with open(img_path, "wb") as f:
                    f.write(img_data)
            except:
                pass
    except:
        pass
    return budget_raw, img_path


def scrape_highest_grossing(soup, year):
    tables = soup.find_all("table", {"class": "wikitable"})
    target_table = None
    for t in tables:
        caption = t.find("caption")
        if caption and "Highest-grossing films" in caption.get_text():
            target_table = t
            break
    if not target_table:
        return []

    data = []
    for row in target_table.find_all("tr")[1:]:
        cols = row.find_all(["td", "th"])
        if len(cols) < 2:
            continue

        title_cell = cols[1]
        title = title_cell.get_text(strip=True)
        link_tag = title_cell.find("a")
        movie_url = urljoin(BASE_URL, link_tag["href"]) if link_tag else None

        box_office_raw = cols[-1].get_text(strip=True)
        budget_raw, img_path = get_budget_and_poster(movie_url, year, title) if movie_url else (None, None)

        data.append({
            "title": title,
            "year": year,
            "budget_raw": budget_raw,
            "box_office_raw": box_office_raw,
            "release_date": None,
            "section": "Highest-grossing",
            "image": img_path
        })
    return data


def scrape_notable_releases(soup, year):
    data = []
    heading = soup.find(id="Notable_films_released")
    if not heading:
        return data

    for sib in heading.find_all_next(["table", "h2"]):
        if sib.name == "h2":
            break
        if sib.name == "table" and "wikitable" in sib.get("class", []):
            for row in sib.find_all("tr")[1:]:
                cols = row.find_all("td")
                if len(cols) < 2:
                    continue
                title_cell = cols[0]
                title = title_cell.get_text(strip=True)
                link_tag = title_cell.find("a")
                movie_url = urljoin(BASE_URL, link_tag["href"]) if link_tag else None

                release_date = cols[1].get_text(strip=True) if len(cols) > 1 else None
                budget_raw, img_path = get_budget_and_poster(movie_url, year, title) if movie_url else (None, None)

                data.append({
                    "title": title,
                    "year": year,
                    "budget_raw": budget_raw,
                    "box_office_raw": None,
                    "release_date": release_date,
                    "section": "Notable release",
                    "image": img_path
                })
    return data

#After EDA analysis i want to mention one thing that code of scrape_notable_releases is redundant as the data of this function is not in proper format
# so even if we remove it it will not affect the final result


def scrape_year(year):
    url = f"{BASE_URL}{year}_in_film"
    print(f"Scraping: {url}")
    resp = requests.get(url, headers=HEADERS, timeout=10)
    if resp.status_code != 200:
        print(f"Failed for {year}")
        return []

    soup = BeautifulSoup(resp.text, "html.parser")
    data = []
    data.extend(scrape_highest_grossing(soup, year))
    data.extend(scrape_notable_releases(soup, year))
    return data


def main():
    all_data = []
    for year in range(1900, 2025):
        year_data = scrape_year(year)
        all_data.extend(year_data)

    df = pd.DataFrame(all_data)
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved {len(df)} rows to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
