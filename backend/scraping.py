import requests
from bs4 import BeautifulSoup
from database import SessionLocal, Article

# Define news sources with logos
NEWS_SOURCES = [
    {
        "name": "BBC News",
        "url": "https://www.bbc.com/news/science_and_environment",
        "logo": "/static/bbclogo.jpg",
        "required_url_part": "/news/science_and_environment"
    },
    {
        "name": "National Geographic",
        "url": "https://www.nationalgeographic.com/environment",
        "logo": "/static/natgeo.webp",
        "required_url_part": "/environment"
    }
]

def fetch_articles():
    session = SessionLocal()
    articles = []

    for source in NEWS_SOURCES:
        response = requests.get(source["url"])
        print(f"Fetching from {source['url']} - Status Code: {response.status_code}")

        if response.status_code != 200:
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract articles for BBC
        if "bbc.com" in source["url"]:
            article_elements = soup.find_all("a", class_="ssrcss-a4w391-PromoLink exn3ah92")

        # Extract articles for National Geographic
        elif "nationalgeographic.com" in source["url"]:
            article_elements = soup.find_all("a")

        for item in article_elements:
            title = item.get_text(strip=True)
            link = item.get("href", "")

            # Ensure link is absolute for BBC
            if link.startswith("/news"):
                link = f"https://www.bbc.com{link}"

            # **Only Keep Articles from the Correct Section**
            if source["required_url_part"] not in link:
                continue  # Skip articles that aren't in the correct section

            # Ignore invalid links
            if not title or not link.startswith("http"):
                continue

            # **Check if article already exists**
            existing_article = session.query(Article).filter(Article.link == link).first()
            if not existing_article:
                new_article = Article(
                    title=title,
                    link=link,
                    source_name=source["name"],
                    source_logo=source["logo"]
                )
                session.add(new_article)
                session.commit()

            articles.append({
                "title": title,
                "link": link,
                "source_name": source["name"],
                "source_logo": source["logo"]
            })

    session.close()
    return articles
