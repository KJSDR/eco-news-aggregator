import requests
from bs4 import BeautifulSoup
from database import SessionLocal, Article

NEWS_SOURCES = [
    "https://www.bbc.com/news/science_and_environment",
    "https://www.nationalgeographic.com/environment",
]

# Define list of words to filter irrelevant articles
EXCLUDED_TITLES = ["Environment", "load more"]

def fetch_articles():
    session = SessionLocal()
    articles = []

    for source in NEWS_SOURCES:
        response = requests.get(source)
        print(f"Fetching from {source} - Status Code: {response.status_code}")

        soup = BeautifulSoup(response.text, "html.parser")

        if "bbc.com" in source:
            for item in soup.find_all("a", class_="ssrcss-afqep1-PromoLink exn3ah91"):
                title = item.get_text(strip=True)
                link = item.get("href", "")

                if title and link.startswith("/news"):
                    full_link = f"https://www.bbc.com{link}"

                    # **Filter out irrelevant titles**
                    if title in EXCLUDED_TITLES:
                        continue

                    existing_article = session.query(Article).filter(Article.link == full_link).first()
                    if not existing_article:
                        new_article = Article(title=title, link=full_link)
                        session.add(new_article)
                        session.commit()

                    articles.append({"title": title, "link": full_link})

        elif "nationalgeographic.com" in source:
            for item in soup.find_all("a"):
                title = item.get_text(strip=True)
                link = item.get("href", "")

                if title and "environment" in link:
                    if title in EXCLUDED_TITLES:
                        continue

                    existing_article = session.query(Article).filter(Article.link == link).first()
                    if not existing_article:
                        new_article = Article(title=title, link=link)
                        session.add(new_article)
                        session.commit()

                    articles.append({"title": title, "link": link})

    session.close()
    return articles
